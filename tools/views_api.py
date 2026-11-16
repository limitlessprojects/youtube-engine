#!/usr/bin/env python3
"""views_api.py — log channel views via YouTube Data API v3 (fallback for views_tracker.py).

Why: the RSS feed (youtube.com/feeds/videos.xml) is IP-walled on some sandbox
classes (HTTP 404 to every UA, day-019 — L-031 class but a 404, not a 403).
The Data API is deterministic, needs no scraping and uses the OAuth grant we
already hold (videos.list is allowed under the upload scope).

What it does:
  1. reads every content/short-*/published.json (canonical id/title/date list)
  2. refreshes the OAuth token (same plumbing as youtube_upload.py)
  3. GET /youtube/v3/videos?part=snippet,statistics for all ids at once
  4. rewrites TODAY's rows in logs/views.csv (re-runs are idempotent per day)
     using the same schema as views_tracker.py: date,video_id,title,views,published

Usage:
  python3 tools/views_api.py [--token-file .secrets/token.json] [--dry]
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import datetime as dt
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
TOKEN_URI = "https://oauth2.googleapis.com/token"
VIDEOS = "https://www.googleapis.com/youtube/v3/videos"
CSV_PATH = ROOT / "logs" / "views.csv"


def published_shorts() -> list[dict]:
    out = []
    for p in sorted((ROOT / "content").glob("short-*/published.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        d["source"] = str(p.parent.relative_to(ROOT))
        out.append(d)
    return out


def load_token(path: str | None) -> dict:
    raw = os.environ.get("YOUTUBE_TOKEN_JSON", "").strip()
    if path:
        raw = Path(path).read_text(encoding="utf-8")
    if not raw:
        sys.exit("no token: set YOUTUBE_TOKEN_JSON or pass --token-file")
    return json.loads(raw)


def refresh(tok: dict) -> str:
    r = requests.post(TOKEN_URI, data={
        "client_id": tok["client_id"], "client_secret": tok["client_secret"],
        "refresh_token": tok["refresh_token"], "grant_type": "refresh_token",
    }, timeout=60)
    r.raise_for_status()
    return r.json()["access_token"]


def fetch_stats(ids: list[str], access: str) -> dict[str, dict]:
    stats: dict[str, dict] = {}
    for i in range(0, len(ids), 50):  # API caps ids at 50 per call
        r = requests.get(VIDEOS, params={
            "part": "snippet,statistics", "id": ",".join(ids[i:i + 50])},
            headers={"Authorization": f"Bearer {access}"}, timeout=60)
        if not r.ok:  # surface the API's own reason (scope errors say so here)
            sys.exit(f"[views] API {r.status_code}: {r.text[:500]}")
        for item in r.json().get("items", []):
            stats[item["id"]] = {
                "views": int(item["statistics"].get("viewCount", 0)),
                "title": item["snippet"]["title"],
                "published": item["snippet"]["publishedAt"][:10],
            }
    return stats


def rewrite_today(rows: list[list], today: str, fresh: list[list]) -> None:
    """Drop today's existing rows, append the fresh ones, keep date order."""
    kept = [r for r in rows if r and r[0] != today]
    kept.extend(fresh)
    kept.sort(key=lambda r: (r[0], r[1]))
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f, quoting=csv.QUOTE_MINIMAL).writerows(kept)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--token-file", default=".secrets/token.json")
    ap.add_argument("--dry", action="store_true", help="print only, do not touch views.csv")
    a = ap.parse_args()

    shorts = published_shorts()
    if not shorts:
        sys.exit("no content/short-*/published.json found")

    access = refresh(load_token(a.token_file))
    stats = fetch_stats([s["video_id"] for s in shorts], access)

    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    fresh, missing = [], []
    for s in shorts:
        st = stats.get(s["video_id"])
        if not st:
            missing.append(s["video_id"])
            continue
        fresh.append([today, s["video_id"], st["title"], str(st["views"]), st["published"]])
        age_h = (dt.datetime.now(dt.timezone.utc)
                 - dt.datetime.fromisoformat(s["published_at"].replace("Z", "+00:00"))
                 ).total_seconds() / 3600
        print(f"[views] {s['source']}  {s['video_id']}  {st['views']:>6,} views  "
              f"(T+{age_h:.1f}h)  {st['title'][:48]}")

    if missing:
        print(f"[views] WARN: API returned no item for: {', '.join(missing)}", file=sys.stderr)

    if a.dry or not fresh:
        return 0

    existing = list(csv.reader(CSV_PATH.open(encoding="utf-8"))) if CSV_PATH.exists() else []
    rewrite_today(existing, today, fresh)
    print(f"[views] {len(fresh)} rows for {today} written to {CSV_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
