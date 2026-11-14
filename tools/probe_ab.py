#!/usr/bin/env python3
"""probe_ab.py — generic L-087 variant probe: render A/B frames, VLM-grade, report.

The reusable form of probe_daylight.py (L-102) / the hook A/B (L-087):
a named weak frame gets ONE variant probe at the gate's own u-moments
BEFORE any full re-render earns pipeline time.

Usage:
  python3 tools/probe_ab.py <slug> --edits <edits.json> --times 25.91 26.5 \
      [--dims vh,cl] [--label s6_variant]

edits.json: {"label": "...", "replaces": [["old exact str", "new str"], ...]}
  applied to render/scenes.html (a COPY — the source is never touched).
Report -> gate/<label>_probe.json ; PNGs -> render/probe_<label>_<t>.png
(+ baseline PNGs render/probe_<t>.png from the unmodified source).
L-096: probe PNGs live in render/, never in gate/.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parent.parent
W, H = 1080, 1920

PROMPT = ("You are a strict motion-design critic. Grade this 9:16 frame on "
          "visual_hierarchy (one dominant element, clear eye path) and "
          "contrast_legibility (text and focal read on a 6-inch daylight "
          "screen). Answer ONLY compact JSON: {\"vh\": n, \"cl\": n} with "
          "integers 1-10.")


def build(short: Path, name: str, replaces: list) -> Path:
    """Inject timeline into scenes.html, apply replaces, write <name>.html."""
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
    for old, new in replaces:
        if html.count(old) != 1:
            raise SystemExit(f"edit target not unique ({html.count(old)}x): {old[:70]}")
        html = html.replace(old, new)
    out = short / "render" / f"scenes.{name}.html"
    out.write_text(html)
    return out


def _ask(path: Path) -> dict:
    r = subprocess.run(["z-ai", "vision", "--image", str(path), "--prompt", PROMPT],
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--edits", required=True)
    ap.add_argument("--times", type=float, nargs="+", required=True)
    ap.add_argument("--label", default=None)
    a = ap.parse_args()
    short = REPO / "content" / a.slug
    spec = json.loads(Path(a.edits).read_text())
    label = a.label or spec.get("label", "variant")
    name = f"probe.{label}"
    var_html = build(short, name, spec["replaces"])
    base_html = build(short, "probe", [])  # unmodified source copy

    pngs = {"base": {}, "var": {}}
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for tag, html in (("base", base_html), ("var", var_html)):
            pg.goto(html.resolve().as_uri())
            pg.wait_for_timeout(600)
            for t in a.times:
                out = (short / "render" /
                       (f"probe_{t}.png" if tag == "base" else f"probe_{label}_{t}.png"))
                pg.evaluate(f"renderFrame({t})")
                pg.screenshot(path=str(out))
                pngs[tag][t] = out
        br.close()
    # html copies are scratch — remove (L-096 hygiene)
    var_html.unlink()
    base_html.unlink()

    res = {"label": label, "times": a.times, "replaces": spec["replaces"],
           "frames": {}, "delta_mean": None, "verdict": ""}
    deltas = []
    for t in a.times:
        b, v = _ask(pngs["base"][t]), _ask(pngs["var"][t])
        d = {k: v[k] - b[k] for k in b}
        deltas += list(d.values())
        res["frames"][str(t)] = {"baseline": b, "variant": v, "delta": d}
    res["delta_mean"] = round(sum(deltas) / len(deltas), 2)
    if res["delta_mean"] >= 0.5:
        res["verdict"] = (f"VARIANT_WINS (mean delta +{res['delta_mean']}) — bank for the "
                          "next re-render round; never mid-decision on an unchanged cut")
    elif res["delta_mean"] <= -0.5:
        res["verdict"] = f"BASELINE_HOLDS (mean delta {res['delta_mean']}) — keep current"
    else:
        res["verdict"] = f"NOISE (mean delta {res['delta_mean']}) — no integration call"
    out = short / "gate" / f"{label}_probe.json"
    out.write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
