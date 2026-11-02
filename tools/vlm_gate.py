#!/usr/bin/env python3
"""VLM frame gate for a short's keyframes (prompts/vlm_inspector.md).

Usage: tools/vlm_gate.py <slug> [--scene s3] [--round N]

For each gate/*.png, asks the vision model to run the inspector checklist
against the scene intent (narration + visual tag), parses the strict-JSON
verdict, and writes gate/report.json. The loop controller (human or agent)
applies fix hints to render/scenes.html and re-runs --keyframes for failed
scenes only. Hard cap: N=2 re-renders per scene (architecture guardrail).
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

CHECKLIST = """You are the VLM Inspector for a costume-rig YouTube Short (1080x1920 vertical).
Inspect the rendered frame against the scene intent. You inspect; you never redesign.

Scene intent: narration = "{narration}"
Visual spec: pose={pose}, prop={prop}, background={background}
Composition note (authoritative): {note}

Checklist:
1. text_collision: caption words overlapping the character, props, or each other?
   Captions must sit in the bottom-20% zone (y > 1536); characters in the central band.
2. anchoring: character feet on a surface (ground, platform, deck) with a contact
   shadow? floating = fail (except characters deliberately in space/air, e.g. falling).
3. drift: consistent character design (navy hoodie, cream face/limbs, teal shoes),
   chunky shapes, palette = deep navy + amber/teal/blue accents?
4. asset_match: does the frame visibly show what the narration names?
5. readability: caption readable? enough contrast against the background?
6. clutter: more than one focal subject?
7. light: does the frame have a visible light source / glow / depth (no flat void)?
8. animated counters: a count-up readout may legitimately show an intermediate value
   mid-scene (e.g. '58% EMPTY' climbing to '99.9999...%'). Only flag it if the FINAL
   value would be wrong, not for intermediate frames of a counting animation.

Return STRICT JSON only (no prose), schema:
{{"scene": "{sid}", "verdict": "pass" | "fix",
  "issues": [{{"check": "...", "severity": "high|medium|low",
    "bbox": [ymin, xmin, ymax, xmax], "fix_hint": "..."}}]}}
bbox in pixels of the 1080x1920 frame. If everything is fine: verdict "pass", issues []."""


NOTES = {
    "hook": "night street set (lamp light, buildings, moon); rig character peers into his own hoodie pocket where a small black hole (dark core, amber accretion arcs, photon ring, glow) has appeared; blurred foreground edges for depth",     "s0": "macro insert: a big magnifier over the pocket; the coin-sized hole (accretion arcs) sits inside the lens; '≈ 1 CM' mono tag pops; character curious at left",     "s1": "space: a balance scale compares the tiny hole (left pan) against planet Earth (right pan); nebula depth layers; character points up from a deck",     "s2": "cross-section cutaway: the hole falls from the surface through labeled layers (floor/sidewalk/rock) leaving an amber dashed trail; the character is a spectator standing on the lawn edge at upper-left - standing is correct",     "s3": "Kurzgesagt atom diagram: chunky broken orbit rings (teal/blue/purple), glowing amber nucleus, electron dots; blueprint grid + registration marks; counting readout '99.9999...% EMPTY' (a counting animation); character amazed, eyes glinting cyan from u~0.3",     "s4": "the hole loops the planet on a chunky broken orbit ring whose near-side arc crosses the planet (through the core); jagged amber cracks accumulate per pass; PASS 0x/04 chip; shocked character on a deck",     "s5": "the hole eats Earth slowly: atoms trickle one by one along the dashed amber path (flow chevrons point at the hole); '1 ATOM AT A TIME' tag; calm character; night-side Earth (dark crescent + amber city lights) with dim atmosphere",     "s6": "Earth shrinks with fold chords, amber shockwave rings and compression spokes and collapses into a marble with amber rings; shocked character on a deck",     "s7": "mirror of the hook: character smugly shows the open pocket flap is empty ('NOTHING.' tag); fade to black at the end", }


def load_intents(short: Path) -> dict:
    script = json.loads((short / "script.json").read_text())
    intents = {"hook": {"narration": script["hook"]["narration"],
                        "pose": "peerdown", "prop": "pocket+glow", "background": "street"}}
    for i, sc in enumerate(script["scenes"]):
        v = sc.get("visual", {})
        intents[f"s{i}"] = {"narration": sc["narration"], "pose": v.get("pose"),
                            "prop": v.get("prop"), "background": v.get("background")}
    return intents


def extract_json(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError("no JSON in response")
    return json.loads(m.group(0))


def unwrap(raw: str) -> str:
    """z-ai vision writes a chat-completion envelope; get message.content."""
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict) and "choices" in obj:
            return obj["choices"][0]["message"]["content"]
        if isinstance(obj, dict) and "content" in obj:
            return obj["content"]
    except json.JSONDecodeError:
        pass
    return raw


def main() -> int:
    slug = sys.argv[1]
    short = REPO / "content" / slug
    gate = short / "gate"
    intents = load_intents(short)
    only = None
    if "--scene" in sys.argv:
        only = sys.argv[sys.argv.index("--scene") + 1]
    rnd = "1"
    if "--round" in sys.argv:
        rnd = sys.argv[sys.argv.index("--round") + 1]

    report_path = gate / "report.json"
    report = json.loads(report_path.read_text()) if report_path.exists() else {"frames": {}}

    frames = sorted(gate.glob("*.png"))
    if only:
        frames = [f for f in frames if f.stem.startswith(only + "_")]
    for f in frames:
        sid = f.stem.split("_")[0]
        intent = intents.get(sid, {})
        prompt = CHECKLIST.format(narration=intent.get("narration", "?"),
                                  pose=intent.get("pose"), prop=intent.get("prop"),
                                  background=intent.get("background"), sid=sid,
                                  note=NOTES.get(sid, "(none)"))
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "v.json"
            verdict = None
            for attempt in range(3):   # SDK sometimes returns empty/init noise
                r = subprocess.run(["z-ai", "vision", "-p", prompt, "-i", str(f),
                                    "-o", str(out)], capture_output=True, text=True, timeout=240)
                raw = out.read_text() if out.exists() else r.stdout
                try:
                    verdict = extract_json(unwrap(raw))
                    break
                except (ValueError, json.JSONDecodeError, KeyError, TypeError):
                    import time
                    time.sleep(4 * (attempt + 1))
            if verdict is None:
                verdict = {"scene": sid, "verdict": "fix",
                           "issues": [{"check": "vlm_parse", "severity": "medium",
                                       "bbox": None, "fix_hint": raw[:400]}]}
        verdict["_frame"] = f.name
        verdict["_round"] = rnd
        report["frames"][f.name] = verdict
        iss = verdict.get("issues", [])
        print(f"[{f.name}] {verdict.get('verdict','?').upper()}"
              + (f"  {len(iss)} issue(s)" if iss else ""))
        for i in iss:
            print(f"    - {i.get('check')}/{i.get('severity')}: {i.get('fix_hint','')[:110]}")
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    n_fix = sum(1 for v in report["frames"].values() if v.get("verdict") != "pass")
    print(f"\nreport: {report_path}  ({len(report['frames'])} frames, {n_fix} not-pass)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
