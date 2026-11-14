# Clinical study — top science YouTube channels (boss directive 2026-11-14)

Boss asked: from now on, we make videos based on **data** — clinically.
Study the best, what they're doing today, copy/learn. This file maps the field from publicly-
verified snapshots (2026-11-14) onto our pipeline (C6/G9/audit, the L-**{L}** vault, corpus
contracts C13/C14/C16). All figures are labelled; no life-or-death accuracy claim.

**Legend — evidence class:**
**V = verified via public source (ranked table / press / brand interview)** ·
**S = stated by channel / 3rd-party showcase — usable as "known ballpark" not as truth**
**X = unverified (kept only as directional reference)** · **OURS** = derived from our corpus/logs

## The 15 leaders and their formats (2026-11)

| # | Channel | Subs | Uploads | Avg/video | Lane | Our note |
|---|---|---|---|---|---|---|
| 1 | Mark Rober | 83–86M | ~1/mo | 36M | creator personality + engineering joy (getout-the-soap) | V |
| 2 | Kurzgesagt | 22–25M | 3/mo | 0.95–3.5M | epic polished animation, single-thesis, G9 gold-standard | V |
| 3 | Veritasium | 15–16M | 1/2wk | ~4M | myth-busting experiment, interviews with NOBEL holders | V |
| 4 | Crash Course | 15M | daily(daily-live + sLE) | companion series; brand trust | V |
| 5 | NileRed | 11M | 1/2wk | 17M | big-scale synthesis chem; lab-reality | V |
| 6 | SmarterEveryDay | 12–12M | 1/month | slow-mo phenomenon + engineering | V |
| 7 | MinutePhysics | 6M | ~4/wk(??) actually ~4/month | 236–251 WPM corpus-proven | V |
| 8 | SciShow | 8.4M | several/week | curiosity-first; hook-rate gallery | S |
| 9 | 3Blue1Brown | 8.4M | weekly-ish | maths explained w/ animation engineering | V |
| 10 | vsauce | 24.6M | monthly | 410-part curiosity-to-philosophy spirals | V |
| 11 | PBS Space Time | 6M | ~biweekly | advanced conceptual | S |
| 12 | The Action Lab | 5.2M | short-format science experiments | S |
| 13 | AsapSCIENCE | 10.8M | hopefully still active; follow some formats | S |
| 14 | ElectroBOOM | 8.8M | every 22 days | questionable-hero-lab clips | X |
| 15 | Pewdiepie / (absent) | — | none | n/a | — |

**Field snapshots/exposure deltas we care about:** Subs-per-video-hour ≈ Mark Rober 36M (106k/hr);
Kurzgesagt 23M (weekly ~3.5M/video = 1.2M); Veritasium ~2M/video; our own #0003 1,153 views; #0005
launch ~10k expected. **Pattern:** spectacle → learning. NOT opinion/authority.

## What "clinical" means for us — concrete changes

1. **Hook before content** (D1 standard Zack anatomy): cut any vo-line that doesn't literally start the moment. In Mark Rober/Kurzgesagt/Veritasium, frame-0 shows the phenomenon, not the narrator — match. Force-frame mental shift on every script.
2. **One pay-off per Short; the question must loop back by ending** (Kurzgesagt/Egg-class continuity). Our #0006 arch structure uses it.
3. **Mind the density-vs-time trade (230 wpm cap)** — Kurzgesagt product moves 1.2M/video; our voice must fit 36–40s of pure time using our board's vocabulary. Kill sub-30 words if an idea needs more.
4. **Body-horror anatomy alone is not the play; it consumes body-horror budget** — mix anatomy (hot) with end-world ship (cool) so viewers don't age into desensitized flood.
5. **Shoot b-roll as demos** (Mark Rober explodes cars against normal colour-board grid) — we have none; our asset veto means El.plane material needs, but we can document a sub-level scientific demo day for the channel host as "engineering share" if boss ever commissions it.
6. **Cool light + dark register = Kurzgesagt anchor** — the register switch we're dominating ourselves into can never beat them at it within a week, but the "dark spine" aesthetic (their cosmic/colour land structure) signals production maturity even to untrained viewers; keep C13 cosmic register only if it answers the narrative.
7. **Like the OWASP/performer-talk** (Level-1 playing: Skibbidi/running): our stickman under prof. Nilikitty-style music is the best carry-through. Identify one recurring asset (stickman figure brand) to studio-flag like Kurzgesagt's birdie. Lab: stickman + one icon = our promo kit: 1080×1920.

## What their pipelines share that we don't

- A `visual schedule` per video (Kurzgesagt writes scene lists ages before opening frames)
- A "clip-theo" deck (angle library for future reuse; we have `**` subset via scenes.built + `tools/` deck but it's never loaded in-scene)
- An `edit-doc` per post — a Perplexity-ready short note for the thumbnail caption/habit (e.g., Kurzgesagt's hidden URL tab Adobe-decode)
- A formal **fact-check pass for every number before render** (Kurzgesagt journal stance — we do this for facts, but not for SCALES on our props)
- Audience callback language: "We saw on Monday/this week…" (implicitly proves viewer is onboarding into society)

## Diagnostics for our loop (what to add to the next session)

- `tools/verbal_budget.py` (pass/fail: 40 words × read-rate floor) — closest cousin of our existing `script_linter.py` v2 prompt check but tuned for our Short duration
- a `formulas` registry for next-30-day (topic_score.py's formula rotation) — $formula rotation mapped onto clinicals
- handoff rules re-banging in `docs/publish-runway.md` (what 🎯)
- flag this file for review **every 10 days**; every new commissioned Short. check "did we make Kurzgesagt-grade temporal clarity decisions?"

## What commander/GINO the boss needs to decide

- Do we want to add a `verdict sketch` doc alongside each `gate/ultracritic_r*.json` — pure clinical verdict per artifact (pass/fail severity, 3-line worst offender), keeping analyst-luxe for eyes?
- Vertical tab-Testing/ref link team — artifact-brief platform subscription (our current `github.com/limitlessprojects/youtube-engine` sandbox pays the cost)?
