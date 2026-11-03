#!/usr/bin/env python3
"""rss_scout.py — zero-friction outlier discovery via channel RSS feeds.

L-053: youtube.com/feeds/videos.xml is served from plain CDN caching and is
NOT behind the captions bot-wall (verified 2026-11-03 from a hard-flagged
datacenter IP that gets Google sorry-pages on watch pages). Each entry carries
yt:videoId, title, published, media:description, media:statistics @views.

This replaces the bot-walled `yt-dlp ytsearch` discovery path (daily spec
step 4) and computes the outlier rule from config/channels.json:

    Outlier Score = video views / channel average views (recent feed window)

Usage:
    python3 tools/rss_scout.py                 # report top outliers
    python3 tools/rss_scout.py --enqueue N     # also append top N URLs to queue
    python3 tools/rss_scout.py --min-score 3   # stricter outlier threshold
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CONFIG = REPO / "config" / "channels.json"
QUEUE = REPO / "config" / "learning_queue.txt"
CACHE = REPO / "research" / "cache" / "channel_ids.json"
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015",
      "media": "http://search.yahoo.com/mrss/"}

# Title keywords that mark a candidate as OUR niche (hypothetical what-if science/history).
NICHE = re.compile(r"\bwhat if|what would happen|suppose|hypothet|could we|why (do|does|is)|how (do|does|did|long|big|small)|end of|last |future of", re.I)


def _http(url: str, timeout: int = 15) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def channel_id_for(handle: str) -> str:
    """Resolve @handle → UC... channel id (cached; the handle page is not walled)."""
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    if handle in cache:
        return cache[handle]
    html = _http(f"https://www.youtube.com/@{handle.lstrip('@')}",
                 timeout=20).decode("utf-8", "ignore")
    m = re.search(r'"externalId":"(UC[a-zA-Z0-9_-]{22})"', html)
    if not m:
        raise RuntimeError(f"could not resolve channel id for {handle}")
    cache[handle] = m.group(1)
    CACHE.write_text(json.dumps(cache, indent=1))
    return m.group(1)


def feed_entries(channel_id: str) -> list[dict]:
    xml = _http(f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}")
    root = ET.fromstring(xml)
    out = []
    for e in root.findall("a:entry", NS):
        vid = e.findtext("yt:videoId", "", NS)
        title = e.findtext("a:title", "", NS)
        pub = e.findtext("a:published", "", NS)
        desc = (e.findtext("media:description", "", NS) or "")[:1200]
        views = 0
        stats = e.find("media:group/media:community/media:statistics", NS)
        if stats is not None and stats.get("views"):
            views = int(stats.get("views"))
        out.append({"id": vid, "title": title, "published": pub,
                    "views": views, "description": desc})
    return out


def scout(min_score: float = 2.0, limit_per_channel: int = 15) -> list[dict]:
    cfg = json.loads(CONFIG.read_text())
    rows: list[dict] = []
    for ch in cfg["channels"]:
        handle = ch["handle"].lstrip("@")
        try:
            cid = channel_id_for(handle)
            entries = feed_entries(cid)[:limit_per_channel]
        except Exception as e:
            print(f"[scout] {handle}: {type(e).__name__}: {e}", file=sys.stderr)
            continue
        if not entries:
            continue
        avg = sum(e["views"] for e in entries) / len(entries)
        for e in entries:
            score = (e["views"] / avg) if avg else 0.0
            niche = bool(NICHE.search(e["title"]))
            rows.append({**e, "channel": ch["name"], "handle": f"@{handle}",
                         "score": round(score, 2), "niche": niche})
    rows.sort(key=lambda r: (not r["niche"], -r["score"]))
    return [r for r in rows if r["score"] >= min_score]


def enqueue(urls: list[str]) -> int:
    existing = {l.strip() for l in QUEUE.read_text().splitlines()}
    added = 0
    with QUEUE.open("a", encoding="utf-8") as f:
        for u in urls:
            if u not in existing:
                f.write(u + "\n")
                existing.add(u)
                added += 1
    return added


def main() -> int:
    min_score = 2.0
    do_enqueue = 0
    args = sys.argv[1:]
    if "--enqueue" in args:
        do_enqueue = int(args[args.index("--enqueue") + 1])
    if "--min-score" in args:
        min_score = float(args[args.index("--min-score") + 1])

    rows = scout(min_score=min_score)
    print(f"[scout] {len(rows)} candidates >= {min_score}x channel average\n")
    print(f"{'score':>6}  {'views':>9}  {'published':<10}  channel / title / id")
    for r in rows[:12]:
        print(f"{r['score']:>6.2f}  {r['views']:>9}  {r['published'][:10]}  "
              f"{r['handle']} | {r['title'][:60]} | {r['id']}"
              f"{'  [NICHE]' if r['niche'] else ''}")
    if do_enqueue:
        urls = [f"https://www.youtube.com/watch?v={r['id']}"
                for r in rows if r["niche"]][:do_enqueue]
        n = enqueue(urls)
        print(f"[scout] enqueued {n} new niche URLs -> config/learning_queue.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
