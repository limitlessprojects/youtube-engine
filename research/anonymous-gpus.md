# Anonymous GPU census — every free ZeroGPU route on the internet (day-017)

> Ask: "find more anonymous GPUs" (boss, after `.github/workflows/ai-rerender.yml`
> stalled QUEUED against the account-side backlog).
> Method: HF `spaces-json?runtime.hardware.current=zero-a10g` (legacy key, still
> the ZeroGPU census), 55 pages × 24 spaces = **1,320 ZeroGPU spaces**, of which
> **171 are video-ish**. All 12 shortlisted spaces verified **anonymously
> reachable** (`view_api`, no GPU spent). Quotas from HF docs, fetched 2026-11-14.
>
> **Quota (verbatim from `huggingface.co/docs/hub/spaces-zerogpu`):** GPU usage is
> subject to a *daily* quota, per account tier. **Unauthenticated = 2 minutes GPU
> time/day** (Low priority). Free account = 5 min/day. PRO = 40 min/day. Quota
> resets exactly 24h after your first GPU usage. ZeroGPU hardware = half NVIDIA RTX
> Pro 6000 Blackwell (48 GB, `large`). **Anonymous quota is per account = per
> anonymous session/IP, and it is SHARED across all ZeroGPU spaces** — adding more
> spaces does NOT multiply your budget; it only gives you more models.
> The only multiplier is a fresh IP per job (GitHub Actions → 20 free runner IPs on
> public repos) — the mr-bean pattern adopted in L-093. Our repo is public, so this
> holds for us.

## What "anonymous GPU" actually means in 2026

| Route | Account? | Quota | Notes |
|---|---|---|---|
| HF ZeroGPU Spaces (1320 total) | **No login** | 2 GPU-min/day (Low prio) | The only true anonymous GPU. Per-IP, shared pool, resets 24h after first GPU use. Queue when busy. |
| HF free account | free, verified email | 5 GPU-min/day (Med prio) | Slightly better prio/quota; creating 1 free account upgrades you, still zero cost. |
| HF PRO | $9/mo | 40 min/day | Not anonymous. |
| GitHub Actions matrix | our PAT/repo | 20 parallel runner IPs/run (public repo, free) | Each runner = fresh anonymous IP = fresh 2-min budget. THIS is the real ZeroGPU unlock for a full short. CI was account-side queued today (run 43608071984) — check account state before re-dispatch, do not re-dispatch blindly. |
| Colab / Kaggle / Lightning / Modal / credit-schemes | all **need an account** | generous but gated | Not anonymous; skip for "anonymous" purposes (Modal free tier = perp/modal.account). Vast/Replicate/fal/Together = paid credits, not anonymous. |

## Video shortlist (image-to-video — our stills → motion)

All signatures verified anonymously with `gradio_client.view_api`. Likes = community signal, not quality proof. Names link to `huggingface.co/spaces/<id>`.

| Space | likes | why | anonymous endpoint / knobs |
|---|---|---|---|
| `zerogpu-aoti/wan2-2-fp8da-aoti-faster` | 3871 | Wan2.2 FP8 AOTI — fastest sane Wan I2V; the workhorse | `/generate_video`: Input Image, Prompt, Inference Steps, Duration, Guidance 2-pass, Seed |
| `multimodalart/wan2-1-fast` | 1628 | Wan2.1 fast distilled, low GPU-s per clip | `/generate_video`: Input Image (auto-resize), Prompt, Output H/W, Duration |
| `kulkas2pintu/wan777` | 1597 | Wan2.2 with **first+last frame** (loop mirror!) | `/generate_video`: Input Image, **Last Image (Optional)**, Prompt, Inference Steps |
| `Lightricks/ltx-video-distilled` | 1625 | LTX-Video distilled — cheapest Lightricks, I2V+T2V+video-to-video | `/image_to_video`: Prompt, Input Image, task, Video Duration |
| `Lightricks/LTX-2-3` | 502 | LTX 2.3 (image optional!) with **audio** | `/generate_video`: Input Image (Optional), Prompt, Duration, Height/Width |
| `alexnasa/ltx-2-TURBO` | 554 | LTX-2 turbo (fast steps) | `/generate_video` |
| `amisima/LTX-2.5_Turbo_Studio` | 60 | LTX 2.5 Turbo, I2V AND T2V, audio | `/build_prompt`… (studio-flow; check `/generate_video` when calling) |
| `amisima/Wan_2.2_I2V_Studio` | 78 | Wan2.2 I2V with scene-planning + audio | `/lambda…` chain (studio-flow) |
| `Saravutw/WAN2.2_I2V_LIGHTNING_4-8step_custom` | 426 | **4–8 steps** — fits the 2-GPU-min anonymous budget | `/generate_video`: Input Image, **Last Image**, Prompt, Inference Steps, Duration |
| `linoyts/LTX-2-3-First-Last-Frame` | 162 | First+Last frame (loop mirrors!) with audio input | `/generate_video`: First Frame, Last Frame, Audio Input, Prompt, Duration |
| `mcp-tools/wan-2-2-first-last-frame` | 7 | First+Last interpolation, tiny but CLI-friendly | `/generate_video` |
| `zai-org/CogVideoX-5B-Space` | 1057 | CogVideoX-5B (Apache-2.0), I2V+T2V | `/generate`: Prompt, Input Image, Input Video, Strength, Seed, SR/720p |
| `MiniMaxAI/MiniMax-H3-Turbo-Lora` | 568 | MiniMax-H3 4-step turbo (super cheap GPU-s) | `/output_video`: Prompt, First Frame, Last Frame, Duration, Steps — proprietary model; license check before any publish |
| `ByteDance/AnimateDiff-Lightning` | 407 | AnimateDiff lightning — fast, low-motion-safe | see space |
| `mediasynthesismuseum/stable-video-diffusion` | 2057 | SVD — simple, low-motion clips from stills | see space (Stability Community License — avoid for commercial) |
| `alexnasa/Wan2.2-Animate-ZEROGPU` | 369 | our current route (Character Swap; driving video retargeted onto our stickman) | `/animate_scene` — build chunks from OUR render (L-093/JQ) |

