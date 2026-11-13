#!/usr/bin/env python3
"""L-087 probe-first hook selection: score N hook-frame candidates with the
same judge the gate uses (glm-4.6v via z-ai CLI), neutral prompt (L-066 —
never name the intended winner, never ask "which did the author mean").

Usage: tools/probe_hook.py <img1> <img2> [...]
Prints per-frame hook_impact scores + the winner; exit 0 always (probe only).
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

PROMPT = """You are a neutral thumbnail judge for vertical Shorts (1080x1920).
Score EACH image 1-10 on hook_impact: would this frame STOP a thumb-scrolling
viewer in under half a second? Instant single focal point, intrigue, readable
at tiny size. Do not assume any image is "the intended one"; judge blind.
Return STRICT JSON only:
{"scores": [n1, n2, ...], "winner_index": 0-based, "reason": "<=25 words"}"""


def unwrap(raw: str) -> str:
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
    imgs = [Path(p) for p in sys.argv[1:]]
    if len(imgs) < 2:
        print(__doc__)
        return 2
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "v.json"
        for attempt in range(3):
            r = subprocess.run(
                ["z-ai", "vision", "-p", PROMPT, "-i", str(imgs[0]),
                 "-i", str(imgs[1]), "-o", str(out)],
                capture_output=True, text=True, timeout=240)
            raw = out.read_text() if out.exists() else r.stdout
            try:
                v = json.loads(re.search(r"\{.*\}", unwrap(raw), re.S).group(0))
                break
            except Exception:
                v = None
        if not v:
            print("PROBE FAILED — judge returned no JSON; keep current variant")
            return 0
    scores = v.get("scores", [])
    for i, (p, s) in enumerate(zip(imgs, scores)):
        print(f"  {p.name}: hook_impact {s}")
    w = v.get("winner_index", 0)
    print(f"WINNER: {imgs[w].name} — {v.get('reason', '')}")
    (imgs[0].parent / "hook_probe_verdict.json").write_text(
        json.dumps({"files": [p.name for p in imgs], "scores": scores,
                    "winner": imgs[w].name, "reason": v.get("reason", "")},
                   indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
