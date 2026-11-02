# Architecture — the multi-agent pipeline

## Flow

```
                    ┌──────────────────────────────┐
                    │  A. Trend Scout (daily/weekly)│
                    │  yt-dlp search · outlier score│
                    │  · channel watch (channels.json)
                    └──────────────┬───────────────┘
                                   │ enqueues video URLs
                                   ▼
                    ┌──────────────────────────────┐
                    │  B. The youtubecheck          │
                    │  transcribe.py (captions →    │
                    │  Whisper fallback)            │
                    └──────────────┬───────────────┘
                                   │ transcript JSON
                                   ▼
                    ┌──────────────────────────────┐
                    │  C. Blueprint Extractor       │
                    │  hook/WPM/rhythm/cut-density  │
                    │  → research/blueprints/       │
                    └──────────────┬───────────────┘
                                   │ structural blueprint (not content!)
                                   ▼
        ┌──────────────────────────────────────────────┐
        │  D. Scriptwriter (prompts/scriptwriter_system)│──► script_linter.py ──┐
        └──────────────────────────┬───────────────────┘                       │ fail
                                   │ pass                                      │
                                   ▼                                           ▼
        ┌──────────────────────────────────────────────┐              back to D
        │  E. Harsh Critic (prompts/critic_system)      │
        │  scores hook/pacing/predictability ≥ 8/10     │
        │  HARD CAP N=2 revisions, then discard premise │
        └──────────────────────────┬───────────────────┘
                                   │ approved script JSON (strict schema)
                                   ▼
        ┌──────────────────────────────────────────────┐
        │  F. Shot List & Assets                        │
        │  visual tags → stickman rig library / props   │
        │  (stickman-video-director, what-if-animation) │
        └──────────────────────────┬───────────────────┘
                                   │ Remotion project state
                                   ▼
        ┌──────────────────────────────────────────────┐
        │  G. Render + VLM Inspector (per scene)        │
        │  text-collision · anchoring · drift · pacing  │
        │  outputs bbox offsets → re-render (max 2)     │
        └──────────────────────────┬───────────────────┘
                                   │ pass
                                   ▼
        ┌──────────────────────────────────────────────┐
        │  H. Audio: fish_tts.py → ASR round-trip check │
        │  → master −14 LUFS, music ducked              │
        └──────────────────────────┬───────────────────┘
                                   ▼
        ┌──────────────────────────────────────────────┐
        │  I. youtube_upload.py                         │
        │  OAuth refresh → resumable upload             │
        │  synthetic-content disclosure: YES            │
        └──────────────────────────┬───────────────────┘
                                   ▼
                    ┌──────────────────────────────┐
                    │  J. Logger (daily, automated) │
                    │  logs/ + lessons/ ledger      │
                    │  → git push (atomic)          │
                    └──────────────────────────────┘
```

## Guardrails (learned the hard way — see ledger)

- **State separation:** script state feeds forward only. VLM fixes change layout,
  assets, timing — never story mid-render.
- **Hard caps:** critic N=2, VLM re-render N=2 per scene. Fail → discard, move on.
  No infinite polish loops, no over-analysis of turbulence.
- **Schema validation:** every agent handoff is strict JSON (scenes: timestamp_start,
  narration, asset_ids, pose). Bad JSON → reject and regenerate that step only.
- **Deterministic daily loop:** the CI runner (`tools/daily_loop.py`) is LLM-free and
  must stay green even when YouTube blocks it (retry, don't fail).
- **Atomic backups:** writes land in `logs/` and `research/` only on success; a failed
  push retries next run. Scratch never blocks the pipeline.
- **Secrets:** keys live in GitHub Actions secrets + local `.secrets/` (gitignored).
  No key material ever enters the repo, logs, or prompts.

## Memory bank

- Now: markdown blueprints in `research/blueprints/` (deterministic, diffable).
- Next: when blueprints > ~50, index them (SQLite FTS first, vector DB only if
  retrieval quality demands it) so the scriptwriter gets the top-3 structural
  blueprints as context per generation.
- Weekly: mine `lessons/` — recurring wins get promoted into `prompts/` and
  `docs/content-strategy.md`; recurring failures become guardrails above.

## Where things run

| Stage | Runs where | Cost |
|---|---|---|
| A–C (scout, transcribe, blueprint) | GitHub Actions daily + local sessions | free (runner minutes) |
| D–E (script, critic) | agent sessions (LLM) | free tier |
| F–G (assets, render, VLM) | sandbox (Remotion/ffmpeg/Playwright) | free |
| H (TTS + ASR) | Fish Audio s2.1-pro-free (daily free quota) + platform ASR | free |
| I–J (upload, log) | local session → OAuth; CI commits logs | free |

## The bot-wall ladder (endgame — everything on GitHub-hosted runners, L-039)

Directive: no residential hardware. Every rung runs on the sandbox or on
GitHub-hosted runners, and each adds an independent chance to get the day's
transcript. One winner is all the daily loop needs.

| Rung | Mechanism | Where it lives |
|---|---|---|
| 1 | Off-peak cron (06:00 UTC) — fewer runners competing, fresh IPs | `daily-loop.yml` schedule |
| 2 | The 6-path chain: captions → yt-dlp → Invidious mirrors → Piped mirrors → Whisper → proxy escalation | `tools/transcribe.py` |
| 3 | **Matrix parallel legs** — 3 jobs = 3 different hosted-runner IPs (fresh per job), `fail-fast: false`, winner merged by priority | `daily-loop.yml` jobs `attempt`/`merge` |
| 4 | **Proxy rotation** — fresh validated proxies from GitHub-hosted lists (updated every 5–30 min); YouTube sees the proxy IP, never ours | `tools/proxy_pool.py` |
| 5 | Player-client rotation — `android` client often gets different treatment than `web` | `YTDLP_PLAYER_CLIENT` env (android leg) |

Why this beats a single residential runner: it's 3 lottery tickets a day instead
of one machine that can die, and it costs zero maintenance. Free proxies are
opportunistic (heavily shared IPs — many are pre-blocked at the captions
endpoint), so rung 4 is a bonus, not a dependency; the legs' fresh runner IPs
and the mirror pool carry the base rate.

Daily ops (3 commands, run anywhere — sandbox or runner):

```bash
python tools/proxy_pool.py best --n 3     # fresh validated proxies, latency-sorted
python tools/proxy_pool.py env            # -> PROXY_URL=... (eval $(...) to use)
python tools/transcribe.py <video-id>     # full 6-path ladder incl. escalation
```

List sources (auto-fetched, overridable via `PROXY_LIST_URLS`):
proxifly/free-proxy-list (every 5 min), monosans/proxy-list (every 30 min,
pre-checked), TheSpeedX/SOCKS-List (daily). Cache: `research/proxies/cache.json`
(20-min TTL, gitignored). Optional extras in Secrets: `YTA_PROXY`,
`YTDLP_COOKIES` (a logged-in cookie jar shifts YouTube's bot heuristics).
