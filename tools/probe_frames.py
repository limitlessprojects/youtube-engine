#!/usr/bin/env python3
"""Quick visual probe: render N probe frames of scenes.built.html, catching JS errors."""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parent.parent
short = REPO / "content" / "short-0001"
script = json.loads((short / "script.json").read_text())
tl = [{"id": "hook", "start": script["hook"]["timestamp_start"],
       "end": script["scenes"][0]["timestamp_start"], "narration": script["hook"]["narration"]}]
for i, sc in enumerate(script["scenes"]):
    end = (script["scenes"][i + 1]["timestamp_start"] if i + 1 < len(script["scenes"])
           else script["timeline"]["total_s"])
    tl.append({"id": f"s{i}", "start": sc["timestamp_start"], "end": end, "narration": sc["narration"]})
tpl = (short / "render" / "scenes.html").read_text()
html = tpl.replace("__TIMELINE__", json.dumps(tl)).replace("__T_END__", json.dumps(tl[-1]["end"]))
out = short / "render" / "scenes.built.html"
out.write_text(html)

times = [float(x) for x in sys.argv[1:]] or [1.2, 4.5, 8.0, 11.5, 16.0, 20.5, 27.0, 34.0, 38.6]
errors = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
    page.goto(out.resolve().as_uri())
    try:
        page.wait_for_function("document.fonts.status === 'loaded'", timeout=10000)
        print("fonts: loaded")
    except Exception:
        print("fonts: TIMEOUT (fallbacks in use)")
    for t in times:
        page.evaluate(f"renderFrame({t})")
        page.screenshot(path=str(short / "render" / f"probe_{str(t).replace('.', '_')}.png"))
        print(f"  t={t} ok")
    browser.close()
if errors:
    print("ERRORS:")
    for e in errors[:12]:
        print("  ", e)
else:
    print("NO JS ERRORS")
