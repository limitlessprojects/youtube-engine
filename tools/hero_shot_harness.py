#!/usr/bin/env python3
"""hero_shot_harness.py — acceptance checklist for anonymous-ZeroGPU hero shots (C16).

The one thing you must get right when generating a Wan-Animate/Wan-I2V shot from an approved
keyframe: input/output AR + sane duration + at least one QA artifact. This tool verifiably
checks those mechanically so a bad run fails LOUD before it reaches the render.
It does NOT judge composition — that stays with the VLM gate + boss.

Usage:
  tools/hero_shot_harness.py --input path/to/keyframe.png --output path/to/shot.mp4 [--qa-dir out/]
Exits 0 on PASS, 2 on FAIL (prints explicit failures).
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def probe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration:stream=codec_name,width,height,r_frame_rate,nb_frames",
                          "-of", "json", str(path)], capture_output=True, text=True, check=False)
    if out.returncode != 0:
        return {}
    return json.loads(out.stdout)


def ar(path: Path) -> float:
    p = probe(path)
    s = next((s for s in p.get("streams", []) if s.get("codec_name") not in (None, "png")), None)
    s = s or next((s for s in p.get("streams", []) if s.get("width")), None)
    if not s:
        return 0.0
    return (s.get("width") or 0) / max(1, s.get("height") or 1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--qa-dir", default="")
    a = ap.parse_args()
    inp, outp = Path(a.input), Path(a.output)
    fails = []
    in_ar = 0.0
    if not inp.exists():
        fails.append(f"input missing: {inp}")
    else:
        if inp.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
            fails.append(f"input not a still (got {inp.suffix})")
        in_ar = ar(inp)
        if in_ar == 0.0:
            fails.append("input AR unreadable (corrupt?)")
    if not outp.exists():
        fails.append(f"output missing: {outp}")
    else:
        p = probe(outp)
        fmt = p.get("format", {})
        dur = float(fmt.get("duration", 0) or 0)
        if not (1.0 <= dur <= 15.0):
            fails.append(f"duration {dur:.2f}s outside [1, 15]s (hero shot range)")
        vs = next((s for s in p.get("streams", []) if s.get("codec_name") in ("h264", "hevc", "vp9", "av1")), None)
        in_ar = in_ar if in_ar else 0.0
        if vs:
            if (vs.get("width") or 0) < 320 or (vs.get("height") or 0) < 240:
                fails.append(f"resolution too low: {vs.get('width')}x{vs.get('height')}")
            ar_o = (vs.get("width") or 0) / max(1, vs.get("height") or 1)
            if in_ar and abs(ar_o - in_ar) / in_ar > 0.02:
                fails.append(f"AR drift: input {in_ar:.4f} vs output {ar_o:.4f} (>2%)")
            fps = vs.get("r_frame_rate", "0/1")
            try:
                n, d = (float(x) for x in fps.split("/"))
                fps_v = n / max(d, 1)
                if not (8 <= fps_v <= 60):
                    fails.append(f"fps {fps_v:.2f} outside [8, 60]")
            except Exception:
                pass
        else:
            fails.append("no h264/hevc/vp9/av1 video stream")
    if a.qa_dir:
        qdir = Path(a.qa_dir)
        qa = list(qdir.glob("qa_*.mp4")) if qdir.exists() else []
        if not qa:
            fails.append(f"qa-dir set but no qa_*.mp4 artifacts found in {qdir}")
    if fails:
        for f in fails:
            print(f"FAIL: {f}")
        return 2
    print(f"PASS: {outp} — hero-shot harness QA green (AR={in_ar:.4f}, {dur:.2f}s)")
    print("NOTE: harness QA is mechanical only. VLM gate + boss sign-off still required before ship.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
