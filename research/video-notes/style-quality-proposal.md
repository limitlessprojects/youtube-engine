# STYLE & QUALITY AMENDMENT PROPOSAL v1 — 2026-11-14 (analysis-only; NOTHING ships without boss directive — C13/C14)

> Author: research subagent, day-017. Sources: `research/video-notes/*.md` (22 files, incl. README synthesis), `content/style-bible.md` (locked 2026-11-13), `docs/plan-30d.md` (day-017), `tools/ultracritic.py`, `engine/core.js`.
> **Status: PROPOSAL. Zero edits made to engine/tools/style-bible/content.** Every amendment below awaits an explicit boss directive. C13 stays in force until then.
> Tone note (C14): direct. Where the corpus says we're wrong, it says so below.

---

## 1. VERDICT — current style bible vs the corpus

### 1.1 What HOLDS (corpus confirms, cite)

| Bible rule | Corpus evidence |
|---|---|
| One accent per scene; background ∈ {deep space, raised, nebula} | Kurzgesagt *Egg* runs two strictly-separated registers (cosmic indigo/nebula vs warm amber domestic) and never blends them in-frame (`h6fcK_fRYaI-VL-06-kurzgesagt-egg.md` §03). Zack files validate flat single-hue grounds — "background discipline: absolute — one flat field per shot" (`ttuKeS5k4Uo-VL-01-zack-stitches.md` §03, `yGw0nhlUtkQ-VL-02-zack-splinters.md` §03). MinutePhysics holds the 3-accent ceiling "used with restraint" (`sEQvDbyFNbo-VL-15c` §03). Buff Motion proves per-plate single saturated field + one accent reads at 2160p→phone (`VL-10a-buff-showreel-1.md` §03/§05). Bible §1 survives. |
| Strokeless background masses / outlined heroes | Egg: "background masses are strokeless, matching our bible §3" — the note literally cross-checks us and confirms (`h6fcK_fRYaI…` §03). |
| Subject = opposite value of ground (C2/contrast_legibility) | Buff plates read at thumbnail scale via value separation (`VL-10a` §05); Zack's flat sky isolates the subject (`ttuKeS5k4Uo…` §03). Holds. |
| 3.2s beat law / ~200 WPM band | Grolar Bears = 197 WPM, ~8–9 beats, best sub-30s calibration in set (`ZA4OQ-1ahXg-VL-14b` §04). MinutePhysics runs hot (236–251) and Zack runs cold (149–181); ours sits inside the survivable band (README synthesis table). L-097 stays. |
| Canvas-first stickman backbone; G9 = meaning-density | Egg executes detail density as *meaning* density with far fewer assets than our layered pipeline assumes (`h6fcK_fRYaI…` §05). Kurzgesagt pipeline note confirms 1200h/video vs our ~0 human-hours — G9 must judge composition density, not primitive count (`uFk0mgljtns-VL-08` §05, flags raw "stroke count" reading in our G9 wording). |
| C5 no-snap-cut (ease-in → hold → ease-out) | Ae Genius ladder: "no divots/creases, front-loaded velocity, designed settle"; our `V2.settle` is the right instinct, cubic eases are the floor (`6zrEKEuJGKs-VL-11-ae-genius-easing.md` §01/§05). EFP Editor: hold IS the emotion credit; Schoonmaker "hold a little too long — if justified" warrants our 0.5s hold floor (`3Q3eITC01Fg-VL-13a-everyframe-editor.md` §05). |
| Bible allows world tokens (Krakatoa earth family) as terrain, not decoration | Egg's register split is the proof that a *strict* two-palette rule "reads as intentional, not drift" (`h6fcK_fRYaI…` §05) — direct precedent for the register amendment in §2.1. |

### 1.2 What the corpus DISPROVES (or outruns)

