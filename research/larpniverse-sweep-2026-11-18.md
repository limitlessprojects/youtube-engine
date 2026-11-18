# Larpniverse / "In this town" deep sweep — 2026-11-18 (day-022 evening session)

Boss directive: exhaustive multi-angle search (GitHub, Gists, GitLab, Hugging Face) for repos,
agent skill files, workflows or scripts replicating @larpniverse (Larptuber / Roblox "In this
world / In this town" surreal storytelling). Verified URLs only; groups A/B/C; absence proof
for exact matches; top-5 adaptable.

## Method — queries actually run

GitHub API repo search (authenticated): `larpniverse` · `larptuber` · `in this town roblox` ·
`huss huss` · `roblox story shorts generator` family. GitHub code-browse via clones.
Web sweep: github.com, gist.github.com (site: search), claudeers.com, awesomeskills.dev,
agentskillshub.top, aibase topic pages, TikTok/Instagram discover pages, huggingface.co
(spaces + text-to-video task), gitlab.com (public projects search). Full query log in the
appendix. Search API total counts are reproducible via
`https://api.github.com/search/repositories?q=<term>`.

## (A) Exact / direct matches — NONE (absence proof)

- `larpniverse` → **GitHub total_count = 0** (repos). Also zero on GitLab public projects,
  zero HF spaces/models, zero gists surfaced by `site:gist.github.com larpniverse`.
- `larptuber` → 2 repos, both unrelated (a LARP-ranking website stub `Larpest/LARPGPT`,
  a joke repo `eczook/larptube`). Neither touches the video format.
- `huss huss` → 15k+ false positives (Hussain names). Nothing format-related.
- Conclusion: **no public repo names itself after the creator or the meme.** The niche's
  tooling hides under mechanism names ("roblox engine", "story reels", "shorts skill") —
  which the (B) sweep then found.

## (B) Closest functional clones & automation repos (ranked by closeness)

### B1. nocodehack/nocodehack-roblox-engine — THE functional clone
https://github.com/nocodehack/nocodehack-roblox-engine
43★ (growing: 13→43 in ~2 days), Python, Apache-2.0, updated 2026-11-18 (same day).
- What: Claude Code skill — "makes animated Roblox-style Shorts from one line: story,
  animation, camera, sound". One file `stories/<name>/story.json` (cast, sets, timed beats,
  camera shots) → Blender 5.2 pipeline renders R6 blocky characters that walk/sit/grab/
  punch/emote on their own → SFX + music bed + captions + loudness mastered to YouTube.
- **"In this world..." is a built-in format** (engine/FORMATS.md §4): title card at t=0
  (1.5s), word-level captions with colored keyword, narrator voice, `story_cuts` camera,
  30-60s (hint 45s), beats = card → rule → 2-4 escalating vignettes → **final turn that
  re-reads the rule**. Plus `narrated_twist` format (hook ends in ellipsis, twist ~70%,
  freeze-frame with label card, loop line).
