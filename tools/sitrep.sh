#!/usr/bin/env bash
# sitrep.sh — ONE call, ONE payload: full workstation situation report.
# Rationale (L-083 resilience protocol): collect all state in a single tool
# call instead of many small reads; resilient to bursty toolcall failures.
# Usage: bash tools/sitrep.sh   (from repo root or anywhere)
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

sec() { printf '\n===== %s =====\n' "$1"; }

sec "GIT log (12)"
git log --oneline -12 2>/dev/null || echo "(git log failed)"
echo "--- status ---"
git status --short --branch 2>/dev/null || echo "(dirty/unknown)"

sec "TOP-LEVEL"
ls -1 2>/dev/null || true
echo "--- docs/ (depth 2) ---"
find docs -maxdepth 2 -type d 2>/dev/null | sort || echo "(no docs/)"
echo "--- consolidation dirs present? ---"
for d in docs/playbook rules parameters dead-ends _archive skills tools; do
  [ -d "$d" ] && echo "OK  $d/ ($(ls -1 "$d" | wc -l) entries)" || echo "MISSING  $d/"
done

sec "LEDGER tail (40)"
[ -f LEDGER.md ] && tail -40 LEDGER.md || echo "(LEDGER.md missing)"

sec "lessons/ (last 12)"
ls -1 lessons/ 2>/dev/null | tail -12 || echo "(no lessons/)"
sec "logs/ (last 12)"
ls -1 logs/ 2>/dev/null | tail -12 || echo "(no logs/)"

sec "CARRY DEBT FILES"
CARRY=$(git ls-files 2>/dev/null | grep -i 'carry' | head -3)
for f in $CARRY; do echo "--- $f ---"; head -120 "$f" 2>/dev/null; done
[ -z "$CARRY" ] && echo "(none tracked)"

sec "VLM GATE rubric (hook_impact / frame0 / signoff)"
GATE="tools/vlm_gate.py"
if [ -f "$GATE" ]; then
  echo "gate file: $GATE ($(wc -l < "$GATE") lines)"
  grep -n -i -E 'hook_impact|frame.?0|frame_0|sign.?off|SIGNOFF|approval|SIGN_OFF' "$GATE" | head -40 || echo "(no matches)"
else
  echo "(vlm_gate.py missing)"
fi

sec "published.json"
[ -f published.json ] && cat published.json || echo "(missing at root)"
[ -f content/short-0004/published.json ] && echo "(0004 HAS published.json!)" || true

sec "QUEUE / INSTANCES"
git ls-files | grep -i -E 'fetch_instances|queue' | head -5 || true
ls -1 runs/ 2>/dev/null | tail -8 || echo "(no runs/)"
ls -1 state/ 2>/dev/null | tail -8 || true
find . -maxdepth 2 -name 'instances*.json' -not -path './.git/*' 2>/dev/null | head -5 || true

sec "VIEWS (latest)"
ls -1t logs/ 2>/dev/null | head -3 || true
V=$(ls -1t logs/ 2>/dev/null | grep -i -E 'view|rss' | head -1)
[ -n "${V:-}" ] && { echo "--- logs/$V (tail 12) ---"; tail -12 "logs/$V"; } || echo "(no views log found)"
[ -f logs/views.csv ] && { echo "--- logs/views.csv (tail 8) ---"; tail -8 logs/views.csv; } || true

sec "30-DAY PLAN (tail 25)"
[ -f docs/30-day-plan.md ] && tail -25 docs/30-day-plan.md || echo "(missing)"
[ -f docs/playbook/30-day-plan.md ] && tail -25 docs/playbook/30-day-plan.md || true

sec "TODAY LOG (2026-11-12)"
[ -f logs/2026-11-12.md ] && cat logs/2026-11-12.md || echo "(no log yet today)"

sec "ACTIONS (recent workflow runs)"
if [ -f /home/z/my-project/.secrets/gh_token ]; then
  TOK=$(cat /home/z/my-project/.secrets/gh_token)
  curl -s -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer $TOK" \
    "https://api.github.com/repos/limitlessprojects/youtube-engine/actions/runs?per_page=3" \
    | python3 -c 'import json,sys
try:
    d=json.load(sys.stdin)
    for r in d.get("workflow_runs",[])[:3]:
        print(f"{r[\"name\"]} | {r[\"status\"]}/{r.get(\"conclusion\")} | {r[\"created_at\"]}")
except Exception as e:
    print("(actions parse fail:", e, ")")' 2>/dev/null || echo "(actions fetch failed)"
else
  echo "(no token; skip)"
fi
printf '\n===== SITREP END =====\n'
