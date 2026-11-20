#!/usr/bin/env bash
# gate_0012_retry.sh — one-shot: probe judge; alive -> ultracritic r2 on #0012.
# Dead -> exit 2 (carry stays open). Publish step is MANUAL-by-runbook:
# the verdict tree in content/short-0012/carry_0012_gate.md governs.
set -u
cd "$(dirname "$0")/.."

HOOK=content/short-0012/gate/hook_u50.png
[ -f "$HOOK" ] || { echo "keyframes missing — run: python3 tools/render_short.py short-0012 --keyframes"; exit 3; }

echo "== judge probe =="
REPLY=$(node /home/z/my-project/scripts/probe_judge.mjs "$HOOK" 2>/dev/null | rg '^MODEL=' | head -1 || true)
if [ -z "$REPLY" ]; then
  echo "JUDGE DEAD (429/no verdict) — leave carry open, do NOT publish."
  exit 2
fi
echo "JUDGE ALIVE ($REPLY) — running gate r2 (video pass auto-wired):"
python3 tools/ultracritic.py short-0012 --round 2
echo "== verdict tree: content/short-0012/carry_0012_gate.md step 3 =="
