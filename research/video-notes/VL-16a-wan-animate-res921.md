# Wan-Animate res921 — Tongyi Lab, Alibaba (acting/performance example, 5.7s)
**Source: humanaigc.github.io/wan-animate (content/aa/act/res921.mp4, official Wan-Animate project page, Tongyi Lab / Alibaba) · accessed 2026-11-14 · analysis-only**

Local wishlist copy `/home/ryioshi/Downloads/wishlist/VL-16a-wan-animate-res921.mp4` is a **corrupt/unfinalized download** (ftyp `qt  `, `mdat` with a 8-byte placeholder size, **no `moov` atom** — ffprobe fails, frames empty). The official site asset is intact; re-downloaded copy at `/tmp/opencode/wishlist/frames/VL-16a-wan-animate-res921.src.mp4` (4,572,037 bytes) was used for frame analysis. Notes below from that copy. Wan-Animate demos are Alibaba research demos — **analysis only, never redistributable in our renders**.

## 01 Verdict
The canonical "input→output pairing" reference for character retargeting: a small driving-performer inset composited top-left over the generated character, same motion, same timing, same filmic grade. This is exactly the pairing discipline our anonymous ZeroGPU hero-shot route (L-093) must reproduce for QA, not for publication.

## 02 Hook anatomy / opening shot anatomy
- Frame 0 (hook.jpg, t=0): the generated character (blond/light-brown-haired man, dark overshirt over grey button-down, standing in a sunlit white hallway) already mid-gesture, arms thrown wide, mouth open — **starts in motion, no title card, no fade-in**.
- Top-left inset (every frame): the driving source — a performer in a teal/green polo + khaki pants against a near-black backdrop, shown **front view and back view side-by-side** in the inset. The inset is present from t=0 and never leaves.
- Motion established in the first 0.5s: expansive two-arm gesture synced 1:1 between inset and main frame; the information the viewer needs ("the small guy drives the big guy") is conveyed by simultaneity, not text.

## 03 Craft notes
- Light: warm directional sunlight through hallway windows, hard-ish key from frame-left, high-key interior with deep ambient falloff to the right; the generated subject sits inside a **photographic lighting environment**, not a flat studio.
- Contrast: soft filmic rolloff, muted greens/browns in clothing, specular window glare in background; grade reads "indie film still", not "AI demo reel".
- Motion register: whole-body large-amplitude acting (arm spread, torso twist, head turn, hand articulation) — the hard case for retargeting (fingers, hands, turns).
- Subject discipline: one character, one static-ish generated environment; the generated camera does NOT cut — it holds a medium shot and lets the performance carry.
- Inset discipline: fixed size, fixed position (top-left), same aspect in every frame; the driving feed is visually "raw" (dark backdrop, flat light) vs the generated feed's warm cinematic grade — deliberate contrast that reads as source→render.

## 04 Pacing + cuts
- Hard cuts detected: **0** (scene_changes.txt empty; single continuous 5.67s take, 720p30, h264+aac).
- The "cut" in this demo is implicit: none. All comparison happens spatially (inset vs main), not temporally.
- Duration ~5.7s — short-loop asset; the official page shows it in a 3-up column row with sibling acting examples (res10, res1311…).

## 05 What maps to our pipeline
For VL-16 / `tools/hero_shot` + anonymous ZeroGPU route, the official demo defines the **minimum QA contract**:
1. **Side-by-side (or PiP) input→output proof, same instant in time** — our pipeline must always emit the driving clip and the generated clip time-aligned, plus a composite with the driving feed inset top-left exactly like res921. Any hero-shot artifact we can't show this way is not verifiable.
2. **Temporal alignment at 30fps, no drift over ≥5s** — res921 holds sync across arm-spread → turn → hand-out gestures; our ZeroGPU chunks (≤140 GPU-s per L-093) must be motion-planned so chunk boundaries land on low-motion frames, then frame-exact assembly must restore continuous sync — otherwise the pairing proof breaks.
3. **Static generated environment** — the demo generates the character into a fixed scene; we should likewise keep hero-shot backgrounds static (or extremely slow push-in) in v1; camera motion amplifies retarget artifacts.
4. **Driving feed requirements** — performer against a plain/dark backdrop, full body visible, both front and rear angle helps the model; our VL-18 "you performing one clear action against a plain wall" source is the right shape; res921 validates that a single frontal performance is already sufficient for convincing retarget when amplitude is large.
5. **Grade matching** — the generated feed adopts the target scene's lighting; our route must replicate via Relighting-LoRA-style finishing or post grade, and our ultracritic should check "subject lit consistently with scene" as a scored axis.
6. **Do not ship the pairing composite** — the inset is QA scaffolding; our published hero shots are the clean generated plate only.

Beauty/identity note: the demo preserves the generated character's face across the gesture (no identity drift visible at this length/resolution) — our acceptance bar for a first anonymous-ZeroGPU hero-shot test should be "no visible identity drift over 5s at 720p", matching this reference.

## 06 Judge anchor?
Not directly (it is a model demo, not a finished short), but its **frames are usable calibration material**: the generated plate frames (hallway, warm light) are decent hero-shot style references; the inset composite is a poor judge image (utilitarian PiP). If fed through ultracritic, expect pass on subject/lighting coherence, fail on "finished-film polish". Use as a **pipeline QA fixture**, not as a style anchor for final renders. Definitely not a PD/public asset — analysis only.

## Compliance: no verbatim text from the video was needed (no on-screen text); official page caption paraphrased; Alibaba demo used for analysis only — frames from it must never enter renders/uploads. View counts: UNKNOWN (project page, no public counter). Source file integrity note: original wishlist download was truncated and silently missing `moov`; the official asset was re-fetched for analysis on 2026-11-14 and stored only under /tmp (not committed). UNKNOWN: exact model variant (page implies Wan-Animate/Wan2.2-Animate), relighting LoRA details beyond the page text.
