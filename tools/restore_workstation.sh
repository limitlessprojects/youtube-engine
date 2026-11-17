#!/usr/bin/env bash
# restore_workstation.sh — one-command recovery after a sandbox recycle.
#
# Usage:
#   bash scripts/restore_workstation.sh <gh_token>     # mint a new PAT, pass it here
#   bash scripts/restore_workstation.sh --from-upload  # recover from the durable mirror
#
# DURABILITY RULE (day 007, L-058): the GitHub token ALWAYS lives in TWO places:
#   .secrets/gh_token   — working copy (used by git)
#   upload/gh_token     — durable mirror (the ONLY dir recycles never touch;
#                         survived all 4 wipes while .secrets/ died twice)
#
# L-122 (day 019): restoring the repo is NOT restoring the auth. This script must
# wire EVERY credential surface the toolchain touches:
#   - origin URL stays CLEAN (no embedded PAT — AGENTS.md §4; URLs surface in errors/logs)
#   - git credential store rebuilt from the mirror (~/.config/opencode/.secrets/git-credentials)
#   - gh_api.py reads the helper at call time; whoami probe proves it (never prints the token)
# Versioned copy: tools/restore_workstation.sh in the repo (this file is the durable one).
set -euo pipefail
ROOT=/home/z/my-project
REPO=$ROOT/youtube-engine
CRED_DIR=/home/z/.config/opencode/.secrets

TOK_SRC=""
case "${1:-}" in
  --from-upload)
    [ -f "$ROOT/upload/gh_token" ] || { echo "FATAL: upload/gh_token mirror missing"; exit 1; }
    TOK_SRC="$ROOT/upload/gh_token" ;;
  "")
    if [ -f "$ROOT/upload/gh_token" ]; then
      TOK_SRC="$ROOT/upload/gh_token"
    else
      echo "FATAL: no GitHub token anywhere."
      echo "Fix: mint a fine-grained PAT (github.com -> Settings -> Developer settings ->"
      echo "Personal access tokens -> Fine-grained; repo: limitlessprojects/youtube-engine;"
      echo "Contents: Read and write; Actions: Read) then: bash scripts/restore_workstation.sh <token>"
      exit 1
    fi ;;
  *)
    printf '%s' "$1" > "$ROOT/upload/gh_token"; chmod 600 "$ROOT/upload/gh_token"
    TOK_SRC="$ROOT/upload/gh_token" ;;
esac

mkdir -p "$ROOT/.secrets"
install -m 600 "$TOK_SRC" "$ROOT/.secrets/gh_token"
chmod 600 "$ROOT/upload/gh_token"

# L-122: wire git's credential store BEFORE any git network call, from the mirror.
mkdir -p "$CRED_DIR"
printf 'https://x-access-token:%s@github.com\n' "$(cat "$TOK_SRC")" > "$CRED_DIR/git-credentials"
chmod 600 "$CRED_DIR/git-credentials"
git config --global credential.helper "store --file=$CRED_DIR/git-credentials"

if [ ! -d "$REPO/.git" ]; then
  git clone -q "https://github.com/limitlessprojects/youtube-engine.git" "$REPO"
fi
cd "$REPO"
# L-122: a recycled clone can carry an embedded token in origin — clean it unconditionally.
case "$(git remote get-url origin)" in
  *x-access-token*|*@github.com*) git remote set-url origin https://github.com/limitlessprojects/youtube-engine.git ;;
esac
git pull --rebase -q || true
git submodule update --init --quiet
[ -f bootstrap.sh ] && bash bootstrap.sh || true

# L-122/L-117: prove the auth surface actually works (never prints the token).
python3 tools/gh_api.py whoami || echo "WARN: gh_api whoami failed — check the credential store"
echo "workstation restored: $REPO @ $(git log --oneline -1)"
