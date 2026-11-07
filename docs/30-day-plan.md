# The 30-Day Plan — Day 008 (Nov 8) → Day 037 (Dec 8)

> Owner: the nightly 23:45 EAT session (platform cron 512606) + the 20:00 UTC
> Actions heartbeat. This doc is the contract: what runs daily, what each
> phase proves, and the forks we pre-decide so nobody spirals at midnight.
> Sources: engine-v3-spec, day007 autopsy, day008 skills-lessons synthesis,
> competitor outlier sweep, 61 ledger lessons.

## Standing rules (every day, no exceptions)

1. **Cadence > polish.** One Short ships daily. A 7/10 that ships beats an
   8.5 that doesn't (R10; L-061). Polish budget: max 2 gate re-render rounds.
2. **The gate is the law, arbitration is the appeal.** VLM verdicts with
   pixel-probe arbitration (day-008 precedent); false positives documented,
   never "fixed" by breaking design.
3. **Measure, never estimate** (L-003): VO durations real, WPM real, views
   real. Every number in every ledger entry has an artifact behind it.
4. **Atomic pushes** after every milestone (L-044). The sandbox dies; the
   repo doesn't.
5. **Fact-check before script freeze.** No claim enters a timeline without a
   source (day-007 standard). The 10x-reaction-time cut is the template.
6. **Disclose synthetic content on every upload.** Non-negotiable (L-013).

## The daily loop (nightly session, ~40 min)

| Step | Action | Tool |
|------|--------|------|
| 1 | Restore check (`.git` present? else L-058 flow) | `scripts/restore_workstation.sh` |
| 2 | Pull + review Actions run (20:00 UTC) | repo |
| 3 | Log channel views from RSS/oEmbed | `tools/rss_scout.py` |
| 4 | Advance the next short (script → VO → render → gate → publish) | v3 pipeline |
| 5 | VLM autopsy the freshest published frame | CDN thumbnail + `z-ai vision` |
| 6 | Ledger entry + log + commit + push | `lessons/` |

## Phase A — Quality proof (Day 008–014, Nov 8–14)

**Question: does engine v3 hold quality at daily cadence?**

- Daily: one Short on the v3 pipeline (dusk world family + stage panels +
  sound design + 176-WPM class pacing). Short #0002 is the template.
- VO: edge-tts default (keyless, proven); Fish s2.1-pro-free via the new
  `vo-gen.yml` CI workflow when a key-less batch is wanted — pick by ASR WER.
- Formula rotation (match execution ceiling, L-060): everyday-curiosity ×2,
  belief-correction ×2, superlative ×2, one wildcard.
- **Day 014 checkpoint (Nov 14):** first-frame VLM autopsy mean ≥7.5/10
  across the week AND pipeline wall-clock ≤40 min/short. Below → freeze
  new features, spend the week on the weakest of the 7 v3 upgrades only.

## Phase B — Signal proof (Day 015–021, Nov 15–21)

**Question: does anything we make actually get watched?**

- Keep the daily cadence (non-negotiable, it's the sample size).
- Add: A/B hooks on the same premise every 3rd day (two cuts of one script,
  publish 48h apart, compare 24h retention + swipe-away).
- Add: the oEmbed view tracker into the nightly loop with a 7-day rolling
  chart committed to `logs/views.csv`.
- **Pre-decided fork (Day 15 = Nov 21, from engine-v3-spec):** if best
  Short quality <8/10 OR median 24h views <1K → **pivot WITHIN YouTube**
  (new format/topic family per the outlier formulas), not away from video.
  The fork executes at the Nov 21 session — no renegotiation.

## Phase C — Scale what works (Day 022–030, Nov 22–Dec 1)

**Question: can we 10x the winner without quality dropping?**

- Double down on the best formula-hook combo from Phase B (2 Shorts/day OK
  if the gate stays green; never lower the gate to ship more).
- Start long-form (8–12 min, 2×/week) ONLY if 10+ Shorts live and the best
  24h median ≥2K views (v3-spec gate). Long-form = 3 shorts-worth of beats
  around one spine, `what-if-animation` 7-beat structure.
- Batch: Sunday session produces Mon–Wed scripts + VO; weeknights render.
- **Day 30 scoreboard (Dec 1):** 10+ Shorts live, one >10K-view outlier,
  engine at 8/10 floor, 30 ledger entries. Miss 2 of 4 → Phase D becomes
  a strategy session with the boss, not a silent grind.

## Phase D — Compound (Day 031–037, Dec 2–8)

- Whatever the scoreboard says: double the winner, kill the losers.
- If Shorts outlier exists → long-form funnel from its best hook.
- If not → boss conversation: pivot proposal with data (which formulas,
  which hooks, which retention curves).
- Week of Dec 7: mine all 30 lessons → `docs/engine-v4-spec.md`.

## Risk register (pre-decided responses)

| Risk | Signal | Response |
|------|--------|----------|
| Sandbox recycle | `.git` missing | L-058 restore flow (upload/ mirrors + PAT) |
| OAuth refresh dies | upload 401 | Ask boss to re-verify the Google app (nura-health) |
| Bot-wall blocks queue head | blocked N days | Rotate queue; radar continues on RSS/oEmbed |
| ASR quota flake | empty verify lines | 2s backoff (vo_pipeline), accept documented biases |
| Gate loop spirals | >2 re-renders | Ship at 7/10, document residuals (day-008 precedent) |
| Views flatline at <100 | Phase B data | Formula rotation, not premise doubt (L-060) |
| Boss unavailable | forks blocked | Pre-decided forks execute automatically |

## What "done" looks like on Dec 8

A channel with 20+ live videos, a repeatable v3 pipeline that one agent
session runs in under an hour, one proven outlier formula, and a ledger
that any future agent (or human) can read as the operating manual.
