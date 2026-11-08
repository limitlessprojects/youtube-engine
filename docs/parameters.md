# Parameters — every tuned constant, its value, why, and its source

> Reader: an agent tuning or questioning a number. If a value here and a value in
> code disagree, THE CODE WINS and this file must be fixed. Sources: `L-###` ledger
> lessons (raw text in `docs/_archive/lessons/`), day-### measurements, commit ids
> where relevant. UNVERIFIED = believed but never measured.

## Script & pacing

| Parameter | Value | Why | Source |
|---|---|---|---|
| Shorts WPM band | **185–215** | edge-tts AndrewNeural +25% voice class; #0004 measured 201 = dead center; #0003 at 205; the older 155–175 band shipped #0001 at 154 = too slow for Shorts (MinuteEarth short-form reference: 176) | `tools/script_linter.py` `WPM_BAND` (day-010); day-007 autopsy |
| Long-form WPM band | 155–175 | original calibration; long-form not yet produced | linter (day-002 era) |
| Mean scene length | ≤3.2s | #0003's 4.22s mean read slow at 205 WPM — static holds, not audio, pace a Short | L-075; linter + ultracritic A2 |
| Max scene length | ≤4.2s | hard ceiling so no beat freezes | L-075 |
| Visual events per ~35s | ≥12 (warn) | sub-beat stamps count; 11 beats + stamps measured well | L-075 (#0004: 11 beats, warn at <10) |
| Opener length | ≤14 words FAIL, ≤12 target | hook must land ≤3s (1.8s ideal) | linter; L-016 |
| Short-sentence ratio | ≥0.15 warn | uniform cadence is a synthetic tell | L-015 |
| Words per ~35s Short | 90–110 | 94 words → 31.2s at 201 WPM (#0004) | day-010 |
| VO line gap | 0.45s default / **0.25s brisk** (`VO_GAP_S`) | brisk gaps for the ≥12-event cut-density class | vo_pipeline (day-010) |
| Words on screen per frame | ≤8 (pill ≤5 keywords) | two competing text systems scored 2.8/10; ≤7 words/frame lifted text_discipline to 7.4 | L-076; caption.js + A1 |

## Voice

| Parameter | Value | Why | Source |
|---|---|---|---|
| edge-tts voice | `en-US-AndrewNeural` | validated keyless default; 179 WPM at +45% on hook test | day-007/008 |
| edge-tts rate | `VO_RATE` env, default +45%; **+25% measured in-band on recent scripts** | text-dependent: same voice+rate ran 238 WPM on #0003's script vs 207 on #0002's; measure per script | day-009; #0004 used +25% → 201 WPM |
| Fish voice | s2.1-pro-free, ref `802e3bc2b27e49c2995d23ef70e6ac89` ("Energetic Male") | measured ~2.6–2.68 w/s at rate 1.0 (=161 WPM, below band) | L-005; day-009 A/B |
| Fish prosody_speed | 1.25 → 153 WPM (below band) | the knob did NOT move pacing into band; possibly MP3 silence padding. Do not retry without silence-trim first (see dead-ends D6) | day-010 |
| ASR WER thresholds | pass ≤0.15, warn ≤0.30 | catches mumbles/mis-synth before render budget | vo_pipeline; L-006 |
| ASR known bias | plural "s" after "bird" dropped by the ASR model | control-tested at normal rate — the verifier, not the TTS | L-066 (day-008) |
| ASR pacing | 2s sleep between lines | service returns empty when hammered | day-008 |
| Fish A/B decision rule | ASR WER first; pacing band breaks ties | WER tied at 0.035 on #0003 → edge won on 205 vs 161 WPM | day-009 |

## Audio mix

| Parameter | Value | Why | Source |
|---|---|---|---|
| Bed peak | 0.16 (≈ −16 dBFS pre-duck) | 0.062 peak (≈ −24 dBFS) was inaudible under VO — the boss heard "no bed at all" | L-074; finish_v3 `bed()` |
| Bed duck under VO | −9 dB, 150 ms ramps | audible-but-polite; verified by measurement | L-074 fix (day-010) |
| Bed audibility gate | non-VO RMS 6–22 dB under VO RMS | catches both "inaudible" (<−22) and "mud" (>−4) | ultracritic A5 |
| Master target | −14 LUFS integrated / −1.5 dBTP / LRA 11 | vendor what-if-animation recipe; #0001 −13.96, #0003 −15.25 both passed ears | finish_v3; vendor master.py |
| SFX classes | riser / whoosh / thump / blip (numpy-synth) | license-free $0; per-short `sfx` table in script.json, else #0002 legacy fallback | day-008/009/010 |

## Render & encode

| Parameter | Value | Why | Source |
|---|---|---|---|
| Frame | 1080×1920 @ 30 fps | Shorts vertical | render_short.py |
| Tail pad | 0.45s | hold black after final fade | render_short.py `--full` |
| Keyframe probes | 1/scene (u=0.5) if scene ≤4.5s, else 3 (u=.25/.6/.9) + end-state probes | enough coverage to catch end-state bugs without VLM budget blowout | render_short.py; L-040 |
| Encode | h264 crf18 preset medium, aac 192k, +faststart | shipped quality on all 4 shorts | finish_v3 |
| Frame feed | `image2pipe` via cat — never image2 demuxer | image2 OOM-kills this sandbox at 1000+ frames; pipe did 1026 frames in 34s | L-072 |
| Render speed (heavy hook) | ~3.6 s/frame at 236 birds/frame | 1000-frame render ≈ 60 min — acceptable nightly; sprite cache is the v4 fix | day-008 |
| Probe frames | any t via `--times` | word-timed beats need word-timed probes | L-065 |

## The gate (ultracritic)

| Parameter | Value | Why | Source |
|---|---|---|---|
| Publish bar (grand mean) | **≥7.5 / 10** | calibrated by measurement: a judge whose honest ceiling for clean frames is 7.0–7.2 would make an 8.5 bar a wall; 7.5 = "solid or better everywhere, clearly solid overall". Boss-criticized #0003 measures 5.20 → fails hard | L-078; ultracritic.py `THRESH_MEAN` |
| Dimension floor | every dim mean ≥7.0 | no dimension may drag | L-078 |
| Frame floor | no single frame <6.0 on any dim | a broken frame can't hide in a mean | L-078 |
| Video pass weight | counts as 3 frames in the grand mean | temporal dims (pacing/life/flow) can't be judged from stills — measured 5.4 (PNG) vs 8.0 (video) on the same short | day-010; ultracritic.py |
| Rounds cap | 3 per night, then carry with report | cadence guardrail; debt is paid next session, never forgiven silently | day-010 amendment |
| vlm_gate re-render cap | 2 per scene | loop guard | architecture guardrail |
| Critic revision cap | N=2 then discard premise | loop guard | L-020 |
| Anchor ladder | 7 = solid/clean, 8 = excellent, 9–10 = exceptional, ≤4 = actual defects | prevents score compression ("be harsh" alone compressed everything to 4–7) | day-010 calibration |

## Vision/infra

| Parameter | Value | Why | Source |
|---|---|---|---|
| Video pass model | glm-4.6v via SDK `video_url` (muted) | the z-ai CLI vision endpoint rejects mp4 ("图片输入格式错误") | day-010 |
| VLM retries | 3 attempts, JSON-extract (regex `\{.*\}`), never `startswith("{")` | model wraps JSON in prose; a startswith guard rejected valid verdicts (L-066 class) | day-010 fix |
| yt-dlp timeout | 180s normal / **75s in proxy mode** | 180s × 3 slow proxies blows a CI leg | L-041 |
| Proxy cache TTL | 20 min | balance freshness vs list fetch | proxy_pool.py |
| Mirror registry cache | 24 h | registries are themselves fetchable JSON | fetch_instances.py (L-050) |
| Views freshness rule | judge a video at ≥48h | Shorts take 2 days to distribute | day-009 stall watch |
| Cron payload limit | ≤2000 chars | platform limit (undocumented until it killed wake-ups) | day-007 |
| Nightly slot | 23:45 EAT (04:45 Beijing) | GLM quota trough; after the 20:00 UTC Actions run | day-007 |

## Engine craft constants (ported/adapted from vendor)

| Parameter | Value | Why | Source |
|---|---|---|---|
| LightVeil strength | 0.28 in wides that must show the floor; 0.42–0.5 elsewhere; ≤0.52 | at 0.52 the floor vanished; holes ≈ the size of the light pool | vendor what-if traps.md (adapted into `V2.veil`) |
| Contrast law | subject value opposite of ground value | camo kills diagrams (bird #10182E on panel #101832) | L-063 |
| Rig limb angles | `a` from straight down; forearm absolute `a2 = a + b` | a:158,b:-120 looks "up" in text but draws down (a2=38°) | L-071 |
| Caption band | bottom 20% (y ≥ 1536); pill center y=1700, font 74px | safe zone; scrim pill added for daylight phones | gate checklist; caption.js (day-010) |
| Face changes | expressions SWAP through a blink, never morph | morphing reads as broken | vendor look.md |
| Emphasis | spent, not spread: the payoff beat gets the longest, richest scene; stamps are fast | montages cut ~fast, the core moment holds | L-003; motionmaxxing law 4 |
| Palette tokens | defined once in `V2.P` (navy/cream/amber family; per-world variants like DAY in #0004) | one world, one light, one accent | L-004 |

## UNVERIFIED / open measurements

- **Fish silence padding**: leading/trailing silence in Fish MP3s never measured
  (`ffprobe silencedetect`) — required before re-judging the prosody_speed knob
  (dead-end D6).
- **Render wall-clock per short**: #0003 ≈ 2h session wall-clock (no sprite
  cache); #0002 ≈ 60 min heavy-hook. The 40-min Day-014 target is not yet met.
- **hook_impact on mid-video frames**: day-010 notes it is structurally capped
  (a diagram frame can't "stop a scroll"); rubric revision (score frame 0 only)
  is PROPOSED, not applied — threshold unchanged this session per constraints.
