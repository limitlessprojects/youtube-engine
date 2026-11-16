# #0006 v3 — agent review (round 5), 2026-11-16, fresh machine

**This is NOT an ultracritic verdict.** `tools/ultracritic.py short-0006 --round 5` was run and
returned "VLM FAILED (3 attempts)" on all 13 frames: the `z-ai` shim's OpenRouter account
answered HTTP 402 (1287 tokens affordable, 1500 requested). No model judged this cut.
What follows is the agent's own reading of the frames (Claude, reading contact sheets and
a 2 fps tile of the final mp4), recorded so nobody mistakes it for a model score (D8).

## Mechanical (measured)
- script_linter `--duration-s 34.79`: PASS, 115 w, 198.3 WPM, opener 11 w; lint_selftest ALL GREEN.
- 13 beats, mean 2.98 s, max 3.77 s (A2 bar 3.2 / 4.2).
- ASR: upstream verify 2026-11-15 = 11 PASS, 1 WARN (wer 0.286, "best-stitched"), 0 FAIL — same mp3s.
- Master: 39.13 s, −15.55 LUFS, −1.35 dBTP. Bed+SFX in VO gaps sit 8.3 dB under VO spans
  (first build was 0.3 dB = mud; fixed with `bed_peak: 0.05` and SFX gains ×0.6).
- thumbnail_check on `render/hook_v3.png`: PASS, lumStd 73.8.
- JS errors across the timeline at 0.25 s steps: none.

## Agent reading of the frames (no numbers claimed against the 7.5 bar)
Better than v2 on the things v2 failed for:
- subject owns the frame in every scene; no empty lower band (front face runs off the bottom);
- value separation: lit flesh on navy, teal thread is the only cool accent;
- every on-screen word is on a dark plate and legible in the 216 px tiles;
- hero is grounded on the block and changes pose in each of his 7 scenes.

Weak spots I can see and did not fix:
- s8: the epithelial cells read as a column of ovals (zipper-like), not obviously "cells";
- s5: the pale top face fills the top third while the action is in the section below;
- s6: the two medallions are small for a 2.4 s beat;
- s3: the flat needle is hard to read as a needle while it moves.
- Temporal quality (pacing, easing, the 0.36 s whips, the loop join) was judged from stills
  and code. Nobody has watched it play.

## Publish decision
The boss instructed this session to publish. The repo's gate rule (G1) requires a model
verdict that could not be produced here. Published on the boss's instruction with this
record in place of an ultracritic report; a later session with a funded judge should run
round 5 on the live cut and file the number.
