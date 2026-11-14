#!/usr/bin/env python3
"""lint_selftest.py — regression guard for script_linter structure rules.

Day-017 found the L-073/L-075/L-077 block was DEAD for JSON scripts (the
dispatcher flattened scripts to narration text, so lint() never saw the
scene JSON — every script since day-008 'passed lint' with the structure
rules silently off). This selftest pins:

  A. deadproof fixture        -> L-073 + L-075 + L-097 all fire
  B. 11-beat #0005 (day-013)  -> L-097 fires (the gate-time failure class)
  C. digits in narration      -> L-090 fires (L-090 class)
  D. real #0005 script.json   -> PASS, 12 beats / 12 required, no L-090
  E. plain-text input         -> 'no scene JSON' warn, no crash

Run: python3 tools/lint_selftest.py  (exit 0 = all green)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from script_linter import lint  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
S5 = json.loads((REPO / "content/short-0005/script.json").read_text())

FAILS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    print(f"  {'ok ' if cond else 'FAIL'} {name}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        FAILS.append(name)


def run(payload, fmt="short", dur=None):
    flat = " ".join([payload["hook"]["narration"]] +
                    [s.get("narration") or "" for s in payload["scenes"]])
    return lint(flat, fmt, dur, data=payload)


print("A. deadproof fixture (off-topic hook, 8s scenes)")
A = {
    "title": "Quantum tornado engines",
    "hook": {"timestamp_start": 0.0, "narration": "Something completely unrelated opens this video."},
    "scenes": [{"timestamp_start": 0.0, "narration": "First line of narration here."},
               {"timestamp_start": 8.0, "narration": "Second line of narration here."},
               {"timestamp_start": 16.0, "narration": "Third line of narration here."}],
    "timeline": {"total_s": 24.0}}
rA = run(A)
check("L-073 fires", any("L-073" in f for f in rA["fails"]), str(rA["fails"]))
check("L-075 mean-scene fires", any("mean scene" in f for f in rA["fails"]))
check("L-097 fires (4 beats < 8)", any("L-097" in f for f in rA["fails"]))

print("B. 11-beat #0005 (day-013 gate-time failure must die at lint)")
B = json.loads(json.dumps(S5))
B["scenes"] = B["scenes"][:-1]  # drop the visual-only 12th beat
rB = run(B)
check("L-097 fires (11 < 12)", any("L-097" in f for f in rB["fails"]), str(rB["fails"]))

print("C. digits in narration (L-090)")
C = json.loads(json.dumps(S5))
C["scenes"][0]["narration"] = "In 1883, Krakatoa was an island near Java."
rC = run(C)
check("L-090 fires on '1883'", any("L-090" in f and "1883" in f for f in rC["fails"]), str(rC["fails"]))

print("D. real #0005 script (12 beats, words-not-digits)")
rD = run(S5, dur=S5["timeline"]["total_s"])  # pipeline passes --duration-s = total_s
check("verdict PASS", rD["verdict"] == "PASS", str(rD["fails"]))
check("beats 12 / required 12", rD["beats"] == 12 and rD["beats_required"] == 12,
      f"{rD['beats']}/{rD['beats_required']}")
check("at-floor warn present", any("beat floor" in w for w in rD["warns"]))
check("no L-090", not any("L-090" in f for f in rD["fails"]))

print("E. plain-text input (no scene JSON)")
rE = lint("The loudest sound ever: an island that blew itself apart. In eighteen eighty three it erupted.",
          "short", None, data=None)
check("unchecked warn present", any("no scene JSON" in w for w in rE["warns"]))

print(f"\n{'ALL GREEN' if not FAILS else 'FAILED: ' + ', '.join(FAILS)}")
sys.exit(1 if FAILS else 0)
