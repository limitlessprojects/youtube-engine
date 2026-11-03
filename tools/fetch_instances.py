#!/usr/bin/env python3
"""fetch_instances.py — live mirror registry for the transcribe ladder (L-050).

Hardcoded mirror lists rot in days (6/6 invidious + 8/8 piped defaults were dead
by 2026-11-03). This fetches the LIVE community registries at runtime, caches
24h, and emits shell exports that transcribe.py already honors:

    eval "$(python3 tools/fetch_instances.py --export)"
    python3 tools/transcribe.py <url>

Sources (all fetched with fail-soft; a dead source is skipped, not fatal):
  - Invidious: https://api.invidious.io/instances.json?sort_by=health (official)
  - Piped:     https://piped-instances.kavin.rocks/ (official registry; may 404)

Usage:
  python3 tools/fetch_instances.py            # human-readable report
  python3 tools/fetch_instances.py --export   # prints: export INVIDIOUS_INSTANCES="..."
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CACHE = REPO / "research" / "cache" / "instances.json"
TTL = 24 * 3600
UA = {"User-Agent": "Mozilla/5.0"}


def _http(url: str, timeout: int = 12) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_invidious() -> list[str]:
    data = json.loads(_http("https://api.invidious.io/instances.json?sort_by=health"))
    hosts = [name for name, meta in data
             if meta.get("type") == "https" and meta.get("api") is not False]
    return ["https://" + h for h in hosts]


def fetch_piped() -> list[str]:
    data = json.loads(_http("https://piped-instances.kavin.rocks/"))
    return [i["api_url"].rstrip("/") for i in data if i.get("api_url")]


def registry() -> dict:
    if CACHE.exists() and time.time() - CACHE.stat().st_mtime < TTL:
        return json.loads(CACHE.read_text())
    out: dict[str, list[str]] = {}
    for name, fn in (("invidious", fetch_invidious), ("piped", fetch_piped)):
        try:
            out[name] = fn()
            print(f"[reg] {name}: {len(out[name])} live instances", file=sys.stderr)
        except Exception as e:
            print(f"[reg] {name} registry unreachable ({type(e).__name__}) — "
                  f"transcribe.py falls back to its defaults", file=sys.stderr)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps({"ts": time.time(), **out}, indent=1))
    return out


def main() -> int:
    reg = registry()
    export = "--export" in sys.argv
    if export:
        if reg.get("invidious"):
            print("export INVIDIOUS_INSTANCES='" +
                  json.dumps(reg["invidious"], separators=(",", ":")) + "'")
        if reg.get("piped"):
            print("export PIPED_INSTANCES='" +
                  json.dumps(reg["piped"], separators=(",", ":")) + "'")
        return 0
    for k, v in reg.items():
        print(f"{k} ({len(v)}):")
        for u in v:
            print(f"  {u}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
