# Short #0001 — "What if a black hole appeared in your pocket?"

- **Format:** Short (30–60s) · sub-angle 1 (absurd physics & survival)
- **Status:** WRITER DRAFT v1 → linter → critic (round 1)
- **Born from:** today's blueprint `research/blueprints/8nHBGFKLHZQ.md` (Kurzgesagt
  calibration: 192 WPM ceiling, 62-word/15s hooks, ~12 cuts/min proxy) + the
  7-beat What-If formula in `docs/content-strategy.md`.

## VO (unique words: 105 → ≈ 40.4s at the measured 2.6 words/sec Fish Audio rate)

| # | t_start | VO | Pose | Prop | BG |
|---|---------|----|------|------|----|
| hook | 0.0 | A black hole just appeared in your pocket. | shocked | tiny_swirl | street |
| 1 | 2.8 | Coin-sized. Harmless-looking. Completely lying. | curious | coin | closeup |
| 2 | 5.5 | That little circle weighs about as much as the whole Earth. | pointing | coin_vs_earth | space |
| 3 | 10.5 | It falls through your hand, through the floor, through the sidewalk. | falling | floor_layers | cross_section |
| 4 | 15.0 | Matter is mostly empty space. To this thing, solid rock is a rumor. | amazed | atom | cross_section |
| 5 | 20.0 | It loops the planet through the core, and every pass cracks the crust. | shocked | earth_orbit_line | globe |
| 6 | 24.5 | And no, it doesn't swallow the Earth in one bite. Real black holes eat slowly: atom by atom, patient, invisible. | calm | atom_trickle | dark |
| 7 | 32.0 | But patience wins. One day the ground gives up, and the planet folds itself into a marble. | shocked | earth_marble | space |
| 8 | 38.5 | Check your pocket. The universe already did. | smug | empty_pocket | street |

**Loop check:** line 8 ("Check your pocket…") flows directly into the hook
("A black hole just appeared in your pocket.") → infinite-replay shape. ✓

## The turn (credibility anchor, beat 5 of the formula)

People expect instant swallowing. The checked counter-intuitive fact: micro
black holes accrete absurdly slowly — the capture cross-section is tiny — so
the hole wouldn't devour Earth in one bite; it would oscillate through the
planet, quake the crust, and eat atom by atom. Grounded in the CERN LSAG
safety-review physics and the Schwarzschild relation (coin-radius hole ≈ one
Earth mass; Earth's own event horizon ≈ 8.9 mm).

## Pipeline status

- [x] writer draft (this file + `script.json`, contract per `prompts/scriptwriter_system.md`)
- [x] `tools/script_linter.py` gate
- [x] critic verdict (`critique.json`, per `prompts/critic_system.md`)
- [ ] TTS (fish_tts.py) + ASR verify
- [ ] stickman render + VLM frame inspection
- [ ] upload (youtube_upload.py, "Altered or Synthetic Content: YES")
