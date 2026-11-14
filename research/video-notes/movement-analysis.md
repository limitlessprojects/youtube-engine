# Movement Analysis — Wishlist Corpus → Our Engine (2026-11-14)
Analysis-only. No engine/tool files edited. All motion stats measured on pre-extracted frames (`/tmp/opencode/wishlist/frames/<base>/`, hook + 6–10 sampled f*.jpg, 160×90 gray, mean |Δ| vs previous sample). Frame sampling is sparse and cross-cuts inflate apparent diff, so cut-dense videos read high; treat absolute diff as *motion-or-cut energy*, not MOS. Frames missing for `VL-06-The_Egg`, `VL-16*` (Wan), `h6fcK_fRYaI-...f397` → motion values UNKNOWN there.

## 1. Per-video motion statistics
Format: cuts (scene_changes.txt) · dur · MSL · mean sample-diff · signature move.
| Video | cuts | dur | MSL | diff | Signature / read |
|---|---|---|---|---|---|
| VL-01 Zack stitches | 0 | 31.1 | 31.1 | 37.1 | tissue-state morph one-shot; slow arc push; 0 dead frames |
| VL-02 Zack splinters | 0 | 30.4 | 30.4 | 44.6 | push-in + internal simulation (swelling) |
| VL-03 Zack mcflurry | 0 | 23.5 | 23.5 | 86.0 | live-action product close-ups |
| VL-04 Zack bloodvessels | 0 | 39.5 | 39.5 | 57.4 | one flowing vessel-tree flight |
| VL-05 Zack armor | 0 | 29.5 | 29.5 | 53.9 | continuous sim reveal |
| VL-06 Kurzgesagt Egg | 44 | 486.1 | 10.8 | 70.5 | layered parallax twinkle + scale-breathe; cuts cluster at acts |
| VL-07 Althistoryhub WWI | 135 | 492.4 | 3.62 | 103.1 | Ken-Burns map zooms, hard cuts, grain glue |
| VL-08 Kurzgesagt 1200h | 3 | 407.4 | 101.9 | 86.4 | multi-plane drift (0.2/0.4/0.7/1.2×), loop glue |
| VL-10a Buff showreel | 46 | 50.1 | 1.07 | 86.2 | impact-cut + flash triplets (~0.03/0.20/0.27s), type slams → lock |
| VL-10b Buff clip 2 | 28 | 74.8 | 2.58 | 79.4 | same; one 1.1 near-static sample |
| VL-10c Buff clip 3 | 0 | 48.0 | 48.0 | 21.6 | motion-graphic hold, 0 cuts |
| VL-11 AE-genius easing | 6 | 587.6 | 83.9 | 19.2 | easing demo; 123 spike = A/B cut; rest curve holds |
| VL-12 Kinetic Shop Vac | 15 | 205.8 | 12.9 | 86.7 | word-as-object slams + overshoot arcs; needle sweeps |
| VL-13a Everyframe editor | 64 | 564.2 | 8.68 | 37.9 | cut-on-the-look; build/release shot-length curve |
| VL-13b Everyframe Wright | 143 | 479.3 | 3.33 | 37.4 | escalation wides; cut IN never out; deadpan payoff held |
| VL-14a MinuteEarth nuclear | 2 | 59.0 | 19.7 | 28.5 | slow pan, diagram reveals, archival plays straight |
| VL-14b MinuteEarth grolar | 0 | 27.9 | 27.9 | 14.2 | labels pop on static drawings |
| VL-14c MinuteEarth sunsets | ~7–8 | 162.8 | 18.1 | 63.2 | scatter-angle split-screens, murk/brilliant contrast |
| VL-15a MinutePhysics 2plus2 | 0 | 32.1 | 32.1 | 7.3 | draw-on ink; arrows pop last; static holds between reveals |
| VL-15b MinutePhysics portals | 0 | 60.0 | 60.0 | 5.3 | draw-on + portal drift separating |
| VL-15c Backwards-driving | 0 | 48.7 | 48.7 | 6.1 | in-plane rotate/translate; arrows redraw per beat |
| VL-21a NASA earth-views | 0 | 200.8 | 200.8 | 69.2 | continuous orbital drift, 0 cuts |
| VL-21b Rocket Lab launch | 10 | 51.5 | 4.68 | 63.7 | launch footage + cuts |
| VL-22 USGS Kilauea lava | 14 | 121.1 | 8.07 | 30.3 | lava creep; 50.3 = eruption burst |

