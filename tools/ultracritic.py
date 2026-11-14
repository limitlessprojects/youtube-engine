#!/usr/bin/env python3
"""ultracritic.py — THE pre-publish quality bar (boss directive, 2026-11-08).

"the video should go through ultracritical vlm feedback iteration before
getting your final posting approval must score out of a certain number of
ranking before its deemed worthy to post"

Usage: tools/ultracritic.py <slug> [--round N] [--frames t1 t2 ...]
                                     [--skip-mechanical]

Part A — MECHANICAL checks (no VLM, instant):
  A1 caption budget: EMPHASIS keyword list per scene ≤ 5 words (L-073/L-076;
     the published #0003 showed up to 22 words/frame = 2.8/10 text_discipline)
  A2 scene pacing: mean scene length ≤ 3.2s, max ≤ 4.2s (L-075; #0003 ran
     4.22s mean against a 1–2s sub-beat spec)
  A3 orientation: hook narration must name the topic (a noun from the title)
     — #0003 never said "sunset" until t≈14s (boss: "no introduction to what
     the topic is about")
  A4 spine: no NEW capitalized entity in the last 2 scenes (tangent-closer
     detector; #0003's Mars beat)
  A5 bed audibility: mastered audio non-VO RMS must sit 6–22 dB under VO RMS
     (L-074; the old inverted-ducked bed was ≈ -30 dB = absent)

Part B — VLM rubric, TWO passes:
  B1 FRAME pass (still-judgeable dims): text_discipline,
     visual_hierarchy, contrast_legibility, production_polish on every
     frame; hook_impact on FRAME 0 ONLY (boss directive 2026-11-09:
     hook_impact asked "would this frame STOP a thumb-scrolling viewer"
     — a property of the thumbnail/hook frame, not of diagram cards;
     averaging it across all frames structurally capped #0004 at 6.6-6.9
     for 7 rounds while craft dims hit 8+)
  B2 VIDEO pass (temporal dims — only if render/short_final.mp4 exists):
     pacing_rhythm, character_life, edit_flow — judged on the actual
     video, because pacing and life-in-motion are temporal properties a
     still cannot show (day-010 calibration: judging them from PNGs
     compressed every frame to 4-6 regardless of real quality)

PUBLISH THRESHOLD (the "certain number" — calibrated day-010):
  · grand mean (all 8 dims) ≥ 7.5/10  AND  every dimension mean ≥ 7.0
  · a frame scoring < 6 on ANY dimension fails that frame
Below threshold → NO POST. Iterate: apply directives → re-render → --round N+1.
Hard cap 3 rounds/night (cadence guardrail): still below → carried to the
next session with the report attached. PUBLISH-OR-REDESIGN IS AUTONOMOUS
(boss directive 2026-11-09: sign-off removed — "you're the autonomous
successful established youtuber in charge"). After a carried round with
hierarchy/composition dims still < 7.0 across 2+ rounds, the call is
structural REDESIGN of the offending scenes, never another polish lap
(carry_r7.md D3; 7 polish rounds moved hierarchy 6.1→6.4 only).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SR = 24000

THRESH_MEAN = 7.5  # day-010 calibration (2 measured rounds + anchor ladder): 7 = solid/clean,
THRESH_DIM = 7.0   # see THRESH_MEAN note
THRESH_FRAME_FLOOR = 6.0

RUBRIC = """You are THE ULTRACRITIC — a merciless pre-publish reviewer for a vertical YouTube Short (1080x1920).
Judge ONLY production values: visual design, text craft, polish. IGNORE narration wording and script content entirely. Score as if reviewing a competitor's video that must EARN its publish slot.

Score each dimension with this EXACT anchor ladder:
· 9-10 = exceptional, broadcast-grade, distinctive — you would screenshot this as a reference
· 8 = excellent — clearly above the average successful Short
· 7 = SOLID — the honest score for a frame with zero defects and clean craft
· 5-6 = flawed — real problems visible (clutter, dead zones, weak focal point, mushy contrast)
· 3-4 = amateur — actual defects (unreadable text, broken layout, illegible)
· 0-2 = broken
Score what you see against these anchors. Do NOT compress scores downward because perfection is rare — a defect-free frame IS a 7, a distinctive one is 8+. Reserve ≤4 for frames with actual defects.