| Bible/gate assumption | Corpus counter-evidence |
|---|---|
| "Hook = text on frame 0" (implicit in our stamp-heavy shorts; `hook_impact` rubric scored on stills with text assumed) | Zack: zero text at t=0, spectacle-first, ~255M/216M/167M (`ttuKeS5k4Uo…` §02, `yGw0nhlUtkQ…` §02, `rRAmNz6G3Tk-VL-03-zack-mcflurry.md` §02). Kurzgesagt Egg + MinutePhysics ×3: blank/near-black t=0, 100% audio-led (`h6fcK_fRYaI…` §02, `0fV8kYoGDNM-VL-15a-minutephysics-2plus2.md` §02, `31kyER-8dak-VL-15b-minutephysics-portals-cube.md` §02, `sEQvDbyFNbo…` §02). README synthesis: "the image (or voice) poses the question; text serves motion, not the hook. Our recent Shorts lean on stamp text to carry frame-0 — the corpus says invert that when the visual can." |
| "Text on screen is the default frame-0" → gate never built for audio-led opens | Egg: "black + voice = maximum open loop… our gate must never penalize audio-led opens (vlm_gate assumed visual hook; this is its weakness)" (`h6fcK_fRYaI…` §02 + README synthesis). MinutePhysics 2+2: "if our judge auto-fails blank t=0 frames, this video is the counter-evidence that the failure is stylistic, not categorical" (`0fV8kYoGDNM…` §06). |
| One locked palette for all story worlds (implicit single-register bible) | Egg: two worlds, strictly alternated, register shifts ARE the story (death→memory→afterlife) (`h6fcK_fRYaI…` §03). Kurzgesagt 1200-hours uses daylight cityscape + night space registers, "two registers again, one per story beat" (`uFk0mgljtns…` §03). MinuteEarth sunsets: gradient skies sell beauty, sketch diagrams sell mechanism — a deliberate two-register mix (`9PJvV5PYDm0-VL-14c-minuteearth-sunsets.md` §03). |
| "No fast cuts, ever" reading of C5 | Buff: 47 shots / 50.07s (MSL ≈ 1.07s) legible at phone scale via single-field plates; flash-triplet stings (≤0.3s cluster) land as deliberate punctuation (`VL-10a` §04). Edgar Wright: snap-inserts legal as *justified* laugh devices (`3FOzD4Sfgag-VL-13b-everyframe-edgar-wright.md` §05). C5's own "if justified" escape hatch covers this — but our transition taxonomy has no named members for it. |
| Type = caption support; stamps are decoration | Shop Vac: type IS the scene — word-as-object, slam+overshoot, one field per plate, ~2–4s perceptual re-layout density (`y4sOfO8Ei1g-VL-12-kinetic-shopvac.md` §03/§05). Our `stamp()` helper exists (`content/short-0005/render/scenes.html:292`) but has no grammar spec, no easing class, no thump-coupling rule. |
| "Muse is safe because we ease everything" | EFP Editor: build→release shape is not optional in polish work — shot-length ramps (long→short at climax→long release); uniform flat scene lengths read as machine-rhythm (`3Q3eITC01Fg…` §04/§05). Our L-097 advisory idea (stddev <15% warn) is corroborated. |
| "Our synth pad ≈ music" | Egg/1200h: original picture-timed scores; our Aadd9 pad is "a template, theirs is bespoke… BIG GAP" (`h6fcK_fRYaI…` §05, `uFk0mgljtns…` §05). Reddit/arXiv echo: no objective quality metric — hero moments need medium-res medium quality (`community-intel.md` §Reddit digest). |
| G9 wording ("primitives are a gate FAIL") | 1200h note: G9 "would flag their flat-vector birds as 'simple shapes' if judged on stroke count — the gate must judge *composition density*, not primitive count (worth checking ultracritic's G9 wording)" (`uFk0mgljtns…` §05). |
| Spectacle hooks must be visual | Zombie case for "the image poses the question" is broad, but Egg/AlternateHistoryHub prove *audio-first* immersion hooks work (black + march + second-person VO) (`MQW3VefRozc-VL-07-althistoryhub-wwi.md` §02). |

### 1.3 Net verdict

The bible's **palette law, stroke law, accent law, beam/glow recipe, layered-assets law (C14) and canvas-first backbone are CORRECT** — the corpus is unusually kind to them. What the corpus attacks is our **hook assumption (text at t=0), our single-register palette, our motion taxonomy (no named fast-transition classes), and our type mechanics (stamp without grammar)**. None of this is a craft failure; all of it is a *specification* failure. Amendments below are surgical, not a rewrite.

---

## 2. PROPOSED AMENDMENTS (C13-compliant format)

> Format per amendment: **Rule** (proposed bible text) · **Why** (corpus evidence) · **Where** (bible section + engine file + gate dim) · **Aesthetic risk**.

### 2.0 Amendment A0 — umbrella: "Register-aware scenes" (enables A1–A3)

- **Rule (bible §1 addendum, proposed):** "Every scene declares exactly one `register` from `{cosmic, earth, sea}`. A register is a token set, not a mood: it fixes background gradient stops, ground masses, fog/glow recipe, and which accent family is legal. Register changes happen ONLY at act/beat boundaries and are announced by the story (death→memory, surface→deep), never per-scene decoration. Two registers may coexist in one Short but never in one frame."
- **Why:** Egg register alternation = the story (`h6fcK_fRYaI…` §03); 1200h two-register daylight/space (`uFk0mgljtns…` §03); sunsets gradient-sky vs sketch-diagram registers (`9PJvV5PYDm0…` §03).
- **Where:** bible §1 (new subsection "Registers"); engine: `engine/core.js` (`V2.P` token groups) + `content/<slug>/render/scenes.html` (per-scene `register:` key); gate dim: new `register_consistency` check inside `production_polish` (or ultracritic G-case, see §3).
- **Aesthetic risk:** MEDIUM — a register flip at the wrong beat reads as a palette bug, not a story beat. Mitigate: one flip per Short max unless the story is explicitly two-world (Egg-shaped); gate checks register tag per scene vs declared intent in `gate/notes.json`.

### 2.1 Amendment A1 — `register` switch spec: cosmic / earth / sea

**Rule text (proposed bible §1.x — Register token table):**

