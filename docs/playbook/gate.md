# Playbook — Gates (stage 6 of 7): vlm_gate (intent) then ultracritic (the bar)

> Purpose: verify scenes match intent (vlm_gate), then decide PUBLISH vs NO-POST
> (ultracritic — the publish authority, rule G1).
> Inputs: `gate/*.png` (keyframes), `gate/notes.json` (scene intent), the
> rendered `<slug>.mp4` (for the video pass), `vo/master.m4a` (for A5).
> Outputs: `gate/report.json` (vlm_gate), `gate/ultracritic_r<N>.json` (the
> verdict trail — COMMIT THESE; they are the carry evidence).

## Commands

```bash
# 1. Intent gate, scene by scene (fix loop, ≤2 re-renders per scene — rule R2):
python3 tools/vlm_gate.py <slug>                 # all frames
python3 tools/vlm_gate.py <slug> --scene s4 --round 2   # one scene after a fix

# 2. THE bar (mechanical A1–A5 + VLM frame pass 5 dims + glm-4.6v video pass 3 dims):
python3 tools/ultracritic.py <slug> --round 1
# iterate: apply directives → re-render changed scenes → --round N+1 (cap 3/night)
```

## What each check is

**vlm_gate** (intent): per-frame checklist against the scene's narration +
visual spec + notes.json — text collision, anchoring, drift, asset match,
readability, clutter, light. It inspects; it never redesigns. Spatial claims get
pixel-probe arbitration before code changes (rule G3).

**ultracritic** (the bar — boss directive 2026-11-08):
- Mechanical (instant, no VLM): A1 caption budget ≤5 keywords · A2 pacing mean
  ≤3.2s/max ≤4.2s · A3 orientation · A4 spine · A5 bed audibility 6–22 dB under VO.
- Frame pass (still dims): hook_impact, text_discipline, visual_hierarchy,
  contrast_legibility, production_polish — anchor-laddered (7 = solid/clean).
- Video pass (temporal dims, REQUIRED): pacing_rhythm, character_life,
  edit_flow — glm-4.6v on the mp4 via SDK `video_url` (CLI vision rejects mp4).
- **Publish = grand mean ≥7.5 AND every dim ≥7.0 AND no frame <6.0 AND video
  pass present.** Weights: video pass counts as 3 frames in the grand mean.
- Control-tested on known-bad #0003 (measures 5.20, catches every known failure
  — rule G5). Threshold history documented per L-078/G6.

## Known failure modes

| Symptom | Cause | Fix |
|---|---|---|
| gate flags things that are by-design | notes missing/stale (L-070) | write `gate/notes.json` BEFORE first render; per-short, never global |
| gate "caption overlaps legs" but looks fine | caption words same color as hero (L-064) | pixel-probe the bbox before touching code |
| every frame scores 4–6 | rubric compression (dead-end D9) — check the anchor ladder is in the prompt | anchors live in `tools/ultracritic.py` RUBRIC — don't strip them |
| video pass "VLM FAILED" | CLI vision endpoint used for mp4 | only the SDK `video_url` path works (ultracritic handles it; node + ultracritic_video.mjs) |
| JSON parse fail on VLM output | model wrapped JSON in prose | extract_json regex (already fixed); retry ×3 built in |
| pacing scored low but video feels fine | judged from stills (dead-end D8) | only the video pass scores temporal dims — never re-enable stills for them |
| frame <6.0 floor breach | one broken frame (hook, s5…) | fix that frame's specific directives; it cannot hide in the mean |

## Acceptance check (this stage IS the acceptance check)

- `ultracritic_r<N>.json` says `PUBLISH_APPROVED` → proceed to stage 7.
- `BELOW_BAR_NO_POST` after 3 rounds → STOP. Commit the report, write the
  carry note (3 named directives) into the ledger line, and hand the debt to
  the next session (rule 7 of the standing rules).

## When no model judge is available (rule G10, day-019)

`ultracritic.py` printing "VLM FAILED (3 attempts)" on every frame is a backend failure (credits, 402),
not a verdict and not a creative round. Do this instead, in order, and commit the outputs:

```bash
python3 tools/script_linter.py content/<slug>/script.json --duration-s <VO seconds>   # PASS
python3 tools/vo_pipeline.py <slug> --verify-only          # offline whisper.cpp, 0 FAIL (L-118)
python3 tools/contact_sheet.py <slug> /tmp/s.jpg --scenes --errors   # read it; fix; repeat
python3 tools/render_short.py <slug> --full --workers 4 && python3 tools/finish_v3.py <slug>
python3 tools/watch_video.py <slug>                        # READ THE SHEETS IN ORDER; note dead seconds
```

Write `gate/agent_review_r<N>.md` (what was measured, what you saw, what you did not fix) and
`gate/watch_r<N>.md`. Label both as agent-judged. Reference numbers so far (motion_probe, 1 s bins):
#0005 median 0.0013 / 18 dead of 36 · #0006 v3 median 0.0051 / 4 dead of 39 · probe target ≥ 0.01.
A funded judge later runs the missing round on the live cut and files the number next to these.
