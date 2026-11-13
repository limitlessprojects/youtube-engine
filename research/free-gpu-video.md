# Free-GPU video generation — repo assessment (day-014, 2026-11-13)

> Boss directive: "use mr-bean-motion-swap's way of accessing free GPU running
> SeedDance 2.5 to improve quality if needed … cheapest route is probably to
> render the layered assets on a free GPU in batches and do all compositing
> locally … and freefield — see how and whether this enhances what we already
> do." Evidence here comes from reading both repos' READMEs/workflows on
> 2026-11-13. Nothing below is tested in our pipeline yet.

## Repo 1: ssmurfgg04-gif/mr-bean-motion-swap

**What it is:** a full-body character-swap pipeline (replace the actor of a
video with a reference character, preserving skeleton motion end-to-end). NOT
a face swap.

**Correction on record:** the model behind it is **Wan2.2-Animate on
HuggingFace ZeroGPU** — there is no SeedDance 2.5 anywhere in the repo. The
boss's memory conflated the two; the transferable asset is the ACCESS PATTERN,
not the model name.

**The free-GPU pattern (what we steal):**

1. Anonymous HuggingFace ZeroGPU quota is per-IP (~160 GPU-seconds).
2. GitHub Actions gives every matrix job a FRESH runner IP (20 parallel jobs
   on the free plan) → the per-IP quota resets per chunk.
3. Work is sliced into ≤140-GPU-second chunks (`plan_chunks.py`, motion-aware).
4. A quota-failure triggers automatic re-runs on a fresh IP (error taxonomy in
   `run_swap.py`).
5. CPU jobs plan chunks and assemble them frame-exactly
   (`assemble_chunks.py`); post-FX (`enhance_swap.py`) and a neutral-prompt
   VLM identity gate (`identity_gate.py`) run locally.
6. Driver: one workflow_dispatch (`swap-character-v2.yml`) with URL inputs —
   no credentials beyond the repo's own GITHUB_TOKEN.

**Why it fits us (C16):** our compositing is already local and deterministic
(scenes.html → ffmpeg). The only GPU-shaped gap is HERO-SHOT image-to-video
(explosion column, pyroclastic surge, space scale pulls) where procedural
animation reads fake. The pattern lets us:

- render keyframes locally in our locked style (C13 bible),
- animate ONLY those hero shots on free ZeroGPU quota,
- slice long generations into ≤140 GPU-s chunks across GH Actions runners,
- composite back locally, judged by ultracritic as usual.

**Costs / risks (UNVERIFIED until first run):**
- ZeroGPU quota numbers (~160 s/IP) are the repo author's measurements, not
  ours; verify with a 5-second probe job before planning real chunks.
- ZeroGPU spaces accept a queue; wall-clock per chunk is minutes, not seconds.
- Model output style will NOT match our bible out of the box — hero shots must
  be fed our approved keyframes (image-to-video, not text-to-video) and graded
  to palette in finish_v3.
- Licensing: output use terms of the underlying space/model must be checked
  per model before anything ships. Keep the hero-shot list small.

## Repo 2: neuregex/freefield

**What it is:** Higgsfield rebuilt on ComfyUI — 120 image/video/VFX/audio
apps, open-weight models only, runnable on Modal cloud or a local GPU.

**Access model:** Modal (L40S/H100/A10G) or local GPU; needs `modal secret
create huggingface HF_TOKEN=...`, a model-download phase
(`modal run infra/modal_app.py::download --pack image`), a deployed gateway
(`modal deploy infra/modal_app.py`), and a Node web layer.

**Verdict: PARKED (L-094).** It solves a problem we don't have yet (model
access breadth); our bottleneck is format/style (L-085 ceiling), and asset
generation is already covered. It also wants an account + deployment +
multi-GB downloads before the first frame exists — that's an infra detour,
not a quality lever. Revisit trigger: a hero shot that genuinely needs a
ComfyUI-class app, or a confirmed Modal free tier worth > the ZeroGPU route.

## Decision (day-014)

1. **Adopt the mr-bean pattern, not the repo**: hero-shot image-to-video via
   GH Actions matrix × ZeroGPU chunks, composited locally (C16). Implement as
   `tools/hero_shot/` when the first hero shot is actually needed — probe the
   quota first (L-047: second egress before verdicts).
2. **freefield parked** with a written revisit trigger.
3. Style bible + layered assets (C13–C15) remain the primary quality lever;
   free-GPU hero shots are an enhancement layered on top, not the fix.
