# Short #0005 — "The loudest sound in history (was heard 3,000 miles away)"

- **Format:** Short (~35s) · **superlative formula #1** (rotation: #0002/#0003
  everyday-curiosity ×2, #0004 belief-correction — plan Phase A). Superlative
  hook: the record + a number too big to believe.
- **Status:** FACT-CHECKED DRAFT v1 (day-013 session, 2026-11-12). Built under
  L-073 orient / L-075 cut density / L-076 keyword captions / L-077 one spine,
  and the **canvas-first mandate (L-085)** — this short VALIDATES the #0004
  postmortem: subject owns the frame, no diagram-in-panel cards.
- **Pacing target:** 185–215 WPM on synced VO (edge-tts +25% class); 11 lines,
  mean ≤3.2s, max ≤4.2s, gap 0.25s brisk; ≥12 visual events.

## Script (122 words → 36.34s measured, day-013)

**VO status (day-013, measured — V1):** 11 lines synthed (edge-tts en-US-AndrewNeural +25%),
spans 33.84s, gap 0.25, WPM 214.5 canon (band ceiling; naive split 216.3, linter convention 201.4
PASS). ASR: every line PASSed in ≥1 of 3 runs (union, provenance in vo/asr_report.json) — the
service hard-throttled on run 3 (L-081); re-verify `--verify-only` off-peak BEFORE render.

| # | VO | Pose/visual | beat |
|---|---|---|---|
| hook | The loudest sound ever: an island that blew itself apart. | hero tiny on a shore rock, KRAKATOA ISLAND OWNS THE FRAME, blast rings + kinetic title (title IS the caption) | superlative + divergence (L-073) |
| s0 | In eighteen eighty three, Krakatoa was an island near Java. | island wide shot, "1883" stamp, Java/Sumatra silhouettes at frame edges | orient place/time |
| s1 | A hundred miles out, it rated about one hundred eighty decibels. | BAROGRAPH GAUGE OWNS FRAME — needle slams past + "180 dB" stamp | the record, scaled |
| s2 | Pain kicks in around one hundred and thirty. This was fifty past it. | GIANT EAR + red-zone arc, hero wincing small at edge | human scale |
| s3 | Forty miles out, over half a ship's crew had their eardrums burst. | SHIP SILHOUETTE OWNS FRAME + "CRACK" stamp, sailor hands to ears | evidence 1 (bodies) |
| s4 | Three thousand miles away, people blamed a nearby ship's cannons. | Rodrigues beach, hero listening, distant "BOOM" kinetic text | evidence 2 (the reach) |
| s5 | The pressure wave circled the entire planet. Three and a half times. | GLOBE OWNS FRAME — one pressure ring orbiting, "3.5×" stamp | the turn (checked fact) |
| s6 | The waves it made killed thirty six thousand people. | dark swell over a village silhouette, hero head-down | the cost |
| s7 | And the island that made the sound was gone. | island splits + sinks into the sea, stunned hero | loss |
| s8 | But Earth wasn't finished. A new island rose, the child of Krakatoa. | small sprouting cone island + "ANAK KRAKATAU" stamp (name lives on screen — ASR can't carry it), pointing hero | legacy |
| s9 | It's been growing for nearly a century — and it could do it all again. | growth rings pulse on the cone → loop mirror of hook, kinetic closer | one closer (L-077), loops to hook |

## Fact sheet — verified 2026-11-12 (DO NOT weaken or inflate)

- **Loudest sound in recorded history = Krakatoa's 27 Aug 1883 blast.**
  Wikipedia "1883 eruption of Krakatoa": heard 4,800 km (3,000 mi) away at
  Rodrigues near Mauritius, "thought to have been cannon fire from a nearby
  ship". Nautilus (Aatish Bhatia, 2014) "The Sound So Loud That It Circled
  the Earth Four Times": heard at 50+ locations spanning a 13th of the globe.
- **~180 dB at 100 miles is CALCULATED, not measured**: Wikipedia — "The
  loudness of the blast heard 160 km (100 mi) from the volcano has been
  calculated to have been 180 dBSPL". The Batavia gasworks barometer (100 mi)
  spiked >2.5 inHg ≈ 172 dB (Nautilus). Phrase: "rated about 180 decibels" —
  do NOT say "measured"; do NOT claim a bigger number.
- **Pain threshold ≈130 dB, jackhammer ≈100 dB** (Nautilus 2014). Phrase:
  "around 130" — never "exactly".
- **Eardrums**: British ship Norham Castle, 40 mi out — captain's log: "So
  violent are the explosions that the ear-drums of over half my crew have
  been shattered" (via Nautilus 2014). Phrase: "over half" — not "all".
- **Pressure wave = 7 barograph passes over 5 days = 3.5 laps of the globe**
  (Wikipedia: four traveling out to the antipode, three back). Say "three
  and a half times" — NOT four, NOT seven.
- **Official toll 36,417** (Dutch colonial estimate), mostly by the ~30 m
  tsunami that swept 165 coastal villages (Nautilus; Wikipedia). Round to
  "thirty-six thousand" in VO; never say "a hundred thousand" (that is a
  different, non-official estimate).
- **Anak Krakatau**: rose permanently above sea level 11 Aug 1930; locally
  named "child of Krakatoa" (Wikipedia "Anak Krakatau"). Still active —
  September 2026 eruption ongoing; grew ~7–9 m/yr before 2018. "Nearly a
  century" (96 yrs) is accurate. "Could do it all again" is a POSSIBILITY
  framing (it is an active stratovolcano), not a prediction.

## Production notes (day-013 — canvas-first mandate, L-085)

- **CANVAS-FIRST is the experiment this short runs.** Every scene: ONE
  dominant subject that owns the frame height (≥60% of canvas height);
  caption/stamp subordinate in the bottom band or the upper corner. NO
  panel-in-world diagram cards — that was #0004's format ceiling
  (visual_hierarchy stuck at 6.1–6.9 across 9 rounds). If a scene can't be
  drawn as "one big thing + hero", redesign the scene, don't shrink the card.
- **Hook variants: probe FIRST (L-087)** before any full render: ≥2 hook
  layouts at u50 + 1 VLM call each (hook_impact + visual_hierarchy +
  dominant_element + one_fix), pick the winner, apply craft-level one_fix.
- **Keyword captions ONLY (L-076)**: EMPHASIS table = whole caption; hook +
  closer use the kinetic title AS the caption (no band caption). Text ≤8
  words/frame incl. stamps.
- **Pose variety**: 11 distinct poses, no adjacent repeats, breath bob + blink
  micro-motion (composer adds). Expressions swap on beats.
- **Cards breathe**: ease-in 0.25s → hold ≥0.5s → ease-out 0.25s; no snap cuts
  (boss note day-010).
- **Audio**: fixed bed (L-074: 0.16 level, −9 dB ducking under VO); sfx:
  thumps on stamps/gauge slam, riser into s5 globe turn, whoosh on s7 sink,
  boom-class thump at s4 "BOOM" text (low seed), riser into closer.
- **VO**: edge-tts en-US-AndrewNeural VO_RATE +25% (the 205 WPM class) —
  measured WPM must land 185–215; if out of band bump VO_RATE ±10–20% (V3).
- **Palette**: DAWN variant of the channel world — peach-to-azure dome, calm
  sea band, the hero (navy hoodie, cream face, orange scarf) continuity.
  Blast-orange carries "the blast" accent (C12: one accent per scene).
