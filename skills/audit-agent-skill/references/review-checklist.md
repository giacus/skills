# Third-Party Agent Skill Review Checklist

## Scope and provenance

- Resolve the canonical owner, repository, revision, and selected skill names.
- Confirm directory names match frontmatter names.
- Check recent maintenance, contributor concentration, signed or verified history,
  releases, and security reporting options.
- Read the governing license and retain required notices for any fork.

## Complete payload

- Read each selected `SKILL.md` from frontmatter through the final line.
- Resolve every relative reference and inspect every referenced file.
- Inventory scripts, binaries, symlinks, submodules, generated files, and remote
  downloads in the selected payload.
- Check for hidden Unicode controls and obvious embedded secrets.

## Behavior and permissions

- Identify shell execution, package installation, network access, browser or
  account access, credential requests, destructive commands, and production use.
- Treat tests, build tools, Git hooks, and historical commits as executable input.
- Check whether logs, traces, HAR files, screenshots, or prompts can disclose
  credentials, personal data, or proprietary context.
- Confirm dangerous actions are explicitly permission-gated.

## Portability and dependencies

- Separate standard Agent Skills behavior from harness-specific tools or metadata.
- Identify required commands, agents, companion skills, generated documents, MCP
  tools, environment variables, and assumed directory layouts.
- Test relative links and parse all YAML frontmatter.
- Validate shell syntax without executing arbitrary skill scripts.

## Verdict

- **Allow**: the reviewed revision has no material unresolved concern.
- **Conditional allow**: install only with named restrictions or missing optional
  capability understood.
- **Reject**: the payload, provenance, license, or requested permissions create an
  unacceptable unresolved risk.

Record the review date and revision. Review future upstream diffs before updating.
