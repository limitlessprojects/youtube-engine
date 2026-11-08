# Exemplars — measured references (frames regenerate deterministically)

**Honest status: no video has passed the 7.5 bar yet.** These are the two
measured anchors every new short is judged against. Frames are NOT stored
(`content/*/gate/*.png` is gitignored); regenerate them from the committed
specs — that is the point of the deterministic engine (rule C6):

```bash
python3 tools/render_short.py short-0004 --keyframes   # the ceiling
python3 tools/render_short.py short-0003 --keyframes   # the failure case
```

## short-0004 — "Why is the sky blue? (It's not the ocean)" — THE exemplar (ceiling 6.92)

- **What to copy:** question-first hook naming the topic at beat 1 (S3); 11
  distinct poses + blinks + breath bob (C4 — character_life 8.0); one text
  system per scene — stamps or a single keyword pill, never both (C1 —
  text_discipline 7.4); day-world grade with a LIGHT vignette (C11 — contrast
  7.2); cards breathe with 0.25s ease-in / ≥0.5s holds; 2.83s mean beats at
  201 WPM (S5/S6 — pacing_rhythm 8.0); 0.25s gaps; per-short sfx table;
  `gate/notes.json` per scene.
- **Spec:** `content/short-0004/` (script.json, vo_lines.json,
  render/scenes.html).
- **Scores (round 4, day-010):** frame grand 6.76 · video pass pacing_rhythm
  8.0 / character_life 8.0 / edit_flow 7.0 · combined **6.92 vs bar 7.5 → NO POST**.
- **Remaining drags (your target):** visual_hierarchy 6.1 (dead zones, focal
  fight), hook_impact 6.4 (frame-judge poster bias on diagram frames), 4 frames
  under the 6.0 floor (hook, s5, s8×2). r4 directives (re-derive from a fresh
  round — the report was lost to BUG-1, see `docs/_audit/inventory.md`):
  NOPE hold idle, cadence variety in 12–28s, loop character position.

## short-0003 — "Why are sunsets orange?" — the measured FAILURE case (5.20)

- **What it proves (boss-criticized, then ultracritic-quantified):** 22
  words/frame full-sentence captions = text_discipline **2.8**; 4.22s mean
  static holds = pacing **5.5**; one pointing gesture all video =
  character_life **6.2**; dark-on-dark line art = contrast min **4**; topic
  ("sunset") first spoken at t≈14s (S3 violation); Mars tangent in the closer
  (S4 violation).
- **Why keep it:** the gate was control-tested against this video (rule G5) —
  it catches every one of these failures mechanically or by rubric.
- **Spec:** `content/short-0003/` (published 2026-11-08 as DeaEvEduh88 — the
  lesson that produced rules C1/C4/C5/C11 and the bar itself).
