#!/usr/bin/env python3
"""fish_tts.py — Fish Audio narration client (s2.1-pro-free, daily free quota).

Usage:
  python tools/fish_tts.py --text "Hello!" --out out.mp3
  python tools/fish_tts.py --text-file script.txt --out vo.mp3 --ref-id 802e3bc2b27e49c2995d23ef70e6ac89

Env: FISH_AUDIO_KEY (required). Never pass the key on the CLI.
Notes (ledger L-005/L-006): measured ~2.6 words/sec on "Energetic Male";
always ASR-verify the render before editing it into a timeline.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

API = "https://api.fish.audio/v1/tts"
DEFAULT_MODEL = "s2.1-pro-free"
DEFAULT_REF = "802e3bc2b27e49c2995d23ef70e6ac89"  # "Energetic Male" — verified in Day 000


def synth(text: str, out: Path, ref_id: str | None, model: str, fmt: str) -> int:
    import requests

    key = os.environ.get("FISH_AUDIO_KEY", "").strip()
    if not key:
        print("env FISH_AUDIO_KEY missing (set it from your secrets store)", file=sys.stderr)
        return 1
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json", "model": model}
    body: dict = {"text": text, "format": fmt}
    if ref_id:
        body["reference_id"] = ref_id

    last = None
    for attempt in range(1, 4):
        try:
            r = requests.post(API, headers=headers, json=body, timeout=120)
            if r.status_code in (401, 403):
                print(f"auth failed ({r.status_code}) — check FISH_AUDIO_KEY", file=sys.stderr)
                return 1
            if r.status_code in (402, 429):
                print(f"quota/limit ({r.status_code}) — daily free quota spent; retry later "
                      f"or fall back to local TTS (kokoro/piper, ledger L-023)", file=sys.stderr)
                return 2
            if r.status_code >= 500:
                last = f"server {r.status_code}"
                time.sleep(3 * attempt)
                continue
            r.raise_for_status()
            data = r.content
            if len(data) < 512:
                last = f"suspiciously small payload ({len(data)}B)"
                time.sleep(2 * attempt)
                continue
            ok_magic = data[:3] == b"ID3" or (len(data) > 2 and data[0] == 0xFF and (data[1] & 0xE0) == 0xE0)
            if fmt == "mp3" and not ok_magic:
                last = "payload is not MP3 (wrong content?)"
                time.sleep(2 * attempt)
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
            words = len(text.split())
            print(f"[tts] wrote {out} ({len(data)} bytes, ~{len(data)/1024:.0f} KiB, "
                  f"{words} words ≈ {words/2.6:.1f}s at 2.6 w/s)")
            print(f"[tts] NEXT (L-006): ASR-verify the render before cutting it into the timeline")
            return 0
        except requests.RequestException as e:
            last = f"{type(e).__name__}: {e}"
            time.sleep(3 * attempt)
    print(f"[tts] failed after 3 attempts: {last}", file=sys.stderr)
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--text")
    ap.add_argument("--text-file")
    ap.add_argument("--out", required=True)
    ap.add_argument("--ref-id", default=DEFAULT_REF)
    ap.add_argument("--no-ref", action="store_true", help="use default free voice, no reference")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--format", default="mp3", choices=["mp3", "wav", "opus"])
    a = ap.parse_args()
    if a.text_file:
        text = Path(a.text_file).read_text(encoding="utf-8").strip()
    elif a.text:
        text = a.text.strip()
    else:
        text = sys.stdin.read().strip()
    if not text:
        print("no text given", file=sys.stderr)
        return 1
    return synth(text, Path(a.out), None if a.no_ref else a.ref_id, a.model, a.format)


if __name__ == "__main__":
    sys.exit(main())
