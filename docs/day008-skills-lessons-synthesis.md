# Skills × Lessons Synthesis — Day 008 (2026-11-08)

> The boss's brief: mine ALL the skills and ALL the lessons, then build Short #0002
> on the result. This doc is the distillate: what 8 days and 61 lessons actually
> change about the way Short #0002 gets made. Everything here cites its source
> (L-### or skill). No vibes.

## 1. The one-sentence diagnosis

Short #0001's premise scored 8/10 and its execution 3.5/10 — the script was never
the bottleneck, the *frame* was (L-059). So Short #0002 inverts the effort budget:
script is already fact-checked and frozen; ~80% of today goes into the visual,
which is where views are won or lost at 195-view baselines.

## 2. The 61 lessons, compressed into 10 working rules

| # | Rule | Source lessons |
|---|------|----------------|
| R1 | **First frame = the premise, on screen at t=0.** Never a caption, never a talking pose. Hook line lands ≤1.8s. | L-016, L-059, v3-spec #1 |
| R2 | **The gap is the world, not the character.** Budget goes to set density, light with a source, depth layers — not to redrawing the stickman. | L-042, day-004 |
| R3 | **Measure, never estimate.** Every timestamp comes from the real VO file duration; every caption width from the canvas measure. | L-003 (day-003), L-005 |
| R4 | **Gate the animation, not the still.** VLM sees keyframes; count-ups at intermediate values and mid-motion squash are by design. Eye arbitration before code changes. | L-045 |
| R5 | **Hard caps everywhere: critic N=2, VLM re-render N=2, TTS retries 3.** Loops are the enemy of cadence. | L-020, L-007, L-023 |
| R6 | **One world, one light, one accent per scene.** Palette tokens defined once; every scene inherits. Dusk-orange on deep blue for #0002, nothing else. | L-004, v3-spec #3 |
| R7 | **ASR-verify generated speech; VLM-verify generated frames.** Both are cheap deterministic round-trips that catch what eyes skip. | L-006, L-059 |
| R8 | **Pacing 170–180 WPM.** #0001's 154 WPM was slow-motion for Shorts; MinuteEarth's 176 is the calibration. | L-056-class (day-007 autopsy), v3-spec #7 |
| R9 | **Credentials and artifacts live in durable mirrors** (`upload/`, the repo). The sandbox is ephemeral by default. | L-058, L-044 |
| R10 | **Cadence beats tooling.** No mid-sprint framework rebuilds; steal patterns instead. | day-007 v3-spec, L-061 |

## 3. What each skill does for Short #0002 (and the next 30 days)

| Skill | Contribution to #0002 tonight | Contribution to the 30-day run |
|-------|------------------------------|-------------------------------|
| stickman-video-director | Rig + pose presets (the hero gawking at the sky) | Style breadth when we add a 2nd format |
| what-if-animation | 7-beat spine → our 8 beats; −14 LUFS master recipe (finish_short.py) | Long-form backbone after day 15 fork |
| tool-reel-system | Caption-sync + pacing math discipline | Edit formula for long-form cuts |
| Youtube_transcriber | — (competitor loop only) | The learning loop's engine, nightly via CI |
| motionmaxxing | Emphasis spent, not spread: beat 4 ("Seven.") gets the longest, richest scene; beats 3+6 are fast stamps | Taste layer on every render |
| motion-skills | Kinetic-type patterns for the caption pops ("SEVEN" scale-pop) | Library to mine per format |
| anthropic skills | Thumbnail/metadata paperwork discipline | Reports + briefs (this doc's format) |
| Remotion | NOT used tonight (R10) | Post-day-30 decision only |
| Manim GX | NOT used (no math overlay needed) | Physics-overlay format later |
| Fish Audio TTS | Deferred: alive per boss (daily free credits) but local key died in recycle #4; edge-tts covers tonight. CI-secret workflow added for batch VO. | Preferred voice once key re-pasted; CI can generate VO without any local key |
| VLM Inspector | The gate tonight — new scene NOTES for #0002, per-scene criticism, N≤2 | Standing gate on every render, forever |
| Openclip | — | Competitor shot-study after first retention data |
| unslop | Applied to this doc + captions (no AI-tell phrasing) | Every user-facing surface |

## 4. Short #0002 build brief (what the synthesis decides)

- **Formula:** everyday curiosity, MinuteEarth 8.7x class (L-060) — chosen
  because it needs charm, not photorealism: our execution ceiling fits.
- **Script:** FROZEN as fact-checked in `content/short-0002/script.md`. Ballerini
  2008 ~7 neighbors; Schiffner & Srinivasan 2016 veer-right + altitude; the
  10x-reaction claim stays CUT. No new claims enter the timeline tonight.
- **VO:** edge-tts `en-US-AndrewNeural` +45% (validated 179 WPM on the hook,
  day 007). Measure every line; ASR-verify 8/8 before render (R3, R7).
- **Visual system (R1, R2, R6):** dusk palette — deep blue gradient sky,
  sunset-orange accent, cream captions. Scene list:
  - hook: sky FULL of birds + stickman tiny below (premise at t=0)
  - s1: murmuration morphing shapes (the wonder shot — dense bird field)
  - s2: two-bird collision diagram, veer-right + altitude split (the belief fix)
  - s3: the rule stamps — fast, 1.0–1.2s cuts (R8 rhythm)
  - s4: ONE bird with seven glowing links — the hero diagram, longest scene (R5 motionmaxxing: emphasis spent)
  - s5: ripple wave through the flock (the payoff)
  - s6: no towers / no radar — icon stamp cut
  - s7: stickman in traffic, bird flies past (the loop-out)
- **Sound:** airy music bed −24 LUFS-ish under VO, ducked −6dB; whoosh SFX at
  s5 ripple; riser into s4 (v3-spec #2 — the biggest $0 lever).
- **Captions:** keyword pops on "Seven", "one rule", "right" — Bricolage 800,
  amber emphasis, never mid-sentence fade (v3-spec #5).
- **Gate:** VLM pass per scene with fresh NOTES; max 2 re-renders; eye
  arbitration on every bbox flag before touching code (R4, R5).
- **Publish:** same-day, synthetic disclosure ON, loop-shaped ending.

## 5. What the synthesis kills (tonight's not-do list)

- No new script beats (frozen; writer-critic loop already passed on structure)
- No Remotion/Manim migration (R10)
- No Fish Audio block — edge-tts is the validated path; Fish returns via CI
- No character redesign — the rig stays, the world levels up (R2)
- No re-gate of scenes whose frames didn't change (L-045 acceptance rule)
