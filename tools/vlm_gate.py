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

CHECKLIST = """You are the VLM Inspector for a stick-figure YouTube Short (1080x1920 vertical).
Inspect the rendered frame against the scene intent. You inspect; you never redesign.

Scene intent: narration = "{narration}"
Visual spec: pose={pose}, prop={prop}, background={background}
Composition note (authoritative): {note}

Checklist:
1. text_collision: caption words overlapping the character, props, or each other?
   Captions must sit in the bottom-20% zone (y > 1536); characters in the central band.
2. anchoring: stickman feet on a surface (ground line or platform)? floating = fail.
3. drift: consistent white stickman style, single amber accent?
4. asset_match: does the frame visibly show what the narration names?
5. readability: caption readable? enough contrast?
6. clutter: more than one focal subject?

Return STRICT JSON only (no prose), schema:
{{"scene": "{sid}", "verdict": "pass" | "fix",
  "issues": [{{"check": "...", "severity": "high|medium|low",
    "bbox": [ymin, xmin, ymax, xmax], "fix_hint": "..."}}]}}
bbox in pixels of the 1080x1920 frame. If everything is fine: verdict "pass", issues []."""


NOTES = {
    "hook": "stickman looks down at his own jacket pocket, where a small black hole"
            " (dark void, thin amber ring, faint glow) has appeared",
    "s0": "stickman inspects the coin-sized hole through a magnifying glass",
    "s1": "a balance scale compares the tiny hole (left pan) against planet Earth"
          " (right pan); stickman points up at the scale",
    "s2": "the FALLING element is the black hole itself: it drops from the open hand"
          " at the top through labeled rock layers (floor/sidewalk/rock), leaving an"
          " amber dashed trail; the stickman is a spectator watching from the ledge"
          " at upper-left — spectator standing is correct",
    "s3": "an atom diagram (tiny nucleus, electron orbits, vast empty boundary)"
          " explains why matter is mostly empty space",
    "s4": "the hole loops the planet on a dashed orbit ellipse through the core;"
          " amber cracks accumulate on the crust after each pass",
    "s5": "the hole eats Earth slowly: white atoms trickle one by one along the"
          " dashed amber path into the hole; stickman watches calmly",
    "s6": "Earth shrinks with accordion fold lines and collapses into a small"
          " marble-sized planet with an amber rim; 'shocked' pose = arms thrown up",
    "s7": "mirror of the hook: stickman smugly shows the pocket is now empty"
          " ('nothing.' bubble); fade to black at the end",
}


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
