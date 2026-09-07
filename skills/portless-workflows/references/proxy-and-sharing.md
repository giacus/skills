<!-- Adapted from vercel-labs/portless; see ../LICENSE. -->

## How It Works

1. `portless proxy start` starts an HTTPS reverse proxy on port 443 as a background daemon. Auto-elevates with sudo on macOS/Linux; falls back to port 1355 if sudo is unavailable. Use `--no-tls` for plain HTTP on port 80. Configurable with `-p` / `--port` or the `PORTLESS_PORT` env var. The proxy also auto-starts when you run an app.
2. `portless <name> <cmd>` assigns a random free port (4000-4999) via the `PORT` env var and registers the app with the proxy
3. The browser hits `https://<name>.localhost`; the proxy forwards to the app's assigned port

Outside LAN mode, the proxy and its HTTP redirect listener bind only to the IPv4 and IPv6 loopback addresses, `127.0.0.1` and `::1`. They do not accept connections through LAN, VPN, or other network interfaces.

`.localhost` domains resolve to `127.0.0.1` natively in Chrome, Firefox, and Edge. Safari relies on the system DNS resolver, which may not handle `.localhost` subdomains on all configurations. Run `portless hosts sync` to add entries to `/etc/hosts` if needed.

Use `portless proxy start --tld localhost --tld test` to serve the same app names under multiple TLDs from one proxy. `PORTLESS_URL` uses the first configured TLD. When configured TLDs overlap (e.g. `example.com` and `dev.example.com`), hostnames are matched against the longest TLD first, regardless of configuration order. `PORTLESS_TLD` accepts the same comma separated list format, e.g. `PORTLESS_TLD=localhost,test`.

TLDs can be multi-segment DNS names such as `dev.example.com`, so local URLs can mirror production structure (`myapp.dev.example.com`). Each label follows DNS rules: lowercase letters, digits, interior hyphens, 63 characters per label, 253 total. Strict OAuth providers that reject `.localhost` redirect URIs accept a real domain like `https://myapp.dev.example.com/api/auth/callback/google`.

Most frameworks (Next.js, Express, Nuxt, etc.) respect the `PORT` env var automatically. For frameworks that ignore `PORT` (Vite, VitePlus, Astro, React Router, Angular, Expo, React Native), portless auto-injects the correct `--port` flag and, when needed, a matching `--host` CLI flag. Injection reaches through a package script whose command starts with the framework or a known runner (`"dev": "vite"`, `"dev": "bunx vite"`). Only the framework's server commands get the flags (`dev`, `serve`, `preview`, `start`, a bare `vite`, or `vite [root]`); a command that does not serve, such as `vite build`, `vite optimize`, `vp test` or `astro check`, rejects them and is left alone. Expo connection modes (`--localhost`, `--lan`, `--tunnel`) are preserved while the assigned port is still injected. A script portless cannot classify is left alone too: a flag before the subcommand on a CLI whose flag grammar it does not track (`vp --mode dev build`). Portless also leaves a script alone when appending flags to it would not work: a compound command (`&&`, `|`, `;`), a trailing `#` comment, its own `--` option terminator, an env prefix (`NODE_ENV=production vite`), delegation to another script (`"dev": "npm run dev:vite"`), or runner flags before the script name (`bun run --bun dev`). Those keep their own port, so set it in the script yourself.

### State directory

Portless stores its state (routes, PID file, port file) in `~/.portless`. When the proxy runs under sudo, this remains the invoking user's home directory so unprivileged apps and the proxy share route registrations. Override with the `PORTLESS_STATE_DIR` environment variable.

### Environment variables

| Variable              | Description                                                                    |
| --------------------- | ------------------------------------------------------------------------------ |
| `PORTLESS_PORT`       | Override the default proxy port (default: 443 with HTTPS, 80 without)          |
| `PORTLESS_APP_PORT`   | Use a fixed port for the app (skip auto-assignment)                            |
| `PORTLESS_HTTPS`      | HTTPS on by default; set to `0` to disable (same as `--no-tls`)                |
| `PORTLESS_LAN`        | Set to `1` to always enable LAN mode (auto-detects LAN IP)                     |
| `PORTLESS_LAN_IP`     | Pin a specific LAN IP for LAN mode                                             |
| `PORTLESS_TLD`        | Use one or more TLDs, single or multi-segment (e.g. localhost,dev.example.com) |
| `PORTLESS_WILDCARD`   | Set to `1` to allow unregistered subdomains to fall back to parent             |
| `PORTLESS_SYNC_HOSTS` | Set to `0` to disable auto-sync of /etc/hosts (on by default)                  |
| `PORTLESS_TAILSCALE`  | Set to `1` to share apps on your Tailscale network (same as `--tailscale`)     |
| `PORTLESS_FUNNEL`     | Set to `1` to share apps publicly via Tailscale Funnel (same as `--funnel`)    |
| `PORTLESS_NGROK`      | Set to `1` to share apps publicly via ngrok (same as `--ngrok`)                |
| `PORTLESS_STATE_DIR`  | Override the state directory                                                   |
| `PORTLESS=0`          | Bypass the proxy, run the command directly                                     |

