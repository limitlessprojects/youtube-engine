# Zack D. Films — production intel (boss-supplied, 2026-11-14)

> Boss passed over a research brief: "research deep study Zack D. Films — it's a completely different
> entity from Pixar/DreamWorks." Channel figures below are **web-verified 2026-11-14** (vidIQ, TubeGrade,
> HypeAuditor, Communitrics); company-team figures remain **boss-supplied, UNVERIFIED**.
> Compliance: analysis-only; their catalog (4,000+ Shorts, all copyrighted) may never be composited,
> remixed wholesale, or re-uploaded; observation stays at the pattern level.

## What it is (per the brief)

Zack D. Films = American digital-media company / YouTube channel — short-form, cinematic **3D**
animated explainers (20–45 s, vertical, high-production, ultra-optimized for Shorts). Founder/lead:
**Zachary Dziadul** (Dec 28, 1992). Figures **web-verified 2026-11-14** — vidIQ (7 Nov snapshot: 29.7M subs / 83,002,853,224 total views / 4,212 videos, joined Jun 7 2021, rank #367 worldwide, #176 Entertainment, ~500K subs last 28d, ~3B views last 28d), TubeGrade (@zackdfilms, 29.6M / 4,100 vids / 82.7B views as of Nov 9 2026, avg ~6.96M views/video, rank #60 fastest-growing this week, rank #346), HypeAuditor (Oct 2026: 29.7M subs, 4,170 videos, ~30 uploads per 2 days rot, engagement rate 3.43%, avg 6.54M views), Communitrics (Sep–Nov 2026: #381, +1.3M subs in 90d). Cadence ~37 uploads/WEEK (~5/day; ~82 videos + 4.43B views gained in Oct 2026 alone).
Team scale per boss brief (UNVERIFIED): ~300 employees, ~200 animators (Aug 2026). Content pillars:
historical incidents, science-how-things-work, unusual stories, "violation/scary injury" hooks.

## Their pipeline (per the brief; near-confirmed by their animator portfolios + job posts)

| Tool | Role | Our analog / overlap |
|---|---|---|
| **Blender** | main workhorse (modeling, rigs, animation, lighting, render) | none (we build SVG/JS, not 3D). The discipline to copy: everything in ONE source-of-truth scene graph |
| **Cascadeur** | physics-based character animation (falls/jumps) | closest cousin = our `engine/rig.js` breathe/blink + hand-keyed poses — we could adopt constraint-assisted key framing later |
| **BlenderKit** | ready-made asset library; "start from template" for consistency | analog of our `V2.*` helpers + locator icons; corpus consistency via a single PNG-icon route |
| **After Effects** | compositing / finishing | our `finish_v3.py` (mux + loudnorm + sound design) + scenes for text — same wedge |
| **EmberGen** | smoke/fire/explosion sim | our hero-shot route (L-093/C16) — never re-render procedural fire; we use approved keyframes |
| **Flamenco** | Blender's render farm manager | analog of our GitHub Actions matrix (ZeroGPU fresh-IP) and of `tools/render_short.py` |
| Quality bar | days start from templates; daily dailies review animator eyeballs | our C6 determinism + ultracritic VLM gate (stricter) + L-069 refuse-to-promote |

Pattern worth stealing: **every asset from a locked template + eyeball dailies + single quality tool (eye) wins** —
we already replaced "eye" with a calibrated VLM and kept C6/L-069; the lesson is *their cadence*, not their tools.

## GitHub state (boss-verified; live 2026-11-14)

**NO dedicated "study/analysis" repo for Zack exists** — search returns replication tools, not case studies:

| Repo | What it is | Verdict |
|---|---|---|
| `Anil-matcha/zack-d-films-ai-video-generator` | agent-native pipeline: topic → Zack-style short via Veo 3.1 / MuAPI / ffmpeg; `SKILL.md` for coding agents | **Production, not study.** Would replace our hand-keyed control; conflicts with our C6/C13; do NOT install; read only to steal the *prompt-shape* for hero shots |
| `J-StaR/VibeCode-Protocol-Suite` | research + pre-production skill suite for planning Zack-style shorts | Same — ideation-only reference; no study |
| Paid "The Zack D. Films Engine" guides | reverse-engineering their prompt structure & visual beats | Paid; inaccessible — analysis stays ours, from the corpus |
| Starpop / Growwly guides | channel-growth analyses | Cite secondary; no raw numbers trusted |
| Wikis / Fandom pages | history/production trivia | Unvetted |

**No conforming skill or bible for "how to study Zack D. Films" exists on GitHub.** The closest thing to a
methodology in our repo is the corpus work itself: `research/video-notes/ttuKeS5k4Uo-VL-01…` through
`yGw0nhlUtkQ` and `rRAmNz6G3Tk` — spectacle-first frame, ~149–181 WPM single-take, zero-text-at-t=0,
body-interior "gross but educational" lane (their highest-views anatomy). Those notes stay authoritative.

## What it means for us — three directional takeaways

1. **Cadence is the moat.** They ship daily via templates + eyeball dailies; we ship slower but with a VLM gate.
   Our cadence on the nightly is ~1 Short/2 days; theirs ≈ 5.3/day (~37 uploads/WEEK, vidIQ 2026-11; Oct 2026 alone: +900K subs, +4.43B views, +712 vids). Different universe, same law:
   reduce friction-to-ship without lowering the bar (C6/L-069/L-090 chain already does this).
2. **Their 3D pipeline has nothing to do with our 2D stickman; the lesson is the *content formula*, not the stack:**
   20–45 s, one HOOK question, one payoff, scare-adjacent anatomy wins (s1/s4/s6 anatomy scenes). Our #0006 hook
   ("Don't know why the island vanished from the map…") matches the pattern — keep anatomy/catastrophe close to the eye.
3. **No external "Zack skill" will teach us anything we need** — every analysis tool they've produced is oriented at
   replication for profit; our study (corpus + gate evidence) is more rigorous and license-safe.

## Compliance
- Every observation here stays at the pattern level; zero pixels/audio/script from their catalog enter our renders.
- The corpus files VL-01..05 hold the raw intel; these notes are derived synthesis.
- Borrowing: our G9 ceiling (Egg) is higher than theirs (The Egg > Zack by craft measure); keep it.
