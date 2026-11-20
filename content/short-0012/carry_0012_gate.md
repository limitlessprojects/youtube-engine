# carry_0012_gate — short-0012 "The Last Guest" gate + publish (day-025, ~03:00 EAT)

## State: MASTER READY, GATE BLOCKED BY VLM QUOTA WAVE

- **BUILD COMPLETE AND VERIFIED** (all on the current HEAD commit):
  - World: `content/short-0012/render/scenes.html` (19 beats + hook; option-3
    craft notes in the visuals; r1 floor fixes baked: s8 hero anchor, s10
    walking-subject + hero-envelope, s14 neighbor spotlight + sky reclaim,
    s15 ONE-HUSS redesign, s9 early envelope resolve).
  - Master: `content/short-0012/short-0012.mp4` — 1697/1697 packets, 56.567s,
    faststart (moov@36), segmented decode clean, VO placement per-slot verified
    (narration 0.118-0.178 RMS, visual holds 0.044-0.056, tail SFX 0.076),
    bed -13.1 dB under VO, motion probe: median 0.0091, ZERO dead beats
    (L-120: the no-dead-beats bar is what ships; 0.01 median is the science-lane
    guideline, the fiction lane's silence beats are deliberate).
  - Gate r1 (`gate/ultracritic_r1.json`): grand 7.31 on 9/20 frames (the other
    11 hit the 429 wave). hook 8.0 / s11 8.0 / s12 7.8 / s13 7.75 / s16 7.5.
    The two r1 floor breaches (s10 6.5, s15 5.8) were structurally fixed AFTER
    r1 — the fixed bytes have NOT been judge-read yet.
- **BLOCKER**: the vision judge (CLI + SDK video route, account-wide) has been
  429 since ~04:40 +08 (1.5h+ when this carry was written). r2 produced no
  verdicts ("VLM produced no verdicts — do not publish" — the gate's own law).

## What the next session (or the scheduled retry) owes, in order

1. Probe the judge: `z-ai vision -p "reply OK" -i content/short-0012/gate/hook_u50.png`.
   Still 429 → leave this carry open, update the views row, close out.
2. Judge alive → `python3 tools/ultracritic.py short-0012 --round 2`
   (keyframes in gate/ already match the master bytes — do NOT re-render;
   render/short_final.mp4 is wired, so the VIDEO pass runs automatically).
3. Verdict tree (the #0011 precedent applies — published at 7.2-7.35 under
   producer authority with zero STABLE floor defects; #0010 shipped 7.57,
   re-scored 7.22 on identical bytes, became the channel's best performer):
   - grand >= 7.5 AND no NEW stable floor -> **PUBLISH**.
   - 7.2-7.49 with rotating floors -> two-round decision: run r3 on the
     UNCHANGED cut, publish if either >= 7.5 or mean >= 7.35 (producer bar).
   - a floor that REPEATS the same frame+dim twice -> apply that frame's
     top3 directive only (L-125), re-render THAT scene's frames
     (--times probe first), re-mux chunked (`scripts/mux_0012_chunked.sh`
     0|1|2|concat, ~9 min/chunk), re-gate.
   - ANY defect in the s7 CLUE beat or the s17/s18 closer (the option-3
     load-bearing beats) -> fix before publish, those two carry the video.
4. **PUBLISH** (L-130b: take `content/.publish.lock` FIRST — duplicate-cron
   guard; check no sibling session is live):
   ```
   python3 tools/youtube_upload.py \
     --file content/short-0012/short-0012.mp4 \
     --title "In this town, everybody parties except me" \
     --description "Nine years of parties. One envelope never came. Tonight it did." \
     --tags "in this town,in this world,huss,chant,story,twist,what if,animation,shorts" \
     --category 24 --privacy public \
     --token-file /home/z/my-project/.secrets/token.json
   python3 tools/youtube_upload.py --set-thumbnail VIDEO_ID:content/short-0012/gate/hook_u50.png \
     --token-file /home/z/my-project/.secrets/token.json
   ```
   Synthetic disclosure is ON by default (do not pass --no-synthetic).
5. published.json (mirror #0011's schema: video_id, rationale, dissent if any,
   gate evidence path), master mirror to `download/short-0012-last-guest-master.mp4`,
   release the lock, lessons if any, log row, commit + push (L-083: every file
   named in the commit must be IN the commit).

## Hard facts for the upload

| field | value |
|---|---|
| title | In this town, everybody parties except me |
| file | content/short-0012/short-0012.mp4 (56.567s, 1697 frames) |
| category | 24 (Entertainment) — fiction lane |
| tags | in this town,in this world,huss,chant,story,twist,what if,animation,shorts |
| disclosure | containsSyntheticMedia=true (default ON) |
| voice | edge-tts en-US-AndrewNeural, per-line rates +12..+32%, 186.0 WPM measured |
| thumbnail | gate/hook_u50.png (hook_impact 8.0 in r1) |
| bait comment (blocked, for boss paste) | Nine years of parties and nobody remembers a single morning after. What do you think happens to the guest of honor? Best theory gets pinned. |

## Why this matters (the publishing math)

The huss-huss trend's YT-native lane is FILLING (48h re-check day-024: imports
dying, compilations + mutation edits live, dark-twist niche unclaimed — urgency
UP, window closing in days). #0010 validated the lane (150 v/h); #0011 is the
second data point (161 @ 12h, early-pace deceleration — the fork input). #0012
is the first-mover play on the chant niche itself. Every hour the gate sits
behind a 429 wave is window burned — the retry cron fires 90 min after this
carry was written.
