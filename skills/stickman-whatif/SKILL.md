---
name: stickman-whatif
description: Produce a gate-passing "What If" stickman explainer Short (1080x1920, 30-60s) on the youtube-engine pipeline — script, VO, scenes, audio, render, gates, publish. Use when the day's mission (docs/plan-30d.md) calls for the next short, or when iterating a carried (below-bar) short.
---

# Stickman What-If — the production skill

You are the session's producer. Follow the steps in order; do not skip gates.
Every command runs from the repo root (`youtube-engine/`). `docs/` paths are
authoritative; this file never restates a number without citing where it lives.

## 1. When to use / not use

**Use** when: the nightly mission says advance the next short; a carried short
needs another gate round; you must diagnose why a short failed the bar.

**Do not use** when: the task is competitor research (`docs/playbook/research.md`),
channel ops/publishing mechanics only (`docs/playbook/publish.md`), or a new
format decision (that's a boss/plan question — Phase B fork, `docs/plan-30d.md`).

## 2. The quality bar (what "done" means)

A short is publishable ONLY at `PUBLISH_APPROVED` from
`tools/ultracritic.py`: **grand mean ≥7.5/10, every dimension mean ≥7.0, no
single frame <6.0 on any dimension, video pass present.** The bar's calibration
evidence: `docs/parameters.md` §Gate; the law: `docs/rules.md` G1.

Anchor examples per dimension (real measured frames — full trails in
`content/short-000{3,4}/`):

| Dimension | A 4 looks like | A 7 looks like | A 9 looks like |
|---|---|---|---|
| text_discipline | #0003: full-sentence captions, up to 22 words, two competing text systems (measured 2.8) | #0004: one keyword pill ≤5 words or one kinetic title, ≤7 words/frame (measured 7.4) | one clean system, ≤6 words, perfectly timed pops (not yet achieved) |
| pacing_rhythm (video pass) | #0003: 4.22s mean static holds, 8 beats in 34s (measured 5.5) | #0004: 2.83s mean, 11 beats + sub-beat stamps (measured 8.0) | same, plus varied beat lengths inside 1.2–3.9s with motivated cuts |
| character_life (video pass) | #0003: one pointing gesture all video (measured 6.2) | #0004: 11 poses, blinks, breath bob (measured 8.0) | character reacts to each beat — anticipation, hold, overshoot |
| contrast_legibility | #0003: white beams + pale dots on dark sky, min 4 | #0004: subjects opposite value of ground (measured 7.2) | every element survives a 6-inch phone in daylight |
| hook_impact | caption-only opener, no premise visual | premise visual at t=0 (#0002 hook frame measured 7.5) | instant focal point + intrigue that stops a scroll |
| visual_hierarchy | two focal subjects fighting | one subject, guided eye path (#0004 measured 6.1 — the current drag) | one subject + depth layers, zero dead zones |
| edit_flow | snap-cut cards with no holds | cards breathe: ease-in 0.25 → hold ≥0.5 → ease-out | every cut motivated; loop-back lands |
| production_polish | floating props, missing shadows | shadows/glows/alignment clean (#0004 day-world grade) | screenshot-worthy craft details |

**No video has passed the bar yet.** #0004 (6.92) is the ceiling and the
reference exemplar; #0003 (5.20) is the measured failure case. Their scores are
the calibration tape: `examples/`.

## 3. Production procedure (exact commands, in order)

```bash
# 0. Preflight — cheap checks before any render budget (rules S7, G2, schemas):
python3 tools/preflight.py <slug>            # must exit 0

# 1. Script: draft per prompts/scriptwriter_system.md (rules 12–16 are the
#    boss-directive law), fact-checking every claim (rule S7). Then:
python3 tools/script_linter.py content/<slug>/script.json --format short   # exit 0 required
#    critic pass (prompts/critic_system.md): all dims ≥8, max N=2 revisions (rule S9).

# 2. VO (per-script rate — rule V3):
VO_RATE=+25% python3 tools/vo_pipeline.py <slug>
#    → write the printed synced starts into script.json; n_fail must be 0.

# 3. Scenes: copy the newest exemplar as boilerplate, then swap content:
cp content/short-0004/render/scenes.html content/<slug>/render/scenes.html
#    author POSES (no adjacent repeats), EMPHASIS (≤5 keywords/scene),
#    renderFrame(t) — pure function of t (rule C6).
#    WRITE gate/notes.json NOW, before any render (rule G2):
cp skills/stickman-whatif/templates/notes.template.json content/<slug>/gate/notes.json
#    probe while authoring:
python3 tools/render_short.py <slug> --times 2.0 5.5 9.0

# 4. Intent gate loop (≤2 re-renders per scene, rule R2):
python3 tools/render_short.py <slug> --keyframes
python3 tools/vlm_gate.py <slug>                    # fix → --scene <sid> --round 2
#    pixel-probe every spatial claim before code changes (rule G3).

# 5. Full render + audio (frame pass only after vlm_gate is clean):
python3 tools/render_short.py <slug> --full         # --resume if interrupted
python3 tools/finish_v3.py <slug>                   # bed 0.16/-9dB duck, −14 LUFS, pipe-encode

# 6. THE BAR:
python3 tools/ultracritic.py <slug> --round 1
#    PUBLISH_APPROVED → step 7. BELOW_BAR → apply top3_directives to the
#    failing frames, re-render those scenes, --round N+1. Cap 3 rounds/night:
#    still below → commit the report + carry note, STOP (never post below bar).

# 7. Publish + record (docs/playbook/publish.md):
python3 tools/youtube_upload.py --file content/<slug>/<slug>.mp4 --title "…" \
  --description "…" --tags "what if,stickman,science" --privacy public --token-file ~/.secrets/token.json
#    write content/<slug>/published.json; ledger line in docs/lessons.md;
#    logs/<date>.md; commit + push (rule R3).
```

## 4. Hard rules (one-liners — full text + evidence: docs/rules.md)

Script: S1 no boilerplate · S2 hook ≤3s · S3 orient first · S4 one spine ·
S5 WPM 185–215 · S6 mean ≤3.2s/max ≤4.2s/≥12 events · S7 fact_sources ·
S8 rhythm variety · S9 critic N=2 · S10 story frozen after script.
Voice: V1 measure · V2 ASR ≤0.15 WER · V3 VO_RATE per script · V4 decode-validate.
Scenes: C1 one text system ≤8 words · C2 opposite-value contrast · C3 world
before character · C4 pose variety + micro-motion · C5 cards breathe · C6 pure
function of t · C7 rig a-from-down, a2=a+b · C8 end-states persist · C9
measureText · C10 bottom-20% captions, anchored feet · C11 grade matches
time-of-day · C12 one accent.
Audio: A1 mix measured (A5) · A2 −14 LUFS · A3 SFX off-word · A4 synth-only.
Render: R1 image2pipe · R2 gate budget · R3 atomic pushes · R4 30fps/1080×1920.
Gate: G1 bar 7.5/7.0/6.0 + video pass · G2 notes before render · G3 pixel-probe
claims · G4 gate end-states · G5 control-test verifiers · G7 temporal dims on
video only. Publish: P1 disclosure automated · P2 end-to-end auth · P3 loop
ending. Dead ends: read `docs/dead-ends.md` before any experiment.

## 5. Pre-flight checklist

`tools/preflight.py <slug>` checks mechanically (exit 1 names the failure):
script.json schema (title/hook/scenes/visual/fact_sources/timeline), vo_lines.json
present, EMPHASIS ≤5 keywords per scene, gate/notes.json present and covering
every scene id, ≥10 scenes, banned-words scan, sfx table present.

Eyeball before the first `--keyframes` (no tool can check these):
- [ ] every scene's `visual` is drawable by the current engine vocabulary
- [ ] no adjacent pose repeats (rule C4) — read the POSES table
- [ ] one accent color per scene; grade matches time-of-day (C11/C12)
- [ ] hook frame = the premise VISUAL at t=0, not a caption
- [ ] every fast-beat scene is described in notes.json (the gate will otherwise
      flag by-design mid-state frames — L-065/L-070)

## 6. Troubleshooting (symptom → cause → fix → verify)

| Symptom | Likely cause | Fix | Verify |
|---|---|---|---|
| linter FAIL orientation | hook never names the topic | put the title's noun in the hook (S3) | re-run linter |
| WPM out of band after VO | text-dependent pacing | adjust `VO_RATE` ±10–20%, re-synth (V3) | `asr_report.json` + timeline.wpm_measured |
| pose reads wrong (up draws down) | rig angles (C7) | arm-up ⇒ small \|b\| so a2≈150° | `--times` probe |
| diagram/stamp gone at scene end | end-state erased (C8) | hold end-state; verdicts outside the object lifecycle | end probes `*_end.png` |
| subject invisible | value camouflage (C2) | lit body on dark ground or inverse | probe + contrast dim |
| "reads as night" on day world | wrong grade (C11) | light vignette, brighter gradients | gate notes-aware pass |
| two text blocks compete | pill + stamp coexist (C1) | kill the pill wherever a stamp exists | text_discipline dim |
| gate flags by-design elements | notes missing/stale (G2) | complete gate/notes.json, re-gate that scene | vlm_gate `--scene` |
| "caption overlaps legs" | same-color false positive | pixel-probe the bbox (G3) before code | probe PNG |
| A5 bed fail | level/duck math (A1) | 0.16 peak, −9 dB duck; measure, don't trust comments | A5 prints dB delta |
| encode OOM/kill | image2 demuxer (R1) | finish_v3 pipes already; custom encodes must pipe | master_report.json |
| VLM JSON parse fail | prose-wrapped JSON | built-in extract+retry; don't add startswith guards (D9-class) | round report parses |
| pacing scored ≤6 on video pass | static holds (S6) | add sub-beat stamps / split scenes | video-pass pacing dim |
| hook_impact low on diagram frames | poster bias on mid frames | strengthen frame 0 focal point; see parameters UNVERIFIED note | frame-0 score |

## 7. Decision log — where the WHY lives

- Numbers and their measurements: `docs/parameters.md` (every value cites source).
- Rule → evidence → enforcer table: `docs/rules.md`.
- Failure history and dead ends: `docs/dead-ends.md`, `docs/lessons.md`.
- Bar calibration + threshold changes: `docs/lessons.md` (L-078) and
  `docs/parameters.md` §Gate. Thresholds change ONLY with a ledger amendment
  (rule G6) — never silently.
- Raw daily history: `docs/_archive/lessons/` (never referenced by active docs).
- Vendor craft sources: `vendor/what-if-animation/references/` (look.md,
  traps.md), `vendor/motionmaxxing/references/` (motion, judgment).
