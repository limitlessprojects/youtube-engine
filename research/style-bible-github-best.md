# Top GitHub repos for style bibles & production "bibles" (2026-11-14, day-017)

> Boss asked: "style bible and all those exist on most starred repos on github find the best of those from github."
> Method: GitHub repository + code + readme searches (stars desc), fetched candidate files raw, re-ranked by
> fitness to OUR job (stylized science-Shorts, pixel-art-adjacent, gate discipline, Wan-Animate hero shots).
> License notes per repo — do not copy assets blindly; borrow STRUCTURES and RULE-FORMATS, not art.

## Honest framing

There is no Pixar/Dreamworks art bible on GitHub (rightfully). The starred artifacts that approximate "style bibles"
cluster into THREE classes, all listed below with real numbers (live fetched 2026-11-14):

- **A. Claude/agent studios with gate-structured bibles** (Donchitos, sickn33) — the "senior-pipeline" shape
- **B. Chinese AI short-drama / anime factories** (shuohao, wind-comic, ChrisChen667 — note: astronomically-starred Chinese studios are the actual production use case in 2026)
- **C. Creator-specific art bibles for open-licensed worlds** (ARIS, Leonxlnx)

## The shortlist (ranked for OUR pipeline)

| # | Repo | stars | License | What it IS | What WE take | What we skip |
|---|---|---|---|---|---|---|
| 1 | `sickn33/agentic-awesome-skills` → `skills/pro-launch/references/04-style-bible.md` | **49,700** (MIT, live-verified 2026-11-14) | Chinese "风格圣经" with RULES TABLE: one-line style name + reason; every rule has (rule / why / how-to-check); 要/不要 with verbatim user quotes; rejected-version screenshots with reasons; OFL-only fonts; colour-budget (frame = paper/ink; colour only for selection); high-frequency-word extraction; "one rule = one screenshot test" | **Format, not language**: our bible should adopt (i) one-line name + reason, (ii) every rule mappable to a screenshot/pixel check, (iii) a REJECTED section (we have ultracritic_r*.json for this), (iv) font licensing discipline | The iOS mirroring ("sounds like SwiftUI") metaphor — the check-notation prose is Chinese-then-English; do NOT cargo-cult it |
| 2 | `Donchitos/Claude-Code-Game-Studios` → `.claude/skills/art-bible/SKILL.md` | **39,216** | see repo (likely MIT) | Full Claude-Code studio w/ 49 agents, 72 skills; art-bible skill with LRIO review passes; director gates (AD-ART-BIBLE at Phase 5); one art-director drafts Sections 1–4 &9; user sign-off loop | **Gate order**: bibles that pass BEFORE asset production, not after; art director as single approval point; "no block = proceed + log" behavior we already implement via canvas-first | The RPG-studio-gamesim scaffolding; we don't need 49 agents |
| 3 | `eternityspring/shuohao-skills` → `skills/character-refs/` | **6,658** | Apache-2.0 | AI short-drama production engine: anchor-lock pattern (ONE front full-body anchor; every other view references only the anchor; stale-invalidation marking; asset.json + PNG + one-click report; 18 per-view variants; quant+seed audits) | **Character anchor protocol for our Wan-Animate hero-shot runs** — L-093/108 hero-shot inputs must be AR-matched/face-locked to one anchor; adopt the anchor→variant disclosure discipline wholesale | The ComfyUI plumbing is fine for them; we stay thin (2–3 variants, not 18) |
| 4 | `ChrisChen667788/wind-comic` | **714** | MIT | Chinese multi-agent studio: 1-line story → full short-drama video (script→cast→storyboard→VO→timeline→mp4), Next.js, 6,918 tests | **Provenance table discipline** (every asset traceable to a decision); consistency subsystem for cast look-locked reuse | It's an app (heavy infra); we never want the orchestration, only the discipline table |
| 5 | `wanshuiyin/ARIS-Movie-Director` → `examples/comic_min_author/ART_BIBLE.md` + `skills/comic-style-bible-lock/SKILL.md` | **78** | see repo | Minimal `STYLE_PREFIX[warm-lab]: flat pixel-art; Edison-lamp glow; 1-step shading` line template + cross-model audit loop; ART_BIBLE examples in plain text | **Prefix-lock**: a literal `STYLE_PREFIX[scene]` one-liner at the top of scenes.built.html to keep render-register per video consistent (we already do this manifestly in notes.json) | The audit tooling |
| 6 | `Leonxlnx/athenaion` / `PauliusOS/pallet-town-3d` (code-as-asset worlds) | 706 / 192 | see repos | Entire worlds built in code — zero asset files; every visual provably derives from source | The "world in source" stance we already own (engine/space.js, V2.REGISTERS); these are validation "it works at scale" demos | Code architecture (ours is tighter) |

