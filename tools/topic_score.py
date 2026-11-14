#!/usr/bin/env python3
"""topic_score.py — rank topic candidates by a transparent, corpus-grounded rubric.

NOT a prediction of views. A triage list so the daily loop never spends render time
on a weak topic before it spends render time on a strong one. Scoring = additive keyword
points cross-checked against our own view log (docs/views.csv) + corpus notes.

Usage: tools/topic_score.py [topics.txt] [--weights weights.json]
Input: one topic per line. Output: ranked table + writes research/topic-backlog.md
"""
import json
import re
import sys
from pathlib import Path

W = {
    "visceral_or_catastrophe": 20,     # Zack anatomy lane (255M/216M)
    "superlative_number": 12,         # "largest/loudest/fastest + number" (177M Lum Stubb, NASA)
    "belief_correction": 15,          # Miles "3.7x" formula + MinutePhysics 236wpm
    "everyday_curiosity": 14,         # "Why don't birds…?" 8.7x, our #0002 1142
    "single_number_in_title": 10,      # one concrete figure anchors the promise
    "child_safe_age": 8,              # corpus skew: huge reach, high all-ages
    "short_audio_run": 10,            # topic explainable in <= 40 words VO
    "production_feasibility": 14,     # one hero + stickman + stamp (our format wins)
    "noun_in_first_line": 8,          # L-073 orientation — noun must survive beat 1
    "sunset_track_record": 4,         # our own organic outliers cluster here
}
VIS = re.compile(r"anatomy|wound|blood|explo|erupt|volcan|spike|fracture|poison|bite|predat|fatal|shock|pressure|injure|splinter|stitch|bleed|scream", re.I)
SUP = re.compile(r"largest|loudest|fastest|first|biggest|smallest|deepest|highest|most|least|greatest|record|never|only", re.I)
BEL = re.compile(r"actually|really|think|believe|myth|not what|misunderstood|surprise|wrong|reason why", re.I)
EVC = re.compile(r"why (don|doesn|won|can)|what if|how (do|does|did|come)|never|always", re.I)
NUM = re.compile(r"\d[\d,]*\s*(miles|mph|fps|db|hz|firearms|kg|km|minutes|hours|years|percent|%|times)", re.I)

def score(topic: str):
    t = topic.lower()
    pts, hits = 0, []
    def add(cond, key, name):
        nonlocal pts
        if cond:
            pts += W[key]; hits.append(name)
    add(bool(VIS.search(t)), "visceral_or_catastrophe", "visceral lane")
    add(bool(SUP.search(t)), "superlative_number", "superlative")
    add(bool(BEL.search(t)), "belief_correction", "belief-correction")
    add(bool(EVC.search(t)), "everyday_curiosity", "everyday curiosity")
    add(bool(NUM.search(t)), "single_number_in_title", "single number")
    words = len(topic.split())
    if words <= 10: hits.append("fits-title")
    if words <= 10: pts += 6
    add("kid|kids|child|tiger|jellyfish|pigeon|hamst|bunny".lower() and bool(re.search(r"kid|child|tiger|jellyfish|pigeon|hamster|bunny|puppy|penguin", t)), "child_safe_age", "kid-skewing")
    if words <= 28: hits.append("audio-compatible (VO<=28 words skeleton)")
    if words <= 28: pts += W["short_audio_run"]
    if "!" not in topic: pts += 2
    hits.append("feasible-format")
    pts += W["production_feasibility"] if re.search(r"why|what if|how", t) else 6
    pts += W["noun_in_first_line"] if len(topic.split()) <= 9 else 0
    if re.search(r"sunset|orange|red sky|evening|dusk", t):
        pts += W["sunset_track_record"]; hits.append("sunset-lane")
    return pts, hits

def main() -> int:
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "topics.txt")
    rows = []
    for line in src.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        pts, hits = score(line)
        rows.append((pts, line, hits))
    rows.sort(key=lambda r: -r[0])
    out = ["| Rank | Score | Candidate | Corpus hits |", "|---|---|---|---|"]
    for i, (pts, line, hits) in enumerate(rows, 1):
        out.append(f"| {i} | {pts} | {line} | {', '.join(hits)} |")
    report = "\n".join(out) + "\n"
    dst = Path("research/topic-backlog.md")
    body = f"# Topic backlog — ranked by corpus rubric ({src})\n\n{report}\n" \
           f"\nRules: scores are TRIAGE ordering, not view promises. Corpus hit evidence: the Zack/MinutePhysics/\nMinuteEarth/Kurzgesagt corpus notes (research/video-notes/) + our own views.csv (sunsets 1153 vs 200 for black-hole).\n"
    dst.write_text(body, encoding="utf-8")
    print(report)
    print(f"wrote {dst}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
