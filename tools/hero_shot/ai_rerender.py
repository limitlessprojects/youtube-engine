#!/usr/bin/env python3
"""AI hero-shot re-render client — HF ZeroGPU, Wan2.2-Animate, ANONYMOUS.

The repo lists ONE anonymous GPU route (docs/lessons.md L-093,
research/free-gpu-video.md): the Wan2.2-Animate ZeroGPU space, per-IP quota,
no account required. This tool drives ONE chunk per invocation — on GitHub
Actions each matrix runner gets a fresh IP, hence fresh anonymous quota
(the documented pattern). Local runs use THIS IP's quota only.

This is an ANONYMOUS demo space: do not blast it. --attempts defaults to 2;
on quota exhaustion we exit 4 immediately (a fresh runner/IP has fresh quota).

Input is OUR deterministic render (C6): no external assets, no licensing
problems, and identical motion across judges. wan re-renders the appearance;
it does NOT preserve text stamps (probe: 180 dB -> 190 dB) — overlay text with
the deterministic pipeline and never expect the model to render words.

Usage:
  tools/hero_shot/ai_rerender.py --slug short-0005 --frames 0 60 --out out/
  tools/hero_shot/ai_rerender.py --slug short-0005 --frames 1080 1104 --out out/
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

SPACE = os.environ.get("HERO_SPACE", "alexnasa/Wan2.2-Animate-ZEROGPU")
FPS = 30
W, H = 1080, 1920

NAMES = ["swapped.mp4", "qa_pose.mp4", "qa_bg.mp4", "qa_mask.mp4", "qa_face.mp4"]


def build_chunk(frames: Path, a: int, b: int, dest: Path) -> Path:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS),
                    "-start_number", str(a), "-i", str(frames / "f%04d.png"),
                    "-frames:v", str(b - a),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23",
                    str(dest)], check=True)
    return dest


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--frames", type=int, nargs=2, required=True,
                    metavar=("START", "END"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--space", default=SPACE)
    ap.add_argument("--resolution", default=os.environ.get("RESOLUTION", "Low Res"),
                    choices=["Low Res", "Medium Res"])
    ap.add_argument("--attempts", type=int, default=2)
    a = ap.parse_args()

    repo = Path(__file__).resolve().parent.parent.parent
    frames = repo / "content" / a.slug / "render" / "frames"
    a0, b0 = a.frames
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    tag = f"{a0:04d}"

    chunk_in = out / f"drive_{tag}.mp4"
    build_chunk(frames, a0, b0, chunk_in)
    edited = frames / f"f{a0:04d}.png"
    duration = max(1, round((b0 - a0) / FPS))

    from gradio_client import Client, handle_file
    last = ""
    for attempt in range(1, a.attempts + 1):
        try:
            print(f"[*] {a.space} attempt {attempt}/{a.attempts} "
                  f"(anonymous, frames {a0}-{b0})", flush=True)
            client = Client(a.space, verbose=False)
            result = client.predict(
                input_video=handle_file(str(chunk_in)),
                max_duration_s=duration,
                edited_frame=handle_file(str(edited)),
                rc_str="Character Swap",
                resolution_choice=a.resolution,
                api_name="/animate_scene",
            )
            if isinstance(result, (list, tuple)):
                for r, n in zip(result, NAMES):
                    src = r if isinstance(r, str) else (r.get("video") if isinstance(r, dict) else None)
                    if src and os.path.exists(src):
                        shutil.copy(src, out / f"chunk_{tag}_{n}")
            (out / f"chunk_{tag}_ok.json").write_text(
                json.dumps({"ok": True, "frames": [a0, b0], "space": a.space}) + "\n")
            print(f"[*] saved {out}/chunk_{tag}_swapped.mp4", flush=True)
            return 0
        except Exception as e:  # noqa: BLE001
            last = f"{type(e).__name__}: {e}".lower()
            print(f"[!] attempt {attempt} failed: {last[:400]}", flush=True)
            if "exceeded zerogpu" in last or "quota" in last:
                print(json.dumps({"ok": False, "reason": "quota", "frames": [a0, b0]}))
                return 4
            if attempt < a.attempts:
                wait = 60 * attempt
                print(f"[*] sleeping {wait}s before retry", flush=True)
                time.sleep(wait)
    (out / f"chunk_{tag}_fail.json").write_text(
        json.dumps({"ok": False, "reason": last[:300], "frames": [a0, b0]}) + "\n")
    print(json.dumps({"ok": False, "reason": last[:200], "frames": [a0, b0]}))
    return 3


if __name__ == "__main__":
    sys.exit(main())
