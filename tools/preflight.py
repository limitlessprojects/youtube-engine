#!/usr/bin/env python3
"""preflight.py — every cheap check, before any render budget is spent.

Usage:
  python3 tools/preflight.py <slug>     # exit 0 = proceed; 1 = fix first
  python3 tools/preflight.py --selftest # L-066 control test: every check must
                                       # FIRE on a known-bad fixture

Enforces (docs/rules.md IDs in brackets):
  P1 script.json schema + non-empty fact_sources on every line  [S7, S10]
  P2 vo_lines.json present, one line per scene + hook            [stage 2 input]
  P3 EMPHASIS keyword pills ≤5 per scene, parseable              [C1/A1]
  P4 gate/notes.json present and covering every scene id         [G2]
  P5 banned-vocabulary scan on narration                         [S1]
  P6 per-short sfx table present (warn — legacy fallback exists) [stage 4]
  P7 ≥10 scenes for a ~35s short (warn)                          [S6]
  P8 scenes.html: renderFrame defined, no Math.random/state      [C6]
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
from script_linter import BANNED  # noqa: E402 — single source of truth [S1]


def check_short(slug: str, root: Path | None = None) -> tuple[list[str], list[str]]:
    """Returns (fails, warns). `root` override exists for the selftest fixtures."""
    base = (root or REPO / "content") / slug
    fails: list[str] = []
    warns: list[str] = []

    # ---- P1 script.json schema ----
    sj = base / "script.json"
    if not sj.exists():
        return [f"P1 missing {sj}"], warns
    try:
        d = json.loads(sj.read_text())
    except json.JSONDecodeError as e:
        return [f"P1 script.json is not valid JSON: {e}"], warns
    for key in ("title", "format", "hook", "scenes", "timeline"):
        if key not in d:
            fails.append(f"P1 script.json missing top-level '{key}'")
    if fails:
        return fails, warns
    lines = [(d["hook"].get("narration") or "", "hook")] + [
        (s.get("narration") or "", f"s{i}") for i, s in enumerate(d["scenes"])
    ]
    for narr, sid in lines:
        if not narr.strip():
            fails.append(f"P1 scene {sid}: empty narration")
    hook = d["hook"]
    for k in ("narration", "visual"):
        if k not in hook:
            fails.append(f"P1 hook missing '{k}'")
    for i, s in enumerate(d["scenes"]):
        sid = f"s{i}"
        for k in ("narration", "visual", "timestamp_start"):
            if k not in s:
                fails.append(f"P1 scene {sid} missing '{k}'")
        srcs = s.get("fact_sources") or []
        if not srcs or not any(str(x).strip() for x in srcs):
            fails.append(f"P1 scene {sid}: fact_sources empty (rule S7 — no claim without a source)")
        v = s.get("visual") or {}
        for k in ("pose", "prop", "background"):
            if not v.get(k):
                warns.append(f"P1 scene {sid}: visual.{k} empty — the composer maps these")
    if not (d["hook"].get("fact_sources") or []):
        fails.append("P1 hook: fact_sources empty (rule S7)")

    # ---- P2 vo_lines.json ----
    vl = base / "vo_lines.json"
    if not vl.exists():
        fails.append("P2 missing vo_lines.json (stage 2 input — write it before VO)")
    else:
        try:
            v = json.loads(vl.read_text())
            n = len(v.get("lines", []))
            want = len(d["scenes"]) + 1
            if n != want:
                fails.append(f"P2 vo_lines.json has {n} lines, script has {want} (hook + scenes)")
            if not all((l.get("narration") or "").strip() for l in v.get("lines", [])):
                fails.append("P2 a vo_lines entry has empty narration")
            keys = [l.get("key") for l in v.get("lines", [])]
            expect = ["hook"] + [f"s{i}" for i in range(len(d["scenes"]))]
            if keys != expect:
                # legacy shape (#0003 era: role strings) still works with
                # vo_pipeline; the key convention is the going-forward spec.
                warns.append("P2 vo_lines keys don't follow the hook/s0… convention (templates/vo_lines.template.json)")
        except (json.JSONDecodeError, KeyError) as e:
            fails.append(f"P2 vo_lines.json unreadable: {e}")

    # ---- P3 + P8 scenes.html ----
    html_p = base / "render" / "scenes.html"
    if not html_p.exists():
        fails.append(f"P1 missing {html_p}")
    else:
        html = html_p.read_text()
        if "function renderFrame" not in html:
            fails.append("P8 scenes.html: no renderFrame(t) — the renderer drives this")
        if "Math.random" in html:
            fails.append("P8 scenes.html uses Math.random — frames must be pure functions of t (rule C6)")
        m = re.search(r"const EMPHASIS = \{(.*?)\};", html, re.S)
        scene_ids = [f"s{i}" for i in range(len(d["scenes"]))]
        if m:
            for line in re.finditer(r"(\w+):\s*(null|\[([^\]]*)\])", m.group(1)):
                sid, words = line.group(1), line.group(3)
                if words is not None:
                    kws = [w.strip().strip('"\'') for w in words.split(",") if w.strip()]
                    if len(kws) > 5:
                        fails.append(f"P3 scene {sid}: {len(kws)} caption keywords > 5 (rules C1/A1)")
            covered = set(re.findall(r"(\w+):", m.group(1)))
            missing = [s for s in scene_ids if s not in covered]
            if missing:
                warns.append(f"P3 EMPHASIS has no entry for {missing} (ok if their stamp IS the text — be deliberate)")
        else:
            warns.append("P3 no EMPHASIS table — captions unverifiable pre-render (rule C1)")

    # ---- P4 gate/notes.json (rule G2: BEFORE the first keyframe render) ----
    notes_p = base / "gate" / "notes.json"
    if not notes_p.exists():
        fails.append("P4 gate/notes.json missing (rule G2 — write it BEFORE the first render; L-070)")
    else:
        try:
            nd = json.loads(notes_p.read_text()).get("notes", {})
            want_ids = {"hook", *scene_ids}
            missing = sorted(want_ids - set(nd))
            if missing:
                fails.append(f"P4 gate/notes.json does not cover {missing} (rule G2)")
        except (json.JSONDecodeError, AttributeError) as e:
            fails.append(f"P4 gate/notes.json unreadable: {e}")

    # ---- P5 banned vocabulary (S1 — same list as the linter) ----
    flat = " ".join(n for n, _ in lines).lower()
    for b in BANNED:
        if re.search(rf"\b{re.escape(b)}\b", flat):
            fails.append(f"P5 banned word/phrase in narration: '{b}' (rule S1)")

    # ---- P6 sfx table ----
    if "sfx" not in d:
        warns.append("P6 no per-short sfx table — legacy #0002 fallback will fire (write the table)")

    # ---- P7 scene count ----
    if len(d["scenes"]) < 10:
        warns.append(f"P7 only {len(d['scenes'])} scenes — rule S6 targets ≥12 visual events per ~35s")

    return fails, warns


def selftest() -> int:
    """L-066 control test: every check must FIRE on a known-bad fixture."""
    with tempfile.TemporaryDirectory() as td:
        base = Path(td) / "short-bad"
        (base / "render").mkdir(parents=True)
        (base / "gate").mkdir(parents=True)
        (base / "script.json").write_text(json.dumps({
            "title": "Test", "format": "short",
            "hook": {"narration": "Imagine a world where this fails.", "visual": {},
                     "fact_sources": []},
            "scenes": [
                {"narration": "One.", "visual": {"pose": "a", "prop": "b", "background": "c"},
                 "timestamp_start": 1.0, "fact_sources": []},
                {"narration": "Two.", "visual": {"pose": "a", "prop": "b", "background": "c"},
                 "timestamp_start": 2.0, "fact_sources": ["ok"]},
            ],
            "timeline": {"fps": 30, "total_s": 5, "gap_s": 0.25},
        }))
        (base / "render" / "scenes.html").write_text(
            "const EMPHASIS = { s0: ['a','b','c','d','e','f'] };\n"
            "function noRender() { return Math.random(); }")
        fails, warns = check_short("short-bad", root=Path(td))

        expect = [
            "P1",  # schema: hook.visual empty / fact_sources empty (x2)
            "P2",  # vo_lines.json missing
            "P3",  # 6 keywords > 5
            "P4",  # notes.json missing
            "P5",  # banned phrase 'imagine a world where'
            "P8",  # no renderFrame + Math.random
        ]
        missing = [tag for tag in expect if not any(f.startswith(tag) for f in fails)]
        print(f"control test: {len(fails)} expected failures fired")
        for f in fails:
            print(f"  FIRED: {f}")
        if missing:
            print(f"❌ SELFTEST FAIL — checks that did NOT fire on known-bad input: {missing}")
            return 1
        print("✅ selftest pass — every check catches its known-bad fixture (L-066)")
        return 0


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] == "--selftest":
        return selftest()
    slug = sys.argv[1]
    fails, warns = check_short(slug)
    for w in warns:
        print(f"  warn: {w}")
    if fails:
        for f in fails:
            print(f"  FAIL: {f}")
        print(f"❌ preflight {slug}: {len(fails)} fail(s) — fix before spending render budget")
        return 1
    print(f"✅ preflight {slug}: clear (warnings above, if any)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
