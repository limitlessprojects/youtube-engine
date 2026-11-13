# The 30-Day Plan — status Day 013 (Nov 12), horizon Day 037 (Dec 8)

> Reader: the next session's agent. This is the contract: what each phase proves,
> what you owe the channel today, and the forks we pre-decided so nobody spirals
> at midnight. Standing rules and the daily loop live in `README.md`; this file
> is the schedule and the scoreboard. History: `docs/_archive/`.

## Standing rules (every day, no exceptions)

1. **Cadence > polish** — one Short ships daily; a 7/10 that ships beats an 8.5 that doesn't. Polish budget: 2 gate rounds + 1 ultracritic round, then ship-or-carry.
2. **The ultracritic gate is the law; arbitration is the appeal** (pixel-probes for spatial claims; false positives documented, never "fixed" by breaking design).
3. **Measure, never estimate** — VO durations, WPM, views, scores: every number has an artifact behind it.
4. **Atomic pushes** after every milestone. The sandbox dies; the repo doesn't.
5. **Fact-check before script freeze** — no claim enters a timeline without a source.
6. **Disclose synthetic content on every upload** (automated in `youtube_upload.py`).
7. **Below bar after 3 rounds → NO POST, carry with report** — cadence debt is paid at the next session, never forgiven silently.

## The daily loop (nightly session, target ≤40 min)

