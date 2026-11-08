# Rules — every hard rule, its evidence, and what enforces it

> Reader: any agent or human about to make a video. One rule = one line + evidence
> + enforcer. "Process" means no tool checks it yet — see `docs/_audit/inventory.md`
> and `tools/preflight.py` for coverage. Sources: `L-###` = ledger lesson (raw text
> in `docs/_archive/lessons/`); `day-010` = the boss-feedback session measurements;
> `vendor` = a law adopted from a vendored skill (cited).

Legend — Enforced by: **linter** = `tools/script_linter.py` exit code;
**A1–A5** = ultracritic mechanical checks; **dim** = a scored rubric dimension in
`tools/ultracritic.py`; **gate** = `tools/vlm_gate.py`; **preflight** =
`tools/preflight.py` (new); **process** = documented discipline, not tool-checked.

## Script (stage: `docs/playbook/script.md`)

| # | Rule | Evidence | Enforcer |
|---|---|---|---|
| S1 | No greetings, channel intros, meta-commentary, disclaimers, or banned boilerplate (delve, tapestry, testament, beacon, unravel, realm, "in summary", "have you ever wondered", "imagine a world where", "welcome back", game-changer, unlock, journey…) | L-014; full list in linter | linter (BANNED list, FAIL) |
| S2 | Hook lands ≤3s, target 1.8s; opener ≤14 words hard cap (target ≤12) | L-016; #0001's slow hook fed a 3.5/10 first-frame autopsy (L-059) | linter (opener word cap) |
| S3 | **Orient before you subvert:** beat 1 NAMES the topic — a noun from the title appears in the hook narration | L-073: #0003 never said "sunset" until t≈14s; boss heard it as "no introduction to the topic" | linter + A3 (FAIL) |
| S4 | **One spine, one closer:** no new entity in the last two scenes | L-077: #0003's Mars tangent beat | linter (warn) + A4 (warn) |
| S5 | WPM band: **185–215** for Shorts on the edge-tts +25% voice class (long-form: 155–175) | #0004 measured 201 WPM = dead center (day-010); #0003 at 205; the old 155–175 band shipped #0001 at 154 WPM = "slow-motion for Shorts" (day-007) | linter (WPM_BAND, FAIL) |
| S6 | **Cut density is the pacing:** mean scene ≤3.2s, max ≤4.2s, ≥12 visual events per ~35s | L-075: #0003 ran 4.22s mean/8 beats → pacing 5.5; #0004 ran 2.83s mean/11 beats → video-pass pacing 8.0 | linter + A2 (FAIL) |
| S7 | Every checkable claim carries a `fact_sources` entry before script freeze | day-007: the "birds react 10× faster" claim was cut as false before it shipped (Ballerini 2008, Schiffner 2016 kept) | preflight (field presence) + process |
| S8 | Rhythmic variety: ≥15% short sentences (≤6 words); 3-word punches next to long flows | L-015 (uniform cadence = synthetic tell) | linter (warn) |
| S9 | Critic loop hard cap N=2 revisions, then discard the premise | L-020 (prevents polish spirals) | process (playbook) |
| S10 | Script state feeds forward only — VLM fixes change layout/assets/timing, never the story | L-021 | process |

## Voice (stage: `docs/playbook/voiceover.md`)

| # | Rule | Evidence | Enforcer |
|---|---|---|---|
| V1 | Measure every VO duration from the real file; never estimate | L-003 (day-003 re-sync: estimates drifted); VO calibration drifted 2.6→2.92 w/s (day-002) | vo_pipeline (ffprobe per line) |
| V2 | ASR-verify every line: WER ≤0.15 pass, ≤0.30 warn, else FAIL | L-006; #0003/#0004 verified 0-fail | vo_pipeline (`asr_report.json`) |
| V3 | VO rate is per-script (`VO_RATE` env): text-dependent pacing is real | day-009: same voice+rate ran 238 WPM on one script, 207 on another | process (measure → set → re-measure) |
| V4 | Validate audio by decoding (ffprobe / MPEG frame sync), never by ID3-prefix magic numbers | L-069: an ID3-only check silently discarded 24 valid Fish MP3s | vo-gen workflow (raw-MPEG accepted) |
| V5 | Fail loudly on shortfall (log status + body head), never green-check an empty result | L-068: 0/8 files with a green check | vo-gen workflow (fail-on-shortfall) |
| V6 | Em-dashes become commas for TTS (neural voices misread them) | vo_pipeline `tts_text` (day-008 era) | vo_pipeline |

## Scenes & animation (stage: `docs/playbook/scenes.md`)

