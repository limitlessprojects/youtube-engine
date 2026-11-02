# Day 000 — Prior Lessons (the archive)

> Everything learned before this ledger existed. Sources: the ReadAny 60-second
> product demo worklog + DIRECTION.md (multi-agent session, delivered
> `readany-demo.mp4`, 10+ VLM passes), and the strategy sessions with Gemini on
> autonomous YouTube pipelines. Lessons are numbered L-001+ for referencing.

## From the ReadAny product demo production

**L-001 — Because-X-so-Y.** Every design decision must derive from the product, not
from taste. Template: "Because the product has X, the film uses Y." (guizang
product-video method). Example that worked: *because the app opens dark navy and reads
warm parchment, the film bridges both — dark cinematic intro → warm product scenes →
dark outro.*

**L-002 — Real footage only.** Never invent UI, stats, or claims. Every shot is real
footage of the live app; every caption is a claim verified on screen first
(motion-video-kit truth rule). Applies to us at scale: every number a video states
must come from a source we can point to.

**L-003 — Emphasis spent, not spread.** (motionmaxxing rule) The emotional core gets
the longest scene (in ReadAny: the chat-with-your-book moment); montages cut fast
(~3.1s per feature). Don't give every scene equal weight.

**L-004 — One world, one light.** All overlays (cursor, captions, logo cards) reuse the
product's exact design tokens. In ReadAny: navy `#0F111A`, amber `#F5A623`, parchment
`#F5F1E9`. For the channel: define the stickman-world tokens once (ink, paper, accent)
and never drift.

**L-005 — TTS timing math.** Fish Audio `s2.1-pro-free`, "Energetic Male"
(`ref_id=802e3bc2b27e49c2995d23ef70e6ac89`) reads at ~2.6 words/sec. Script timing =
words / 2.6 + breathing room. Verified end-to-end with ASR round-trips.

**L-006 — ASR-verify generated speech.** After every TTS render, run speech-to-text on
the result and diff against the script (this caught timing/mumble issues before render).
Cheap, deterministic QC. Artifacts: `work/vo/*.asr.json`.

**L-007 — VLM-gate every scene, scene by scene.** 10+ VLM critique passes were run on
the demo (landing, reader, panels, chat states, stats/settings, AI settings, drafts,
frames). Each pass produced concrete fixes (spacing, contrast, timing) and a re-render.
Rule: no scene ships on the first render; every scene gets a VLM pass + fix cycle.

**L-008 — Written QA gates before delivery.** The demo shipped only after: duration
≤ 60.0s; every VO sentence fully inside its scene (no bleed across cuts); on-screen
text held ≥ 2.5s and readable at 1080p; URL readable ≥ 2s. Write the gates down BEFORE
rendering; check them mechanically.

**L-009 — End quieter than you began.** (motionmaxxing rule 5) Final card holds still,
music resolves, no burst at the end.

**L-010 — The 12 skills we already mined** (cloned in the ReadAny session): remotion-dev/skills,
guizang-product-video-skill, product-launch-motion, motionmaxxing, motion-video-kit,
claude-motion-design, agent-video-editor, iart-ai/motion-skills, saas-motion-kit,
onetake, bang-motion, claude-remotion-kickstart. What each taught is folded into
`skills/REGISTRY.md`. Several are forked on the account already.

## From the strategy sessions (Gemini, distilled + verified)

**L-011 — Niche pick.** What-If stickman explainers = minimal visual expectation gap
(no uncanny valley), fast frame generation, retention driven by story not graphics.
Sub-angles ranked: (a) absurd physics & survival, (b) micro-history & alternate
geopolitics, (c) extreme bio/medical scenarios. Generic stickman fights = oversaturated.

**L-012 — Cadence.** Long-form 8–12min: 2/week. Shorts 30–60s: 1/day, cut from the
long-form's best hook as a funnel. Batch-produce, schedule via YouTube Studio queue.

**L-013 — Monetization guardrails.** YouTube penalizes *inauthentic/reused* content,
not AI content. Rules: vary pacing/poses every 3–5s; script personality (dry humor,
self-aware banter); always tick "Altered or Synthetic Content: Yes"; never AI personas
giving health/financial/legal/political advice (YMYL ban).

**L-014 — Anti-boilerplate blacklist.** Banned: "delve", "tapestry", "testament",
"beacon", "unravel", "realm", "in summary", "have you ever wondered", "imagine a world
where", "welcome back to the channel", rhetorical questions closing paragraphs.
Enforced mechanically by `tools/script_linter.py`, not by vibes.

**L-015 — Rhythmic variety.** Force 3-word punchlines next to long flowing sentences.
Hypnotic uniform cadence = synthetic tell = swipe-away.

**L-016 — Hook law.** The divergence/ promise must land inside 3 seconds (target 1.8s
for Shorts if swipe-away > 35%). No greetings, no channel intros, ever.

**L-017 — Open loops.** One unresolved paradox every ~90s (long-form); Shorts end by
looping into the opening line (infinite replay trick). Long-form: 3–5 sub-scenarios,
each ends with payoff + micro-hook.

**L-018 — Outlier ratio is the compass.** `Outlier Score = video views / channel
average views`. Flag ≥ 5×, extract that transcript's structure the same day. Competing
on topic choice, not production budget.

**L-019 — Transcript over viewing.** We "watch" competitors by transcript: pacing,
hook structure, word distribution, joke frequency → structural blueprint → original
topic, same rhythm. Never paraphrase content; steal structure only (transformative
rule). Foreign-language adaptions must be rewritten + re-visualized from scratch to
pass the reused-content filter.

**L-020 — Critic hard cap.** Writer→Critic loop runs max N=2 revisions. Fail twice →
discard the premise, move on. Prevents infinite polish loops and over-analysis.

**L-021 — Schema-validated handoffs.** Agents exchange strict JSON (scenes with
timestamps, asset ids, narration). Script state feeds forward only — VLM fixes change
layout/asset/timing, never story, mid-render.

**L-022 — Safe zones & z-index.** Subtitles anchored to bottom 20%; characters bound
to central 60%; every layer has an explicit z. VLM outputs bounding boxes; overlap > 0%
→ auto offset shift before encode.

**L-023 — Local fallbacks for everything external.** TTS fallback (Kokoro/Piper local),
transcription fallback (faster-whisper local), atomic git backups (failed pushes queue
to `.queue/` and retry). Zero-cost pipeline must not depend on any single remote
being up.

**L-024 — Memory bank.** Daily metrics (CTR, swipe-away, AVD) adjust generation weights;
top-retention script structures stored as reusable blueprints. Start with markdown
blueprints in `research/blueprints/`; graduate to a vector DB when there's enough
volume to need it.

**L-025 — yt-dlp, not downloader sites.** The sketchy ad-ware downloaders are banned
from the pipeline. yt-dlp + youtube-transcript-api + faster-whisper only.
