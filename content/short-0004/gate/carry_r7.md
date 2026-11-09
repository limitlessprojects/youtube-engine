# carry_r7.md — #0004 debt report + 3 directives (recreated day-012)

> NOTE: this file was referenced by commit f32dc9b (day-011) and
> `docs/lessons.md` L117 but never actually committed — the commit message
> overclaimed. Recreated day-012 from the r7 gate artifacts. Lesson filed:
> a report named in a commit message must exist IN that commit (L-083).

## State after round 7 (evidence: gate/ultracritic_r7.json)

| round | grand mean | verdict |
|---|---|---|
| r4 | 6.92 | NO POST (carried) |
| r5 | 6.98 | NO POST |
| r6 | 7.11 | NO POST |
| r7 | 7.14 (frame-only; video pass 429-blocked) | NO POST — carried |

- text_discipline 8.0 ✓ · contrast_legibility 7.57 ✓
- **hook_impact 6.86 ✗** — rubric defect, not craft: it was averaged across
  ALL frames; diagram cards structurally cannot "stop a thumb-scroll".
  Boss directive 2026-11-09: score hook_impact on frame 0 ONLY.
- **visual_hierarchy 6.43 ✗, flat 6.1–6.4 across all 7 rounds** — polish
  rounds can't move it → structural ceiling. Frames below floor in r7:
  hook_u50 6.6 (hierarchy 6, polish 6), s4_u50 6.6 (hook 6 / hierarchy 6 /
  polish 6), s5_u50 7.0 (hierarchy 6).

## Directives (boss, 2026-11-09)

- **D1 — one dominant element in s4, s6, s8.** Restructure those scenes so
  a single element owns the frame (kill competing props/dead zones). r7
  evidence: s4_u50 hierarchy 6; hierarchy flat ≤6.4 for 7 rounds.
- **D2 — probe-test hook variants.** Hook frame is the weakest measured
  frame (6.6). Render ≥2 hook-frame variants, pixel-probe + VLM-probe them,
  pick the strongest as frame 0 before any full re-render.
- **D3 — video pass backoff, then ONE full round → publish-or-redesign.**
  The video pass died on 429s (r7). Back off, re-run; then exactly one full
  ultracritic round on the restructured cut. Below bar after that round →
  REDESIGN the scenes structurally (not another polish lap). Decision is
  autonomous (boss: sign-off removed, 2026-11-09).

## Boundaries

- Thresholds unchanged (7.5 mean / 7.0 dim / 6.0 floor — day-010 calibration).
- Published videos untouched; gate behavior changes ONLY the boss-authorized
  rubric edit (hook frame-0) — no threshold drift.
