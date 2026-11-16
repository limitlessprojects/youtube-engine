#!/usr/bin/env python3
"""contact_sheet.py — render probe frames and tile them into ONE image for eye review.

Usage:
  tools/contact_sheet.py <slug> <out.jpg> t1 t2 t3 ...     # explicit times (s)
  tools/contact_sheet.py <slug> <out.jpg> --every 1.5      # whole timeline, fixed step
  tools/contact_sheet.py <slug> <out.jpg> --scenes         # 2 frames per scene (u=.3,.8)
  options: --cols N (default 6)  --errors (also walk the timeline and print JS errors)

Why (day-018): an agent that can SEE images judges a 6-12 frame sheet in one read —
far cheaper and steadier than per-frame VLM calls (L-080/L-101 noise). Probes land in
render/ (never gate/, L-096). Needs ImageMagick (`magick`).
"""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_short as rs
from playwright.sync_api import sync_playwright


def main() -> int:
    a = sys.argv[1:]
    if len(a) < 3:
        print(__doc__); return 2
    slug, out = a[0], Path(a[1]); rest = a[2:]
    cols = 6
    if "--cols" in rest:
        i = rest.index("--cols"); cols = int(rest[i + 1]); del rest[i:i + 2]
    errors = "--errors" in rest
    rest = [x for x in rest if x != "--errors"]
    short = rs.REPO / "content" / slug
    tl = rs.build_timeline(short)
    html = rs.build_html(short, tl)
    if rest[0] == "--every":
        step = float(rest[1]); times = []; t = 0.0
        while t < tl[-1]["end"]:
            times.append(round(t, 2)); t += step
    elif rest[0] == "--scenes":
        times = [round(s["start"] + u * (s["end"] - s["start"]), 2) for s in tl for u in (0.3, 0.8)]
    else:
        times = [float(x) for x in rest]
    tmp = short / "render" / "_sheet"; tmp.mkdir(parents=True, exist_ok=True)
    files, errs = [], []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": rs.W, "height": rs.H}, device_scale_factor=1)
        pg.on("pageerror", lambda e: errs.append(str(e)[:300]))
        pg.goto(html.resolve().as_uri()); pg.wait_for_timeout(350)
        try:
            pg.wait_for_function("document.fonts.status === 'loaded'", timeout=10000)
        except Exception:
            print("fonts: timeout")
        if errors:
            t = 0.0
            while t < tl[-1]["end"]:
                try:
                    pg.evaluate(f"renderFrame({t})")
                except Exception as e:
                    errs.append(f"t={t:.2f}: {str(e)[:240]}")
                t += 0.25
        for t in times:
            f = tmp / f"t{str(t).replace('.', '_')}.png"
            try:
                pg.evaluate(f"renderFrame({t})")
            except Exception as e:
                errs.append(f"t={t}: {str(e)[:240]}")
            pg.screenshot(path=str(f)); files.append(str(f))
        b.close()
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["magick", "montage", *files, "-tile", f"{cols}x", "-geometry", "360x640+4+4",
                    "-background", "#222", str(out)], check=True)
    print(f"sheet -> {out}  times={times}")
    print("JS errors:", errs[:10] if errs else "none")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
