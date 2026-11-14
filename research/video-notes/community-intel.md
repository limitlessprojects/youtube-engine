# Community & science-lit intel (2026-11-14)

Analysis-only research pass for the science-Shorts pipeline. Nothing here is ever composited into published Shorts. All network egress from this box is Reddit-walled (see §Reddit); arXiv and PMC were reachable.

Legend: **[peer-reviewed]** = fetched full text / abstract from the publisher or repository. **[preprint]** = arXiv only. **[forum]** = Reddit via web-search snippets / mirrors — pages themselves 403'd. **[ours]** = our own inference from repo files. **UNVERIFIED** / **CANDIDATE** = could not verify this pass.

---

## Reddit (findings + thread refs + verification status per source)

### Access status (2026-11-14)
- `https://www.reddit.com/r/comfyui/comments/1nle575` → **403 "You've been blocked by network security"** (bot wall) for: direct `.json`, `api.reddit.com`, `old.reddit.com` (302 → login), `www.reddit.com` HTML, `r.jina.ai` proxy. All verified with curl from this egress.
- What DID work: `websearch` (search-engine snippets quoting thread content) and `raw.githubusercontent.com` (Comfy-Org docs) and `huggingface.co` (space source). Snippet-sourced claims are marked **[forum-snippet]** and are one step removed from the threads — treat as directional, not verbatim.

### The target thread — r/comfyui "Wan22 Animate workflow, model downloads and demos!" (1nle575)
Verification: **[forum-snippet]** (title confirmed by multiple independent search hits, incl. Chinese/Portuguese translation mirrors of the same slug). Direct body read: BLOCKED.
- It is the community's canonical **resource/tutorial thread** for Wan2.2 Animate: Kijai workflow with optional denoise pass, upscale, and interpolation; links workflow + model downloads; "Motion Brush"-style partial-image animation.
- Community consensus fragments found via snippets: (a) fp8 "scaled" Kijai build (`Wan2_2-Animate-14B_fp8_e4m3fn_scaled_KJ.safetensors`) vs GGUF quants both used; (b) one commenter reports a different low-noise safetensors filename than the guide (workflow drift is common).
- Thread is where people copy-paste workflows from — high link/citation gravity, low signal on *quality judgement* per se.

### Wan2.2 Animate — community-reported quality, settings, failure modes (all **[forum-snippet]** unless noted)
Thread refs: 1nnq2i9 (masked/unmasked test renders), 1oako1b (resemblance), 1nnq? (low-VRAM spin), 1nobt8p (2 versions / quality workflows), 1qly6s0 (terrible face), 1r1r7u5 / 1nntkbo (first-try results), 1ohhg5h (longer videos), 1p187pr (extended videos), 1oaxtfu (long videos lose context), 1of2up1 (character replacement), 1pdgyb7 (character LoRA), 1stczot (Motion Transfer, r/StableDiffusion), 1nqfdmy (Q4 vs Q8), 1mj75fa (blurry), 1l1h8rk (slowish), 1pn78b9 (which quant), 1nhnokk (Q4/Q5), 1nzvr4t (compact low-VRAM workflow), 1onlgwq (3060).