Dimensions:
1. hook_impact: would this frame STOP a thumb-scrolling viewer? instant focal point + intrigue?
2. text_discipline: word count on screen (count EVERY text element). >8 words visible = max 5. TWO competing text systems (e.g. big header + separate caption block) = max 4. One clean system with ≤6 words = 8+.
3. visual_hierarchy: one clear focal subject? guided eye path? depth/layers? no large dead zones?
4. contrast_legibility: would every element survive a 6-inch phone in daylight? foreground/background separation?
5. production_polish: shadows, glows, alignment, palette control, craft details.

Return STRICT JSON only: {"scores": {"hook_impact": n, "text_discipline": n, "visual_hierarchy": n, "contrast_legibility": n, "production_polish": n}, "mean": n, "words_visible": n, "top3_directives": ["specific fixable directive", "...", "..."]}"""

# Body frames (frame 1+): identical minus hook_impact — a diagram card is
# not a thumbnail; judging it on thumb-stopping power manufactured the
# structural 6.x ceiling (carry_r7.md). Boss directive 2026-11-09.
RUBRIC_BODY = RUBRIC.replace(
    "1. hook_impact: would this frame STOP a thumb-scrolling viewer? instant focal point + intrigue?\n",
    "").replace(
    '"scores": {"hook_impact": n, "text_discipline": n',
    '"scores": {"text_discipline": n')

VIDEO_RUBRIC = """You are THE ULTRACRITIC — pre-publish reviewer judging a vertical YouTube Short VIDEO (with sound muted for this pass).
Judge ONLY production values: pacing, editing rhythm, animation life. IGNORE narration wording and script content.

Anchor ladder (EXACT):
· 9-10 = exceptional — professional editor rhythm
· 8 = excellent
· 7 = SOLID — honest score for clean, watchable, correctly-paced editing
· 5-6 = flawed — visible rhythm problems
· 3-4 = amateur — pacing actively hurts the video

Dimensions:
1. pacing_rhythm: does the visual tempo hold attention? scene changes and sub-beats neither freeze nor frantic; diagram cards hold long enough to register.
2. character_life: does the character read ALIVE — breathing, blinking, pose changes across scenes, reacting to beats — or like a static cutout slid between backgrounds?
3. edit_flow: cuts feel motivated, transitions breathe (ease in, hold, ease out — no snap-cuts), the loop from last scene back to the hook composition lands.

