# Blocked work log — wishlist items we could NOT complete from this machine (2026-11-14)

> Everything below is investigation state, not a failure to try harder. Each item lists:
> what was wanted, every route tried (with verbatim error/status), what would unblock it,
> and what is already known from open sources. analysis-only; nothing composited into renders.

## VL-09 — Gunner "Gunner Reel 2015–'22" (Tier 2 motion-craft reference, gunner.work → vimeo.com/758035927)

**Wanted:** Gunner's showreel 2015–'22 for C15 motion grammar (easing, overshoot, secondary motion).

**Routes tried (all failed):**
1. `gunner.work` → 200, but only link is `/reel/`; `/reel/` → **HTTP 500** (21 bytes) — showreel page dead.
2. Vimeo channel `vimeo.com/gunneranimation` → RSS lists the reel: `Gunner Reel 2015–'22`,
   duration 102s, 540×960 (`vimeo.com/758035927`, embed hash `h=764ddf2609`).
3. `player.vimeo.com/video/758035927` (with/without hash, with/without Referer header) →
   **HTTP 401** then **HTTP 403** (config JSON refused; ~3.6 KB error body).
4. Direct progressive-MP4 pattern `player.vimeo.com/video/758035927/config` → 403.
5. YouTube search via invidious (`Gunner showreel 2015 2022`) → no Gunner upload; only other studios (unusable).

**What we know (public, from the RSS we DID fetch):** the reel contains their published client work
(Storybots "Lasers", Duolingo "Duocon", Dropbox logo system, Walmart Text-to-Shop, Squarespace Walt,
Bones, Walt (153s)) — all character/brand motion, single-field colour, strong key-pose/hit frames,
matching the Buff Motion grammar at higher polish. Analysis from the RSS titles alone puts Gunner's
work in the same class as VL-10/12 — it would add calibration data, not a new doctrine.

**To unblock:** boss sends the 2015–'22 reel directly (any URL/MP4), OR a vimeo login/token for the
box, OR Gunner re-opens their /reel/ page. **Estimated value if it lands:** marginal — Tier 2
benchmark already covered by VL-10/11/12; affects calibration, not direction.

## VL-17 — r/comfyui Wan 2.2 Animate thread (Tier 4 hero-shot input→output grading)

**Wanted:** thread `reddit.com/r/comfyui/comments/1nle575` — Wan 2.2 Animate ComfyUI workflows,
demos, failure modes, quality expectations for community-driven character retargeting.

**Routes tried (all failed):**
1. `https://www.reddit.com/r/comfyui/comments/1nle575.json` → **HTTP 403**
   ("You've been blocked by network security. Log in to your Reddit account or use your developer token.")
2. `old.reddit.com/r/comfyui/comments/1nle575.json` → **404** (deleted/wrong id path or IDremoved as of 2026-11-14 — UNVERIFIED which).
3. `r.jina.ai/http://www.reddit.com/.../1nle575.json` proxy → proxied fine but upstream returned 403; proxy payload: "You've been blocked by network security…"
4. `https://www.reddit.com/r/comfyui/comments/1nle575` (browser UA, accept header) → **403**.

**What we know (community-intel.md §Reddit, flagged CANDIDATE not verified):** consensus from
search-snippet aggregation (not the live thread): AR-matched inputs; frames-skip=0; sweet-spot
480×832–854×480; quantization eats likeness first; failure modes = identity drift, hands,
context loss; quality is judged by eye/likeness/flicker with no objective metric; hero-shot runs
must stay Medium-Res. **This is second-hand until the thread is readable.**

**To unblock:** boss reads/saves the thread (paste the text or a screenshot), OR reddit API token
for this box, OR a reddit mirror that parses 1nle575 truthfully. **Value it adds:** hardens the
L-093 hero-shot spec (QA pairing contract, resolution choice, retries) — the anonymous ZeroGPU
WAN-Animate route is already built and probed; this would refine its acceptance thresholds.

## VL-18 / VL-19 / VL-20 — boss-side items (wishlist Tier 4/5)

- **VL-18** (phone clip performing one action): not attempted (boss filmed; needs direct file or a transfer link).
- **VL-19/20** (2–3 style-anchor Shorts "by your eye"): not attempted — boss must pick them.
- **VL-22** USGS "lava fountain" 0626 Popocatepetl sibling clips referenced by community members: untouched.

## VL-11 residual + VL-13b retry flap

- yt-dlp on this IP hit HTTP **429 Too Many Requests** on subtitles mid-batch (batch aborted VL-11);
  fixed by retrying without `--write-auto-subs` (merged manually, `.en.vtt` fetched via invidious captions
  endpoint — fine). **Lesson:** on YT subtitle 429s, drop autosubs and pull captions via invidious instead.

## NASA caption .vtt 403 (both VL-21a, VL-21b)

- `images-assets.nasa.gov/video/<id>.vtt` → **403 AccessDenied** with browser UA/Referer — NASA bucket
  serves thumbnails + .vtt links but blocks anonymous .vtt fetches from here. Imagery verified by frame
  reading only. If the boss wants verbatim captions: curl from a different egress, or ask your library
  contact — the .mp4s and .srt/.vtt are in `images-assets.nasa.gov/video/<id>/collection.json`.

## What IS committed (no action needed)

Everything else in the wishlist is on GitHub: 21/22 items analyzed (research/video-notes/), full
cleansed transcripts (research/transcripts/), index + README, learning_queue seeded, community-intel
with 12 arXiv papers, movement map, style/quality amendment proposal, motion_probe tool, L-109.
The only intentionally-untracked files: raw videos/captions/frames/.ci-artifacts (per repo .gitignore).

## Appendix 2026-11-14 (late) — exhaustion pass, boss: "unblock what is blocked"

- **VL-09 Gunner (vimeo.com/758035927)** — every anonymous route exhausted:
  yt-dlp says "The web client only works when logged-in" (login wall confirmed);
  `player.vimeo.com/.../config` 401→403; `/reel/` page 500s; gunner.work → legacy.gunner.work → vimeo channel only; YouTube search shows no Gunner uploads (only near-miss studios: Animasia, Magic Light, Film in Finland).
  **Status: requires boss cookie/file/token. Not unblockable from this box.**
- **VL-17 r/comfyui thread 1nle575** — `api.reddit.com/.../1nle575.json?raw_json=1` → 403 (two hosts); `old.reddit.com` → 404; r.jina.ai proxy → upstream 403; wayback machine (`archive.org/wayback/available`) → 0 snapshots.
  **Status: requires boss login/paste. Not unblockable from this box.**
- **VL-21 NASA captions (.vtt/.srt)** — bucket `images-assets.nasa.gov/video/<id>/*` returns 403 AccessDenied for both extensions with browser UA/Referer AND without; egress-independent bucket policy, not a network flap; no public API serves them.
  **Status: gone for good without a NASA grant/boss-provided export; frames analysis is complete and committed.**
- **CI run 43608071984 (19-chunk ai-rerender matrix)** — finished **failure** at 17:34Z (never assigned a runner). Nothing to cancel; no task lost (mission was re-scoped to hero-chunk-only this session).
- **VL-16b wan-animate rep-shots.mp4** — re-download in progress (~14.9/42.2 MB; server cuts connections; `-C -` resume loop running); will be integrity-verified by ffprobe when it lands.
- **E11venLabs A/B** — $6, commercial license; spend requires boss sign-off only.
- **Custom thumbnail phone verification** — Studio requires a verified number; boss must verify once in Studio; `--set-thumbnail` stays best-effort after that.
- **VL-18/19/20** — boss-side inputs (phone clip; style anchors by their eye; PD picks).
