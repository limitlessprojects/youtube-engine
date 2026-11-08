#!/usr/bin/env python3
"""views_tracker.py — nightly view sampler for OUR channel via RSS (bot-wall-free).

30-day plan Phase B prep: append one row per live video to logs/views.csv:
    date,video_id,title,views,published
7-day rolling comparison happens in the ledger; the CSV is the artifact (L-003:
measure, never estimate).

Usage: python3 tools/views_tracker.py   (idempotent per day: rewrites today's rows)
"""
from __future__ import annotations

import csv
import datetime as dt
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHANNEL_ID = "UCo_p5nBuNe9KW_W_x90Nitg"  # Jack Blessed
FEED = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
CSV = REPO / "logs" / "views.csv"
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015",
      "media": "http://search.yahoo.com/mrss/"}


def fetch() -> list[dict]:
    req = urllib.request.Request(FEED, headers={"User-Agent": "Mozilla/5.0 (rss-scout/1)"})
    root = ET.fromstring(urllib.request.urlopen(req, timeout=20).read())
    rows = []
    for e in root.findall("a:entry", NS):
        vid = e.findtext("yt:videoId", namespaces=NS)
        title = (e.findtext("a:title", namespaces=NS) or "").strip()
        pub = (e.findtext("a:published", namespaces=NS) or "")[:10]
        stats = e.find("media:group/media:community/media:statistics", NS)
        views = int(stats.get("views", "0")) if stats is not None else 0
        rows.append({"video_id": vid, "title": title, "published": pub, "views": views})
    return rows


def main() -> None:
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    rows = fetch()
    if not rows:
        print("[views] RSS returned no entries — leaving CSV untouched")
        return
    existing: dict[tuple[str, str], list[str]] = {}
    if CSV.exists():
        with CSV.open() as f:
            for r in csv.reader(f):
                if len(r) >= 5 and r[0] and r[0] != "date":
                    existing[(r[0], r[1])] = r  # (date, video_id) -> row
    out = []
    seen_today = set()
    for v in rows:
        row = [today, v["video_id"], v["title"], str(v["views"]), v["published"]]
        out.append(row)
        seen_today.add(v["video_id"])
        print(f"[views] {v['video_id']}  {v['views']:>7,}  {v['title'][:60]}")
    # drop stale duplicates of today, keep history, sort by date desc then id
    merged = [r for k, r in existing.items() if k[0] != today and k[1] not in seen_today]
    all_rows = sorted(out + merged, key=lambda r: (r[0], r[1]), reverse=True)
    with CSV.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "video_id", "title", "views", "published"])
        w.writerows(all_rows)
    print(f"[views] wrote {len(all_rows)} rows -> {CSV.relative_to(REPO)} ({today})")


if __name__ == "__main__":
    main()
