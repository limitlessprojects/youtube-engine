# Video wishlist — intake log & analysis synthesis (2026-11-14, day-017 session A)

Boss-ordered research pass on `/home/ryioshi/Downloads/video-wishlist.md` (v1, boss,
"we also aim on our mission to learn — send me the list of videos you'd want me to download").
Purpose: calibrate our hook/pacing/motion/structure against the field before authoring #0006,
closing the carry_r10 video-VLM calibration debt one level deeper (we study with our own eyes now).

Everything below is **analysis-only** (nothing from the corpus is ever composited into a
published Short; NASA/USGS PD is the only render-eligible class, with attribution courtesy line).

## Intake status (22 IDs)

| ID | What | Status | Note file |
|---|---|---|---|
| VL-01..05 | Zack D. Films Shorts (stitches 255M, splinters 216M, McFlurry 167M, blood vessels 157M, ancient armor 157M) | ✅ done | c5G_25dhoeU-VL-04, ciIAcD4eXsI-VL-05, rRAmNz6G3Tk-VL-03, ttuKeS5k4Uo-VL-01, yGw0nhlUtkQ-VL-02 |
| VL-06 | Kurzgesagt "The Egg" (36M, 486s) | ✅ done | h6fcK_fRYaI-VL-06-kurzgesagt-egg.md (G9 ceiling anchor) |
| VL-07 | AlternateHistoryHub WWI Pt.1 (7.9M, 492s) | ✅ done | MQW3VefRozc-VL-07-althistoryhub-wwi.md (what-if spine template) |
| VL-08 | Kurzgesagt "1200 Hours" (9.1M, 408s) | ✅ done | uFk0mgljtns-VL-08-kurzgesagt-1200-hours.md (studio pipeline vs ours) |
| VL-09 | Gunner '22 showreel | ❌ blocked (status + routes tried: `BLOCKED.md` §VL-09) | analysis burden: boss's direct MP4 or vimeo login |
| VL-10 | Buff Motion 2025 showreel | ✅ done (3 files, 2160p downloaded; only showreel analyzed in depth) | VL-10a-buff-showreel-1.md |
| VL-11 | Ae Genius easing curves (97.5k, 588s) | ✅ done (re-downloaded after 429 flap) | 6zrEKEuJGKs-VL-11-ae-genius-easing.md |
| VL-12 | Kinetic "Shop Vac" (1.74M, 206s) | ✅ done | y4sOfO8Ei1g-VL-12-kinetic-shopvac.md |
| VL-13 | Every Frame a Painting: editor 2.8M + Edgar Wright 11.4M | ✅ done (both) | 3Q3eITC01Fg-VL-13a-everyframe-editor.md, 3FOzD4Sfgag-VL-13b-everyframe-edgar-wright.md |
| VL-14a/b/c | MinuteEarth (nuclear 23.3M, Grolar 2.87M, sunsets 169k) | ✅ done (sunset = our #0003 A/B) | nGutkWaXDUs-VL-14a, ZA4OQ-1ahXg-VL-14b, 9PJvV5PYDm0-VL-14c |
| VL-15a/b/c | MinutePhysics (2+2, portals cube, backwards) | ✅ done | 0fV8kYoGDNM-VL-15a, 31kyER-8dak-VL-15b, sEQvDbyFNbo-VL-15c |
| VL-16 | Wan-Animate official demos (res921 + rep_shots) | ⏳ frames extracted, notes pending (subagent running) | — |
| VL-17 | r/comfyui Wan 2.2 Animate thread | ❌ blocked (status + routes tried: `BLOCKED.md` §VL-17) | needs boss/reddit token or thread paste; community-intel.md marks findings CANDIDATE |
| VL-18/19/20 | boss phone clip; style-anchor Shorts; PD picks | ⏳ pending boss | — |
| VL-21 | NASA PD: Earth views (200s) + Rocket Lab PREFIRE (51.5s) | ✅ done (PD) | notes pending (same subagent as VL-16) |
| VL-22 | USGS PD: Kilauea lava fountain (2.5M, 121s) | ✅ done (PD) | notes pending (same subagent as VL-16) |

Raw videos live in `/home/ryioshi/Downloads/wishlist/` (kept OUT of git), captions as `.en.vtt`
beside them, frames+cut maps under `/tmp/opencode/wishlist/frames/`.
**Full cleansed transcripts of 17 items with per-word counts + WPM → `research/transcripts/INDEX.md`.**

## Synthesis — what the field is doing vs what we're doing

**Hook anatomy (the frame-0 lesson, across Zack/Kurzgesagt/MinutePhysics):**
- Zack: spectacle first, zero text on t=0 (raw wound fills frame) — curiosity gap, ~149–181 WPM,
  mostly continuous takes; body-interior "gross but educational" is his highest-view lane.
- Kurzgesagt The Egg: audio-led hook (black frame + second-person VO; zero visuals) — our gate
  must never penalize audio-led opens (vlm_gate assumed visual hook; this is its weakness).
- MinutePhysics: blank-page cold-opens + audio-led; black ink + lined paper + ≤2 accents.
- MinuteEarth: stakes-ladder + archival-payoff hybrid; name-swap puzzle (Grolar) is the best
  sub-30s WPM calibration in the set (~197 WPM).
- All top-performers resolve the same tension the same way: **the image (or voice) poses the
  question; text serves motion, not the hook.** Our recent Shorts lean on stamp text to carry
  the frame-0 — the corpus says invert that when the visual can.

**Pacing / WPM (hard data):**
| channel | WPM | MSL | our ~200 band? |
|---|---|---|---|
| Zack | ~149–181 | single-take | below ours |
| MinuteEarth | ~125–197 | 2–8s | straddles |
| MinutePhysics | ~236–251 | continuous | above ours |
| Kurzgesagt | ~110 | ~11.3s long-take | way below |
| us (#0003 etc) | ~200–214 | 12 beats, 3.2s law | ours |
Implication: our ~200 WPM band + 3.2s beat law is fine, but clarity-first topics (ours!) work at
~150–180 WPM. L-097 stands (contexts differ); the A2 belief-correction blank-page pattern is a
strong#0006 candidate format (premise → contradiction → resolution).

**Craft / motion vocabulary (study picks):**
- Shop Vac kinetic type = word-as-object (slam+overshoot, arc-path reveals, one field per plate) →
  adopt `V2.backOut`/`backIn`-style easings for stamp hits (Ae Genius ladder: backOut, easeOutQuint,
  3-key f3; C5 "no creases" rule confirmed).
- EFP Editor = cut on eye/pose change; emotion earns screen time (build→release beat-shape) →
  advisory layer on top of L-097 (v1 uniform floor stays; build-up beats may breathe).
- Buff Motion: 47 shots in 50s ≈ 1.07s MSL with one deliberate ~4.5s hold + seeing them
  single-field plates read at Shorts scale; adopt notchWipe/flashCut taxonomy + one-hold-per-15s
  (NOT the agency cold-open).
- Edgar Wright: hold-then-cut for the payoff ("setup → shortest insert → over-hold the result") →
  deadpanHold on insight beats, max 1 per Short.

**Structure templates worth stealing:**
1. Belief-correction (MinutePhysics): blank page → premise → contradiction → resolution — direct
   #0006 skeleton for "Everyone says X is true" hooks.
2. What-if spine (AlternateHistoryHub): divergence → dominoes → escalation, ending on "one
   scenario" hedge — for #0001-style topics.
3. Name-swap puzzle (MinuteEarth Grolar): question via naming ambiguity — clean for Short hooks.
4. Two-register palette switch (Kurzgesagt Egg): cosmic world ≠ human world, strictly alternate —
   maps to our world-token system; proposed `register: cosmic|earth|sea` scene flag.

**Community & science-lit (`community-intel.md`, 25KB, 12 verified arXiv papers + OA meta):**
VBench/++/2.0 vocabulary for our gate dims (subject consistency, flicker); Sci-VBench — perceptual
quality clusters by model but scientific correctness does NOT (our rubric-judge is validated;
fact-check stays mandatory); Reel Deal (N=62)/PaperTok — short explainers win; TED clarity
(β=0.339 likes) — clarity-weighted hooks; Heliyon PRISMA 40-study microlearning review anchors
retention. Reddit digest: AR-matched inputs; 468×848/832×480 sweet spots; frames-skip=0;
quantization eats likeness first; identity drift/hands/context loss = failure modes; quality
judged by eye/likeness/flicker with NO objective metric — hero shots must be Medium-Res; canvas
stickman stays the backbone.

**Blocked items: see `BLOCKED.md` (routes tried, verbatim errors, what unblocks each).**
## Tooling shipped this session (2026-11-14, session A follow-up)
- `tools/rejected_log.py` — auto-ledger from gate/ultracritic_r*.json + gate/report.json; writes research/video-notes/rejected/<slug>-<ts>.md with below-threshold frames grouped by class. Ran on short-0005 → research/video-notes/rejected/short-0005-20261114T182711Z.md (r1: 10 fails incl. s6_u50 low-contrast; r10: 5; r11: 3).
- `tools/hero_shot_harness.py` — C16 hero-shot QA pairing check: input still (AR/format) + output video (duration [1,15]s, AR ≤2% drift, fps [8,60], codec h264/hevc/vp9/av1 ≥320x240) + optional --qa-dir requiring qa_*.mp4 artifacts; prints PASS/FAIL + explicit failures. Harness mechanical only — VLM gate + boss still gate ship.
- `research/zack-d-films-intel.md` — boss-supplied production intel on Zack D. Films (Blender+Cascadeur+Flamenco/AE/EmberGen pipeline, cadence moat; no study repo on GitHub; VL-01..05 our reference notes).
- `research/style-bible-github-best.md` — + boss-verified KiwiTrek/ArtBible & Pixar/DreamWorks orgs note (pattern only; never copy content).
- `engine/core.js` — additive motion-grammar easing library (V2.backInBig etc.) + RESERVED V2.REGISTERS (boss-held C13 flip).

**Pending/waiting items (not done, named):**
- VL-16/VL-21/VL-22 analysis notes — subagent running (Wan demos + NASA/USGS frames done).
- VL-17 reddit thread — 403 everywhere from this IP (unverifiable here; notes marked CANDIDATE).
- VL-09 Gunner — vimeo 401/403; needs boss.
- VL-11/VL-13b — retried + frame-extracted + analyzed ✓ (added to the corpus this session).
- VL-18/19/20 — boss-side (phone clip; 2 style-anchor Shorts by their eye; PD grading picks).

## Compliance
Analysis-only. No corpus material (frames, audio, footage) enters any published Short. Shorts
bottom of corpus may be referenced for analysis verbatim ≤50-word quotable snippets. NASA/USGS PD
may be composited into future renders WITH courtesy attribution line in `content/<slug>/assets/NOTICE.md`.
All notes committed to git; raw videos NOT committed.

## Re-run the intake (for future Claudes)
1. `invidious_instances=$(python3 tools/fetch_instances.py --export)`
2. captions: `/api/v1/captions/<yt-id>?lang=en` (text/vtt) — works when YouTube is bot-walled.
3. download Shorts via 3 live invidious instances or `yt-dlp --write-auto-subs`; on DNS flaps
   just retry; on 429 subtitle 429, drop `--write-auto-subs`+`--no-write-info-json` and merge manually.
4. frame extractor one-liner lives in session notes; scene cuts via `ffmpeg -vf "select='gt(scene,0.3)',showinfo" -f null -`.
5. Fan out one subagent per corpus group (frames + vtt + cut map), return digests; writes
   `research/video-notes/<base>.md` per video; never composites anything into renders.
