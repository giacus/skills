---
name: portless-workflows
description: Configure or troubleshoot named local development URLs with Portless. Use for .localhost routing, project integration, or explicit proxy, sharing, and startup-service work; not unrelated internal test or production ports.
license: Apache-2.0
---

<!-- Adapted from vercel-labs/portless; see LICENSE. -->

# Portless Workflows

Use named local URLs and the project's existing Portless setup. Read only the
reference needed for the current operation. Commands use the `portless` executable.

## Choose the needed reference

- For installation, project scripts, monorepos, Turborepo, worktree naming, or
  bypassing the proxy, read [integration](references/integration.md).
- For TLS, environment variables, LAN, Tailscale, or ngrok, read
  [proxy and sharing](references/proxy-and-sharing.md).
- For explicitly requested startup behavior, read
  [startup service](references/startup-service.md).
- For exact commands, configuration fields, or precedence, read
  [CLI and configuration](references/cli-and-config.md).
- For a routing or certificate failure, start with the read-only
  `portless doctor` command and load the relevant section of
  [troubleshooting](references/troubleshooting.md).

## Execution boundaries

Inspect the current routes and configuration before changing them. Preserve
project conventions and use `portless get <name>` or `PORTLESS_URL` for wiring
services rather than guessing their ports. Keep `PORTLESS=0` as the explicit
direct-server fallback. Do not replace internal test or production ports merely
because this skill is active.

Keep local development loopback-only and strict-routed unless broader access is
authorized. A command example is not permission to expose an app or change
machine configuration. Respect existing authorization and repository policy for
software installation, CA trust, `/etc/hosts`, privileged startup services, LAN
or public tunnels, forceful takeover, pruning, and cleanup. Complete safe
inspection first; ask only for a material action not already authorized.

Verify the requested route or operation and report the usable URL and any
remaining limitation. Running a local app does not authorize publishing it.

### Requirements

- Node.js 24+
- macOS, Linux, or Windows
- `openssl` (for `--https` cert generation; ships with macOS and most Linux distributions; on Windows, install via `winget install -e --id ShiningLight.OpenSSL.Dev` or use the copy bundled with Git for Windows)
- `tailscale` CLI (optional, for `--tailscale` and `--funnel`)
- `ngrok` CLI (optional, for `--ngrok`)
