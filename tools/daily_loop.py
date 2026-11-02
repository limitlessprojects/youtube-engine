#!/usr/bin/env python3
"""daily_loop.py — the deterministic daily learning loop (LLM-free, CI-safe).

Steps:
  1. pop first item off config/learning_queue.txt
  2. transcribe (tools/transcribe.py — captions -> yt-dlp subs -> mirrors ->
     whisper -> proxy-pool escalation)
  3. extract structural blueprint (tools/blueprint_extractor.py)
  4. append to logs/YYYY-MM-DD.md
  5. commit + push (queue line removed only on success)

Retry semantics (ledger L-031): if transcription is blocked (cloud-IP bot-wall —
expected on GitHub runners), the item STAYS in the queue, the log says so, and the
exit code is 0. CI stays green; the item is retried tomorrow or processed locally.

CI matrix mode (bot-wall ladder rung 3, L-039): set CI_TRANSCRIPTS_DIR and the
loop skips live transcription — it merges attempt artifacts produced by the
parallel matrix legs (each leg = a fresh GitHub-hosted runner IP + strategy):
direct -> proxy -> android priority, first success wins, blueprint + commit.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

import transcribe as TR  # noqa: E402
import blueprint_extractor as BP  # noqa: E402

QUEUE = REPO / "config" / "learning_queue.txt"


def queue_items() -> list[str]:
    lines = [l.strip() for l in QUEUE.read_text(encoding="utf-8").splitlines()]
    return [l for l in lines if l and not l.startswith("#")]


def pop_queue(item: str) -> None:
    lines = QUEUE.read_text(encoding="utf-8").splitlines()
    out = [l for l in lines if l.strip() != item]
    QUEUE.write_text("\n".join(out) + "\n", encoding="utf-8")


def git(*args: str) -> bool:
    r = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[git] {' '.join(args)} failed: {r.stderr.strip()[:300]}")
        return False
    return True


def commit_and_push(msg: str) -> None:
    if not git("add", "-A"):
        return
    if not git("commit", "-m", msg, "--allow-empty"):
        return
    if not git("push"):
        print("[loop] push failed — will retry next run (atomic-backup rule, L-023)")


def append_log(text: str) -> Path:
    today = dt.date.today().isoformat()
    logs = REPO / "logs"
    logs.mkdir(exist_ok=True)
    f = logs / f"{today}.md"
    header = (f"# Daily execution log — {today}\n\n" if not f.exists() else "")
    with f.open("a", encoding="utf-8") as fh:
        if header:
            fh.write(header)
        fh.write(text.rstrip() + "\n\n")
    return f


def _finish(vid: str, path: str, segs: list[dict], item: str, via: str) -> int:
    """Shared success tail: write transcript, blueprint, pop queue, log, commit."""
    TR.OUT.mkdir(parents=True, exist_ok=True)
    (TR.OUT / f"{vid}.json").write_text(
        json.dumps({"id": vid, "path": path, "segments": segs}, indent=1), encoding="utf-8")
    (TR.OUT / f"{vid}.txt").write_text("\n".join(s["text"] for s in segs) + "\n", encoding="utf-8")
    try:
        b = BP.extract(vid)
        BP.BP.mkdir(parents=True, exist_ok=True)
        (BP.BP / f"{vid}.json").write_text(json.dumps(b, indent=1), encoding="utf-8")
        (BP.BP / f"{vid}.md").write_text(BP.to_md(b), encoding="utf-8")
        summary = (f"- SUCCESS `{vid}` via {via}: {b['words']}w, {b['duration_s']}s, "
                   f"**{b['wpm']} WPM**, hook {b['hook_15s_words']}w/15s, "
                   f"opener {b['opener_sentence_words']}w, "
                   f"{len(b['open_loop_markers'])} loop markers. "
                   f"Blueprint: research/blueprints/{vid}.md")
    except Exception as e:
        summary = f"- WARN `{vid}` transcribed but blueprint failed: {type(e).__name__}: {e}"
        print(summary)
    pop_queue(item)
    append_log(summary)
    commit_and_push(f"chore(daily): blueprint {vid}")
    print("[loop] done")
    return 0


def merge_ci_artifacts(artifacts_dir: Path) -> int:
    """Matrix mode: collect attempt artifacts, first success (by priority) wins."""
    items = queue_items()
    if not items:
        append_log("- queue empty — scout new outliers (config/channels.json rule) and enqueue.")
        commit_and_push("chore(daily): queue empty note")
        print("[loop] queue empty")
        return 0
    item = items[0]
    vid = TR.video_id(item)
    print(f"[loop] merging CI attempts for {vid} ({len(items)} in queue)")
    for leg in ("direct", "proxy", "android"):   # priority order
        j = artifacts_dir / f"attempt-{leg}" / f"{vid}.json"
        if j.exists():
            data = json.loads(j.read_text(encoding="utf-8"))
            print(f"[loop] winner: attempt-{leg}")
            return _finish(vid, f"ci-{leg}", data.get("segments", []), item,
                           f"ci matrix leg {leg}")
    append_log(f"- RETRY: `{vid}` blocked across all matrix legs (direct/proxy/android). "
               "Item kept in queue; ladder rung 5 = wait for rotation / local session.")
    commit_and_push(f"chore(daily): blocked on {vid} — all CI legs")
    print("[loop] blocked on all legs — will retry")
    return 0


def main() -> int:
    ci_dir = os.environ.get("CI_TRANSCRIPTS_DIR", "").strip()
    if ci_dir:
        return merge_ci_artifacts(Path(ci_dir))

    items = queue_items()
    if not items:
        append_log("- queue empty — scout new outliers (config/channels.json rule) and enqueue.")
        commit_and_push("chore(daily): queue empty note")
        print("[loop] queue empty")
        return 0

    item = items[0]
    vid = TR.video_id(item)
    print(f"[loop] processing {vid} ({len(items)} in queue)")

    try:
        segs, path = TR.transcribe(vid)
    except TR.Blocked as e:
        append_log(f"- RETRY: `{vid}` blocked by YouTube ({e}). Item kept in queue. "
                   "Mitigations: PROXY_POOL=auto, YTDLP_COOKIES_FILE secret, or local session.")
        commit_and_push(f"chore(daily): blocked on {vid} — retry tomorrow")
        print("[loop] blocked (expected on cloud IPs) — will retry")
        return 0
    except Exception as e:
        append_log(f"- ERROR: `{vid}` hard failure: {type(e).__name__}: {e}. Item kept; inspect transcribe.py.")
        commit_and_push(f"chore(daily): error on {vid}")
        print(f"[loop] hard error: {e}", file=sys.stderr)
        return 0

    return _finish(vid, path, segs, item, path)


if __name__ == "__main__":
    sys.exit(main())
