# #0006 v3 — watch of the LIVE upload (BHRLMfSbHBw), 2026-11-16

Method: `tools/watch_video.py https://youtu.be/BHRLMfSbHBw` — the YouTube-served file (AV1 1080×1920@30,
39.16 s) tiled at 10 fps and read in order by the agent, plus measured motion and audio. The agent did
not hear the audio; audio lines below are measurements only.

## Measured
- Motion (motion_probe, 1 s bins): median beat energy **0.0051** (probe target ≥ 0.01). 39 s = 6 moving,
  29 ambient, **4 dead: 9–10 s, 20–21 s, 23–24 s, 37–38 s**.
- Same probe on #0005 (published, 631 views in 5 h): median 0.0013, 18 dead of 36. v3 is ~4× livelier
  than the last published short and still under the probe's own target.
- Audio as served: −15.5 LUFS integrated, −3.9 dBTP, 0 clipped samples; starts within 0.1 s, fades over
  the last 0.7 s. Bed+SFX 8.3 dB under VO (measured on the local master).

## What the filmstrip shows
Works:
- Frame 0 is a complete picture with the title; the last frame matches it, so the loop joins cleanly.
- Every scene change is a camera whip with one in-between frame; no flash frames, no blank frames.
- X-ray sweep (7–8.6 s), needle ladder (14–16.6 s) and zip-shut (18–20 s) read clearly in sequence.
- All text is legible at 180 px wide tiles; no text collides with the hero or the thread.

Does not work — one pattern, repeated in 9 of 13 scenes:
- **The action finishes early and the picture then holds while the voice keeps talking.** Stills hid
  this; the filmstrip makes it obvious. Hold lengths after the last meaningful change:
  s0 ~1.0 s (empty wound after the stitches fall) · s1 ~1.6 s · s2 ~1.8 s · s3 ~1.1 s · s4 ~1.3 s ·
  s5 ~1.6 s · s6 ~1.0 s · s7 ~1.4 s · s10 ~2.0 s. Only idle motion (ECG, hero sway, slow push) remains.
  These are exactly the probe's dead/ambient seconds.
- Hook: the needle hovers for the first ~1.2 s before it moves. The first second is the one that
  decides the swipe.
- s3: the flat needle reads as a pale hook riding above the ladder, not as a needle in tissue.
- s7: the dissolve happens in a small area at the top of the seam; most of the frame is unchanged.
- s8: the cell column still reads as a zipper of ovals.

## Verdict (agent, not a model score)
Clear and good-looking, under-animated. It is better than anything on the channel on subject, contrast
and continuity, and it would likely still lose points on pacing/edit-flow with a real video judge.
It stays up: the repo forbids delete-and-republish, and none of this is a factual error.
The fix belongs in #0007's scene writing (rule C18), not in a re-upload.
