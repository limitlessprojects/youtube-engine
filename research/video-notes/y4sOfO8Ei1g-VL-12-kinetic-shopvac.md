# Shop Vac (kinetic typography animation) — Jarrett Heather (for Jonathan Coulton) (~1.74M views per wishlist brief, 206s; upload 2010-11)
**Source: youtube.com/watch?v=y4sOfO8Ei1g · accessed 2026-11-14 · analysis-only**

## 01 Verdict
The reference for word-level kinetic type: every lyric line is a designed composition, not a caption — type IS the scene, the illustration is the set dressing. Motion vocabulary (zoom-push, radial spin-in, mirrored flip, parallax slide, star-wipe slam) is exactly the toolset for our title-slam / stamp beats.

## 02 Hook anatomy / opening grammar (first 2 seconds)
- t≈0.0–1.5s: dark-red vignette field, small amber italic "JONATHAN COULTON" top-center; a single white lowercase "sh" punches in bottom-left and grows to full "shop vac" slab-serif by t≈2s (f00→f02→sv_2.jpg). No logo sting, no channel card.
- Grammar: artist-credit line small + title line HUGE, two-word max, one accent color (amber on deep red). The type arrives word-by-word on the downbeat — the promise is "watch the words perform."
- Retention driver: information gap is lyric-vs-image mismatch — mundane suburban imagery (lawn, tissue box, sheet music) played against mounting existential dread; the viewer stays to see what the next line LOOKS like.

## 03 Craft notes: motion vocabulary (cite timestamps)
- **Ease/overshoot/settle**: type enters with hard ease-out + motion blur (sv_12.jpg "DRIVEWAY" streaks in with radial blur smear; sv_20.jpg "VERY OWN" slides on a diagonal blur trail) — fast in, dead-stop settle, hold, then hard cut. No floaty drift.
- **Squash on slam**: star graphic at sv_28.5s bursts outward with heavy motion blur and a word clipped by the star shape — impact frames carry 2–4 frame blur, then freeze clean.
- **Mirrored/inverted type**: f03.jpg shows a two-line headline with the second line flipped vertically (mirror-reveal gag) — type as spatial object, not layout text.
- **Perspective floor type**: sv_6.jpg "TOWN OF" set in true 3D perspective on a road plane with lane markings receding — type locked to a world plane, parallax with the camera push.
- **Illustrated diagram plates**: f05.jpg / f09.jpg tissue-box "exploded view" with dotted leader lines, corner callouts, "YOU CAN CRY" ribbon — motion-graphics infographic grammar; f06.jpg sheet-music plate with chord symbols (B7 E B7) — the lyric rendered as artifact.
- **Color discipline**: one saturated field per plate (forest green, deep red, mustard cream, oxblood, navy vignette, purple) — never more than 2–3 hues + cream type per frame; vignette on everything; grain/textured paper backgrounds.
- **Type discipline**: condensed heavy sans/slab for headlines, small grotesque for captions; mixing of italic small-caps credit vs all-caps hero lines; kerning/leading are part of the animation (letters arc along a dial sweep at f01.jpg — characters placed on a circular path and revealed sequentially).
- **Chart-like motion**: f01.jpg gauge/dial with letters "…ING FOR" riding the arc — word-on-path reveal synced to a needle sweep.
- 2010-era After Effects + Illustrator/Photoshop pipeline (per public descriptions); 854×480/30fps master here is the f397 re-encode.

## 04 Pacing + cuts
- scene_changes.txt: **15 detected changes** (28.46, 28.50, 28.53, 34.27, 34.43, 35.30, 43.18, 72.21, 100.77, 170.57, 172.61, 176.24×3, 184.25); shots = 16, mean 12.9s, but the detector misses intra-plate type re-animations (kinetic plates re-layout words every beat). True perceptual cut/re-layout density is far higher — roughly every 2–4s a new type composition lands.
- No audio track in the .f397 master (silent); it's a lyric video for a ~3:26 song, so rhythm is musical (≈4/4, ~120bpm feel). WPM not measurable from vtt (absent); lyric density ≈ normal song cadence.
- Structure: hook (credit+title) → verse plates (suburban set-dressing) → chorus slam (star/red) → bridge (diagram plates) → out. Visual energy tracks the song's dynamics, not a uniform grid.

