"""Make a QR code that opens a local dev server on a phone.

Usage:
    python phone_qr.py PORT [--path /some/page] [--out file.svg]

Finds this machine's Tailscale address (preferred) and home Wi-Fi address (fallback),
checks the server answers on each, and writes one SVG with a QR code per reachable
address. Prints a JSON summary. Exit codes: 0 ok, 2 server is localhost-only,
3 server not running, 4 no network address found.

Standard library only; QR encoding is the vendored qrcodegen.py (Project Nayuki, MIT).
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qrcodegen import QrCode  # noqa: E402

# ---------- pure logic (tested) ----------

def candidate_urls(port: int, path: str, tailscale_ip: str | None, lan_ip: str | None) -> list[tuple[str, str]]:
    path = "/" + path.lstrip("/")
    out = []
    if tailscale_ip:
        out.append(("Tailscale", f"http://{tailscale_ip}:{port}{path}"))
    if lan_ip:
        out.append(("Home Wi-Fi", f"http://{lan_ip}:{port}{path}"))
    return out


def classify(cands: list[tuple[str, str]], reach: dict[str, bool], localhost_ok: bool) -> tuple[str, list[tuple[str, str]]]:
    if not cands:
        return "no-network", []
    ok = [c for c in cands if reach.get(c[1])]
    if ok:
        return "ok", ok
    return ("localhost-only" if localhost_ok else "down"), []


def qr_svg(items: list[tuple[str, str]], module: int = 8, border: int = 4) -> str:
    """One QR code per (label, url), side by side, each with its label and url beneath."""
    codes = [QrCode.encode_text(url, QrCode.Ecc.MEDIUM) for _, url in items]
    side = max(c.get_size() for c in codes) + border * 2
    cell = side * module
    gap, text_h = 24, 56
    width = len(codes) * cell + (len(codes) - 1) * gap
    height = cell + text_h
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
             f'<rect width="{width}" height="{height}" fill="#fff"/>']
    for i, ((label, url), qr) in enumerate(zip(items, codes)):
        x0 = i * (cell + gap)
        off = (side - qr.get_size()) // 2  # centre smaller codes in the shared cell
        d = "".join(f"M{x0 + (x + off) * module},{(y + off) * module}h{module}v{module}h-{module}z"
                    for y in range(qr.get_size()) for x in range(qr.get_size()) if qr.get_module(x, y))
        parts.append(f'<path class="qr" fill="#000" d="{d}"/>')
        cx = x0 + cell / 2
        parts.append(f'<text x="{cx}" y="{cell + 18}" text-anchor="middle" font-family="system-ui,sans-serif" font-size="18" font-weight="600" fill="#000">{escape(label)}</text>')
        parts.append(f'<text x="{cx}" y="{cell + 42}" text-anchor="middle" font-family="ui-monospace,monospace" font-size="14" fill="#333">{escape(url)}</text>')
    parts.append("</svg>")
    return "".join(parts)

# ---------- environment probes ----------

def tailscale_ip() -> str | None:
    try:
        out = subprocess.run(["tailscale", "ip", "-4"], capture_output=True, text=True, timeout=5)
        ip = out.stdout.strip().splitlines()[0] if out.returncode == 0 and out.stdout.strip() else None
        return ip
    except (OSError, subprocess.TimeoutExpired):
        return None


def lan_ip() -> str | None:
    """Address of the interface holding the default route. UDP connect sends no packets."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("192.0.2.1", 80))  # TEST-NET-1, never routed anywhere real
            ip = s.getsockname()[0]
        return None if ip.startswith(("127.", "100.")) else ip  # 100.x is Tailscale's range
    except OSError:
        return None


def reachable(url: str, timeout: float = 2.0) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=timeout):
            return True
    except urllib.error.HTTPError:
        return True  # it answered, even if with 404
    except (urllib.error.URLError, OSError, ValueError):
        return False

# ---------- CLI ----------

HINTS = {
    "localhost-only": "The server only listens on localhost. Restart it listening on all interfaces "
                      "(e.g. vite --host, next dev -H 0.0.0.0, python -m http.server --bind 0.0.0.0).",
    "down": "Nothing answers on that port, even on localhost. Start the server first.",
    "no-network": "No Tailscale or Wi-Fi address found. Turn on Tailscale or connect to a network.",
}
EXIT = {"ok": 0, "localhost-only": 2, "down": 3, "no-network": 4}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("port", type=int)
    p.add_argument("--path", default="/")
    p.add_argument("--out")
    a = p.parse_args(argv)

    cands = candidate_urls(a.port, a.path, tailscale_ip(), lan_ip())
    reach = {url: reachable(url) for _, url in cands}
    local_ok = reachable(f"http://127.0.0.1:{a.port}{'/' + a.path.lstrip('/')}")
    status, ok = classify(cands, reach, local_ok)

    result: dict = {"status": status, "urls": [{"label": l, "url": u} for l, u in ok]}
    if status == "ok":
        out = a.out or os.path.join(tempfile.gettempdir(), "phone-qr", f"phone-qr-{a.port}.svg")
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(qr_svg(ok))
        result["svg"] = os.path.abspath(out)
        unreachable = [l for l, u in cands if not reach[u]]
        if unreachable:
            result["note"] = f"Not reachable via {', '.join(unreachable)} (firewall, or that network is off)."
    else:
        result["hint"] = HINTS[status]
    print(json.dumps(result, indent=2))
    return EXIT[status]


if __name__ == "__main__":
    sys.exit(main())
