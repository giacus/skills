#!/usr/bin/env python3
"""Validate portable Agent Skills without executing bundled skill code."""

from __future__ import annotations

import re
import stat
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
INLINE_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK_PATTERN = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
AVAILABLE_SKILLS_HEADING = re.compile(r"^## Available Skills\s*$", re.MULTILINE)
NEXT_HEADING = re.compile(r"^##\s+", re.MULTILINE)
INVENTORY_ROW_PATTERN = re.compile(r"^\s*\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|", re.MULTILINE)


def secret_patterns() -> list[tuple[str, re.Pattern[str]]]:
    """Construct signatures without embedding sample credentials in this file."""

    return [
        (
            "private key",
            re.compile("-" * 5 + r"BEGIN (?:(?:RSA|EC|OPENSSH|DSA) )?PRIVATE KEY"),
        ),
        (
            "GitHub token",
            re.compile(r"\b(?:gh" + r"[pousr])_[A-Za-z0-9]{30,}\b"),
        ),
        (
            "GitHub fine-grained token",
            re.compile(r"\bgithub_" + r"pat_[A-Za-z0-9_]{40,}\b"),
        ),
        (
            "AWS access key",
            re.compile(r"\bA" + r"KIA[0-9A-Z]{16}\b"),
        ),
        (
            "Slack token",
            re.compile(r"\bx" + r"ox[baprs]-[A-Za-z0-9-]{20,}\b"),
        ),
        (
            "Google API key",
            re.compile(r"\bAI" + r"za[0-9A-Za-z_-]{35}\b"),
        ),
        (
            "npm token",
            re.compile(r"\bnpm" + r"_[A-Za-z0-9]{36}\b"),
        ),
        (
            "live Stripe secret key",
            re.compile(r"\bsk_" + r"live_[A-Za-z0-9]{20,}\b"),
        ),
    ]


def add_error(errors: list[str], message: str) -> None:
    errors.append(message)


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, object] | None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        add_error(errors, f"{path.relative_to(REPO_ROOT)}: SKILL.md is not UTF-8")
        return None

    if not lines or lines[0] != "---":
        add_error(errors, f"{path.relative_to(REPO_ROOT)}: missing opening frontmatter delimiter")
        return None

    try:
        closing_index = lines[1:].index("---") + 1
    except ValueError:
        add_error(errors, f"{path.relative_to(REPO_ROOT)}: missing closing frontmatter delimiter")
        return None

    try:
        metadata = yaml.safe_load("\n".join(lines[1:closing_index]))
    except yaml.YAMLError as exc:
        add_error(errors, f"{path.relative_to(REPO_ROOT)}: invalid YAML frontmatter: {exc}")
        return None

    if not isinstance(metadata, dict):
        add_error(errors, f"{path.relative_to(REPO_ROOT)}: frontmatter must be a mapping")
        return None
    return metadata


def extract_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    return target.split(maxsplit=1)[0]


def has_symlink_component(path: Path, boundary: Path) -> bool:
    current = path
    while current != boundary:
        if current.is_symlink():
            return True
        current = current.parent
    return boundary.is_symlink()


def validate_markdown_file_links(
    markdown_path: Path,
    boundary: Path,
    errors: list[str],
) -> None:
    text = markdown_path.read_text(encoding="utf-8")
    raw_targets = INLINE_LINK_PATTERN.findall(text)
    raw_targets.extend(REFERENCE_LINK_PATTERN.findall(text))

    for raw_target in raw_targets:
        target = unquote(extract_link_target(raw_target))
        parsed = urlparse(target)
        if parsed.scheme or target.startswith(("#", "//")):
            continue
        relative_target = target.split("#", 1)[0]
        if not relative_target:
            continue
        if relative_target.startswith("/"):
            add_error(
                errors,
                f"{markdown_path.relative_to(REPO_ROOT)}: local link must be relative: {target}",
            )
            continue

        resolved = (markdown_path.parent / relative_target).resolve()
        try:
            resolved.relative_to(boundary.resolve())
        except ValueError:
            add_error(
                errors,
                f"{markdown_path.relative_to(REPO_ROOT)}: link escapes allowed boundary: {target}",
            )
            continue
        if not resolved.exists():
            add_error(
                errors,
                f"{markdown_path.relative_to(REPO_ROOT)}: missing linked file: {target}",
            )


def validate_markdown_links(skill_dir: Path, errors: list[str]) -> None:
    for markdown_path in sorted(skill_dir.rglob("*.md")):
        if has_symlink_component(markdown_path, skill_dir):
            continue
        validate_markdown_file_links(markdown_path, skill_dir, errors)


