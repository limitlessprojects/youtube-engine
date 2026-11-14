# Wan-Animate "replacement showcase" (rep_shots) — Tongyi Lab, Alibaba (replacement demos, ~21.8s)
**Source: humanaigc.github.io/wan-animate (content/aa/rep_shots.mp4, official Wan-Animate project page, Tongyi Lab / Alibaba) · accessed 2026-11-14 · analysis-only**

Local wishlist copy `/home/ryioshi/Downloads/wishlist/VL-16b-wan-animate-rep-shots.mp4` is a **corrupt/unfinalized download** (ftyp `qt  `, no `moov` atom). The official asset is intact; re-downloaded copy `/tmp/opencode/wishlist/frames/VL-16b-wan-animate-rep-shots.src.mp4` (42,183,708 bytes, content-length match) was used for analysis. Wan-Animate demos are Alibaba research demos — **analysis only; frames must never enter renders/uploads**. On-screen text ("Original" / "Generated") is demo chrome, not content.

## 01 Verdict
The reference for our anonymous-ZeroGPU hero-shot route (L-093): character *replacement* in existing film footage — original actor left panel, generated replacement right panel, lighting and environment preserved. This is the strongest public evidence that Wan2.2-Animate-class models hold identity, motion, and lighting match well enough to anchor our hero-shot plan. It is also a cautionary tale: even the official demo ships with visible relighting compromises and it never proves itself without the side-by-side.

## 02 Hook anatomy / opening shot anatomy
- Frame 0 (t=0, hook.jpg): side-by-side 2560×720 split — left panel labeled "Original" (white sans-serif, top-left), right panel labeled "Generated" (top-center-left above right panel). Source film clip: woman in dark blazer in a wood-paneled study/library. Generated panel: same room, same camera, same blocking — woman re-cast as a fair-haired woman in a russet corset/period dress.
- The established information in the first second: **identical room, identical framing, identical blocking; only the person and wardrobe differ.** No title sequence, no branding beyond the two panel labels. The pairing IS the message.
- Second vignette (from ~t=2.2s): man in a suit entering a stately room with onlookers → generated as long-haired leather/fur warrior character; same blocking (hand on doorframe, briefcase). Cuts back to vignette 1 and alternates through the 21.8s runtime.
- Opening with the easier, more static vignette (woman, chest-up, minimal movement) before the harder locomotion+crowd shot is deliberate demo sequencing.

## 03 Craft notes
- Format: **2560×720, two 1280×720 panels side-by-side**, 30fps, h264+aac. No letterbox; panels keep the film's native framing.
- Light: generated panel **matches the source lighting** — warm study lamps on skin (vignette 1), flat institutional corridor light + warm doorway on the warrior (vignette 2). This is the Relighting-LoRA claim made visible: same key/fill ratio, same color temperature, same shadow direction in both panels.
- Contrast/grade: generated panel is graded to sit *inside* the source's filmic contrast (slightly lifted blacks vs source, marginally less crisp — a recurring AI-generation signature: faces slightly softer, speculars flatter).
- Motion register: vignette 1 — micro-motion (speech, brow, breathing, hand on hip); vignette 2 — locomotion (walk-through-door, stride, arm swing, prop carry). The harder vignette is the real benchmark.
- Subject discipline: background actors, room, furniture are pixel-consistent between panels (they are the same plate); only the target character is regenerated — visibly correct compositing discipline.
- Failure modes visible on close look (analysis): minor edge softness/halation around hair and shoulders in the generated panel; slightly plasticky skin highlights in vignette 2; jewelry/buckle speculars less coherent; fine fabric texture (corset lacing) holds up better than expected; background extras remain stock — good (they should be untouched).

## 04 Pacing + cuts
- scene_changes.txt (threshold 0.3): **0 events**; threshold 0.08 also returned no events — the detector is useless on this composition (both panels share layout; vignette switches change large regions but score below threshold, or the switches are whip/dissolve). **Visual frame sampling shows ~5 vignette switches**: woman (t=0) → man (t≈2.2) → woman (t≈6.5) → man (t≈8.7) → woman (t≈15.3) → man (t≈17.4–21.8). Treat the detector count as "0; manual count ≈5", flag as UNKNOWN for exact switch timestamps (±1s from 10-frame sampling).
- Cuts are hard switches between two setups; no fades observed in sampled frames.
- For our pipeline: pairing-composite comparisons defeat naive scene-cut detection — any automated QA that relies on scene_changes alone will misread hero-shot composites; use frame-diff on the subject region instead.

## 05 What maps to our pipeline
For `tools/hero_shot` + the anonymous-ZeroGPU route (L-093), this official demo is the **acceptance spec**:
1. **Side-by-side output is the only credible proof** — our pipeline should emit, per hero shot: (a) clean generated plate, (b) side-by-side vs source clip with panel labels, (c) inset-PiP variant (res921-style) for social/QA. Never publish (b)/(c) as final.
2. **Component isolation** — regenerate ONLY the character; keep the source plate (room, extras, props) byte-identical outside the character matte. Any bleed/flicker outside the matte = fail. Our v1 should measure outside-matte pixel delta; the official demo passes this by construction.
3. **Lighting replication is the hard gate, not motion** — ZeroGPU chunks that produce motion-correct but mis-lit plates are worthless; score "key direction, color temp, contrast ratio vs source" as a first-class ultracritic axis before publish.
4. **Vignette difficulty ordering** — replicate the demo's sequencing: static dialogue coverage first, then locomotion/crowd second. Our first anonymous-ZeroGPU test should be a chest-up static shot (vignette 1 class), not a walk-through-door (vignette 2 class).
5. **Chunking** — 21.8s demo at 30fps = 654 frames; L-093's ≤140 GPU-s per chunk implies ~3–5 chunks per shot; motion-plan chunk cuts on low-amplitude frames (the demo's speech beats), frame-exact reassembly, and verify A/V + identity continuity across chunk seams — this is where anonymous-quota assembly most likely breaks.
6. **Do not copy the demo chrome** — "Original/Generated" labels are QA scaffolding; our published hero shots carry none of it.
7. **Source licensing hygiene** — the demo re-skins *studio film footage*; that is fine for Alibaba's research page, NOT fine for us to redistribute. Our route must use our own source plates (or VL-21/VL-22 PD plates) — never scraped studio clips.

## 06 Judge anchor?
Not as a finished product (it is a research demo), but its frames are the **best available calibration targets for a "character-replacement quality" pass** in ultracritic — if we add such a pass, vignette-1 frames (easier) define the passing floor and vignette-2 frames (harder) define the stretch bar. Run only the generated panels through the critic; feeding the side-by-side composite will confound subject scoring. Expect the critic to over-penalize skin softness; calibrate with the fact that official output is the reference.

## Compliance: Alibaba research demos — analysis-only, not redistributable; no frames used for training/render. No verbatim captions quoted beyond the two panel labels. View counts: UNKNOWN (project page, no counter). Local wishlist file was corrupt (no `moov`); official asset re-fetched under /tmp (not committed), content-length verified. Cut count from scene_changes.txt = 0 (detector unreliable here — documented); ~5 vignette switches by 10-frame sampling, timestamps ±1s UNKNOWN. Source film footage shown in the demo is studio IP — identified by appearance only, not named, and never reused. Exact model checkpoint/LoRA weights UNKNOWN beyond page text (Relighting LoRA, Wan-Animate based on Wan I2V).
