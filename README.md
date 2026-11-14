# youtube-engine — an autonomous "What If" stickman Shorts studio

One repo holds everything the channel knows and makes: the pipeline, the rules,
the research loop, and the daily paper trail. Channel: **Jack Blessed**
(@JackBlessed-u5x). Format: "What If" stickman explainers, Shorts 30–60s daily.

**READ THIS FIRST if you are a fresh agent:** your whole job tonight is in
`docs/plan-30d.md` (status + today's deliverable) and `docs/playbook/` (how).
The gate decides what ships — never your enthusiasm (`docs/playbook/gate.md`).

## The pipeline in 10 steps

```
1  topic (formula rotation)                     docs/plan-30d.md
2  script draft + fact-check                    prompts/scriptwriter_system.md
3  lint + critic (N=2 cap)                      tools/script_linter.py
4  VO synth → measure → ASR verify → timeline   tools/vo_pipeline.py        [playbook/voiceover.md]
5  scenes.html authoring (engine/*.js)          content/<slug>/render/      [playbook/scenes.md]
6  keyframe render + vlm_gate loop (≤2/scene)   tools/render_short.py, tools/vlm_gate.py
7  full render + audio finish (−14 LUFS)        tools/finish_v3.py          [playbook/audio.md]
8  ULTRACRITIC: A1–A5 + frame pass + video pass tools/ultracritic.py        [playbook/gate.md]
9  publish ONLY on PUBLISH_APPROVED             tools/youtube_upload.py     [playbook/publish.md]
10 ledger + log + commit + push                 docs/lessons.md, logs/
```

Steps 2–10 are the nightly loop (~40 min target). A short that doesn't clear
the bar after 3 rounds is carried with its report — cadence debt is paid, never
forgiven silently.

## Where everything lives

| Path | What |
|---|---|
| `docs/plan-30d.md` | **today's mission**: phases, status, forks, risks |
| `AGENTS.md` | machine runbook: fresh-clone setup, VLM/judge state, publish path, multi-session concurrency |
| `docs/publish-runway.md` | the publish runway: exact commands to ship a Short (lint → render → gate → upload) |
| `docs/playbook/` | one file per stage: script, voiceover, scenes, audio, render-encode, gate, publish, research |
| `docs/rules.md` | every hard rule + evidence + the tool that enforces it |
| `docs/parameters.md` | every tuned constant + why (WPM band, bar 7.5, bed levels…) |
| `docs/lessons.md` | the ledger, deduplicated and grouped (raw history in `docs/_archive/`) |
| `docs/dead-ends.md` | tried and failed — read before experimenting |
| `docs/registry.md` | every skill/repo we build on (verified only) |
| `skills/stickman-whatif/` | the production skill: SKILL.md + templates + exemplars |
| `engine/` | the render engine (rig, world, diagram, caption modules) |
| `tools/` | executable pipeline — every file has a docstring; `tools/preflight.py` runs the cheap checks |
| `content/short-NNNN/` | per-short spec: script.json, vo/, render/scenes.html, gate/ (verdict trail) |
| `prompts/` | system prompts: scriptwriter, critic, VLM inspector, blueprint analyst |
| `research/`, `config/`, `logs/` | competitor blueprints, queue, daily logs + views.csv |
| `vendor/` | pinned submodules (what-if-animation is the backbone — see registry) |
| `docs/_archive/` | raw history. Never deleted; never *depended on* for operational knowledge (provenance citations only). |

## The daily loop (runs itself + you)

- **GitHub Actions (20:00 UTC):** the LLM-free research heartbeat — transcribe
  queue head via the 5-leg bot-wall ladder, blueprint it, log + commit
  (`docs/playbook/research.md`).
- **Agent session (23:45 EAT, platform cron):** restore check → review the run →
  views → pay any carry debt → advance the next short through steps 2–10 → ledger.

## Non-negotiables

- The ultracritic bar is the publish authority: **≥7.5 mean, every dim ≥7.0, no
  frame <6.0, video pass required.** Below = NO POST, carry with report.
- Zero AI boilerplate (linter-enforced), fact-checked claims with sources,
  synthetic-content disclosure ON every upload (automated), one Short daily.
- Measure, never estimate. Every number in every entry has an artifact.
- Atomic pushes after every milestone — the sandbox dies; the repo doesn't.
  Recovery: `bash /home/z/my-project/scripts/restore_workstation.sh --from-upload` (~2 min).

## Secrets

GitHub Actions secrets: `FISH_AUDIO_KEY`, `GOOGLE_CLIENT_ID`,
`GOOGLE_CLIENT_SECRET`, `YOUTUBE_TOKEN_JSON` (+ optional `YTA_PROXY`,
`YTDLP_COOKIES`). Local twins live at `/home/z/my-project/.secrets/` (outside this repo),
durable mirrors in `/home/z/my-project/upload/` (the one directory sandbox
recycles never touch). Never commit key material.

## License

Our code: MIT. Vendored skills keep their own licenses (see each submodule);
`what-if-animation` and `tool-reel-system`: verify before commercial use.
