# How to Make a Kurzgesagt Video in 1200 Hours — Kurzgesagt (~9.1M views, 408s)
**Source: youtube.com/watch?v=uFk0mgljtns · accessed 2026-11-14 · analysis-only**

## 01 Verdict
Their studio's own pipeline documentary — research → script → illustration → narration → animation → music — shipped as a bright, flat, infinitely-loopable cityscape illustration that never stops moving. It is the clearest map of what "one video = 1200 hours" means, and the honest yardstick for what our $0/day pipeline can and cannot replicate.

## 02 Hook anatomy
- Frame 0 (hook.jpg, t≈0s): bright cyan sky, flat cartoon city (pink/magenta rooftops, hot-air balloon, birds on a chimney, distant teal skyline). Zero text. The promise is carried by VO + familiar Kurzgesagt art: *the city you live in is the studio that makes the videos you watch.*
- Frame 1 (f00, t≈0s): Kurzgesagt logo spin-in on deep navy — brand stamp.
- Frame 2 (f02, t≈1:45): bold white "ILLUSTRATION" section card with purple circuit-board motifs and a progress-line node graphic, birds perched around — the video is openly structured as pipeline stages with literal chapter cards.
- Title promise: "How to Make a Kurzgesagt Video in 1200 Hours" — a number + a mystery (why 1200?). Audio open: "for years people have asked how we make our videos so let's finally talk about it… how to make a Kurzgesagt video in 1200 hours or more."
- What frame 0 promises in the first 2 seconds: *a cheerful, maximalistly-detailed answer to "how is this made" — you will see the whole machine.*

## 03 Craft notes
- Palette: daylight register — cyan→teal sky gradients, magenta/pink rooftops, lime/emerald trees, hot-air balloon accents; night register for space scenes (deep navy + glowing Earth, f00). Two registers again, one per story beat.
- Parallax/depth: multi-plane cityscape (clouds ~0.2×, skyline ~0.4×, buildings/trees ~0.7×, birds/balloon foreground ~1.2×) — the strongest depth read of the three; everything drifts independently.
- Detail density: extremely high but flat-vector — every window, antenna, chimney bird, and tree is a deliberate shape; "wow" props (hot-air balloon with pattern, chimney swallows) recur as motifs.
- Motion grammar: constant gentle drift + loop; section cards punctuate stages; characters (birds, duck-like crew members) carry business through every scene; holds are rare — motion is the glue, not cuts.
- Character work: recurring duck/bird mascot-crew — simple shapes, strong silhouettes, expressive eyes; used as "studio staff" stand-ins.

## 04 Pacing + cuts
- Cut count (scene_changes.txt): only **2 detections** (t≈15.03/15.07 — a double-cut flash frame, and t≈141.5) — the detector almost entirely missed transitions because the video uses fades/animated wipes and continuous scenes. Real scene-change count is much higher; **UNKNOWN** (detector limitation).
- Mean shot length: not measurable from the detector; visually the video is long continuous animated scenes with section-card punctuation.
- WPM: ~4,782 raw VTT tokens / ~1,034 deduplicated words ÷ 6.8 min ≈ **~150 WPM**. (Karaoke VTT deduplicated; approximate.)
- Attention control: perpetual micro-motion (drifting clouds, bobbing balloon, birds landing) + chapter cards as progress markers + a running numeric mystery (1200 hours) resolved at the end.

## 05 What maps to our pipeline
Mapping their six stages 1:1 onto ours:

| Their stage | Our equivalent | Gap |
|---|---|---|
| 1. Topic from an ever-growing list, "whatever excites us" | `content/` shorts queue (short-0001..0005) + `research/video-wishlist.md` | GAP: no living topic backlog scored by excitement/feasibility; our picks are ad-hoc per day |
| 2. Research: books, papers, expert interviews; view can change mid-research | none — `tools/blueprint_extractor.py` only extracts visuals; no research step | **BIG GAP**: no research artifact, no expert fact-check loop; our scripts are written from general knowledge |
| 3. Script: rough draft → rewritten repeatedly → external expert fact-check; "usually takes 2–3 weeks" | `script_linter.py` (style/lint) + manual writing | GAP: no multi-draft rewrite protocol, no external fact-check, no ~2–3 week script SLA; our scripts are same-day |
| 4. Illustration: 2–3 illustrators, 8–12 weeks, Illustrator, asset library + from-scratch | generated cutouts (`rembg_cutouts.py`, `cutout_assets.py`) + engine scene composition | **BIG GAP**: no human illustration, no shared asset LIBRARY with reuse tracking, no 8–12 week per-video budget; our assets are one-shot generations |
| 5. Narration: recorded in a small booth after full illustration | `tools/vo_pipeline.py` (edge-tts AndrewNeural, +45% rate, ASR-verified) / `fish_tts.py` | partial: we have ASR verify + timeline sync; GAP: no booth-quality human VO, no intimacy direction, single fixed voice |
| 6. Animation: AE + C4D, hundreds/thousands of parts, scenes taken apart & rigged, 8–10 weeks, every motion manual | `engine/rig.js` (procedural rigs), `engine/world.js`, `engine/core.js` (procedural animation, no manual keyframing) | **BIG GAP**: our animation is procedural/parametric; theirs is hand-keyed for 8–10 weeks — our asset-decomposition discipline (layers for parallax) is right, the motion authorship is not |
| 7. Music: ORIGINAL song composed to the finished video; SFX as "icing" | `tools/finish_v3.py` synthesized Aadd9 pad + riser/whoosh/thump | **BIG GAP**: our "music" is a template pad; no original composition, no picture-timed scoring |
| 8. Parallel production (2–4 videos at once) + review every few days | daily_loop cadence, sitrep | partial: we parallelize via queue, GAP: no structured multi-day review sittings / tweak-until-right loop |
| End | `tools/render_short.py` + `finish_v3.py` mux; `gate/` + `ultracritic.py` | our gate is automated; theirs is human review — complementary, not equivalent |

- **content/style-bible.md**: their daylight cityscape register is NOT covered by our dark bible at all (our §1 allows only deep-space/raised/nebula backgrounds) — if we ever want bright-register scenes, bible amendment needed. Their 1200-hour budget is the sanity check for every "just make it look like Kurzgesagt" request: one of our shorts costs ~0 human-hours of illustration; theirs costs ~200+.
- **gate/**: our G9 detail-density gate would flag their flat-vector birds as "simple shapes" if judged on stroke count — the gate must judge *composition density*, not primitive count (worth checking ultracritic's G9 wording).

## 06 Judge anchor?
Partially — an anchor for "motion glue + multi-plane parallax + register discipline," not for our dark palette. Would clear 7.5 on composition/depth/motion; would not clear our palette-consistency check (bright daylight vs. locked dark bible) and would be an unfair G9 benchmark (hand-illustrated vs. generated). Use as process benchmark, not frame anchor.

## Compliance: analysis-only; quotes ≤12 words; cut count from scene_changes.txt (2 detected; detector misses fades — true count UNKNOWN); views/durations from wishlist brief. UNKNOWN: exact per-stage hours beyond what VO states, team size beyond 2–3 illustrators/animators, publication date.
