# STYLE BIBLE — locked 2026-11-13 (boss directive, rules C13–C17, G9)

> This file is the single source of visual truth. Every asset is generated or
> CHECKED against it before render (C13). The engine tokens in
> `engine/core.js` (`V2.P`, gradients, rims, vignette) implement this bible;
> if engine and bible disagree, fix the engine, never "just this once" the
> scene. Changing the bible requires a boss directive.

## 1. Colour palette (8 slots, no drift — C12/C13)

| Slot | Token (`V2.P`) | Hex | Use |
|---|---|---|---|
| Deep space | `bgDeep` | `#070A18` | deepest background, night voids |
| Raised ground | `bgRaised` | `#0E1430` | panels, decks, mid-ground masses |
| Nebula purple | `nebPurple` / `nebPurple2` | `#5B3A9E` / `#3A2470` | sky gradients, dusk worlds |
| Amber (PRIMARY accent) | `amber` / `orange` | `#FFB054` / `#FF8A3D` | heroes, glow, ONE accent per scene |
| Teal (SECONDARY accent) | `teal` | `#2FD4C5` | shoes, cool rims, water/energy |
| Signal blue | `blue` | `#4AA8FF` | cool light, data, cold objects |
| Cream (skin/light) | `cream` | `#F6EFE3` | faces, limbs, light shafts, titles |
| Ink | `ink` | `#141222` | outlines, silhouettes, shadows |

Scene rule: background = one of {deep space, raised, nebula gradient}; ONE
warm accent (amber family) OR one cool accent (teal/blue) per scene — never
both at equal weight. Magenta `#C2447E` and the earth/rock families
(`earthSea`, `crust`, `rock`) are WORLD tokens for terrain scenes (e.g.
Krakatoa), not decorations.

## 2. Gradient & glow recipe (implemented as `vGlow*`, `vBeam`, `vCone`)

- **Glow:** radial, 3 stops — core at full opacity, mid at 0.30–0.35 alpha at
  30%, zero at 100%. Warm = `#FFD7A0→#FFB054→0`; cool = `#9FC0FF→#4AA8FF→0`;
  teal = `#7DF0E4→#2FD4C5→0`; danger red `#FF5A4A` reserved for heat/lava.
- **Beam/cone:** linear, bright base fading to 0, never a hard-edged polygon.
- **Depth grade:** every scene gets a visible light source + vignette
  (`vVig`: 0 → 0.82 alpha `#05050A` at edges) + horizon band. A flat void
  background is a gate fail (checklist 7).
- **Rim light:** every hero/asset gets a rim — warm `vRimR/L` (#FFB15A) on
  warm scenes, teal `vRimTeal*` on cool scenes, 4px on the light side.

## 3. Outline rules

- Characters and hero props: 3–4px `ink` `#141222` outline, rounded joins.
- Background masses (hills, panels, clouds): NO outline — separate them by
  value contrast and gradient, not strokes (outline-everything is the
  "colouring book" read).
- Text: cream or amber fill, `ink` or dark-navy stroke only when it sits on a
  busy zone; captions live in the bottom-20% band (C10).
- Subjects are the opposite value of their ground (C2) — checked before
  render, not after.

## 4. Reference frames (calibration set — check every new asset against these)

1. `content/short-0002/render/probe_2_72.png` — #0002 hook: title hierarchy,
   dusk world, rim-lit hero, flock density. The current gold standard (7.5/10).
2. `content/short-0004/gate/` r8 hook frame — calm-water hero composition.
3. #0005 Krakatoa hook (to be rendered canvas-first) — will join this list
   only if it beats the calibration set (gate ≥7.5 hook).
4–5. OPEN SLOTS: reserved for the first two style-bible-compliant layered
   renders; filled the moment they clear the gate.

## 5. Asset construction (C14 — layered, never flat)

- Characters, key objects, backgrounds are SEPARATE transparent layers
  (image-model asset + background removal), composed in the scene, so
  parallax can move them independently.
- Every asset: bold readable silhouette, rim light, soft gradient shading,
  1–3 tiny detail props (scratches, rivets, wear) — detail density is a gate
  dimension (G9), primitives are a gate FAIL ("basic shapes" read).
- Free-material policy (boss 2026-11-12): public-domain/CC0 sources
  (NASA, USGS, Wikimedia PD) allowed with license noted in
  `content/<slug>/assets/NOTICE.md`; generated assets preferred for the
  character.

## 6. Motion design (C15 — the professional feel lives here)

- Parallax: ≥2 depth planes per scene, background moves at ~0.3× hero speed.
- Everything eases (no linear tweens, no snap-cuts — C5); squash & stretch on
  impacts and jumps; idle breathing/blink always on (C4).
- Secondary motion: hair, cloth, smoke, particles on relevant props.
- Camera: slow pushes (scale 1.0→1.06 over a scene) on held beats; subtle
  grain + vignette over the final grade (finish_v3).

## 7. Accuracy pass (C17 — before animating a scene)

1. List EVERY object the scene will show.
2. Check each against real references for shape, scale, colour (e.g.
   Krakatoa: caldera shape, ship scale vs wave height).
3. Add ONE detailed "wow" element per scene (a specific, research-backed
   detail the viewer didn't expect).
4. The object list goes in `gate/notes.json` so the gate checks the scene
   against intent (G2).

## 8. Hero shots only for image-to-video (C16)

Procedural animation is the default. Image-to-video (free-GPU route,
`research/free-gpu-video.md`) is reserved for hero shots — explosions,
fluids, space scale pulls — FED our approved keyframes, palette-graded back
into the bible before compositing.
