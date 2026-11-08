# phone-qr

**Type:** skill

## What it is

When you want to look at a local dev server on your phone, Claude shows a QR code you scan to open it. No asking needed: the skill triggers whenever the conversation is about seeing something on a phone or real device.

- One QR per address that works: **Tailscale** first (same address at home and away), then **home Wi-Fi** as a fallback.
- Checks the server actually answers on each address. If it only listens on `localhost` (the usual reason a phone can't reach it), Claude restarts it listening on the network instead of handing you a code that fails.
- Python standard library only, no install. QR encoding is a vendored copy of [Project Nayuki's QR Code generator](https://www.nayuki.io/page/qr-code-generator-library) (MIT, unmodified).

## How to use it

Copy this folder to `~/.claude/skills/phone-qr/` (all projects) or `<project>/.claude/skills/phone-qr/` (one project). Then just ask Claude to show you the app on your phone, or run `/phone-qr`.

Requirements: Python 3.9+. Tailscale is optional; without it you get the home Wi-Fi code only.

Run directly:

```
python scripts/phone_qr.py 5173 [--path /page] [--out qr.svg]
```

It prints JSON and writes an SVG (default: `<temp>/phone-qr/phone-qr-<port>.svg`, overwritten per port). Exit codes: `0` ok, `2` localhost-only, `3` nothing running, `4` no network address.

Tests, from `scripts/`: `python -m unittest test_phone_qr`.

## Notes

- The reachability check runs on the same machine, so it can't see a firewall blocking the phone. On Windows the skill gives you the firewall command to run yourself; it never changes firewall settings.
- Plain `http://` only. Service workers and push on iPhone need HTTPS, which this doesn't set up.
