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
    "hook": "dusk world: gradient sky (deep blue to horizon orange), sun glow, stars, treeline silhouettes; the sky is FULL of birds — a dense swirling murmuration mass plus a higher sheet of stragglers; the stickman hero (navy hoodie, cream face, teal shoes, orange scarf) stands small on the dark field bottom-left, head tilted back gawking up, one hand raised; one bird swoops low over him; the mass haze blob behind the flock is by design (reads as one creature)",
    "s0": "PURE SKY SHOT — no character in this scene BY DESIGN (the script intent's 'sky-shot' pose means exactly that). The murmuration mass twists mid-frame (soft dark haze blob under the birds is by design). The near-miss (two birds + amber spark) only appears in the LAST ~40% of the scene — early-beat frames legitimately show only the flock. Hills/treeline are the consistent dusk world in every scene.",
    "s1": "collision-avoidance diagram over the dusk sky on a dark stage panel. The two feature birds are CREAM-BODIED (lit by the dusk light — dark silhouettes would vanish on the dark panel; this is by design) with amber beak, amber rim and dark eye; they close head-on along dashed amber trails. At ~2.3s two stamp cards pop in (CARD 1 VEER / CARD 2 ALTITUDE) — early-beat frames before 2.3s legitimately show NO cards. Then the birds fork apart — left bird breaks down-right, right bird up-left (top-down chirality). Both birds are present throughout; the cream bodies sit at both trail ends. Tags 'VEER RIGHT' and 'NEVER THE SAME HEIGHT' pop late. Hero presents from bottom-left with orange scarf.",
    "s2": "FOUR fast stamp beats (word-timed, ~1s each — v3 cut-rate spec): a given keyframe shows ONLY the beat active at its timestamp: beat 1 struck-through chat bubbles 'NO NEGOTIATION' (0-0.66s), beat 2 struck-through sound waves 'NO CHATTER' (0.66-1.32s), beat 3 big 'JUST THE RULE' card (1.32-2.31s), beat 4 six checked birds + 'EVERY BIRD. EVERY TIME.' (2.31s+). Earlier beats are gone in later frames BY DESIGN. Hero nods mid-right with scarf.",
    "s3": "THE insight diagram on a dark stage panel: one big CREAM feature bird center (cream = lit by design; amber beak + amber rim + dark eye) with a teal glow, exactly SEVEN smaller blue-gray birds around it, each connected by a glowing teal link that DRAWS ON one by one over ~2.5s — early-beat frames legitimately show fewer than seven links (animation in progress; gate the end-state at u60+). A dim background murmuration (low opacity, by design = 'not the flock'). Late: 'NOT THE FLOCK' (on a dark scrim) struck through, then a huge bright teal 'SEVEN.' pops. Hero amazed mid-left with cyan eye glint. NOTE: bottom captions are the SAME cream color as the hero — do not mistake caption words inside the bottom-20% band for the hero's limbs; the hero stands with feet at y~1520, clear of the caption band.",
    "s4": "the ripple: a band of ~52 birds in 4 flowing rows (dark silhouettes on the LIT dusk sky — correct contrast here, no panel in this scene); a glowing amber wavefront arc sweeps left→right — birds behind the front are turned (angled) with amber flash halos at the front. The origin bird at left is CREAM (the lit protagonist). Late: two stamp cards '1 SYSTEM' and '1 MOVE'. Hero leans in mid-right. NOTE: caption words are cream-colored and sit in the bottom 20% band — they are captions, not character limbs; the hero's feet end at y~1520.",
    "s5": "THREE fast beats (word-timed): a given keyframe shows ONLY the beat active at its timestamp — beat 1 struck-through control-tower stamp 'NO TOWERS' (0-0.64s), beat 2 struck-through radar-dish stamp 'NO RADAR' (0.64-1.28s), beat 3 payoff: seven CREAM birds in a warm glow ring + glowing 'ONE RULE' card + 'SEVEN FRIENDS' tag (1.28s+). Earlier beats are ABSENT in later frames BY DESIGN (fast cuts) — do not flag their absence in the payoff beat, and vice versa. Hero points up mid-left.",
    "s6": "the loop-out mirror: dusk street with three cars in a traffic jam (brake lights red, exhaust puffs); hero at the wheel of the closest car (visible in the window, orange scarf, tired face); one bird flies past arrow-straight above the jam; the camera tilts UP at the end and the sky fills with the murmuration again (mirroring the hook frame — the loop); birds fading in during the tilt are by design",
}


def load_notes(short: Path) -> dict:
    """Per-short scene notes (gate/notes.json) override the built-in #0002 set
    (day-009: hardcoded #0002 notes made the gate flag short-0003's frames
    against ANOTHER VIDEO's design — the verifier must know the intent)."""
    f = short / "gate" / "notes.json"
    if f.exists():
        return json.loads(f.read_text())["notes"]
    return NOTES


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
    NOTES_LOCAL = load_notes(short)
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
                                  note=NOTES_LOCAL.get(sid, "(none)"))
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
