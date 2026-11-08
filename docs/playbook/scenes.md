# Playbook — Scenes & animation (stage 3 of 7)

> Purpose: author `content/<slug>/render/scenes.html` — the deterministic visual
> spec the renderer executes. This is where most of the gate score is won or lost.
> Inputs: `script.json` (frozen story + timestamps), engine modules `engine/*.js`,
> the newest exemplar `content/short-0004/render/scenes.html`.
> Outputs: `render/scenes.html` (+ `gate/notes.json` BEFORE the first render —
> rule G2), later `render/probe_*.png` / `render/frames/`.

## The engine, in one screen

| Module | Gives you |
|---|---|
| `engine/core.js` | palette `V2.P`, easing (`V2.backOut`, `V2.clamp01`), text, vignette+grain `V2.grade(t)`, `V2.veil` (LightVeil), helpers |
| `engine/rig.js` | the hero: two-segment limbs `{a,b}`, 9 expressions, looks (`kip`, `kipAmber`), `V2.joints(pose)` — **a is from straight DOWN, forearm absolute angle a2=a+b** (rule C7) |
| `engine/space.js` | space props (planets, orbits) |
| `engine/world.js` | one-point-perspective rooms `V2.makeRoom`/`V2.box`, the night-street set, light pools |
| `engine/diagram.js` | the schematic ground: `V2.schematic(t, id, …)`, draw-on paths, mono labels, count-ups |
| `engine/caption.js` | `V2.caption(text, u, emWords, opts)` — keyword pills ONLY (rule C1); fallback = first 4 words, never the sentence |

scenes.html contract: define `POSES` (no adjacent repeats, rule C4), the world
palette (per-world variant like #0004's `DAY`), `const EMPHASIS = {s0: ["kw1","kw2"], …}`
(≤5 keywords/scene), and `function renderFrame(t)` — a PURE function of t
(rule C6): read `TL` (injected timeline), compute scene + `u` progress, draw.

## Commands

```bash
# Boilerplate: copy the newest exemplar and swap content:
cp content/short-0004/render/scenes.html content/<slug>/render/scenes.html
# Write gate/notes.json FIRST (rule G2) — per-scene authoritative composition
# notes (what is by-design: fast beats, end-states, contrast choices).
# Probe single frames while authoring (no full render):
python3 tools/render_short.py <slug> --times 4.2 11.7
```

## Rules that bite here (docs/rules.md §Scenes)

C1 one text system ≤8 words · C2 subjects opposite value of ground · C3 world
before character · C4 pose variety + micro-motion · C5 cards breathe (ease-in
≥0.25 → hold ≥0.5 → ease-out) · C6 pure function of t · C8 end-states persist ·
C10 captions bottom-20%, feet anchored · C11 grade matches time-of-day ·
C12 one accent per scene.

## Known failure modes

| Symptom | Cause | Fix |
|---|---|---|
| pose reads wrong (e.g. "arms up" draws down) | rig angles: a from straight down, a2=a+b (L-071) | read `V2.joints` math; arms-up needs small \|b\| (a2≈150°) |
| diagram vanished at end of scene | animated out before scene end (L-079) | hold the end-state; gate end-state probes will catch it |
| verdict/stamp faded with its object | drawn inside the object's lifecycle | draw verdicts outside the object's group lifecycle |
| subject invisible on panel | same value as ground (L-063) | lit (cream) body on dark panel / dark silhouette on lit sky |
| "reads as night" on a day world | dusk vignette/grade reused (day-010) | light day vignette; brighten gradients two steps |
| two text blocks competing | caption pill + stamp coexist (L-076) | pill dies wherever a stamp/label exists; title IS the caption in hook/closer |
| caption touches the hero's shoes | pill band vs feet | raise hero (feet ≤ y≈1400) or move pill `opts.y` |
| snap-cut card transitions | no hold on diagram frames (boss note) | ease-in 0.25 → hold ≥0.5 → ease-out 0.25 |
| JS error at some t | non-deterministic state (Math.random) | seed everything; re-render same t must be identical |

## Acceptance check

- `--times` probes of every scene's start/mid/end look right to your eye first
  (the gate is second opinion, not first).
- `gate/notes.json` exists and describes every scene's by-design elements.
- Re-render one t twice → byte-identical frame (rule C6 spot check).
