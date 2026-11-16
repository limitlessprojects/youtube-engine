# Handoff — day-018 (2026-11-16, fresh machine `/home/ryioshi`, Claude Code)

> Reader: the next agent. Read this after `AGENTS.md`. It records what this session
> changed, what it could NOT do, and the working method that produced the #0006 v3 cut.
> Status lines marked **VERIFIED** were checked this session; everything else says how
> it was (or was not) checked.

## 1. What happened

- #0006 (stitches) was sitting CARRIED at 6.72 / 6.61 with three polish directives.
  I did not run a third polish lap. I looked at the frames and the problem was the
  design, not the details: a navy dermis on a navy sky with a 13 px thread and a tiny
  hero. Nothing owned the frame (C2, C3, L-085, L-112 all at once).
- Rebuilt the scene file from zero: `content/short-0006/render/scenes.html` (v3).
  The carried version is kept beside it as `scenes.v2-carried.html` for comparison.
- Script, fact sheet and VO are UNCHANGED (same 12 mp3s, same timeline). Only the
  title changed: "The thread doctors hide under your skin" (old title is in
  `script.json → title_history`). The linter's L-073 rule forced the word "thread" /
  "doctors" — the first title I wrote failed it, which is the rule doing its job.
- `script.json` now carries a per-short `sfx` table (28 cues timed to the new visuals)
  and `gate/notes.json` describes the v3 intent.

## 2. The design that worked (reuse it)

**One lit object, one continuous take.**

1. Pick the single object the whole explanation lives on, and make it bright on a dark
   room. Here: a textbook skin block — top face is the skin surface in perspective,
   front face is the cross-section. Light flesh on navy passes C2 by construction.
2. Let the object run off the bottom edge. The lower 20% is covered by the Shorts UI
   anyway; a subject that continues past the frame cannot leave a "dead band".
3. Scenes are camera moves on that object (`SC.<id>.cam = [start, end]`), joined by a
   0.36 s eased whip from the previous scene's last camera. No set changes, no fades.
4. State is a plain object per frame (`S0()` → `open(z)`, `xray`, `scanZ`, `th`,
   `seam`, `cells`, …). Each scene only fills in state; `block(S, t)` draws everything.
   Adding a scene is ~15 lines and cannot break another scene.
5. Make the claim literal. "Under the surface" is drawn as layers: dermis underlayer →
   wound → under-skin objects → skin cover. X-ray is the cover turning translucent.
   No label is doing the work the picture should do.
6. One cool accent (teal thread) against a warm subject. The old cut had amber thread
   on violet tissue at similar value — it vanished.
7. First frame == last frame (open wound, needle poised, same title) so the loop is
   seamless and the thumbnail is simply frame 0.

`pr(x, z, d)` is the whole "3D": x∈[-1,1], z∈[0,1] front→back, d px below the surface.

## 3. Tools added

- **`tools/contact_sheet.py`** — renders probe frames and tiles them into one JPG.
  `--scenes` (2 per scene), `--every 1.5`, or explicit times; `--errors` walks the
  timeline at 0.25 s and prints JS exceptions. An agent that can read images reviews a
  whole short in 3 reads. This replaced per-frame VLM calls for iteration: ~10 s per
  sheet, no API cost, no ±0.8 judge noise (L-080/L-101). Use the VLM gate for the
  record, use your own eyes for the loop.
  Sheets are downscaled — open one probe at full size before trusting small text.

## 4. What I could not do — be honest about these

- **ASR verification of the VO is still open.** `faster-whisper` does not install on
  this box (Python 3.14, ctranslate2 has no wheel); the `z-ai asr` shim is not
  implemented. The mp3s are the day-017 set and were never ASR-verified (12/12 empty
  that night). Nobody — human or model — has confirmed the words by ear in a logged way.
- **No model-judged gate ran on v3.** Frame review was done by me (the agent) from
  contact sheets. That is an agent judgment, not an ultracritic verdict (dead-end D8).
  The temporal dims in particular were judged from stills + the motion code, not from
  watching the video.
- See §6 for the publish state at the end of the session.

## 5. Advice

- Look at the frames before reading the directives. Three rounds of written
  directives on #0006 were all true and all beside the point.
- When a gate dim is stuck across rounds, change the format, not the parameters
  (L-085 said this already; it took a rebuild to act on it).
- Full render here is ~1.4 s/frame (≈ 27 min for 39 s). Iterate on sheets, render
  once. Clip paths and per-frame gradients are the cost.
- The scratchpad under `/tmp/claude-*` is wiped between days. Anything you want
  tomorrow goes in the repo.
- `V2.grade()`'s vignette (0.82) crushes a bright subject into an oval once the
  camera zooms. v3 draws its own 0.5 vignette; consider lowering the engine default.
- `V2.Hero` time arguments: older scenes pass frames, v3 passes seconds. Check which
  one a helper expects before copying idle-motion code.
- Credentials: never paste a token into a command line. This harness blocks commands
  that read `~/.config/opencode/.secrets/*` into variables — use git's credential
  helper (already configured) and let the human run anything that needs the raw PAT.
