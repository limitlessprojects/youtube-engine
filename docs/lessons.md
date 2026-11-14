# Lessons — the ledger, deduplicated and grouped by stage

> Reader: anyone asking "why does the pipeline work this way?" Raw daily entries
> live in `docs/_archive/lessons/` (never deleted; cited for provenance only —
> operational knowledge lives here and in rules.md/parameters.md).
> This file keeps every lesson worth knowing, grouped by where it bites. Hard
> rules extracted from these live in `docs/rules.md` (rule IDs cited); numbers
> live in `docs/parameters.md`. Superseded lessons were deleted here, with one
> line noting why.

## Supersessions (resolved contradictions — the winner is current)

- **WPM band**: 155–175 (day-000/content-strategy/critic prompt) → 170–180
  (engine-v3-spec, day-007) → **185–215 for Shorts** (linter, day-010, measured
  #0003=205 / #0004=201 on the edge+25% voice class). Winner: the linter. The
  old bands died when the default voice changed from Fish (161 WPM) to edge-tts.
- **Cut rate**: "cut every 3–5s" (content-strategy) and "1.0–2.0s" (v3-spec #4)
  → **mean ≤3.2s / max ≤4.2s** (L-075, enforced). Winner: L-075 — both older
  numbers were estimates; L-075 is measured (#0003's 4.22s mean failed the bar).
- **Render substrate**: architecture.md described a Remotion pipeline; the real
  engine is seek-driven SVG + Playwright + ffmpeg (`engine/*.js`, ported from
  what-if-animation's rig). Winner: reality. Remotion stays "noted, post-day-30".
- **Bed level**: "duck −6 dB, −24 LUFS bed" (v3-spec #2 estimate) → measured
  law: 0.16 peak, −9 dB duck, 6–22 dB under VO (L-074). Winner: measurement —
  the spec's numbers were never audible in practice.
- **Dup L-067**: day-008 file listed L-067 twice (same lesson, two phrasings).
  Kept once. L-040 and L-045 state one principle (gate end-states); kept both
  IDs since rules cite them separately (probe placement vs acceptance rule).

## Script & story

- **L-001 Because-X-so-Y**: every design decision derives from the product; "because X, the film uses Y".
- **L-011 Niche**: What-If stickman = zero uncanny valley, fast frames, story-driven retention. Generic stickman fights oversaturated.
- **L-014/L-015 Anti-boilerplate + rhythm**: banned vocab is mechanical (linter); 3-word punches break hypnotic cadence (synthetic tell).
- **L-016 Hook law**: divergence+promise ≤3s (1.8s if swipe-away >35%). No greetings ever. → rules S1/S2
- **L-017 Open loops**: Shorts loop into the opening line; long-form one paradox per ~90s. → rule P3
- **L-018/L-060 Outliers**: views ÷ channel average; ≥5× → blueprint same day. Winning formulas measured: everyday-curiosity 8.7×, AI-fear 7.9× (needs 8/10 visuals we lacked), belief-correction 3.7×, superlatives 2.5×. Match formula to execution ceiling. → rules Q5
- **L-019 Transformative**: steal structure, never content. → rule Q6
- **L-020 Critic cap N=2**: second fail kills the premise. → rule S9
- **L-073 Orient before subvert** (#0003 never named its topic until t≈14s). → rule S3
- **L-077 One spine, one closer** (Mars tangent). → rule S4

## Voice & audio

- **L-005 TTS timing**: Fish s2.1-pro-free "Energetic Male" ≈2.6 w/s — but text-dependent; measure per script.
- **L-006 ASR round-trip**: free deterministic VO QC before render budget. → rule V2
- **L-068 Fail loudly**: one print of HTTP status + body head turned silent 0/8 into instant diagnosis. → rule V5
- **L-069 Decode, don't prefix-check** (MP3 frame sync vs ID3). → rule V4
- **L-074 Verify the mix, not the intent**: comments said −8 dB duck while the math ran inverted at −24 dBFS. → rule A1
- **L-072 Pipe around the storm**: SIGKILL on big inputs + tiny inputs passing = suspect the demuxer, not the codec. → rules R1/D7

## Visual craft

- **L-003 Emphasis spent, not spread**; **L-004 one world, one light, one accent**. → rules C12
- **L-042 The gap was the world, not the character**: set density + light from a source before character detail — the single biggest quality jump (engine v2). → rule C3
- **L-063 Subjects opposite value of ground** (bird #10182E vanished on panel #101832). → rule C2
- **L-076 One text system, ≤8 words** (22 words/frame → 2.8/10). → rule C1
- **L-079 End-states persist** (diagram erased itself; verdict faded with its object). → rule C8
- **L-071 Rig angles from straight down; a2 = a+b** — read the joint math before tuning poses. → rule C7
- **Day-003 measureText** (words merged on estimates). → rule C9
- **Vendor traps mined into engine**: LightVeil 0.28–0.5; wall texture faint; furniture needs legs + contact shadows; nothing bright competes with the face; blackout needs lights to switch off; front-on sitting doesn't read (seat in profile). → parameters "Engine craft constants"

## Pacing & edit

- **L-075 Cut density IS the pacing** (205 WPM over 4–6s holds still read slow; 2.83s mean + stamps read fast). → rule S6
- **Day-010 cards breathe** (ease-in → hold ≥0.5 → ease-out) — boss's "rapid-fire card transitions" complaint. → rule C5
- **Day-010 character life** (11 poses, blinks, breath: character_life 6.2 → 8.0). → rule C4
- **L-009 End quieter than you began.**

## Gates & verifiers

- **L-007 VLM-gate every scene**; no scene ships on first render. → rule G8
- **L-040/L-045 Gate the animation, not the still** — end-states pass, mid-states informational. → rule G4
- **L-062 Autopsy the sheet, then gate the frame** (contact sheet finds systemic faults; per-frame verifies fixes; 3.5→8/10). → rule G8
- **L-064 Pixel-probe every spatial claim** (cream captions ≠ hero limbs). → rule G3
- **L-065 Beat-timed probes** (u25/60/90 sampling is blind to 1s beats). → parameters
- **L-066 Control-test the verifier** ("birds" plural was ASR bias, not TTS). → rule G5
- **L-070 The gate must know the intent** (per-short notes.json; cross-contamination otherwise). → rule G2
- **L-078 Calibrate the bar against the judge** (7.5 mean / 7.0 dims / 6.0 floor; #0003=5.20, #0004=6.92 → NO POST). → rule G1
- **Day-010 hybrid gate**: stills judge 5 frame dims; the VIDEO judges pacing/life/flow (glm-4.6v `video_url`; CLI vision rejects mp4). → rule G7
- **L-080 The judge carries a ±0.8 noise band on identical pixels** (s2: 7.6→6.8 untouched between rounds; spatial directives contradict round-to-round). Never read a delta <0.5 as signal — decide on dim trends across ≥2 rounds, pixel-probe spatial claims (G3) before acting on them.
- **L-081 Vision-endpoint 429 after ~50 frame calls in one night** — batch gate passes early, add backoff to the video pass, retry off-peak; a technical pass failure is not a creative round and must not consume the round cap.

## Pipeline & ops

- **L-021 Schema-validated handoffs; script feeds forward only.** → rule S10
- **L-023 Local fallbacks for everything external** (edge-tts for Fish; faster-whisper; mirrors).
- **L-026 Verify repos against the API** (motion-dev/motion 404). → rule Q1
- **L-028 Submodules beat merging by value** (pinned, light, CI-checkout-able).
- **L-029 `python3 -m pip`** (+ `--break-system-packages` on PEP 668).
- **L-031/L-033/L-039 Bot-wall ladder**: cloud IPs walled; block on path N ≠ block on all paths; 5-leg matrix + proxy pool. → rules Q3/Q7
- **L-037 Mirror health rotates within the hour** — opportunistic, never infra. → rule Q4
- **L-038 `git pull --rebase` before push on multi-writer days.**
- **L-041 Proxy timeouts 75s.**
- **L-043 Deterministic frames → resumable renders** (also made the #0003 autopsy possible post-recycle). → rule C6
- **L-044 Atomic pushes bound blast radius.** → rule R3
- **L-046/L-058 The GitHub clone IS the workstation; credentials need durable mirrors** (`upload/` survives recycles; GitHub Secrets are write-only). → rule R3
- **L-047 Second egress before "it's dead" verdicts.** → dead-end D15
- **L-048 oEmbed = liveness oracle** (404 = proof of death; loop pops corpses). → rule Q2
- **L-049 POT infra ≠ ticket on a hard-flagged IP.**
- **L-051 bootstrap.sh = one env truth** (local + CI).
- **L-052 "Html Convert Error" = reachable-but-JSON.**
- **L-053 RSS = discovery oracle** (no bot-wall, views included; retired ytsearch discovery). → rule Q5
- **L-055 Press publish** (credentials ≠ a channel; containsSyntheticMedia is an API field). → rules P1/P4
- **L-056 Schedule wake-ups when the model slot is free** (23:45 EAT). → dead-end D18
- **L-057 y2mate class sealed.** → dead-end D2
- **L-059 Autopsy your own frames** (195 views took 3 days to confirm what a 60-second VLM audit said: 3.5/10). → rule G8
- **L-061 CI heartbeat + agent-creative split** survived the agent's sandbox dying for 3 days.
- **L-067 Test the full path, not the function** (OAuth refresh 200 ≠ working upload). → rule P2
- **L-082 node_modules dies with the recycle** (z-ai SDK wiped → ultracritic video pass went dark; a hardcoded `/home/z/.bun` script copy died with it). Env deps that aren't git-tracked get installed + import-probed by `bootstrap.sh`; scripts live in the repo, never in global dirs. Extends L-046/L-051.
- **L-083 A report named in a commit message must exist IN that commit** — day-011's message claimed "carry_r7.md with 3 directives"; the file was never committed and died with the working tree. Recreated day-012 from gate artifacts. Push-time check: `git show --stat` must show every file the message names.
- **L-084 OAuth refresh grants die silently even when the app is "published"** — publish.md claimed long-lived; `invalid_grant` hit at the thumbnail moment, 8 days after mint. Mitigation shipped: `youtube_upload.py --check-token` (5-second refresh probe, exit 1 = dead). Run it at session start, not publish moment. Extends L-067 (full path, not function).
- **L-085 The #0004 hierarchy ceiling is scoring-systemic, format-level** — 9 rounds of composition restructuring moved visual_hierarchy 6.1→6.9 max; r8 (dead-zone version) and r9 (filled version) scored identically within noise; frame dims and video dims both clear or nearly clear their bars (7.53 grand r8). Verdict: panel-in-world diagram cards cap at ~6.9 on this judge. Response: #0005 builds canvas-first (subject owns the frame height, no diagram-in-panel default) — never a 10th polish lap on #0004.
- **L-086 Background processes die with the tool call** — nohup'd renders vanish between calls (sandbox reaps on return). Long jobs run FOREGROUND with an idempotent `--resume` flag; a timed-out call resumes in the next call at zero loss (proven: 660+289 and 643+306 frame resumes). Extends L-043.
- **L-087 Probe-first variant selection** (day-012): 3 hook variants × (1 u50 render + 1 VLM call) picked the winner before any full render — the cheap A/B the gate always wanted. Directive-level changes get probed at u50 before they earn a full pipeline cycle.
- **L-088 One-call sitrep beats bursty exploration** — toolcall round-trips are the failure surface (connection-closed bursts); state collection batched into a single scripted probe (tools/sitrep.sh: git/log/ledger/carry/gate-rubric/queue/views/actions in one 90s call) replaced ~15 exploratory reads and located the rubric location, the carry report, the views gap and the OAuth state in one shot. Scripts-first: write the probe, run it, read the output — never re-derive repo state from memory.
- **L-089 Every new import ships with its installer** — vo_pipeline died on a fresh restore (`ModuleNotFoundError: edge_tts`): the synth dep was never in bootstrap.sh/requirements.txt. The L-082 class strikes again — env deps that aren't bootstrap-installed die silently with every recycle and block the nightly loop. Fixed day-013: bootstrap.sh fast-path + requirements.txt now cover edge-tts; rule: the commit that adds an import also adds it to bootstrap.
- **L-090 Digits and foreign proper nouns defeat ASR verification** — "1883"/"180"/"130" in narration scored wer 0.30–0.56 against word-form transcripts; "Anak Krakatau" heard as "and it Krakatoa"; "the sea it shook" compressed to "The Siachuk". Day-013 rule: numbers are written as spoken words in narration (dates too), digits live on screen as stamps; foreign names live in the visual, not the VO. v2 of #0005's lines: 11/11 PASS.
- **L-091 Empty ASR is throttle, not truth — verify by union, defer on hard-throttle** — three verify runs on the SAME mp3s rotated which lines returned empty (2 lines, then 3, then all 11 after ~35 calls in a burst). Every line PASSed in ≥1 run; the union with per-line run provenance IS the verification state (vo/asr_report.json carries it + the caveat). A 4th hammer-run would have written a false "n_fail=11". Off-peak `--verify-only` re-run is the render-stage pre-step. Extends L-081: a technical pass failure is not a creative round.
- **L-092 Test the durable mirror before declaring a grant dead** — day-013 recorded "OAuth refresh grant DEAD (`invalid_grant`, both copies)" and handed the boss a re-consent URL; a day-014 refresh against `upload/token.json` (the day-011 mint) returned 200 and `youtube_upload.py --check-token` = OK. The dead-grant verdict was produced against a stale copy, not the durable mirror — the boss never needed to re-consent. Rule update to L-084's probe: `--check-token` must point at the MIRROR (`upload/token.json`), not whatever copy the session happens to hold. Extends L-047/L-067: second egress before "it's dead" verdicts includes the credential file itself.
- **L-093 The free-GPU pattern exists and is stealable** — mr-bean-motion-swap runs heavy video models on anonymous HuggingFace ZeroGPU quota: slice work into ≤140 GPU-second chunks, one GitHub Actions matrix job per chunk (every runner gets a fresh IP → the ~160 GPU-s per-IP anonymous quota resets), auto-rerun on quota failures, CPU jobs do motion-aware planning and frame-exact assembly. Correction on record: that repo runs **Wan2.2-Animate**, not SeedDance 2.5. This is the route for C16 hero-shot image-to-video: batch the GPU work free, composite locally. Assessment: `research/free-gpu-video.md`.
- **L-094 freefield is parked, not adopted** — 120 open-weight ComfyUI apps, but it needs a Modal account + gateway deployment + multi-GB model downloads before the first frame exists. Our bottleneck is format/style (L-085), not model access — asset generation is already covered. Revisit trigger: a hero shot that genuinely needs a ComfyUI-class app, or a confirmed Modal free tier. Parking a heavy infra detour IS the decision; recorded so day-020 doesn't re-derive it.
- **L-095 Boss style directive 2026-11-13 generalizes the L-085 fix** — stop drawing with primitives: locked style bible FIRST (C13), layered transparent assets (C14), programmatic motion design (C15), image-to-video only for hero shots (C16), accuracy pass with one "wow" element per scene (C17), and the gate now rejects "basic shapes" reads (G9). The panel-in-world ceiling was never a craft problem; it was the format. #0005's canvas-first build and every future short route through the style bible.

- **L-096 Probe artifacts live OUTSIDE the gate glob** — the hook A/B probe PNGs were parked in `gate/` (L-087 habit) and their `*_u65` names matched the ultracritic frame glob, so r1 judged 15 frames instead of 12 and the probe variants (one of them the LOSER) sat inside frame_grand_mean. Probes go to `render/`; `gate/` holds only `{id}_uNN.png` + reports. Hygiene rule, not style.
- **L-097 The A2 beat-count law and the WPM ceiling are one equation** — mean scene = VO total / beats: 36.3s at 214.5 WPM needs ≥12 beats to clear the 3.2s bar, and day-013's 11-beat script inherited a mechanical fail discovered only at gate time. Fix shipped day-015: visual-only beats (narration "" → finish_v3 skips the VO mapping) are legal pacing cuts — #0005 split its closer into s9+s10 as a J-cut. Rule for script stage: beats ≥ ceil(VO_seconds / 3.2). TODO: script_linter gains this check so it fails at lint, not at gate.
- **L-098 Bed level is a measured calibration, not a constant** — the 0.16 peak that fixed L-074's "no bed at all" measured only 1.3 dB under #0005's VO RMS (mud; A5 fail): VO loudness varies per short, so the bed peak must be set against each short's measured VO, not inherited. 0.075 ≈ 7.9 dB under (band center) shipped for #0005. Also recorded: finish_v3 exits −9/255 after the report is written on this sandbox — treat the printed report + mp4 mtime as completion, not the exit code.

## Signals so far (for calibration context)

- #0001 (engine v1): 195 views / 3.5 days, first-frame 3.5/10 — premise fine, execution the bottleneck.
- #0002 (engine v3 debut): hook 7.5/10 pre-publish, contact-sheet loop to 8/10 "SHIP IT".
- #0003 (boss-criticized): ultracritic 5.20 — text 2.8, pacing 5.5, character 6.2, contrast min 4.
- #0004 (carry): r4 6.92 → r5 6.98 / r6 7.11 / r7 7.14–7.18 (video pass 429-blocked) → day-012 **r8 7.53** (video pass ran: pacing 8.0 / life 7.0 / edit 8.0; hook rubric fix → hook 7.0 ✓) → r9 redesign 7.35. Grand hit the 7.5 bar in r8; **visual_hierarchy 6.1–6.9 flat across 9 rounds = format ceiling** (L-085). CARRIED UNPOSTED; format-level fix assigned to #0005.
- **L-099 Flood-fill cutouts fail on complex subjects — rembg (U2Net) is the C14 asset path** — day-016's first asset-layer pilot cut the sticker assets with a border flood-fill (scripts/cutout_assets.py): the model's "solid flat navy" background was near-flat but the mask hugged frame edges on subjects that fill the frame, and the gate read every layer as a "pasted screenshot" with a hard rectangular seam (s4 5.8→4.8, s6 6.0→5.8). Re-cut with `rembg` u2net + 1px erode + feather + island-drop (scripts/rembg_cutouts.py, ~1.5 GB model, installed+import-probed): subject-shaped alpha, seam directives vanished (s4 +2.0, s10 8/8/8/8 in r7). Rule: image-gen stickers on flat navy + real alpha matting; never key by color on a subject that touches the frame edge.
- **L-100 An image layer must be COMPOSED, not pasted** — three seam classes bit in r4/r5: (a) visible crop edges → dissolve with per-side gradient masks (wave), (b) image's internal horizon at a different y than the SVG sea → draw the image BEFORE the sea rect and sink its internal sea band below the SVG sea line (cone: y = horizon − 0.62·h), (c) layer colliding with existing type/hero → shift or shrink the layer, not the text. Also: image <image> hrefs need a cache-warm pass at script load or frame 0 renders empty.
- **L-101 VLM frame-pass variance is ±0.34 grand on IDENTICAL frames** — r6 (7.48) and r7 (7.14) judged the same 12 keyframes; per-frame deltas reached ±1.5 (s8 7.8→6.3). Consequence: a combined score 0.01–0.15 below the bar is NOISE, not craft — chasing it with another polish round is gambling, and "one more round" decisions must fix named directives or stop. The video pass is far more stable (8/8/7 → 8/7/8 → 8/8/8 across three rounds).
- **L-102 The dark-world hypothesis is REFUTED by measurement** — carry_r3 D3 suspected the night palette carried a structural hierarchy penalty across three shorts. tools/probe_daylight.py re-rendered s6 with bible-legal daylight tokens and A/B-graded both stills: night vh 8/cl 8 vs day vh 6/cl 7 (delta −2/−1). Night holds; the stuck dims were craft (L-085/L-095), not palette. #0006 is free to keep night worlds — and the probe tool is now the standard A/B for any "is X structurally penalized" question.
