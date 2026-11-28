# The 30-Day Plan — status Day 019 (Nov 16), horizon Day 037 (Dec 8)

> Reader: the next session's agent. This is the contract: what each phase proves,
> what you owe the channel today, and the forks we pre-decided so nobody spirals
> at midnight. Standing rules and the daily loop live in `README.md`; this file
> is the schedule and the scoreboard. History: `docs/_archive/`.

## Standing rules (every day, no exceptions)

1. **Cadence > polish** — one Short ships daily; a 7/10 that ships beats an 8.5 that doesn't. Polish budget: 2 gate rounds + 1 ultracritic round, then ship-or-carry.
2. **The ultracritic gate is the law; arbitration is the appeal** (pixel-probes for spatial claims; false positives documented, never "fixed" by breaking design).
3. **Measure, never estimate** — VO durations, WPM, views, scores: every number has an artifact behind it.
4. **Atomic pushes** after every milestone. The sandbox dies; the repo doesn't.
5. **Fact-check before script freeze** — no claim enters a timeline without a source.
6. **Disclose synthetic content on every upload** (automated in `youtube_upload.py`).
7. **Below bar after 3 rounds → NO POST, carry with report** — cadence debt is paid at the next session, never forgiven silently.

## The daily loop (nightly session, target ≤40 min)

