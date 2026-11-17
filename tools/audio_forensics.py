#!/usr/bin/env python3
"""audio_forensics.py — find the 'loud buzzing like static' the boss reported.

For each input audio file:
  - decode to mono 48k float
  - window the file in 100 ms hops / 200 ms windows
  - per band (sub-100 rumble, 100-300 pad zone, 300-1k, 1-4k speech, 4-8k hiss,
    8-16k, 16k+) report: median level (dBFS) and 10th-percentile floor
  - flag VO gaps (speech-band energy low) and report what is audible in them
  - FFT the whole file: exact narrowband peaks (hum / pad tones) with levels
Usage: python3 audio_forensics.py file1 [file2 ...]
"""
import subprocess, sys, json
import numpy as np

SR = 48000

def decode(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le",
                        "-ac", "1", "-ar", str(SR), "-"], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode()[:400])
    return np.frombuffer(r.stdout, dtype=np.float32).astype(np.float64)

BANDS = [(20, 100, "rumble"), (100, 300, "pad-zone"), (300, 1000, "low-mid"),
         (1000, 4000, "speech"), (4000, 8000, "hiss"), (8000, 16000, "air8-16k"),
         (16000, 20000, "top16k+")]

def band_fft(x):
    n = len(x)
    X = np.fft.rfft(x * np.hanning(n))
    p = 20 * np.log10(np.abs(X) / n + 1e-12)
    f = np.fft.rfftfreq(n, 1 / SR)
    return f, p

def analyze(path):
    x = decode(path)
    dur = len(x) / SR
    print(f"\n===== {path}  ({dur:.1f}s, peak {20*np.log10(np.abs(x).max()+1e-12):+.1f} dBFS)")
    # windowed analysis: 200 ms window, 100 ms hop
    W, H = int(0.2 * SR), int(0.1 * SR)
    nw = (len(x) - W) // H
    freqs = np.fft.rfftfreq(W, 1 / SR)
    win = np.hanning(W)
    # per-window per-band RMS dB
    band_rms = {name: np.full(nw, np.nan) for _, _, name in BANDS}
    speech = np.full(nw, np.nan)
    for i in range(nw):
        seg = x[i*H:i*H+W] * win
        X = np.abs(np.fft.rfft(seg))
        # power spectral density -> band RMS (approx: sum of |X|^2 / n^2 * 2)
        P = (X**2) / (W**2) / (np.sum(win)**2 / W**2) * 2
        for lo, hi, name in BANDS:
            m = (freqs >= lo) & (freqs < hi)
            band_rms[name][i] = 10*np.log10(P[m].sum() + 1e-15)
        m = (freqs >= 300) & (freqs < 4000)
        speech[i] = 10*np.log10(P[m].sum() + 1e-15)
    # VO gaps: speech-band in the bottom quartile of its own range
    thr = np.nanpercentile(speech, 25)
    gaps = speech <= thr
    print(f"  windows: {nw} | gap windows (speech paused): {gaps.sum()} ({100*gaps.mean():.0f}%)")
    hdr = f"  {'band':>10} | {'all-median dB':>13} | {'all-floor p10':>13} | {'GAP-median':>10} | {'VO-median':>9}"
    print(hdr)
    for _, _, name in BANDS:
        v = band_rms[name]
        gm = np.nanmedian(v[gaps]) if gaps.any() else float("nan")
        vm = np.nanmedian(v[~gaps]) if (~gaps).any() else float("nan")
        print(f"  {name:>10} | {np.nanmedian(v):>13.1f} | {np.nanpercentile(v,10):>13.1f} | {gm:>10.1f} | {vm:>9.1f}")
    # narrowband peaks over the whole file
    f, p = band_fft(x)
    # smooth-ish peak pick: local maxima above band median + 12 dB
    peaks = []
    for lo, hi in [(40, 70), (90, 130), (150, 200), (210, 240), (250, 300),
                   (300, 500), (500, 900), (900, 4000), (4000, 8000)]:
        m = (f >= lo) & (f < hi)
        if not m.any():
            continue
        i = np.argmax(p[m]) + np.argmax(m)
        # per-bin level -> total power in a 5-Hz neighborhood around the peak
        peaks.append((f[i], p[i]))
    print("  narrowband peaks (bin level dB, whole-file FFT):")
    for fr, lv in peaks:
        print(f"    {fr:8.1f} Hz : {lv:+7.1f} dB")
    # top 5 absolute FFT peaks
    mask = (f > 30) & (f < 16000)
    idx = np.argsort(p[mask])[-5:]
    fs, ls = f[mask][idx], p[mask][idx]
    print("  top-5 FFT bins overall:")
    for fr, lv in sorted(zip(fs, ls), key=lambda t: -t[1]):
        print(f"    {fr:8.1f} Hz : {lv:+7.1f} dB")

for p in sys.argv[1:]:
    analyze(p)
