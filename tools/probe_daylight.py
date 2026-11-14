#!/usr/bin/env python3
"""probe_daylight.py — carry_r3 D3: isolate the dark-world hypothesis.

Renders the SAME s6 frame twice: once as committed (night palette) and once
with a daylight/warm-sky token override (bible-legal warm variant). Then
VLM-grades BOTH stills on visual_hierarchy + contrast_legibility (1-10) and
reports the delta. If daylight scores >=1.0 higher, the night palette
carries a structural penalty on this judge and the next short gets a
daylight world (carry_r3 D3 decision rule).

Usage: python3 tools/probe_daylight.py <slug> <t>
Writes gate/day_night_probe.json + the two probe PNGs in render/.
"""
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parent.parent
W, H = 1080, 1920

DAY_OVERRIDE = {
    "skyTop": "#3E5E96", "skyMid": "#7B8FC4", "skyLow": "#E8A06B",
    "horizon": "#FFC98A", "dawnBand": "#FFD9A0",
    "seaFar": "#3E6FA8", "seaMid": "#4A7CB8", "seaNear": "#3A6BA4",
    "foam": "#CFE2F2",
}


def build(short: Path) -> Path:
    script = json.loads((short / "script.json").read_text())
    tl = [{"id": "hook", "start": script["hook"]["timestamp_start"],
           "end": script["scenes"][0]["timestamp_start"]}]
    for i, sc in enumerate(script["scenes"]):
        end = (script["scenes"][i + 1]["timestamp_start"]
               if i + 1 < len(script["scenes"]) else script["timeline"]["total_s"])
        tl.append({"id": f"s{i}", "start": sc["timestamp_start"], "end": end})
    tpl = (short / "render" / "scenes.html").read_text()
    html = tpl.replace("__TIMELINE__", json.dumps(tl)).replace(
        "__T_END__", json.dumps(tl[-1]["end"]))
    out = short / "render" / "scenes.probe.html"
    out.write_text(html)
    return out


def day_variant(src: Path) -> Path:
    html = src.read_text()
    block = re.search(r"const NIGHT = \{(.*?)\};", html, re.S).group(1)
    repl = ",\n".join(f'  {k}: "{v}"' for k, v in DAY_OVERRIDE.items())
    html = html.replace(block, "\n" + repl + ",\n")
    out = src.with_name("scenes.probe_day.html")
    out.write_text(html)
    return out


def shot(page, t: float, path: Path) -> None:
    page.evaluate(f"renderFrame({t})")
    page.screenshot(path=str(path))


def _ask(path: Path) -> dict:
    import subprocess
    prompt = ("You are a strict motion-design critic. Grade this 9:16 frame on "
              "visual_hierarchy (one dominant element, clear eye path) and "
              "contrast_legibility (text and focal read on a 6-inch daylight "
              "screen). Answer ONLY compact JSON: {\"vh\": n, \"cl\": n} with "
              "integers 1-10.")
    r = subprocess.run(["z-ai", "vision", "--image", str(path), "--prompt", prompt],
                       capture_output=True, text=True, timeout=180)
    try:
        blob = r.stdout[r.stdout.index("{"): r.stdout.rindex("}") + 1]
        payload = json.loads(blob)
        content = payload["choices"][0]["message"]["content"]
    except Exception:
        raise RuntimeError(f"probe call failed: {r.stdout[-300:]}")
    m = re.search(r"\{[^{}]*\"vh\"[^{}]*\}", content, re.S)
    if not m:
        raise RuntimeError(f"no JSON in probe answer: {content[:300]}")
    return json.loads(m.group(0))


def grade(img_a: Path, img_b: Path) -> dict:
    return {"night": _ask(img_a), "day": _ask(img_b)}


def main() -> int:
    slug, t = sys.argv[1], float(sys.argv[2])
    short = REPO / "content" / slug
    base = build(short)
    day = day_variant(base)
    pn = short / "render" / "probe_day_night.png"
    pd = short / "render" / "probe_day_light.png"
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.goto(base.resolve().as_uri())
        pg.wait_for_timeout(600)
        shot(pg, t, pn)
        pg.goto(day.resolve().as_uri())
        pg.wait_for_timeout(600)
        shot(pg, t, pd)
        br.close()
    res = grade(pn, pd)
    res["frame_t"] = t
    res["delta"] = {k: res["day"][k] - res["night"][k] for k in res["night"]}
    verdict = ("DAYLIGHT_WINS >=1.0 — next short gets a daylight world"
               if (res["delta"]["vh"] + res["delta"]["cl"]) / 2 >= 1.0
               else "NIGHT holds — no structural palette penalty measured")
    res["verdict"] = verdict
    out = short / "gate" / "day_night_probe.json"
    out.write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
