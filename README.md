# youtube-engine

**The operating base for our autonomous YouTube channel.** One repo that holds the
lessons ledger, the skill stack, the competitor-research pipeline, the tools, and the
daily scheduler. Everything the channel learns lives here; everything the channel
makes starts here.

- Channel format: **"What If" stickman explainers** (Shorts 30–60s daily + long-form 8–12min 2×/week)
- Non-negotiables: zero AI boilerplate, retention-first structure, VLM-checked frames,
  synthetic-content disclosure on every upload, daily paper trail

---

## Repo map

```
youtube-engine/
├── lessons/        The daily ledger. What we learned, what we change tomorrow.  ← START HERE
├── docs/           Strategy, architecture, tooling registry, YouTube OAuth guide
├── prompts/        System prompts: scriptwriter, harsh critic, VLM inspector, blueprint analyst
├── skills/         The 13-skill stack registry (sources + roles + status)
├── tools/          Executable pipeline: transcribe (6-path + proxy ladder), blueprint, linter, TTS, render, VLM gate, master, upload, daily loop
├── vendor/         Git submodules of the skills/repos we build on (pinned commits)
├── config/         Competitor channels + learning queue (video URLs to process next)
├── research/       Output: transcripts/ and structural blueprints/ of competitor videos
├── logs/           Daily execution logs (auto-appended by the scheduler)
└── .github/
    └── workflows/  daily-loop.yml — GitHub Actions scheduler (06:00 UTC daily + manual)
```

## The daily loop (runs itself)

Every day at 06:00 UTC a GitHub runner:

1. Pops the next video off `config/learning_queue.txt`
2. Transcribes it (captions via `youtube-transcript-api`; Whisper fallback locally via
   `vendor/Youtube_transcriber`)
3. Extracts a **structural blueprint** — hook length, WPM, sentence rhythm, cut density,
   open-loop markers — into `research/blueprints/`
4. Appends the day's log to `logs/YYYY-MM-DD.md` and commits back to this repo

Queue a new competitor video:

```bash
echo "https://www.youtube.com/watch?v=VIDEO_ID" >> config/learning_queue.txt
```

Run the loop locally:

```bash
pip install -r requirements.txt
python tools/daily_loop.py
```

## The 13-skill stack (short version)

| # | Skill | Source | Role |
|---|-------|--------|------|
| 1 | stickman-video-director | `kaomei/stickman-video-director` (submodule) | Script → multi-style stickman video |
| 2 | what-if-animation | `kelano86/what-if-animation` (submodule) | 7-beat What-If formula, SVG+Remotion, 11-pt self-check |
| 3 | tool-reel-system | `kelano86/tool-reel-system` (submodule) | Reverse-engineered reel script + edit formula |
| 4 | Youtube_transcriber | `Rakile/Youtube_transcriber` (submodule) | The "youtubecheck": competitor transcripts via Whisper |
| 5 | motionmaxxing | our fork (submodule) | Turns AI-slop motion into designer-grade films |
| 6 | motion-skills | our fork (submodule) | 50 motion-graphics skills, 14 installable packs |
| 7 | anthropic skills | `anthropics/skills` (submodule) | docx/pdf/pptx/xlsx/canvas-design/skill-creator |
| 8 | Remotion | `remotion-dev/remotion` (npm dep) | Programmatic video assembly |
| 9 | Manim GX | our fork `manimgx` (noted) | Math/3D animation engine, Rust GPU core |
| 10 | Fish Audio TTS | in-house `tools/fish_tts.py` | s2.1-pro-free narration, daily free quota |
| 11 | VLM Inspector | in-house `prompts/vlm_inspector.md` | Frame-by-frame QC before any render ships |
| 12 | Openclip | our fork `Openclip` (noted) | Competitor video → study clips |
| 13 | unslop | our fork `unslop` (noted) | De-AI-ifies anything that looks vibecoded |

Full details, provenance and status: [`skills/REGISTRY.md`](skills/REGISTRY.md) and
[`docs/tooling.md`](docs/tooling.md) (25+ repos verified and catalogued).

## Secrets (never in code)

GitHub Actions secrets on this repo (encrypted at rest by GitHub):

| Secret | Used for |
|---|---|
| `FISH_AUDIO_KEY` | TTS narration |
| `GOOGLE_CLIENT_ID` | YouTube OAuth client |
| `GOOGLE_CLIENT_SECRET` | YouTube OAuth client |
| `YOUTUBE_TOKEN_JSON` | Full OAuth token JSON (upload scope, refresh token) |
| `YTA_PROXY` (optional) | Explicit proxy for the transcribe chain |
| `YTDLP_COOKIES` (optional) | Logged-in cookie jar that softens the bot-wall |

Local-only twin lives outside this repo at `~/.secrets/` — `token.json`,
`client_secret.json` and any key material are gitignored and must never be committed.

## Publishing

`tools/youtube_upload.py` refreshes the OAuth token and uploads via the YouTube Data API
resumable protocol. Every upload must tick **"Altered or Synthetic Content: Yes"** and
follow the monetization guardrails in [`docs/content-strategy.md`](docs/content-strategy.md).

## License

Our code: MIT (see LICENSE). Vendored skills keep their own licenses — see each
submodule. `what-if-animation` and `tool-reel-system`: verify license before any
commercial use (noted in tooling registry).