- Stack: Claude Code + Blender + Roblox Studio MCP (fetches real hair/faces/clothes from
  the user's Studio, ~50 hair / 110 shirts / 130 emotion-tagged classic faces), numpy/pillow,
  ffmpeg. ElevenLabs optional (characters "speak" in Roblox blips by default), Blotato for
  optional YouTube posting. Quality tiers: draft (minutes) / preview (~1h) / mid (~2h,
  postable) / cloud farm. Scene gates print REPORT PASS (body overlap, foot slide, hidden
  faces, jump cuts) — the same "verify the artifact" religion as our C6/L-125.
- Closeness: script→render→sound→caption→loudness = the Larpniverse pipeline shape minus
  the actual Roblox game capture; "In this world" IS one of its 10 formats.
- Missing vs Larpniverse: no trending-research loop, no gate on retention craft (it gates
  animation legality, not storytelling), no views feedback loop.

### B2. Harishisonline/rblx-animates-skill — the measured production bible
https://github.com/Harishisonline/rblx-animates-skill
1★ (new), Python + Blender kit, updated 2026-11-17. Claude plugin for the Instagram channel
@rblxanimates: **Blox City** (storyline episodes) + **In this town / In this world** (one-rule
worlds), 9:16 90-120s, original blocky Roblox-style characters.
- The `references/` folder is the richest public intelligence on this format anywhere:
  - `INTOWN_FORMAT.md` — beat-by-beat template MEASURED from two viral reference reels
    (premise 0-4s "In this town, [ordinary thing] [one exact rule]", first word ≤0.2s;
    rule mechanics; town texture (2-3 deadpan examples w/ 2-5-word kickers); personal
    stake; inciting event; escalation ladder ("The following night... Nothing. ...
    Nothing.", spoken countdowns); turn/discovery; reveal+callback — twist in a 4-6 word
    sentence, end immediately).
  - `ENDING_RULE.md` v2 (2026-11-18): "In this town/world" ends on the last story line,
    **hard cut, NO like/share/follow CTA** (0 of 32 giant-channel videos end on a viewer
    question). Story itself drives comments (loophole debates, mysteries, easter eggs).
  - `VOICE_SPEC.md` intown_v1 — the measured narration recipe: reels run 229-285 WPM,
    F0 median 181-203Hz, word gaps 0.1-0.4s (none >0.6s), -14 LUFS, LRA 0.8-1.9 LU;
    ElevenLabs "Alex" multilingual_v2 stability 0.55 / similarity 0.75 / style 0.0 /
    speed 1.15, cut gaps >0.34s→0.30s, two-pass loudnorm I=-14 TP=-1.5. Calm deadpan
    first-person AI storyteller — 0 exclamation marks, 0 spoken SFX, viewers accept the
    AI voice (AudioSet synth classifier 0.82-0.86).
  - `VIRAL_PLAYBOOK.md` — the feed-gate model (stayed-to-watch → %viewed+rewatches →
    shares/comments), premise generator formula (everyday action + absurd VISIBLE
    consequence + loophole/underdog flip), 7 premise families incl. **"Counter over your
    head"** and **"Power/tier/zero underdog"** (exactly our #0010 premise), premise score
    card (mute test: rule reads in 2s sound-off; 3x escalation), 10 mistakes, pre-publish
    checklist. Breakout benchmarks: 85-105% viewed on **35-55s** shorts.
  - COMPETITORS.md, GROWTH_LOOP.md, LESSONS.md, 2 full example episodes (scripts, cue
    files, mix configs, QA reports), face atlases, sound pack, TEMPOREX "Numbers" bed
    policy (copyrighted → kit composes an original numpy bed instead — same $0 doctrine
    as our L-124).
- Closeness: this IS a working channel's operating system for the format, with measured
  numbers — the best "production settings" source the boss asked to copy from.
- Missing: it renders in Blender (needs a Mac/GPU, ~5h/episode); no autonomous publish.

### B3. marktremmel/in-this-town-tutorial — the format's teaching handbook
https://github.com/marktremmel/in-this-town-tutorial
0★, HTML (GitHub Pages), updated 2026-11-16. A university unit (Digital Culture, SEK
Budapest): `files/In_This_Town_Handbook.pdf` (2.3MB, full machinima unit), Assignment
Brief, Story Doc Template, camera clips (dolly/orbit/timelapse), boards (keyposes, set,
props, lighting day/dusk, AI boards, bubbles, fx). Roblox Studio-native (not AI).
- Closeness: craft vocabulary (key poses, boards, set grammar) — useful as a checklist
  language, not a pipeline.

### B4. The meta-index: zhuyansen/awesome-claude-video-skills
https://github.com/zhuyansen/awesome-claude-video-skills — 2.1k★, 180 agent video skills,
security-graded, EN/中文. The registry where the niche skills surface (agentskillshub.top
lists 515 video skills; "Stories & animation" = 35). Start here for any future sweep.

### B5. Adjacent faceless-shorts automation (same pipeline shape, not Roblox)
- https://github.com/howznguyen/shorts-kit (161★) — narrated vertical shorts with a coding
  agent + Remotion; 9+ agent skills, 20+ story flows, **fact ledger**, CC0 SFX. The nearest
  cousin to OUR canvas pipeline (and it validates the fact-ledger idea we already run).
- https://github.com/gyoridavid/short-video-maker (1.5k★) — MCP + REST shorts maker.
- https://github.com/IgorShadurin/app.yumcut.com (914★) — prompt→vertical video w/ script,
  scenes, voiceover, subtitles.
- https://github.com/itsPremkumar/Automated-Video-Generator (130★) — agentic text→video,
  free TTS, captions, MIT.
- N8N ViralFlow (self-hosted n8n: prompt→shorts w/ TTS, Docker/Ollama/MinIO).
- https://github.com/ayush-that/jiang-clips (337★) + tryvinci/vinci-clips (159★) — long→
  short clippers (different problem: repurpose, not originate).

## (C) Prompt / skill file templates found
1. `nocodehack-roblox-engine/skills/roblox-engine/SKILL.md` (15KB) — the full agent
   workflow (setup gates, format picker, write→lint→gate→draft→look→HQ→sound_mix loop,
   "only fix what a REPORT or frame shows — one change, one scene" ≈ our L-125).
2. `nocodehack .../engine/FORMATS.md` — machine-readable story.json specs per format
   (in_this_world, narrated_twist, versus, POV, skit, time-stamped...).
3. `rblx-animates-skill/kit/SKILL.md` (33KB) + `references/*` (INTOWN_FORMAT, ENDING_RULE,
   VOICE_SPEC, VIRAL_PLAYBOOK, STORY, MUSIC_PLAYBOOK, LESSONS) — prompt-grade specs with
   measured numbers (see B2).
4. `marktremmel/in-this-town-tutorial/files/Story_Doc_Template.html` — a fill-in story
   doc for the format.
5. Gists: nothing format-specific surfaced (site:gist.github.com sweeps: roblox story
   tiktok / "in this town" / "in this world" → only unrelated hits). No leaked
   Larpniverse course dumps exist publicly under those names.

## The extracted production settings we are actually adopting (→ #0010)

| Setting | Value (source) |
|---|---|
| Length | 35-55s sweet spot (VIRAL_PLAYBOOK breakouts; boss script 52s) |
| Pace | 229-285 WPM delivered, calm deadpan, 0 "!", 0 spoken SFX (VOICE_SPEC) |
| Gaps | 0.1-0.4s, none >0.6s; first word ≤0.3s (ours: gap 0.25s ✓) |
| Sentences | median 9-10 words; ~15% are 1-5-word kickers ("Nothing.") |
| Structure | premise+exact rule in sentence 1 → mechanics → texture → stake → escalation ladder → turn → 4-6-word twist, hard cut |
| Ending | NO CTA; last story line; hard cut; loop-friendly (ENDING_RULE v2) |
| Loudness | -14 LUFS, LRA ≤2 LU, TP -1.5 (we ship -15 LUFS house, close) |
| Mute test | rule must read sound-off in 2s → giant $0 / $50,000 stamps |
| Shares | absurd rule + big escalation + twist (not moral lessons) |
| Category | Entertainment (24) for fiction lane (channel science lane stays 27) |

## Top-5 adaptable in under 30 minutes (for OUR canvas stack)
1. **rblx-animates references** — read INTOWN_FORMAT + VOICE_SPEC + ENDING_RULE, apply to
   script + VO immediately (done for #0010). Zero code.
2. **nocodehack FORMATS.md beat schemas** — the escalation-ladder + rule-re-read beat
   math, portable to any script.json.
3. **shorts-kit fact-ledger pattern** — we already run it (L-091); steal their 20+ story
   flow list for the topic bench.
4. **in-this-town-tutorial boards/keyposes vocabulary** — a pre-render "board" contact
   sheet discipline (we have contact_sheet.py; formalize as a gate artifact).
5. **awesome-claude-video-skills index** — subscription sweep weekly for new niche skills.

## Appendix — full query log (reproducible)
GitHub repo search: larpniverse (0) · larptuber (2, irrelevant) · "in this town" roblox (7
→ 4 relevant) · huss huss (noise) · roblox story video generator · faceless shorts
automation · brainrot video generator. Web: "larpniverse github" · github "in this town"
roblox story generator · site:gist.github.com roblox story tiktok · "how to make viral
roblox stories" master prompt · huggingface roblox story space · gitlab roblox shorts
automation · claudeers.com + awesomeskills.dev + agentskillshub.top registries · TikTok/
Instagram discover ("how creators make Roblox story Shorts" — social tutorials, no repos).
HF: no niche spaces (only generic Wan2.2/LTX text-to-video). GitLab: nothing relevant.

— Compiled by the day-022 evening session; clones of B1-B3 under /tmp/larp-research for
  reference (not vendored; licenses: Apache-2.0 / custom-NOASSERTION / none).
