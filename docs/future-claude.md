# Directive to the next Claude — review and improve the 30-day plan + documentation hygiene

Boss read `../AGENTS.md` (after finishing the day's work) and said, verbatim import:

> "also tell the future ai to review improve 30 day plan etc approaches to stuff and organizing documentation and instructions"

If you're reading this: **your first job is not a new Short. It is a 20-minute honest audit of the project's paperwork, then small corrective commits.**

## Why this exists

During 2026-11-14, the boss caught three legitimate paperwork failures:

1. The 30-day plan (`docs/plan-30d.md`) drifts faster than sessions update it — it claims stale status, stale closure decisions, and imprecise scenes. Update it.
2. Dashboards / views / lessons live in scattered files (`logs/views.csv`, `logs/2026-11-14.md`, `docs/lessons.md`, `gate/*`, `published.json`) — every new agent re-derives the same things. Consolidate, don't duplicate.
3. Instructions often still say "work hard and push the plan" without locale facts (e.g., playwright cache symlink `1255→1254`, `--break-system-packages`, token-frozen-CI Secrets) — AGENTS.md covers some, but not all topics like design judgment

## Non-negotiable scope

Touch:

1. `docs/plan-30d.md` — refresh from ALL current inputs or delete and supersede with a short current plan. Never leave stale claims in a dated file.
2. `docs/registry.md` — verify every tool listed actually exists and is used; dead rows: remove (reference AGENTS.md for the running machine).
3. `AGENTS.md` — add what "verified" today already established (playwright symlink, pip `--break-system-packages`, rich agents GOOD, harness gained capabilities) so the next session starts zero-dependency.
4. `README.md` — referenced files must ALL exist (Point to `docs/plan-30d.md` and `docs/publish-runway.md` and `AGENTS.md`).
5. `research/video-notes/README.md` + `video-notes/BLOCKED.md` — keep current; no-delete-republish rule spelled out.
6. `.gitignore` — keep frames-ignored convention paired with the principle "report + JSON allowed, pixels stay local"; never commit mp4s.

Do NOT (heavy):

- Move files around (this program has settled locations — write new co-locations in docs/_archive/ if needed)
- Rewrite history or change "last verified" dates without re-checking reality
- Force "fresh" marketing prose; terse mechanical claims only

## The 90-minute audit script (run in this order)

1. Read this repo for the four above-mentioned files in order, one pass.
2. For each stale claim, choose: (a) correct + re-verify today, (b) archive to `docs/_archive/` with the date, (c) delete.
3. Commit `docs(audit): <list of fixes>` — 1 atomic commit, loud message.
4. Ask the boss **before** touching:
   - the 30-day plan MORE-than-deletion (i.e., before deciding phases exist);
   - the style bible / canvas-first / C13 (boss owns);
   - Voices/engines (boss owns spend).
5. If you're ever in doubt, **the rule is no change, write the question to `logs/<date>.md` and stop** — silence on documentation drift is not exemption to authorize.

## Pace rule

Maintenance cadence: lazy once per 3 sessions, never after each Short. Total time ≤ 90 min, throughput ≥ one fix per 10 min.

## Final note from this session's losses

2026-11-14 was a gold-standard run of "go back to the paper" — `AGENTS.md` triggered a working matrix job + produced a hand-drawn deliverable; `BLOCKED.md` gave future agents direct failure report + fix; `TOP10-UPGRADES.md` was the boss's "correct me on the direction of the channel" override; the action of merging fresh-machine port (different agent) was exactly the kind of consolidation the boss wants more of — not less. Your job is to make the NEXT agent start here, faster than you did.
