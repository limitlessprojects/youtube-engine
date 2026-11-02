# Tooling Registry — verified repos only

> Rule L-026: no repo enters this table without a verified GitHub API hit (200) and a
> real clone/submodule or documented use. Names suggested by AI chats that failed
> verification are listed under "Rejected" so we don't re-chase them.

## ✅ Vendored as pinned submodules (`vendor/`)

| Repo | Pinned | License | Role in our pipeline |
|---|---|---|---|
| `kaomei/stickman-video-director` | `d19705d` | MIT | Core director: script → multi-style stickman video (science, dark psychology, lore, historical styles). Main render path. |
| `kelano86/what-if-animation` | `8092fb5` | see repo (verify before commercial use) | The 7-beat What-If formula (decoded from 5 scripts across 4 channels), SVG-in-Remotion rendering, storyboard self-check (11-pt), SFX/music pipeline, −14 LUFS mastering. Our format backbone. |
| `kelano86/tool-reel-system` | `33bf721` | see repo (verify before commercial use) | Reverse-engineered reel script formula + frame-by-frame edit teardown (from 16 reels of a 630k AI-tools creator, with view counts). Template for our Remotion edit skill. |
| `Rakile/Youtube_transcriber` | `c5d8f9f` | see repo | **The youtubecheck.** faster-whisper transcription of YouTube/local media → the transcript layer of the whole research pipeline. Python 3.11+, ffmpeg required. |
| `anthropics/skills` | `ca45fc4` | MIT-ish (see repo) | docx/pdf/pptx/xlsx, canvas-design, skill-creator etc. — our doc/report/description generator layer. |
| `limitlessprojects/motionmaxxing` (our fork) | `8c8ec0f` | MIT (see NOTICE) | "Looksmaxxing for motion graphics" — taste studies, runtime rules. Already proven in the ReadAny demo. AKA "motion max". |
| `limitlessprojects/motion-skills` (our fork) | `bb5a3ce` | MIT (see repo) | 50 open-source motion skills / 14 installable packs (kinetic typography, data-viz, explainers, TikTok/Reels, WebGL, Manim). Skill library to draw from. |

## 📌 Verified & noted (adopt when the stage needs them)

| Repo | Status | Role |
|---|---|---|
| `remotion-dev/remotion` | verified 200 | Programmatic video engine (npm dep in render projects; `remotion-dev/skills` also exists for agent skills). |
| `motion-canvas/motion-canvas` | verified 200 | Alternative code-driven motion-graphics engine; secondary renderer for procedural scenes. |
| `yt-dlp/yt-dlp` | verified 200 | Search + (with cookies/proxy) audio & subtitle fetch. The only downloader we use (L-025). |
| `jdepoix/youtube-transcript-api` | verified 200 | Primary caption fetch path; cloud-IP blocks need proxy/cookies (L-031). |
| `SYSTRAN/faster-whisper` | verified 200 | Local Whisper engine inside Youtube_transcriber fallback. |
| `hexgrad/kokoro` | verified 200 | Local TTS fallback if Fish Audio quota/battery runs dry (L-023). |
| `rhasspy/piper` | verified 200 | Second local TTS fallback. |
| `openai/whisper` | verified 200 | Reference model; we use faster-whisper impl. |
| `gestura-ai/stick-gen` | verified 200 | Text→stickman motion generation (poses/velocity). Character animation upgrade path. |
| `filippocalippo/StykAnimate-App` | verified 200 | Open stick-figure animation software w/ IK; procedural rig path. |
| `blixvip/stick` | verified 200 | Stick animation tooling — same family as above; compare and pick. |
| `SamurAIGPT/open-ai-video-agent` | verified 200 | Multi-shot video agent patterns / SKILL.md workflows; mine for orchestration ideas. |
| `chroma-core/chroma` | verified 200 | Future vector index for the blueprint memory bank (L-024) once volume justifies. |
| `Zulko/moviepy` | verified 200 | Python editing fallback for quick chops (Openclip/supoclip use ffmpeg directly too). |
| `imputnet/cobalt` | verified 200 | Clean download frontend alternative (self-host); only if yt-dlp path fails long-term. |
| `limitlessprojects/Openclip` (our fork) | fork | YouTube video → viral clips; competitor clip study tooling. |
| `limitlessprojects/supoclip` (our fork) | fork | OpusClip alternative — clipping pipeline reference. |
| `limitlessprojects/manimgx` (our fork) | fork | Manim API on a Rust GPU core — math/3D explainer scenes when stickmen need physics overlays. |
| `limitlessprojects/unslop` (our fork) | fork | De-AI-ifies vibecoded UI — run on any web-facing studio tooling before we ship it. |
| `limitlessprojects/teardown` (our fork) | fork | 3D simulator skill — possible future "take it apart" video format. |
| `limitlessprojects/awesome-claude-skills` (our fork) | fork | Discovery list — periodic sweep for new skills. |
| `limitlessprojects/awesome-video-as-code` (our fork) | fork | Discovery list for code-driven video tooling. |
| `limitlessprojects/awesome-ai-motion-graphics` (our fork) | fork | Discovery list for motion-graphics skills. |
| `limitlessprojects/awesome-motion-design-agent-skills` (our fork) | fork | GSAP/Motion/Remotion/Lottie/Rive skill lists. |
| `limitlessprojects/claude-seo` (our fork) | fork | Title/description/GEO skills — reuse for YouTube metadata engine. |

## ❌ Rejected / not found

| Name (as suggested) | Result | Note |
|---|---|---|
| `motion-dev/motion` ("motion max") | 404 | Resolved as **motionmaxxing** (our fork, L-027). |

## Rejected tools (policy)

- Web downloaders (Y2mate-class), ad-ware converters: banned from the pipeline (L-025).
- ElevenLabs for production VO: free tier is non-commercial — we default to Fish Audio
  (daily free quota) + local fallbacks. Revisit only with a paid plan and license check.
