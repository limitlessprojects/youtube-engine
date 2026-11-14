# How to Do Visual Comedy — Every Frame a Painting (Tony Zhou) (~11.4M views per brief, 479s)
**Source: youtube.com/watch?v=3FOzD4Sfgag · 2026-11-14 · analysis-only · no captions**

## 01 Verdict
The joke lands ON THE CUT: setup held to arm expectation, payoff in the shortest insert, one beat too long. Transfers to number landings, reaction faces, count-up pops.

## 02 Hook anatomy (first 2s)
- t=0.4s: cold open on a startled close-up (hook.jpg). Frame 1 IS a punchline face: "what did he see?"
- Anti-orient hook on facial information gap. Borrow the face, not the opacity — S3 still governs.

## 03 Craft notes: cut grammar
- **Impact frame first**: hook.jpg, f0.jpg (startled young man) — reaction close-ups before context.
- **Escalation wide**: f2.jpg — burning house, swarming crowd: reaction-at-scale; cut IN, never out.
- **Sight-gag tableau**: f4.jpg — overhead, victim by a yellow GLUE gun: eye reads victim → weapon → wrong weapon in one saccade.
- **Deadpan payoff**: f6.jpg — glasses woman, dark surround: the laugh lives in the held beat AFTER the cut.
- **Rule**: long master (arm) → short insert (payoff) → reaction held one beat too long → cut BEFORE the smile peaks.

## 04 Pacing + cuts
- **143 cuts / 144 shots**, mean 3.33s, min 0.04s (flash), max 34.1s (master).
- Densest: t≈206–223s (~1.2s/shot, snap-zoom montage); t≈336–348s (~1s). Sparsest: t≈79–112s (10–20s holds).
- 3.33s mean ≈ 2.6× the "editor" episode; ~0.5s insert floor except 0.04–0.27s flash gags.
- No vtt → cadence UNKNOWN.

## 05 What maps to our pipeline
- **Big-number land (s3)**: setup→insert→reaction — (1) count-up lands fast (backOut, VL-11), (2) `stamp` hit (VL-12), (3) hold the RESULT one beat too long before the verdict cut — we cut ON the land and lose the laugh. Extend post-payoff hold ≥1.5× settle (L-097 release ≥ build).
- **Reaction face beats**: `engine/rig.js` supports eye/brow keys — add `deadpanHold`: 8–12 still frames post-gag (C4 exception, max 1/Short).
- **Count-up pops**: accelerate INTO landing (velocity ease-in, inverse of our easeOut), then stamp-slam.
- **Cut on the gag**: cut ON the gesture apex (pose key) — VL-13a's "eyes-change frame" for limbs.
- **C5**: flash inserts legal only as justified laugh devices with written reason; default stays eased. Linter should accept a `comedy triplet` annotation so the fast cluster doesn't trip beat advisories.
- **Not adoptable**: snap-zoom spam; needle-drop sync (finish_v3's synth pad is our ceiling); live-action budget.

## 06 Judge anchor?
No — process anchor for comedy beats; justifies one deadpan hold per Short.

## Compliance: no caption track; frames + detector only. Views ~11.4M per brief. Detector stats are lower bounds; timing values are our measurements, not episode numbers. Film excerpts not redistributed.