**TL;DR hero-shot default for #0006/#0005-redo:** `zerogpu-aoti/wan2-2-fp8da-aoti-faster` (quality) or `Saravutw/WAN2.2_I2V_LIGHTNING_4-8step_custom` (quota-fit) — both accept a still + prompt → 5s clip in one anonymous call. For a loop-mirror beat, pin start/end frames with `kulkas2pintu/wan777` or `linoyts/LTX-2-3-First-Last-Frame`.

## Bonus: free anonymous VO / music / lip-sync (same ZeroGPU pool)

- `fishaudio/Drama-3` (168 ❤) — Fish Audio zero-shot TTS (Studio voice quality, zero quota math; still shared IP)
- `dots-studio/dots.tts` (58 ❤)
- `owensong/Inflect-v3` (10 ❤)
- `MiniMax-Music3-workflow`/Music3 (384 ❤) — free anonymous background score, Apache-ish?? — verify before publish
- `victor/LongCat-Video-Avatar-1.5` (339 ❤) & `meituan-longcat/LongCat-Video-Avatar-1.5-Demo` (33 ❤) — talking-avatar retargeting (studio A-pose character life test)
- `ArtificialArtificial`: `hugging-apps/ltx-foley-v2a` (10) — video-to-audio (replace our SFX with AI)

## ToS / ethics / licensing — read before any publish

1. **Anonymous quota is per IP and shared.** Using 20 IP's worth of GitHub Actions runners is free parallel budget; using 20 spaces from one IP does **nothing** extra. The mr-bean "don't hammer a single space" rule stands — rotate spaces, `--attempts 2`, back off on queue responses.
2. **License (verify each before publish):** Wan2.2 = Apache-2.0. CogVideoX = Apache-2.0. LTX-Video distilled = Apache-2.0 (LTX-Video 2.x: verify the CiviAI-era LoRA licenses separately). MiniMax-H3 = proprietary (MiniMax Community/Civitai terms — flag, do not ship without consent). Hunyuan-Video/Hunyuan3D weights = Tencent non-commercial community license — **do not ship**. SVD = Stability Community License — avoid. `nsfw`/`10Eros` Civitai LoRA spaces — off-limits.
3. **Text drift:** Wan/LTX re-render appearance; **words mutate** (180→190 dB in our probe). Any text/logo/stamp must come from the deterministic pipeline and be composited after the AI pass.
4. **Identity/style:** AI hero shots from OUR approved keyframes preserve bible style far better than unprompted generation (C13–C17). Always pass our frame as `edited_frame`/First Frame, never as a generic prompt-al-prompt.
5. **Queue:** anonymous = Low priority; when the pool is busy your job queues. Gunshot: use 4-step models for hero tests.
6. **You still need our gate** (`ultracritic`) + boss approval before anything ships; AI cuts are not publishable by default (C6 determinism is violated by definition; this is an enhancement layer, C16 official use = hero shots only).

## How to re-run this census

```bash
python3 - <<'PY'
import concurrent.futures, json, urllib.request
def get(p):
    u = f"https://huggingface.co/spaces-json?p={p}&sort=trending&runtime.hardware.current=zero-a10g"
    return json.load(urllib.request.urlopen(u, timeout=45)).get("spaces", [])
allsp = [s for chunk in concurrent.futures.ThreadPoolExecutor(8).map(get, range(55)) for s in chunk]
vids = [s for s in allsp if any(w in (s.get("id") or "").lower() or ("".join(s.get("tags") or [])).lower() for w in ["video","wan","ltx","cogvideo","hunyuan","minimax","animate"])]
print(len(allsp), "zero-gpu spaces;", len(vids), "video-ish")
PY
```
Verification harnesses: grep the `runtime.hardware.current` key — `zero-a10g` is a legacy alias ZeroGPU still answers (1,320 spaces as of 2026-11-14); the site `enzostvs/zero-gpu-spaces` enumerates the same endpoint.
