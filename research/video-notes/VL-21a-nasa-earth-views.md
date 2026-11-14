# Earth Views from the ISS — NASA (ISS crew Earth-observation footage, ~200.8s)
**Source: NASA ("Earth Views from the ISS" compilation, NASA-produced, public domain) · accessed 2026-11-14 · analysis-only**

File: `/home/ryioshi/Downloads/wishlist/VL-21a-nasa-earth-views.mp4` (55 MB). NASA-produced footage is a **public-domain work of the US federal government (17 U.S.C. §105)**; usable in renders with courtesy "NASA" line. One frame set appears to include an ISS robotic arm (Canadarm2) and Soyuz/Progress modules — hardware names are facts, fine.

## 01 Verdict
Long-take, near-zero-cut orbital footage: Earth limb, cloud decks, coastline, ISS structure against the black — the definitive PD source for our "space feels real" hero shots, C14 asset variety (Earth plates), and C17 space-topic accuracy.

## 02 Hook anatomy / opening shot anatomy
- Frame 0 (f00 / hook.jpg, t≈0): **black frame with faint gray text** "That's here. / That's home. / That's us." (small, low-contrast, centered-left). A quiet, literary text cold-open — not a NASA original card, likely the compilation's own intro; treat the text card as compilation-specific styling, not NASA house style.
- f01 (t≈20s): top-down nadir view over a rugged cloud-covered coastline (ocean dark, land mass bright) — first "wow" plate.
- f02 (t≈40s): **Earth limb from ISS altitude** — thin blue atmospheric glow arc, cloud swirls below, black above. The hero composition.
- f05 (t≈100s): ISS hardware (Soyuz modules + solar arrays) framed against the limb with a distant vehicle/craft in the black — scale-establishing shot.
- f07 (t≈140s): Canadarm2 + payload against Earth — technology-vs-planet juxtaposition.
- f08 (t≈160s): sun on the limb — starburst/lens flare with horizon glow, ISS truss silhouetted.
- Note: opening black card means a viewer expecting spectacle waits ~10–20s; do NOT copy the slow open — borrow the plates, not the pacing.

## 03 Craft notes
- Light: single dominant source (sun), hard shadows, Earth as bounce fill; ISS modules lit flat-white, gold foil/MLI glints.
- Contrast: abyss-black space vs clipped cloud whites; limb glow as natural gradient (deep blue → cyan → white at terminator).
- Motion register: **orbital drift** — the Earth glides slowly through frame; station/camera micro-jitter; no motivated camera moves. Time-lapse feel without cutting.
- Subject discipline: Earth and station only; no crew faces, no UI overlays (compilation text cards aside).

## 04 Pacing + cuts
- scene_changes.txt at threshold 0.3: **0 entries** — effectively zero hard cuts across ~200s (long uninterrupted takes; any cuts are below the 0.3 threshold or the file is one continuous orbit pass with dissolves; UNKNOWN whether gentle dissolves exist below threshold — f00 is black, so at least one fade exists).
- Content for C14 asset pool (timestamps approximate, from 10-frame sample):
  - ~0–20s: black title card / fade-up (skip)
  - ~20–40s: nadir coastline + cloud-deck plates
  - ~40–80s: Earth limb + atmosphere glow plates (f02-type), high-altitude cloud textures
  - ~80–120s: ISS modules/solar arrays vs limb (f05-type), docked vehicles
  - ~120–160s: Canadarm2 + payload (f07), stations hardware close passes
  - ~160–200s: sun-strike on limb / flare plates (f08), then fade to near-black (f09)
- If we cut this into our pipeline, each plate yields 5–20s of usable hero background/plate footage.

## 05 What maps to our pipeline
- **Hero shots**: limb-glow (f02) and sun-strike (f08) are the two compositions to replicate in `tools/hero_shot` tests — limb gradient is a grading target; sun-strike tests emissive + flare handling in i2v.
- **C14 asset variety**: direct PD plates for Earth/space B-roll under our #0001 lineage; cuts cleanly into Remotion/ffmpeg composite layers; desaturate/grade to our deep-space bible without fighting compilation styling (plates are neutral NASA camera originals).
- **C17 accuracy**: orbital mechanics look — Earth drifts, doesn't pan; clouds have parallax against station at different rates; limb glow is atmospheric scattering (thin), not a thick "atmosphere wall"; station-mounted shots always include structure or hardware. Use these to veto any Krakatoa/space hero-shot draft that looks like a Hollywood "space ocean".
- **License note**: NASA = PD (17 U.S.C. §105), courtesy line "NASA"; no attribution legally required, courtesy expected; compilation text styling ("That's here…") is likely not NASA house style and should not be copied verbatim into our videos (also avoid the quote).

## 06 Judge anchor?
Yes, partially — limb-glow and coastline frames are excellent **hero-test images** through ultracritic for "composition/depth/scale" axes. They will fail "palette consistency" against our deep-space bible unless graded (they read cool-bright/natural), so use as composition anchors, not palette anchors. Passes the 7.5-ish bar easily on clarity/subject; use for critic calibration on space scenes.

## Compliance: NASA PD note above. Text card words not transcribed beyond short phrase reference; the compilation's authorship (NASA vs third-party assembler) is UNKNOWN — intro card styling suggests a third-party compilation of NASA clips; treat each plate as NASA PD but verify the specific clip provenance (NASA archives: nasa.gov image/video library) before on-screen attribution wording. View count UNKNOWN. No verbatim quotes >50 words.