## 05 What maps to our pipeline
- **Tween curves** (`engine/core.js:25-43`): we have `easeIn/easeOut/easeInOut` (cubic) and `V2.settle` (damped sine). Shop Vac shows we should add an **overshoot-out** (back-out, ~1.7–2.0 overshoot) specifically for type slams, and use `V2.settle` on the landed word (amp 4–8px, decay ~6) rather than a binary stop — our C5 "no snap-cut" is satisfied by overshoot+settle, not by slow fades.
- **Title-slam beats** (`tools/finish_v3.py` — "thump — soft stamp impacts at word-timed card beats"): the shopvac slam is the visual twin of finish_v3's thump class. Proposed: a `stamp` visual directive in scenes.html — word scales 1.35→1.0 with 3f motion blur → 2f overshoot → settle, paired with the thump SFX at the same word timestamp.
- **Word-on-path reveal**: arc/dial-path word reveals (f01.jpg) could be a `typePath` directive for hook cards; cheap in canvas (rotate per glyph around a pivot).
- **Mirrored/flip line**: the f03.jpg mirror-flip is a one-line canvas transform (scaleY -1 → 1 with easeOut) — adopt as a transition taxonomy entry `flipReveal`.
- **Transition taxonomy for `tools/render_short.py` scenes**: {hard cut, eased slide-in, slam+overshoot, star/shape wipe, perspective plane push, diagram-plate swap}. Today C5 enforces breathe (ease-in ≥0.25s → hold ≥0.5s → ease-out); shopvac adds that **incoming** type may arrive fast (≤150ms) IF it settles with overshoot — i.e., split C5 into IN (fast+overshoot OK) vs OUT (ease-out ≥0.25s mandatory). This is a concrete C5 amendment to propose, not change unilaterally.
- **Style bible §6 (motion)**: add "word-level slam grammar" — type as hero object with rim/gradient/vignette discipline already in bible §2; the shopvac plates validate bible's "one accent field per scene" rule (§1) at full saturation.
- **Hook calibration** (`tools/probe_hook.py`): our probes score hook_impact on stills; a shopvac-style hook (tiny credit + huge two-word title, word arriving on beat) is a missing archetype between "full-text card" and "pure image." Add as a labeled probe candidate class.
- Concrete engine changes: (1) add `V2.backOut(t, s=1.70158)` to `engine/core.js`; (2) add `stamp` + `flipReveal` + `typeArc` directives to the scenes.html spec; (3) finish_v3: couple `thump` SFX to `stamp` directive timestamps automatically; (4) lint: new warn if a `stamp` lands off-beat vs VO word grid (needs word timestamps — ties to L-097 beat law via the VO ladder).

## 06 Judge anchor?
Yes for **motion craft / title design** dimensions, not for palette: his fields are saturated vintage poster colors, ours are deep-space nebula (bible §1). Use as reference for `pacing_rhythm` and type-impact, never as a palette or grade anchor. Would not pass our gate as a frame (not our style), but the frame at sv_2.jpg would score well on hook_impact text-hierarchy.

## Compliance: no verbatim quotes >50 words (none quoted). Views ~1.74M per wishlist brief (CreativeBloq-listed); exact count UNKNOWN. No vtt for this .f397 master — lyric content paraphrased from frames. "Jarrett Heather" as animator per public sources; single-author credit on the video UNKNOWN. Scene-change count from automated detector (15); intra-plate re-layouts not counted — true density higher, UNKNOWN precisely. "~120bpm" is impression, UNKNOWN. 854×480 frames upscaled for inspection only.
