# Playbook — Render & encode (stage 5 of 7)

> Purpose: turn scenes.html into frames (gate probes first, full pass only when
> the gates are green) and encode the final mp4.
> Inputs: `render/scenes.html`, `script.json` (synced timeline).
> Outputs: `gate/*.png` (keyframes), `render/probe_*.png`, `render/frames/`,
> and (with stage 4) `<slug>.mp4`.

## Commands

```bash
# Gate keyframes (scene midpoints; 3 per scene if >4.5s + end-state probes):
python3 tools/render_short.py <slug> --keyframes
# Arbitrary probe frames (word-timed beats — rule: probe at the beats, L-065):
python3 tools/render_short.py <slug> --times 3.2 7.9
# Full pass ONLY after vlm_gate is green (render budget guard):
python3 tools/render_short.py <slug> --full            # add --resume if frames exist
```

How it works: `render_short.py` injects the synced timeline from script.json
into scenes.html (`__TIMELINE__` / `__T_END__` → `scenes.built.html`), then
drives `renderFrame(t)` via Playwright at 1080×1920 and screenshots. Every
frame is a pure function of t (rule C6) — this is what makes renders resumable
(`--resume`) and the #0003 post-recycle autopsy possible.

Encoding lives in `tools/finish_v3.py` (stage 4): `cat frames | ffmpeg
-f image2pipe` → h264 crf18 + AAC 192k + faststart. **Never encode a 1000+ frame
set with the image2 demuxer** (L-072 OOM — permanent pipe-encode in code).

## Known failure modes

| Symptom | Cause | Fix |
|---|---|---|
| fonts timeout message | Google Fonts offline | falls back to system faces; check the frame — if the display face is missing, bundle it locally |
| render dies partway | sandbox/OOM | `--full --resume` skips frames already on disk |
| probe shows blank/JS error | scenes.html runtime error at that t | `tools/probe_frames.py` catches JS errors; fix scenes.html |
| heavy scene ~3.6 s/frame | 200+ sprite objects (birds class) | acceptable nightly; sprite cache is the v4 fix — don't block cadence |
| gate flags "missing asset" | beat unsampled | probe at the beat's word time (`--times`), not uniform u25/60/90 (L-065) |

## Acceptance check

- `--keyframes` produced a PNG per scene (+ end probes) with no blank files.
- Full frame count ≈ `(total_s + 0.45) × 30`, files ≥ ~1 KB each.
- Re-render of one t is byte-identical (determinism spot check).
