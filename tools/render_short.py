#!/usr/bin/env python3
"""Render a short's scenes.html (seek-driven SVG) to PNG frames.

Usage:
  tools/render_short.py <slug> --keyframes   # gate frames at scene midpoints (+u .25/.75 if long)
  tools/render_short.py <slug> --full        # every frame at FPS
  tools/render_short.py <slug> --times 3.2 7.9   # arbitrary probe frames
  tools/render_short.py <slug> --frames 0 60     # render frames [0, 60) (AI-rerender chunks)

Builds render/scenes.built.html by injecting the synced timeline from
script.json into render/scenes.html, then drives renderFrame(t) via
Playwright (chromium, 1080x1920 — Shorts vertical).
"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parent.parent
FPS = 30
W, H = 1080, 1920


def build_timeline(short: Path) -> list[dict]:
    script = json.loads((short / "script.json").read_text())
    starts = [("hook", script["hook"]["timestamp_start"], script["hook"]["narration"])]
    for sc in script["scenes"]:
        starts.append((f"s{sc.get('index', len(starts)-1)}" if False else None,
                       sc["timestamp_start"], sc["narration"]))
    # id convention: hook, then s0..s7 (visual spec keys in scenes.html)
    tl = [{"id": "hook", "start": script["hook"]["timestamp_start"],
           "end": script["scenes"][0]["timestamp_start"],
           "narration": script["hook"]["narration"]}]
    for i, sc in enumerate(script["scenes"]):
        end = (script["scenes"][i + 1]["timestamp_start"]
               if i + 1 < len(script["scenes"])
               else script["timeline"]["total_s"])
        tl.append({"id": f"s{i}", "start": sc["timestamp_start"],
                   "end": end, "narration": sc["narration"]})
    return tl


def build_html(short: Path, tl: list[dict]) -> Path:
    tpl = (short / "render" / "scenes.html").read_text()
    t_end = tl[-1]["end"]
    marker = ("<!-- STYLE_PREFIX: register=reserved (engine/core.js V2.REGISTERS, boss-flip only); "
              "bible=content/style-bible.md; verdicts=gate/ultracritic_r*.json; "
              "no new register/token/style change without boss directive -->\n")
    html = tpl.replace("__TIMELINE__", json.dumps(tl)).replace("__T_END__", json.dumps(t_end))
    if "<head>" in html and "STYLE_PREFIX" not in html:
        html = html.replace("<head>", "<head>\n" + marker, 1)
    out = short / "render" / "scenes.built.html"
    out.write_text(html)
    return out


def shot(page, t: float, path: Path) -> None:
    page.evaluate(f"renderFrame({t})")
    page.screenshot(path=str(path))


def main() -> int:
    slug = sys.argv[1]
    short = REPO / "content" / slug
    tl = build_timeline(short)
    html = build_html(short, tl)
    mode = sys.argv[2] if len(sys.argv) > 2 else "--keyframes"

    if mode == "--times":
        times = [float(x) for x in sys.argv[3:]]
        jobs = [(t, short / "render" / f"probe_{str(t).replace('.', '_')}.png") for t in times]
    elif mode == "--keyframes":
        gate = short / "gate"
        gate.mkdir(exist_ok=True)
        jobs = []
        for sc in tl:
            dur = sc["end"] - sc["start"]
            us = [0.5] if dur <= 4.5 else [0.25, 0.6, 0.9]
            for u in us:
                t = sc["start"] + u * dur
                jobs.append((t, gate / f"{sc['id']}_u{int(u*100):02d}.png"))
    elif mode == "--frames":
        a, b = int(sys.argv[3]), int(sys.argv[4])
        frames = short / "render" / "frames"
        frames.mkdir(parents=True, exist_ok=True)
        t_end = tl[-1]["end"]
        jobs = [(min(i / FPS, t_end), frames / f"f{i:04d}.png") for i in range(a, b)]
    elif mode == "--full":
        frames = short / "render" / "frames"
        frames.mkdir(parents=True, exist_ok=True)
        t_end = tl[-1]["end"]
        n = int(round((t_end + 0.45) * FPS))   # tail pad: hold black after fade
        jobs = [(min(i / FPS, t_end), frames / f"f{i:04d}.png") for i in range(n)]
        if "--resume" in sys.argv:
            before = len(jobs)
            jobs = [(t, f) for (t, f) in jobs if not (f.exists() and f.stat().st_size > 1000)]
            print(f"  resume: {before - len(jobs)} frames already on disk, {len(jobs)} to go", flush=True)
    else:
        print(__doc__)
        return 2

    url = html.resolve().as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        page.goto(url)
        page.wait_for_timeout(350)
        try:
            page.wait_for_function("document.fonts.status === 'loaded'", timeout=10000)
        except Exception:
            print("  fonts: timeout — falling back to system faces", flush=True)
        for i, (t, path) in enumerate(jobs):
            shot(page, t, path)
            if mode == "--full" and i % 120 == 0:
                print(f"  frame {i}/{len(jobs)}", flush=True)
        browser.close()
    print(f"DONE {len(jobs)} frames -> {jobs[0][1].parent}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
