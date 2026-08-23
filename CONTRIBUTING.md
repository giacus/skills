# Contributing

## Add or Change a Skill

1. Create `skills/<skill-name>/SKILL.md` using lowercase letters, digits, and
   hyphens. Keep the folder name identical to frontmatter `name`.
2. Put activation guidance in the frontmatter `description` and keep the body
   focused on instructions an agent cannot cheaply infer.
3. Add only resources the skill uses. Link references with relative paths.
4. Document required tools and any harness-specific behavior.
5. Review scripts and mark directly executable files executable.
6. Add or update the skill's row in the README `Available Skills` inventory,
   linking exactly to `skills/<skill-name>/SKILL.md`.
7. Run `./scripts/validate-skills.sh` before opening a pull request.

The README inventory is validated against the skill frontmatter: every skill
must appear exactly once, with the matching name and canonical link target.

Do not commit credentials, confidential data, copied third-party skills, generated
installation state, or project-specific rules that belong in the project itself.

## Third-Party Derivatives

Prefer a direct upstream dependency. If an intentional fork is necessary, rename
the skill to prevent collisions, retain attribution and required license files,
and document the upstream repository, original skill name, and reason for the
fork.

## Pull Requests

Explain the activation behavior, user-facing change, tools or permissions needed,
security considerations, and validation performed. Do not execute arbitrary skill
scripts in CI unless they have explicit tests and a controlled environment.
