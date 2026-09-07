<!-- Adapted from vercel-labs/portless; see ../LICENSE. -->

## CLI Reference

| Command                                           | Description                                                    |
| ------------------------------------------------- | -------------------------------------------------------------- |
| `portless`                                        | Run dev script through proxy                                   |
| `portless`                                        | From monorepo root: run all workspace packages                 |
| `portless --script <name>`                        | Run a specific package.json script (default: dev)              |
| `portless run [cmd] [args...]`                    | Infer name from project, run through proxy (auto-starts)       |
| `portless run --name <name> <cmd>`                | Override inferred base name (worktree prefix still applies)    |
| `portless <name> <cmd> [args...]`                 | Run app at `https://<name>.localhost` (auto-starts proxy)      |
| `portless get <name>`                             | Print URL for a service (for cross-service wiring)             |
| `portless get <name> --no-worktree`               | Print URL without worktree prefix                              |
| `portless list`                                   | Show active routes                                             |
| `portless doctor`                                 | Check proxy, routes, DNS, CA trust, and LAN prerequisites      |
| `portless trust`                                  | Add local CA to system trust store (for HTTPS)                 |
| `portless clean`                                  | Remove state, CA trust entry, and /etc/hosts block             |
| `portless prune`                                  | Kill orphaned dev servers from crashed sessions                |
| `portless prune --force`                          | Kill orphans with SIGKILL instead of SIGTERM                   |
| `portless proxy start`                            | Start HTTPS proxy as a daemon (port 443, auto-elevates)        |
| `portless proxy start --no-tls`                   | Start without HTTPS (plain HTTP on port 80)                    |
| `portless proxy start --lan`                      | Start in LAN mode (mDNS `.local`, auto-follows LAN IP changes) |
| `portless proxy start -p <number>`                | Start the proxy on a custom port                               |
| `portless proxy start --tld test`                 | Use .test instead of .localhost                                |
| `portless proxy start --tld localhost --tld test` | Serve both TLDs from one proxy                                 |
| `portless proxy start --tld dev.example.com`      | Use a multi-segment TLD for production-parity URLs             |
| `portless proxy start --foreground`               | Start the proxy in foreground (for debugging)                  |
| `portless proxy start --wildcard`                 | Allow unregistered subdomains to fall back to parent route     |
| `portless proxy stop`                             | Stop the proxy                                                 |
| `portless service install`                        | Start the HTTPS proxy when the OS starts                       |
| `portless service install --lan`                  | Start the service in LAN mode                                  |
| `portless service install --wildcard`             | Persist wildcard routing in the startup service                |
| `portless service status`                         | Show service and proxy status                                  |
| `portless service uninstall`                      | Remove the startup service                                     |
| `portless alias <name> <port>`                    | Register a static route (e.g. for Docker containers)           |
| `portless alias <name> <port> --force`            | Overwrite an existing route                                    |
| `portless alias --remove <name>`                  | Remove a static route                                          |
| `portless hosts sync`                             | Add routes to /etc/hosts (fixes Safari)                        |
| `portless hosts clean`                            | Remove portless entries from /etc/hosts                        |
| `portless <name> --app-port <n> <cmd>`            | Use a fixed port for the app instead of auto-assignment        |
| `portless <name> --tailscale <cmd>`               | Share the app on your Tailscale network (tailnet)              |
| `portless <name> --funnel <cmd>`                  | Share the app publicly via Tailscale Funnel                    |
| `portless <name> --ngrok <cmd>`                   | Share the app publicly via ngrok                               |
| `portless <name> --force <cmd>`                   | Kill the existing process and take over its route              |
| `portless --name <name> <cmd>`                    | Force `<name>` as app name (bypasses subcommand dispatch)      |
| `portless <name> -- <cmd> [args...]`              | Stop flag parsing; everything after `--` is passed to child    |
| `portless --help` / `-h`                          | Show help                                                      |
| `portless run --help`                             | Show help for a subcommand (also: alias, hosts, clean)         |
| `portless --version` / `-v`                       | Show version                                                   |

**Reserved names:** `run`, `get`, `alias`, `hosts`, `list`, `doctor`, `trust`, `clean`, `prune`, `proxy`, and `service` are subcommands and cannot be used as app names directly. Use `portless run <cmd>` to infer the name, or `portless --name <name> <cmd>` to force any name including reserved ones.

## portless.json

Optional config file. Portless looks for it in the current directory.

| Field     | Type    | Default                    | Description                                              |
| --------- | ------- | -------------------------- | -------------------------------------------------------- |
| `name`    | string  | inferred from package.json | Base app name (worktree prefix still applies)            |
| `script`  | string  | `"dev"`                    | Name of a package.json script to run                     |
| `appPort` | number  | auto-assigned              | Fixed port for the child process                         |
| `proxy`   | boolean | auto-detected              | Whether to route through the proxy (`false` for tasks)   |
| `apps`    | object  |                            | Overrides for workspace packages, keyed by relative path |
| `turbo`   | boolean | `true`                     | Set `false` to use direct spawning instead of turborepo  |

Each `apps` entry has the same shape (`name`, `script`, `appPort`, `proxy`). When `apps` is present, top-level fields apply only in single-app mode.

### package.json "portless" key

Instead of a separate `portless.json`, you can add a `"portless"` key to your `package.json`. A string value is shorthand for setting the name:

```json
{ "portless": "myapp" }
```

An object supports all per-app fields (`name`, `script`, `appPort`, `proxy`):

```json
{ "portless": { "name": "myapp", "script": "dev:app" } }
```

Precedence (closest wins): CLI flags > package.json `"portless"` key > portless.json app entry > defaults.
