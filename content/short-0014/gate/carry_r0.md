# carry_r0 — short-0014 handoff (day-031, effective-09:45 session -> world-build session)

## DONE this session (all committed)

- Fork verdict EXECUTED: #0013 relit 108→133→133 flat (T+61h) — fiction lane DEAD
  per day-030 pre-registered rule; science lane takes the slot. #0014 = science.
- Topic: "The stitches doctors never remove" (backlog rank-2, narrowed to the
  dissolve story; sequel grammar to #0006 = channel #1 performer).
- script.md + script.json: 14 beats (13 narrated + s7b 1.2s visual-only hold),
  110 words, timeline 40.074s. Lint PASS (opener 11w, beat law 14/13, WPM band OK).
- VO: 13 mp3s fresh (vo/), ASR 13/13 PASS wer=0.00 FIRST RUN — zero throttle,
  NO union debt. WPM measured 199.7 (dead center 185-215).
- Critic r1 agent-judged PASS (all six dims >= 8, round 1) — gate/critic_r1.md.
- SFX: 14 events, beat-derived from measured TL (L-146 protocol).

## NEXT SESSION OWNS: world build -> render -> gate -> publish

1. World: clone content/short-0013/render/scenes.html as the base (the engine:
   LOOKS presets + LOOK_KEYS blends, deterministic mulberry PRNG, bean() cast with
   blink/pose/sway/walk-bob, camera creep on every hold + ease-out glides, flash/kick
   event windows, SEQ map). Rebuild the beat content per script.json visual.v3 fields:
   skin-hill landscape, bead-chain seam, droplet link-snaps, WEEK ticks, strength bar,
   macrophage swallow, body cross-section, two tuned chains, permanent glint, clean-skin
   end mirror. CRITICAL (L-0013 bug class): SEQ map must key sequential TL ids (s0..s11
   + s7b) to semantic beat kinds — build_timeline renumbers; verify beat 0 = hook seam
   pull and s7b = the hold BEFORE rendering.
2. Look: bright-3d v2 (bible bands lum 0.43-0.54 / sat 0.38-0.65; ink outlines, DOF).
   Light arc: clinic-golden default -> deep macro cool at s8 -> warm day at s11 end
   (clean skin lands in daylight).
3. Render: python3 tools/render_short.py short-0014 --full --workers 4 (~1200 frames
   at 40.07s x 30fps). Then motion probe (scripts/motion_probe_png.py pattern),
   pixcheck lum/sat vs bible bands.
4. Mux: chunked recipe (L-139; scripts/mux_0012_chunked.sh pattern), decode-clean verify.
5. finish_v3.py short-0014 (SFX 14 events + bed ~-8dB per friend bible).
6. Gate r1: tools/ultracritic.py (judge glm-5.3-flash; if dead -> L-115b D8
   agent-review path, labeled). Bar: combined >= 7.2 precedent band = publish; else
   iterate per docs/playbook/gate.md (max 3 laps, L-125 polish-lap law).
7. Publish: tools/youtube_upload.py (disclosure OFF default, L-143), thumbnail =
   best hook frame (hook_u50 pattern), published.json, mirrors to upload/ +
   download/. Then lessons + log + commit+push (L-083).

## Disciplines

- Before publish: sitrep + git log diff vs session start HEAD (L-130/L-136 sibling guard).
- Publish lock content/.publish.lock (L-130b).
- r3 polish directives from #0013 (hill-lull figure, earlier payoff, hook-mirror end
  frame) — apply where the story allows; the end-frame mirror is ALREADY specced (s11).
