# Beautiful easing curves in After Effects — Ae Genius (Jake Bartlet) (~97.5k views per brief, 588s)
**Source: youtube.com/watch?v=6zrEKEuJGKs · 2026-11-14 · analysis-only**

## 01 Verdict
3-tier ladder: "Easy Ease = noob" → graph-editor sculpting → expression slider for curves two keys can't express. Core law: no divots/creases, front-loaded velocity, designed settle.

## 02 Hook anatomy (first 2s)
- t=0–4s: white card, Ae logo → wordmark (hook.jpg, f0.jpg); t≈4s direct intro ("teaching motion designers… a decade", paraphrase).
- t≈30s the promise: a circle "extremely smooth… you need the graph editor" (paraphrase, vtt). Names the wrong mental model, then demos the right one.

## 03 Craft notes: the easing ladder
- **Tier 1 — Easy Ease (F9)** (vtt ~1:50): "level one… total Noob" — floor, not goal.
- **Tier 2 — value curve** (~3:00): drag influence handles (Shift = symmetric); strong ease-out key 1 → ease-in key 2; red-vs-blue A/B proves shape > plugin.
- **Tier 3 — expression slider + post-expression graph** (~5:00): slider wired `value - slider`; keyframe the SLIDER; Show Post-Expression Graph sculpts curves two keys can't. Any crease = broken; back key ≈ fastest point.
- **Without expressions**: add a THIRD key, sculpt handles ("99% of the time this is how I work", paraphrase).
- **Entrance character**: high velocity → symmetric ease into rest. Ladder applies to rotation/scale/pendulum.

## 04 Pacing + cuts
- **6 changes** → 7 shots, mean 84.0s (screencast): 180s intro, 72s Tier-2, 117s Tier-3, 185s pendulum/outro.
- ≈**218 WPM** (2,136 words / 9.8 min); demos hold 2–4s per A/B comparison.

## 05 What maps to our pipeline (engine/core.js, engine/rig.js)
Our grammar (cubic eases + `V2.settle`, `engine/core.js:25–43`) needs three imports:
1. **`V2.backOut(t, s=1.70158)`** — overshoot ease-out for `stamp` slams + count-up pops (~1.1× land, settle).
2. **`V2.easeOutQuint(t)`** — long-tail settle (his post-expression "ease into resting spot"); replace cubic `easeOut` on hero landings/verdict cards.
3. **`V2.kf3(A,B,C)`** — 3-key middle-sculpt convenience in `engine/rig.js`, mirroring his "add a third keyframe" workflow.
- **C5 in curve space**: no-divots = in-between smoothness, not just cut ease. Lint: flag d²v spikes as `edit_flow` fails.
- **sac_in / sac settle** (user terms, no repo symbol): `sac_in` = `backOut(s≈1.2)` ≤150ms, ≥8% overshoot; `sac settle` = `easeOutQuint` final 60%. Pairs with finish_v3 `thump` (VL-12).
- **A/B habit**: his red/green/blue circles → render two curve variants of a stamp beat, pick by gate score.

## 06 Judge anchor?
No for frames (screencast). YES as craft anchor for tween review; cite in C5 discussions.

## Compliance: paraphrased only, no quotes >50 words. Views ~97.5k per brief. Detector "shots" are screencast segments. sac_in/sac settle semantics inferred. Curve params are ours, not his.