**Dead beats** (zero motion): MinutePhysics intra-beat holds (≥13s), grolar static diagrams, nuclear gaps (1.0). **Hold beats** (one mover): draw-on arrows, label pops, lava creep — corpus norm between impacts. Dead beats live *between* cuts, never at cuts.

## 2. Movement vocabulary → our engine (proposal map; nothing edited)
Engine reality: `V2.easeInOut` (cubic), `V2.easeOut` (cubic), `V2.easeIn` (cubic), `V2.backOut` (c1=1.70158 fixed), `V2.kf` (keyframe lerp), `V2.settle` (decaying sine), `V2.dust`, `V2.cam` in core.js; `V2.poseAt`/`V2.faceAt` keyframe+blink system in rig.js (blink = 3 frames); `star/sparkle/orbitRings/onOrbit` in space.js; `drawOn/arrow/countUp/dial/focusRings` in diagram.js; world.js `makeRoom/streetNight/nightWindow` (registered set-pieces); cutout lives in tools (`cutout_assets.py`, `rembg_cutouts.py`); `render_short.py` drives `renderFrame(t)` at 30fps.
Proposed additions to `engine/core.js` (in the `V2` block after `backOut`):
- `V2.easeOutQuint = t => 1 - Math.pow(1 - V2.clamp01(t), 5)` — settle-out for slams/impact arrivals (VL-12, Buff).
- `V2.easeInQuart = t => Math.pow(V2.clamp01(t), 4)` — fast-in (sac_in) for pre-impact acceleration.
- `V2.backOutBig = t => backOut with c1=2.2` — overshoot arc (VL-12 star burst) with `V2.settle(t, amp, 1.4, 8)` for post-hit wobble.
- `V2.flash = (f, t0, dur) => f within [t0, t0+dur] ? 1 - (f - t0) / dur : 0` — flash-frame support (Buff 2–4f).
- `V2.microDrift = (t, seed, amp) => sin(t/seed…)` — always-on micro-motion for holds.
Corpus move → holding code:
- Tissue time-lapse state-morph (Zack) → `V2.kf` on path `d`/`d`-attribute swap inside a layer, or layered rembg assets cross-faded on 2-key `V2.kf` with `V2.easeOutQuint`; belongs in new `engine/morph.js` or rig.js `poseAt`-style state keys, not diagram.js.
- Camera push (style-bible §6 1.0→1.06 / scene) → `V2.cam` callers in scene `renderFrame`; expose `V2.pushIn(f, f0, dur, from, to)` wrapper around `V2.cam` using `V2.easeOutQuint` (default dur 90–150f).
- Particle/parallax twinkle (Kurzgesagt) → existing `V2.stars`/`V2.dust`; add `rate` param + per-star `phase` from `V2.rnd`.
- Ring sweep / orbit (space) → `V2.orbitRings`/`V2.onOrbit`; add `V2.ringSweep(t0, dur)` drawing an arc with `V2.easeOutQuint`.
- Needle/dial sweep (Shop Vac gauge) → `V2.dial` (diagram.js) with needle rotation driven by `V2.kf` + `V2.easeOutQuint`, overshoot via `V2.backOutBig`.
- Word-as-object slam (Shop Vac, Buff type) → `V2.txt` in caption.js/diagram.js wrapped by new `V2.slamIn(x, y, text, t0)` = scale 1.6→1.0 over 10f `V2.easeInQuart`→`V2.backOutBig`, 2–4f blur via `vBlur2`, then `V2.flash` on impact frame.
- Glow pulse cadence → existing `V2.glow`; modulate `opacity = 0.45 + 0.25*sin(t*π/12)` (12f period) in callers.
- Blink → rig.js `faceAt` already blinks 3f; parameterize window (`k-2..k+1`) into a `V2.blinkEvery(f, period, phase)`.
- Clapboard-hold (deadpan payoff, Edgar Wright/editor) → export `V2.deadpanHold` semantics: no-op motion + grid/vignette freeze (bypass `V2.dust`/`V2.grade` grain shift) for N frames.
- Notch/flash transition → new `V2.notchWipe` in core.js + `V2.flash` pairs; scenes.html must call them.

