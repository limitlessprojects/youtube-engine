# What if Germany Won WWI? (Part 1) — AlternateHistoryHub (~7.9M views, 492s)
**Source: youtube.com/watch?v=MQW3VefRozc · accessed 2026-11-14 · analysis-only**

## 01 Verdict
The what-if spine done as a history lecture with a map: divergence point → treaty dominoes → one pivotal military decision → alternate timeline escalation. Weak on motion craft, strong on *structure* — this is the template shape for our #0001-style counterfactual topics.

## 02 Hook anatomy
- Frame 0 (hook.jpg / f00, t≈0s): pure black. Opens on **period music** — "Johny Get Your Gun" marching-song over black for ~8 seconds before any narration. A deliberate "we are inside 1914" time-machine cue.
- Frame 1 (f01, t≈?): white-on-black map of Europe with a small Imperial-Germany flag pinned on Berlin and a faded archival-photo inset top-right — the promise: *this is a map-driven alternate history, not a lecture with talking heads.*
- Frame 2 (f02): map zooms to the Western Front — a red line bisecting the France/Germany border (the Schlieffen-plan corridor). The divergence geography is drawn before it's spoken.
- Frame f04: full-screen archival film-grain (vertical scratches, dust) — texture as "old footage" signifier.
- Frame f07: ornate vintage film-frame border with tilted imperial flags — silent-film title-card pastiche.
- Frame f09: end screen with "subscribe" + cross-promo (not part of hook).
- Title promise: "What if Germany Won WWI? (Part 1)" — direct counterfactual question. Audio open (after march): "what if in an alternate timeline Germany and the Central Powers won World War I — let's go back to 1914 with the assassination of…" — states the divergence point inside ~60s.
- What frame 0 promises in the first 2 seconds: *period immersion + a question the video will answer*; the black + march says "history, but wrong."

## 03 Craft notes
- Palette: archival monochrome (sepia/grayscale photos, film grain, vignette, rounded-corner frames) against stark white-map/black-ocean cartography with a single red accent line (the front) and small grayscale flag icons. Utilitarian, not beautiful — the aesthetic is "documentary dossier," deliberately opposite to Kurzgesagt polish.
- Parallax/depth: essentially flat 2D maps with slow Ken Burns zooms/pans; archival photos with corner-pin tilts; no layered depth planes, no character rigs.
- Detail density: maps are simplified (borders only), flags are low-res; interest comes from *information* (borders, front line, flag placements), not rendering.
- Motion grammar: slow zooms toward the relevant border/region; hard cuts between map states, photo stills, and section title cards; grain overlay unifies everything.
- Character work: none — no characters; "actors" are nations as flag icons and archival crowd/soldier photos.

## 04 Pacing + cuts
- Cut count (scene_changes.txt): **134 detections** over 492s — very high for a "static map" video; many are photo/grain/title-card swaps. Mean shot length ≈ **3.7s**.
- WPM: ~5,730 raw VTT tokens / ~1,257 deduplicated words ÷ 8.2 min ≈ **~150 WPM** — lecture cadence with music intro padding. (Karaoke VTT deduplicated; approximate.)
- Attention control: 3–4s cut rhythm + map zooms + a relentless question engine ("what if…?", "what would this look like?"). No moment is allowed to sit still; the grain + march bed keep energy up despite zero animation.

## 05 What maps to our pipeline
- **THE WHAT-IF SPINE (the deliverable for our #0001-style topics):**
  1. **Frame 0 immersion** — black + period cue (music/texture) before any words. Our pipeline can do this today: `tools/finish_v3.py` already synthesizes a bed; GAP: no "period cue" library or per-video music selection — everything gets the same Aadd9 pad.
  2. **State the real timeline first, fast** — 1914, Franz Ferdinand, the alliance dominoes, the one decisive decision (Belgium/Schlieffen). One sentence per domino, map zoom per domino. Our `engine/diagram.js` + `engine/world.js` can render map-state beats; GAP: no map asset pack (Europe 1914 borders, flags) in assets; our Krakatoa world tokens are terrain, not cartography.
  3. **Identify the single pivot** — the video stakes everything on ONE decision (invading Belgium → British entry). Our script templates should force a "one pivot" beat; GAP: `script_linter.py`/`content/` has no counterfactual beat sheet (divergence → pivot → domino chain → escalation → "this is one scenario" hedge).
  4. **Domino chain** — Belgium → Britain → two-front war → 1917 crisis (Russia exits, France nearly breaks, US barely enters). Each domino = one visual state change.
  5. **Escalation into the alternate** — "Germany keeps Alsace-Lorraine, reparations on France, aristocratic monarchies survive, a German-led 20th century without Nazis." Escalate consequences across domains (military → political → ideological → economic), each with a map/flag/photo beat.
  6. **Hedge/close** — "this is one scenario… this is Cody of Alternate History Hub." A one-line epistemic hedge before the outro protects credibility.
  7. **Part 1 cliffhanger + cross-promo end screen** — series architecture; GAP: our pipeline has no series/part structure or end-screen cross-promo templates.
- **tools/finish_v3.py**: his grain/vignette/period-frame grade maps to our "subtle grain + vignette over the final grade" step — we already do this; GAP: no archival-frame overlay, no film-grain-per-scene intensity control.
- **engine/diagram.js**: maps to our diagram beats; GAP: no animated border-draw or red-front-line reveal primitive.
- **gate/**: his video would FAIL our G9 detail-density and likely motion-grammar checks — it is a slideshow with music. It passes on *structure* alone. Lesson: our gate measures craft, not spine; the spine lives in the script, which our gate does not score. GAP: no "narrative spine" rubric dimension in ultracritic.
- **render_short.py**: 492s long-form; for our shorts, compress spine to: 0–2s black+cue → divergence in one line → pivot → 2–3 dominoes → one-line alternate outcome. Repeatable for #0001-style topics.

## 06 Judge anchor?
No as a craft anchor (fails G9/motion). Yes as a *structure* reference for counterfactual scripts — but our ultracritic has no dimension that rewards it, so it would score ~5–6/10 on craft dims while being strategically the most useful video in this tier for topic architecture. Would not clear 7.5/7.0 as a frame judge.

## Compliance: analysis-only; quotes ≤12 words; cut count from scene_changes.txt (134); views/durations from wishlist brief. UNKNOWN: exact upload date, Part 2 existence/performance, whether maps are licensed assets, precise per-frame timing of map zooms.
