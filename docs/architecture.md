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

## Residential runner (the bot-wall endgame, ledger L-037)

A self-hosted runner on ANY home machine (laptop, mini-PC, NAS) does two things at once:
jobs start instantly (no hosted-queue lag) and YouTube sees a residential IP — the
direct paths in transcribe.py stop being blocked, no mirrors needed.

One-time setup on that machine (3 commands + 1):

```bash
# get a fresh registration token (expires in 1h):
curl -s -X POST -H "Authorization: Bearer <GH_PAT>" \
  https://api.github.com/repos/limitlessprojects/youtube-engine/actions/runners/registration-token
# then on the machine:
./config.sh --url https://github.com/limitlessprojects/youtube-engine --token <TOKEN> --labels home --unattended
./svc.sh install && ./svc.sh start        # or just: ./run.sh for a session runner
```

Then switch the workflow's `runs-on: ubuntu-latest` to `runs-on: [self-hosted, home]`
when the runner is online; hosted runners remain the fallback (GitHub routes to them
if the label doesn't match — keep a dual-job or the default label fallback).
