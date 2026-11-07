# Engine v3 — Quality Spec & 23-Day Plan (day-007 session, 2026-11-07)

> Source of truth for the quality sprint. Derived from: Short #0001 autopsy
> (195 views, VLM 3.5/10 — see L-059), competitor outlier sweep
> (`research/cache/competitor_sweep_2026-11-07.json`), 2026 TTS/framework
> research. Owner: every nightly session until v3 ships.

## Why (evidence)

- Short #0001: 195 views / 3.5 days. VLM audit: "a rough animatic, not a
  product" — zero hook in frame, visual poverty (stickman + white lines on
  flat black), dead composition, half-muted mid-sentence captions.
- MinuteEarth Shorts run 176 WPM; ours ran 154. We are too slow for the format.
- First 2–3 seconds decide retention (2025-26 retention studies).

## The 7 upgrades (ordered by impact-per-effort)

1. **First frame = the premise.** The hook's visual is on screen at 0.0s
   (pocket + black hole, birds + sky full of birds). Never open on a caption
   or talking pose. Hook line lands in ≤ 1.8s.
2. **Sound design** (biggest $0 lever): music bed from YouTube Audio Library
   or Mixkit (duck -6 dB under VO, -24 LUFS bed), 3 SFX per video (whoosh,
   impact, riser) from freesound CC0. Short #0001 had none.
3. **Color script + glow.** Dark-space radial gradient background per scene;
   luminous objects via layered gradients + shadowBlur/blur (accretion disks,
   rim light). One accent color per scene. No flat black + white lines.
4. **Cut rate 1.0–2.0s** (pose or scene change), was 3–5s. Pose change =
   squash-and-stretch + anticipation, not just translate.
5. **Caption craft.** High-contrast white, keyword pops in accent color,
   never mid-sentence fades, never muted gray words.
6. **Character identity.** Keep the stickman (brand) + accent-color scarf/
   prop, expression variety.
7. **Pacing: 170–180 WPM target** for Shorts (MinuteEarth calibration).

## VO stack (research 2026-11-07)

- Fish S2 free tier = Elo-1,125 class — fine, keep when key available (CI
  secret `FISH_AUDIO_KEY`; local key lost in recycle #4 — re-paste when handy).
- **edge-tts = keyless fallback** (Microsoft neural voices, free, pip): test
  tonight; if ASR-verifiable it becomes the default for daily Shorts.
- Kokoro-82M (Apache, CPU) + Step Audio EditX (Apache, 1,102 Elo) are the
  self-host upgrades if we outgrow both. Don't block cadence on VO swaps.

## Frameworks decision

Do NOT rebuild on Remotion/Motion Canvas mid-sprint — cadence beats tooling.
Steal their patterns (springs, sequences, interpolate) into the existing
canvas engine. Revisit after day-30 scoreboard.

## Cadence & scoreboard (day 30 = 2026-12-01)

- Daily Short from day 008 (Short #0002 script ready: fact-checked, 90 words,
  ~34s, 176-WPM-class pacing).
- Long-form 2x/week only after 10 Shorts + retention data.
- **Pre-decided fork (day 15 = Nov 21):** if best Short < 8/10 quality or
  median views < 1K → pivot WITHIN YouTube (format/topic per outlier
  formulas), not away from video.
- Day-30 goal: 10+ Shorts live, one >10K-view outlier, engine v3 at 8/10 floor.

## Outlier formulas (match formula to execution ceiling)

| Formula | Example (score) | We can execute now? |
|---|---|---|
| Belief correction | "Strings Don't Vibrate The Way You Think" (3.7x) | ✅ |
| Everyday curiosity | "Why Don't Birds Cause MORE Crashes?" (8.7x) | ✅ (Short #0002) |
| Superlatives | "The Dumbest AH Scenarios" (2.5x) | ✅ |
| Fear/wonder + topical AI | "AI Just Crossed the Terrifying Line" (7.9x) | ❌ needs 8/10 visuals first |
