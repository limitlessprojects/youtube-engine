#!/usr/bin/env python3
"""script_linter.py — mechanical anti-boilerplate gate (runs before critic, render, upload).

Checks: banned vocabulary, greeting/intro patterns, hook length, WPM band,
rhetorical-closing question, disclaimer phrases.

Input: plain text, or a script JSON with {"scenes":[{"narration": "..."}]} (also
accepts the scriptwriter output contract; `loop_line` included).
Exit: 0 pass, 1 fail. --json for machine-readable report.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

BANNED = [
    "delve", "delving", "tapestry", "testament", "beacon", "unravel", "unravelling",
    "realm", "in summary", "in conclusion", "have you ever wondered",
    "imagine a world where", "welcome back", "welcome to the channel", "game-changer",
    "game changer", "supercharge", "unlock the", "elevate your", "embark on a journey",
    "it's important to remember", "it is important to note", "this is purely theoretical",
    "in today's video", "smash that like", "hit that subscribe", "without further ado",
]
GREETING = re.compile(r"^(hi|hey|hello|yo|welcome|what's up|ladies and gentlemen)\b", re.I)
DISCLAIMER = re.compile(r"(theoretical|hypothetical) (scenario|exercise|thought experiment)", re.I)
WPM_BAND = {"short": (185, 215), "long": (155, 175)}  # day-010: shorts class = edge-tts +25% (L-075)
FISH_WPS = 2.6  # measured: Fish Audio s2.1-pro-free "Energetic Male" (needs rate knob)


def narration_from(payload: str) -> tuple[str, list[str]]:
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return payload, []
    lines: list[str] = []
    if isinstance(data, dict):
        if data.get("hook", {}).get("narration"):
            lines.append(data["hook"]["narration"])
        for sc in data.get("scenes", []):
            if isinstance(sc, dict) and sc.get("narration"):
                lines.append(sc["narration"])
        if data.get("loop_line"):
            lines.append(data["loop_line"])
    return " ".join(lines), [ln for ln in lines]


def lint(text: str, fmt: str, duration_s: float | None) -> dict:
    fails: list[str] = []
    warns: list[str] = []
    low = text.lower()
    words = len(re.findall(r"[A-Za-z']+", text))
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

    for b in BANNED:
        if re.search(rf"\b{re.escape(b)}\b", low):
            fails.append(f"banned word/phrase: '{b}'")
    if sents and GREETING.search(sents[0]):
        fails.append(f"greeting opener: '{sents[0][:60]}…'")
    if DISCLAIMER.search(low):
        fails.append("disclaimer phrase present (meta-commentary)")
    if sents and sents[-1].rstrip().endswith("?"):
        warns.append("script closes on a rhetorical question (banned closer pattern)")

    opener_words = len(sents[0].split()) if sents else 0
    if opener_words > 14:
        fails.append(f"hook too long: opener is {opener_words} words (target ≤ 12, hard cap 14)")

    if duration_s and duration_s > 0:
        wpm = words / (duration_s / 60)
    else:
        implied_s = words / FISH_WPS
        wpm = 156.0  # == words/(implied/60) when duration derived from same rate; informational
        warns.append(f"no duration given; implied VO length {implied_s:.1f}s at {FISH_WPS} w/s")
    lo, hi = WPM_BAND.get(fmt, (150, 180))
    if not (lo - 15 <= wpm <= hi + 15):
        fails.append(f"WPM out of band: {wpm:.0f} (target {lo}–{hi})")
    elif not (lo <= wpm <= hi):
        warns.append(f"WPM slightly out of band: {wpm:.0f} (target {lo}–{hi})")

    short_ratio = (sum(1 for s in sents if len(s.split()) <= 6) / len(sents)) if sents else 0
    if sents and short_ratio < 0.15:
        warns.append(f"rhythm flat: only {short_ratio:.0%} short sentences (mix 3-word punches in)")

    # ---- boss-directive structure rules (2026-11-08, enforced at script time) ----
    try:
        data = json.loads(text) if text.strip().startswith("{") else None
    except json.JSONDecodeError:
        data = None
    if isinstance(data, dict) and data.get("scenes") and data.get("hook", {}).get("narration"):
        hook = data["hook"]["narration"]
        scenes = data["scenes"]
        # L-073: orient — topic noun from the title must appear in the hook
        title = data.get("title", "")
        title_nouns = [w for w in re.findall(r"[A-Za-z]{4,}", title)
                       if w.lower() not in {"what", "when", "where", "which", "your", "never"}]
        if title_nouns and not any(n.lower() in hook.lower() for n in title_nouns):
            fails.append(f"L-073 orientation: hook never names the topic {title_nouns[:4]}")
        # L-075: pacing — scene durations from timestamps if present
        starts = [data["hook"].get("timestamp_start", 0.0)] + [s.get("timestamp_start") for s in scenes]
        if all(isinstance(x, (int, float)) for x in starts) and len(starts) > 2:
            total = data.get("timeline", {}).get("total_s") or (starts[-1] + 3)
            ends = starts[1:] + [total]
            durs = [e - s for s, e in zip(starts, ends) if e > s]
            if durs:
                if sum(durs) / len(durs) > 3.2:
                    fails.append(f"L-075 pacing: mean scene {sum(durs)/len(durs):.2f}s > 3.2s")
                if max(durs) > 4.2:
                    fails.append(f"L-075 pacing: max scene {max(durs):.2f}s > 4.2s")
                if len(durs) < 10:
                    warns.append(f"L-075 cut density: {len(durs)} scenes — target ≥ 12 visual events/35s")
        # L-077: spine — no new capitalized entity only in the last 2 scenes
        early = " ".join([hook] + [s.get("narration", "") for s in scenes[:-2]])
        early_caps = set(re.findall(r"\b[A-Z][a-z]{2,}\b", early))
        for s in scenes[-2:]:
            new = [c for c in re.findall(r"\b[A-Z][a-z]{2,}\b", s.get("narration", ""))
                   if c not in early_caps and c not in {"The", "And", "But", "Same", "Only", "Your"}]
            if new:
                warns.append(f"L-077 spine: new entity {new} only in the closer — tangent?")

    return {
        "verdict": "FAIL" if fails else "PASS",
        "words": words,
        "sentences": len(sents),
        "opener_words": opener_words,
        "wpm": round(wpm, 1),
        "short_sentence_ratio": round(short_ratio, 2),
        "fails": fails,
        "warns": warns,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("script", nargs="?", help="path to .txt/.md/.json script (or '-' for stdin)")
    ap.add_argument("--format", choices=["short", "long"], default="short")
    ap.add_argument("--duration-s", type=float, default=None)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.script == "-":
        text = sys.stdin.read()
    elif a.script:
        text = open(a.script, encoding="utf-8").read()
    else:
        text = sys.stdin.read()
    flat, _lines = narration_from(text)
    report = lint(flat or text, a.format, a.duration_s)
    if a.json:
        print(json.dumps(report, indent=1))
    else:
        icon = "✅" if report["verdict"] == "PASS" else "❌"
        print(f"{icon} {report['verdict']} — {report['words']}w, {report['sentences']} sents, "
              f"WPM {report['wpm']}, opener {report['opener_words']}w")
        for f in report["fails"]:
            print(f"  FAIL: {f}")
        for w in report["warns"]:
            print(f"  warn: {w}")
    return 1 if report["verdict"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
