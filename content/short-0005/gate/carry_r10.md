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

## Studio reconciliation (session B, same day — read before acting on the blocker above)

- **The OAuth grant is NOT dead — the CI secret is a stale copy.** The verdict
  above tested the Actions secret `YOUTUBE_TOKEN_JSON` (and a fresh-machine
  box with no mirrors). The durable mirror `upload/token.json` refreshed
  200 OK before AND after the CI probe (studio probes 14:1xZ and later;
  CI invalid_grant 14:23:16Z) — two different copies, two different states.
  Filed as L-105 ("a token copy is not the token"). Consequences:
  - NO re-consent is needed to publish from the studio
    (`tools/youtube_upload.py --token-file .secrets/token.json`, seeded from
    the live mirror).
  - The CI path is FIXED (studio, 14:49Z): all three secrets refreshed from
    the live mirror (YOUTUBE_TOKEN_JSON + GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET
    from the token's own minting client) — the PAT turned out to carry
    secrets-write. Verified end-to-end: dry-run run 43606867269 = SUCCESS
    (vs 43604597533 = failure on the stale copy 26 minutes earlier).
  - The real boss item is unchanged: nura-health app → **Production**
    (Testing mode kills the day-011 refresh token ~Nov 19 — every copy,
    mirror included, dies then).
- **r10/r11 do not satisfy carry_r9 D1.** Those rounds ran on a substitute
  judge (glm-4.5v via OpenRouter) with 3 frames unscored per round and an
  agent-judged video pass; this file's own calibration note says the numbers
  are not comparable to r1–r9. The clean two-round decision still fires at
  **23:45 EAT on the studio judge** as **r12/r13** (runbook in carry_r9.md;
  the studio's z-ai VLM was verified live this afternoon — 4 successful
  vision calls during the s6 D2 probe).
- **D2 is done** (session B): s6 hero-1.2 + stamp-to-crest-void probe =
  NOISE (mean −0.25; vh +1 at settled t, cl −1 at both) — current
  composition holds. Evidence: gate/s6_variant_probe.json, tools/probe_ab.py.
  The "D2 named, not run" debt above is closed.
- **D3 merged**: both sessions fixed the dead linter dispatch independently;
  the merged script_linter carries session A's 3-tuple wiring + the studio's
  L-097 VO ladder / at-floor warn / per-token L-090 + tools/lint_selftest.py
  (10/10 green). #0003 fails at lint as designed; #0004/#0005 pass.