Return STRICT JSON only: {"scores": {"pacing_rhythm": n, "character_life": n, "edit_flow": n}, "mean": n, "top3_directives": ["...", "...", "..."]}"""


# ---------------- Part A: mechanical ----------------

def mech_checks(short: Path) -> tuple[list[str], list[str]]:
    fails: list[str] = []
    warns: list[str] = []
    script = json.loads((short / "script.json").read_text())

    # A2 pacing
    starts = [script["hook"]["timestamp_start"]] + [s["timestamp_start"] for s in script["scenes"]]
    ends = [s["timestamp_start"] for s in script["scenes"]] + [script["timeline"]["total_s"]]
    durs = [e - s for s, e in zip(starts, ends)]
    mean_d = sum(durs) / len(durs)
    if mean_d > 3.2:
        fails.append(f"A2 mean scene {mean_d:.2f}s > 3.2s (pacing)")
    if max(durs) > 4.2:
        fails.append(f"A2 max scene {max(durs):.2f}s > 4.2s (pacing)")
    if len(durs) < 10:
        warns.append(f"A2 only {len(durs)} beats in {script['timeline']['total_s']:.0f}s — target ≥ 12 visual events")

    # A3 orientation: a title noun must appear in the hook narration
    title_nouns = [w for w in re.findall(r"[A-Za-z]{4,}", script["title"])
                   if w.lower() not in {"what", "when", "where", "which", "your", "never", "it's"}]
    hook_low = script["hook"]["narration"].lower()
    if title_nouns and not any(n.lower() in hook_low for n in title_nouns):
        fails.append(f"A3 hook never names the topic {title_nouns[:4]} — orient first, subvert second (L-073)")

    # A4 spine: new capitalized entities in the last 2 scenes = tangent closer
    early = " ".join([script["hook"]["narration"]] + [s["narration"] for s in script["scenes"][:-2]])
    early_caps = set(re.findall(r"\b[A-Z][a-z]{2,}\b", early))
    for s in script["scenes"][-2:]:
        new = [c for c in re.findall(r"\b[A-Z][a-z]{2,}\b", s["narration"])
               if c not in early_caps and c not in {"The", "And", "But", "Same", "Only", "Your", "What"}]
        if new:
            warns.append(f"A4 new entity {new} appears only in the closer — tangent? (L-077 spine rule)")

    # A1 caption budget from scenes.html EMPHASIS table
    html_p = short / "render" / "scenes.html"
    if html_p.exists():
        html = html_p.read_text()
        m = re.search(r"const EMPHASIS = \{(.*?)\};", html, re.S)
        if m:
            for line in re.finditer(r"(\w+):\s*\[([^\]]*)\]", m.group(1)):
                sid, words = line.group(1), [w.strip().strip('"\'') for w in line.group(2).split(",") if w.strip()]
                if len(words) > 5:
                    fails.append(f"A1 scene {sid}: {len(words)} caption keywords > 5 (L-076)")
        else:
            warns.append("A1 no EMPHASIS table found — caption budget unverifiable")

    # A5 bed audibility (needs the mastered file)
    ok, detail = bed_check(short)
    if not ok:
        fails.append(f"A5 {detail}")

    return fails, warns


def bed_check(short: Path) -> tuple[bool, str]:
    """Master non-VO RMS must be 6-22 dB under VO RMS (audible but polite)."""
    import numpy as np
    master = None
    for cand in ["render/master.wav", "render/short_final.mp4"]:
        p = short / cand
        if p.exists():
            master = p
            break
    if master is None:
        return True, "bed: no mastered file yet (checked at master time)"
    try:
        r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(master), "-f", "f32le",
                            "-ac", "1", "-ar", str(SR), "-"], capture_output=True, timeout=180)
        y = np.frombuffer(r.stdout, dtype=np.float32)
        if len(y) < SR:
            return True, "bed: master too short to measure"
        script = json.loads((short / "script.json").read_text())
        spans = [(script["hook"]["timestamp_start"],
                  script["hook"]["timestamp_start"] + script["hook"]["audio_dur_s"])]
        for s in script["scenes"]:
            spans.append((s["timestamp_start"], s["timestamp_start"] + s["audio_dur_s"]))
        n = len(y)
        vo_m = np.ones(n, bool)
        for s, e in spans:
            vo_m[max(0, int((s - 0.05) * SR)): min(n, int((e + 0.05) * SR))] = False
        rms = lambda m: float(np.sqrt(np.mean(y[m if isinstance(m, np.ndarray) else slice(None)] ** 2)) + 1e-12)
        r_vo, r_bed = rms(vo_m), rms(~vo_m)
        if r_vo <= 0:
            return True, "bed: VO absent?"
        db = 20 * np.log10(r_bed / r_vo)
        if db < -22:
            return False, f"bed inaudible: {db:.1f} dB under VO (< -22; L-074 class)"
        if db > -4:
            return False, f"bed too loud: {db:.1f} dB under VO (mud)"
        return True, f"bed {db:.1f} dB under VO ✓"
    except Exception as e:  # noqa: BLE001
        return True, f"bed: measure skipped ({type(e).__name__})"


# ---------------- Part B: VLM rubric ----------------

def unwrap(raw: str) -> str:
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict) and "choices" in obj:
            return obj["choices"][0]["message"]["content"]
        if isinstance(obj, dict) and "content" in obj:
            return obj["content"]
    except json.JSONDecodeError:
        pass
    return raw


def extract_json(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError("no JSON in response")
    return json.loads(m.group(0))


def vlm_score(frame: Path, rubric: str | None = None) -> dict | None:
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "v.json"
        for _ in range(3):
            r = subprocess.run(["z-ai", "vision", "-p", rubric or RUBRIC, "-i", str(frame),
                                "-o", str(out)], capture_output=True, text=True, timeout=240)
            raw = out.read_text() if out.exists() else r.stdout
            try:
                v = extract_json(unwrap(raw))
                if "scores" in v:
                    return v
            except (ValueError, json.JSONDecodeError):
                continue
    return None


def main() -> int:
    slug = sys.argv[1]
    short = REPO / "content" / slug
    round_n = int(sys.argv[sys.argv.index("--round") + 1]) if "--round" in sys.argv else 1
    skip_mech = "--skip-mechanical" in sys.argv

    fails, warns = ([], []) if skip_mech else mech_checks(short)
    if fails:
        print("❌ MECHANICAL FAIL — fix before spending VLM calls:")
        for f in fails:
            print(f"  FAIL: {f}")
        for w in warns:
            print(f"  warn: {w}")
        (short / "gate" / f"ultracritic_r{round_n}.json").write_text(
            json.dumps({"round": round_n, "mechanical_fails": fails, "warns": warns,
                        "verdict": "MECHANICAL_FAIL"}, indent=1))
        return 1
    for w in warns:
        print(f"  warn: {w}")

    frames = sorted((short / "gate").glob("*.png"))
    if not frames:
        print("no gate frames — run render_short.py --keyframes first")
        return 1
    results = []
    for i, f in enumerate(frames):
        rub = RUBRIC if i == 0 else RUBRIC_BODY  # hook_impact: frame 0 only
        v = vlm_score(f, rub)
        if v is None:
            print(f"  {f.stem}: VLM FAILED (3 attempts)")
            continue
        v["frame"] = f.stem
        v["is_hook_frame"] = (i == 0)
        results.append(v)
        s = v["scores"]
        mean_v = v.get("mean") or sum(s.values()) / len(s)
        flag = "" if mean_v >= THRESH_MEAN else "  ← below bar"
        print(f"  {f.stem:10s} mean {mean_v:.1f}  (words {v.get('words_visible','?')}){flag}")

    if not results:
        print("VLM produced no verdicts — do not publish")
        return 1

    dims: list[str] = []
    for r in results:
        for k in r["scores"]:
            if k not in dims:
                dims.append(k)
    # hook_impact (frame 0 only): average over frames that HAVE the dim
    dim_means = {d: sum(r["scores"][d] for r in results if d in r["scores"])
                 / max(1, sum(1 for r in results if d in r["scores"])) for d in dims}
    frame_means = [r.get("mean") or sum(r["scores"].values()) / len(r["scores"]) for r in results]
    # floor check on each frame's OWN dims (body frames carry 4 dims, hook 5)
    frame_floor_breaches = [r["frame"] for r in results
                            if min(r["scores"].values()) < THRESH_FRAME_FLOOR]
    hook_score = results[0]["scores"].get("hook_impact") if results else None
    if hook_score is not None:
        print(f"  hook_impact (frame 0 only): {hook_score}")

    print(f"\n  FRAME GRAND MEAN {sum(frame_means)/len(frame_means):.2f}/10 (bar {THRESH_MEAN})")
    for d in dims:
        mark = "✓" if dim_means[d] >= THRESH_DIM else "✗"
        print(f"  {mark} {d:22s} {dim_means[d]:.1f}")
    if frame_floor_breaches:
        print(f"  frames below {THRESH_FRAME_FLOOR} floor: {frame_floor_breaches}")

    # ---- B2: VIDEO pass (temporal dims) on the rendered mp4 ----
    video = None
    for cand in (short / "render" / "short_final.mp4", short / f"{slug}.mp4"):
        if cand.exists() and cand.stat().st_size > 100_000:
            video = cand
            break
    video_dims = {}
    video_directives = []
    video_source = "none"
    agent_vp = os.environ.get("ULTRACRITIC_VIDEO_JSON")
    if agent_vp:
        # Agent-judged temporal pass — this box has no video-VLM backend (OpenRouter
        # 402s video, Z.ai balance empty, Gemini key dead). Scores below were produced
        # by the agent watching the cut, and the report labels them as such. Never
        # present them as a model's verdict.
        try:
            vp = json.loads(Path(agent_vp).read_text())
            video_dims = {k: float(v) for k, v in vp["scores"].items()}
            video_directives = vp.get("top3_directives", [])
            video_source = "agent-judged (no video VLM backend available)"
            print(f"\n  VIDEO pass (temporal dims) — AGENT-JUDGED via {Path(agent_vp).name}")
            for d, val in video_dims.items():
                mark = "✓" if val >= THRESH_DIM else "✗"
                print(f"  {mark} {d:22s} {val:.1f}")
            for dd in video_directives[:3]:
                print(f"    → {dd[:110]}")
        except Exception as e:  # noqa: BLE001
            print(f"\n  ⚠ ULTRACRITIC_VIDEO_JSON unreadable ({e}) — video pass treated as MISSING")
            video_dims = {}
    elif video is not None and video.stat().st_size > 100_000:
        print(f"\n  VIDEO pass (temporal dims) on {video.name} ({video.stat().st_size//1024} KiB)")
        # glm-4.6v via SDK video_url (the CLI vision endpoint rejects mp4 as
        # an image format — day-010); prompt via temp file. The script lives
        # IN the repo so node resolves z-ai-web-dev-sdk from the project root
        # (the old /home/z/.bun copy died with the recycle — BUG, day-011)
        vid_script = Path(__file__).resolve().parent / "ultracritic_video.mjs"
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as pf:
            pf.write(VIDEO_RUBRIC)
            prompt_path = pf.name
        r = subprocess.run(["node", str(vid_script), str(video), prompt_path],
                           capture_output=True, text=True, timeout=300)
        vv = None
        if r.returncode == 0 and r.stdout.strip():
            # L-066 class bug (fixed day-010): the model may wrap the JSON in
            # prose/markdown — extract_json handles that; the old
            # startswith("{") guard rejected valid verdicts
            try:
                vv = extract_json(r.stdout)
            except (ValueError, json.JSONDecodeError):
                vv = None
        if vv:
            video_source = "glm-4.6v via z-ai SDK video_url"
            video_dims = vv["scores"]
            video_directives = vv.get("top3_directives", [])
            for d, val in video_dims.items():
                mark = "✓" if val >= THRESH_DIM else "✗"
                print(f"  {mark} {d:22s} {val:.1f}")
            for dd in video_directives[:3]:
                print(f"    → {dd[:110]}")
        else:
            err = (r.stderr or "").strip().splitlines()[-1:]
            print(f"  ⚠ video pass failed (rc={r.returncode}) {err[0][:140] if err else '(no stderr)'}")
            print("  ⚠ frame pass alone cannot approve — fix the video pass, re-run")
    else:
        print("\n  ⚠ no rendered mp4 — temporal dims unverified; run the full render first")

    # ---- combined verdict ----
    all_dims = {f"frame:{d}": v for d, v in dim_means.items()}
    all_dims.update({f"video:{d}": v for d, v in video_dims.items()})
    n_frames = len(frame_means)
    frame_grand = sum(frame_means) / n_frames
    if video_dims:
        video_grand = sum(video_dims.values()) / len(video_dims)
        grand = (frame_grand * n_frames + video_grand * 3) / (n_frames + 3)  # video pass counts as 3 frames
    else:
        grand = frame_grand
    ok = (grand >= THRESH_MEAN and all(v >= THRESH_DIM for v in all_dims.values())
          and not frame_floor_breaches and bool(video_dims))
    verdict = "PUBLISH_APPROVED" if ok else "BELOW_BAR_NO_POST"
    report = {"round": round_n, "verdict": verdict, "grand_mean": round(grand, 2),
              "frame_grand_mean": round(frame_grand, 2),
              "dim_means": {k: round(v, 2) for k, v in all_dims.items()},
              "frame_means": {r["frame"]: round(m, 2) for r, m in zip(results, frame_means)},
              "floor_breaches": frame_floor_breaches,
              "video_directives": video_directives,
              "video_pass_source": video_source,
               "frames": results, "warns": warns}
    (short / "gate" / f"ultracritic_r{round_n}.json").write_text(json.dumps(report, indent=1))
    print(f"\n  COMBINED GRAND MEAN {grand:.2f}/10 (bar {THRESH_MEAN}) — video pass required")
    print(f"{'✅' if ok else '❌'} {verdict} → gate/ultracritic_r{round_n}.json")
    if not ok:
        # autonomous publish-or-redesign triage (boss: sign-off removed)
        chronic = [d for d in ("frame:visual_hierarchy", "frame:hook_impact")
                   if d in all_dims and all_dims[d] < THRESH_DIM]
        if chronic:
            print(f"  DECISION (autonomous): chronic structural dims {chronic} — "
                  "REDESIGN the offending scenes (one dominant element), not another polish lap")
        else:
            print("  DECISION (autonomous): dims are craft-level — apply top3 directives, one more round")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