### HTTP/2 + HTTPS

HTTPS with HTTP/2 is enabled by default (faster page loads for dev servers with many files). WebSockets work over both HTTP/1.1 (Upgrade) and HTTP/2 (RFC 8441 extended CONNECT), so dev server HMR works through the proxy. First run generates a local CA and adds it to the system trust store. After that, no prompts and no browser warnings.

```bash
portless proxy start --cert ./c.pem --key ./k.pem  # Use custom certs
portless proxy start --no-tls                       # Disable HTTPS (plain HTTP)
portless trust                                      # Add CA to trust store later
```

On Linux, `portless trust` supports Debian/Ubuntu, Arch, Fedora/RHEL/CentOS, and openSUSE (via `update-ca-certificates` or `update-ca-trust`). On Windows, it uses `certutil` to add the CA to the system trust store. On WSL, it updates both the Linux trust store and the Windows current-user Root store so Windows browsers trust portless HTTPS certificates.

### LAN mode

```bash
portless proxy start --lan
portless proxy start --lan --https
portless proxy start --lan --ip 192.168.1.42
```

`--lan` explicitly binds the proxy to the IPv4 and IPv6 unspecified addresses, `0.0.0.0` and `::`, and advertises `<name>.local` hostnames over mDNS so devices on the same Wi-Fi can reach your apps. Portless auto-detects your LAN IP and follows network changes automatically, but you can pin a specific address with `--ip <address>` or the `PORTLESS_LAN_IP` environment variable. Set `PORTLESS_LAN=1` to default to LAN mode every time the proxy starts.

Portless remembers LAN mode via `proxy.lan`, so if you stop a LAN proxy and start again, it stays in LAN mode. All proxy settings (port, TLS, TLDs, LAN) are persisted and reused on auto-start unless overridden by explicit flags or env vars. Use `PORTLESS_LAN=0` for one start to switch back to `.localhost` mode. If a proxy is already running with different explicit LAN/TLS/TLD settings, portless warns and asks you to stop it first.

LAN mode depends on the system mDNS helpers that portless launches: macOS includes `dns-sd`, while Linux uses `avahi-publish-address` from `avahi-utils` (install via `sudo apt install avahi-utils` or your distro’s tooling).

- **Next.js**: add your `.local` hostnames to `allowedDevOrigins`:

  ```js
  // next.config.js
  module.exports = {
    allowedDevOrigins: ["myapp.local", "*.myapp.local"],
  };
  ```

- **Expo / React Native**: portless always injects `--port`. React Native also gets `--host 127.0.0.1`. Expo gets `--host localhost` outside LAN mode, but in LAN mode portless leaves Metro on its default LAN host behavior instead of forcing `--host` or `HOST`.

### Tailscale sharing

Share dev servers with teammates on your Tailscale network using `--tailscale`, or expose to the public internet with `--funnel`:

```bash
portless myapp --tailscale next dev
# -> https://myapp.localhost           (local)
# -> https://devbox.yourteam.ts.net    (tailnet)

portless myapp --funnel next dev
# -> https://myapp.localhost           (local)
# -> https://devbox.yourteam.ts.net    (public internet)
```

Tailscale HTTPS certificates must be enabled before `--tailscale` or `--funnel` can register HTTPS URLs. Funnel must also be enabled for the tailnet and node before `--funnel` can register the public URL. If either setting is missing, portless exits before starting the child process.

Each `--tailscale` app is root-mounted on its own Tailscale HTTPS port (443, then 8443, 8444, etc.) so no framework `basePath` configuration is needed. Set `PORTLESS_TAILSCALE=1` to share every app by default. `portless list` shows both local and tailnet URLs. Tailscale serve registrations are cleaned up when the app exits. Requires `tailscale` CLI installed and connected, with Tailscale HTTPS certificates enabled.

### ngrok sharing

Expose a dev server to the public internet with ngrok using `--ngrok`:

```bash
portless myapp --ngrok next dev
# -> https://myapp.localhost           (local)
# -> https://abc123.ngrok.app          (public internet)
```

Set `PORTLESS_NGROK=1` to enable ngrok by default when portless runs an app. `portless list` shows both local and ngrok URLs. The ngrok tunnel is cleaned up when the app exits. Requires the `ngrok` CLI to be installed and authenticated with `ngrok config add-authtoken <token>`.
