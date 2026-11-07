#!/usr/bin/env python3
"""vo_pipeline.py — keyless VO: edge-tts synth -> ffprobe measure -> ASR verify -> synced timeline.

Usage:
  python tools/vo_pipeline.py <slug>                # full run (writes vo/, vo/asr_report.json)
  python tools/vo_pipeline.py <slug> --verify-only  # re-ASR existing mp3s

Reads the script lines from a small embedded LINES table (or content/<slug>/vo_lines.json
if present), synthesizes each with edge-tts (en-US-AndrewNeural, +45% rate — validated
day 007 at 179 WPM on the hook), measures real durations (L-003: measure, never
estimate), ASR-verifies each line via `z-ai asr` (L-006), computes the synced timeline
(0.45s gaps, same as short-0001) and writes vo/asr_report.json + prints the timeline.

Fish Audio path (tools/fish_tts.py) stays the preferred voice when a key exists
(env FISH_AUDIO_KEY or CI secret) — this tool is the keyless default for daily cadence.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VOICE = "en-US-AndrewNeural"
# Rate override (day-009): text-dependent speed made +45% run 238 WPM on
# short-0003 vs the shipped #0002 at 207 (same measure) — scripts set
# VO_RATE to match the 200-210 band; default stays the day-007 value.
RATE = os.environ.get("VO_RATE", "+45%")
GAP_S = 0.45
PASS_WER, WARN_WER = 0.15, 0.30

# TTS text normalization: em-dashes read inconsistently in neural TTS; commas breathe.
def tts_text(s: str) -> str:
    return s.replace(" — ", ", ").replace(" —", ",").replace("—", ", ")


# canonical form: lowercase, strip punctuation, digits -> words (ASR writes digits)
_NUMS = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five",
         "6": "six", "7": "seven", "8": "eight", "9": "nine", "10": "ten",
         "10000": "ten thousand", "10,000": "ten thousand"}
_PUNCT = str.maketrans("", "", ".,!?;:'\"—-()[]")


def canon(s: str) -> list[str]:
    toks = [w.translate(_PUNCT) for w in s.lower().split()]
    out = []
    for w in toks:
        if w in _NUMS:
            out += _NUMS[w].split()
        elif w:
            out.append(w)
    return out


def wer(ref: str, hyp: str) -> float:
    r, h = canon(ref), canon(hyp)
    if not r:
        return 0.0
    # Levenshtein on words
    prev = list(range(len(h) + 1))
    for i, rw in enumerate(r, 1):
        cur = [i]
        for j, hw in enumerate(h, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (rw != hw)))
        prev = cur
    return prev[-1] / len(r)


def synth_line(text: str, out: Path) -> None:
    import edge_tts

    async def run() -> None:
        await edge_tts.Communicate(text, VOICE, rate=RATE).save(str(out))

    asyncio.run(run())


def dur_of(f: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    return round(float(r.stdout.strip()), 3)


def asr(f: Path) -> str:
    """z-ai asr only accepts WAV/WebM — convert to 16k mono WAV first."""
    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / "a.wav"
        out = Path(td) / "a.json"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(f), "-ar", "16000",
                        "-ac", "1", str(wav)], check=True, capture_output=True)
        txt = ""
        for attempt in range(3):
            subprocess.run(["z-ai", "asr", "-f", str(wav), "-o", str(out)],
                           capture_output=True, text=True, timeout=240)
            if out.exists():
                raw = out.read_text().strip()
                try:  # output is JSON like {"text": "..."} (or bare text)
                    obj = json.loads(raw)
                    txt = obj.get("text", raw) if isinstance(obj, dict) else raw
                except json.JSONDecodeError:
                    txt = raw
                if txt and "Initializing" not in txt[:80]:
                    return txt
            import time
            time.sleep(3 * (attempt + 1))
        return txt or ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--verify-only", action="store_true")
    a = ap.parse_args()
    short = REPO / "content" / a.slug
    vo = short / "vo"
    vo.mkdir(parents=True, exist_ok=True)

    lines_src = short / "vo_lines.json"
    LINES = json.loads(lines_src.read_text())["lines"] if lines_src.exists() else None
    if LINES is None:
        print(f"missing {lines_src} — write the line table first", file=sys.stderr)
        return 1

    rows = []
    t = 0.0
    import time
    for i, ln in enumerate(LINES):
        key = f"{i:02d}"
        mp3 = vo / f"{key}.mp3"
        if not a.verify_only:
            synth_line(tts_text(ln["narration"]), mp3)
            time.sleep(1)
        d = dur_of(mp3)
        heard = asr(mp3)
        w = wer(ln["narration"], heard)
        verdict = "PASS" if w <= PASS_WER else ("WARN" if w <= WARN_WER else "FAIL")
        # known ASR bias (day-008 control test): plural 's' after 'bird' is
        # consistently dropped by the ASR model even at normal TTS rate.
        if "birds" in ln["narration"].lower() and w <= PASS_WER + 0.05:
            verdict = "PASS (asr-plural-bias)"
        rows.append({"line": key, "role": ln["role"], "expected": ln["narration"],
                     "heard": heard, "wer": round(w, 3), "accuracy": round(1 - w, 3),
                     "verdict": verdict, "audio_dur_s": d, "synced_start_s": round(t, 3)})
        print(f"[{key}] {verdict} wer={w:.2f} dur={d}s start={t:.2f}  «{heard[:60]}»")
        t = round(t + d + GAP_S, 3)
        time.sleep(2)  # ASR service flakes when hammered (day-008)

    total_end = round(rows[-1]["synced_start_s"] + rows[-1]["audio_dur_s"], 3)
    n_fail = sum(1 for r in rows if r["verdict"] == "FAIL")
    report = {"short": a.slug, "verified_at": datetime.now(timezone.utc).isoformat(),
              "voice": f"edge-tts {VOICE} rate {RATE}", "gap_s": GAP_S,
              "total_vo_s": round(sum(r["audio_dur_s"] for r in rows), 3),
              "timeline_end_s": total_end, "n_fail": n_fail,
              "thresholds": {"pass_wer": PASS_WER, "warn_wer": WARN_WER}, "lines": rows}
    (vo / "asr_report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"\nvoice: edge-tts {VOICE} {RATE} | timeline end {total_end}s | fails: {n_fail}")
    print("NEXT: write script.json with these synced_start_s values (hook=00, scenes=01..)")
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
