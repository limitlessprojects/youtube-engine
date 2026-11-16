#!/usr/bin/env python3
"""watch_video.py — let an image-reading agent "watch" a finished video.

An agent cannot play a file. This is the closest honest substitute: the video tiled at
10 fps into a few sheets (every 3rd frame, in order, 12 per row) plus measured motion and
audio numbers. Read the sheets left-to-right like a filmstrip. It still is NOT hearing the
audio — say so in whatever you write (dead-end D8).

Usage:
  tools/watch_video.py <slug|video-file|youtube-url> [--out DIR] [--fps 10]

  slug        -> content/<slug>/<slug>.mp4
  youtube-url -> downloaded with yt-dlp (watch the LIVE upload, not your local copy)

Prints: sheet paths, per-second motion classes (via tools/motion_probe.py), the seconds
where the picture is dead, integrated loudness / true peak, and clipping count.
"""
import json, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def main() -> int:
    a = sys.argv[1:]
    if not a:
        print(__doc__); return 2
    src = a[0]
    out = Path(a[a.index("--out") + 1]) if "--out" in a else REPO / "content" / "_watch"
    fps = int(a[a.index("--fps") + 1]) if "--fps" in a else 10
    out.mkdir(parents=True, exist_ok=True)
    if src.startswith("http"):
        for old in out.glob("live.*"):
            old.unlink()
        subprocess.run(["yt-dlp", "-q", "-f", "bv*+ba/b", "-o", str(out / "live.%(ext)s"), src], timeout=300)
        vids = sorted(out.glob("live.*"))
        if not vids:
            print("download failed (bot wall?) — fall back to the local mp4"); return 1
        video = vids[0]
    elif Path(src).exists():
        video = Path(src)
    else:
        video = REPO / "content" / src / f"{src}.mp4"
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                               capture_output=True, text=True).stdout.strip())
    sheets, t = [], 0.0
    while t < dur:
        f = out / f"watch_{int(t):03d}s.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-t", "10", "-i", str(video), "-vf",
                        f"fps={fps},scale=180:320,tile=12x9:padding=3", "-frames:v", "1", "-q:v", "3", str(f)], check=True)
        sheets.append(str(f)); t += 10
    print(f"video: {video}  ({dur:.2f}s)\nsheets ({fps} fps, 12 per row = {12 / fps:.1f}s per row):")
    for s in sheets:
        print("  ", s)
    r = subprocess.run([sys.executable, str(REPO / "tools" / "motion_probe.py"), str(video), "--format", "json"],
                       capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
        beats = [b for b in d["beats"] if b["frames"] > 3]
        cls = {}
        for b in beats:
            cls[b["classification"]] = cls.get(b["classification"], 0) + 1
        dead = [f"{b['start']:.0f}-{b['end']:.0f}s" for b in beats if b["classification"] == "dead"]
        print(f"motion: median beat energy {d['median_beat_motion']:.4f} (probe target >= 0.01) | {cls} of {len(beats)} seconds")
        print("dead seconds:", ", ".join(dead) or "none")
    except Exception as e:
        print("motion_probe failed:", e)
    ln = subprocess.run(["ffmpeg", "-v", "info", "-i", str(video), "-af", "loudnorm=print_format=summary", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    for line in ln.splitlines():
        if "Input Integrated" in line or "Input True Peak" in line:
            print("audio:", line.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