| # | Rule | Evidence | Enforcer |
|---|---|---|---|
| C1 | **One text system per scene, ≤8 words on screen.** Keyword pills ≤5 words; the pill DIES wherever a stamp/label exists; in hook/closer the kinetic title IS the caption | L-076: full-sentence captions put 22 words/frame on #0003 → text_discipline 2.8/10; keyword law lifted it 2.8 → 4.7 → 7.3 → 7.4 (#0004) | A1 (FAIL) + `engine/caption.js` contract + dim `text_discipline` |
| C2 | **Subjects are the opposite value of their ground** (lit body on dark panel, dark silhouette on lit sky) | L-063: birds at #10182E vanished on panels at #101832; #0004 contrast dim 7.2 ✓ | dim `contrast_legibility` + gate check 5 |
| C3 | **The gap was the world, not the character:** budget set density + light from a visible source before character detail | L-042: the biggest single quality jump of engine v2; #0001 (twig man) → #0002 (dusk world) 3.5→8/10 contact-sheet | dim `visual_hierarchy` + gate check 7 |
| C4 | No pose repeats in adjacent scenes; idle micro-motion (breath bob, blink) always on | day-010 rule 16: #0003 single pointing gesture → character_life 6.2; #0004 11 poses + blinks → 8.0 | dim `character_life` (video pass) |
| C5 | Cards and diagram frames BREATHE: ease-in ≥0.25s → hold ≥0.5s → ease-out; no snap-cuts | Boss autopsy of #0003 ("rapid-fire card transitions"); r2 fix on #0004 | dim `edit_flow` (video pass) |
| C6 | Every frame is a pure function of t — no Math.random, no state (deterministic re-render) | L-043 (resumable renders; the #0003 autopsy was only possible because frames re-render identically) | process (convention; probe re-render diff) |
| C7 | Rig joint math: `a` is measured from straight DOWN, forearm absolute angle `a2 = a + b`; direction = (sin a, cos a) | L-071: `a:158, b:-120` read as "arms up" but drew a2=38° pointing down | process (read `V2.joints` before tuning) |
| C8 | **End-states persist; verdicts outlive what they strike** — diagrams must not animate out before the scene ends; strike-through labels don't fade with their object | L-079: #0004's s4 photon diagram erased itself pre-verdict; s7 verdict faded with the mirror | gate end-state probes (`*_end.png` in `--keyframes`) |
| C9 | Caption width via canvas `measureText`, never character-count estimates | day-003: estimates merged caption words ("groundgives") | `engine/caption.js` (`V2._meas`) |
| C10 | Characters anchored: feet on a surface with contact shadow; captions in the bottom-20% band (y ≥ 1536) | gate checklist 1–2; day-009 caption-shoes fix (heroes raised to y1385–1395) | gate checks 1–2 + pixel-probe arbitration |
| C11 | Grade must match the world's time-of-day (a dusk vignette on a day world reads as night) | day-010 r1: "background reads as night sky with moon" on the day short | gate (notes-aware) + dim `production_polish` |
| C12 | One accent color per scene; palette tokens defined once (`V2.P`), never drift | L-004; vendor look.md | process + dim `production_polish` |

## Audio (stage: `docs/playbook/audio.md`)

| # | Rule | Evidence | Enforcer |
|---|---|---|---|
| A1 | **Audio claims are measured, never trusted:** bed must sit 6–22 dB (RMS) under VO | L-074: the bed comment said "-8 dB ducked" while the code ran it INVERTED at −24 dBFS = inaudible; two stacked bugs | ultracritic A5 (FAIL) |
| A2 | Master to −14 LUFS integrated / −1.5 dBTP, two-pass loudnorm | vendor what-if-animation master recipe; #0001 −13.96, #0003 −15.25 | finish_v3 (`master_report.json`) |
| A3 | An illustrative SFX lands in the pause AFTER its word, never on it | vendor sound.md/traps.md ("a pop on a word covers the word") | process (ear check on master) |
| A4 | All music/SFX synthesized in-repo (numpy) — license-free at $0 | day-008 (v3-spec #2 closed: no download lottery) | process (finish_v3 synth) |

## Render & encode (stage: `docs/playbook/render-encode.md`)

| # | Rule | Evidence | Enforcer |
|---|---|---|---|
| R1 | Encode frames via `image2pipe` (cat | ffmpeg), never the image2 demuxer, on 1000+ frame renders | L-072: image2 OOM-killed this sandbox; pipe ran 1026 frames in 34s | finish_v3 (permanent) |
| R2 | Gate budget: vlm_gate ≤2 re-render rounds per scene; ultracritic ≤3 rounds per night, then carry with the report | architecture guardrail + day-010 amendment (cadence debt is paid, never forgiven silently) | process (playbook) |
| R3 | Atomic git push after every milestone | L-044/L-058: 5 sandbox recycles; only unpushed work was ever lost | process |
| R4 | fps 30, 1080×1920, tail pad 0.45s, h264 crf18 + aac 192k + faststart | shipped on #0001–#0004 | render_short + finish_v3 |

## Gate (stage: `docs/playbook/gate.md`)

| # | Rule | Evidence | Enforcer |
|---|---|---|---|
| G1 | **The ultracritic is the publish authority:** grand mean ≥7.5, every dimension ≥7.0, no frame <6.0, video pass REQUIRED. Below bar → NO POST, carry with report | Boss directive 2026-11-08; L-078 calibration: boss-criticized #0003 measures 5.20 (fails hard), #0004 earned 6.92 over 4 rounds → NO POST | `tools/ultracritic.py` exit code |
| G2 | Gate notes are scene spec: write `gate/notes.json` BEFORE the first keyframe render | L-070: stale #0002 notes made the gate flag #0003 against another video's design (5 false fails) | preflight (presence check) |
| G3 | Pixel-probe every spatial gate claim before acting on it | L-064: "caption overlaps legs" was the caption's own words in the hero's x-column; probes refuted 3 high flags in one minute | process (+ `probe_*.png` artifacts) |
| G4 | Gate animations at their END-state; mid-flight prop states are informational | L-040/L-045: the gate demanded the marble end-state at u25 of a 5.3s collapse | render_short `--keyframes` (end probes) |
| G5 | Control-test every verifier against a known-bad artifact before trusting it | L-066: the "birds" plural was an ASR bias, not a TTS bug (control at normal rate); day-010: ultracritic control-tested on #0003 — catches all known failures | process (playbook step) |
| G6 | Thresholds are calibrated by measurement and documented when changed, never silent | L-078: an 8.5 bar under a judge whose honest ceiling measured 7.0–7.2 would have silently repealed the cadence law | process (ledger amendment) |
| G7 | Temporal dimensions are judged on the VIDEO (glm-4.6v video pass), never on stills | day-010: pacing scored 5.4 from PNGs (structurally capped) but 8.0 from the video | ultracritic B2 (required for pass) |
| G8 | Two VLM layers: contact-sheet autopsy (systemic) THEN per-frame gate (verification) | L-062: #0002 loop 3.5 → 5 → 7 → 8/10 | process (playbook) |

## Publish (stage: `docs/playbook/publish.md`)

| # | Rule | Evidence | Enforcer |
|---|---|---|---|
| P1 | Synthetic-content disclosure ON every upload (`status.containsSyntheticMedia: true`) | L-013/L-055: accepted by API first try on #0001 | youtube_upload.py |
| P2 | Verify auth END-TO-END with a real upload; a 200 from the refresh endpoint proves nothing | L-067: refresh returned 200 but the uploader shipped the stale token (`access_token` vs `token` key mismatch) | process |
| P3 | Shorts end by looping into the opening line (infinite replay) | L-017; #0002's loop-mirror ending; #0004's loop position directive | critic `loop` dim |
| P4 | Press publish. "Engine ready" is not "video live" | L-055: the channel sat empty while everything was built | process |

## Research loop (stage: `docs/playbook/research.md`)

| # | Rule | Evidence | Enforcer |
|---|---|---|---|
| Q1 | No repo/skill enters the registry without a verified API 200 + real clone | L-026: `motion-dev/motion` was a hallucinated 404 | process (registry discipline) |
| Q2 | oEmbed is the liveness oracle: 404 = proof of death (pop the queue); anything else = keep | L-048: multi-day retries of dead IDs are impossible now | transcribe.py (`DeadID`) |
| Q3 | A block on path N is evidence about path N only — never short-circuit the ladder | L-033/L-039: one Blocked re-raise killed the mirror paths; first proxy's failure killed the pool's at-bat | transcribe.py (per-attempt wrap) |
| Q4 | Mirrors are opportunistic, never infrastructure; query live registries, don't hardcode | L-037/L-050: 6/6 hardcoded mirrors dead in a day | fetch_instances.py |
| Q5 | Outlier score (views ÷ channel average) ≥5× → blueprint its transcript the same day | L-018; MinuteEarth 8.7× picked the #0002 formula | process (rss_scout) |
| Q6 | Steal structure, never content — transcripts are read for pacing/rhythm only | L-019 (transformative rule) | process |
| Q7 | Bot-wall posture: GitHub-runner matrix + mirrors + proxies only; no residential hardware, no y2mate-class sites, no cobalt | Boss directive; L-031, L-054, L-057 | process (policy) |

## Evidence-coverage summary

- 51 rules total (A1 A2 A3 A4 C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 G1 G2 G3 G4 G5 G6 G7 G8 P1 P2 P3 P4 Q1 Q2 Q3 Q4 Q5 Q6 Q7 S1 S2 S3 S4 S5 S6 S7 S8 S9 S10 V1 V2 V3 V4 V5 V6). Tool-enforced (linter / A1–A5 / vo_pipeline / gate dims /
  upload / preflight / render+finish artifacts): 38 (75%) — preflight
  (`tools/preflight.py`, self-tested per L-066) newly covers S7, G2, the C1
  keyword cap, the S1 scan and a C6 Math.random guard. Process-only: 13 —
  human/agent discipline marked "process" above.
- Every rule cites at least one ledger lesson or measured report. No rule is
  asserted from opinion. UNVERIFIED items: none at rule level (parameters
  carry the few UNVERIFIED notes — see `docs/parameters.md`).
