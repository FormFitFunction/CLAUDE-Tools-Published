---
name: phone-qr
description: Show a scannable QR code that opens a local dev server on the user's phone. Use whenever the user wants to see, test, review or try something on their phone, iPhone, a real device or a real mobile screen, or asks for a QR code or phone link to a local server — including when you start or restart a server for that purpose. Not needed for checks you do yourself in the browser pane.
---

# Phone QR

Goal: the user scans one QR code and the page opens on their phone. Always show the QR on your own initiative when a server is being run so the user can look at it on a phone; don't wait to be asked.

## Steps

1. **Server must listen on all interfaces**, not just localhost, or the phone can't reach it. When you start the server, start it that way; when it's already running localhost-only, restart it that way (tell the user in one line):
   - Vite: `--host` · Next: `-H 0.0.0.0` · Astro: `--host` · webpack-dev-server: `--host 0.0.0.0`
   - Python: `python -m http.server PORT --bind 0.0.0.0` · Expo: already LAN by default
   - In `.claude/launch.json` entries, put the flag in `runtimeArgs`.
2. **Make the QR:** `python ~/.claude/skills/phone-qr/scripts/phone_qr.py PORT [--path /page]`. It prints JSON:
   - `ok` → `svg` is a file with one QR per reachable address: Tailscale (preferred, same address at home and away) and Home Wi-Fi (fallback when Tailscale is off on the phone).
   - `localhost-only` (exit 2) → go back to step 1.
   - `down` (exit 3) → start the server first. `no-network` (exit 4) → tell the user.
3. **Show it:** send the `svg` path with `SendUserFile` (`display: "render"`) and a one-line caption naming the URLs. Re-send only if the port, path or addresses change.

## If the phone can't open it

The script's check runs from this PC, so it can't see Windows Firewall blocking the phone. If the user reports it won't load:
- Phone side: Tailscale on (for the Tailscale code), or on the same Wi-Fi (for the other).
- PC side: Windows Firewall. Changing firewall rules is a security setting the user must make themselves — give them this command to run in an **admin** PowerShell, with the port filled in, and never run it yourself:
  `New-NetFirewallRule -DisplayName "Dev server PORT" -Direction Inbound -Protocol TCP -LocalPort PORT -Action Allow -Profile Private`
  If their Wi-Fi is marked Public, suggest switching it to Private in Windows Settings › Network instead of opening the port on Public.

## Notes

- Codes use plain `http://`. HTTPS (needed for service workers and push on iPhone) is out of scope. `tailscale serve` can add it, but its certificate publishes the machine's Tailscale name in public certificate-transparency logs, so only use it if the user agrees.
- Files, all in this skill's `scripts/`: `phone_qr.py` (logic), `test_phone_qr.py` (run `python -m unittest test_phone_qr` from that folder), `qrcodegen.py` (vendored QR encoder, Project Nayuki, MIT, unmodified).
