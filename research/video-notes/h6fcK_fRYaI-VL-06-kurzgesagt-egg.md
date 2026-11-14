# The Egg — A Short Story — Kurzgesagt (~36M views, 486s)
**Source: youtube.com/watch?v=h6fcK_fRYaI · accessed 2026-11-14 · analysis-only**

## 01 Verdict
The G9 ceiling for a reason: a second-person existential hook ("you were on your way home when you died") carried by flat-but-luminous vector illustration with enormous emotional range — it proves that a palette-locked, 2D, zero-3D short can out-hit blockbusters on feeling.

## 02 Hook anatomy
- Frame 0 (hook.jpg, t≈0s): near-black deep-navy frame. Almost nothing on screen — the promise is carried 100% by audio: "you were on your way home when you died." A held black beat forces the ear to lead.
- Frame 1 (f00/f01): giant magenta field, two enormous glossy eyes snap open (f00), then a crescent moon/entity face with dot-eyes looms over a tiny magenta human figure seated on a cosmic hand/planet (f01). Scale contrast: god-entity vs. speck of a person — the premise is the image.
- Frame 2 (f02–f03): the protagonist is shown turning off / looking at a phone (f02), then a warm family hospital scene — father holding newborn, mother on bed, amber/orange palette (f03) — grounding the cosmic premise in domestic stakes.
- Title promise: "The Egg — A Short Story" + thumbnail (not analyzed) promise a twist cosmology; the audio open-question is literal second-person: *you died — where are you now?*
- What frame 0 promises in the first 2 seconds: "this is about YOUR death and something enormous is on the other side of it." No text needed; black + voice = maximum open loop.

## 03 Craft notes
- Palette discipline: two worlds, strictly separated — (a) cosmic register: deep indigo/near-black ground, nebula purple, magenta/hot-pink entity accents, tiny warm sparkles (stars/particles); (b) human register: saturated amber/orange/warm coral domestic interiors with teal-shadowed skin. Never blended in one frame — register shifts ARE the story (death→memory→afterlife→reveal).
- Parallax/depth: layered starfields with twinkling 4-point stars at multiple rates, foreground silhouette masses (entity limbs, hill crests) against gradient nebula sky; human figures sit on mid-ground "hand" forms. Depth is built from value + hue separation, not outlines (background masses are strokeless, matching our bible §3).
- Detail density: low-poly flat shapes but high *meaning* density — every prop (phone, hospital monitor with EKG trace, newborn) is research-true and story-functional; sparkles/particles carry the "cosmos alive" feel. No wasted geometry.
- Motion grammar: slow drifts, scale breathes, eyes blink, particles twinkle; cuts cluster at act boundaries (see §04). Squash on the entity's expressions; stillness is used deliberately (the black open).
- Character work: the "god" entity is a simple crescent-moon face with dot eyes — iconic, instantly readable, infinitely expressive via eye spacing alone. The human is a small magenta silhouette — empathy via scale, not facial detail.

## 04 Pacing + cuts
- Cut count (scene_changes.txt): **43 detections**, but heavily clustered — a burst of ~15 micro-cuts around t≈356–359s (end-beat montage); before that, long holds (5.24s, 13s, 39/39.52/40.72 cluster, 151s, 169–176 cluster, 208, 233, 242, 248, 256, 277, 286, 302–305, 351–359, 364).
- Mean shot length ≈ 486/43 ≈ **11.3s** (long-take grammar; the burst at the end is a deliberate acceleration).
- WPM: ~2,700 raw VTT tokens / ~907 deduplicated words ÷ 8.1 min ≈ **~110 WPM** — far below our 200–210 Shorts band; this is meditative, pause-driven delivery. (Count method: karaoke-rolling VTT lines deduplicated; approximate.)
- Attention control: not cut-density — it uses (1) second-person address, (2) register shifts (cosmic↔domestic), (3) withheld reveal structure ("the Egg" twist lands late). Long holds work because the eye constantly has particle/parallax motion.

## 05 What maps to our pipeline
- **content/style-bible.md §1**: our bible is deep-space dark with one warm accent — Kurzgesagt's cosmic register is the closest living match to `bgDeep #070A18` + `nebPurple` + amber heroes. Their register-split (two palettes for two story worlds) is a technique we can steal: our bible allows world tokens (Krakatoa earth family) — Egg proves a *strict* two-register rule reads as intentional, not drift.
- **style-bible.md §3/§5**: strokeless background masses + outlined heroes — exactly our rule; confirms we're aligned. Their "detail density" is meaning-density (story props), which maps to our gate dimension G9 — but executed with far fewer assets than our layered pipeline assumes.
- **engine/ (core.js, world.js, rig.js, space.js)**: their parallax starfields and breathing scale maps to our `space.js`/`world.js` depth planes; blink/idle maps to `rig.js`. GAP: our engine has no "register switch" concept — no per-scene palette override table; would need a scene-level `register: cosmic|human` token set.
- **tools/finish_v3.py**: their score is original, picture-timed (composed to the finished video). Our synth bed + riser/whoosh/thump is license-free but generic — GAP: no music-per-video composition; our audio is a template, theirs is bespoke. Also GAP: they duck nothing — music and VO are mixed as one artistic whole.
- **tools/render_short.py / engine**: length. Egg is 486s with ~11s mean shots — our Shorts pipeline is 30–60s; the *long-form* ceiling techniques (second-person VO, withheld twist, register shifts) are largely UNUSED in our shorts format. GAP: no long-form template, no twist-structure beat sheet in content/.
- **gate/ + tools/ultracritic.py**: G9 (detail density) and palette-drift checks would pass an Egg frame trivially; but our ultracritic has no dimension for "emotional register shift" or "VO address mode" (2nd person vs 3rd) — GAP in rubric coverage.
- **vo_pipeline**: their narration is human-recorded, intimate, close-mic. Our edge-tts/fish-tts AndrewNeural is serviceable but cannot sell second-person grief; for long-form ceiling work, GAP: no intimate/whisper voice profile validated.

## 06 Judge anchor?
Yes — unambiguous anchor for palette discipline, depth grading, and detail-density-as-meaning (G9). It would clear 7.5 on composition, palette, motion; the hook (black + voice) would fail a naive "frame-0 must show subject" gate, so the gate must not penalize audio-led opens. It would NOT anchor our warm-bright human register against our dark bible — use it only for the cosmic register.

## Compliance: analysis-only; no verbatim quotes >50 words (only ≤12-word fragments); cut count from scene_changes.txt (43, detector-dependent, dissolves may be missed); views/durations from wishlist brief. UNKNOWN: exact upload date, whether hook.jpg is t=0 exactly, full VTT word-level timing beyond sampled cues.
