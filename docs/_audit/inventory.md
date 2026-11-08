# Repo Inventory — 2026-11-09 (consolidation session, Phase 0)

Read-only audit of all 220 tracked files. Verdicts: KEEP (stays as-is),
MERGE (content folds into a consolidated doc), ARCHIVE (moves to
`docs/_archive/`, never deleted, never referenced by active docs),
DELETE (provable dead weight — none found; history is preserved via _archive).

Two handoff bugs found during inventory (fix proposals in the session report):

- **BUG-1 — gate evidence is gitignored.** `.gitignore` line
  `content/*/gate/*` (only `report.json` is negated) means every
  `ultracritic_r*.json` verdict was lost in the sandbox recycle. The day-010
  carry explicitly depends on `content/short-0004/gate/ultracritic_r4.json` —
  which no longer exists anywhere. Gate round evidence must be durable.
- **BUG-2 — dead doc reference.** `engine/core.js` and
  `content/short-0001/render/scenes.html` cite `docs/visual-craft.md`; that
  file was written day-004 but never committed and is not in any git history.
  Its surviving essence: L-042 (world before character) + the palette block
  in `engine/core.js`.

## 1. Root

| Path | Purpose | Last modified | Referenced by code? | Verdict |
|---|---|---|---|---|
| `README.md` | Entry point (102 lines) | day-008 era | — | **REWRITE** (Phase 2: stale — describes research loop as "the daily loop", no mention of ultracritic gate or v3 video pipeline) |
| `bootstrap.sh` | One-command env restore (deps, submodules, POT server) | day-005 | `scripts/restore_workstation.sh` (outside repo), CI workflows | KEEP |
| `requirements.txt`, `LICENSE`, `.gitignore`, `.gitmodules` | deps/legal/ignore/submodules | — | pip / git | KEEP (.gitignore gains `!content/*/gate/ultracritic_r*.json`) |

## 2. docs/ (7 files, 670 lines)

