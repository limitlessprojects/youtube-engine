# The 13-Skill Stack

> The active stack for the channel. Sources verified 2026-11-02 (L-026: every entry
> has a 200 + a real clone). Vendor code lives in pinned submodules under `vendor/`.

| # | Skill | Source (pinned) | What it does for us | Status |
|---|-------|-----------------|---------------------|--------|
| 1 | **stickman-video-director** | `kaomei/stickman-video-director` @ `d19705d` | Script → multi-style stickman video (science / dark-psychology / lore / historical styles). Main render engine. | ✅ submodule |
| 2 | **what-if-animation** | `kelano86/what-if-animation` @ `8092fb5` | The 7-beat What-If formula, SVG-in-Remotion frames, storyboard + 11-point self-check, SFX pipeline, −14 LUFS master. Format backbone. | ✅ submodule |
| 3 | **tool-reel-system** | `kelano86/tool-reel-system` @ `33bf721` | Codified script + edit formula from 16 top AI-tool reels (view counts attached). Template for our edit skill. | ✅ submodule |
| 4 | **Youtube_transcriber** | `Rakile/Youtube_transcriber` @ `c5d8f9f` | **The youtubecheck**: faster-whisper transcription of competitor/local video → transcript layer. | ✅ submodule |
| 5 | **motionmaxxing** ("motion max") | our fork @ `8c8ec0f` | Taste layer: turns AI-slop motion into designer-grade films. Rules already proven on the ReadAny demo. | ✅ submodule |
| 6 | **motion-skills** | our fork @ `bb5a3ce` | 50 skills / 14 packs: kinetic typography, data-viz, explainers, Shorts/Reels, WebGL, Manim. Skill library. | ✅ submodule |
| 7 | **anthropic skills** | `anthropics/skills` @ `ca45fc4` | docx/pdf/pptx/xlsx + canvas-design + skill-creator: metadata pages, thumbnails briefs, reports. | ✅ submodule |
| 8 | **Remotion** | `remotion-dev/remotion` (npm) | Programmatic video assembly for all rendered scenes. | 📌 noted |
| 9 | **Manim GX** | our fork `manimgx` | Rust-GPU Manim for physics/math overlay scenes. | 📌 noted |
| 10 | **Fish Audio TTS** | in-house `tools/fish_tts.py` | s2.1-pro-free narration, daily free quota; ~2.6 words/s measured. Local fallbacks: kokoro, piper. | ✅ in-house |
| 11 | **VLM Inspector** | in-house `prompts/vlm_inspector.md` | Scene-by-scene frame QC with bbox offsets, N=2 re-render cap. | ✅ in-house |
| 12 | **Openclip** | our fork `Openclip` | Competitor video → study clips for shot-level analysis. | 📌 noted |
| 13 | **unslop** | our fork `unslop` | De-AI-ifies vibecoded UI — used on any studio tooling before it ships. | 📌 noted |

## Lineage — how the stack improves on each part

- `what-if-animation` gives the **story spine** (7 beats, one rig = zero character
  drift) → `stickman-video-director` gives **style breadth** (multi-genre visual
  systems) → `motionmaxxing` + `motion-skills` give the **taste ceiling** and motion
  QC → `tool-reel-system` contributes the **edit format** (caption sync, pacing math)
  → Remotion/Manim are the **render substrate** → `Youtube_transcriber` + blueprint
  extractor close the **learning loop** from competitors → anthropic skills handle
  the **paperwork layer** (metadata, thumbnails briefs) → unslop keeps anything
  user-facing from looking machine-made.

## Update policy

```bash
git submodule update --remote vendor/what-if-animation   # pull upstream skill
git add vendor/what-if-animation && git commit -m "chore(vendor): bump what-if-animation"
```
Check each upstream's changelog before bumping; note material changes in the ledger.
