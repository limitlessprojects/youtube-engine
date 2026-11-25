# mromidev/claude-animated-shorts — deep read + adoption plan (day-030)

Source: github.com/mromidev/claude-animated-shorts (4.9k stars, MIT). A Claude
skill for code-rendered animated shorts — same philosophy as our pipeline (the
video is REAL rendered animation written by the agent, no AI video generators).
Their proof: "The Bridge That Fell for a Song" (67s, 1831 Broughton bridge);
friend reports 40k subs with these techniques. This note maps their measured
style bible (references/STYLE_BIBLE.md, built from 20 reference shorts) onto
our pipeline and names what we adopt for #0013+.

## The five deltas that matter (measured, ours vs theirs)

| dim | theirs (20 refs) | ours (#0012) | fix |
|---|---|---|---|
| luminance | lum mean 0.43-0.54, p98 0.9-1.0 | dark navy night ~0.3 | brighten worlds to lum ~0.5, keep blacks for contrast beats |
| saturation | 0.38-0.65 (VERY saturated) | muted blue-gray | raise to ~0.5; gold accent stays the through-line |
| depth | 3D toon env, hand-painted textures, ink outlines, soft DOF | flat 2D parallax-less scenes | paint the world (three layers + blur bg), thin ink outlines on edges+creases |
| camera | holds 80% + ease-out bursts (peak px/frame decaying over 8-10 frames), continuous follow moves BETWEEN subjects, push-ins, dutch tilts | static per-scene, event-led | camera-led motion: follow-the-object moves, 4-frame flash cuts instead of hard swaps |
| lighting | warm key + blue/purple shadows, window-light pools TINT characters, transitions with story beats (noon→sunset→night-blue) | flat night+moon | keyed scenes with pools + beat-linked light transitions |

Their feed thumbnail is BRIGHT and saturated; ours is a dark navy frame — a
CTR-visible difference on the Shorts shelf before a single frame plays.

## Script formula (20/20 follow it) — gap analysis for #0013

1. **Hook**: paradox as fact, sentence 1, ~10-16 words, no setup. (We match:
   "EVERYBODY PARTIES. EXCEPT ME.")
2. **Setting**: 1-2 lines, present tense, named everyman, numbers. (Match.)
3. **Escalation**: 3-6 beats where OTHERS laugh/doubt/mock — SHORT DIALOGUE
   LINES — stakes climb. (We DON'T match: #0012 has zero quoted lines from
   other characters. The huss chant is ambient, not voiced friction.)
   → adopt: give the town quoted lines; mockery aimed AT the protagonist.
4. **1-2 exaggeration jokes**: claim-vs-reality gags. (We don't match;
   the "4s TOO SLOW" metronome gag was close — keep and sharpen.)
5. **Mystery beat**: a "Wait, …?" question, ~1 per video. (Adopt.)
6. **Pivot word**: "You see," (14/20 videos) → mechanism via everyday analogy.
   (Adopt where lane-appropriate; horror lane can use "Here's the thing,".)
7. **Ironic payoff**: last 1-2 sentences, lands twist, ends on last word.
   (Match — #0012's "making sure I'd say yes." is exactly this.)

Sentence style: ~13.5 words median, plain spoken, contractions, every sentence
illustrated literally, props carry jokes. Voice: 3.5-4.1 w/s (median 3.7 =
~222 wpm) — ours measures 186 wpm; the fiction lane's slower read is
deliberate, but #0013 should sit ≥3.4 w/s outside the twist/tail beats.

## Audio + captions

- Loudness −14 LUFS integrated, LRA ~2.4 (heavy compression), music/SFX bed
  only 5-10 dB under speech. Ours: bed −13.1 dB (slightly colder) — nudge to
  ~8 dB under for #0013, keep the A5 register rules (no 100-300 Hz mud, L-124).
- Their scores are designed ("march scores") not ambient pads — consider one
  motif instrument tied to the town (the huss chant itself can BE the score).
- Captions: ONE word at a time, white bold sans + thin black outline,
  lower-middle, hard swaps. Our overlay_caps.py does phrase-level — switch to
  word-mode for #0013.

## Camera recipe (concrete numbers)

- Holds ~80% of frames (<0.5 px/frame); moves are ease-out BURSTS: peak speed
  first frame, decay over 8-10 frames (e.g. 720p px/frame: 6,26,12,14,6,5,2,1).
- Hard cuts ~0-1 per video; most "cuts" are 4-frame flash effects; place
  changes ride 6-8 frame crossfades.
- Continuous follow moves: camera rides a bullet/oil-stream/ball BETWEEN
  subjects — one move stitches two beats.
- Slow push-ins during holds; low camera heights; dutch tilts for drama/falls.

## QA loop (already our shape — keep)

story.ts shot planning → stills → side-by-side sheets → frame-by-frame QA vs
reference → 2K render + sound mix. Ours: beat sheet → scenes.html → keyframes
→ ultracritic → finish_v3. Adopt their SIDES-BY-SIDE practice: tile our frame
next to the matching reference frame during render QA (contact_sheet.py
already does tiles — add a --with-reference mode).

## Adoption plan (sequenced for #0013, not a rewrite)

1. **World relight** (biggest win, cheapest): lum → 0.5, saturation → 0.5,
   painted 3-layer depth with bg blur, ink outlines, window-light pools.
   Reuse scenes.html engine; add a --look bright3d preset. MEASURE lum/sat
   with the same stats (pixcheck) and pass/fail against the bible's bands.
2. **Camera-led motion**: ease-out burst helper in the render engine; every
   scene gets one move (push-in or follow); 4-frame flash cuts replace hard
   scene swaps; keep motion-probe green (zero dead beats).
3. **Escalation dialogue + mystery beat + pivot** in the beat sheet template
   (fiction lane keeps its twist grammar; the middle gets voiced friction).
4. **Word-mode captions** + bed to −8 dB + motif instrument.
5. Keep: 186-200 wpm pacing flexibility for horror, hook-at-frame-1, no CTA,
   twist-ends-on-last-word.

## What NOT to adopt

- Their 3.7 w/s median as a hard floor — our fiction lane breathes; the bible
  is a longform-adjacent story lane (99.5 WPM competitor blueprint sits in
  research/blueprints/), Shorts story lanes skew faster but twist-tales hold.
- "No captions unless user asks" — YouTube Shorts retention data favors ON
  captions for our audience; keep captions, upgrade their style.
- Copying their look wholesale: adopt the MEASURABLES (lum/sat/depth/camera),
  keep the Jack Blessed night-fiction identity (gold envelope accent family).