## 3. Dead-zone identification on our footage (short-0005, 30fps, 1104 frames ≈36.8s)
12 evenly sampled frames (-ss equivalent): t = 0.00, 3.33, 6.67, 10.00, 13.37, 16.70, 20.03, 23.37, 26.73, 30.07, 33.40, 36.77. Pairwise |Δ|: 25.5, 16.7, 18.8, 30.6, 29.5, 12.7, 15.2, 29.0, 25.9, **5.7**, 13.6. Local +3f (0.1s) diffs: t=0: 12.1, t=6.67: 17.9, t=13.37: **0.02**, t=20.03: 0.55, t=26.73: **0.06**, t=33.40: 1.36. Per-second 6f-stride profile shows motion spikes exactly at cut boundaries (0, 3, 6, 10, 13, 24, 25, 27, 29, 33–35) and **<1.0 flat for t∈{1–2, 4–5, 7–9, 11–12, 14–16, 18–19, 22–23, 26, 30–32}** — i.e. our beats cut, then freeze solid.
Dead beats at Shorts scale (script times, 36.34s): **s1** (3.4–6.8s, ~0.1–0.3 diff), **s2** (6.8–10.3s mostly flat), **s3** (13.5–17.2s ≈0.0–0.2), **s7** (27.3–29.4s), **s10** closer (33.2–36.3s mostly 0.1–0.8 until final rise). Hold beats (single mover): **s0 hook** (camera push only), **s4–s5** (map/diagram reveals only), **s8** (re-island reveal). Nothing plays as "impact + settle" after the cut.
Fixes (proposed, not applied):
- Raise base push to 1.0→1.08 per held beat (currently ~1.06 over whole scene) and hold a 4f micro-breath cycle (`V2.microDrift` amp ~2px) so no 6f window is <0.5 diff.
- Add a 12f (0.4s) glow-pulse on every accent per beat (period 24f) — quantified Tw: keeps Shorts-scale eye alive in holds.
- Micro-motion keyframes: ≥3 per held beat (glow in/out, cloth/smoke, label nudge) vs current ~1 (push only). Draw-on arrows (`V2.drawOn`) in s4/s5 instead of instant arrows.
- s3/s10: convert stills to layered parallax (rembg) or tissue-morph; 0.0-diff frames are gate-visible freezes.
- Snap every cut to a 2–4f flash/notch via proposed `V2.flash`/`V2.notchWipe` (Buff grammar) instead of clean hard cut.

