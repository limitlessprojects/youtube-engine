# Video wishlist — boss-downloaded learning intake (v1, 2026-11-14)

> You asked which videos I want downloaded and sent. This list is mapped to real
> pipeline debts, not generic "inspiration": the funded video-VLM calibration
> debt (carry_r10), the empty `learning_queue.txt`, C15 motion craft, the L-097
> beat law, and hook/frame-0 calibration. Send in tiers; every file that lands
> gets processed the same day (protocol at the bottom).

## How to send (keeps my intake fast)

- **Format:** MP4 preferred (MOV/AVI fine). 1080p is plenty — no 4K. Keep each
  file under ~100 MB.
- **Trim long-forms** to the 2–4 minutes that matter and put the timestamps in
  the name, e.g. `VL-06-egg_00m-04m.mp4`. Shorts: send whole.
- **Naming:** `VL-<number>-<short-slug>.mp4` using the numbers below.
- **With each batch, paste the source URLs** (one per line, same order as the
  files). I seed `config/learning_queue.txt` from them for the
  transcript/blueprint pipeline and record provenance in the notes.
- Public YouTube/Vimeo only — nothing paywalled or private.

## Tier 1 — Shorts-native benchmark set (SEND FIRST)

Feeds: hook_impact calibration, topic selection, retention model, #0006.

| ID | What | Where | Why I want it |
|---|---|---|---|
| VL-01…05 | Zack D. Films — his 5 most-viewed Shorts (Shorts tab → Sort: Popular) | youtube.com/@zackdfilms | The king of our exact format: 29.7M subs, ~83B total views (vidiq, 2026-11-14), community-reported ~3 Shorts/day averaging ~5M views, 23 Shorts over 100M. I need his frame-0 hook anatomy, VO cadence, caption placement, loop closers, and how the title IS the hook. |
| VL-06 | Kurzgesagt — "The Egg" | youtube.com/channel/UCsXVk37bltHxD1rDPwtNM8Q (Popular tab) | Their most-viewed (~89M reported). Gold standard for our ceiling: palette discipline, parallax depth, detail density — the concrete G9 bar. |
| VL-07 | AlternateHistoryHub — "What if Germany Won WWI? (Part 1)" | youtube.com/user/AlternateHistoryHub | The what-if spine: divergence point → domino chain → escalation. Direct template for our #0001-style topics. |
| VL-08 | Kurzgesagt — "How to Make a Kurzgesagt Video in 1200 Hours" | same channel | Their pipeline in the open: research → script → illustrate → animate → narrate → music (~9.1M views). Mirror-check for our vo_pipeline. |

## Tier 2 — Motion craft (C15)

Feeds: render_short motion quality, G9 critic calibration, style bible §6.

| ID | What | Where | Why |
|---|---|---|---|
| VL-09 | Gunner '22 showreel | gunner.work (reel on site / their Vimeo) | Easing, overshoot, settle and secondary-motion grammar from a top-tier studio (now a non-profit school). |
| VL-10 | Buff Motion — latest showreel | buffmotion.com / their YouTube | Punchy brand-motion: sting-level impacts, quick transitions that read at Shorts scale. |
| VL-11 | Ae Genius — "Beautiful easing curves in After Effects" (or the "Easing — Motion Design Techniques" tutorial) | YouTube search: exact titles | A 3-tier easing taxonomy I can translate into our tween curves directly. |
| VL-12 | Kinetic typography — top 3 pieces from CreativeBloq's "15 must-see examples" (incl. "Shop Vac") or the "Kinetic Typography" YouTube channel | creativebloq.com/typography/examples-kinetic-typography-11121304 | Word-level motion for our kinetic titles/stamps — where the word lands vs the beat. |

## Tier 3 — Structure & rhythm (L-097 beat law, #0006 authoring)

Feeds: script_linter beat law validation, cut-density targets, pacing.

