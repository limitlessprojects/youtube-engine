# Short #0003 — "Why sunsets are orange (it's not the sun)"

- **Format:** Short (30–40s) · everyday-curiosity formula #2 (rotation: #0002 was
  everyday-curiosity #1; next in queue after this: belief-correction)
- **Status:** FACT-CHECKED DRAFT v0 (day-009 session) → VO (Fish CI vs edge-tts,
  picked by ASR WER per day-008 plan) → engine v3 render
- **Pacing target:** 170–180 WPM (MinuteEarth calibration; #0002 ran 178.8 ✓)

## Script (≈102 words → ~35s @ 176-WPM class)

| # | t | VO | Pose/visual | beat |
|---|---|---|---|---|
| hook | 0.0 | The sun doesn't turn orange. Your sky just runs out of blue. | giant half-set sun on horizon, stickman tiny on hill | premise |
| 1 | ~4.4 | Sunlight looks white — but it's carrying every color at once. | white beam fans into rainbow through air wedge | wonder |
| 2 | ~8.9 | Air is a sieve: molecules fling blue sideways about six times harder than red. | two-lane photon diagram: blue bounces hard, red drifts | domino 1 (belief fix) |
| 3 | ~14.1 | At noon, your beam crosses one patch of air. At sunset? Thirty-eight. | stamps: NOON 1× air vs SUNSET 38× air | domino 2 |
| 4 | ~19.4 | Thirty-eight times the air, and every step bleeds more blue away. What survives the whole trip is orange. | long grazing beam, blue sparks bleeding out along path, orange arrives at stickman | the turn (longest scene — emphasis spent) |
| 5 | ~25.4 | The blue that got thrown out? It never dies — it becomes the rest of your sky. | sky dome overhead glowing blue while low beam stays orange | payoff |
| 6 | ~30.3 | Same sun. Same air. Only the angle changed. | three stamps with mini icons | close |
| 7 | ~32.7 | On Mars, dust flips the trick — blue sunsets. Go watch yours tonight. | Mars panel: butterscotch sky, BLUE halo sunset → cut back to hill | loop-out |

## Fact sheet — verified 2026-11-08 (DO NOT weaken or inflate)

- **Rayleigh scattering ∝ 1/λ⁴**: Wikipedia "Rayleigh scattering" — scattering
  "inversely proportional to the fourth power of the wavelength". Blue ~450nm
  vs red ~700nm → (700/450)⁴ ≈ **5.9 ≈ "about six times"** (computed
  2026-11-08; do NOT say "ten times" — that ratio is 400 vs 700nm).
- **Air mass 1 (zenith) → ≈38 (horizon)**: Wikipedia "Air mass (astronomy)",
  citing Kasten & Young 1989 — "reaching a value of approximately 38 at the
  horizon". Phrase as "one patch of air" vs "thirty-eight times the air".
- **Mars blue sunsets**: NASA JPL, "Curiosity Rover Views Serene Sundown on
  Mars" (May 8, 2015) — fine dust forward-scatters blue light, which "stays
  closer to the direction of the sun"; daytime Martian sky is butterscotch.
  Phrase: "dust flips the trick — blue sunsets."
- **"The rest of your sky"**: same Rayleigh physics — the scattered blue IS
  the sky's blue (sky opposite the sun stays blue at sunset). Poetic but
  accurate; no new numeric claim.
- **CUT CLAIMS (do not restore)**: "the sun changes color" (false — path, not
  the sun); "10x more scattered" (wrong wavelengths pair); "clouds make
  sunsets orange" (unverified mechanism for this script — out of scope).

## Production notes (engine v3 spec applies)

- First frame = the premise at t=0: giant low sun + orange horizon + deep
  blue upper sky, stickman small on the hill (R1). NOT a caption.
- **This video's diagram IS the dusk palette** — the world is the fact.
  Deep-blue gradient up top, sunset-orange accent at the horizon, cream
  captions (one world, one light, one accent — R6).
- Sound design: warm pad bed ducked under VO, "strip" SFX along s4 path,
  soft riser into s4, low thump on the 38× stamp.
- Captions: keyword pops on "out of blue", "six times", "thirty-eight",
  "orange", "blue sunsets" — Bricolage 800, amber emphasis, no mid-sentence
  fades.
- **VO A/B (day-008 decision)**: Fish s2.1-pro-free via `vo-gen.yml` CI
  (first real run — boss confirmed daily credits alive) vs edge-tts Andrew
  +45%. Pick by ASR WER, not vibes. Fish ref voice: Energetic Male.
- Loop shape: end on the same hill/horizon composition as the hook.
