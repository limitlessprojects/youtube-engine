# The publish runway (next session onward; 2026-11-14, session A)

Tooling shipped today (2026-11-14) wires the three failure-points from the plan-30d scoreboard (cadence,
thumbnail, topic) into mechanical tools + one ranked list:

## 1. Publish a Short (cadence path)

```
# local Mac path (boss's box):
bash bootstrap.sh --ci
python3 tools/lint_selftest.py          # 10/10 self-test REQUIRED
python3 tools/render_short.py <slug> --full
python3 tools/finish_v3.py <slug>
python3 tools/youtube_upload.py --check-token
# gate: python3 tools/ultracritic.py <slug> --round N   (boss bar)
# publish (pick one):
skyline: gh workflow run publish.yml -R limitlessprojects/youtube-engine -f slug=<slug> -f title="…" -f privacy=public -f dry_run=false
local   : python3 tools/youtube_upload.py --file content/<slug>/<slug>.mp4 --title "…" --set-thumbnail VIDEO_ID:content/<slug>/render/hook_*.png
# thumbnail sanity check MUST run first:
python3 tools/thumbnail_check.py content/<slug>/render/hook_*.png    # PASS + warnings ok; FAIL → fix or don't set
```

The manual CI path (`.github/workflows/publish.yml`) is authoritative for token-less boxes (AGENTS.md §3);
the local path is for the studio with `.secrets/` present. Disclosure (`containsSyntheticMedia`) is always on.
**Delete-and-republish is forbidden** — every republish re-seeds the audience from scratch and counts as spam.
Re-uploads happen via Studio description edit + a brand-new public Short only, never with the same ID.

## 2. Thumbnail logic (what we learned from #0005 + the thumbnail-check tool)

- The feed shows a Shorts grid tile (vertical); desktop/category surfaces use 16:9-like tiles. Studio accepts
  any aspect; the 1280×720 floor keeps desktop clean. VERTICAL thumbnails are set fine, same as our hook_B_u65.png.
- One readable foreground subject + at most ~6 words of type. Ours ships/stamps read at grid scale.
- Near-black or maroon dominant thumbnails **win attention in dark-mode grids** (.hook_B won that race).
  Use `tools/thumbnail_check.py` as a floor: FAIL = can't upload safely; lumStd<40 = weak silhouette.
- Never set a low-resolution or busy frame as thumbnail; the grid is the only reason a nobody finds us.
- Cost: thumbnail fetch happens with the publish push; if `thumbnails.set` 403s (phone verification),
  the video stays live and unblocks later with one command — thumbnail flops are survivable.

## 3. Topic selection (the corpus-calibrated ranker)

`tools/topic_score.py` ranks candidate Long-reads by additive keyword weights calibrated against:
- Zack D. Films anatomy lane (~255M/216M views across 5 corpus items) → `visceral` +20
- "Largest/first/most + a number" superlative lane → +12 (NASA record 177M; the print culture's 421M)
- Belief-correction 3.7x formula (MinutePhysics 236–251 wpm) → +15
- Everyday curiosity 8.7x lane ("Why don't birds…", our #0002) → +14
- Clarity-first sunsets lane (our #0003 1153) → +4 (vestigial track record, not a predictive claim)
**Scores are triage ordering, not predictions.** `research/topic-backlog.md` is the output; the list
resets each session as videos ship. Run: `python3 tools/topic_score.py candidates.txt`.

## 4. Topic → beat → engine mapping

Momentum: one topic leads one Short. Candidates that survive ranking get: corrected script (script_linter+
lint_selftest) → scenes.html (one hero + stickman + one stamp; C14 licensed assets only) → render →
finish (LUFS-14; silence budget first) → 3-gate ultracritic + video judge → thumbnail-check → publish.

## Red lines that block the runway

- lint_selftest not 10/10 → stop.
- gate below bar on the UNCHANGED cut → carry; no ship; no workaround re-render of the same cut.
- thumbnail_check FAIL → don't set; Shorts feed punishes it.
- Any corpus or external pixels composited that the boss didn't approve → never, period.
