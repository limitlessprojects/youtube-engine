# Top 10 highest-leverage upgrades — web-researched + in-house evidence (day-017)

> Boss asked: "whats the top 10 most important things that will 10x what were doing or improve what we do so far search the web deeply and ofc give me your recommendations."
> Method: live web research (YouTube blog/Help/2026–2027 guides; Shorts algorithm deep-dives; AI TTS pricing/license boards; microlearning + science-video retention literature — Springer, Frontiers, BMC, Heliyon/PRISMA, Vietnamese cohort; Wan2.2/Veo/Kling/LTX comparisons) cross-checked against our corpus notes (research/video-notes/) + our own gate data (L-085/95/101/105; #0005 perf).
> Verdict rules: nothing raises the quality bar at the expense of viewer response; the gate stays the law; boss owns register/style/audio-spend decisions.

## 1. Cheapen the loop — measure before you render; archive everything fast

**The single fastest compounding win.** Every Short costs us: animate (… 1104 frames @~0.19 s), finish, VLM gate, fail/iterate, re-sumo, re-encode. The `tools/motion_probe.py` we just built says a beat-level dead check costs ~15 s of decode. Views row for #0004 measured 1.2× per re-upload (RSS bot-walled from this IP, so we can't read the metric cleanly — L-102 notes, day-017). **Recommendation:** make motion_probe mandatory in the loop; target <3 fail/re-render cycles per Short (today ≈5+ at #0005-level craft). Every gate round should leave the scene knowing whether it's improving — and failures log, not drift.

## 2. Hook the viewer on the FOREGROUND — question/promise in the first spoken sentence, title = promise

Web + corpus agree (Zachary: 220M McFlurry title = curiosity gap, not content summary; Kurzgesagt "The Egg": audio-led; MinutePhysics belief-correction). **Title ≈ spoken first 15 words** — the promise IS the hook. Our candidates #0007–#0009 consumed the corpus verbatim. **Recommendation:** no Shorts drafts without matching V2/V3 hook test (audio-led cand). Validate against "How many chose to view" in Studio per upload; if <25%, never ship a similar premise again.

## 3. Identity > everything: variety the corpus doesn't give us — forge a signature LINK between scenes

Kurzgesagt = one studio world. We have scene-cousin fragments (s8 Anak 4-step cycle) but every scene starts from scratch; the corpus's top shots share a **palette, vector asset, one motion grammar, one register per video**. **Recommendation:** finish `engine/space.py` world descriptors + `engine/diagram.js` icon families as reusable libraries; C14 veto honored — no mixed icon routes. Every new Short draws from the same bible before adding anything.

## 4. Length discipline + open-source authenticy

Shorts algorithm (2026-verified): watch-through% + viewed-vs-swiped carry the feed; 20–40 s performs best unless retention is excellent at 50+ s. Our Shorts average ~36 s. Shorten hard topics to <30 s when in doubt (~150 wpm → 72 words). **Our #0003 (34.9 s, 188 wpm) sat at the band's floor — already the kindest choice.** The corpus says: no CTA before the premise delivers.

## 5. Caption policy: ASR-clean by construction — burned-in captions permanently bake numbers in

Our L-090 enforced spoken numbers only. Corpus studies seconds: minutes reading sinks comprehension beyond what a Short can pay back. **Recommendation:** never add on-screen captions for the narration track (our stamps are narrative — L-085 disciplined text is fine); keep only punched reveal stamps & icon labels. Never leak `vo_line` transcripts on screen.

## 6. Voice quality actually closes deals — and we can own it for <$10/mo

Artificial Analysis (Sep 2026 Elo: Cartesia 3.6 1,282 / ElevenLabs v3 Conversational 1,210 / Fish Drama 3 parity). Our Fish Audio free lane is workable but shaky; **ElevenLabs Starter at $6 unlocks commercial license.** **Recommendation:** A/B one published Short on ElevenLabs voice with consent (boss-only spend) — expect a "Feel" lift on watch-through%; if no measurable difference, stay Fish Audio. Never spend on Ultra clone before it's 10 k words into the catalog.

## 7. Silence is a bug, not a texture — the ghost of silence

Our ffmpeg whoosh/thumps + Aadd9 pad were an audio floor. The corpus's best (Kurzgesagt beats, The Egg) ride **silence and single instrument hits** — no pads, no risers everywhere. **Recommendation:** silent beat structure; one 2-second swell per 12 beats max; let "THE LOUDEST SOUND IN HISTORY" quote-time ride without bed. Student-viewing tests prize clarity over density.

## 8. The science-lit verdict: clarity > novelty; retention = content integrity

Heliyon PRISMA (40 studies — videos help vs. text, but only when organized; video learning outperforms text in retained % vs immediate); 2026 microlearning review (YouTube source, β unclear but consistently ≈ 0.6–0.7 cognitive effect); TED clarity (β=.339 likes). **Recommendation:** never land a Short with a "confusion point" — cut the paired concept if you can't reduce it to one sentence; psychology of "aha" requires the reveal to be imediate. Our L-097 3.2 s floor enforces this.

## 9. Community pass: the hidden failure modes of the hero-shot route (reddit/HN)

It took a year; our $0.84/us run (L-093/108) passed 5/8 against community blind spots. **Recommendation:** Medium-Res always; AR-match input; `frames-skip=0`; quantization kills likeness first; identity drift/hands/context loss judged by eye only — never at CI. Hero shots legitimate as C16 exceptions ONLY; never from the Loop Tonic track; never A-pose patches over them.

## 10. Discipline loops beat A/B matrices — the cadence has teeth

Block porting (day-013/014/017) everywhere hit the same wall: week-2–4 edits become 80% glue code, 20% story. **Recommendation:** keep day-cycles to publish + ONE structural edit (never two); daily feedback relapse check, not merge-batch reviews; lockout = no delete-and-republish (YouTube flags that — delete-and-republish shifts seed audiences); updates = Studio description edit only.

---

**What NOT to do (weaponized don'ts from this research):**

- Ending-screen "Subscribe" animation on a Short — 2026 Shorts retention data prefers a clean cut-back loop; YouTube manual & corpus agree.
- Stock 3-in-1 "audio-equalizer" overlays — zero science retention evidence; reads as spam.
- VTT-burned synced captions — L-090/caption policy already forbids.
- AI-generated entire cut — C6/kad die-eng model mismatches; the gate will never certify it — correctly.
- Sunsets #0003 re-grade — the sunset verdict is recorded (L-102); re-packaging the aesthetic can wait for #0006 anyway.
- #0001 "WWI" full repair — recorded, redirected, not deleted; leave #0004 alone unless boss escalates.
