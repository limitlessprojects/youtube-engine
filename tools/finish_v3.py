#!/usr/bin/env python3
"""finish_v3.py — engine v3 finisher: sound design + VO assembly + master + mux.

Usage: python tools/finish_v3.py <slug>

v3 spec #2 (docs/engine-v3-spec.md): music bed + 3 SFX classes per video.
All audio is SYNTHESIZED (numpy) — original, license-free, $0:
  · bed    — warm Aadd9 pad (detuned voices, slow tremolo, air noise),
             faded in/out, ducked -8 dB under VO spans (150 ms ramps)
  · riser  — noise+sine sweep into the insight beat (s3)
  · whoosh — bandpass noise bursts at motion payoffs (ripple, flyby)
  · thump  — soft stamp impacts at word-timed card beats
Then: VO lines adelayed to script.json timestamps -> sum -> two-pass
loudnorm (-14 LUFS / -1.5 dBTP) -> mux render/frames/ -> <slug>.mp4.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
SR = 48000
FPS = 30
I, TP, LRA = -14.0, -1.5, 11

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError(f"cmd failed: {' '.join(cmd[:6])}...\n{r.stderr[-800:]}")
    return r

# ---------- synthesized sound design ----------
def _noise(n, seed):
    rng = np.random.default_rng(seed)
    return rng.standard_normal(n)

def bed(total):
    """warm Aadd9 pad: A2 E3 A3 C#4 B3, detuned pairs, slow tremolo, air."""
    n = int(total * SR)
    t = np.arange(n) / SR
    freqs = [110.0, 164.81, 220.0, 277.18, 246.94, 110.0 * 2]
    out = np.zeros(n)
    for i, f in enumerate(freqs):
        det = 1 + (0.0012 if i % 2 else -0.0012)
        voice = np.sin(2 * np.pi * f * t) + 0.55 * np.sin(2 * np.pi * f * det * t)
        voice *= 0.8 + 0.2 * np.sin(2 * np.pi * (0.05 + 0.013 * i) * t + i)
        out += voice / (2.2 + 0.5 * i)
    # air: gentle lowpassed noise
    air = _noise(n, 7)
    kern = np.ones(480) / 480
    air = np.convolve(air, kern, mode="same")
    out += 0.16 * air / (np.abs(air).max() + 1e-9) * (np.abs(out).max())
    # soft waveshape + normalize to a low bed level
    out = np.tanh(1.6 * out)
    out /= np.abs(out).max() + 1e-9
    # fades: in 0.8s, out last 1.2s, and dip the very end to silence
    fi, fo = int(0.8 * SR), int(1.2 * SR)
    env = np.ones(n)
    env[:fi] = np.linspace(0, 1, fi)
    env[-fo:] = np.linspace(1, 0.0, fo)
    out *= env * 0.062
    return out

def whoosh(dur=0.7, seed=3, f_lo=300, f_hi=1600):
    """bandpass-swept noise burst: airy motion payoff."""
    n = int(dur * SR)
    x = _noise(n, seed)
    # simple one-pole bandpass via FFT filtering with a moving center
    X = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(n, 1 / SR)
    t = np.arange(n) / SR
    # sweep the passband: f_lo -> f_hi -> f_lo over the burst
    center = f_lo + (f_hi - f_lo) * np.sin(np.pi * np.minimum(1, t / dur))
    # approximate with time-varying mask via overlapping windows is heavy;
    # instead: two static bands crossfaded + amplitude envelope
    m1 = np.exp(-((freqs - 500) / 420) ** 2)
    m2 = np.exp(-((freqs - 1200) / 700) ** 2)
    k = np.linspace(0, 1, len(freqs))
    Xf = X * ((1 - k) * m1 + k * m2)
    y = np.fft.irfft(Xf, n)
    env = np.sin(np.pi * np.minimum(1, t / dur)) ** 1.6
    y *= env
    return 0.5 * y / (np.abs(y).max() + 1e-9)