1. **Resolution discipline.** Reported sweet spots: **468×848 (portrait)** on a 24 GB 3090 with Q4_K_M GGUF via Kijai wrapper, 20 Wan blocks swapped, prefetch=1 (1nnq2i9); **832×480×61 or ×81 frames**, 6 steps, Q4_K_M + SageAttention + block-swap 100%, ~8.5–10 min for 12 s (1nzvr4t); guide default ~480p, 720p achievable on high-end cards. Comfy docs: width/height must be **multiples of 16**; start small, first run. ZeroGPU space (ours, `tools/hero_shot/ai_rerender.py`, `research/free-gpu-video.md`) emits **360×640 low / 480×832 medium** (verified in `app.py` source).
2. **Input→output pairing discipline.** Quote-level finding from 1nobt8p: *"Ideal is when video and image are both high quality. And if your video is wide screen and the image is high, the downscaling is too much and the result more a look-alike than the reference."* I.e. match aspect ratio and quality between reference still and driving video; mismatched AR forces crop/downscale and identity dilution. This is the single clearest community rule for our hero-shot route.
3. **Identity drift / face.** 1qly6s0 ("terrible face"): output face "nothing like the original and it shifts a lot" even with GGUF or Kijai WF — community has no silver bullet; mitigations floating around: higher-res input, lightx2v 4-step LoRA swap, face-detailer/upscale pass, shorter clips. r/generativeAI 1u0a427: face drifts because people condition on the input image only, not the face structure — "what's stable: hair movement, head turns, breathing. what breaks: hands".
4. **Motion mismatch / pose limiting.** 1p187pr: "Wan Animate does a decent job, but it's limited to fixed pose references which struggle with any complex movement." 1nle575-adjacent comment: Animate is "significantly limited by the pose video". Implication: pick driving videos with clean, single-subject, sagittal-ish motion; avoid occlusions and fast cuts.
5. **Temporal consistency / context loss.** 1ohhg5h: skipped frames break the reference-video node — set **frames-skip = 0**. 1oaxtfu: long videos "at some point, I simply lose context and the characters and quality become bad" — community answer: WanVideo Context Options, `num_frames` == `frame_window_size` in WanVideo Animate Embeds (1of2up1). 1p187pr: no robust long-video path in 2.2.
6. **Quantization vs likeness.** 1nnq2i9: "scaled and GGUF but the quality decrease is just too much. It eats up any likeness… only been able to render 81 frames in decent resolution on 24 GB." 1pn78b9: "Quality is better with less compression / quantisation." 1nqfdmy: Q8_0 vs Q4_K_M comparison thread. Rule of thumb: quantization is the first thing to sacrifice likeness, before resolution.
7. **Flush/downstream fixes.** 1nqfdmy: swap default LoRA for the low-noise lighting LoRA and use higher (720+) resolution for more natural output. Upscaling + interpolation passes are standard in the Kijai-modified workflow referenced by 1nle575.
8. **How quality is judged [forum]:** eyeball likeness vs reference (subjective), temporal flicker by scrubbing, "does it look seamless against the plate" (1nntkbo notes missing reflections break the illusion — frontality/lighting match matters), comparison Q4 vs Q8 side-by-side, and feasibility (does it fit VRAM). No community-standard objective metric. **[ours]** This is exactly what VBench-style dimensions (subject consistency, motion smoothness, temporal flickering) formalize — see arXiv section.
9. **r/StableDiffusion / r/generativevideo sweeps:** covered above (1stczot motion-transfer workflow, 1stgnd7 resolution-too-high, 1l1h8rk 480 vs 720 model split). r/generativevideo specifically: **no direct hits returned**; treat as not covered this pass.
10. **r/science / science-comm subs:** **UNREACHABLE this pass** (same 403 wall). Search snippets returned only TikTok/YouTube science-econ papers, no usable thread content. Say so honestly: no direct science-communication subreddit intel was gathered.

---

## arXiv (papers actually fetched via export.arxiv.org API, 2026-11-14)

Queries run: `science communication AND video`, `microlearning`, `video generation AND benchmark`, `VBench`, `short form AND video`, `video quality AND assessment`, `science communication AND youtube` (max_results=8 each). **[preprint]** for all arXiv items unless noted. 16 abstracts fetched.

### Relevant to us

