# Registry — every skill and repo we build on (verified only)

> Reader: anyone adding a dependency or looking for a capability. Rule Q1
> (L-026): nothing enters this table without a verified GitHub API 200 + a real
> clone/submodule. Rejected names stay at the bottom so we don't re-chase them.
> Supersedes `skills/REGISTRY.md` + `docs/tooling.md` (both archived).

## The active stack (what the daily pipeline actually uses)

| Capability | Where it lives | Status |
|---|---|---|
| Render engine (rig, world, diagrams, captions) | **in-house `engine/*.js`** — ported from `vendor/what-if-animation/studio/src/engine/rig.tsx` (MIT, © 2026 FreshStack), restyled for our cast | ✅ main path |
| 7-beat What-If formula, look/sound/traps references | `vendor/what-if-animation` (submodule @ `8092fb5`) | ✅ backbone |
| Voice (default) | edge-tts `en-US-AndrewNeural` via `tools/vo_pipeline.py` | ✅ keyless |
| Voice (preferred, optional) | Fish Audio s2.1-pro-free via `tools/fish_tts.py` + `.github/workflows/vo-gen.yml` (CI secret) | ✅ daily credits |
| Intent gate / publish bar | `tools/vlm_gate.py` / `tools/ultracritic.py` (+ `ultracritic_video.mjs`, glm-4.6v) | ✅ in-house |
| Audio finish | `tools/finish_v3.py` (numpy-synth bed/SFX, −14 LUFS, pipe-encode) | ✅ in-house |
| Script gates | `tools/script_linter.py` + `prompts/scriptwriter_system.md` + `prompts/critic_system.md` | ✅ in-house |
| Publish | `tools/youtube_upload.py` (OAuth, disclosure automated) | ✅ in-house |
| Hero-shot i2v (free GPU, experimental) | `tools/hero_shot/ai_rerender.py` + `.github/workflows/ai-rerender.yml` (ZeroGPU Wan2.2-Animate anonymous ~160 GPU-s/IP; census `research/anonymous-gpus.md`) | ⚠️ boss-directed experiment — text stamps DRIFT (AGENTS.md §6); never gated/shipped without boss sign-off |
| Research loop | `tools/transcribe.py`, `daily_loop.py`, `blueprint_extractor.py`, `rss_scout.py` + `vendor/Youtube_transcriber` (Whisper fallback) | ✅ CI daily |
| Bot-wall infra | `tools/proxy_pool.py`, `fetch_instances.py`, `vendor/bgutil-ytdlp-pot-provider` (@2.0.2, POT server :4416) | ✅ opportunistic |
| Taste layer (motion QC laws) | `vendor/motionmaxxing` (our fork @ `8c8ec0f`): 12 craft references, ~4,300 measured moves (M913–M974) | ✅ mined into rules |
| Skill library (per-format mining) | `vendor/motion-skills` (our fork @ `bb5a3ce`): 50 skills / 14 packs (kinetic type, data-viz, explainers, WebGL, Manim) | 📌 mine per format |
| Doc/report layer | `vendor/skills` (anthropics @ `ca45fc4`): docx/pdf/pptx/xlsx, canvas-design | 📌 as needed |

## Reference-only vendored (not on the render path)

| Repo | Pinned | What it's for |
|---|---|---|
| `vendor/stickman-video-director` (kaomei, MIT) | `d19705d` | Style breadth reference (6 style systems, storyboard discipline, voice-continuity rules). Its Director/Autopilot modes assume generation tools we don't run — we ported ideas, not the pipeline. |
| `vendor/tool-reel-system` (kelano86) | `33bf721` | Edit formula reference (caption sync, pacing math from 16 top reels). License: verify before commercial use. |
| `vendor/what-if-animation` | `8092fb5` | Also: `references/formula.md` (7 beats), `look.md` (measured genre grammar), `traps.md` (mined into `docs/rules.md` §Scenes + parameters). License: verify before commercial use. |

## Verified & noted (adopt when the stage needs them)

| Repo | Role when adopted |
|---|---|
| `remotion-dev/remotion` | Programmatic video engine — post-day-30 decision only (dead-end D10) |
| `motion-canvas/motion-canvas` | Secondary code-driven engine — same condition |
| `SYSTRAN/faster-whisper` | Local Whisper (already inside the transcribe ladder) |
| `hexgrad/kokoro`, `rhasspy/piper` | Local TTS fallbacks if Fish and edge both die (L-023) |
| `gestura-ai/stick-gen`, `filippocalippo/StykAnimate-App`, `blixvip/stick` | Character animation upgrade path |
| `SamurAIGPT/open-ai-video-agent` | Multi-shot agent orchestration patterns |
| `chroma-core/chroma` | Vector index for blueprints at >50 volume (L-024) |
| `Zulko/moviepy` | Quick chop fallback |
| `imputnet/cobalt` | CLOSED (dead-end D3) |
| Our forks: `Openclip`, `supoclip`, `manimgx`, `unslop`, `teardown`, `claude-seo`, `awesome-claude-skills`, `awesome-video-as-code`, `awesome-ai-motion-graphics`, `awesome-motion-design-agent-skills` | Competitor clip study / math overlays / de-AI pass / SEO / discovery lists |

## Rejected

| Name | Result |
|---|---|
| `motion-dev/motion` ("motion max") | 404 — resolved to motionmaxxing (L-027) |
| y2mate-class downloaders, ElevenLabs production VO | Policy (L-025, D2, D14) |

## Update policy

```bash
git submodule update --remote vendor/what-if-animation
git add vendor/what-if-animation && git commit -m "chore(vendor): bump what-if-animation"
```

Check the upstream changelog first; material changes go into the ledger. Our
forks (motionmaxxing, motion-skills) are updated by pushing to the fork.
