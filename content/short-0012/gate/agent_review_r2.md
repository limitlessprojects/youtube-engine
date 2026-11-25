# #0012 "The Last Guest" — agent review r2 (D8), 2026-11-20 ~15:40 EAT

**This is NOT an ultracritic verdict.** The model API is down ACCOUNT-WIDE since
~04:40 +08 (16h+): z-ai vision (CLI video route), SDK createVision (glm-4.6v),
AND the plain text chat route all return 429 — the outage is not vision-pool-
specific and shows no reset sign. `ultracritic.py --round 2` cannot run.
What follows is the agent's own reading of the 20 gate keyframes (Claude, via
contact sheets `gate/sheet_A.jpg` + `gate/sheet_B.jpg`, tiled from the master
bytes), recorded per L-115b / the #0006-v3 precedent so nobody mistakes it
for a model score. Probe log: this carry, below.

## Mechanical (measured, from the day-025 build + today's re-verify)
- Master `content/short-0012/short-0012.mp4`: 1697 packets, 56.567s, faststart,
  segmented decode clean; today re-mirrored from `upload/short-0012.mp4`,
  ffprobe duration 56.566667 — byte-identical logistics, L-140 recipe.
- VO placement per-slot verified (narration 0.118–0.178 RMS, holds 0.044–0.056,
  tail SFX 0.076); bed −13.1 dB under VO; motion probe median 0.0091, ZERO dead
  beats; 186.0 WPM measured; keyframes re-rendered FROM THESE BYTES today.
- Gate r1 (model, 9/20 frames before the wave): grand 7.31 — hook 8.0, s11 8.0,
  s12 7.8, s13 7.75, s16 7.5; floors s10 6.5 / s15 5.8.

## Agent reading of the frames (no numbers claimed against the 7.5 bar)
r1's two floor breaches are FIXED IN THE SHIPPED BYTES:
- **s15** (was 5.8, huss-plate clutter): exactly ONE red "HUSS!" plate above the
  crowd at the golden wall — the ONE-HUSS redesign landed; nothing clutters.
- **s10** (was 6.5, no subject/anchor): dark hero now WALKS the mailbox row,
  gold envelope present at frame left; the nine-years-of-envelopes composition
  reads. Mid-zone contrast is modest at tile scale — the one frame I would
  nudge if a re-render were free (envelope glow +10%); not a floor defect.
Load-bearing beats all read:
- **s7 CLUE**: the gray/pale returned guest sits INSIDE the warm-lit waving
  group, crescent moon above — legible at 216 px, the option-3 visual clue works.
- **s12**: envelope macro with red seal fills the frame — strongest frame in
  the cut, r1's 7.8 plausible-to-conservative.
- **s17/s18 closer**: hero + gray guest together at the open door (s17), warm
  crowd + small high "HUSS HUSS HUSS" chant plates walking-out shot (s18) —
  the whisper-tail lands visually; no epilogue needed.
- **hook/s0–s9**: subject ownership consistent, gold-envelope accent is the
  through-line, palette orange/blue-gray per bible; s4/s5 practice beats read
  ("WAVE BOW", "4s TOO SLOW"); s9's dark envelope-in-slot resolve is deliberate
  negative space (fiction lane, L-120 note).
- G9: no basic-shapes reads — faces, hands, posture, collars/ties everywhere.

## Publish decision
Boss instructed publish twice today ("next day is here did you publish no 12").
The model gate cannot run (16h+ account-wide outage incl. the text route).
Under producer authority + L-115b (agent-with-eyes is the sanctioned judge
outage path, #0006-v3 precedent) + the #0011 precedent bar (7.2–7.35 published,
zero STABLE floor defects): **PUBLISH**. Mechanical checks on the exact shipped
bytes are green; the agent read finds zero stable floor defects; r1's floors
are structurally fixed in these bytes. A later session with a live judge owes
round 2 on the LIVE cut (video pass wired) and files the number here.

## ADDENDUM (day-030, judge returned as glm-5.3-flash) — the owed r2 number

ultracritic --round 2 on the LIVE cut ran day-030: **combined 7.29** (frame
grand 7.33; video dims pacing 7.0 / character_life 7.0 / edit_flow 7.0;
hook_impact **9.0 — channel record**; text_discipline 8.9; visual_hierarchy
6.2). Verdict file: gate/ultracritic_r2.json. BELOW the 7.5 machine bar, and
the below-floor frame set moved to s10/s12/s14/s1/s9 — vs r1's s10/s15 — on
identical bytes; s12 scored 7.8 under glm-4.6v and <6.0 under glm-5.3-flash
(cross-model wander, L-144). No re-render: the cut is 5 days live, floors
rotated across models, and the #0010 precedent (7.57→7.22 on identical bytes,
best performer) covers the noise band. The r2 video directives (idle-life
micro-motion in solo holds; trim ~0.5s off the envelope-storm hold; faster
final dolly-in) are REAL and queued for #0013's engine, not a re-lap here.
