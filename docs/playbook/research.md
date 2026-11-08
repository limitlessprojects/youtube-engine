# Playbook — Research loop (the CI side; runs without you)

> Purpose: the LLM-free heartbeat that turns competitor videos into structural
> blueprints and watches the downloader horizon. It runs itself on GitHub
> Actions (20:00 UTC daily, 5-leg matrix); your job is only to queue items,
> read its output, and mine blueprints when scripting.
> Outputs: `research/blueprints/*.json|.md`, `logs/YYYY-MM-DD.md`,
> `research/cache/` (downloaders radar, sweeps), queue pops.

## Commands

```bash
# Queue a competitor video (one URL per line, FIFO):
echo "https://www.youtube.com/watch?v=VIDEO_ID" >> config/learning_queue.txt
# Run the loop locally:
python3 tools/daily_loop.py
# Outlier discovery (no bot-wall — RSS carries view counts):
python3 tools/rss_scout.py --enqueue 2
# Views of OUR channel (nightly):
python3 tools/views_tracker.py
```

## How it works

1. `daily_loop.py` pops the queue head → `transcribe.py` runs the 6-path ladder:
   captions API → yt-dlp subs → Invidious mirrors → Piped mirrors → Whisper →
   proxy escalation. Every path wraps its own failures (rule Q3 — a block on
   path N is evidence about path N only). oEmbed pre-checks liveness; 404 pops
   the item as RETIRED (rule Q2).
2. `blueprint_extractor.py` (deterministic, no LLM) → WPM, hook length, sentence
   rhythm, cue density, cut estimate → `research/blueprints/`. The LLM analyst
   prompt (`prompts/blueprint_analyst.md`) is for the session agent to extend
   it — structure only, never content (rule Q6).
3. CI matrix: 5 legs (direct/proxy/android/mweb/tv) = 5 fresh runner IPs per
   day, `continue-on-error`, first winner merges. Blocked days stay green and
   retry (queue item only pops on success).
4. `probe_downloaders.py` radar: daily snapshot of y2mate-class sites into
   `research/cache/downloaders.json` — research-only, never production (Q7, D2).

## Known failure modes

| Symptom | Cause | Fix |
|---|---|---|
| item blocked N days straight | hard-flagged IPs (L-049) | rotate the queue (move to back); matrix keeps buying daily lottery tickets |
| all mirrors dead | registry decay (L-050) | `fetch_instances.py` feeds live registries; never hardcode |
| local push rejected | runner committed meanwhile | `git pull --rebase` before push (L-038) |
| WebFetch says a site is gone | fetcher artifact on JSON (L-052/L-047) | second egress (curl) before any "dead" verdict |

## Acceptance check

- The Actions run is green (blocked-but-retried counts as green).
- New blueprints land as `.json` + `.md` pairs with oEmbed title/author inside.
- The queue never has a known-dead ID at head (oEmbed pre-check enforces).
