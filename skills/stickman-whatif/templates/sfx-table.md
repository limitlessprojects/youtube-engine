# SFX table — per-short sound design (`sfx` in script.json)

All SFX are numpy-synthesized by `tools/finish_v3.py` (rule A4: license-free,
$0). Place every hit in the pause AFTER its word (rule A3 — a pop on a word
covers the word). `at` values are final-timeline seconds (post-VO-sync).

| Kind | Sound | Duration | Params | Use it for |
|---|---|---|---|---|
| `riser` | noise + rising sine sweep | 1.3s | — | the 1–2s BEFORE an insight/payoff beat |
| `whoosh` | bandpass-swept noise burst | 0.7s | `seed`, `f_lo` (default 900), `f_hi` (default 3800) | motion payoffs: waves, flybys, sweeps |
| `thump` | soft 68 Hz stamp impact + click | 0.28s | `seed` | card/stamp landings (word-timed) |
| `blip` | tiny 2.1 kHz tick | 0.09s | — | near-misses, sparks, small UI beats |

Placement recipe (from the #0002–#0004 measured tables):

1. One `riser` ending at the insight scene's start (at = scene_start − 1.3).
2. One `whoosh` at each big motion payoff (wavefront, flyby) — start ~0.85s in.
3. `thump` at every stamp card landing (word-timed: when the card text pops).
4. `blip` sparingly for near-miss/small beats.
5. Gain 0.6–1.0; the bed handles the rest.

Bed (automatic, not in the table): warm Aadd9 pad, 0.16 peak, ducked −9 dB
under VO spans with 150 ms ramps, fades in 0.8s / out 1.2s. Verified by
ultracritic A5 (non-VO RMS 6–22 dB under VO) — never trust the code comments
over the measurement (L-074).

Example rows:

```json
"sfx": [
  {"at": 0.95, "kind": "blip", "gain": 0.6},
  {"at": 2.35, "kind": "thump", "seed": 21, "gain": 0.7},
  {"at": 5.50, "kind": "riser", "gain": 0.6},
  {"at": 12.10, "kind": "whoosh", "seed": 3, "f_lo": 900, "f_hi": 3800, "gain": 0.9}
]
```
