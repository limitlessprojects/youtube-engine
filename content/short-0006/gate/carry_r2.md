# carry_r2 — #0006 final decision, day-018 09:45 EAT session (2026-11-15)

## The four-round ladder (bar 7.5 combined, no dim <7, no frame <6.0)

| round | canvas | judge | FRAME GRAND | VIDEO (pacing/life/edit) | COMBINED | verdict |
|---|---|---|---|---|---|---|
| r1 | v1 world | glm-4.6v (studio) | 6.97 | 6.0 / 5.0 / 6.0 | 6.72 | BELOW_BAR_NO_POST |
| r2 | v2 redesign | glm-4.6v (studio) | 6.90 | 5.0 / 5.0 / 6.0 | 6.61 | BELOW_BAR_NO_POST |
| r3 | v2 + D1/D2/D3 fix set | glm-5.3-flash (see L-113) | 7.00 | 7.0 / 8.0 / 7.0 | **7.06** | BELOW_BAR_NO_POST |
| r4 | v2 + D-set + r3 directives | glm-5.3-flash | 7.04 | 7.0 / 8.0 / 7.0 | **7.10** | BELOW_BAR_NO_POST |

**DECISION: CARRIED UNPOSTED** per plan rule 7. The budgeted two-round decision
(5a36f7a: "r3/r4 two-round decision") is spent. r3→r4 moved +0.04 = L-101 noise;
the anti-chasing law forbids a fifth lap. No dim reached 7 in any round.

## What this session added on top of the D-fix set (a71a6ef)

All verified by eye at thumbnail scale BEFORE the gate rounds (L-112 protocol):

1. **D2 residuals fixed (the D-fix set missed three real defects):**
   - s6 SEAM label: the hero is drawn AFTER the label plate, so the hood
     occluded "SE" — moved the label to x-center 950, clear of head + glow chord.
   - s10/s11 title: the "warm glow plate" (V2.glow is screen-blend LIGHT) washed
     the cream title; replaced with a 0.90 ink plate (190/1200/700/470) + tamed
     the 0.42 band glow to 0.18.
   - **kineticTitle pop timing** (the big one): 0.22s stagger + 0.4s fade meant
     "SEE." reached full opacity only ~0.9s after t0 — at the old timing the
     closing word of the short NEVER showed solid before the video ended.
     Now 0.12 / 0.3 → full title solid by ~0.55s. Proven: text_discipline
     8.7 (r3) / 8.8 (r4) = highest of any round.
2. **r3 video-pass directives applied (s8/s9 dead-air):** ~2s-cadence
   stitch-tension pulse on the amber thread (was a 10s sine = frozen read),
   springy overshoot/settle on the s8 seal-wave land, breathing micro-glow
   near the s9 hero. Video pass held 7/8/7 in r4 (did not regress).
3. **r3 vh nudge (partial):** s0 loop ensemble enlarged (stroke 16, knots r25)
   + one row-level bloom; s6 clean-side under-seam arc made the dominant
   element (12w, 0.55, 190-glow). visual_hierarchy moved 5.5 → 5.8 only.

## Why it still floors — the third confirmation of the template ceiling

- frame:visual_hierarchy across ALL rounds and BOTH judges: 5.5–5.9. The r3
  per-frame table scores vh ≈ 5 on 13/13 frames — the judge is grading the
  world template (three stacked bands of similar weight, no single subject
  ≥50% in most scenes), exactly the L-085 (#0004) + L-112 (#0006 r1/r2)
  pattern. Scene-level nudges cannot fix a world-level composition law.
- r4 hook_impact 5.0 vs r3 hook_impact 7.2 — the hook scene code was UNTOUCHED
  between rounds: same frame, same model (glm-5.3-flash), ±2.2 per-frame
  variance. Confirms L-101/L-103 at the new judge; combined r3→r4 (+0.04) is
  noise, not signal.

## Liabilities CLOSED this session

- **ASR union-verify: GREEN** (12/12, 0 fails, VO_GAP_S=0.25 timeline 37.79s
  matches the build; the gap-0.45 first run was a false alarm — mp3s identical,
  total_vo_s 35.04 exact). Line 10 WARN 0.29 is a hyphen tokenizer artifact
  ("best-stitched" → "best stitched", semantically identical — see L-115).
- **VLM credits: LIVE** — the Z.ai endpoint now answers (probe + 2 full gate
  rounds + video passes all succeeded; boss top-up or funded flash tier).
  Judge identity note: requesting glm-4.6v now returns model glm-5.3-flash —
  the service aliases old vision names (L-113). r3/r4 are an internally
  consistent pair on the new judge; never compare them to r1/r2 absolute
  numbers, only to the bar.
- **vo_pipeline ASR_SLEEP_S** shipped (per-line sleep parameterizable; the
  2s default trips the per-minute throttle on back-to-back verify runs).
- **fetch_instances.py** fixed for scalar registry values (upstream shape change).

## Open liabilities for the next session

- views_tracker 404'd 3/3 on 2026-11-15 (L-031 bot-wall class) — retry next
  session; latest row remains 2026-11-14 (#0005 631, #0004 1153, #0003 1142,
  #0001 201).
- Fish VO A/B — moot for #0006 (carried); revisit only if a future cut wants it.
- Hook probe (L-087 A/B) — moot for #0006; the hook is now a #0007-world item.

## Directive for #0007 (the world, not the scenes)

The next short's world must be designed ONE-DOMINANT from the first sketch:
one subject ≥50% width/height in every scene, one focal order, bands that
SUBORDINATE to the subject (texture, not zones). Run the L-112 checklist +
this dominance law BEFORE the first gate round. #0006's master (39.13s,
−15.16 LUFS, 12.06 MB, upload/short-0006.mp4) is publish-ready on every axis
except the bar — if a future world solves vh, re-gating this cut is cheap
(frames re-render in ~10 min, judge probe first).
