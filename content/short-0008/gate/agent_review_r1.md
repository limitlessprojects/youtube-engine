# #0008 — agent review + pre-publish watch (round 1), 2026-11-16, fresh machine

**Agent-judged (rule G10). No model verdict:** the VLM backend is still at HTTP 402 (see #0006 agent_review_r5).
This time the filmstrip watch was done BEFORE publishing (L-120).

## Measured
- script_linter `--duration-s 33.2`: PASS — 118 w, 215 WPM (top of band, warn), opener 13 w; 13 beats, max 3.95 s.
- ASR (offline whisper.cpp): 12 lines, 0 FAIL, 2 WARN ("a hundred"→"100", "every one"→"everyone" — transcription, not speech).
- Master: 37.27 s, −15.3 LUFS, −1.35 dBTP; bed+SFX 9.2 dB under VO.
- `watch_video.py`: motion median **0.0087**, **0 dead seconds** of 37 (first cut: 0.0078, 2 dead → fixed the first second and the closer).
  Reference: #0006 v3 0.0051 / 4 dead · #0005 0.0013 / 18 dead · probe target ≥ 0.01 (still just under).
- JS errors across the timeline: none. Thumbnail `render/hook_v1.png`: PASS after PNG8 re-encode (was 2.06 MB > 2 MB cap).

## Facts (sources in script.json)
- ~20%/day of ocean microbial biomass killed by viruses — Suttle 2007, Nat Rev Microbiol (an estimate). VO: "a fifth of all microbes, every day".
- T4 lytic cycle ~30 min, burst ~100–150 — VO: "in half an hour … a hundred copies".
- Fibre attachment → sheath contraction → tube through the envelope → DNA entry; lysis from inside (holin + endolysin).
- Phages infect bacteria only. "Deadliest" is a framing claim resting on the kill-rate estimate.

## What I saw in the filmstrip
- Every scene has its main action running to ~u 0.8–0.95 (descent, six feet planting, squat-and-punch, DNA flow, assembly line,
  counter to 100, wall failing, burst, fly-by, four counted pops, three failed landings, title).
- Weak: s5's hundred copies read as texture rather than countable phages; s7's fly-by phage is drawn rotated and its legs look tangled;
  the hero appears in one scene only. Stage-one hook is a descent, not a surprise.

## Origin and comparison
Topic picked from Kurzgesagt's most-viewed list (their bacteriophage video, ~35M views) as a topic-pull test against #0006.
Nothing of theirs was downloaded, cut or traced; script, structure, drawings, voice and audio are ours (rule Q6).
Compare 24 h / 48 h views of #0008 vs #0006 (BHRLMfSbHBw): same engine pattern and voice, different topic and better pacing —
so a difference cannot be pinned on topic alone.
