# AGENTS.md — runbook for coding agents on this repo

The fresh agent's job lives in `docs/plan-30d.md` + `docs/playbook/`; this file is
**the machine-specific "how to even run anything here"** that `docs/` cannot know.
Everything below was measured on 2026-11-14 (CachyOS, fresh clone of `limitlessprojects/youtube-engine`).

## 1. First command on a fresh clone

```bash
bash bootstrap.sh --ci          # repo deps; will NOT give you chromium or a VLM
python3 -m pip install --user --break-system-packages -U playwright edge-tts yt-dlp
```

- `python3 --version` = 3.14; PyPI refuses system installs on Arch → `--break-system-packages`.
- Playwright's pinned `chromium_headless_shell` may not match the cache. Verify:
  `python3 -c "from playwright.sync_api import sync_playwright; ..."` or just run
  `tools/render_short.py <slug> --times 2.0`. If it errors with "Executable doesn't exist…
  chromium_headless_shell-12XX", symlink the cached one:
  `ln -sfn ~/.cache/ms-playwright/chromium_headless_shell-<cached> ~/.cache/ms-playwright/chromium_headless_shell-<wanted>`
  and likewise `chromium-<cached>` → `chromium-<wanted>`. (On this box: cache = 1254, wanted = 1255.)
- `sudo` is passwordless. Do NOT `pacman -S chromium`; Playwright's own build is what the repo renders with, and the box already has it.

## 2. The VLM problem (read this before you "just run the gate")

`tools/vlm_gate.py`, `tools/ultracritic.py`, `tools/probe_*.py` shell out to a `z-ai` CLI.
**The Z.ai account is out of balance** (error 1113 on every model). The tools run unmodified
if a `z-ai` executable exists on PATH. This box has `~/.local/bin/z-ai`, a shim that routes
`z-ai vision -p PROMPT -i IMG -o OUT` to OpenRouter `z-ai/glm-4.5v` (key from
`~/.local/share/opencode/auth.json` → `openrouter.key`). It works; it has not been calibrated
against the repo's anchor ladder — so: **expect frame scores to drift; the bar is still 7.5/7.0/6.0,
and you may need 2 rounds where the original machine needed 1.**

**Calibration note (2026-11-14):** on IDENTICAL frames, r10 **7.33** / r11 **7.63** (frame grand
7.11/7.27); per-frame deltas to ±2.0 (s8 4→6). Neither round PUBLISH_APPROVED (r10: vh 6.3,
floor s4/s6/s8; r11: hook_impact 6.0 <7, vh 5.3, floor hook/s4). The vlm_gate intent checks mostly
fail as `vlm_parse` — glm-4.5v answers with markdown fences and prose; extraction choked on 11/12
frames. Do NOT compare to the glm-4.6v ladder in `docs/lessons.md`. The bar did not move; the cut
did not get worse — the judge did.

The **video pass** (pacing_rhythm / character_life / edit_flow, REQUIRED) has no working
backend anywhere on this box: OpenRouter 402s video ($1 min), Z.ai is empty, Gemini key is dead.
`tools/ultracritic.py` now accepts `ULTRACRITIC_VIDEO_JSON=<path>` with
`{"scores":{"pacing_rhythm":n,"character_life":n,"edit_flow":n},"top3_directives":[…]}` —
an **agent-judged** video pass, recorded as `video_pass_source: "agent-judged (no video VLM
backend available)"` in the report. Use it, and label the judgment as yours. Dead-end D8 stands:
never present agent-judged temporal dims as a model's verdict, and never judge them from
mid-video stills without saying so.

## 3. Publishing (the machine you are on has no local YouTube token)

There is **no `.secrets/` here**. The repo's GitHub Actions secrets DO have
**L-105 correction (studio, same day): the "grant is dead" verdict tested a stale COPY.**
The durable mirror `upload/token.json` refreshes 200 OK; the CI secret was stale. All three
Actions secrets were refreshed from the mirror at 14:49Z (the PAT carries secrets-write) and
`publish.yml` **dry-run 43606867269 = SUCCESS**. So: publish path works from any box now — but
the bar is unchanged and you still need a green gate. The studio's two-round decision
(**r12/r13**, 23:45 EAT) is authoritative; r10/r11 (glm-4.5v, this box) are NOT the D1 verdict.
`docs/lessons.md` L-105; `gate/carry_r10.md` → "Studio reconciliation".

