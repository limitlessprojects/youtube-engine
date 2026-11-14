# How Stitches Work — Zack D. Films (~255M views, 31.1s)
**Source: youtube.com/watch?v=ttuKeS5k4Uo · accessed 2026-11-14 · analysis-only

## 01 Verdict
Textbook body-horror hook: a raw open leg wound fills frame 0 with zero words on screen, then the video calmly narrates the healing biology — spectacle first, science second.

## 02 Hook anatomy
- Frame 0 (t≈0.05s): extreme close-up of a shin with a deep, open, bloody laceration, red-white wound interior, leg against flat sky-blue backdrop, white sneaker just entering frame bottom-right. No text, no title card. The wound IS the hook.
- Frame 1 (f00, ~t=0s): the wound is being laced shut — white suture thread crisscrossing taut across the gap; information gap widens (what happens next inside?).
- Frame 2 (f02): time-skip — same wound now healed pink with neat white stitch spirals; one legible story beat without a single cut of explanation.
- Retention driver: open question + mild disgust response ("how does that close?"). VO opens with "when you get stitches…" — names the topic in the first words (satisfies our S3 orient law).

## 03 Craft notes
- Palette: saturated warm skin tones + wound reds against a clean cyan-sky gradient; high saturation, low noise, cinematic 3D render (Blender-class).
- Lighting: soft key from above/side, subsurface-scattering skin shading; wound interior lit to read wet/glossy.
- Composition: vertical 9:16, subject fills 80–90% of frame width, camera pushes in/rotates slowly; shallow depth.
- Background discipline: flat, single-hue sky — never competes with the subject; no environment clutter.
- Type: small white sentence-case captions, bottom-center band, 1–3 words per beat ("If you", "just go ahead" pattern seen across this set) — text never covers the wound.
- Motion language: continuous slow camera arc + progressive tissue simulation; no cuts.

## 04 Pacing + cuts
- Hard cuts detected: **0** (scene_changes.txt empty — continuous single-take camera/simulation; possibly below detector threshold, UNKNOWN if any dissolves exist).
- Mean shot length ≈ 31.1s (single continuous shot).
- WPM: ~77 words / 31.1s ≈ **149 WPM** — below our ~200 WPM Shorts target; Zack breathes. Slow, confident cadence.
- Observation: zero cut-density; momentum comes from tissue-state progression (open → laced → inflamed → healed), i.e. a simulation time-lapse, not edit rhythm.

## 05 What maps to our pipeline
- Hook calibration rubric: frame-0 spectacle with zero text is a strong "hook_impact" archetype — our #0002 gold-standard alternative; supports ruling that text is NOT required at t=0 when the image poses the question.
- Style bible: his flat-sky discipline validates our "background = one of {deep space, raised, nebula}" rule — one field, zero competition. Our bible is darker; he proves legibility wins over palette match.
- Stickman animation approach: his tissue-progression time-lapse (state A → state B in one continuous shot) maps to our engine's morph/simulation beats — worth a "wound-healing style" state-machine test for science explainers.
- Gate/ultracritic: candidate anchor for "hook without text" calibration case; probe_hook.py should score pure-image hooks against our text-heavy calibration set to avoid bias.
- Topic selection: body-interior "gross but educational" topics (stitches, splinters) are his highest-view lane.

## 06 Judge anchor?
Likely 7.5+ on hook_impact and composition/legibility; fails our dark-bible palette consistency (he is bright-sky, we are deep-space) and text_discipline is trivially satisfied (almost no text). Not a style match for slots 4–5 of style bible §4, but a valid hook-impact anchor. Would pass the 7.5/7.0 bar as a judged frame on its own merits; would NOT anchor our palette.

## Compliance: no verbatim quotes >50 words; no fake data; cut count from empty scene_changes.txt (0); view count from wishlist brief (~255M). UNKNOWN: exact render engine, upload date, whether dissolves exist below detector threshold.