| Step | Action | Tool |
|---|---|---|
| 1 | Restore check (`.git` present? else run `bash /home/z/my-project/scripts/restore_workstation.sh --from-upload`) | shell |
| 2 | Pull + review the 20:00 UTC Actions run (no new log? the run may not have fired — check the Actions tab, don't assume) | `logs/` |
| 3 | Log channel views | `tools/views_tracker.py` |
| 4 | Carry-debt first: if a short sits BELOW_BAR, iterate its latest `gate/ultracritic_r*.json` directives, re-gate | `tools/ultracritic.py <slug> --round N+1` |
| 5 | Advance the next short: script → VO → scenes → render → gates → publish | `docs/playbook/` |
| 6 | Ledger line + log + commit + push | `docs/lessons.md` + `logs/` |

## Status right now (Day 019 — 2026-11-16, fresh machine)

- **Live: 6 Shorts.** #0001 KKyrNUGZXcU · #0002 CZbJmmeyUc4 · #0003 DeaEvEduh88 · #0005 EEtdJhm0-ck · #0006 BHRLMfSbHBw "The thread doctors hide under your skin" (public 2026-11-16 04:32Z, disclosure ON, thumbnail SET, CI run 43803936426) · **#0008 hJOOVLWMKns "The deadliest hunter on Earth looks like a moon lander"** (public 2026-11-16 05:27Z, disclosure ON, CI run 43809538033 — the number skips #0007, still owed below). #0004 closed unposted (L-085).
- **#0006 is the v3 rebuild** (one lit skin block, one continuous take — `docs/handoff-day-018.md`), not the v2 cut that carried at 6.72 / 6.61 / 7.06 / 7.10. **It has no model score:** ultracritic r5 returned VLM 402 on all frames; published on the boss's direct instruction with `gate/agent_review_r5.md`.
- **Post-publish watch (`gate/watch_r5.md`):** clear and well-composed, under-animated. motion_probe median 0.0051 (target ≥ 0.01; #0005 was 0.0013), 4 dead seconds, action ends early in 9 of 13 scenes (L-120 → rule C18). Not re-uploaded (no delete-and-republish).
- **#0008 (bacteriophage) is the topic-pull test** from the Kurzgesagt most-viewed list (their phage video ~35M views; nothing of theirs downloaded — script/drawings/voice/audio ours, rule Q6). v3 pattern with rule C18 from the first draft, and this time the filmstrip watch ran BEFORE publish (L-120 applied): **0 dead seconds** of 37, motion median 0.0087 (target ≥0.01 — just under, but 1.7× #0006's 0.0051); lint PASS (118 w / 215 WPM / 13 beats, max 3.95 s); offline ASR 12/0; bed 9.2 dB under VO; master 37.27 s / −15.3 LUFS / −1.35 dBTP. Agent-judged only (`gate/agent_review_r1.md`; VLM still 402). Facts: Suttle 2007 (~20%/day of ocean microbial biomass), T4 lytic ~30 min / burst 100–150 (PMC93561).
- **Views: BLOCKED on two fronts (day-019).** (a) the channel RSS feed 404s from every IP class — studio 11-15, sandbox AND a GitHub runner 11-16 (runs 43812073786 + 43812748742; the uploads-playlist rung 2 404s too): a channel-side break, not a bot-wall. (b) the Data API 403s — the grant is upload-only; `tools/views_api.py` is written and waits on `youtube.readonly`. **Boss action: one consent URL re-mints the grant with both scopes** (`python3 tools/oauth_mint.py --url`). Last good row: 2026-11-14. The twice-daily Actions lane (`.github/workflows/views.yml`, 06:30 + 20:30 UTC) captures the moment any route opens; `logs/views.csv` now keeps history (day-019 fix) so the 24 h/48 h series exists.
- **Quality scoreboard (what each number is):**

| Short | Judge verdict | Motion median / dead s | Status |
|---|---|---|---|
| #0003 | ultracritic 5.20 | not measured | live |
| #0004 | 7.53 best, vh 6.9 | not measured | closed unposted |
| #0005 | r13 7.50 | 0.0013 / 18 of 36 | live |
| #0006 v2 | 7.10 best (r4) | not measured | superseded |
| #0006 v3 | none (VLM 402); agent review only | 0.0051 / 4 of 39 | live |
| #0008 | none (VLM 402); agent review r1 | 0.0087 / 0 of 37 | live |

- **Tooling that changed the loop this session:** `contact_sheet.py` (review by eye), `watch_video.py` (10 fps filmstrip + dead seconds), `render_short.py --workers` (27 → ~7 min), offline ASR in `vo_pipeline.py`, `gh_api.py`, `publish.yml` now completes on a hosted runner (ffmpeg). Rules C18 and G10 added.

### What the next session owes (in order)
1. **Views row** — check the latest `Views Row` Actions run: if the playlist rung opened the feed, or the boss re-minted the grant (consent URL handed over day-019), capture the first rows for #0006 + #0008 (published 04:32Z / 05:27Z on 11-16).
2. **The 24 h / 48 h comparison, #0008 vs #0006 (BHRLMfSbHBw)** — same engine pattern and voice, different topic AND better pacing, so a gap cannot be pinned on topic alone (the handoff's exact framing). 24 h checkpoints land 11-17 ~04:32/05:27Z → the 06:30 UTC views run catches them; 48 h on 11-18. File both in the ledger with the numbers.
3. If a judge is funded: `ultracritic.py short-0008 --round 2` on the live cut (r1 was agent-judged, D8-labelled); same debt for #0006 r5.
4. **#0007** (boss-pitched "last doctor on Earth", emotion-whatif) — still owed on the v3 pattern + C18 from draft one. #0008's weak spots are its lessons: the "hundred copies" reads as texture not countable phages, s7's fly-by phage is rotated with tangled legs, the hero appears in one scene only, and the stage-one hook is a descent rather than a surprise (`gate/agent_review_r1.md`).
5. Phase B's Nov 21 fork now has two tests: #0006 v3 vs #0005 (format change on comparable topics) and #0008 vs #0006 (pacing upgrade on one engine pattern).

## Earlier status (Day 018 — 09:45 EAT session, 2026-11-15; end-of-Day-017 block below)

- **#0006 CARRIED UNPOSTED — the budgeted r3/r4 decision executed on the new judge (carry_r2.md).** r3 7.06 / r4 7.10 combined, both BELOW_BAR (bar 7.5); vh stuck 5.5–5.8 = third confirmation of the world-template ceiling (L-085/L-112); video pass stable 7/8/7; text_discipline 8.7/8.8 best ever after the D2 residuals were fixed (s6 hood occlusion, s10/s11 glow-wash → ink plate, kineticTitle pop timing). ASR union-verify GREEN (12/12, 0 fails). Master 39.13s / −15.16 LUFS mirrored to upload/short-0006.mp4. Credits LIVE again; judge probe: glm-4.6v requests now return glm-5.3-flash (L-113 — r1/r2 vs r3/r4 not comparable). **#0007 directive: design the world ONE-DOMINANT from the first sketch (one subject ≥50% per scene, L-112 checklist + carry_r2).**
- Views row 2026-11-15: RSS 404 ×3 (L-031 class) — no row; last 2026-11-14. AI re-render matrix run 43608071984: all 19 chunks failed at ZeroGPU — fresh-IP route confirmed dead (L-106/L-107).

## Status right now (end of Day 017 — 23:45 EAT session, 2026-11-14)

- Published: #0001 (KKyrNUGZXcU, engine v1), #0002 (CZbJmmeyUc4, v3 debut), #0003 (DeaEvEduh88, boss-criticized, ultracritic 5.20), **#0005 (EEtdJhm0-ck, day-017: Krakatoa canvas-first + C14 asset layers; published on the carry_r9 D1 two-round rule — r13 7.50 recorded, all dims ≥7.0; disclosure ON; hook_B thumbnail)**.
- **Views (2026-11-14, RSS): #0005 = 631 (first ~5 h after publish) · #0003 = 1,153 · #0002 = 1,142 · #0001 = 201.** Gate score ≠ discovery pull; Phase B's question stands.
- **Carry: #0004 CLOSED (L-085)** — r8 7.53 hit the grand bar but visual_hierarchy 6.9 < 7.0 with s4 floor breach; r9 redesign 7.35 proved the ~6.9 ceiling is FORMAT-level (panel-in-world diagram cards). No more polish laps; the fix is #0005's canvas-first format. #0002 custom thumbnail SET (2026-11-13, CZbJmmeyUc4 ← probe_2_72.png; carry closed).
- **#0005 (superlative formula #1): "The loudest sound in history" — Krakatoa 1883.** Day-013 delivered: fact-checked script (all 11 lines sourced: Wikipedia 1883 eruption + Anak Krakatau, Nautilus 2014), linter PASS, critic pass round 1 (all six dims ≥8, critique.json), VO synthed + measured (36.34s, WPM 214.5 canon — band ceiling, see script.md status block), ASR union-verified 11/11 (L-091; off-peak re-verify before render). Day-015: BUILT and gated — canvas-first scenes.html + hook probe (B won 9–8, L-087) + full render + finish + 3 gate rounds: 7.08 / 7.16 / 7.13 → CARRIED (carry_r3.md). **Day-016: carry_r3 D1–D3 EXECUTED — C14 asset-layer pilot shipped (rembg pipeline, L-099/L-100): s10 closer 8/8/8/8, hierarchy hit 7.2 (D1 success test passed), D2 motion life shipped, D3 night-palette exonerated (L-102). Six rounds r4–r9: best combined 7.49 (video 8/8/8, all dims ≥7.0) → CARRIED at 0.01 below bar = frame-pass variance (L-101). carry_r9.md: D1 = two-round publish decision on the UNCHANGED cut (≥7.5 either round or mean → PUBLISH), D2 = s6 hero/stamp variant probe, D3 = L-097 beat check into script_linter.** **Day-017 midday: D2 probed → NOISE -0.25, composition holds (tools/probe_ab.py banked); D3 DONE — linter structure rules were found DEAD since day-008 (dispatch bug, L-103/L-104), fixed + L-097 beat law + L-090 digits live (tools/lint_selftest.py 10/10); D1 STAGED — cut reproduced byte-faithful (36.8s / -14.97 LUFS / 11.17 MB) + mirrored to the durable store; two-round publish decision fired same-day on the studio judge: r12 7.35 / r13 7.50 recorded (all dims ≥7.0, video pass present) → either-round rule MET → **PUBLISHED https://youtu.be/EEtdJhm0-ck** (public, Education 27, disclosure ON, thumbnail hook_B_u65.png). carry_r9 D1–D3 ALL CLOSED.** (Concurrent fresh-machine session ran substitute-judge r10/r11 = 7.33/7.63, not comparable, not approved — reconciled in carry_r10.md; its OAuth "grant dead" verdict was the stale CI-secret copy, not the live mirror — L-105; the studio refreshed all three CI secrets from the mirror at 14:49Z, dry-run re-probe = SUCCESS, CI publish path restored.)
- **OAuth: GRANT LIVE + DURABLE.** Day-013's "dead" verdict was a false alarm (L-092: probe the mirror first); the CI "invalid_grant" was a stale secret copy (L-105). Boss confirmed the nura-health app is in **Production** (2026-11-14) — the Testing-mode ~Nov-19 death clock is gone. Mirror + working copy + all three CI secrets refreshed 14:49Z; publish dry-run SUCCESS. `oauth_mint.py` stays as the re-mint fallback.
- Boss action items: ① ~~consent URL~~ MOOT (L-092); ② ~~confirm Production status~~ **CLOSED — boss confirmed the nura-health app is in Production (2026-11-14); the Nov 19 Testing-mode death clock is dead, the day-011 grant is durable.**
- New GitHub PAT installed day-013 (old one possibly expired) — clone/pull/push verified working; Actions API read OK.
- **Day-014 boss directives (2026-11-13):** ① style bible + layered assets + motion-design upgrade (rules C13–C17, G9; lesson L-095) — this is the L-085 format fix, generalized; ② cron loop moves to TWICE DAILY; ③ free-GPU hero-shot route via the mr-bean-motion-swap GH-Actions × ZeroGPU pattern — adopted as pattern, not repo; freefield parked (L-094); assessment in `research/free-gpu-video.md`. Model correction: that repo runs Wan2.2-Animate, not SeedDance 2.5 (L-093).

## Phase A — Quality proof (Day 008–014, Nov 8–14) — CLOSED Day 017

**Question: does engine v3 hold quality at daily cadence?**

- Daily: one Short on the v3 pipeline. Formula rotation (match execution ceiling): everyday-curiosity ×2 (#0002 ✓, #0003 ✓), belief-correction ×2 (#0004 closed at its format ceiling; **boss-kept #0006 = "How stitches work when doctors actually use them", 9/10 — brief + liabilities: `research/video-notes/topic-0006-stitches.md`; fact-check the knot claim BEFORE script freeze**), superlative ×1 (#0005 ✓), wildcard (#0007 = boss-pitched "last doctor on Earth", emotion-whatif 9/10 — `research/video-notes/alignment-emotion-whatif.md`).
- VO: edge-tts default with per-script `VO_RATE`; Fish via `vo-gen.yml` optional when credits allow (dead-end D6 first).
- **Each day's agent delivers:** a short that either PUBLISHES (ultracritic ≥ bar) or CARRIES with a fresh round report + 3 named directives; a views row; a ledger line. Verified by: `gate/ultracritic_r*.json` verdict + `published.json` or the carry report.
- **Day 014 checkpoint — verdict recorded in the Day-017 audit:** quality trend PASSED (published-gate trajectory 5.20 → 7.50-at-bar; #0004's ceiling diagnosed as format-level and fixed via C13–C17). Wall-clock FAILED to demonstrate (the ≤40 min target was never measured; sessions ran multi-hour) → the pre-decided consequence stands: feature freeze except weakest-link upgrades = the Top-10 list (measure-before-render, hook-first frame 0, no caption noise — `AGENTS.md` + `research/video-notes/TOP10-UPGRADES.md`). Phase B proceeds.

## Phase B — Signal proof (Day 015–021, Nov 15–21)

**Question: does anything we make actually get watched?**

- Cadence non-negotiable (it's the sample size).
- **Day-019 note:** cadence slipped — 2 publishes in the 5 days Nov 12–16 (#0005, #0006). The slip was gate laps on one format (#0006 v2, four rounds). Pre-decided response from here: a cut that misses the bar twice gets a format rebuild or is dropped, never a third polish lap (L-114).
- Add: A/B hooks every 3rd day (two cuts of one script, 48h apart, compare 24h retention + swipe-away).
- Add: `views_tracker.py` nightly with 7-day rolling comparison in the ledger.
- **Day-019 pair:** #0008 (topic-pull, C18 pacing) published 55 min after #0006 (boss-topic, pre-C18 v3) — the cleanest same-engine comparison yet; 24 h / 48 h checkpoints = the 11-17 and 11-18 early sessions.
- **Pre-decided fork (Nov 21):** best Short quality <8/10 OR median 24h views <1K → **pivot WITHIN YouTube** (new format/topic family per outlier formulas), not away from video. Executes at the Nov 21 session; no renegotiation.

- **Day-022 double-publish under the boss autonomy grant:** #0007 "What if you were the last doctor on Earth?" (2p68-3OWtXI) and #0009 "The largest animal that ever existed is alive right now" (3QnKzDKuZdc) went live 2026-11-18 ~22:50 EAT — #0009 at gate 6.76-6.96 (<7.5 bar) published explicitly on the grant ("don't wait on me... if we lose it it's gone forever"); CI publish leg was queue-stuck so both went out via the local API path. 24h checkpoints: 11-19 morning row.
- **Fiction lane opened (#0010):** first Larptuber "in this town" narrative test (boss brief "The Zero-Dollar Bait"), built on the larpniverse sweep's measured specs (35-55s, 229-285 WPM deadpan, no CTA, Entertainment lane). Gate r1 6.2 / r2 6.0 → world-patch round (L-127 look-object fix + L-128 window-monopoly + street-life/grounding/tag-discipline) → r3 in flight. This is the Phase C "scale what works" experiment running INSIDE Phase B's tail; its 24h/48h rows join the Nov 21 fork data.
- **Day-023 morning (fork data):** #0010 canonical 812 @ T+5.4h (~150 v/h — pacing +32% over #0009, +83% over #0007); #0007 636 / #0009 1,071 @ T+7.8h; duplicate z_s5j5hTMOg still PUBLIC (0 views, delist = open boss Studio action; scope re-verified upload-only, no re-consent → bait comments still 403). **#0011 staged = fiction test #2, "The Value System"** (boss day-022 brief #2, refined to intown specs, lint pre-clear PASS; evening session owns the build+publish so the Nov 21 fork gets a second fiction row). Median 24h ≈ 1.1-1.15K — above the fork's 1K trip line but thin; #0011's row decides.

- **Day-023 20:00 (boss directive, additive to the evening session):** larpniverse
  canon dissection landed (research/larpniverse-canon-dissection-2026-11-19.md — 12
  boss-supplied videos decoded; **huss-huss = the town chant**, spoken "hush hush
  hush" / captioned HUSS!, trend peaking on TikTok, YT-native lane empty; canon WPM
  187-213 re-validates the house band). **#0012 STAGED = fiction test #3, the
  huss-huss test: "In this town, everybody parties except me" (The Last Guest)** —
  canon skeleton + our dark twist, 139w/16 beats, lint PASS. Build = post-fork
  session's call (Nov 21 fork decides lane; #0011's row is its input). Cast law:
  ours (neighbor/paperboy), never theirs. L-133/L-134 lessons banked.


## Phase C — Scale what works (Day 022–030, Nov 22–Dec 1)

- Double the best formula-hook combo (2 Shorts/day OK if the gate stays green; never lower the bar to ship more).
- Long-form (8–12 min, 2×/week) ONLY if 10+ Shorts live AND best 24h median ≥2K views. Long-form = 3 shorts-worth of beats around one spine, 7-beat formula.
- Batch Sundays: Mon–Wed scripts+VO; weeknights render.
- **Day 30 scoreboard (Dec 1):** 10+ Shorts live, one >10K outlier, engine at 8/10 floor, 30 ledger entries. Miss 2 of 4 → Phase D becomes a boss strategy session.

## Phase D — Compound (Day 031–037, Dec 2–8)

- Double the winner, kill the losers; Shorts outlier → long-form funnel from its best hook.
- No outlier → boss conversation with data (formulas, hooks, retention curves).
- Week of Dec 7: mine all 30 days → engine-v4 spec.

## Risk register (pre-decided responses)

| Risk | Signal | Response |
|---|---|---|
| Sandbox recycle | `.git` missing | `bash /home/z/my-project/scripts/restore_workstation.sh --from-upload` (~2 min, proven 5×) |
| OAuth refresh dies | upload 401 | boss re-verifies the Google app (project nura-health) |
| Bot-wall blocks queue head | blocked N days | rotate queue; radar continues on RSS/oEmbed |
| ASR quota flake | empty verify lines | 2s backoff, accept documented biases (L-066) |
| Gate loop spirals | >3 ultracritic rounds | carry with report; next session pays the debt |
| Views flatline <100 | Phase B data | formula rotation, not premise doubt (L-060) |
| Boss unavailable | forks blocked | pre-decided forks execute automatically |
| ffmpeg wrapper noise | exit 255 post-success | verify artifacts, not exit codes (day-010) |

## day-024 (Nov 20) — #0011 SHIPPED at the format ceiling; #0012 build-ready

- **#0011 published** (1jSxHM4r00I, 22:52Z) under producer authority at combined
  7.19-7.35 across 5 rounds (zero stable defects, wander-class floors, L-085
  ceiling ~7.4 frame; rationale in published.json). The Phase C fork's second
  fiction row: ~46h of data at the Nov 21 fork session.
- **#0012 build-ready**: boss's option-3 craft notes baked (s5b returned-guest clue,
  s4 chant practice, s12/s12b "making sure I'd say yes" closer), VO measured
  (53.02s total, per-line rates), lint PASS (delivery WPM 186.0). Build = the next
  session's job IF the fork says fiction; the script survives either way.
- L-135/L-136/L-137 appended (ffmpeg teardown-hang recipe; duplicate-cron physical
  guards; delivery-WPM metric).

## day-030 (Nov 25) — 5-day gap closed; fiction fork input COMPLETE; #0013 pivots the look

- **Cron outage**: agent-wake cron dead since Nov 20 20:30 (Actions lane never
  died). 5-day views rows complete. #0012 shipped day-025 (BuiZ_hg48K0, L-115b
  path), r2 debt paid day-030 (7.29, hook 9.0, L-144).
- **Fork input is now complete and it says PIVOT, not quit**: fiction rows are
  1227 / 369 / 105 (48h flatline each) — BUT the flatline correlates with our
  DARK look (lum ~0.3) vs the 20-performing-short bible band (lum 0.43-0.54,
  sat 0.38-0.65) and with zero dialogue friction in all three scripts.
  #0013 = fiction lane, "in this town" grammar kept, but built on the
  bright-3D world preset + escalation-dialogue beats per
  research/friend-skill-cartoon-3d-short.md (world relight is step 1; camera
  ease-out bursts step 2; word-captions + bed −8 dB step 3). If the relit
  look's first short also flatlines, the lane dies for real and the science
  lane (Krakatau-class, blueprint lane live in Actions) takes the slot.
- **Disclosure policy (day-030)**: uploads default to NO synthetic flag;
  boss Studio-checks the three live videos manually if a label shows there.

## day-031 (Nov 28) — FORK VERDICT EXECUTED: fiction lane dead, science lane takes the slot

- **#0013 relit verdict (T+61h): 22 → 108 → 133 → 133 flat.** The bright-3d look did
  NOT break the fiction flatline (same pin shape as #0012's 55→100→105). Per the
  day-030 pre-registered fork: the fiction lane dies; science takes the slot.
  Reading: the PREMISE lane owns the flatline, not the look — #0013's gate was the
  channel's second-best ever (7.20) and it still pinned, so quality was not the
  blocker either.
- **#0014 STAGED same-session**: "The stitches doctors never remove" (backlog rank-2,
  dissolve story, sequel grammar to #0006 the #1 performer). Script 14 beats/110w/40.07s,
  lint PASS, critic r1 PASS (agent-judged), VO 13/13 ASR-clean FIRST run (no union
  debt), WPM 199.7 dead-center. Carry_r0: world (from #0013 engine) -> render ->
  gate -> publish.
- **Scheduler**: job 549218 reinstated agent-side (cron tool recovered). Fires
  09:45/23:45 EAT. Caveat: 5 fires through Nov 28 morning produced ZERO session
  commits — sessions die mid-loop; if day-032 shows no session commit, cron is
  unreliable platform-side and the loop falls back to boss pings.