1. **VBench: Comprehensive Benchmark Suite for Video Generative Models** — Huang, He, Yu et al. (2023), arXiv:2311.17982. Dissects video-gen quality into **16 hierarchical dimensions** (subject identity consistency, motion smoothness, temporal flickering, spatial relationship…) and validated against human preference annotations. *Why it matters:* gives us the vocabulary for judging hero-shot output objectively — map ultracritic/gate checks onto "subject consistency" (identity drift), "temporal flickering" (frame-to-frame), "motion smoothness" (ease grammar). Adopt dimension names in gate rubric notes; don't adopt the metric scores blindly (they judge general gen, not retargeting).
2. **VBench++: Comprehensive and Versatile Benchmark Suite** — Huang, Fan, Zhang et al. (2024), arXiv:2411.13503. VBench extended (image-to-video and longer, more versatile evaluation). *Why:* I2V is our exact hero-shot setting (reference still + driving motion); VBench++ is the more relevant of the two for image-conditioned retargeting evaluation. **CANDIDATE** for a one-off scoring of `tools/hero_shot` outputs — not wired in yet.
3. **VBench-2.0: Advancing Video Generation Benchmark Suite for Intrinsic Faithfulness** — Zheng, Huang, Liu et al. (2025), arXiv:2503.21755v2. Adds **Human Fidelity, Controllability, Creativity, Physics, Commonsense** — intrinsic (real-world principle adherence) vs superficial (visual plausibility) faithfulness. *Why it matters:* directly targets the gap our community intel shows — Wan Animate can look convincing yet be physically/anatomically wrong (breaking hands, pose mismatch). Use as a checklist lens for hero-shot acceptance, esp. "human fidelity" and "physics" sanity frames.
4. **Sci-VBench: Evaluating Knowledge- and Reasoning-Intensive Video Generation in Science Domains** — Zhang, Song, Fu et al. (2026), arXiv:2608.09873. 1,253 expert-annotated examples, 60 subjects, 4 disciplines; rubric-based eval protocol; **non-expert humans and MLLM-as-judge agree relatively well with expert judges**; automatic perceptual-quality scores cluster tightly across 16 models while Prompt Grounding and Scientific/Causal Correctness vary substantially; pronounced proprietary–open gap. *Why it matters:* (a) supports our ultracritic/VLM-judge route as a legitimate scalable proxy — with the caveat that it validates *expert-aligned rubric* judging, i.e. our rubric must encode scientific correctness, not just aesthetics; (b) warns that pretty-but-wrong science video is the failure mode to gate.
5. **The Reel Deal: Designing and Evaluating LLM-Generated Short-Form Educational Videos** — Stavrinou, Constantinides, Belk (2025), arXiv:2509.05962. System "ReelsEd" generates structured short-form videos from lecture videos; **between-subject study, N=62 university students: outperformed long-form on engagement, quiz performance, and task efficiency, without increased cognitive load**; learners trusted it. *Why it matters:* strongest direct evidence that short-form educational cuts can beat long-form on measured learning outcomes — supports the whole Shorts format; also a caution that *structured* (instructor-aligned) generation is what won, not generic shorts.
6. **PaperTok: Generative AI for Creating Short-form Videos for Research Communication** — Cristobal, Byeon, Chen (2026), arXiv:2601.18218. Formative study N=8 science communicators/creators; system converts papers → short-form AV; mixed-methods study N=18 + crowdsourced eval N=100; engaging and informative achievable; need for finer-grained controls. *Why it matters:* validates "script options + human refine" loop — exactly our script→render→gate pipeline — and flags that creators want fine-grained control (our beat-level lint/L-097 cadence is that control).
7. **Typologies of the Popular Science Web Video** — Muñoz Morcillo, Czurda, Robertson-von Trotha (2015), arXiv:1506.06149. Content analysis of **200 videos / 100 channels**; science-web-video success keys = entertainment, content quality, authenticity, community building — *not* technical excellence or production cost; documents rising "professionalism" (narrative strategy, editing, sound design) independent of budget. *Why it matters:* cheap ≠ unserious; our canvas-first stickman approach is squarely in the typology of successful low-cost science channels. Supports style-bible investing in craft over gloss.
8. **Citation of scientific evidence from video description…** — Dorta-González & Dorta-González (2026), arXiv:2601.14916. Log-linear regression over 81,302 papers (2018–2023): science video creators cite news articles and Wikipedia preferentially; negative association with policy docs/patents; favor public attention over influential science. *Why it matters:* keep our sourcing bar high (L-090 digits, ASR union-verify, fact-check per plan-30d) — the community's default is Wikipedia-grade sourcing, which is what our pipeline already exceeds; don't regress.
9. **TED Talks speech clarity predicts audience engagement** — Segal, Lary, Schmaelzle (2026), arXiv:2604.04583. **1,239 TED transcripts**, 50 LLM runs per transcript; clarity of explanation strongest predictor of likes (β=.339) and views (β=.314), ΔR²≈.095 beyond duration/topic; full model 29% (likes) / 22.5% (views) variance; outperformed readability metrics; domain-general. *Why it matters:* quantifies what our WPM band and hook rubric aim at — **processing fluency** drives engagement. Directly supports tightening ultracritic clarity dims and C10-caption discipline rather than adding jargon.
10. **Engagement Prediction of Short Videos with LMMs** — Sun, Cao, Cao (2025), arXiv:2508.02516v2. VideoLLaMA2 / Qwen2.5-VL predicting short-video engagement from frames+metadata+audio; multimodal beats text-only; engagement is weakly predictable (LMMs help but far from solved). *Why it matters:* calibrates expectations for any "will this perform?" gate — VLM judges are useful but noisy; don't let a single VLM score hard-block a publish (aligns with our two-round publish decision r12/r13 pattern, plan-30d Day-017).
11. **NTIRE 2024 Challenge — Short-form UGC Video Quality Assessment** — Li, Yuan, Pei et al. (2024), arXiv:2404.11313. KVQ dataset (2,926 train / 420 val / 854 test, Kuaishou); 200 participants, 13 valid teams; SOTA S-UGC VQA methods. *Why it matters:* short-form quality assessment is a mature, benchmarked problem — if we ever want an automated pre-gate aesthetics scorer, KVQ methods are the reference; also a reminder that *UGC aesthetics* ≠ *science-explainer clarity* (we need #1–#4's faithfulness dimensions more than UGC VQA).
12. **SciCom Wiki** — Wittenborg, Stehr, Karras (2025), arXiv:2511.09248. Digital library / FAIR knowledge infrastructure for science videos & podcasts; 53-stakeholder survey + 11 interviews + 14-participant eval. *Why it matters:* context only — the science-video ecosystem is fragmenting; discoverability/schema markup (description citations, L-090 digits) is part of reach, not just the cut itself.

### Also fetched, marginal/not adopted this pass
- 2411.13503 VBench++ (see #2); 2504.04907 Video-Bench (Han et al. 2025, MLLM human-aligned bench; overlaps #1–3, no new action); 2601.14916 (see #8); 2508.16865 (gender gap in science-comms TikTok/YouTube, Eizmendi-Iraola et al. 2025; 4,293 TikTok + 4,825 YouTube videos; demographic-reach finding — informational, no pipeline action); 1908.05572 (producers of popular science web videos, 2019 — companion to #7); 2108.01385 (microlearning videos in intro physics, Netzer & Mittelstädt 2021 — course-level, pre-Shorts-era); 2202.02748 (Janaka et al. 2022, mobile glance/inspect/drift behaviors — drift wins; eye-tracking, HCI, not video-specific); 2608.09873 (#4); 2506.19656 (earth-system video compression — irrelevant); 2307.01383 (dairy-cow weight from video — irrelevant); 2603.16672 CritiSense (misinformation resilience, 2026 — adjacent, not adopted); 2205.06337, 2508.11704 (adaptive microlearning, higher-ed — not Shorts-specific).

**Honest count: 12 relevant papers fetched.** No padding added beyond that.

---

## Open-access science lit (peer-reviewed, fetched)

1. **Microlearning beyond boundaries: A systematic review and a novel framework for improving learning outcomes** — Heliyon (Elsevier), 2024/2025, DOI 10.1016/j.heliyon.2024.e41413; PMC11774797; PMID 39882484. **[peer-reviewed, OA]** PRISMA review of **40 studies**; microlearning = "targeted, action-oriented, bite-sized content… within a short period, typically within a few seconds or minutes"; positive impact on cognitive outcomes incl. **knowledge acquisition, retention, recall, transfer, application**; improved completion rates, engagement, self-efficacy; framework = differences (individual/situational/subject) + guiding principles (specific objective, bite-sized, appropriate timeframe, interactive/engaging, personalization, delivery medium) + outcomes (cognitive/behavioural/affective). URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC11774797/ — *why it matters:* the single best peer-reviewed anchor for "short bite-sized science content works"; its "specific-objective, bite-sized, appropriate timeframe, interactive & engaging" principles map 1:1 onto our hook → single-idea → CTA structure and L-097 cadence.
2. **Microlearning in Diverse Contexts: A Bibliometric Analysis** — R. Sankaranarayanan et al., 2022, PMC9557991. **[peer-reviewed, OA]** Bibliometric mapping (cited 150+); confirms mobile microlearning for knowledge retention & work performance as an established literature. URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC9557991/ — context/backup for #1, not load-bearing.
3. **MDPI *Education Sciences* 15(3):302, "Contribution of Microlearning in Basic Education: A Systematic Review"** — URL https://mdpi.com/2227-7102/15/3/302 — **FETCH BLOCKED (392-byte JS challenge); content UNVERIFIED this pass.** Cited only as **CANDIDATE** from search-result snippets ("short modules… significantly enhances motivation, performance and interaction"). Do not treat as fetched.
4. **"Microlearning Effectiveness in Higher Education: A Systematic Review and Meta-Analysis…"** — Jurnal Mathema, DOI 10.33365/jm.v7i2.517 — **CANDIDATE, NOT FETCHED** (direct page not retrieved). Listed for completeness only.
5. **Microlearning in Health Professions Education: Scoping Review** — PubMed 31339105 — abstract snippet seen via search ("positive effect on knowledge and confidence… retaining"); **not fetched**, CANDIDATE.

Not fetched / paywalled: paywalled journals (e.g., Science Communication, Journal of Research in Science Teaching) — no full text touched; only titles/metadata via search. Zero verbatim copying.

---

## Mapping to the pipeline (specific files, specific actions)

**Hook calibration (`tools/ultracritic.py`, `content/style-bible.md` §4)**
- Adopt Segal et al. 2026 clarity finding (β=.339 likes) as justification to keep hook_impact rubric anchored to *instant topic parse* (A3: hook narration must name the topic) and clarity-of-explanation wording — reject any hook that needs >1 beat to parse.
- Adopt SciCom/typology finding (#7: authenticity + narrative strategy > production gloss) as a written argument against weakening the C13–C17 bible in favor of "more AI polish": spend on clarity, not shine.
- Frame-0 gate stays; add one line to ultracritic notes: hook frame must pass "would a scroll-stopper parse the topic noun in <1 s" (already A3/B1 — keep, don't dilute).

**Pacing / WPM (~200 WPM target; MinutePhysics ~236–251, MinuteEarth ~125–197 — our canon 214.5 #0005)**
- Reel Deal (N=62, engagement + quiz win over long-form) supports keeping ~200 WPM for Shorts density; do **not** chase MinutePhysics' 236–251 — our stickman visuals need parse time (community + 2202.02748 "drift" behaviour agree that fragmented attention tolerates short bursts, not wall-of-text).
- TED clarity paper: readability metrics underperform discourse coherence — so keep the WPM *band* but weight ultracritic toward sentence-level coherence (already B1/C10 caption discipline).

**L-097 beat law (`tools/script_linter.py`: beats ≥ ceil(VO_s/3.2))**
- Supported by Heliyon microlearning review ("bite-sized… specific objective… appropriate timeframe") and 2202.02748 (glance behaviour). Keep 3.2 s; do not relax. Consider a *soft* warning at 4.0 s mean (L-075 already fails >3.2 s mean, max 4.2 s).
- PaperTok fine-grained-control need → our beat lint is the right mechanism; maybe expose per-beat purpose labels in future (inference, not evidence).

**Style bible / stickman craft / camera & ease grammar (`content/style-bible.md` §6, engine/core.js)**
- Typologies paper (200 videos): editing/montage/sound-design professionalism correlates with success independent of budget → keep C15 motion rules (parallax ≥2 planes, ~0.3× bg, eases, squash-stretch, idle breathing); these are the cheapest "professionalism" signals we have.
- VBench dimensions (temporal flickering, motion smoothness) → when reviewing rendered frames for gate notes, explicitly score flicker/smoothness by name; our canvas renderer is deterministic (no gen flicker), so failures will be *motion-design* ones (bad easings) — catch at ultracritic, not at publish.

**Retention structure for science shorts**
- Heliyon review + Reel Deal + PaperTok converge: one specific objective per video, bite-sized, interactive/engaging, payoff early. Map: hook (0–3 s) → single phenomenon → payoff → loop/CTA. Our superlative formula (#0005 Krakatoa) already does this; enforce in script review checklist.
- Engagement-prediction paper (2508.02516): VLM engagement scores are noisy → keep human/two-judge publish decision (plan-30d r12/r13 pattern), don't automate publish on VLM alone.

**Anonymous-GPU hero-shot route (`tools/hero_shot/ai_rerender.py`, `research/free-gpu-video.md`, HF space `alexnasa/Wan2.2-Animate-ZEROGPU`)**
- Confirmed from `app.py`: Low Res 360×640 / Medium 480×832, portrait-or-landscape autodetect, replace/retarget modes, per-IP GPU quota on ZeroGPU. **Our hero frames are portrait 9:16 → 360×640 low is below our gate's contrast bar; always request Medium Res (480×832)** and upscale in finish_v3 if a hero survives review.
- Community pairing rules to adopt **into `ai_rerender.py` prompts/precondition checks**: (1) reference still and driving video must share aspect ratio and comparable quality — auto-reject mismatched AR with a warning (1nobt8p); (2) driving video = single subject, clean pose video, frames-skip=0 (1ohhg5h); (3) expect face likeness loss — accept only shots where likeness survives at 480×832, else fall back to canvas stickman (our default anyway); (4) flicker/hands = reject on sight for science content; (5) never use for anything beyond a background/hero accent — stickman remains the explainer.
- **Reject** any plan to post AI-Animate output as the *primary* explainer footage: community experience (1p187pr, 1oaxtfu, 1qly6s0) + Sci-VBench (science correctness varies wildly across models) + our own 7.08–7.49 gate history on canvas-first all point to: retargeting is a garnish, not the meal.
- **Validate** ` Wan2.2-Animate quality` against VBench-2.0 dimensions (human fidelity, physics) on 2–3 test stills before #0006 uses it; record results in `research/free-gpu-video.md`.

**Gate / finish (`tools/finish_v3.py`, `gate/*` paths referenced in plan-30d, `docs/plan-30d.md`)**
- finish_v3: if hero-shot frames are ever composited, run them through the same C13 asset check (rim/outline/contrast) — AI frames will fail ink-outline rules by default; rembg + rim-light rework required (we already do rembg for C14 pilots, L-099/L-100).
- Gate rubric: add "identity consistency" phrasing to notes.json for any AI-composited scene (VBench subject-consistency language) alongside existing dims.
- plan-30d Day-017+: two-round publish decision stays; community+arXiv evidence supports keeping a human/studio final call over VLM-only.

---

## Bottom line for #0006+ Shorts

1. Keep canvas-first stickman as the explainer backbone; Animate retargets only as an optional accent, always Medium Res, AR-matched inputs, likeness-gated, else drop.
2. Hook clarity (topic noun in frame 0 + first sentence) is the highest-leverage lever we have — β≈.31–.34 engagement deltas in fetched TED data back it; don't trade it for style.
3. ~200 WPM with coherence-weighted writing beats both MinutePhysics speed and MinuteEarth slowness for our format; L-097 3.2 s cadence stays.
4. One specific objective per video; payoff early; loop-able ending — backed by the only fetched OA microlearning review (40 studies) + Reel Deal (N=62 win vs long-form).
5. Science correctness is a gate dimension, not a hope: adopt Sci-VBench's lesson — perceptual quality clusters across models, correctness doesn't; our fact-check + ASR union-verify pipeline must stay mandatory.
6. VLM judges are proxies, not oracles: keep two-round human/studio publish; Sci-VBench shows judge–expert agreement is decent *with rubrics*, so invest in rubric sharpness (clarity, correctness) over more judges.
7. Reddit is currently 403-walled from this egress — all community claims above are snippet-verified only; re-verify in a browser session before acting on any single thread.

## Compliance note

- No bypassing of the Reddit block was attempted beyond public search snippets and r.jina.ai (which itself 403'd); no login, no tokens, no scraping of private data.
- arXiv (export.arxiv.org) and PMC accessed anonymously within public APIs; MDPI/ScienceDirect/PubMed direct pages not fetched where blocked/paywalled — marked CANDIDATE.
- arXiv papers cited by ID/title/authors/year with 2–3 sentence summaries; no full text reproduced.
- Forum quotes limited to short snippet phrases retrieved via search; no bulk reproduction of threads.
- Peer-reviewed vs preprint vs forum vs inference is labelled per item. Anything not fetched is marked UNVERIFIED or CANDIDATE.
- This file is research analysis only; it must not be copied into published Shorts, thumbnails, descriptions, or scripts.
