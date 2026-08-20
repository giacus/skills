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
- Run validation locally before pushing. GitHub Actions must remain
  `workflow_dispatch`-only and is an optional remote safety signal.
- Before an explicitly authorized merge, run the validation command above and
  inspect the proposed diff. Any validation expected to exceed five minutes
  requires an advance duration warning and explicit owner consent; still-valid
  evidence may be reused for unchanged expensive surfaces when stated.
