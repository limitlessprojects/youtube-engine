# Playbook — Audio (stage 4 of 7)

> Purpose: assemble VO + synthesized sound design, master, and verify the mix by
> measurement (rule A1).
> Inputs: `render/frames/` (full frame set from stage 5 — audio is often run
> after the first full render), `vo/NN.mp3`, `script.json` (timestamps + `sfx`).
> Outputs: `vo/master.m4a` (−14 LUFS), `<slug>.mp4` (muxed), `vo/master_report.json`.

## Commands

```bash
python3 tools/finish_v3.py <slug>
# then the mechanical mix check is part of the gate (A5) — but run it early:
python3 tools/ultracritic.py <slug> --skip-mechanical   # frame pass needs gate/*.png
# A5 specifically: re-run ultracritic mechanical after the master exists.
```

What finish_v3 does (all parameters: docs/parameters.md §Audio):

1. Decodes VO lines, places each at its `timestamp_start` (rule V1 made these real).
2. Synthesizes the bed: warm Aadd9 pad, detuned voices, air noise — **0.16 peak**
   (the old 0.062 was inaudible), **−9 dB duck under VO spans** with 150 ms ramps
   (the old formula was INVERTED — loudest under the voice; L-074).
3. Places the per-short `sfx` table from script.json (riser/whoosh/thump/blip,
   numpy-synthesized, license-free — rule A4). No table → the #0002 legacy
   fallback (don't rely on it; write the table).
4. Two-pass loudnorm → −14 LUFS / −1.5 dBTP / LRA 11 → AAC 192k.
5. Muxes frames via `image2pipe` (rule R1) → `<slug>.mp4` + `master_report.json`.

## Rules that bite here

A1 mix measured (A5 gate: non-VO RMS 6–22 dB under VO) · A2 −14 LUFS master ·
A3 SFX land in the pause AFTER the word · A4 synthesized only.

## Known failure modes

| Symptom | Cause | Fix |
|---|---|---|
| A5 FAIL "bed inaudible (< −22 dB)" | level too low OR duck math inverted again | check `finish_v3.bed()` peak (0.16) and the duck sign (LOW during VO); re-measure, never trust comments (L-074) |
| A5 FAIL "bed too loud (> −4 dB)" | mud under the voice | lower bed peak; keep −9 dB duck |
| SFX buries a word | hit lands ON the word | move it into the pause after (rule A3) |
| master_report shows LUFS far off −14 | one-pass loudnorm or changed mix | finish_v3 is two-pass; re-run and read the report |
| encode hangs/dies on 1000+ frames | image2 demuxer (L-072) | finish_v3 already pipes; if a custom encode is added, pipe it too |
| ffmpeg exits 255 after success | wrapper noise in this sandbox | verify artifacts (file size + ffprobe), not exit codes |

## Acceptance check

- `master_report.json`: LUFS within ~±1.5 of −14, TP ≤ −1.5, duration ≈
  `timeline.total_s + 0.45`.
- Ultracritic mechanical A5 prints `bed … dB under VO ✓`.
- Ear check once through: every word clear, hits off-words, bed present in gaps.
