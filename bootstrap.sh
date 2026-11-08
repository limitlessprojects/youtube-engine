#!/usr/bin/env bash
# bootstrap.sh — zero-touch environment restoration for the studio.
#
# L-051: the sandbox is volatile (2 full wipes in 24h; pip packages vanish every
# recycle). This script is the ONE command a fresh session runs:
#
#     bash bootstrap.sh            # full local restore
#     bash bootstrap.sh --ci       # CI subset (no whisper, no POT server)
#     bash bootstrap.sh --whisper  # also install faster-whisper (~200MB)
#
# Idempotent: safe to run on every spawn. Everything is verified, not assumed.

set -uo pipefail
CI=0; WANT_WHISPER=0; START_POT=1
for arg in "$@"; do
  case "$arg" in
    --ci) CI=1; START_POT=0 ;;
    --whisper) WANT_WHISPER=1 ;;
  esac
done

ok()   { printf "  \033[32mok\033[0m  %s\n" "$1"; }
warn() { printf " warn %s\n" "$1"; }
fail() { printf "  \033[31mFAIL\033[0m %s\n" "$1"; }

echo "== bootstrap: studio environment =="

# --- 1. Python deps (fast path: check before installing) ---------------------
PY="python3"
$PY -c "import requests" 2>/dev/null && $PY -c "import yt_dlp" 2>/dev/null \
  && $PY -c "import youtube_transcript_api" 2>/dev/null \
  && ok "python deps present (requests, yt-dlp, youtube-transcript-api)" || {
  echo "  installing python deps..."
  $PY -m pip install -q -U requests yt-dlp youtube-transcript-api \
    && ok "python deps installed" || fail "python deps"
}

# bgutil POT plugin (yt-dlp provider plugin; server built separately)
$PY -c "import importlib.metadata as m; m.version('bgutil-ytdlp-pot-provider')" 2>/dev/null \
  && ok "bgutil pot plugin present" || {
  $PY -m pip install -q -U bgutil-ytdlp-pot-provider \
    && ok "bgutil pot plugin installed" || warn "bgutil pot plugin (non-fatal: captions ladder works without it)"
}

if [ "$WANT_WHISPER" = "1" ]; then
  $PY -c "import faster_whisper" 2>/dev/null && ok "faster-whisper present" || {
    $PY -m pip install -q faster-whisper && ok "faster-whisper installed" || fail "faster-whisper"
  }
fi

# --- 2. Git identity + secrets hygiene ---------------------------------------
if [ ! -d .git ]; then fail "not a git repo — run from the repo root"; exit 1; fi
git config user.name  >/dev/null 2>&1 || git config user.name "limitlessprojects"
git config user.email >/dev/null 2>&1 || git config user.email "limitlessprojects@users.noreply.github.com"
# The token lives one level above the repo (project .secrets/); mirror it locally.
if [ ! -f .secrets/gh_token ] && [ -f ../.secrets/gh_token ]; then
  mkdir -p .secrets && cp ../.secrets/gh_token .secrets/gh_token && chmod 600 .secrets/gh_token
fi
[ -f .secrets/gh_token ] && chmod 600 .secrets/gh_token 2>/dev/null && ok "git identity + token perms" \
  || warn ".secrets/gh_token missing — pushes will fail until restored"

# --- 3. Submodules (shallow, only what's missing) -----------------------------
if [ "${CI:-0}" = "0" ]; then
  MISSING=$($PY - <<'EOF'
import subprocess, configparser, os
cp = configparser.ConfigParser(); cp.read(".gitmodules")
missing = []
for s in cp.sections():
    path = cp[s]["path"]
    if not os.path.exists(path) or not os.listdir(path):
        missing.append(path)
print(" ".join(missing))
EOF
)
  if [ -n "$MISSING" ]; then
    echo "  initializing submodules: $MISSING"
    git submodule update --init --depth 1 $MISSING >/dev/null 2>&1 \
      && ok "submodules initialized" || warn "some submodules failed (non-fatal)"
  else
    ok "submodules present"
  fi
fi

# --- 3b. z-ai SDK (node_modules is not git-tracked; the ultracritic video
#     pass needs it — day-011: recycle wiped it and the pass went dark) ------
if [ -x "$(command -v node)" ]; then
  node -e "import('z-ai-web-dev-sdk').then(()=>1).catch(()=>process.exit(1))" 2>/dev/null \
    && ok "z-ai-web-dev-sdk present" || {
    (cd "$(dirname "$0")/.." && npm install --no-audit --no-fund z-ai-web-dev-sdk >/dev/null 2>&1) \
      && ok "z-ai-web-dev-sdk installed" || warn "z-ai SDK install failed (video pass will be dark)"
  }
fi

# --- 4. POT server (local sessions only; CI skips — runner IP is fresh) -------
if [ "$START_POT" = "1" ] && [ -x "$(command -v node)" ]; then
  if curl -sf --max-time 2 http://127.0.0.1:4416/ping >/dev/null 2>&1; then
    ok "POT server already running (4416)"
  elif [ -f vendor/bgutil-ytdlp-pot-provider/server/src/main.ts ]; then
    ( cd vendor/bgutil-ytdlp-pot-provider/server \
      && { [ -f build/main.js ] || { npm ci --silent >/dev/null 2>&1 && npx tsc >/dev/null 2>&1; }; } \
      && { nohup node build/main.js >/tmp/bgutil.log 2>&1 & } && sleep 3 )
    curl -sf --max-time 3 http://127.0.0.1:4416/ping >/dev/null 2>&1 \
      && ok "POT server started (4416)" || warn "POT server did not answer ping (non-fatal)"
  else
    warn "bgutil submodule missing — skipping POT server (non-fatal)"
  fi
elif [ "$CI" = "1" ]; then
  ok "CI mode: POT server skipped (runner IP is fresh each run)"
fi

# --- 5. Status ---------------------------------------------------------------
NODE_V=$(node --version 2>/dev/null || echo "absent")
echo "== bootstrap done | node: $NODE_V | yt-dlp: $($PY -m yt_dlp --version 2>/dev/null || echo absent) =="
exit 0
