#!/usr/bin/env python3
"""oauth_mint.py — re-consent flow for the YouTube OAuth Desktop client (L-084 fix).

The refresh grant dies silently (invalid_grant, L-084). This tool mints a fresh
token.json with a paste-back code flow that works from any headless sandbox:

  1. print the consent URL:
       python3 tools/oauth_mint.py --url
  2. boss opens it, authorizes, gets redirected to http://localhost/?code=...
     (the page itself will fail to load — EXPECTED; the code is in the address bar)
  3. boss copies the `code=...` value and runs:
       python3 tools/oauth_mint.py --code 4/0AX4...
  4. tool exchanges it, writes token.json to upload/ (durable mirror) +
     .secrets/ (working copy), then probes refresh health (exit 0 = live).

Never prints or commits secrets. Token files are gitignored/outside the repo.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

SECRETS_CLIENT = "/home/z/my-project/upload/client_secret.json"
TOKEN_MIRROR = "/home/z/my-project/upload/token.json"
TOKEN_WORKING = "/home/z/my-project/.secrets/token.json"
SCOPE = "https://www.googleapis.com/auth/youtube.upload"
REDIRECT = "http://localhost"  # registered Desktop-client loopback redirect
TOKEN_URI = "https://oauth2.googleapis.com/token"


def client() -> tuple[str, str]:
    c = json.load(open(SECRETS_CLIENT, encoding="utf-8"))
    c = c.get("installed", c)
    return c["client_id"], c["client_secret"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", action="store_true", help="print the consent URL")
    ap.add_argument("--code", default="", help="authorization code pasted back by the boss")
    a = ap.parse_args()
    if not a.url and not a.code:
        ap.error("need --url or --code")
    cid, csec = client()

    if a.url:
        q = urllib.parse.urlencode({
            "client_id": cid,
            "redirect_uri": REDIRECT,
            "response_type": "code",
            "scope": SCOPE,
            "access_type": "offline",   # force a refresh token
            "prompt": "consent",        # force a FRESH grant (old one is dead)
        })
        print("Open this URL in your browser, authorize, then paste back the code:")
        print()
        print(f"https://accounts.google.com/o/oauth2/v2/auth?{q}")
        print()
        print("After authorizing you land on http://localhost/?code=... (page won't load")
        print("— expected). Copy the code= value and run:")
        print("  python3 tools/oauth_mint.py --code 'PASTE_CODE_HERE'")
        return 0

    # exchange
    data = urllib.parse.urlencode({
        "code": a.code,
        "client_id": cid,
        "client_secret": csec,
        "redirect_uri": REDIRECT,
        "grant_type": "authorization_code",
    }).encode()
    r = urllib.request.Request(TOKEN_URI, data=data)
    with urllib.request.urlopen(r, timeout=60) as resp:
        out = json.load(resp)

    tok = {
        "token": out["access_token"],
        "access_token": out["access_token"],
        "refresh_token": out["refresh_token"],
        "token_uri": TOKEN_URI,
        "client_id": cid,
        "client_secret": csec,
        "scopes": [SCOPE],
        "universe_domain": "googleapis.com",
        "account": "",
        "expiry": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + out.get("expires_in", 3600))),
        "expires_in": out.get("expires_in", 3600),
        "scope": out.get("scope", SCOPE),
        "token_type": out.get("token_type", "Bearer"),
    }
    for path in (TOKEN_MIRROR, TOKEN_WORKING):
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(tok, indent=2), encoding="utf-8")
        p.chmod(0o600)
        print(f"[mint] saved token -> {p} (mode 600)")

    # health probe the minted grant immediately (L-067: full path, not function)
    data = urllib.parse.urlencode({
        "client_id": cid, "client_secret": csec,
        "refresh_token": out["refresh_token"], "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request(TOKEN_URI, data=data)
    with urllib.request.urlopen(req, timeout=60) as resp:
        json.load(resp)
    print("[mint] refresh grant: LIVE (probe OK)")
    print("[mint] NEXT: re-run any blocked upload work, e.g. #0002 --set-thumbnail")
    return 0


if __name__ == "__main__":
    sys.exit(main())