| Step | Action | Tool |
|---|---|---|
| 1 | Restore check (`.git` present? else run `bash /home/z/my-project/scripts/restore_workstation.sh --from-upload`) | shell |
| 2 | Pull + review the 20:00 UTC Actions run (no new log? the run may not have fired — check the Actions tab, don't assume) | `logs/` |
| 3 | Log channel views | `tools/views_tracker.py` |
| 4 | Carry-debt first: if a short sits BELOW_BAR, iterate its latest `gate/ultracritic_r*.json` directives, re-gate | `tools/ultracritic.py <slug> --round N+1` |
| 5 | Advance the next short: script → VO → scenes → render → gates → publish | `docs/playbook/` |
| 6 | Ledger line + log + commit + push | `docs/lessons.md` + `logs/` |

## Status right now (end of Day 013 nightly session, 2026-11-12)

- Published: #0001 (KKyrNUGZXcU, engine v1), #0002 (CZbJmmeyUc4, v3 debut), #0003 (DeaEvEduh88, boss-criticized, ultracritic 5.20).
- **Views (2026-11-12, RSS): #0003 = 1,148 · #0002 = 1,141 · #0001 = 197.** The 5.20-scored short still leads — gate score ≠ discovery pull; Phase B's question stands.
- **Carry: #0004 CLOSED (L-085)** — r8 7.53 hit the grand bar but visual_hierarchy 6.9 < 7.0 with s4 floor breach; r9 redesign 7.35 proved the ~6.9 ceiling is FORMAT-level (panel-in-world diagram cards). No more polish laps; the fix is #0005's canvas-first format. #0002 thumbnail unblocked by the live grant (L-092) — ship it next session.
- **#0005 (superlative formula #1): "The loudest sound in history" — Krakatoa 1883.** Day-013 delivered: fact-checked script (all 11 lines sourced: Wikipedia 1883 eruption + Anak Krakatau, Nautilus 2014), linter PASS, critic pass round 1 (all six dims ≥8, critique.json), VO synthed + measured (36.34s, WPM 214.5 canon — band ceiling, see script.md status block), ASR union-verified 11/11 (L-091; off-peak re-verify before render). **Next session: scenes.html canvas-first + hook-variant probes (L-087) → render → gate → publish-or-carry.**
- **OAuth (L-084/L-092): GRANT LIVE — day-013's "dead" verdict was a false alarm.** A day-014 refresh against the durable mirror (`upload/token.json`, day-011 mint) returned 200 and `youtube_upload.py --check-token` = OK. Working copy at `.secrets/token.json`. Unblocks, in order: #0002 thumbnail (`--set-thumbnail`), then uploads. `oauth_mint.py` stays as the re-mint fallback.
- Boss action items open: ① ~~click the consent URL~~ MOOT (L-092 — grant never died); ② confirm the nura-health OAuth app is in **Production** status in Google Cloud Console (Testing mode kills refresh tokens in 7 days — the day-011 mint will die ~Nov 19 if the app is still in Testing).
- New GitHub PAT installed day-013 (old one possibly expired) — clone/pull/push verified working; Actions API read OK.
- **Day-014 boss directives (2026-11-13):** ① style bible + layered assets + motion-design upgrade (rules C13–C17, G9; lesson L-095) — this is the L-085 format fix, generalized; ② cron loop moves to TWICE DAILY; ③ free-GPU hero-shot route via the mr-bean-motion-swap GH-Actions × ZeroGPU pattern — adopted as pattern, not repo; freefield parked (L-094); assessment in `research/free-gpu-video.md`. Model correction: that repo runs Wan2.2-Animate, not SeedDance 2.5 (L-093).

## Phase A — Quality proof (Day 008–014, Nov 8–14)

**Question: does engine v3 hold quality at daily cadence?**

- Daily: one Short on the v3 pipeline. Formula rotation (match execution ceiling): everyday-curiosity ×2 (#0002 ✓, #0003 ✓), belief-correction ×2 (#0004 built, in carry), superlative ×2 (#0005, #0006), one wildcard (#0007).
- VO: edge-tts default with per-script `VO_RATE`; Fish via `vo-gen.yml` optional when credits allow (dead-end D6 first).
- **Each day's agent delivers:** a short that either PUBLISHES (ultracritic ≥ bar) or CARRIES with a fresh round report + 3 named directives; a views row; a ledger line. Verified by: `gate/ultracritic_r*.json` verdict + `published.json` or the carry report.
- **Day 014 checkpoint (Nov 14):** first-frame VLM autopsy mean ≥7.5 across the week AND pipeline wall-clock ≤40 min/short. Below → freeze new features; spend the following week on the weakest v3 upgrade only.

## Phase B — Signal proof (Day 015–021, Nov 15–21)

**Question: does anything we make actually get watched?**

- Cadence non-negotiable (it's the sample size).
- Add: A/B hooks every 3rd day (two cuts of one script, 48h apart, compare 24h retention + swipe-away).
- Add: `views_tracker.py` nightly with 7-day rolling comparison in the ledger.
- **Pre-decided fork (Nov 21):** best Short quality <8/10 OR median 24h views <1K → **pivot WITHIN YouTube** (new format/topic family per outlier formulas), not away from video. Executes at the Nov 21 session; no renegotiation.

## Phase C — Scale what works (Day 022–030, Nov 22–Dec 1)

- Double the best formula-hook combo (2 Shorts/day OK if the gate stays green; never lower the bar to ship more).
- Long-form (8–12 min, 2×/week) ONLY if 10+ Shorts live AND best 24h median ≥2K views. Long-form = 3 shorts-worth of beats around one spine, 7-beat formula.
- Batch Sundays: Mon–Wed scripts+VO; weeknights render.
- **Day 30 scoreboard (Dec 1):** 10+ Shorts live, one >10K outlier, engine at 8/10 floor, 30 ledger entries. Miss 2 of 4 → Phase D becomes a boss strategy session.

## Phase D — Compound (Day 031–037, Dec 2–8)

- Double the winner, kill the losers; Shorts outlier → long-form funnel from its best hook.
- No outlier → boss conversation with data (formulas, hooks, retention curves).
- Week of Dec 7: mine all 30 days → engine-v4 spec.

## Risk register (pre-decided responses)

| Risk | Signal | Response |
|---|---|---|
| Sandbox recycle | `.git` missing | `bash /home/z/my-project/scripts/restore_workstation.sh --from-upload` (~2 min, proven 5×) |
| OAuth refresh dies | upload 401 | boss re-verifies the Google app (project nura-health) |
| Bot-wall blocks queue head | blocked N days | rotate queue; radar continues on RSS/oEmbed |
| ASR quota flake | empty verify lines | 2s backoff, accept documented biases (L-066) |
| Gate loop spirals | >3 ultracritic rounds | carry with report; next session pays the debt |
| Views flatline <100 | Phase B data | formula rotation, not premise doubt (L-060) |
| Boss unavailable | forks blocked | pre-decided forks execute automatically |
| ffmpeg wrapper noise | exit 255 post-success | verify artifacts, not exit codes (day-010) |
