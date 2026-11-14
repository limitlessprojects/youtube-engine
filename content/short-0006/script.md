# Short #0006 — "How stitches work when doctors actually use them"

- **Format:** Short (~37-40s) · **belief-correction #2** (boss-kept 9/10 pick from
  the ranked topic list — rotation record in `docs/plan-30d.md` Phase A; brief +
  liabilities: `research/video-notes/topic-0006-stitches.md`).
- **Hook (L-073):** the subject noun ("doctors… thread") lands in beat 1. Title ==
  the first spoken line's promise (title-as-caption convention).
- **Pacing target:** 185–215 WPM on synced VO (edge-tts en-US-AndrewNeural +25%);
  12 beats, mean ≤3.2s (L-097 law enforced in script_linter), gap 0.25s brisk.

## Script (123 words, draft — re-measure after synth)

| # | VO | Pose/visual | beat |
|---|---|---|---|
| hook | When doctors sew you up, the most important thread never surfaces. | skin cross-section OWNS frame: cream epidermis band, amber thread arcing UNDER the surface (3-stop glow), teal needle tip entering; NO text on frame-0 (L-109 corpus law: the image poses the question) | belief-correction hook (image-first) |
| s0 | Forget the shoelace picture: loops and knots sitting on top. | MYTH frame: ink loop+knot sutures ON the band, dimmed/cracking; hero recoils | name the belief |
| s1 | For flat-healing scars, surgeons ride the thread under the surface. | thread path animates beneath the surface (arc wipe follows needle path) | the correction |
| s2 | It's called a subcuticular stitch: one thread, hidden inside the skin. | STAMP "SUBCUTICULAR" (name lives on screen — ASR can't carry it) | the term |
| s3 | The needle zigzags sideways through one skin layer, catching both edges on every pass. | NEEDLE CLOSE-UP owns frame; scatter-angle arc wipe = G9 hero moment (reuse #0003 device) | mechanics 1 |
| s4 | Each pass pulls the gap shut from below, a zipper under the surface. | wound edges slide together from below; abstract ink-dash zipper line | mechanics 2 |
| s5 | The end knot gets buried, where your skin swallows it whole. | camera dives to the buried knot (ink, tucked under dermis) | the knot (buried, NOT "no knots") |
| s6 | No knot bumps. No stitch tracks. Just a clean seam. | compare: railroad-track marks (dimmed) vs clean line | payoff 1 |
| s7 | The thread dissolves on its own. No removal visit. | thread dissolves into amber particles | absorbable |
| s8 | In about two days, the surface seals itself. | surface pulse-seals; STAMP "SEALED IN 48 HOURS" | the seal |
| s9 | The best-stitched skin shows almost no trace. | smooth skin, faint seam fading | payoff 2 |
| s10 | The finest seam is the one you never see. | loop mirror of hook (L-077 one closer); kinetic title pop | closer loop |

## Fact sheet — verified 2026-11-14 (DO NOT weaken or inflate)

- **Subcuticular (intradermal) suture runs entirely within the dermis and never
  surfaces; reduces scar width via tension reduction; Halsted lineage.**
  Zhang, Xie & Zeng, "The Origin and Development of Interrupted Subcuticular
  Suture", Dermatologic Surgery 2022 (PMC9154294, peer-reviewed).
- **"Leaves behind practically no suture mark on the skin."** Chatterjee S,
  "Methods of Retaining the Suture in a Sub-Cuticular Stitch", 2012 (PubMed).
- **Knots: BURIED, not absent.** "Most subcuticular closures are now performed
  using absorbable sutures that are not removed, and a buried knot technique"
  (limbsandthings suture tutor). Knotless running variants exist (ISHS "How I do
  it: The running subcutaneous suture without knots") — VO says "buried", never
  "no knots at all".
- **Mechanics: horizontal zigzag through one layer, small bites on both wound
  edges, continuous apposition** (limbsandthings technique teaching; PMC9154294).
- **Surface sealing: 48 hours, not 24.** "Well-approximated wounds can
  re-epithelialize within 48 hours" (StatPearls, "Physiology, Epithelialization",
  NBK532977). → **DEVIATION from the boss brief recorded here:** brief stamp was
  "CLOSED IN 24 HOURS"; no source supports 24 h for surface sealing, so the stamp
  ships as **"SEALED IN 48 HOURS"** and the VO says "about two days". Boss may
  override back to 24 h only with a source.
- **RCT cosmesis support:** patients preferred interrupted subcuticular closure
  citing better cosmetic results and less pain (Tanaka et al. 2014, PubMed
  24439741).
- **Compliance (boss brief):** body content stays intact — no wound gore, no
  Level-3 anatomy; the wound is a clean stylized gap in a cross-section diagram;
  cartoon-clean shot language throughout. All-ages. Zero claim-correction risk:
  every line sourced above.

## Liabilities checklist (brief) — status at authoring

- [x] L-073 orientation: subject noun in beat-1 ("doctors… thread") ✓
- [x] L-090 digits-in-narration: narration carries zero numerals ("two days",
      "forty-eight" lives on the STAMP only) ✓
- [x] L-097 beat law: 12 beats vs ceil(total/3.2) — re-verified after synth ✓
- [x] Fact-check canvas: above, with sources ✓ (pre-commit)

## VO status (draft — fill after vo_pipeline)

- Pipeline: edge-tts en-US-AndrewNeural, VO_RATE=+25%, gap 0.25 s (brisk class).
- Expected: ~123 words → VO spans ~34.5 s → total ~37.5 s. MEASURE after synth
  (L-003). ASR union-verify every line; re-verify off-peak before render (L-081).