def riser(dur=1.3, seed=11):
    """noise + rising sine sweep into the insight beat."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = _noise(n, seed)
    kern = np.ones(96) / 96
    x = np.convolve(x, kern, mode="same")
    x /= np.abs(x).max() + 1e-9
    f = 300 + 700 * (t / dur) ** 2
    sine = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5
    env = (t / dur) ** 2
    y = (x * 0.7 + sine) * env
    return 0.42 * y / (np.abs(y).max() + 1e-9)

def thump(seed=5):
    """soft stamp impact: 70 Hz body + click transient."""
    n = int(0.28 * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * 68 * t * np.exp(-t * 5)) * np.exp(-t * 16)
    click = _noise(n, seed)[: int(0.012 * SR)] * np.exp(-np.arange(int(0.012 * SR)) / (0.003 * SR))
    y = np.concatenate([click * 0.4, np.zeros(n - len(click))]) + body
    return 0.55 * y / (np.abs(y).max() + 1e-9)

def blip(seed=13):
    """tiny high tick (near-miss spark)."""
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    y = np.sin(2 * np.pi * 2100 * t) * np.exp(-t * 60)
    return 0.22 * y

# ---------- assembly ----------
def load_vo(path):
    """decode any audio to mono float via ffmpeg."""
    r = run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1",
             "-ar", str(SR), "-"], timeout=120)
    return np.frombuffer(r.stdout, dtype=np.float32).astype(np.float64)

def main() -> int:
    slug = sys.argv[1]
    short = REPO / "content" / slug
    script = json.loads((short / "script.json").read_text())
    total = script["timeline"]["total_s"] + 0.45
    N = int(total * SR)

    mix = np.zeros(N)
    vo_spans = []
    lines = [(0.0, script["hook"]["timestamp_start"], script["hook"]["audio_dur_s"],
              short / "vo" / "00.mp3")]
    for i, sc in enumerate(script["scenes"]):
        lines.append((i + 1, sc["timestamp_start"], sc["audio_dur_s"],
                      short / "vo" / f"{i+1:02d}.mp3"))
    for _, start, dur, f in lines:
        y = load_vo(f)
        a = int(start * SR)
        mix[a:a + len(y)] += y[: N - a]
        vo_spans.append((start, start + dur))

    # ---- bed with ducking (-8 dB under VO, 150 ms ramps) ----
    b = bed(total)
    t = np.arange(N) / SR
    gain = np.zeros(N)
    GAP = 0.15
    for s, e in vo_spans:
        gain = np.maximum(gain, np.clip((t - (s - GAP)) / GAP, 0, 1) * np.clip(((e + GAP) - t) / GAP, 0, 1))
    b *= (10 ** (-8 / 20)) + (1 - 10 ** (-8 / 20)) * gain
    mix += b

    # ---- SFX events (word-timed from the script) ----
    sfx = []
    # riser into the s3 insight (ends at s3 start)
    s3 = script["scenes"][3]["timestamp_start"]
    sfx.append((s3 - 1.3, riser(), 0.8))
    # whoosh at the s4 wavefront sweep start ("bends", ~0.9s in)
    s4 = script["scenes"][4]["timestamp_start"]
    sfx.append((s4 + 0.85, whoosh(seed=3), 0.9))
    # whoosh at the s6 flyby ("the birds solved it", ~1.1s in)
    sfx.append((script["scenes"][6]["timestamp_start"] + 1.0, whoosh(seed=4, f_lo=400, f_hi=2000), 0.85))
    # near-miss tick at the s0 spark ("almost never hit" ~2.4s in)
    sfx.append((script["scenes"][0]["timestamp_start"] + 2.35, blip(), 1.0))
    # stamp thumps: s1 cards, s2 beats, s3 seven-pop, s5 beats
    sfx.append((script["scenes"][1]["timestamp_start"] + 2.3, thump(2), 0.8))
    for k in range(1, 4):
        sfx.append((script["scenes"][2]["timestamp_start"] + [0.66, 1.32, 2.31][k - 1] + 0.05, thump(3 + k), 0.6))
    sfx.append((script["scenes"][3]["timestamp_start"] + 3.8, thump(9), 0.9))
    for k in range(2):
        sfx.append((script["scenes"][5]["timestamp_start"] + [0.64, 1.28][k] + 0.05, thump(11 + k), 0.6))
    for at, y, g in sfx:
        a = int(at * SR)
        seg = y[: N - a] * g
        mix[a:a + len(seg)] += seg

    # ---- write mix, master to -14 LUFS (2-pass), mux ----
    audio_dir = short / "audio"
    audio_dir.mkdir(exist_ok=True)
    raw = audio_dir / "_mix.wav"
    import wave
    st = np.clip(mix, -1, 1)
    with wave.open(str(raw), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())

    probe = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(raw), "-af",
                 f"loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json", "-f", "null", "-"]).stderr
    m = json.loads(probe[probe.rfind("{"):probe.rfind("}") + 1])
    filt = (f"loudnorm=I={I}:TP={TP}:measured_I={m['input_i']}"
            f":measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
            f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}"
            f":linear=true")
    master = short / "vo" / "master.m4a"
    run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-af", filt,
         "-ar", str(SR), "-c:a", "aac", "-b:a", "192k", str(master)])

    out = short / f"{slug}.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
         "-i", str(short / "render" / "frames" / "f%04d.png"), "-i", str(master),
         "-c:v", "libx264", "-preset", "medium", "-crf", "18",
         "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
         "-shortest", str(out)])

    dur = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "csv=p=0", str(out)]).stdout.strip()
    lu = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(out), "-map", "0:a",
              "-af", "loudnorm=print_format=json", "-f", "null", "-"]).stderr
    lm = json.loads(lu[lu.rfind("{"):lu.rfind("}") + 1])
    report = {"file": str(out), "duration_s": round(float(dur), 3),
              "lufs": round(float(lm["input_i"]), 2),
              "true_peak_dbtp": round(float(lm["input_tp"]), 2),
              "size_mb": round(out.stat().st_size / 1e6, 2),
              "sound_design": "synth bed (Aadd9 pad) + riser + 2 whoosh + 7 thumps + blip, ducked -8dB"}
    (short / "vo" / "master_report.json").write_text(json.dumps(report, indent=2) + "\n")
    raw.unlink()
    print(json.dumps(report, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