`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `YOUTUBE_TOKEN_JSON` (values unreadable by design).
So the publish path is CI, not local:

```bash
# 1) local: finish the bar; if PUBLISH_APPROVED, then
# 2) commit + push, then dispatch the manual workflow:
gh workflow run publish.yml --repo limitlessprojects/youtube-engine \
  -f slug=short-0005 -f title="…" -f privacy=public -f dry_run=true   # probe only
gh workflow run publish.yml --repo limitlessprojects/youtube-engine \
  -f slug=short-0005 -f title="…" -f privacy=public -f dry_run=false  # actually publishes
```

`publish.yml` re-renders in CI (deterministic, rule C6), finishes, uploads with
`containsSyntheticMedia=true`, sets the thumbnail (`content/<slug>/render/hook_*.png` is
committed, so it is available), writes `published.json`, pushes. It is **manual only** and has
a `dry_run` default of true — never dispatch `dry_run=false` without a green gate.
Thumbnails need channel phone verification; a 403 there is survivable (video stays live).
`tools/youtube_upload.py` gained `--id-file` so the workflow can hand the video id to the
thumbnail + record steps.

If you DO find a local token (`/home/z/my-project/.secrets/token.json` or the boss hands you
one): `python3 tools/youtube_upload.py --check-token` FIRST (L-084: refresh grants die
silently), then upload with `--token-file`, then `--set-thumbnail VIDEO_ID:img.png`.

## 4. Git auth

`origin` = clean HTTPS URL (no embedded token — never re-add it).
`~/.config/opencode/.secrets/github_token` (= the PAT the boss gave, belongs to user
`limitlessprojects`, scopes: `repo`, `workflow`, `admin:*`, etc.) is mirrored into git's
credential store at `~/.config/opencode/.secrets/git-credentials` (mode 600,
`credential.helper=store --file=…`). Clone/push/dispatch all work. **Never print, log, commit,
or store the token itself in memory/docs/notes.**

## 5. What is gitignored that you'll still want

`*.mp4`, `content/*/render/frames/`, `content/*/gate/*` (except the committed few),
`content/*/*.mp4`. So: **a finished cut does not exist in git on a fresh clone — re-render it.**
Frame count ≈ `(total_s + 0.45) × 30`. `--full --resume` after any interruption.

## 6. The AI re-render route (ZeroGPU anonymous — day-017 boss directive)

The ONLY anonymous GPU route listed in the repo: HF Space `alexnasa/Wan2.2-Animate-ZEROGPU`
(Wan2.2-Animate `/animate_scene`, `Character Swap`, per-IP quota ~160 GPU-s, no token needed).

- `tools/hero_shot/ai_rerender.py` — our own minimal gradio_client driver (NOT vendored from
  the mr-bean repo). One 2 s chunk per call; `--attempts 2`; on quota → exit 4 (a fresh runner IP
  has fresh quota — that is the whole point of the GitHub Actions matrix).
- `tools/render_short.py --frames A B` renders a frame window only (chunk rendering on runners).
- `tools/finish_v3.py --audio-only` rebuilds `vo/master.m4a` without video (collect step remuxes it).
- **Full census of anonymous GPU routes: `research/anonymous-gpus.md`** — 1,320 ZeroGPU spaces (171 video-ish), 2 GPU-min/day/anon-IP (shared), fresh-IP matrix = the only multiplier; Wan2.2 FP8 AOTI (3871❤), Saravutw 4–8step (426❤), kulkas2pintu/wan777 & LTX-2-3-First-Last-Frame for loop mirrors; verify licenses (Hunyuan AVOID, MiniMax-H3 proprietary, SVD AVOID, NSFW Civitai LoRAs off-limits).
- `.github/workflows/ai-rerender.yml` — manual dispatch only; 19 × 2 s windows re-render
  deterministically (C6), AI-re-render them anonymously on fresh runner IPs, assemble verifies
  ALL chunks exist (no silent partial cuts), upscales 1080×1920@30, concats, muxes audio,
  uploads artifact `ai-full` (7-day retention). Nothing is uploaded to YouTube, ever, by this path.

Hard truth learned in probe (gate/s3, 2026-11-14): the model preserved our stickman + scene remarkably
well BUT **text stamps DRIFT** — `180 dB` → `190 dB` — and pacing morphs subtly. This route is a
boss-directed experiment, not a gate path: the deterministic render is the canonical cut. Never ship,
gate, or publish an AI re-render without the boss's explicit sign-off, and never trust its on-screen
words. Also never re-dispatch just to re-roll — one run eats the free plan's whole 20-runner quota.

## 7. Advice for whoever comes next

- This repo is run by MULTIPLE concurrent agent sessions (studio + fresh-machine opencode).
  Before every commit: `git fetch origin && git pull --rebase` — and re-read what changed
  (session B independently fixed the same linter bug same-day; both merged cleanly except a
  conflict marker left INSIDE the docstring, which I cleaned). Keep commits small and atomic;
  never push over a sibling's unreviewed work; write your ledger entries as additions, not edits.
- The boss asked this box to publish, not just build — but the box's gate is not the verdict.
  The D1 two-round publish decision on #0005 fires on the studio judge (r12/r13). Don't touch it.

- The boss authorized building the publish path; the publish decision is the studio gate.
- Do not fabricate views/scores/transcripts. The RSS bot-wall 404s from this IP; `views_tracker`
  is behind a wall — say so.
- The open gate weakness is still visual_hierarchy (format-level, L-085). Don't burn rounds.
- `tools/script_linter.py` had a latent bug: `main()` flattened JSON to plain text and then
  re-parsed *the flat text* for the structure block, so every L-073/075/077 check was dead
  code on the CLI path. Fixed (parse once, thread the payload through). CLI now really
  enforces orientation, pacing, spine, **L-090 digits-in-narration** and the **L-097
  beat-count law** (beats ≥ ceil(VO_seconds/3.2)). Sanity: #0003 fails with the documented
  4.22s/5.90s pacing, L-097 (8 < 11) and the L-077 'Mars' closer warning; #0005 and #0004 pass.
- Keep the paper trail: commit the `gate/ultracritic_r*.json`, write the ledger line in
  `docs/lessons.md`, and `contextm` a `session_note` at every decision.
- If the YouTube refresh grant is dead (`--check-token` FAIL), the fix is the boss re-verifying
  the Google app (`nura-health`) is in **Production**, not "try again".

## 8. The boss's Top-10 highest-leverage upgrades (day-017, research/video-notes/TOP10-UPGRADES.md)

Authority: web-swept (YouTube blog/Help; 2026 Shorts algorithm deep-dives; Artificial Analysis TTS boards;
Springer/Heliyon/Frontiers/BMC retention science; Wan2.2/Veo/Kling/LTX comparisons) cross-checked against our corpus.
Order = ship order. Full provenance: `research/video-notes/TOP10-UPGRADES.md` — read it first next session.

1. **Measure before render** — `tools/motion_probe.py` mandatory per Short; target <3 re-render cycles per upload; log failures, don't drift.
2. **Foreground hook** — question/promise as the first spoken line; title = promise; audio-led opens count; per upload, watch Studio "How many chose to view" (<25% → kill that premise shape).
3. **One signature world** — same palette/register/motion grammar every Short (Kurzgesagt proof); WIP `engine/space.py` + `engine/diagram.js` icon families; no mixed vector routes.
4. **Length discipline** — Shorts algorithm weights constant with duration; 20–40 s is the sweet spot; cut hard topics to <30 s (~150 wpm); no CTA before the premise lands.
5. **Caption policy** — no narration captions; stamps only; never burn numbers on screen; L-090 holds.
6. **Voice reality** — Fish Audio works; ElevenLabs Starter ($6, commercial license) is the A/B candidate; never clone before 10k words of catalog.
7. **Silence is a feature** — silence/instrument-hits > synth-pad beds; one 2s swell per 12 beats; let the quote-time ride dry.
8. **Clarity > novelty** — Heliyon PRISMA 40-study; TED clarity β=.339; no Short ships with a confusion point; L-097 3.2s floor enforces.
9. **Hero-shot discipline** — community pass (reddit, CANDIDATE): Medium-Res only; AR-match input; frames-skip=0; quantization kills likeness first; C16 exceptions only.
10. **Cadence beats spectacle** — one structural edit per publish; no delete-and-republish; re-uploads via Studio description edit only; weekly retention re-read, not merge-batch review.
