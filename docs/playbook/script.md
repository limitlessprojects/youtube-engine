# Playbook — Script (stage 1 of 7)

> Purpose: turn a topic + formula into a frozen, fact-checked, lint-clean script
> spec. Reader: the session agent at the start of a short.
> Inputs: topic (formula rotation in `docs/plan-30d.md`), blueprints
> (`research/blueprints/`), rules `docs/rules.md` §Script.
> Outputs: `content/<slug>/script.md` (human-readable), `script.json` (schema
> below), `vo_lines.json` (line table for VO).

## Commands (in order)

```bash
# 1. Draft against prompts/scriptwriter_system.md (rules 1–16 baked in),
#    fact-checking every claim as you write (rule S7).
# 2. Lint (fails → fix, do not proceed):
python3 tools/script_linter.py content/<slug>/script.json --format short
# 3. Critic pass (prompts/critic_system.md): all six dims ≥8, N=2 cap (rule S9).
#    Linter PASS does not exempt the critic; the critic scores retention, the
#    linter scores hygiene.
```

## script.json schema (current, from short-0004)

```json
{
  "title": "Why is the sky blue? (It's not the ocean)",
  "format": "short",
  "hook": {"timestamp_start": 0.0, "narration": "…", "visual": {"pose": "…", "prop": "…", "background": "…"}, "fact_sources": ["…"], "audio_dur_s": 0.0},
  "scenes": [ /* same shape as hook, timestamp_start ascending */ ],
  "sfx": [{"at": 0.95, "kind": "blip|thump|riser|whoosh", "seed": 21, "gain": 0.7}],
  "timeline": {"fps": 30, "total_s": 31.18, "gap_s": 0.25, "voice": "edge-tts … rate +25% (measured 201 WPM …)", "words": 94, "wpm_measured": 201}
}
```

`timestamp_start` / `audio_dur_s` are written by the VO stage (real durations),
not estimated here. `sfx.at` values are final-timeline seconds.

## Rules that bite here (full table: docs/rules.md §Script)

S1 banned vocab · S2 hook ≤3s/opener ≤14w · S3 orient (topic named in hook) ·
S4 one spine one closer · S5 WPM 185–215 · S6 mean ≤3.2s, max ≤4.2s, ≥12 events ·
S7 fact_sources required · S8 rhythm variety.

## Known failure modes

| Symptom | Cause | Fix |
|---|---|---|
| linter FAIL "hook too long" | opener >14 words | cut to the divergence+promise in one breath |
| linter FAIL "L-073 orientation" | hook subverts a topic it never named | put the title's noun in the hook narration |
| linter FAIL "WPM out of band" | drafted at the old 165 pace or at 3.2 w/s edge class | re-time at 185–215; re-check after real VO durations land (stage 2) |
| A4 warn "new entity in closer" | tangent entity in last 2 scenes | move it to the backlog, close on the spine |

## Acceptance check (gate to the next stage)

- linter exit 0 (PASS) with the script's JSON.
- Critic verdict `pass` (all dims ≥8) within N=2.
- Every scene has `fact_sources` + a `visual` the engine can draw (poses from
  the current POSES vocabulary in any recent scenes.html).
- ≥10 scenes for ~35s (rule S6 warn floor).
