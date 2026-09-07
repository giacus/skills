<!-- Adapted from vercel-labs/portless; see ../LICENSE. -->

## Troubleshooting

### Run diagnostics

Use `portless doctor` first when local routing or HTTPS behavior looks wrong. It is read-only and checks Node.js, state directory permissions, proxy liveness, route entries, hostname resolution, local CA trust, and LAN mode prerequisites.

### Proxy not running

The proxy auto-starts when you run an app with `portless <name> <cmd>`. If it doesn't start (e.g. port conflict), start it manually:

```bash
portless proxy start
```

### Port already in use

Another process is bound to the proxy port. Either stop it first, or use a different port:

```bash
portless proxy start -p 8080
```

### Framework not respecting PORT

Portless auto-injects the right `--port` flag and, when needed, a matching `--host` flag for frameworks that ignore the `PORT` env var: **Vite**, **VitePlus** (`vp`), **Astro**, **React Router**, **Angular**, **Expo**, and **React Native**. SvelteKit uses Vite internally and is handled automatically. Injection reaches through a package script whose command starts with the framework or a known runner, and only for the framework's server commands (`dev`, `serve`, `preview`, `start`, or a bare `vite`) — `vite build`, `vite optimize`, `vp test` and other non-serving commands reject the flags, so they are left untouched, as is any invocation portless cannot classify (`vp --mode dev build`). It is also skipped for a compound command (`&&`, `|`, `;`), a trailing `#` comment, its own `--` option terminator, an env prefix (`NODE_ENV=production vite`), delegation to another script, and runner flags before the script name (`bun run --bun dev`) — each of those keeps its own port and the app returns 502, so set the port in the script yourself.

For other frameworks that don't read `PORT`, pass the port manually:

- **Webpack Dev Server**: use `--port $PORT`
- **Custom servers**: read `process.env.PORT` and listen on it

### Permission errors

The default ports (80 for HTTP, 443 for HTTPS) require `sudo` on macOS and Linux. Portless auto-elevates with sudo when needed. If sudo is unavailable, it falls back to port 1355 (no sudo needed). On Windows, no elevation is required.

```bash
portless proxy start --https           # Auto-elevates with sudo for port 443
portless proxy start -p 1355 --https   # No sudo needed (URLs include :1355)
portless proxy stop                    # Stop (use sudo if started with sudo)
```

### Safari can't find .localhost URLs

Safari relies on the system DNS resolver for `.localhost` subdomains, which may not resolve them on all macOS configurations. Chrome, Firefox, and Edge have built-in handling.

Fix:

```bash
portless hosts sync    # Adds current routes to /etc/hosts
portless hosts clean   # Remove entries later
```

Auto-syncs `/etc/hosts` for route hostnames by default. Set `PORTLESS_SYNC_HOSTS=0` to disable.

### Browser shows certificate warning with --https

The local CA may not be trusted yet. Run:

```bash
portless trust
```

This adds the portless local CA to your system trust store. After that, restart the browser.

### Remove portless from the machine

```bash
portless clean
```

Stops the proxy if needed, removes the portless CA from the trust store (when portless added it), deletes known files under state directories, and removes the portless `/etc/hosts` block. May require `sudo` on macOS/Linux. If trust-store removal fails, portless retains its CA certificate and key so a later `portless clean` can safely retry.

### Proxy loop (508 Loop Detected)

If your dev server proxies requests to another portless app (e.g. Vite proxying `/api` to `api.myapp.localhost`), the proxy must rewrite the `Host` header. Without this, portless routes the request back to the original app, creating an infinite loop.

Fix: set `changeOrigin: true` in the proxy config (Vite, webpack-dev-server, etc.):

```ts
// vite.config.ts
proxy: {
  "/api": {
    target: "https://api.myapp.localhost",
    changeOrigin: true,
    ws: true,
  },
}
```

Portless automatically sets `NODE_EXTRA_CA_CERTS` in child processes so Node.js trusts the portless CA. If you run a separate Node.js process outside portless, point it at the CA manually: `NODE_EXTRA_CA_CERTS=~/.portless/ca.pem`. Alternatively, use `--no-tls` for plain HTTP.

### Tailscale not working

If `--tailscale` or `--funnel` fails:

```bash
tailscale status     # Check if connected
tailscale up         # Connect to your tailnet
```

Requires the Tailscale CLI to be installed (https://tailscale.com/download) and on PATH.

### ngrok not working

If `--ngrok` fails:

```bash
ngrok version                         # Check if installed
ngrok config add-authtoken <token>    # Configure authentication
```

Requires the ngrok CLI to be installed (https://ngrok.com/download) and on PATH.
