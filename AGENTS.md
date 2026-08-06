# Public Agent Skills Repository Instructions

This public repository contains only skills authored or intentionally maintained
by us. Do not copy unchanged third-party skills here merely because they are
installed or allowlisted elsewhere.

- Keep each source at `skills/<name>/SKILL.md` with matching directory and
  frontmatter names.
- Use `giacus` as the public author identity.
- Never commit credentials, personal email addresses, machine-local paths,
  private repository names, confidential data, authenticated response bodies,
  or generated installation state.
- Preserve attribution and required license notices for any intentionally
  divergent maintained fork.
- Run `./scripts/validate-skills.sh` and review the complete diff after changes.