| ID | What | Where | Why |
|---|---|---|---|
| VL-13 | Every Frame a Painting — the "How Does an Editor Think…" episode (+1 more of your pick) | youtube.com/user/everyframeapainting | Cut grammar: why/when a cut lands, rhythm vs continuity — the reasoning behind our no-snap-cut rule (C5). |
| VL-14 | MinuteEarth — their 3 most-viewed Shorts, must include "Why Are Some Sunsets SO MUCH Better Than Others?" | youtube.com/user/minuteearth (Shorts tab) | Our WPM + cut-density benchmark per channels.json. The sunsets Short directly overlaps our live #0003 — a free A/B against our own treatment. |
| VL-15 | MinutePhysics — their 3 most-viewed Shorts | youtube.com/@MinutePhysics (Shorts tab) | Hand-drawn minimalism ceiling: how simple visuals carry dense ideas. |

## Tier 4 — Hero-shot i2v route (C16, tools/hero_shot/)

Feeds: the free-GPU Wan2.2-Animate route (L-093), first hero shot for #0006+.

| ID | What | Where | Why |
|---|---|---|---|
| VL-16 | Wan-Animate official demo video(s) — the motion-swap reference you named | humanaigc.github.io/wan-animate | The exact route: character image + performer video → character performs. I need the input→output pairing to spec our first hero shot. |
| VL-17 | One Wan 2.2 Animate ComfyUI demo output | reddit.com/r/comfyui/comments/1nle575 (workflow + demos thread) | A second real input/output pair to grade fidelity and failure modes. |
| VL-18 | (no download) A 5-second phone clip of YOU performing one clear action (point / wave / duck) against a plain wall | filmed on your phone | A clean motion-source: our character keyframe + your performance = a real hero-shot test on the free ZeroGPU route, zero downloads needed. |

## Tier 5 — Style anchors + public-domain raw material

Feeds: style bible §4 open reference slots, C14 assets, C17 accuracy pass.

| ID | What | Where | Why |
|---|---|---|---|
| VL-19…20 | 2–3 animated shorts whose frames MATCH the bible aesthetic: deep-space background, ONE amber accent, teal rim, ink outlines, glow | your eye — anything that "feels like our #0002 hook frame" | Calibration frames for the two open reference slots in style bible §4. |
| VL-21 | NASA footage: 1 rocket launch + 1 Earth-from-space sequence | nasa.gov (public domain) | Hero-shot grading tests + accuracy-pass material for space topics (#0001 lineage). |
| VL-22 | USGS volcanic eruption footage | usgs.gov (public domain) | Krakatoa/Anak Krakatau realism for the accuracy pass (C17) — it is literally our #0005 topic family. |

## What happens to each file (so the learning compounds)

1. **video-understand pass** on the MP4 (the funded video-VLM this box has —
   this closes carry_r10's "needs one funded video-VLM" debt) → structured
   notes in `research/video-notes/VL-NN-<slug>.md`.
2. **Frame-0 + pixel probe** on every Short → hook pattern library (what the
   top performers do in the first 2 seconds vs us).
3. **Cut/beat map** (transition timestamps vs VO timing) → validate or refine
   the L-097 law (`beats ≥ ceil(VO/3.2)`) before #0006 is authored.
4. **Judge anchors:** 2–3 known-gold frames from the corpus through
   ultracritic → anchor the scale against L-101 judge drift.
5. **Transcripts** from your URL manifest → `config/learning_queue.txt` →
   blueprint_extractor (the daily loop finally gets fuel again).
6. **Deltas** → style-bible proposals (need your directive per C13), render
   engine, critic prompts. Everything committed to the repo.

## Priority if you only send a few

VL-01…05 (Zack D. Films) → VL-06 (The Egg) → VL-09 (Gunner reel) → VL-16 (Wan-Animate demo).

## Do not bother sending

- Our own published Shorts (I can re-render every cut deterministically from source).
- Full 10-minute long-forms — trim to the segment that matters.
- Anything paywalled, private, or behind a login.

## Compliance line

Study corpus stays local in research notes (analysis only — nothing borrowed is
ever composited into a published Short). Only public-domain/CC0 material
(NASA/USGS/Wikimedia) may enter renders, with license noted in
`content/<slug>/assets/NOTICE.md` per the free-material policy.