### Also-relevant (starred, skip or file away)

- `TheOrcDev/skills` (106⭐) — CLI skills index; file-away, no direct lift
- `jbang2004/long-wind` (120⭐), `merlinhu1/codex-game-studio` (78⭐), `striderZA/OpenCodeGameStudios` (124⭐) — studio scaffolding; nothing for our content
- `ajinnaaa/extract-visual-style-2` (171⭐) — extracting visual bibles from references; useful for #0006 research pass when we sample a reference's palette from a rival Short automatically  
- `ChrisChen667788/wind-comic`-lineage clones (v13.17+) — reusable cast + series-continuity machinery if we ever go serial

## What this validates (our architecture)

1. Our **canvas-first → notes.json → art-director sign-off** order is the SAME shape the 39k-star studio uses.
2. Our **gate discipline** (VLM anchors + L-069 performer verify) is MORE rigorous than any of these repos (most have zero visual gates).
3. Our **forgeable failure modes** (palette drift, text-as-banner, snap cuts) are exactly what sickn33's "要/不要 with verbatim originals" format catches — we already have it in `ultracritic_r*.json` and L-077/085 lines.

## Consequences for our repo (proposed, not applied)

1. **Adopt `STYLE_PREFIX[scene]`** as a literal first line in scenes.built.html (additive, harmless if unused).
2. **Convert `content/style-bible.md` REJECTED fragments into a screenshots/REJECTED/ log** — every ultracritic FAIL gets a thumbnail + reason; becomes our bible's strongest section automatically.
3. **Character-anchor protocol for hero shots** (from shuohao): one anchor + all views from it + stale-marking on any model/seed change — document THIS as the L-093/108 acceptance spec (tracked in community-intel.md).
4. **Rule→screenshot tests**: every bible rule that cannot be checked by a still wins the
   "scripts/linter detects — nothing" bucket and drifts; L-090/L-097 already do this for math.

## TL;DR for boss

The best GitHub "style bible" for us is not one repo — it's a **blend**:
- `sickn33`'s rule-table+screenshot-check format (book-of-rules shape)
- `Donchitos`'s gate ordering (bible before assets, never after)
- `shuohao`'s anchor-lock protocol (character consistency)
- `wind-comic`'s provenance discipline (every pixel traceable to a decision)
- our own canvas-first + VLM gate + L-097/090 floor tests (already strictly better than all of them on the verify axis)

No single repo here will *change* our output on its own; all four reaffirm our order — adopt the formats, not the taste.

## Addendum (boss-verified 2026-11-14, session A — include this section verbatim)

Direct answer to "where are Pixar/DreamWorks' design bibles": **nowhere on GitHub.**
- GitHub repository search returns **0 results** for both `"design bible" pixar` and `"design bible" dreamworks`.
- The official studio GitHub orgs host technical/production tools, NOT internal art/design bibles:
  - **PixarAnimationStudios** (github.com/PixarAnimationStudios) — OpenUSD, OpenSubdiv, RenderMan-related projects.
  - **dreamworksanimation** — MoonRay, OpenRV, OpenEXR, USD plugins.
- Generic community art-bible guide worth a look (structure reference, NOT license-cleared to copy
  wholesale — tiny 2-page doc, unknown license terms, author: Guillem Álava Burgueño / @WillyTrek19 /
  supervised by @raysan5; status: educational study material, no studio affiliation):
  - **KiwiTrek/ArtBible** — "A useful guide around the creation and usage of art bibles for your own projects."
  Use its section ordering (purpose → materials → palette → typography → camera/lenses) as a sanity-check
  for our bible's organization; adopt nothing from its prose without a rewrite.
- Verify: KiwiTrek/ArtBible is educational-only; we adopt the section pattern, not the content.

Related official machinery worth tracking (technical, not art):
- Pixar: OpenUSD (`PixarAnimationStudios/OpenUSD`) — the industry interchange we render-hatch against
  (scene/material LOD descriptions, composition arcs); our scenes.built.html is a baby USD in HTML.
- DreamWorks: MoonRay (open-sourced renderman-terms successor) + OpenEXR (our .png set emission is fine).

**Bottom line:** the bible-annotation folk-knowledge on GitHub is agent-skills scaffolding + AI-studio
pipelines (above), not studio glossaries. KiwiTrek is the only "read the art-bible how-to" artifact and
is structurally useful only.
