#!/usr/bin/env python3
"""blueprint_extractor.py — transcript -> structural blueprint (no LLM, deterministic).

Input : research/transcripts/<id>.json (from tools/transcribe.py)
Output: research/blueprints/<id>.json + <id>.md

Metrics: duration, words, WPM, hook length, sentence rhythm (short/long mix),
cue density, open-loop markers, estimated cut density. The LLM blueprint analyst
(prompts/blueprint_analyst.md) extends these numbers qualitatively — it never
contradicts them.
"""
from __future__ import annotations

import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TR = REPO / "research" / "transcripts"
BP = REPO / "research" / "blueprints"

STOP = set("""a an and are as at be but by for from has have he her his i if in into is it its
of on or our she that the their them then there these they this to was we were what when where
which who will with would you your do does did not no so about just like can could should""".split())

CUE_WORDS = ["but", "so", "then", "now", "which means", "here's", "and that", "until", "suddenly"]
LOOP_MARKERS = [r"what if", r"but here's", r"the problem", r"turns out", r"until", r"nobody",
                r"no one", r"the answer", r"here's the thing", r"which means"]


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def extract(vid: str) -> dict:
    data = json.loads((TR / f"{vid}.json").read_text(encoding="utf-8"))
    segs = data["segments"]
    text = " ".join(s["text"] for s in segs)
    sents = sentences(text)
    words = [w for w in re.findall(r"[a-zA-Z']+", text.lower()) if w]

    duration = (segs[-1]["start"] + segs[-1]["duration"]) if segs else 0.0
    wpm = round(len(words) / (duration / 60), 1) if duration > 0 else 0.0

    # hook = everything in the first 15 seconds
    hook_text = " ".join(s["text"] for s in segs if s["start"] < 15)
    hook_words = len(hook_text.split())

    sent_lens = [len(s.split()) for s in sents]
    short_ratio = round(sum(1 for n in sent_lens if n <= 6) / len(sent_lens), 2) if sent_lens else 0.0

    # first sentence = the actual opening line
    opener_words = sent_lens[0] if sent_lens else 0

    bigrams = Counter(zip(words, words[1:]))
    top_bigrams = [
        {"pair": f"{a} {b}", "n": n}
        for (a, b), n in bigrams.most_common(8)
        if a not in STOP and b not in STOP and n > 1
    ][:5]

    cue_n = sum(len(re.findall(re.escape(c), text, re.I)) for c in CUE_WORDS)
    loops = [{"t": round(segs[i]["start"], 1), "marker": m}
             for i, s in enumerate(segs) for m in LOOP_MARKERS
             if re.search(m, s["text"], re.I)][:12]

    # estimated cuts: sentence-start connectors ("And/But/So/Now") as proxy + sentence rate
    connector_starts = sum(1 for s in sents if re.match(r"^(and|but|so|now|which|then)\b", s, re.I))
    est_cpm = round(len(sents) / (duration / 60), 1) if duration > 0 else 0.0

    return {
        "id": vid,
        "duration_s": round(duration, 1),
        "words": len(words),
        "wpm": wpm,
        "hook_15s_words": hook_words,
        "opener_sentence_words": opener_words,
        "sentences": len(sents),
        "avg_sentence_words": round(statistics.mean(sent_lens), 1) if sent_lens else 0,
        "short_sentence_ratio": short_ratio,
        "cue_word_density_per_min": round(cue_n / (duration / 60), 1) if duration > 0 else 0.0,
        "connector_starts": connector_starts,
        "estimated_cuts_per_min_proxy": est_cpm,
        "open_loop_markers": loops,
        "top_bigrams": top_bigrams,
        "language_note": data.get("path", "unknown-path"),
    }


def to_md(b: dict) -> str:
    loops = ", ".join(f"{l['marker']}@{l['t']}s" for l in b["open_loop_markers"][:8]) or "none detected"
    bi = ", ".join(f"`{x['pair']}`×{x['n']}" for x in b["top_bigrams"]) or "—"
    return f"""# Blueprint — {b['id']}

| Metric | Value |
|---|---|
| Duration | {b['duration_s']}s |
| Words | {b['words']} |
| WPM | {b['wpm']} (our band: 155–175) |
| Hook (first 15s) | {b['hook_15s_words']} words |
| Opener sentence | {b['opener_sentence_words']} words (our rule: ≤ 12) |
| Sentences | {b['sentences']} (avg {b['avg_sentence_words']} words) |
| Short-sentence ratio | {b['short_sentence_ratio']} |
| Cue-word density | {b['cue_word_density_per_min']}/min |
| Est. cut density (proxy) | {b['estimated_cuts_per_min_proxy']}/min |
| Open-loop markers | {loops} |
| Top bigrams | {bi} |

Source path: `{b['language_note']}` — numbers from tools/blueprint_extractor.py (deterministic).
Next: run the LLM analyst (prompts/blueprint_analyst.md) to add beats + takeaways.
"""


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: blueprint_extractor.py <video-id> (transcript must exist)", file=sys.stderr)
        return 1
    vid = sys.argv[1]
    if not (TR / f"{vid}.json").exists():
        print(f"transcript missing: {TR / (vid + '.json')} — run tools/transcribe.py first", file=sys.stderr)
        return 1
    BP.mkdir(parents=True, exist_ok=True)
    b = extract(vid)
    (BP / f"{vid}.json").write_text(json.dumps(b, indent=1), encoding="utf-8")
    (BP / f"{vid}.md").write_text(to_md(b), encoding="utf-8")
    print(f"[bp] {vid}: {b['wpm']} WPM, hook {b['hook_15s_words']}w/15s, "
          f"{len(b['open_loop_markers'])} loop markers -> {BP / (vid + '.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
