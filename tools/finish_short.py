#!/usr/bin/env python3
"""Finish a short: VO assembly at synced timestamps -> -14 LUFS master -> mux.

Usage: tools/finish_short.py <slug>

Reads script.json (synced timeline + vo files in vo/), builds the full audio
track (each line adelayed to its timestamp_start), masters it to -14 LUFS /
-1.5 dBTP (two-pass loudnorm, what-if-animation master.py recipe), then muxes
with render/frames/ into <slug>.mp4 (h264 crf18, faststart).
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FPS = 30
I, TP, LRA = -14.0, -1.5, 11


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError(f"cmd failed: {' '.join(cmd[:6])}...\n{r.stderr[-800:]}")
    return r


def main() -> int:
    slug = sys.argv[1]
    short = REPO / "content" / slug
    script = json.loads((short / "script.json").read_text())
    lines = [("00", script["hook"]["timestamp_start"])] + [
        (f"{i+1:02d}", sc["timestamp_start"])
        for i, sc in enumerate(script["scenes"])
    ]
    t_end = script["timeline"]["total_s"]
    total_dur = t_end + 0.45

    # ---- audio assembly: adelay each VO line to its synced start ----
    vo_files = [short / "vo" / f"{k}.mp3" for k, _ in lines]
    inputs = []
    for f in vo_files:
        inputs += ["-i", str(f)]
    fc, mix = [], ""
    for i, (k, start) in enumerate(lines):
        ms = int(round(start * 1000))
        fc.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
                  f"adelay={ms}|{ms}[a{i}]")
        mix += f"[a{i}]"
    fc.append(f"{mix}amix=inputs={len(lines)}:normalize=0,"
              f"apad=whole_dur={total_dur}[mixout]")
    raw = short / "vo" / "_assembled.wav"
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex",
         ";".join(fc), "-map", "[mixout]", str(raw)])

    # ---- two-pass loudnorm to -14 LUFS ----
    probe = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(raw), "-af",
                 f"loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json", "-f",
                 "null", "-"]).stderr
    m = json.loads(probe[probe.rfind("{"):probe.rfind("}") + 1])
    filt = (f"loudnorm=I={I}:TP={TP}:LRA={LRA}:measured_I={m['input_i']}"
            f":measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
            f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}"
            f":linear=true")
    master = short / "vo" / "master.m4a"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-af", filt,
         "-ar", "48000", "-c:a", "aac", "-b:a", "192k", str(master)])

    # ---- mux with rendered frames ----
    out = short / f"{slug}.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
         "-i", str(short / "render" / "frames" / "f%04d.png"), "-i", str(master),
         "-c:v", "libx264", "-preset", "medium", "-crf", "18",
         "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
         "-shortest", str(out)])

    # ---- report ----
    dur = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "csv=p=0", str(out)]).stdout.strip()
    lu = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(out), "-map", "0:a",
              "-af", "loudnorm=print_format=json", "-f", "null", "-"]).stderr
    lm = json.loads(lu[lu.rfind("{"):lu.rfind("}") + 1])
    size = out.stat().st_size / 1e6
    report = {"file": str(out), "duration_s": round(float(dur), 3),
              "lufs": round(float(lm["input_i"]), 2),
              "true_peak_dbtp": round(float(lm["input_tp"]), 2),
              "size_mb": round(size, 2)}
    (short / "vo" / "master_report.json").write_text(json.dumps(report, indent=2) + "\n")
    raw.unlink()
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