| Path | Purpose | Referenced? | Verdict |
|---|---|---|---|
| `docs/30-day-plan.md` | Phase A-D plan + day-009/010 amendments | ledger, plan | **REWRITE** → `docs/plan-30d.md` (status now: Day 010 done, #0004 in carry) |
| `docs/architecture.md` | Multi-agent pipeline diagram + bot-wall ladder | `tools/transcribe.py`, `tools/proxy_pool.py` (comments) | MERGE → `docs/playbook/` (pipeline section) + ladder detail → `docs/playbook/research.md`; diagram shows Remotion path that was never built (actual: seek-driven SVG + Playwright + ffmpeg) |
| `docs/content-strategy.md` | Niche, formula, algorithm playbook | prompts link it | MERGE → `docs/playbook/script.md` (STALE: says 155–175 WPM / "cut every 3–5s" — contradicts enforced 185–215 / mean ≤3.2s) |
| `docs/day008-skills-lessons-synthesis.md` | R1–R10 rules from 61 lessons | historical | ARCHIVE (superseded by `docs/rules.md`; R1–R10 all carry into rules) |
| `docs/engine-v3-spec.md` | The 7 upgrades + cadence forks | ledger refs | MERGE into `docs/parameters.md` + `docs/plan-30d.md` (forks), ARCHIVE original (spec #4 "cut 1.0–2.0s" superseded by L-075 law) |
| `docs/tooling.md` | Verified repo registry (L-026 rule) | README links | MERGE with `skills/REGISTRY.md` → one `docs/registry.md` |
| `docs/youtube-oauth.md` | OAuth state, secrets map, upload path | `tools/youtube_upload.py` docstring | MERGE → `docs/playbook/publish.md` (current; upload checklist in the tool docstring is stale — API field automates disclosure) |
| *(missing)* `docs/visual-craft.md` | Craft distillate | cited by `engine/core.js`, short-0001 scenes.html | BUG-2 — never committed; essence → `docs/rules.md` (contrast law, world-before-character) |
| `docs/_audit/` | this file | session | KEEP (audit trail) |

## 3. lessons/ (12 files, 1,110 lines) — the raw ledger

| Path | Purpose | Verdict |
|---|---|---|
| `lessons/LEDGER.md` | Method + index (L-001..L-079) | MERGE → `docs/lessons.md` (deduplicated, grouped by stage); index archived |
| `lessons/day000-prior-lessons.md` | L-001..L-025 (pre-repo archive) | ARCHIVE after extraction |
| `lessons/2026-11-0*-day001..010.md` (10 files) | Daily entries, L-026..L-079 | ARCHIVE after extraction (raw history, never deleted) |

Extraction mapping (evidence chains preserved): hard rules → `docs/rules.md`;
parameters → `docs/parameters.md`; dead ends → `docs/dead-ends.md`;
narrative history stays in `_archive/`.

## 4. prompts/ (4 files, 195 lines)

| Path | Purpose | Referenced? | Verdict |
|---|---|---|---|
| `prompts/scriptwriter_system.md` | Writer contract + rules 1–16 | architecture doc | KEEP (STALE SPOT: rule 5 says 190–210, linter says 185–215 — align to linter; self-check says 3.2 w/s = edge+25% class, current) |
| `prompts/critic_system.md` | 6-dim script critic, N=2 cap | architecture doc | KEEP + FIX (STALE: pacing 155–175 contradicts linter's 185–215 short band; day-010 linter is the enforced truth) |
| `prompts/vlm_inspector.md` | Frame QC checklist | `tools/vlm_gate.py` docstring only (code embeds its own CHECKLIST) | MERGE the checklist into the skill doc; keep file as the intent-gate reference |
| `prompts/blueprint_analyst.md` | Transcript → structural blueprint | `tools/blueprint_extractor.py` docstring | KEEP (research loop) |

## 5. skills/ and vendor/ (the motion-design repos)

| Path | What it is | Role today | Verdict |
|---|---|---|---|
| `skills/REGISTRY.md` | 13-skill stack table | index | MERGE with `docs/tooling.md` → `docs/registry.md` (STALE: lists stickman-video-director as "Main render engine" — actual render path is the in-house `engine/` ported from what-if-animation's rig; vendor is now reference/port source) |
| `vendor/what-if-animation/` | 7-beat formula, look/kit/sound/traps references, Remotion studio, −14 LUFS recipe | **The** format backbone; `engine/*.js` is a port of its rig.tsx; traps.md is mined into rules | KEEP (submodule, pinned) |
| `vendor/stickman-video-director/` | Director/Autopilot skill: storyboards + Gemini-clip prompts, 6 styles | Style breadth reference; NOT the render path (its autopilot uses generation tools we don't run) | KEEP (submodule) — registry text corrected |
| `vendor/motionmaxxing/` | Taste layer: 12 craft-law references, ~4,300 measured moves (M913–M974), "never ship" list | Taste QC layer (emphasis spent, time breathes, cut on motion) | KEEP (submodule) |
| `vendor/motion-skills/` | 50-skill library (kinetic type, data-viz, explainers, WebGL, Manim) | Library to mine per format | KEEP (submodule) |
| `vendor/tool-reel-system/` | Remotion reel template from 16 top reels | Edit formula reference (caption sync, pacing math) | KEEP (submodule) |
| `vendor/Youtube_transcriber/`, `vendor/bgutil-ytdlp-pot-provider/`, `vendor/skills/` (anthropics) | research loop / POT infra / doc tooling | active support | KEEP (submodules) |

## 6. tools/ (18 files) — all have docstrings; 4 need `--help`-class fixes

| Tool | Stage | Status |
|---|---|---|
| `transcribe.py` | research | KEEP (6-path ladder) |
| `blueprint_extractor.py` | research | KEEP |
| `rss_scout.py` | research/outlier | KEEP |
| `proxy_pool.py`, `fetch_instances.py`, `probe_downloaders.py` | research infra | KEEP (radar policy) |
| `daily_loop.py` | research CI loop | KEEP |
| `script_linter.py` | script gate | KEEP (the enforced law: 185–215 band, L-073/075/077 rules) |
| `fish_tts.py` | voice | KEEP |
| `vo_pipeline.py` | voice | KEEP (edge-tts default + ASR verify) |
| `render_short.py` | render | KEEP (`--keyframes/--full/--times/--resume`) |
| `probe_frames.py` | render debug | KEEP (hardcodes short-0001 — noted for future param) |
| `vlm_gate.py` | intent gate | KEEP (embedded NOTES are #0002-era fallback; per-short `gate/notes.json` wins) |
| `ultracritic.py` + `ultracritic_video.mjs` | **THE publish bar** | KEEP (bar 7.5 / dims ≥7.0 / floor 6.0 — unchanged this session) |
| `finish_v3.py` | audio master + mux | KEEP (pipe-encode permanent, bed 0.16/-9dB duck) |
| `finish_short.py` | v1 finisher | ARCHIVE? NO — **KEEP** (no dead code deletion without proof; it's the pre-sfx fallback path, unused since day-008. Marked deprecated in its docstring instead) |
| `youtube_upload.py` | publish | KEEP + docstring fix (stale manual-disclosure checklist; API automates it) |
| `views_tracker.py` | monitoring | KEEP |
| *(new Phase 4)* `preflight.py` | meta-check | TO CREATE (runs linter + A1–A4 mechanical + file presence, zero render budget) |

## 7. engine/ (6 files) — the v2/v3 render core

| File | Purpose | Verdict |
|---|---|---|
| `core.js` | palette, easing, helpers | KEEP (dead `docs/visual-craft.md` cite → repoint to rules.md) |
| `rig.js` | two-segment limbs, 9 expressions, looks (ported from what-if-animation rig.tsx) | KEEP |
| `space.js`, `world.js`, `diagram.js`, `caption.js` | sets/world/diagrams/keyword captions | KEEP (caption.js v2.1 = L-076 fix) |

## 8. content/ (4 shorts), config/, research/, logs/, .ci-artifacts/

| Path | Purpose | Verdict |
|---|---|---|
| `content/short-0001..0004/` | per-short spec + VO + gate evidence | KEEP (exemplars: #0004 = newest under day-010 law; #0003 = the measured failure case) |
| `content/*/gate/*` | gate round evidence | BUG-1: un-ignore `ultracritic_r*.json` + `notes.json` |
| `config/channels.json`, `learning_queue.txt` | research inputs | KEEP |
| `research/blueprints/` (4), `research/cache/` | research outputs | KEEP |
| `logs/YYYY-MM-DD.md` + `views.csv` | daily execution log (auto-appended) | KEEP (runtime artifacts, not docs) |
| `.ci-artifacts/` | bot-wall ladder attempt logs | KEEP (evidence of ladder results) |

## 9. .github/workflows/

| File | Purpose | Verdict |
|---|---|---|
| `daily-loop.yml` | 5-leg matrix + merge, 20:00 UTC | KEEP |
| `vo-gen.yml` | Fish VO via CI secret | KEEP |

## Self-check (per Phase 0 instruction)

Did I read everything or only filenames? Read in full: all 12 lesson files,
all 7 docs, README, REGISTRY, all 4 prompts, 8 of 18 tools completely
(ultracritic, script_linter, render_short, finish_v3, vo_pipeline, vlm_gate,
caption.js, ultracritic_video.mjs) and the remaining 10 tools' docstrings +
call graphs (grep-verified who references whom). Vendor: what-if-animation
SKILL.md + look.md + traps.md in full; motionmaxxing SKILL.md first 50 lines +
reference list; stickman-video-director SKILL.md first 60 lines + structure;
tool-reel-system + motion-skills structure. Content: scenes.html headers of
all shorts + short-0004 EMPHASIS block + gate reports. Workflows: headers +
schedule. Everything else is binary (mp3/png) or generated (logs, blueprints)
— verified by existence and spot reads, not line-by-line.

Honest gaps (things a cold agent cannot get from this repo even after my
reading): the exact content of lost `docs/visual-craft.md` (BUG-2), the
r1–r3 ultracritic round reports of #0004 (BUG-1), and #0003's gate PNGs
(gitignored by design, re-renderable deterministically — acceptable loss).
