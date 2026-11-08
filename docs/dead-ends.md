# Dead ends — tried, measured, failed. Do not retry without the stated condition.

> Reader: any agent about to "try something". Check this list first. Each entry:
> what was tried, what happened (measured), the condition under which a retry is
> allowed. Sources: ledger lessons in `docs/_archive/lessons/`.

| # | Dead end | What happened | Retry only if |
|---|---|---|---|
| D1 | **Fish `prosody_speed` rate knob** (1.25) | Measured 153 WPM vs 161 at 1.0 — did NOT move pacing into the 185–215 band (day-010). Suspected cause: MP3 silence padding eats the delta. | Silence per file is measured (`ffprobe silencedetect`) and trimmed, AND daily credits allow an A/B |
| D2 | **y2mate-class downloader sites** (y2mate, yt5s, yt1s, cnvmp3, 9xbuddy, savefrom, ovc, ssyoutube) | 2026 snapshot: connection failures, Cloudflare challenges, HTML at documented AJAX endpoints, JS-signed APIs. Sealed by design against this use case (L-057). Daily radar runs; research-only. | The radar (`research/cache/downloaders.json`) reports a site exposing a stable callable API — evaluate, never auto-wire |
| D3 | **Cobalt instances for YouTube** | Official blocked since 2025; 1 of 19 community instances alive and it requires an API key; self-hosting on a runner = same bot-wall (L-054). CLOSED. | Boss provisions a VPS/edge egress ($2–5/mo own-IP instance) |
| D4 | **Residential / self-hosted runner** | Banned by boss directive ("no residential runner, everything on yours or github runners"). The 5-leg matrix + mirror ladder replaced it (L-039). | Boss changes the directive |
| D5 | **Direct captions/extraction from cloud or runner IPs** | Bot-walled (IpBlocked / "Sign in to confirm you're not a bot") from every datacenter IP tried, incl. GitHub runners (L-031, L-049). Search (`ytsearch`) works; extraction doesn't. | A non-flagged exit appears (the matrix keeps trying fresh runner IPs daily) |
| D6 | **ID3-prefix media validation** | Rejected 24 valid Fish MP3s that used raw MPEG frame sync (0xFFFB) — the verifier was the bug (L-069). | Never; decode-based validation is the permanent fix |
| D7 | **ffmpeg `image2` demuxer for 1000+ frame encodes** | OOM-killed the sandbox repeatedly; `image2pipe` (cat | ffmpeg) is permanent (L-072). | Never on this filesystem class |
| D8 | **Judging temporal dims (pacing/life/flow) from stills** | Structurally capped: same short scored pacing 5.4 from PNGs and 8.0 from video (day-010). | Never; the video pass exists for this |
| D9 | **"Be harsh, if in doubt score lower" as a rubric prompt** | Compressed every frame to 4–7 regardless of quality — a bar nothing can pass is as broken as one everything passes (L-066 class, day-010). | Never; anchor ladders + measured calibration are the fix |
| D10 | **Remotion / Motion Canvas migration mid-sprint** | Cadence beats tooling (R10); the seek-driven SVG engine ships daily. Steal patterns (springs, interpolate) instead. | After the day-30 scoreboard, with boss sign-off |
| D11 | **Face morphing / smooth expression blends** | Expressions must SWAP through a blink; morphs read as broken (vendor look.md, adopted). | Never |
| D12 | **Fades as the default transition** | Motionmaxxing measured law: things arrive by moving/cutting/unmasking; fades only for deliberate single-object dissolves. | Calm-brand conditions only (not this channel) |
| D13 | **Full-sentence on-screen captions (karaoke subtitles)** | The published #0003 carried up to 22 words/frame → text_discipline 2.8/10, boss: "too many words on screen" (L-076). Keyword pills only. | Never |
| D14 | **Web downloaders in the pipeline generally; ElevenLabs production VO** | Policy (L-025): ad-ware converters banned; ElevenLabs free tier is non-commercial. | ElevenLabs: paid plan + license check |
| D15 | **Treating a single tool's failure as resource death** | WebFetch's "Not Found" / "Html Convert Error" on LIVE, REACHABLE resources nearly caused a live queue item to be retired (L-047/L-052). | Never; second-egress verification is the rule |
| D16 | **Editing files with stale old_str / batch edits unverified** | MultiEdit with pre-sed text silently no-op'd half a batch (day-008). Edits are verified by grep before moving on. | Never |
| D17 | **Estimating text widths by character count** | `len*size*0.62` undershot DejaVu Sans Bold → caption words merged ("groundgives") (day-003). Canvas measureText is permanent. | Never |
| D18 | **Scheduling agent wake-ups during live sessions** | One model slot: cron fires during evening chats died silently with "concurrency limit exceeded" (L-056). Deep-night slots only. | Platform gains multi-slot concurrency |
| D19 | **Hardcoded mirror lists** | 6/6 Invidious + 8/8 Piped defaults dead within days (L-050). Live registries, cached, always. | Never |
| D20 | **Silent success paths in CI workflows** | vo-gen run 1 "succeeded" with 0/8 files (L-068). Logging + fail-on-shortfall is the permanent shape. | Never |
