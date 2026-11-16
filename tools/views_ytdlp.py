#!/usr/bin/env python3
"""views_ytdlp.py — view-count capture when the RSS feed is walled (day-019).

Why this exists (2026-11-16): the channel feed 404s from every non-runner IP
we've seen (studio 2026-11-15 ×3, fresh sandbox ×3 + curl; playlist variant
too), and the sandbox class is hard-walled for yt-dlp default AND rotated
player clients ("Sign in to confirm you're not a bot"). GitHub-hosted runners
are fresh IPs — the daily-loop transcribe matrix wins there (android leg,
2026-11-16), so the views workflow runs this on a runner.

Ladder: player_client rotation android → mweb → tv → default (L-049: client
diversity only helps on fresh IPs). Video list: content/short-*/published.json
(canonical). Merge: shared with views_tracker.py (idempotent per day, history
kept since day-019).

Usage: python3 tools/views_ytdlp.py   (exit 1 if every client is walled)
"""
from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from views_tracker import REPO, merge_today, write_rows  # noqa: E402

CLIENTS = ["android", "mweb", "tv", ""]


def published_shorts() -> list[dict]:
    out = []
    for p in sorted((REPO / "content").glob("short-*/published.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        d["source"] = p.parent.name
        out.append(d)
    return out


def view_count(video_id: str, client: str) -> int | None:
    cmd = ["yt-dlp", "--skip-download", "--js-runtimes", "node",
           "--print", "%(view_count)s"]
    if client:
        cmd += ["--extractor-args", f"youtube:player_client={client}"]
    try:
        r = subprocess.run(cmd + [f"https://www.youtube.com/watch?v={video_id}"],
                           capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return None
    lines = [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]
    if r.returncode == 0 and lines and lines[-1].isdigit():
        return int(lines[-1])
    return None


def main() -> int:
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    vids = published_shorts()
    if not vids:
        sys.exit("[views] no content/short-*/published.json found")

    for client in CLIENTS:
        label = client or "default"
        print(f"[views] yt-dlp ladder: client={label}")
        got: dict[str, int] = {}
        for s in vids:
            v = view_count(s["video_id"], client)
            if v is None:
                print(f"[views]   {s['video_id']} FAIL — next client")
                got = {}
                break
            got[s["video_id"]] = v
            print(f"[views]   {s['video_id']}  {v:>7,}  {s['source']}")
        if len(got) == len(vids):
            fresh = [[today, s["video_id"], s["title"], str(got[s["video_id"]]),
                      s["published_at"][:10]] for s in vids]
            write_rows(merge_today(fresh, today))
            print(f"[views] wrote {len(fresh)} rows for {today} via yt-dlp/{label}")
            return 0

    sys.exit("[views] yt-dlp ladder exhausted — every client walled from this IP")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
