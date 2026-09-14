# Agent Skills

[![Validate skills](https://github.com/giacus/skills/actions/workflows/validate.yml/badge.svg)](https://github.com/giacus/skills/actions/workflows/validate.yml)
[![skills.sh](https://skills.sh/b/giacus/skills)](https://skills.sh/giacus/skills)

Security-conscious, portable Agent Skills published by
[@giacus](https://github.com/giacus). This repository contains public skill
source that you can read, review, and install directly with the standard
`skills/<name>/SKILL.md` layout.

## Available Skills

| Skill | Purpose | Example prompt |
| --- | --- | --- |
| [`audit-agent-skill`](skills/audit-agent-skill/SKILL.md) | Review a skill repository before installing, updating, forking, or allowlisting it. | "Use `audit-agent-skill` to review these upstream skills before I install them." |
| [`write-durable-code-comments`](skills/write-durable-code-comments/SKILL.md) | Experimentally preserve verified, otherwise invisible local invariants during implementation. | "Use `write-durable-code-comments` while implementing this change, then report retained comments for review." |
| [`focused-code-review`](skills/focused-code-review/SKILL.md) | Review changes against repository standards and the available specification. | "Use `focused-code-review` for this task." |
| [`focused-debugging`](skills/focused-debugging/SKILL.md) | Diagnose uncertain bugs and performance regressions using representative evidence. | "Use `focused-debugging` for this task." |
| [`behavioral-tdd`](skills/behavioral-tdd/SKILL.md) | Implement explicitly requested test-first work through public interfaces. | "Use `behavioral-tdd` for this task." |
| [`find-agent-skills`](skills/find-agent-skills/SKILL.md) | Find suitable agent skills for an explicit discovery request or capability gap. | "Use `find-agent-skills` for this task." |
| [`portless-workflows`](skills/portless-workflows/SKILL.md) | Configure and troubleshoot named local development URLs. | "Use `portless-workflows` for this task." |

## Maintained Derivatives

These renamed skills intentionally diverge from reviewed upstream snapshots so
their activation and operating boundaries fit this shared cross-project setup:

| Maintained skill | Upstream source and original skill | Intentional divergence |
| --- | --- | --- |
| `focused-code-review` | `mattpocock/skills` `code-review` at `5c89081d4bbeb3d039a42093653f90bb698d780e` | Resolve the baseline from supplied context, include work-in-progress files, and continue standards review without requiring external issue-tracker setup. |
| `focused-debugging` | `mattpocock/skills` `diagnosing-bugs` at `321658273cb1d20b76026717d027d505790106d4` | Keep reproduction evidence central while allowing labelled source analysis when a runnable loop is unavailable; rank evidence-supported hypotheses and minimise proportionately. |
| `behavioral-tdd` | `mattpocock/skills` `tdd` at `321658273cb1d20b76026717d027d505790106d4` | Activate for explicit TDD or test-first work, not every integration-test request, and reuse established public seams without redundant confirmation. |
| `find-agent-skills` | `vercel-labs/skills` `find-skills` at `773fb2c7bbf16781670a3520affc4abd0c6151ae` | Require explicit discovery intent or a concrete capability gap, and separate discovery from installation authority. |
| `portless-workflows` | `vercel-labs/portless` `portless` at `2e87792c0da55ee514ce1d566045877f6d86cc24` | Split the monolithic guide into selective references and add approval boundaries without removing operational coverage. |

The original licenses and attribution are retained with each maintained skill.

Read a skill's `SKILL.md` and adjacent files before installing it. Skills are
operational instructions for an agent and should be treated as executable
supply-chain content.

## Preview

List the skills discovered by the CLI without installing them:

```bash
npx --yes skills@latest add giacus/skills --list
```

## Install

Open the interactive installer:

```bash
npx skills@latest add giacus/skills
```

Install one skill globally for Codex:

```bash
npx --yes skills@latest add giacus/skills \
  --global \
  --yes \
  --agent codex \
  --skill audit-agent-skill
```

Install every skill globally for Codex, Claude Code, Cursor, and Pi:

```bash
npx --yes skills@latest add giacus/skills \
  --global \
  --yes \
  --agent codex \
  --agent claude-code \
  --agent cursor \
  --agent pi \
  --skill '*'
```

The current CLI identifiers above are `codex`, `claude-code`, `cursor`, and
`pi`. The CLI manages each harness's installation path and symlinks. Use its
inventory rather than assuming a particular filesystem layout:

```bash
npx skills@latest list --global
```

See the
[`skills` CLI supported-agent table](https://github.com/vercel-labs/skills#supported-agents)
for other harnesses and current target paths.

## Requirements

- Node.js 22.20.0 or newer, as currently required by `skills@latest`;
- Git;
- npm's `npx` command.

Check the installed versions before troubleshooting discovery or installation:

```bash
node --version
git --version
npx --version
```

Repository validation additionally requires Bash, Python 3.10 or newer, and
PyYAML. CI uses Python 3.12 and pins PyYAML 6.0.2.

## Portability

The `SKILL.md` files are the portable source of truth. Optional
`agents/openai.yaml` files provide presentation and invocation metadata for
Codex; they do not replace `SKILL.md`, grant runtime permissions, or affect
harnesses that ignore them.

## Security

Review the complete selected payload before installation. Never put tokens,
passwords, private keys, API credentials, production secrets, personal data, or
machine-local configuration in a public skill.

See [SECURITY.md](SECURITY.md) for private vulnerability reporting. Repository
validation is a baseline only; it does not prove that operational instructions
are safe.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Add each skill at
`skills/<skill-name>/SKILL.md`, keep the directory name equal to frontmatter
`name`, and run:

```bash
./scripts/validate-skills.sh
```

Project-specific workflows belong in the relevant project repository.
Third-party skills remain upstream dependencies unless this repository
intentionally maintains a renamed, attributed fork.

## License

Repository-authored content is available under the [MIT License](LICENSE). A
maintained fork must also preserve its upstream notices and license obligations.
