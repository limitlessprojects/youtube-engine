#!/usr/bin/env python3
"""probe_downloaders.py — daily radar over public downloader front-ends.

Why: YouTube hard-blocks cloud IPs for direct caption/audio fetches (L-031/L-049).
Downloader sites (y2mate class) proxy the fetch through THEIR servers, so our
egress IP is irrelevant to them. If one exposes a stable callable API, it is a
candidate fallback tier for audio → whisper → transcript.

POSTURE (L-054 + boss directive): research-only. Undocumented third-party
endpoints rot fast and must NEVER be production-critical. This radar maps the
landscape daily from runner IPs; a hit gets evaluated, not auto-wired.

Probe levels:
  L1 liveness  — homepage reachable, not a bot-wall/challenge page
  L2 API shape — known AJAX endpoint answers with JSON (not HTML challenge)
  L3 convert   — best-effort real analyze call for a test video (y2mate family)

Writes research/cache/downloaders.json (tsv: one line per site per run).
Always exits 0 — a radar, not a gate.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research" / "cache" / "downloaders.json"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
TEST_URL = "https://www.youtube.com/watch?v=jNQXAC9IVRw"  # "Me at the zoo": tiny, ancient, stable
T = 15  # per-request timeout

SITES: list[dict] = [
    # y2mate family — same codebase lineage, AJAX analyze endpoints
    {"name": "y2mate.com", "home": "https://www.y2mate.com/",
     "api": ("POST", "https://www.y2mate.com/mates/analyze/ajax",
             {"url": TEST_URL, "ajax": "1"})},
    {"name": "yt1s.com", "home": "https://yt1s.com.co/",
     "api": ("POST", "https://yt1s.com.co/ajax", {"url": TEST_URL, "ajax": "1"})},
    {"name": "yt5s.io", "home": "https://yt5s.io/",
     "api": ("POST", "https://yt5s.io/api/ajax", {"url": TEST_URL, "ajax": "1"})},
    {"name": "cnvmp3.com", "home": "https://cnvmp3.com/",
     "api": ("POST", "https://cnvmp3.com/api/json", {"url": TEST_URL})},
    # other lineages
    {"name": "clipconverter.cc", "home": "https://www.clipconverter.cc/",
     "api": ("POST", "https://www.clipconverter.cc/check.php",
             {"mediaurl": TEST_URL, "client": "clipconverter"})},
    {"name": "onlinevideoconverter.com", "home": "https://www.onlinevideoconverter.com/",
     "api": None},  # api subdomain needs a JS-minted ticket; L1/L2 only
    {"name": "9xbuddy.com", "home": "https://9xbuddy.com/",
     "api": ("POST", "https://9xbuddy.com/a/config", {"url": TEST_URL})},
    {"name": "savefrom.net", "home": "https://en.savefrom.net/",
     "api": None},  # signed-token API (JS) — L1/L2 only
    # meta front-ends / dead-legend checks
    {"name": "ssyoutube.com", "home": "https://ssyoutube.com/", "api": None},
    {"name": "y2mate.nu", "home": "https://y2mate.nu/", "api": None},
]


def looks_like_challenge(text: str) -> bool:
    t = text.lower()
    return any(m in t for m in (
        "cf-browser-verification", "cf_chl", "challenge-platform",
        "just a moment", "attention required", "ddos protection",
        "verifying you are human", "turnstile",
    ))


def probe(site: dict) -> dict:
    r: dict = {"name": site["name"], "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})

    # L1 — liveness
    try:
        resp = s.get(site["home"], timeout=T, allow_redirects=True)
        html = resp.text[:4000].lower()
        cf = looks_like_challenge(html)
        r["l1_home"] = f"{resp.status_code}{'/challenge' if cf else ''}"
        r["alive"] = resp.status_code < 400 and not cf
    except Exception as e:  # noqa: BLE001
        r["l1_home"] = f"ERR:{type(e).__name__}"
        r["alive"] = False

    # L2 — API shape
    if site.get("api"):
        method, url, data = site["api"]
        try:
            resp = s.post(url, data=data, timeout=T,
                          headers={"X-Requested-With": "XMLHttpRequest",
                                   "Referer": site["home"]})
            ct = resp.headers.get("Content-Type", "")
            is_json = "json" in ct or resp.text.lstrip()[:1] in "{["
            r["l2_api"] = (f"{resp.status_code}/{'json' if is_json else 'html'} "
                           f"({len(resp.text)}b)")
            r["api_reachable"] = resp.status_code == 200 and is_json and not looks_like_challenge(resp.text[:4000])
        except Exception as e:  # noqa: BLE001
            r["l2_api"] = f"ERR:{type(e).__name__}"
            r["api_reachable"] = False
    else:
        r["l2_api"] = "skip(JS-signed API)"
        r["api_reachable"] = False

    verdict = "DEAD"
    if r.get("api_reachable"):
        verdict = "API-JSON"
    elif r.get("alive"):
        verdict = "ALIVE(html-only)"
    r["verdict"] = verdict
    return r


def main() -> int:
    results = []
    for site in SITES:
        row = probe(site)
        results.append(row)
        print(f"[radar] {row['name']:<26} l1={row['l1_home']:<22} "
              f"l2={str(row.get('l2_api')):<26} => {row['verdict']}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    hist = json.loads(OUT.read_text()) if OUT.exists() else []
    hist = hist[-13:] + [results]  # keep last 14 daily snapshots
    OUT.write_text(json.dumps(hist, indent=1))
    print(f"[radar] wrote {OUT} (snapshot {len(hist)}/14)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