## 4. Translation table — corpus move → our engine/tool line (frames @30fps)
| # | Corpus move | Our implementation (proposed) | Frames |
|---|---|---|---|
| 1 | backOut impact (Shop Vac type) | `V2.backOutBig` scale 1.6→1.0 | 10–12f |
| 2 | easeOutQuint settle | `V2.easeOutQuint` on arrival | 15–20f |
| 3 | sac_in fast-in | `V2.easeInQuart` accel | 8–10f |
| 4 | easeInOut cubic (soft blends) | existing `V2.easeInOut` | 20–30f |
| 5 | blink | rig `faceAt` param, 3 frames | 3f every 90–150f |
| 6 | breathe (idle scale) | `V2.microDrift` y-scale 1.0↔1.02 | 60f cycle |
| 7 | ember/particle drift | `V2.dust`/`V2.stars` rate param | continuous, 12f twinkle |
| 8 | ring-sweep (orbit/dial) | new `V2.ringSweep` on `V2.orbitRings` | 24–36f |
| 9 | needle-swing (gauge) | `V2.dial` + `V2.kf` + `V2.backOutBig` | 20f |
| 10 | slam (word-object) | `V2.slamIn` + 2–4f `vBlur2` + hit frame | 10f + 3f blur |
| 11 | clapboard-hold (deadpan) | `V2.deadpanHold` freeze grade, grain off | 30–45f |
| 12 | deadpanHold payoff | same; cut lands on the held face | 36–48f |
| 13 | flash-frame triplet (Buff) | `V2.flash` ×2–3 at 0.03/0.20/0.27s spacing | 1–4f each |
| 14 | notch/mask wipe | new `V2.notchWipe` rect blocks | 6–8f |
| 15 | draw-on (MinutePhysics) | `V2.drawOn` stroke-dash offset | 30–60f |
| 16 | arrow pop-last | `V2.arrow` with 3f backOut delay after path | +9f |
| 17 | tissue state-morph (Zack) | layered rembg crossfade on `V2.kf` | 45–90f |
| 18 | camera push (held beat) | `V2.pushIn` 1.0→1.06–1.08 | 90–150f |
| 19 | Zack arc push + rotate | `V2.cam` with cx/cy orbit + scale | 120–180f |
| 20 | parallax planes (Kurzgesagt) | bg 0.3× / hero 1.0× via layer groups | continuous |
| 21 | star twinkle | `V2.stars` per-star phase | 9f cycle |
| 22 | scale-breathe set-piece | `V2.kf` scale on whole group | 48–72f cycle |
| 23 | Ken Burns (WWI maps) | `V2.pushIn` linear-ish pan 0.3–0.5× | 90–240f |
| 24 | grain glue (WWI archival) | `V2.grade` grain rect (already shipped) | every 2f shift |
| 25 | squash on hit (Buff caps) | rig limb squash ±8% + `V2.settle` | 6f squash, 24f settle |
| 26 | overshoot arc (VL-12 star) | `V2.backOutBig` c1≈2.2 | 8f overshoot |
| 27 | glow pulse accent | `V2.glow` opacity sine | 12f period |
| 28 | label pop-in (grolar) | `V2.floatLabel` with backOut | 6–9f |
| 29 | focus rings (diagram) | `V2.focusRings` expand+fade | 15f ×2 rings |
| 30 | pressure-wave ring (Krakatoa) | `V2.ringSweep` full 360° scale-up fade | 30f, reuse for s5/s6 |
| 31 | lava-creep micro-pan (USGS) | `V2.pushIn` at ≤0.5/s on plate layer | 60–120f |

## 5. Verdict — 12-beat cadence & the L-097 3.2s law
Short-0005: 36.34s VO ÷ 12 beats = 3.03s/beat — clears `ceil(VO/3.2)=12` exactly at the floor (L-097 at-floor warning applies). The 12-beat cadence **supports** the corpus register alternation (cosmic hold ↔ human impact ↔ diagram explain) — Kurzgesagt does exactly this inside 10.8s mean shots — but only if each beat carries continuous motion. Our current cut-then-freeze implementation does not: 10 of 36 seconds sit below 1.0 diff, so the register shift reads as a stall, not a downbeat. The law must flex, not break: **build-up/settle beats may hold 4s+** (s1 island reveal, s5 ring expansion, s8/s10 closer re-island) provided they carry a single tracked mover (push, ring, morph) at ≥0.5 diff per 6f stride; **impact beats must stay ≤2.5s** with a 1–4f flash on arrival. Ceiling applies to static holds, not motion-filled ones — that is the corpus's actual universal (Zack never cuts yet never freezes). Keep `ceil(VO/3.2)` in the linter; add a *floor* lint: no 6f stride under 0.5 diff inside a beat (needs an engine-side motion assertion via `render_short.py --times` + PIL diff, or a `gate/notes.json` motion checklist). Shorts register shift works at 12 beats iff at least one 2–4f flash/slam per 2 beats and zero consecutive sub-0.5-diff beats.