def validate_repository_markdown_links(errors: list[str]) -> None:
    for markdown_path in sorted(REPO_ROOT.rglob("*.md")):
        relative_parts = markdown_path.relative_to(REPO_ROOT).parts
        if ".git" in relative_parts or relative_parts[0] == "skills":
            continue
        if has_symlink_component(markdown_path, REPO_ROOT):
            continue
        validate_markdown_file_links(markdown_path, REPO_ROOT, errors)


def validate_readme_skill_inventory(discovered_names: set[str], errors: list[str]) -> None:
    """Require README's Available Skills table to be an exact skill index."""

    readme_path = REPO_ROOT / "README.md"
    try:
        text = readme_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        add_error(errors, f"README.md: cannot read skill inventory: {exc}")
        return

    heading = AVAILABLE_SKILLS_HEADING.search(text)
    if heading is None:
        add_error(errors, "README.md: missing '## Available Skills' inventory")
        return

    next_heading = NEXT_HEADING.search(text, heading.end())
    section = text[heading.end() : next_heading.start() if next_heading else len(text)]
    entries = INVENTORY_ROW_PATTERN.findall(section)

    listed_names: list[str] = []
    for label, raw_target in entries:
        name = label.strip().strip("`")
        target = unquote(extract_link_target(raw_target))
        listed_names.append(name)
        expected_target = f"skills/{name}/SKILL.md"
        if target != expected_target:
            add_error(
                errors,
                f"README.md: skill inventory target for '{name}' is '{target}', expected '{expected_target}'",
            )

    counts: dict[str, int] = {}
    for name in listed_names:
        counts[name] = counts.get(name, 0) + 1
    for name, count in sorted(counts.items()):
        if count > 1:
            add_error(errors, f"README.md: duplicate skill inventory entry '{name}' ({count} links)")

    listed = set(listed_names)
    for name in sorted(discovered_names - listed):
        add_error(errors, f"README.md: missing skill inventory entry '{name}'")
    for name in sorted(listed - discovered_names):
        add_error(errors, f"README.md: extra skill inventory entry '{name}'")


def validate_skills(errors: list[str]) -> set[str]:
    if not SKILLS_ROOT.is_dir():
        add_error(errors, "skills/: directory is missing")
        return set()

    skill_dirs = sorted(
        path
        for path in SKILLS_ROOT.iterdir()
        if path.is_dir() and not path.is_symlink() and not path.name.startswith(".")
    )
    if not skill_dirs:
        add_error(errors, "skills/: no skill directories found")
        return set()

    names: dict[str, Path] = {}
    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            add_error(errors, f"{skill_dir.relative_to(REPO_ROOT)}: SKILL.md is missing")
            continue
        if skill_md.is_symlink():
            continue

        metadata = parse_frontmatter(skill_md, errors)
        if metadata is None:
            continue
        name = metadata.get("name")
        description = metadata.get("description")
        if not isinstance(name, str) or not name.strip():
            add_error(errors, f"{skill_md.relative_to(REPO_ROOT)}: name is required")
        else:
            if not NAME_PATTERN.fullmatch(name) or len(name) > 64:
                add_error(errors, f"{skill_md.relative_to(REPO_ROOT)}: invalid skill name: {name}")
            if name != skill_dir.name:
                add_error(
                    errors,
                    f"{skill_md.relative_to(REPO_ROOT)}: name '{name}' does not match directory",
                )
            if name in names:
                first = names[name].relative_to(REPO_ROOT)
                add_error(errors, f"{skill_md.relative_to(REPO_ROOT)}: duplicate name '{name}' (first at {first})")
            else:
                names[name] = skill_md

        if not isinstance(description, str) or not description.strip():
            add_error(errors, f"{skill_md.relative_to(REPO_ROOT)}: description is required")
        elif len(description) > 1024:
            add_error(
                errors,
                f"{skill_md.relative_to(REPO_ROOT)}: description exceeds 1024 characters",
            )

        validate_markdown_links(skill_dir, errors)

    return set(names)


def repository_files() -> list[Path]:
    return sorted(
        path
        for path in REPO_ROOT.rglob("*")
        if path.is_file()
        and not path.is_symlink()
        and ".git" not in path.relative_to(REPO_ROOT).parts
    )


def validate_no_symlinks(errors: list[str]) -> None:
    for path in sorted(REPO_ROOT.rglob("*")):
        if ".git" in path.relative_to(REPO_ROOT).parts:
            continue
        if path.is_symlink():
            add_error(errors, f"{path.relative_to(REPO_ROOT)}: symbolic links are not allowed")


