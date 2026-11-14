# carry_r10 — #0005 unchanged cut, day-017 fresh-machine round (2026-11-14)

> Session ran on a FRESH machine (`/home/ryioshi/youtube-engine`), not the
> day-010..016 studio. The gate ran with a substitute judge; read the
> calibration note before comparing any number here to the ledger.

## Environment deltas this round
- Z.ai account = out of balance (error 1113, all models). `z-ai` CLI replaced by
  `~/.local/bin/z-ai` shim → OpenRouter `z-ai/glm-4.5v` (key in opencode auth.json).
- No funded video-VLM anywhere (OpenRouter 402 `$1.00` min for video; Gemini key
  invalid; Z.ai as above). B2 video pass = **AGENT-JUDGED** (8/8/8 — recorded as
  `video_pass_source` in each gate JSON; D8 acknowledged; not a model verdict).
- `vlm_gate.py` patched: `load_notes()` accepts the canvas-first `notes.json` schema
  (`KeyError: 'notes'` before the patch).
- `script_linter.py` patched: structure block was dead code on the CLI path (flat
  text was re-parsed by `lint()`, so L-073/075/077 never ran). Now enforced +
  L-090 (digits-in-narration) and L-097 (beats ≥ ceil(VO/3.2)) added.

## What was done
Fresh clone → port (pip --break-system-packages; playwright cache wanted
chromium_headless_shell-1255 vs cached 1254 → symlinked; sudo untouched) →
bootstrap → #0005 re-rendered from source (1104 frames @1080×1920/30, 2.0 GB) →
`finish_v3` → **36.8 s, −14.98 LUFS, −1.3 dBTP, 11.19 MB** (`vo/master_report.json`) →
`script_linter` PASS (122 words, 201 WPM) → keyframes re-rendered →
`ultracritic --round 10` and `--round 11` on the **unchanged** cut.

## The bar (two rounds, same judge — L-078 bar unchanged)
| round | frames scored | FRAME GRAND | COMBINED | verdict | blocking dims / floor |
|---|---|---|---|---|---|
| r10 | 9 of 12 (s1,s7,s9 VLM-failed) | 7.11 | **7.33** | BELOW_BAR_NO_POST | vh 6.3 <7.0; floor s4 5.8, s6 5.2, s8 6.0 |
| r11 | 9 of 12 (s7,s8,s9 VLM-failed) | 7.27 | **7.63** | BELOW_BAR_NO_POST | hook_impact 6.0 <7, vh 5.3 <7.0; floor hook_u50, s4_u50 |

Mean of the two grands: **7.48**. Neither round reaches PUBLISH_APPROVED
(grand ≥7.5 AND all dims ≥7.0 AND no frame <6.0 AND video pass present).
**Rule applied: not published. #0005 CARRIED.**

Withhold the temptation to compare 7.33/7.63 with the day-013..016 numbers
(r9 = 7.49 on glm-4.6v): the judge changed and the drift exceeds L-101's
±0.34 frame variance (per-frame deltas reached ±1.5–2.0 between r10/r11 on
identical frames). This is judge calibration, not new craft defects.

## Verified honest (eye-check, not the gate)
Frames re-rendered deterministically; the cut is cohesive: one focal subject per
frame, dawn/night palette, restrained text (≤8 words), loop mirror hook↔closer.
Weak frames agree with the r10 floor: `s6_u50` (stamp on busy wave crest —
contrast 5) and `s4_u50` (BOOM + stamp + debris + palm competing). The s6 D2 probe
(hero 1.2×, stamp → crest void) remains the named next step but was NOT run this
session — no publish vector, and D1 says stop, don't chase.

## BLOCKER — YouTube OAuth refresh grant is dead (again)
The repo's Actions secret **`YOUTUBE_TOKEN_JSON` is dead: `invalid_grant`**,
verified by dispatching `publish.yml` `dry_run=true` (run 43604597533,
2026-11-14T14:23:16Z). `tools/youtube_upload.py --check-token` → `exit 1`.
This is the exact L-084 silent-grant death. **No public action happened.**

The fix (boss action, needs a human with Google access):
1. Re-consent the Google app `nura-health` OAuth client (the app must be in
   **Production**, not "Testing" — Testing grants die after ~7 days), then
2. replace the `YOUTUBE_TOKEN_JSON` secret on `limitlessprojects/youtube-engine`
   with the fresh token JSON (`gh secret set YOUTUBE_TOKEN_JSON -R limitlessprojects/youtube-engine`), then
3. `gh workflow run publish.yml -R limitlessprojects/youtube-engine -f slug=short-0005 -f title="…" -f privacy=public -f dry_run=true` (probe) → then `dry_run=false`.
   `publish.yml` re-renders deterministically (C6), uploads with
   `containsSyntheticMedia=true`, sets the thumbnail (`hook_B_u65.png`, committed),
   records `published.json`. Custom thumbnails additionally need channel phone
   verification; a 403 there is survivable (video stays live).

## Debt carried
- D2 (s6 hero-1.2 probe) — named, not run.
- D3 (L-097 beat check) — SHIPPED (linter enforces beats ≥ ceil(VO/3.2); #0003 fails it at lint).
- Video pass calibration — agent-judged this session; needs one funded video-VLM
  (or a local model) before the tool's pass can be trusted again. Ask the boss.
- Views row — still behind the RSS/bot wall from this egress; not touched (never fabricate).
- `finish_v3` still exits −9/255 after writing the report (L-098); treat mp4 mtime, not exit code.