| Token slot | `cosmic` | `earth` (Krakatoa family) | `sea` |
|---|---|---|---|
| background deep | `#070A18` (`bgDeep`) | pre-dawn/night warm-dark: `#1A0F14`→`#2A1610` horizon gradient (new token `bgEarthDeep`) | wave-blue deep: `#071B2E`→`#0B2E4A` (new token `bgSeaDeep`; mid `#123F5C` holds bioluminescence) |
| background raised/mid | `#0E1430` (`bgRaised`) | `crust #5C4038` / `rock #6B4B42` shadowed masses (`crust2 #4A3430`, `rock2 #57392F`) | `earthSea #1E5F8A` / `earthSea2 #174C71` (existing tokens, promoted from "Krakatoa terrain" to sea-primary) |
| sky gradient stops | `nebPurple #5B3A9E` → `nebPurple2 #3A2470` → `bgDeep` | ember dawn: `#FF8A3D` (low, sun-side) → `#C2447E` (mid) → `#2A1610` (zenith) — reuses `orange`/`nebMagenta` as *sky*, not accent | `#2FD4C5`-dim teal glow at shallow → `#0E3A52` → `#040E1C` abyss; abyss floor `#020A14` |
| legal accents (ONE per scene) | `amber`/`orange` (hero/glow) XOR `teal`/`blue` (cool rims, data) | `amber`/`orange` lava/sun XOR `cream` dawn shaft; lava-red `#FF5A4A` reserved heat/lava (bible §2 danger red) | `teal #2FD4C5` (bio/energy) XOR `blue #4AA8FF` (cold light/depth); abyss = NO warm accent, teal only |
| fog/glow recipe | cool `#9FC0FF→#4AA8FF→0` beams; warm `#FFD7A0→#FFB054→0` for hero cores | hot `#FF8A3D`-core glow low on horizon; `vCone` ember shafts; heavy vignette `vVig` 0.82 | teal glow `#7DF0E4→#2FD4C5→0`; god-ray cones from surface; abyss scenes: zero beam, rim-only |
| ground mass fills | `bgRaised` masses, strokeless | `crust/rock` families, strokeless; lava cracks = accent | `earthSea`/`earthSea2` masses; strokeless trench silhouettes |
| hero rim | warm `vRimR/L` (#FFB15A) or teal `vRimTeal*` per accent | warm rim only (dawn/lava side) | teal rim only (abyss); shallow-water scenes may use blue rim |
| typography stroke | `ink` on busy zones (existing) | `ink` or dark-brown `#2A1610` | `ink` or `#04121E` deep-sea navy |
| example scene | Krakatoa hook night sky, cosmos hero pulls | #0005 Krakatoa caldera at dawn; any volcano/impact lane | #0004 calm-water hero (r8 7.53) and any ocean/diver/reef lane |

**Consumption spec (how `scenes.html` should consume it — PROPOSED, not applied):**

```
scene(s) => {
  register: "cosmic" | "earth" | "sea",   // REQUIRED key; linter/gate reads it
  ...
}
```
`render/scenes.html` resolves the register once per scene into a local `R = REGISTERS[scene.register]` token bundle (gradient stops, accent, rim set, vignette strength). `V2.P` stays the flat palette; `REGISTERS` is a new pure lookup (no rendering logic). Existing scenes default to `cosmic` under a compat shim until re-authored. Bible §8 Accuracy pass gains step 0: "declare the register; every object checked against that register's legal accent."

**Story-move evidence:** The Egg proof is direct — the register split *carried the narrative* (cosmic ≠ human world; strict alternation; "register shifts ARE the story") (`h6fcK_fRYaI…` §03/§05). 1200h repeats it (daylight city ↔ night space) (`uFk0mgljtns…` §03). Sunsets uses two registers as beauty-vs-mechanism (`9PJvV5PYDm0…` §03). The Grolar diagram (color = legend) is the same principle at diagram scale (`ZA4OQ-1ahXg…` §03).

**Why (summary):** single-register bible forces every topic into night-space; corpus shows register-as-story is the highest-leverage palette move available to us, and we already own 80% of the tokens (`earthSea`, `crust`, `rock`, `nebMagenta`).
**Where:** bible §1 (new §1.x "Registers" + token table) + bible §7 (accuracy step 0); engine: `engine/core.js` (`REGISTERS` map), `content/<slug>/render/scenes.html` (scene key + resolve), `docs/playbook/scenes.md` (authoring doc); gate: `production_polish` + new `register_consistency` case (§3.3).
**Aesthetic risk:** MEDIUM-HIGH if misused — register flip without story cause = palette drift, the exact C12 failure. Hard rule: ≤1 flip per Short unless script declares two-world structure; flip must land on an act boundary beat; `gate/notes.json` must name the flip beat so the gate can check it.

### 2.2 Amendment A2 — Word-as-object stamp grammar (Shop Vac as our type-mechanics upgrade)

**Rule text (proposed bible §6 motion addendum + scenes.html `stamp` directive spec):**

"Stamp beats (word-as-object) follow ONE field per plate and a three-phase grammar: **SLAM** (≤150 ms in, `backOut`-class, ≥8% overshoot, 2–4f motion-blur impact frame) → **ARC** (word travels its entrance along a short arc/path — dial-sweep, diagonal blur-trail, or perspective plane — never a straight-line pop unless the beat is a *count-up pop*) → **OVERSHOOT→SETTLE** (`easeOutQuint` long tail, `V2.settle` damped sine amp 4–8 px decay ~6, ≥2f overshoot before dead stop). One field per plate: saturated single ground, cream/amber slab hero word, ≤1 glyph accent (star/asterisk/burst) optional, vignette on everything. Stamps couple to `finish_v3.py` `thump` at the same word timestamp. C5 splits into IN (fast + overshoot legal ≤150 ms) and OUT (ease-out ≥0.25 s mandatory)."

Concrete mechanics lifted from corpus (cite, don't copy art):
- Shop Vac: "type enters with hard ease-out + motion blur … fast in, dead-stop settle, hold, then hard cut. No floaty drift." Squash on slam; "impact frames carry 2–4 frame blur, then freeze clean"; star-wipe slam clips the word; perspective-floor "TOWN OF" locked to road plane; arc/dial word-on-path reveal; diagram-plate exploded views (`y4sOfO8Ei1g-VL-12-kinetic-shopvac.md` §03/§05).
- Buff Motion: "type plates slam scale with 2–4f blur then lock — same grammar as VL-12"; one accent glyph per plate; "nobrand" full-bleed serif on saturated field (`VL-10a` §03).
- Ae Genius: `sac_in` ≈ `backOut(s≈1.2)` ≤150 ms, ≥8% overshoot; `sac settle` ≈ `easeOutQuint` final 60%; "99% of the time this is how I work = add a third key and sculpt"; no-divots rule = in-between smoothness, not just cut-ease (`6zrEKEuJGKs…` §05).

**Our current state:** `stamp(t, x, y, text, size, color, …)` exists in scenes.html (`short-0005/render/scenes.html:292`, used at 540,760 "1883" and 540,1010 "36,000 LIVES") but has no overshoot/settle spec, no blur impact frame, no arc, no thump coupling, no linter check.

**Why:** our stamps are centered pops; the corpus' reference class treats the word as a physical object that arrives with mass. This is the single cheapest perceived-production-value delta available to us (pure canvas transforms + one `finish_v3` coupling).
**Where:** bible §6 (motion) + bible §2 (glow recipe reused for slam impact rim); engine: `engine/core.js` (add `V2.backOut`, `V2.easeOutQuint`, `V2.kf3`), `content/<slug>/render/scenes.html` (`stamp` directive gains `arc:`/`blur:`/`settle:` params), `tools/finish_v3.py` (auto-pair `thump` to `stamp` timestamps), `tools/script_linter.py` or new `tools/lint_stamps.py` (warn if stamp off-beat vs VO word grid); gate: `pacing_rhythm` + `production_polish`; ultracritic G-case for stamp legibility.
**Aesthetic risk:** MEDIUM. Overshoot on EVERY stamp = tic, not grammar (Buff rate-limits flashes ≤0.3s, ≤1 per Short; same discipline needed). Cap: ≤2 stamp slams per Short; each must be word-timed to the VO grid.

### 2.3 Amendment A3 — Easing standards by beat role + transition taxonomy (junk the gormless)

**Rule text (proposed bible §6, replaces/absorbs current "everything eases" vagueness):**

| Beat role | Easing class | Spec |
|---|---|---|
| stamp / slam (word-as-object, count-up land) | `backOut`-class impact | `backOut(t, s≈1.70158)` ≤150 ms in; ≥8% overshoot; 2–4f blur impact; settle via `easeOutQuint` + `V2.settle` (VL-11, VL-12, VL-13b backOut count-up) |
| reveal / scale-guide / verdict card / hero landing | `easeOutQuint` | long-tail settle ≈ post-expression "ease into resting spot"; replaces cubic `easeOut` on hero landings (VL-11) |
| breathe / idle / parallax / camera push | cubic `easeInOut` + `V2.settle` | existing law, unchanged; parallax 1.0→1.06 over a scene on held beats (bible §6) |
| count-up / number pops | velocity ease-**in** into landing, then stamp-slam | "accelerate INTO landing… then stamp-slam" (`3FOzD4Sfgag…` §05) — inverse of our default |
| transition taxonomy (render_short scenes) | canonical set | `notchWipe` (mask notch blocks, VL-10a f07) · `flashCut` (N≤3 immediate hard cuts ≤0.3s, pairs with whoosh/thump, VL-10a §03; VL-13b flash gags legal only with written justification) · `deadpanHold` (8–12 still frames post-gag/insight, max 1 per Short, `3FOzD4Sfgag…` §05, C4 exception) · `flipReveal` (scaleY −1→1 `easeOut`, VL-12 §05) · `typeArc` (glyph-on-arc, VL-12 f01) · `hardCut` (default, on eyes/pose-change frame, VL-13a) · eased slide (existing) |

**Hard caps (proposed):**
- `flashCut`: ≤1 cluster per Short, ≤3 frames, only with a written "if justified" note in `gate/notes.json` (mirrors Schoonmaker/C5 escape hatch, `3FOzD4Sfgag…` §05; `VL-10a` §05 "rate-limit the device so it stays a sting, not a tic").
- `deadpanHold`: max 1 per Short; 8–12 still frames; only post-insight/post-gag (Edgar Wright "one beat too long"; `3FOzD4Sfgag…` §03/§05).
- **1-hold-per-15s hard cap** on deliberate long holds: beyond one ≤4.5–5s hold per ~15s the pacing reads as Stall, not Breath (Buff's single 4.5s content hold amid 1.07s MSL is the ceiling case, `VL-10a` §04/§05; our L-097 floor stays 3.2s — this caps the *ceiling* deliberately).
- Shot-length shape should ramp, not flatline: advisory (not fail) when scene-duration stddev <15% of mean across ≥8 scenes — suggest build (shortening toward insight) → release (longest after) (`3Q3eITC01Fg…` §05; EFP Editor 15s up / 30s down release-heavier ratio).
- Release ≥ build: post-insight visual-only beat ≥ its pre-insight neighbor; our #0005 s9/s10 L-097 split is the right instinct — formalize as `finish_v3` expectation (`3Q3eITC01Fg…` §05; `3FOzD4Sfgag…` §05 "extend post-payoff hold ≥1.5× settle").

**Junked (proposed names, never used):** cross-dissolves (Buff: "No cross-dissolves visible", `VL-10a` §03), floaty drift/linear tweens (bible §6 already bans; corpus confirms), uniform 3.2s metronome (EFP Editor variance law), "ease everything the same" (VL-11 tier-1 "Easy Ease = noob").
**Where:** bible §6 (full rewrite of the section, boss-gated); engine: `engine/core.js`, `engine/rig.js` (`kf3`), `tools/render_short.py`/`scenes.html` (taxonomy directives), `tools/finish_v3.py` (whoosh↔flashCut, thump↔stamp pairing), `tools/script_linter.py` (attention-curve advisory), `docs/playbook/scenes.md`; gate: `pacing_rhythm`, `edit_flow` (new G-case: flash/deadpan caps; d²v spike lint VL-11 §05).
**Aesthetic risk:** LOW for easing classes; MEDIUM for `flashCut`/`deadpanHold` (overuse = tic); mitigated by hard caps + linter warnings + ultracritic G-cases.

### 2.4 Amendment A4 — Hook rule revision: text NOT mandatory at t=0 (audio-carry case)

**Rule text (proposed bible §4/§6 + `probe_hook.py` rubric revision):**

"Frame 0 must pose the question — by image, by voice, or both — but is NOT required to carry text. Three legal hook archetypes: (1) **Spectacle/image-led** (Zack: wound fills frame, zero words — `ttuKeS5k4Uo…` §02; MinuteEarth nuclear: bomb dominates t=0 — `nGutkWaXDUs-VL-14a-minuteearth-nuclear-weapon.md` §02; Maggie-McFlurry pattern-interrupt — `rRAmNz6G3Tk…` §02); (2) **Audio-led / blank-page** (Kurzgesagt Egg black + 2nd-person VO — `h6fcK_fRYaI…` §02; MinutePhysics ×3 blank lined paper, VO carries 100% — `0fV8kYoGDNM…` §02, `31kyER-8dak…` §02, `sEQvDbyFNbo…` §02; AlternateHistoryHub black + period march, ~8s before words — `MQW3VefRozc…` §02); (3) **Text-stamp** (current default, still legal — Shop Vac two-word title slam, `y4sOfO8Ei1g…` §02). Our stamp-text-at-t=0 default is demoted from 'the' hook to ONE of three."

Gate/probe implications (detailed in §3):
- `tools/probe_hook.py` rubric gains an **"audio-carry" case**: when t=0 is blank/black and VO carries the promise, score hook on VO content (question posed in sentence 1? stakes named? second-person address?) with a **wider tolerance band** (proposed: hook_impact ±1.0 vs image-hooks, and never auto-fail for absence of text). `vlm_gate.py`/`ultracritic.py` frame-0 prompt gains explicit "audio-led open: do NOT penalize empty/black frame; judge the voice promise" clause (today's prompt assumes a visual subject — `h6fcK_fRYaI…` §02, `0fV8kYoGDNM…` §06).
- Calibration set gains three new labeled anchors: (a) VL-01 stitches frame-0 (spectacle/image), (b) VL-15a 2+2 frame-0 (audio-led blank), (c) VL-06 Egg hook (audio-led black) — as "hook WITHOUT text" references; plus negative control VL-10a letter-assembly open (must score LOW).
- S3 orient law unchanged: topic noun still lands ≤3s — by voice if not by image (`ttuKeS5k4Uo…` §02 confirms Zack satisfies S3 in word 1).

**Why:** top-performers resolve tension identically — "the image (or voice) poses the question; text serves motion, not the hook" (README synthesis §Hook anatomy). Our recent Shorts "lean on stamp text to carry the frame-0 — the corpus says invert that when the visual can." Demoting text-at-0 is a rubric fix, not a content retreat.
**Where:** bible §4 (reference-frames/calibration rule) + bible §6; engine: none (prompt/rubric only); tools: `probe_hook.py` (audio-carry case), `vlm_gate.py` + `ultracritic.py` (frame-0 prompt clause), `docs/playbook/hook-calibration*` if present (rubric doc); gate: `hook_impact` (frame 0 only) + new G-case §3.2.
**Aesthetic risk:** LOW for spectacle hooks; MEDIUM for audio-led — a bad VO line with a black frame is WORSE than a weak text hook (no visual promise at all). Mitigate: audio-led opens require script-stage sign-off that sentence 1 poses the question AND stakes by word ≤10; probe set must include a failing audio-led case to keep the rubric honest.

### 2.5 Amendment A5 — Style revisions for quality (one paragraph per axis)

**Palette.** Hold `bgDeep #070A18`/`bgRaised #0E1430`/`nebPurple` cosmic core exactly as locked; ship the A1 token table for `earth` and `sea` as *world* tokens (the bible already legalizes `earthSea/crust/rock` for Krakatoa terrain — A1 promotes them to first-class registers and adds the warm-dawn sky stops + `bgSeaDeep`/abyss pair). One accent per scene stays inviolable; the Egg proves strict two-register alternation reads as intent, not drift (`h6fcK_fRYaI…` §03). Danger red `#FF5A4A` remains heat-only. Never blend registers in a frame; flips land on act beats with `gate/notes.json` declaring the flip. (C12 no-drift survives intact — drift is *within*-scene, not *between*-register.)

**Type.** Two legal systems, never mixed (text_discipline max-4 trigger today): (a) **caption band** — cream, sentence-case, bottom-20% (C10), 1–4 words/beat, white, small — the Zack system (`ttuKeS5k4Uo…` §03); (b) **stamp/word-as-object** — slab/all-caps hero word per A2 grammar, ≤2 per Short, word-timed to VO. Hand-lettered-in-scene labels for diagrams (MinuteEarth Grolar: color IS the legend, no legend box, `ZA4OQ-1ahXg…` §03) are a third *diagram-internal* system, legal only inside diagram plates. Shop Vac additions: letter-spacing as animation, word-on-arc, mirror-flip (`flipReveal`), perspective-plane type (`y4sOfO8Ei1g…` §03). Absolute ceiling: >8 words visible = max 5 (existing rule, unchanged, confirmed by #0003's 22-word failure, ultracritic.py header comment).

**Motion.** Canonical easing table per A3: `backOut` for slams, `easeOutQuint` for reveals/hero landings/verdict cards, cubic `easeInOut`+`V2.settle` for breath/parallax/camera, velocity ease-in for count-ups, `kf3` third-key sculpt for anything two keys can't express. Transition taxonomy is CLOSED (strong cut, eased slide, `notchWipe`, `flashCut`≤1/≤3f, `deadpanHold`≤1, `flipReveal`, `typeArc`, diagram-plate swap) — anything else is a C5 exception requiring written justification. Shot-length shape ramps (build→release), release ≥ build; one ≤4.5s hold per ~15s hard cap; parallax ≥2 planes at 0.3× (bible §6, corpus-confirmed: Kurzgesagt parallax multi-plane, `uFk0mgljtns…` §03; Egg value+hue separation not outlines, `h6fcK_fRYaI…` §03).

**Background rule.** Bible §1 "background = one of {deep space, raised, nebula gradient}" EXPANDS to "one register-appropriate ground per A1 table — {cosmic: bgDeep/bgRaised/nebula} ∪ {earth: crust/rock/warm dawn gradient} ∪ {sea: earthSea/abyss gradient}" — one field, zero competition, subject opposite value (C2). Zack's flat-sky discipline (`ttuKeS5k4Uo…` §03, `yGw0nhlUtkQ…` §03) and Egg's strokeless masses (`h6fcK_fRYaI…` §03) remain the invariants; bright-register daylight scenes stay OUT (1200h daylight excluded — our bible is dark; `uFk0mgljtns…` §05). Flat void = gate fail (checklist 7) survives only for cosmic; sea-abyss may run near-void with rim-only definition, which is register-legal because value structure is present (silhouette masses against graded water).

**Character rig.** Canvas stickman stays the backbone (community-intel: "canvas stickman stays the backbone… hero shots must be Medium-Res; identity drift/hands/context loss = failure modes"). Upgrades: Egg proves scale-as-empathy (small silhouette + giant simple-shape entity beats detailed faces) (`h6fcK_fRYaI…` §03) — our rigs may do ONE giant-silhouette beat per two-world short. `rig.js` gains blink/idle already present; add `deadpanHold` pose (8–12 still frames, post-gag/insight) and eye/brow keys already exist for comedy beats (`3FOzD4Sfgag…` §05). Register note: warm rim on earth register, teal rim on sea — rig rim-light selection follows register, not scene accent (avoid the #0005 r1 "amber+teal pair reads as UI artifacts" conflict, `short-0005/render/scenes.html:549`). Cut on pose/expression change (EFP Editor eyes-change analog, `3Q3eITC01Fg…` §05; Wright apex rule, `3FOzD4Sfgag…` §05) — a cut mid-gesture is an `edit_flow` fail.

**Audio.** Split the gap honestly: our synth bed (Aadd9 pad + riser/whoosh/thump, `finish_v3.py`) is license-free and serviceable BUT the corpus ceiling is bespoke picture-timed scores (Egg: composed to the finished video; 1200h: full score stage; AlternateHistoryHub: period-cue immersion before words, `MQW3VefRozc…` §02; Buff: thump-class word-timed stings, `VL-10a` §03). Proposed ladder: (1) NOW: auto-couple existing thump↔stamp, whoosh↔flashCut; per-video "cue" choice from a tiny license-free cue library (march/ambient/riser variants) for immersion opens; (2) NEXT: commission/generate ONE theme per formula lane (not per short) — closes 80% of the bespoke gap at ~0 marginal cost; (3) NEVER per-short bespoke scoring at our cadence. Also: duck nothing (music+VO mixed as one whole — Egg style, `h6fcK_fRYaI…` §05); VO stays edge-tts AndrewNeural for Shorts, but second-person/long-form ambitions need an intimate profile validated first (Egg GAP, `h6fcK_fRYaI…` §05). Sci-VBench/Heliyon echo: audio-led opens are safe — clarity-first scripting is the retention lever (community-intel bottom line #2/#4).

**Texture.** Bible §6 grain+vignette stays. Corpus additions: lined-paper/sketch-wobble is a *register* texture (earth/diagram lanes — MinutePhysics blank-page opens, `0fV8kYoGDNM…` §02); film-grain + archival-inset treatment only for real-archival payoff beats (MinuteEarth nuclear, max 1/video, `nGutkWaXDUs…` §05) — license/cost means we borrow the *device* not the footage; Shop Vac's grain/textured-paper vignette on stamp plates (`y4sOfO8Ei1g…` §03) — proposed as optional `stamp` plate backdrop; AlternateHistoryHub grain/vignette unify (`MQW3VefRozc…` §03) — already our finish step. DO NOT adopt 2D grain overlays at levels that fight the deep-space nebula grade.

---

## 3. GATE / ULTRACRITIC IMPLICATIONS

### 3.1 Dimensions that already hold (keep, cite evidence)
- `contrast_legibility` — Buff thumbnail-scale proof (`VL-10a` §05); C2 pre-render check stays. No new cases.
- `text_discipline` — existing >8 words = max 5; two systems = max 4 (ultracritic.py:81). A5 type section only *adds* a legal third diagram-internal system; no threshold changes.
- `pacing_rhythm` — L-097 floor stands; corpus confirms 3.2s (Grolar 197 WPM, `ZA4OQ-1ahXg…` §04) and permits breath at high-information diagrams. Keep dimension; add ramp advisory (not a fail) per A3.
- `visual_hierarchy` — #0004's ~6.9 format ceiling (L-085) is NOT a bible failure; do not chase it via style changes; the canvas-first format was the fix. Hold dim; expect format-level variance.
- `character_life` — rig blink/breathe/idle already enforced (C4); deadpanHold is a *permitted exception*, not a loosening.
- `edit_flow` — transitions breathe; taxonomy closure actually *tightens* this dim (unlisted transition = fail).

### 3.2 Hook audio-carry calibration (NEW cases/prompt clauses)
1. `vlm_gate.py` / `ultracritic.py` frame-0 prompt: add "If frame 0 is black/blank/near-empty and the VO poses the question, DO NOT score hook_impact down for absence of text; score the promise (question posed? stakes named? second-person address?)" (`h6fcK_fRYaI…` §02; `0fV8kYoGDNM…` §06).
2. `probe_hook.py`: new labeled class **audio-carry** with three calibration refs (VL-01, VL-06, VL-15a) + one failing case (audio-led open where sentence 1 poses nothing) to anchor the low end; tolerance band hook ±1.0 vs image hooks.
3. Judge-instruction gotcha: glm-4.5v markdown-fence parsing noise (carry_r10) means the audio-carry clause must be SHORT and imperative, or it becomes another vlm_parse casualty. Keep ≤2 sentences.

### 3.3 Register mismatch (NEW G-case)
`ultracritic.py` gains a register-consistency check (cheap, notes.json-driven, not VLM): for each scene, `scene.register` must equal the declared register in `gate/notes.json`; any scene whose dominant tokens fall outside its register's legal set (e.g., warm amber accent inside `sea`/abyss scene = >20% sampled pixels in warm band) flags `REGISTER_MISMATCH`. Hierarchy: notes.json vs pixels — pixel check advisory only when notes.json absent. Budget: one PIL pass, ms-class.

### 3.4 Mid-hold drift (NEW G-case) — guards the A3 "1-hold-per-15s" cap
Detect holds >4.5s where no depth-plane motion/blink/particle delta exists between sampled mid-hold frames (VLM-free, pixel-diff): flags `MID_HOLD_DRIFT` → routes to `pacing_rhythm` advisory. Rationale: Egg/Buff holds work BECAUSE something always moves (`h6fcK_fRYaI…` §04 "the eye constantly has particle/parallax motion"; `VL-10a` §04 sawtooth). A dead hold is a freeze, not a breath.

### 3.5 G9 ceiling checks (wording + two anchors)
- G9 stays "composition density / meaning density," NOT primitive count (`uFk0mgljtns…` §05) — **verify ultracritic's current wording**; if it says "stroke count/primitives," that's a bug, file it.
- G9 anchor ladder gains: VL-06 Egg frame (ceiling, meaning-dense flats) and VL-15c backwards-driving frame (floor-of-excellence for austere apparatus: zero decoration, total mechanism clarity, `sEQvDbyFNbo…` §06) — both rated as *craft* anchors only, never palette anchors.
- Note VL-08/12-hours explicitly: hand-illustrated vs generated — usable as process benchmark, never as frame anchor (`uFk0mgljtns…` §06).

### 3.6 What the gate must NOT do
No new hard fails for: audio-led opens (A4), register flips at declared beats (A1), flashCut/deadpanHold within caps (A3). These are *annotated permits* — logged, capped, judged as craft. The Sci-VBench lesson governs: correctness/clarity stay mandatory checks; perceptual quality is proxy — keep two-round publish (community-intel bottom line #5/#6; plan-30d Phase A/B fork stands).

---

## 4. BLOCKING QUESTIONS FOR THE BOSS (closed-response)

1. **A1 register table — ship as bible §1.x now, or hold until a register-native short (#0006?) is scripted?** (a) now, (b) with #0006, (c) never/keep single-register.
2. **A1 legal flips per Short:** (a) 1 max (Egg-strict), (b) ≤2 at act boundaries, (c) unlimited with notes.json declaration.
3. **Sea register scope:** is sea approved for #0004-style water lanes now, or only after a boss-rendered sea pilot clears the gate? (a) approve now, (b) pilot first, (c) refuse sea entirely.
4. **A2 stamp grammar: adopt `V2.backOut`/`easeOutQuint`/`kf3` into core.js** — (a) yes, all three, (b) backOut only, (c) hold all engine changes.
5. **A2 stamp cap per Short:** (a) ≤2 (recommended), (b) ≤1, (c) no cap.
6. **A3 transition taxonomy CLOSED list** — ratify the 8 named transitions and make unlisted = C5 fail? (a) ratify, (b) ratify minus flashCut, (c) ratify minus deadpanHold, (d) keep taxonomy advisory only.
7. **A3 flashCut cap:** (a) ≤1 cluster/Short, ≤3 frames, written justification (recommended), (b) ban entirely, (c) allow ≤2.
8. **A3 1-hold-per-15s hard cap** — (a) hard cap (gate-enforced), (b) advisory only, (c) reject.
9. **A3 release ≥ build + post-insight visual-only beat** — formalize as `finish_v3` expectation? (a) yes, (b) advisory in linter only, (c) reject.
10. **A4 hook rule revision** — demote text-at-t0 from default to one of three archetypes; ratify audio-carry probe case + wider tolerance? (a) ratify fully, (b) ratify spectacle-only, keep audio-led as gate-fail override case per-short, (c) reject (keep text-at-0 default).
11. **A4 VO bar for audio-led opens:** sentence 1 must pose question + stakes in ≤10 words — (a) hard script-lint, (b) script-review checklist only, (c) no bar.
12. **A5 audio ladder step (2):** commission ONE theme per formula lane — budget approval? (a) approve (license-free/CC0 or commission, cost TBD by boss), (b) step (1) only, (c) reject any audio spend.
13. **A5 second-person/intimate VO profile** for any future long-form/Egg-shaped work — (a) approve validation spike, (b) reject, edge-tts stands, (c) defer past Day 30.
14. **G9 wording:** if ultracritic says "primitive count," file as bug + fix to "composition density"? (a) yes, (b) leave wording, add clarification note only.
15. **§3.3 register mismatch + §3.4 mid-hold drift G-cases** — implement as notes.json/pixel checks (no VLM)? (a) both, (b) register only, (c) neither.
16. **#0006 skeleton:** belief-correction blank-page (MinutePhysics 2+2) vs name-swap puzzle (Grolar) vs what-if spine (V-07)? README flags all three; thesis for THIS proposal: (a) belief-correction, (b) name-swap, (c) what-if, (d) boss's call — proposals only.
17. **Reject list ratification (§5):** confirm Buff agency cold-open + hyperkinetic 1.07s MSL stay rejected for our format? (a) confirm, (b) revisit at Phase C.
18. **Cadence vs this proposal:** any amendment adopted → does it block day-018 cadence (plan-30d §1) or land as lint-only warnings first? (a) lint-only first, render next short, (b) block and amend bible now, (c) carry all to day-020 review.

---

## 5. WHAT NOT TO ADOPT

1. **Buff agency cold-open / identity-first logo assembly** (5s wordmark before promise) — wrong format for a Short; "take the letter-assembly device, not the pacing" (`VL-10a` §02/§05). Our hook must deliver the promise inside 2s (A4).
2. **Buff's hyperkinetic ~1.07s MSL as a house style** — it works because every plate is a single-field craft ceiling; adopting <1.07s MSL at our asset quality invites shearing. We adopt the *taxonomy and the one-hold-per-15s cap*, not thetempo (`VL-10a` §04/§05).
3. **Agency palettes / per-client plates / 2160p asset cost / UI-card chrome density** — our palette is locked C13; stickman world has no UI furniture (`VL-10a` §05).
4. **Kurzgesagt production scale as a target** — 1200h/video, 2–3 illustrators, 8–12 weeks; our $0/day pipeline cannot and should not chase it; adopt register discipline and parallax layering only (`uFk0mgljtns…` §05).
5. **MinutePhysics ~236–251 WPM as band target** — tolerable at 32s with short sentences, but our clarity-first lane breathes at ~150–200; Grolar 197 WPM is the Shorts calibration, Zack 149–158 the body-horror cadence reference (README synthesis; `0fV8kYoGDNM…` §04; `ZA4OQ-1ahXg…` §04).
6. **AlternateHistoryHub's slideshow-with-music craft** — fails G9/motion; structure only (what-if spine for #0001-class topics), never visual reference; also its frames are a *license/archival* rabbit hole we should not open for Shorts (`MQW3VefRozc…` §05/§06).
7. **MinuteEarth "Step N:" labels, host intro, 163s runtime, Patreon end card** — retention poison for Shorts loop mechanics; borrow the Step-3 split-screen and scattering-diagram composition only (`9PJvV5PYDm0…` §02/§04/§05).
8. **Zack's bright flat-sky photoreal palette as a visual reference** — hook mechanics only; he fails our dark bible by design, and that's correct (`rRAmNz6G3Tk…` §05, `ttuKeS5k4Uo…` §06).
9. **Cross-dissolves, floaty drift, linear tweens, metronome-uniform scene lengths, snap-cuts without written justification** (`VL-10a` §03; `3Q3eITC01Fg…` §04; bible §6).
10. **Out-frame spectacle as REQUIRED hook** — corpus disproves the necessity (A4); keep spectacle legal, not mandatory.
11. **ZI-style raw footage compositing** — copyright class; NASA/USGS PD only, with NOTICE.md attribution, and even then as payoff inset max 1/video (`nGutkWaXDUs…` §05; README compliance block).
12. **Real-footage archival beats for #0006** — out of scope for this proposal; flagged as future lane only.
13. **AI re-render route as a quality shortcut** — AGENTS.md §6: deterministic render is canonical; Wan2.2 text stamps drift ("180 dB"→"190 dB"); never gate/publish AI re-renders without boss sign-off. Not a style amendment; noted so no one "solves" A2 with it.
14. **Snap-zoom spam / needle-drop sync** (Edgar Wright montage density at Shorts scale; `3FOzD4Sfgag…` §05 "Not adoptable").
15. **Treating gate as oracle / automating publish on VLM alone** — community-intel (VLM engagement scores noisy; Sci-VBench judge–expert agreement only with rubrics) → two-round publish decision stays (community-intel bottom line #6; `3Q3eITC01Fg…` §05 §06).

---

## 6. Adoption order (if boss green-lights)

1. **Lint/prompt-only first** (zero render risk): A4 probe/prompt clauses, A3 linter advisories (ramp, flash/deadpan caps as warnings), §3.3/§3.4 G-cases, A2 stamp `backOut` behind a flag.
2. **Engine tokens** (A1 `REGISTERS`, A2 easings) — one PR, `lint_selftest.py`-class self-test.
3. **Bible text** (§1 registers, §6 motion rewrite, §4 calibration) — boss-signed; then `docs/playbook/scenes.md` follows.
4. **First register-native short** (#0006 candidate) as the proof render; gate as usual; carry report either way.
5. **Never:** bulk re-render of #0001–#0005 "to the new style." Cadence > polish (plan-30d §1).

## 7. Compliance & provenance

- Analysis-only. No corpus material composited into any render. No verbatim quotes >50 words used. No views/scores fabricated; all view/WPM figures are per-note (info.json / brief / prefix-diff estimates, ±10% where flagged).
- Notes carry their own UNKNOWNs (upload dates, detector reliability, sub-threshold dissolves); this proposal inherits them — no number here is stronger than its note.
- VL-09 (Gunner reel, vimeo 401/403), VL-17 (Reddit, 403), VL-16/VL-21/VL-22 (notes pending), VL-18/19/20 (boss-side) are EXCLUDED — nothing herein cites them.
- This file is research analysis; it must not be copied into scripts, thumbnails, descriptions, or published Shorts.