def validate_shell_scripts(files: list[Path], errors: list[str]) -> None:
    for path in files:
        if path.suffix not in {".sh", ".bash"}:
            continue
        result = subprocess.run(
            ["bash", "-n", str(path)],
            capture_output=True,
            check=False,
            text=True,
        )
        if result.returncode:
            detail = result.stderr.strip() or "bash -n failed"
            add_error(errors, f"{path.relative_to(REPO_ROOT)}: {detail}")


def validate_executable_bits(files: list[Path], errors: list[str]) -> None:
    for path in files:
        try:
            first_line = path.open("rb").readline(256)
        except OSError as exc:
            add_error(errors, f"{path.relative_to(REPO_ROOT)}: cannot read file: {exc}")
            continue
        if not first_line.startswith(b"#!"):
            continue
        mode = path.stat().st_mode
        if not mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
            add_error(errors, f"{path.relative_to(REPO_ROOT)}: shebang file is not executable")


def validate_yaml_files(files: list[Path], errors: list[str]) -> None:
    for path in files:
        if path.suffix not in {".yaml", ".yml"}:
            continue
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
            add_error(errors, f"{path.relative_to(REPO_ROOT)}: invalid YAML: {exc}")


def validate_unicode_controls(files: list[Path], errors: list[str]) -> None:
    control_pattern = re.compile(r"[\u202a-\u202e\u2066-\u2069]")
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        match = control_pattern.search(text)
        if match:
            line = text.count("\n", 0, match.start()) + 1
            add_error(errors, f"{path.relative_to(REPO_ROOT)}:{line}: hidden Unicode control")


def validate_secrets(files: list[Path], errors: list[str]) -> None:
    patterns = secret_patterns()
    assignment_prefix = r"(?:[A-Za-z][A-Za-z0-9]*[_-])*"
    assignment_key = assignment_prefix + r"(?:api[_-]?key|token|secret|password|private[_-]?key)"
    assignment_pattern = re.compile(
        r"\b" + assignment_key + r"\b\s*[:=]\s*['\"]?([^\s'\"#]{12,})",
        re.IGNORECASE,
    )
    placeholders = ("example", "placeholder", "redacted", "changeme", "your-", "<", "${")

    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        for label, pattern in patterns:
            match = pattern.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                add_error(errors, f"{path.relative_to(REPO_ROOT)}:{line}: possible {label}")

        for match in assignment_pattern.finditer(text):
            value = match.group(1).lower()
            if any(marker in value for marker in placeholders):
                continue
            line = text.count("\n", 0, match.start()) + 1
            add_error(errors, f"{path.relative_to(REPO_ROOT)}:{line}: possible assigned secret")


def validate_public_artifacts(files: list[Path], errors: list[str]) -> None:
    patterns = [
        (
            "personal email address",
            re.compile(
                r"\b[\w.+-]+@(?:gmail|icloud|outlook|hotmail|yahoo)\.[a-z]+\b",
                re.IGNORECASE,
            ),
        ),
        ("absolute macOS home path", re.compile(r"/Users/[A-Za-z0-9._-]+")),
        ("absolute Linux home path", re.compile(r"/home/[A-Za-z0-9._-]+")),
    ]
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        for label, pattern in patterns:
            match = pattern.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                add_error(
                    errors,
                    f"{path.relative_to(REPO_ROOT)}:{line}: public artifact violation ({label})",
                )


def validate_public_identity(errors: list[str]) -> None:
    requirements = {
        REPO_ROOT / "README.md": "[@giacus](https://github.com/giacus)",
        REPO_ROOT / "LICENSE": re.compile(
            r"^Copyright \(c\) \d{4}(?:-\d{4})? giacus$",
            re.MULTILINE,
        ),
    }
    for path, requirement in requirements.items():
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            add_error(errors, f"{path.relative_to(REPO_ROOT)}: cannot verify public identity: {exc}")
            continue

        matches = requirement in text if isinstance(requirement, str) else requirement.search(text)
        if not matches:
            add_error(errors, f"{path.relative_to(REPO_ROOT)}: public identity must use giacus")


def main() -> int:
    errors: list[str] = []
    validate_no_symlinks(errors)
    discovered_names = validate_skills(errors)
    validate_readme_skill_inventory(discovered_names, errors)
    validate_repository_markdown_links(errors)
    files = repository_files()
    validate_shell_scripts(files, errors)
    validate_executable_bits(files, errors)
    validate_yaml_files(files, errors)
    validate_unicode_controls(files, errors)
    validate_secrets(files, errors)
    validate_public_artifacts(files, errors)
    validate_public_identity(errors)

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    skill_count = sum(
        1
        for path in SKILLS_ROOT.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )
    print(f"Validated {skill_count} skill(s); no errors found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
