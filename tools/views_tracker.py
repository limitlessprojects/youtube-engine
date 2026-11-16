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
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHANNEL_ID = "UCo_p5nBuNe9KW_W_x90Nitg"  # Jack Blessed
# Rung 1 is the channel feed; rung 2 is the uploads PLAYLIST feed — day-019:
# the channel_id variant 404s from every IP class we've tried (studio 11-15,
# sandbox + GitHub runner 11-16) while the channel itself is fine; playlist
# feeds survive some channel-side breakage modes (rename/handle churn).
FEEDS = [
    f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}",
    f"https://www.youtube.com/feeds/videos.xml?playlist_id=UU{CHANNEL_ID[2:]}",
]
CSV = REPO / "logs" / "views.csv"
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015",
      "media": "http://search.yahoo.com/mrss/"}


def fetch() -> list[dict]:
    # bot-wall ladder (L-031): a 404/429 on one attempt is NOT a verdict —
    # rotate UA + backoff per feed; rung 2 = uploads-playlist variant (day-019)
    uas = ["Mozilla/5.0 (rss-scout/1)",
           "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0",
           "curl/8.5.0"]
    last_err: Exception | None = None
    for feed in FEEDS:
        for i, ua in enumerate(uas):
            try:
                req = urllib.request.Request(feed, headers={"User-Agent": ua})
                root = ET.fromstring(urllib.request.urlopen(req, timeout=20).read())
                break
            except Exception as e:  # noqa: BLE001
                last_err = e
                print(f"[views] {feed.split('?', 1)[1]} attempt {i + 1} failed ({e}); retrying…"
                      if i < len(uas) - 1 else f"[views] {feed.split('?', 1)[1]} all {len(uas)} attempts failed: {e}")
                time.sleep(3)
        else:
            continue
        break
    else:
        raise SystemExit(f"[views] every feed variant unreachable: {last_err}")
    rows = []
    for e in root.findall("a:entry", NS):
        vid = e.findtext("yt:videoId", namespaces=NS)
        title = (e.findtext("a:title", namespaces=NS) or "").strip()
        pub = (e.findtext("a:published", namespaces=NS) or "")[:10]
        stats = e.find("media:group/media:community/media:statistics", NS)
        views = int(stats.get("views", "0")) if stats is not None else 0
        rows.append({"video_id": vid, "title": title, "published": pub, "views": views})
    return rows


def read_history() -> list[list[str]]:
    """Every captured row except the header, deduped per (date, video_id).

    HISTORY IS KEPT (day-019 fix): the pre-019 merge dropped all older rows of
    every video in today's feed, so the CSV held only the latest row per video
    and the plan's 24 h/48 h comparisons had no time series to read.
    """
    seen: dict[tuple[str, str], list[str]] = {}
    if CSV.exists():
        with CSV.open() as f:
            for r in csv.reader(f):
                if len(r) >= 5 and r[0] and r[0] != "date":
                    seen[(r[0], r[1])] = r
    return list(seen.values())


def write_rows(all_rows: list[list[str]]) -> None:
    with CSV.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "video_id", "title", "views", "published"])
        w.writerows(sorted(all_rows, key=lambda r: (r[0], r[1]), reverse=True))


def merge_today(fresh: list[list[str]], today: str) -> list[list[str]]:
    """Idempotent per day: today's rows are REPLACED, every other day stays."""
    return [r for r in read_history() if r[0] != today] + fresh


def main() -> None:
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    rows = fetch()
    if not rows:
        print("[views] RSS returned no entries — leaving CSV untouched")
        return
    fresh = []
    for v in rows:
        fresh.append([today, v["video_id"], v["title"], str(v["views"]), v["published"]])
        print(f"[views] {v['video_id']}  {v['views']:>7,}  {v['title'][:60]}")
    all_rows = merge_today(fresh, today)
    write_rows(all_rows)
    print(f"[views] wrote {len(all_rows)} rows -> {CSV.relative_to(REPO)} ({today})")


if __name__ == "__main__":
    main()
