#!/usr/bin/env python3
"""motion_probe.py — visual motion-energy probe for rendered Shorts.

Usage:
    python tools/motion_probe.py <slug>             # e.g. short-0005
    python tools/motion_probe.py <video.mp4>        # direct video path
    python tools/motion_probe.py <slug> --format json
    python tools/motion_probe.py --self-test [--sample-every N] [--format json|table]

What it does:
    Decodes grayscale frames via an ffmpeg pipe (rawvideo grayf32le (f32le), 15 fps,
    downscaled to 270x480 by default) and computes, per frame, the mean
    absolute pixel delta vs the PREVIOUS frame ("motion energy", 0..1) and
    the fraction of pixels whose abs delta exceeds 8/255 ("changed pct").
    Frames are grouped into BEATS:
      · if content/<slug>/script.json exists, beats = hook + scenes
        (timestamp_start boundaries; the last beat ends at
        timeline.total_s or the video duration), labeled hook, s0, s1, ...
      · otherwise (video path, or no script.json) beats = 1-second bins.
    Per beat it reports: median motion energy, mean changed pct, a
    classification, and it lists the worst 3 and best 3 beats by median
    energy. Classification per beat:
      · dead     — changed pct < 0.02 (visually static)
      · strobing — changed pct > 0.35 AND high-frequency flicker (the
                   per-frame changed-pct series within the beat alternates
                   sign of its frame-to-frame delta on > 50% of transitions,
                   i.e. energy flip-flops instead of holding)
      · ambient  — changed pct < 0.10 (gentle drift/grain/breathing)
      · moving   — everything else

IMPORTANT — what this measures and what it does NOT:
    This tool measures VISUAL motion energy ONLY. A beat can be narratively
    rich while visually dead (a held hero frame under a dense VO line), and
    a beat can be visually loud while narratively empty. Do not use this as
    a story-quality gate; use it to catch renders that forgot to animate.

Self-test mode (--self-test):
    Runs the probe on our #0005 frames only
    (content/short-0005/render/frames) and prints the per-frame energies.
    Default --sample-every 90 ≈ every 90th frame (≈12 frames for the 1104
    frames of #0005, decoded via ffmpeg's select filter, not all frames).
    Override with --sample-every N (1 = every frame; full #0005 decode at
    15 fps is ~550 frames and takes a few seconds). The self-test never
    touches or writes any repo file; it only reads frames.

Output:
    Default is a human-readable table on stdout. --format json emits a
    single JSON object for CI/gate reuse (keys: source, fps, beats,
    worst3, best3, median_beat_motion, verdict).

Exit codes:
    0 — probe ran; median beat motion >= 0.01
    2 — probe ran but median beat motion < 0.01 — possible dead Short;
        the offending beat indices are printed (L-097 language)
    1 — usage error, missing input, or ffmpeg/decode failure
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
FPS = 15
SRC_FPS = 30               # render/frames are rendered at 30 fps
WIDTH, HEIGHT = 270, 480
DELTA_THRESHOLD = 8 / 255  # gray f32le is normalized 0..1; 8/255 keeps the >8 threshold on the 0..255 scale
DEAD_PCT = 0.02
STROBE_PCT = 0.35
AMBIENT_PCT = 0.10
DEAD_SHORT_ENERGY = 0.01   # exit-2 threshold (L-097)
SELF_TEST_SLUG = "short-0005"
SELF_TEST_SAMPLE_EVERY = 90


def fail(msg: str) -> "SystemExit":
    print(f"motion_probe: error: {msg}", file=sys.stderr)
    return SystemExit(1)


def resolve_source(arg: str) -> tuple[str, Path | None, Path | None]:
    """Return (kind, video_path, frames_dir). kind in {'video','frames','slug-video'}."""
    p = Path(arg)
    if p.is_file() and p.suffix.lower() in {".mp4", ".mov", ".mkv", ".webm"}:
        return "video", p, None
    if p.is_dir() and (p / "render" / "frames").is_dir():
        return "frames", None, p / "render" / "frames"
    slug_dir = REPO / "content" / arg
    if slug_dir.is_dir():
        mp4 = slug_dir / f"{arg}.mp4"
        if mp4.is_file():
            return "slug-video", mp4, None
        frames = slug_dir / "render" / "frames"
        if frames.is_dir():
            return "frames", None, frames
        raise fail(f"slug '{arg}' has neither render/frames/ nor {arg}.mp4")
    raise fail(f"'{arg}' is neither an existing video file nor a known slug under content/")


def ffmpeg_cmd(kind: str, video: Path | None, frames: Path | None,
               sample_every: int) -> tuple[list[str], float]:
    """Build the ffmpeg decode command. Returns (cmd, delta_step_seconds).

    delta_step_seconds is the source-time spacing between consecutive decoded
    frames (i.e. energies[i] compares t and t + step).
    """
    tail = f"scale={WIDTH}:{HEIGHT},format=gray"
    if sample_every > 1:
        sel = f"select='not(mod(n\\,{sample_every}))',setpts=N/{FPS}/TB,"
        if kind in {"video", "slug-video"}:
            vf = f"fps={FPS}," + sel + tail
            step = sample_every / FPS
        else:
            vf = sel + tail
            step = sample_every / SRC_FPS
    else:
        if kind in {"video", "slug-video"}:
            vf = f"fps={FPS}," + tail
            step = 1.0 / FPS
        else:
            vf = f"fps={FPS}," + tail
            step = 1.0 / FPS
    if kind in {"video", "slug-video"}:
        assert video is not None
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(video),
               "-vf", vf, "-fps_mode", "passthrough",
               "-f", "rawvideo", "-pix_fmt", "grayf32le", "-"]
    else:
        assert frames is not None
        pattern = str(frames / "f%04d.png")
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error",
               "-framerate", str(SRC_FPS), "-i", pattern,
               "-vf", vf, "-fps_mode", "passthrough",
               "-f", "rawvideo", "-pix_fmt", "grayf32le", "-"]
    return cmd, step


def decode_energies(kind: str, video: Path | None, frames: Path | None,
                    sample_every: int = 1) -> tuple[np.ndarray, np.ndarray, float]:
    """Decode frames, return (energies, changed_pcts, fps_effective).

    energies[i] / changed_pcts[i] describe the delta between frame i and
    frame i+1 (arrays are len(frames)-1).
    """
    frame_bytes = WIDTH * HEIGHT * 4  # f32le
    cmd, step = ffmpeg_cmd(kind, video, frames, sample_every)
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        raise fail("ffmpeg not found on PATH")
    assert proc.stdout is not None
    prev = None
    energies: list[float] = []
    changed: list[float] = []
    n = 0
    while True:
        buf = proc.stdout.read(frame_bytes)
        if len(buf) < frame_bytes:
            break
        frame = np.frombuffer(buf, dtype=np.float32).reshape(HEIGHT, WIDTH)
        if prev is not None:
            d = np.abs(frame - prev)  # normalized 0..1 (gray f32le)
            energies.append(float(d.mean()))
            changed.append(float((d > DELTA_THRESHOLD).mean()))
        prev = frame
        n += 1
    _, err = proc.communicate()
    if proc.returncode != 0:
        raise fail(f"ffmpeg decode failed: {err.decode('utf-8', 'ignore')[-400:]}")
    if n < 2:
        raise fail("decoded fewer than 2 frames — nothing to diff")
    return np.array(energies), np.array(changed), 1.0 / step


def load_beats(slug: str | None, duration_s: float) -> list[dict]:
    """Beat boundaries from script.json (hook + scenes) or 1-second bins."""
    if slug:
        script_path = REPO / "content" / slug / "script.json"
        if script_path.is_file():
            try:
                script = json.loads(script_path.read_text())
            except json.JSONDecodeError:
                script = {}
            starts: list[tuple[str, float]] = []
            hook = script.get("hook") or {}
            if "timestamp_start" in hook:
                starts.append(("hook", float(hook["timestamp_start"])))
            for i, sc in enumerate(script.get("scenes") or []):
                if "timestamp_start" in sc:
                    starts.append((f"s{i}", float(sc["timestamp_start"])))
            if starts:
                starts.sort(key=lambda kv: kv[1])
                total = float((script.get("timeline") or {}).get("total_s") or duration_s)
                beats = []
                for j, (name, start) in enumerate(starts):
                    end = starts[j + 1][1] if j + 1 < len(starts) else total
                    beats.append({"label": name, "start": start, "end": max(end, start + 1e-6)})
                return beats
    n_bins = max(1, int(np.ceil(duration_s)))
    return [{"label": f"bin{i}", "start": float(i), "end": float(i + 1)} for i in range(n_bins)]


def classify(pct: float, pct_series: np.ndarray) -> str:
    if pct < DEAD_PCT:
        return "dead"
    if pct > STROBE_PCT:
        if len(pct_series) >= 3:
            d = np.diff(pct_series)
            flips = float((np.sign(d[:-1]) * np.sign(d[1:]) < 0).mean()) if len(d) > 1 else 0.0
        else:
            flips = 0.0
        if flips > 0.5:
            return "strobing"
        return "moving"
    if pct < AMBIENT_PCT:
        return "ambient"
    return "moving"


def analyze(energies: np.ndarray, changed: np.ndarray, beats: list[dict],
            fps_eff: float) -> dict:
    # energies[i] is the delta between frame i and frame i+1; frame i is at t=i/fps_eff
    frame_t = np.arange(len(energies)) / fps_eff
    beat_rows = []
    for b in beats:
        mask = (frame_t >= b["start"]) & (frame_t < b["end"])
        e = energies[mask]
        c = changed[mask]
        if len(e) == 0:
            beat_rows.append({**b, "frames": 0, "median_energy": None,
                              "mean_changed_pct": None, "classification": "n/a"})
            continue
        pct = float(c.mean())
        beat_rows.append({
            **b,
            "frames": int(len(e)),
            "median_energy": float(np.median(e)),
            "mean_changed_pct": pct,
            "classification": classify(pct, c),
        })
    scored = [r for r in beat_rows if r["median_energy"] is not None]
    ranked = sorted(scored, key=lambda r: r["median_energy"])
    worst = ranked[:3]
    best = ranked[-3:][::-1]
    med = float(np.median([r["median_energy"] for r in scored])) if scored else 0.0
    return {"beats": beat_rows, "worst3": worst, "best3": best, "median_beat_motion": med}


def print_table(source: str, fps_eff: float, result: dict) -> None:
    print(f"motion_probe — source: {source}  (decode @ {fps_eff:g} fps, {WIDTH}x{HEIGHT} gray)")
    print(f"{'beat':<6}{'start':>7}{'end':>7}{'frames':>7}{'medE':>9}{'chg%':>8}  class")
    print("-" * 58)
    for r in result["beats"]:
        if r["median_energy"] is None:
            print(f"{r['label']:<6}{r['start']:>7.2f}{r['end']:>7.2f}{r['frames']:>7}{'n/a':>9}{'n/a':>8}  n/a (no sampled frames)")
            continue
        print(f"{r['label']:<6}{r['start']:>7.2f}{r['end']:>7.2f}{r['frames']:>7}"
              f"{r['median_energy']:>9.4f}{r['mean_changed_pct'] * 100:>7.1f}%  {r['classification']}")
    print("-" * 58)
    print("worst 3 beats (lowest median energy):")
    for r in result["worst3"]:
        print(f"  {r['label']}: medE={r['median_energy']:.4f} chg={r['mean_changed_pct'] * 100:.1f}% {r['classification']}")
    print("best 3 beats (highest median energy):")
    for r in result["best3"]:
        print(f"  {r['label']}: medE={r['median_energy']:.4f} chg={r['mean_changed_pct'] * 100:.1f}% {r['classification']}")
    print(f"median beat motion: {result['median_beat_motion']:.4f}")
    if result["median_beat_motion"] < DEAD_SHORT_ENERGY:
        dead_idx = [r["label"] for r in result["beats"]
                    if r["median_energy"] is not None and r["median_energy"] < DEAD_SHORT_ENERGY]
        print(f"WARNING (L-097): median beat motion < {DEAD_SHORT_ENERGY} — possible dead Short.")
        print(f"  dead beat indices: {', '.join(dead_idx)}")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Visual motion-energy probe for rendered Shorts.")
    ap.add_argument("target", nargs="?", help="<slug> (content/<slug>) or path to a video file")
    ap.add_argument("--format", choices=["table", "json"], default="table")
    ap.add_argument("--self-test", action="store_true",
                    help=f"probe ONLY #0005 frames ({SELF_TEST_SLUG}); prints per-frame energies")
    ap.add_argument("--sample-every", type=int, default=None,
                    help="decode every Nth frame (default 1; self-test default "
                         f"{SELF_TEST_SAMPLE_EVERY} ≈ 12 frames for #0005)")
    args = ap.parse_args(argv)

    if args.sample_every is not None and args.sample_every < 1:
        return fail("--sample-every must be >= 1")

    if args.self_test:
        sample = args.sample_every if args.sample_every is not None else SELF_TEST_SAMPLE_EVERY
        frames = REPO / "content" / SELF_TEST_SLUG / "render" / "frames"
        if not frames.is_dir():
            return fail(f"self-test frames not found: {frames}")
        energies, changed, fps_eff = decode_energies("frames", None, frames, sample)
        duration_s = len(energies) / fps_eff
        beats = load_beats(SELF_TEST_SLUG, duration_s)
        result = analyze(energies, changed, beats, fps_eff)
        result.update({"source": str(frames), "fps": fps_eff, "sample_every": sample,
                       "per_frame_energies": [round(float(e), 6) for e in energies]})
        if args.format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"self-test — #0005 frames, every {sample}th frame ({len(energies) + 1} frames decoded)")
            for i, e in enumerate(energies):
                print(f"  frame[{i * sample:>4}] -> frame[{(i + 1) * sample:>4}]  energy={e:.4f}  changed={changed[i] * 100:.1f}%")
            print()
            print_table(str(frames), fps_eff, result)
        return 2 if result["median_beat_motion"] < DEAD_SHORT_ENERGY else 0

    if not args.target:
        ap.print_help()
        return 1
    sample = args.sample_every or 1
    kind, video, frames = resolve_source(args.target)
    source = str(video or frames)
    slug = args.target if kind == "frames" and not Path(args.target).is_dir() else (
        args.target if (REPO / "content" / args.target).is_dir() else None)
    energies, changed, fps_eff = decode_energies(kind, video, frames, sample)
    duration_s = len(energies) / fps_eff
    beats = load_beats(slug, duration_s)
    result = analyze(energies, changed, beats, fps_eff)
    result.update({"source": source, "fps": fps_eff, "sample_every": sample,
                   "verdict": "dead-short" if result["median_beat_motion"] < DEAD_SHORT_ENERGY else "ok"})
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print_table(source, fps_eff, result)
    return 2 if result["median_beat_motion"] < DEAD_SHORT_ENERGY else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
