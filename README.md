# Agent Skills

Portable, public Agent Skills authored or intentionally maintained by Giacomo Leo.
Each skill uses the standard `skills/<name>/SKILL.md` layout and can be consumed
without the private dotfiles toolkit.

## Install

Install interactively into the current project:

```bash
npx skills@latest add giacus/agent-skills
```

Install every skill globally for the supported harnesses:

```bash
npx --yes skills@latest add giacus/agent-skills \
  --global \
  --yes \
  --agent codex claude-code cursor pi \
  --skill '*'
```

Install one skill into the current project:

```bash
npx --yes skills@latest add giacus/agent-skills \
  --skill audit-agent-skill
```

Preview the skills discovered in this repository:

```bash
npx --yes skills@latest add giacus/agent-skills --list
```

`skills@1.5.21` requires Node.js 22.20.0 or newer. The public install also
requires Git and npm's `npx` command. Repository validation requires Bash,
Python 3.10 or newer, and PyYAML (CI pins PyYAML 6.0.2).

## Available Skills

| Skill | Purpose | Example prompt |
| --- | --- | --- |
| `audit-agent-skill` | Review a skill repository before installing, updating, forking, or allowlisting it. | "Use `audit-agent-skill` to review these three upstream skills before I add them globally." |
| `write-durable-code-comments` | Experimentally preserve verified, otherwise invisible local invariants during implementation. | "Use `write-durable-code-comments` while implementing this change, then report its proposed comments for review." |

## Harnesses and Installation State

The `SKILL.md` files are the portable source of truth. The bootstrap is tested
with the current `npx skills` identifiers `codex`, `claude-code`, `cursor`, and
`pi`. Other compatible harnesses can consume the same source format.

With the current CLI, shared global copies for Codex and Cursor are written to
`~/.agents/skills`. Claude Code and Pi receive harness-specific links under
`~/.claude/skills` and `~/.pi/agent/skills` when multi-agent symlink installation
is available. Treat `npx skills@latest list --global` as the authoritative
inventory because harness and CLI layouts can evolve.

The optional `agents/openai.yaml` files contain presentation metadata for Codex.
They do not replace `SKILL.md`, add runtime permissions, or affect harnesses that
ignore them.

## Security

Skills are executable supply-chain content: their instructions can cause an agent
to run bundled or repository code. Read the complete selected payload before
installation, use explicit allowlists for third-party collections, and never put
tokens, passwords, private keys, API credentials, or production secrets in Git.

See [SECURITY.md](SECURITY.md) for reporting concerns. Repository validation is a
baseline only; it does not prove that operational instructions are safe.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Add each skill at
`skills/<skill-name>/SKILL.md`, keep the directory name equal to frontmatter
`name`, and run:

```bash
./scripts/validate-skills.sh
```

Project-specific workflows belong in the relevant project repository. Third-party
skills remain upstream dependencies unless this repository intentionally maintains
a renamed, attributed fork.

## License

Repository-authored content is available under the [MIT License](LICENSE). A
maintained fork must also preserve its upstream notices and license obligations.
