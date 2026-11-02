#!/usr/bin/env python3
"""proxy_pool.py — fresh, validated proxies from GitHub-hosted lists (L-039).

The bot-wall endgame rung: YouTube sees the proxy's IP, not the runner's
(docs/architecture.md "The bot-wall ladder"). Lists live in public GitHub
repos updated every 5-30 minutes; we fetch, validate against YouTube
reachability + latency, cache, and serve.

Sources (override with PROXY_LIST_URLS env, comma-separated):
  - proxifly/free-proxy-list   (7k stars, updated every 5 min, protocol://host:port)
  - monosans/proxy-list        (updated every 30 min, pre-checked, host:port)
  - TheSpeedX/SOCKS-List       (5.9k stars, daily, host:port http + socks5)

Usage:
  python tools/proxy_pool.py best --n 3      # print N best (validated)
  python tools/proxy_pool.py env             # print PROXY_URL=<best> (eval me)
  python tools/proxy_pool.py test --proxy http://1.2.3.4:8080
  python tools/proxy_pool.py refresh         # force re-fetch + re-validate

Exit 0 with a proxy, exit 3 (retryable) when none validate.
Cache: research/proxies/cache.json (gitignored) holds {proxy, ms, checked_at}.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import sys
import time
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parent.parent
CACHE = REPO / "research" / "proxies" / "cache.json"
CACHE_TTL = 20 * 60  # minutes-fresh window

SOURCES = [
    # (url, line_format)  line_format: "scheme_host_port" | "host_port"
    ("https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt",
     "scheme_host_port"),
    ("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
     "host_port"),
    ("https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
     "host_port"),
]
PROBE_URL = "https://www.youtube.com/robots.txt"
TIMEOUT = 6


def fetch_list() -> list[str]:
    """Round-robin across sources so one repo's ordering can't dominate."""
    urls = [u.strip() for u in
            __import__("os").environ.get("PROXY_LIST_URLS", "").split(",") if u.strip()]
    pairs = [(u, fmt) for u, fmt in SOURCES] if not urls else [(u, "auto") for u in urls]
    # requests needs PySocks for socks; http proxies work everywhere (and
    # yt-dlp --proxy takes both). Keep the pool to what we can actually use.
    try:
        import socks  # noqa: F401
        usable = ("http", "https", "socks5")
    except ImportError:
        usable = ("http", "https")
    per_source: list[list[str]] = []
    for url, fmt in pairs:
        try:
            r = requests.get(url, timeout=10,
                             headers={"User-Agent": "youtube-engine/proxy-pool"})
            r.raise_for_status()
        except Exception as e:
            print(f"[pp] source down: {url.split('/')[2]}: {type(e).__name__}",
                  file=sys.stderr)
            per_source.append([])
            continue
        parsed: list[str] = []
        for line in r.text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "://" in line:
                if line.split("://")[0] in usable:
                    parsed.append(line)
            elif fmt in ("host_port", "auto") and line.count(":") == 1:
                parsed.append(f"http://{line}")
        per_source.append(parsed)
        print(f"[pp] {url.split('/')[2]}: {len(parsed)} usable candidates",
              file=sys.stderr)
    out: list[str] = []
    for i in range(max((len(p) for p in per_source), default=0)):
        for src in per_source:
            if i < len(src):
                out.append(src[i])
    seen: set[str] = set()
    return [p for p in out if not (p in seen or seen.add(p))]


def validate(proxy: str) -> dict | None:
    t0 = time.monotonic()
    try:
        r = requests.get(PROBE_URL, proxies={"http": proxy, "https": proxy},
                         timeout=TIMEOUT, headers={"User-Agent": "Mozilla/5.0"})
        ok = r.status_code == 200 and ("User-agent" in r.text or "Disallow" in r.text)
    except Exception:
        return None
    ms = int((time.monotonic() - t0) * 1000)
    return {"proxy": proxy, "ms": ms} if ok else None


def validated_pool(limit: int = 300, workers: int = 24) -> list[dict]:
    candidates = fetch_list()[:limit]
    print(f"[pp] validating {len(candidates)} candidates "
          f"({workers} workers, {TIMEOUT}s timeout)...", file=sys.stderr)
    good: list[dict] = []
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        for res in ex.map(validate, candidates):
            if res:
                good.append(res)
    good.sort(key=lambda x: x["ms"])
    return good


def load_cache(max_age: float = CACHE_TTL) -> list[dict] | None:
    if not CACHE.exists():
        return None
    data = json.loads(CACHE.read_text())
    if time.time() - data.get("checked_at", 0) > max_age:
        return None
    return data.get("proxies", [])


def save_cache(proxies: list[dict]) -> None:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(
        {"checked_at": time.time(), "proxies": proxies}, indent=1) + "\n")


def best(n: int = 1, refresh: bool = False) -> list[dict]:
    pool = None if refresh else load_cache()
    if not pool:
        pool = validated_pool()
        if pool:
            save_cache(pool)
    return pool[:n]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["best", "env", "test", "refresh"])
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--proxy")
    ap.add_argument("--limit", type=int, default=240)
    ap.add_argument("--workers", type=int, default=24)
    args = ap.parse_args()

    if args.cmd == "test":
        res = validate(args.proxy or "")
        print(json.dumps(res or {"proxy": args.proxy, "ok": False}, indent=1))
        return 0 if res else 3

    n = max(1, args.n)
    pool = best(n, refresh=(args.cmd == "refresh"))
    if not pool:
        print("[pp] no working proxies this round — retry later (exit 3, retryable)",
              file=sys.stderr)
        return 3
    if args.cmd == "env":
        print(f"PROXY_URL={pool[0]['proxy']}")
    else:
        for p in pool:
            print(f"{p['proxy']}  {p['ms']}ms")
    return 0


if __name__ == "__main__":
    sys.exit(main())
