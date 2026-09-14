<!-- Adapted from vercel-labs/portless; see ../LICENSE. -->

## Installation

Install globally (recommended) or as a project dev dependency. Do NOT use `npx` or `pnpm dlx` for one-off execution.

```bash
# Global (available everywhere)
npm install -g portless

# Or per-project dev dependency
npm install -D portless
```

When installed per-project, invoke via package.json scripts or `npx portless` (since the package is local, npx will not download anything).

## Quick Start

```bash
# Install globally (or add -D to a project)
npm install -g portless

# Run your app (auto-starts the HTTPS proxy on port 443)
portless run next dev
# -> https://<project>.localhost

# Or with an explicit name
portless myapp next dev
# -> https://myapp.localhost
```

The proxy auto-starts when you run an app. You can also start it explicitly with `portless proxy start`. Auto-start reuses the configuration (port, TLS, TLDs) from the most recent proxy run, so a restart or reboot does not silently revert to defaults. Explicit env vars always take priority.

In non-interactive environments (no TTY, or `CI=1`), portless exits with a descriptive error instead of prompting. Task runners like turborepo should pre-start the proxy.

## Integration Patterns

### Zero-config (recommended)

Bare `portless` works out of the box. It runs the `"dev"` script from `package.json` through the proxy, inferring the app name from the package name, git root, or directory:

```bash
portless        # -> runs "dev" script, https://<project>.localhost
pnpm dev        # -> works without portless, plain "next dev"
```

Use an optional `portless.json` to override defaults (name, script, port):

```json
{ "name": "myapp" }
```

```bash
portless        # -> runs "dev" script, https://myapp.localhost
```

### Monorepo

One `portless.json` at the repo root. Portless discovers packages from `pnpm-workspace.yaml`, or the `"workspaces"` field in `package.json` (npm, yarn, bun):

```json
{
  "apps": {
    "apps/web": { "name": "myapp" },
    "apps/api": { "name": "api.myapp" }
  }
}
```

```bash
portless                  # from repo root: start all packages with a "dev" script
cd apps/web && portless   # start just one package
portless --script start   # run "start" instead of "dev"
```

The `apps` map is optional and only provides name overrides. Unlisted packages auto-discover with inferred names.

Without an `apps` map, hostnames follow `<package>.<project>.localhost`. The project name comes from the most common npm scope (e.g. `@myorg/web` and `@myorg/api` produce `myorg`), falling back to the workspace root directory name. If a package's short name matches the project name, it uses the bare `<project>.localhost`.

### Turborepo

For turborepo projects, use portless as the `dev` script with the real command in a separate script:

```json
{
  "scripts": { "dev": "portless", "dev:app": "next dev" },
  "portless": { "name": "myapp", "script": "dev:app" }
}
```

`pnpm dev` runs turbo, which runs `portless` in each package. Portless detects the package manager and runs `pnpm run dev:app` through the proxy.

### package.json scripts

You can still use portless directly in scripts:

```json
{
  "scripts": {
    "dev": "portless run next dev"
  }
}
```

The proxy auto-starts when you run an app. Or start it explicitly: `portless proxy start`.

### Multi-app setups with subdomains

```bash
portless myapp next dev          # https://myapp.localhost
portless api.myapp pnpm start    # https://api.myapp.localhost
portless docs.myapp next dev     # https://docs.myapp.localhost
```

By default, only explicitly registered subdomains are routed (strict mode). Start the proxy with `--wildcard` to allow any subdomain of a registered route to fall back to that app (e.g. `tenant1.myapp.localhost` routes to the `myapp` app). Exact matches always take priority over wildcards.

### Git worktrees

`portless run` automatically detects git worktrees. In a linked worktree, the branch name is prepended as a subdomain prefix so each worktree gets a unique URL:

```bash
# Main worktree (no prefix)
portless run next dev   # -> https://myapp.localhost

# Linked worktree on branch "fix-ui"
portless run next dev   # -> https://fix-ui.myapp.localhost
```

No config changes needed. Put `portless run` in `package.json` once and it works in all worktrees.

### Bypassing portless

Set `PORTLESS=0` to run the command directly without the proxy:

```bash
PORTLESS=0 pnpm dev   # Bypasses proxy, uses default port
```
