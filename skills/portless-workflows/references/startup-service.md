<!-- Adapted from vercel-labs/portless; see ../LICENSE. -->

## OS startup service

Use the service command when users want the proxy to start automatically after reboot:

```bash
portless service install
portless service install --lan
portless service install --wildcard
PORTLESS_STATE_DIR=~/.portless-lan PORTLESS_LAN=1 portless service install
portless service status
portless service uninstall
```

The service uses portless defaults unless install options or `PORTLESS_*` environment variables are provided: HTTPS on port 443 with `.localhost` names. `service install` accepts proxy options including `--port`, `--no-tls`, `--lan`, `--ip`, `--tld`, `--wildcard`, `--cert`, and `--key`. Use `--state-dir <path>` or `PORTLESS_STATE_DIR=<path>` to choose where service state and logs are written.

The chosen service configuration is written into launchd, systemd, or Task Scheduler and reused after reboot. `portless service status` reports the installed port, HTTPS mode, TLDs, LAN mode, wildcard mode, and state directory. macOS and Linux install a root-owned service so port 443 can bind at boot. Windows installs a Task Scheduler startup task that runs as SYSTEM. Installation and removal may require administrator privileges. `portless clean` automatically removes the service.
