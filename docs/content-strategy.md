# Content Strategy — the channel playbook

Position: **"What If" stickman explainers.** Shorts (30–60s) daily + long-form
(8–12 min) 2×/week. Faceless, code-rendered, zero marginal cost.

## Why this niche (and which sub-angles)

Stickman + What-If wins because the visual expectation gap is zero (no uncanny
valley), frames render in seconds, and retention comes from the story. Three
sub-angles, ranked for us:

1. **Absurd physics & survival** — "What if gravity turned off for 10 seconds while
   you were driving?" Black stickmen on clean bright fields, simple vector props.
2. **Micro-history & alternate geopolitics** — "What if Napoleon won at Waterloo?"
   Stickmen in one prop hat (Roman helmet, bicorne) — cheap costume, huge signal.
3. **Extreme bio/medical scenarios** — "What if you only drank saltwater for a week?"
   Simplified anatomy diagrams with exaggerated faces.

Oversaturated and banned from our queue: generic stickman fights, quote compilations,
generic top-10s.

## The script formula (What-If, 7-beat — from vendor/what-if-animation, cross-checked)

1. **Cold open** — the divergence happening, right now. No greeting. ≤ 3s.
2. **Premise title card** — the question, stated clean.
3. **Immediate dominoes** — first 0–5 years / first minutes. Escalate.
4. **The fun** — the absurd-but-true consequences, fastest cuts, jokes land here.
5. **The turn** — one real, checked fact that reframes everything (our credibility
   anchor; every fact gets a source in the script page).
6. **Long-term legacy** — 50+ years out, one strong image.
7. **Loop** — final line bridges into the opening line (Shorts infinite replay).

Long-form = same spine, 3–5 sub-scenarios, each ending with a payoff + a micro-hook
(one open-loop mystery every ~90s).

## Algorithm playbook (what we actually optimize)

- **Shorts 2026:** swipe-away rate and completion/replay rate rule everything. First
  frame = motion. Hook ≤ 1.8s if swipe-away > 35%.
- **Long-form:** CTR from the title/thumbnail engine; AVD from segmented value.
  Title formulas: `[extreme action] + [ordinary object] = [absurd consequence]`,
  curiosity gaps, counter-intuitive truths. No clickbait we can't pay off in beat 5.
- **Pacing bands:** narration 155–175 WPM (Shorts aim ~165); cut every 3–5s; a pose
  change every 3–5s; nothing static longer than 4s.
- **Outlier scouting:** `Outlier Score = video views / channel average views`; ≥ 5×
  gets its transcript blueprinted the same day (see `config/channels.json`).

## Monetization & policy guardrails (2026 rules)

- YouTube penalizes **inauthentic/reused** content, not AI content. Our defenses:
  structural narrative depth, varied pacing/poses, original scripts, distinct
  animation timing, self-aware humor — checked by the critic + VLM passes.
- **Always** tick "Altered or Synthetic Content: Yes" on upload.
- **YMYL ban:** no AI persona giving health/medical/financial/legal/political advice.
  Bio scenarios are framed as entertainment-with-sources, never counsel.
- Foreign-language adaptations: rewritten hook, re-visualized from scratch, original
  VO — structure borrowed, nothing else.

## Anti-boilerplate (mechanically enforced)

Blacklist lives in `tools/script_linter.py` (banned words, greeting detection, WPM
band, hook length). A script that fails the linter does not proceed to critic, render,
or upload. See `prompts/scriptwriter_system.md` for the positive rules (rhythmic
variety, 3-word punchlines, declarative sentences, dry irony).

## Workflow for one video (the whole pipeline)

```
trend scout (yt-dlp search + outlier score)
  → enqueue → transcript → blueprint (research/blueprints/)
  → scriptwriter (prompt) → linter → critic (N=2 max) → gate
  → shot list (visual tags) → assets (stickman rig library)
  → Remotion/stickman render → VLM frame inspection (scene-by-scene) → gate
  → TTS (fish_tts.py) + ASR verify → master (-14 LUFS)
  → youtube_upload.py (synthetic-content box: YES)
  → daily log + ledger
```
