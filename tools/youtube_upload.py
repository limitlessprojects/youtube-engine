#!/usr/bin/env python3
"""youtube_upload.py — publish a finished video via YouTube Data API v3 (requests only).

Usage:
  python tools/youtube_upload.py --file final.mp4 --title "..." --description "..." \
      --tags "what if,stickman,science" --privacy public

Credentials:
  - token JSON via env YOUTUBE_TOKEN_JSON (CI) or --token-file (local; gitignored!)
  - client id/secret: taken from the token JSON, overridable with
    GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET envs.

Operator checklist before upload (docs/youtube-oauth.md):
  [ ] "Altered or Synthetic Content" = YES in Studio after upload
  [ ] title/thumbnail pay off honestly
  [ ] cadence respected (Shorts daily, long-form 2x/week) — use Studio scheduling
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

TOKEN_URI = "https://oauth2.googleapis.com/token"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3/videos"
THUMB = "https://www.googleapis.com/upload/youtube/v3/thumbnails/set"


def load_token(a: argparse.Namespace) -> dict:
    raw = os.environ.get("YOUTUBE_TOKEN_JSON", "").strip()
    if a.token_file:
        raw = Path(a.token_file).read_text(encoding="utf-8")
    if not raw:
        sys.exit("no token: set YOUTUBE_TOKEN_JSON or pass --token-file")
    return json.loads(raw)


def refresh(tok: dict, client_id: str, client_secret: str) -> dict:
    import requests
    r = requests.post(TOKEN_URI, data={
        "client_id": client_id, "client_secret": client_secret,
        "refresh_token": tok["refresh_token"], "grant_type": "refresh_token",
    }, timeout=60)
    r.raise_for_status()
    out = dict(tok)
    out.update(r.json())
    # the refresh response calls it access_token; everything downstream
    # reads ["token"] — bridge it or we ship the STALE token (day-008 bug)
    out["token"] = out["access_token"]
    return out


def set_thumbnail(video_id: str, image: Path, tok_access: str) -> None:
    """Custom thumbnail (unlocked by phone verification, boss 2026-11-09).
    Idempotent: re-running just re-sets the same image."""
    import requests
    r = requests.post(
        f"{THUMB}?videoId={video_id}",
        headers={"Authorization": f"Bearer {tok_access}",
                 "Content-Type": "image/png"},
        data=image.read_bytes(), timeout=120)
    r.raise_for_status()
    print(f"[yt] thumbnail SET for {video_id} <- {image.name}")


def upload(file: Path, tok_access: str, meta: dict) -> str:
    import requests
    size = file.stat().st_size

    def _init(status_extra: dict):
        status = {"privacyStatus": meta["privacy"], "selfDeclaredMadeForKids": False}
        status.update(status_extra)
        return requests.post(
            f"{UPLOAD}?uploadType=resumable&part=snippet,status",
            headers={
                "Authorization": f"Bearer {tok_access}",
                "Content-Type": "application/json; charset=UTF-8",
                "X-Upload-Content-Length": str(size),
                "X-Upload-Content-Type": meta["contentType"],
            },
            json={"snippet": {
                "title": meta["title"], "description": meta["description"],
                "tags": meta["tags"], "categoryId": meta["categoryId"],
                "defaultLanguage": "en", "defaultAudioLanguage": "en",
            }, "status": status},
            timeout=120,
        )

    # Altered/synthetic media disclosure (studio policy: AI voice + AI visuals
    # => disclose YES, docs/youtube-oauth.md checklist). The API supports
    # status.containsSyntheticMedia; if a given API version rejects the field
    # we retry once without it and fall back to the manual Studio step.
    extra = {"containsSyntheticMedia": True} if meta.get("synthetic") else {}
    init = _init(extra)
    if init.status_code == 400 and extra:
        print("[yt] containsSyntheticMedia rejected — retrying without (manual Studio step needed)")
        init = _init({})
    init.raise_for_status()
    loc = init.headers.get("Location")
    if not loc:
        sys.exit(f"resumable init returned no Location header ({init.status_code})")
    print(f"[yt] init OK ({size} bytes) — uploading…")
    with file.open("rb") as f:
        put = requests.put(loc, data=f, headers={"Content-Type": meta["contentType"]}, timeout=3600)
    put.raise_for_status()
    vid = put.json().get("id", "?")
    return vid


def main() -> int:
    ap = argparse.ArgumentParser()
    _no_upload = ("--set-thumbnail" in sys.argv) or ("--check-token" in sys.argv)
    ap.add_argument("--file", required=not _no_upload)
    ap.add_argument("--title", required=not _no_upload)
    ap.add_argument("--description", required=False, default="")
    ap.add_argument("--set-thumbnail", default="", metavar="VIDEO_ID:IMAGE",
                    help="skip upload; set a custom thumbnail (phone-verified capability)")
    ap.add_argument("--tags", default="")
    ap.add_argument("--privacy", default="public", choices=["public", "unlisted", "private"])
    ap.add_argument("--category", default="27", help="27=Education, 24=Entertainment, 28=Sci/Tech")
    ap.add_argument("--token-file")
    ap.add_argument("--content-type", default="video/mp4")
    ap.add_argument("--check-token", action="store_true",
                    help="probe refresh grant health; exit 0 = healthy (L-084: "
                         "verify BEFORE the publish moment, grants die silently)")
    ap.add_argument("--id-file", default="",
                    help="write the uploaded video id to this file (CI publish path)")
    ap.add_argument("--no-synthetic", action="store_true",
                    help="skip the altered/synthetic disclosure (default: disclose YES per studio policy)")
    a = ap.parse_args()

    file = Path(a.file) if a.file else None
    if file is not None and not file.exists():
        sys.exit(f"missing video file: {file}")
    import requests  # noqa: F401  (fail fast if requests missing)

    tok = load_token(a)
    client_id = os.environ.get("GOOGLE_CLIENT_ID", tok.get("client_id", ""))
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", tok.get("client_secret", ""))
    if not a.check_token:
        # (with --check-token the probe below does the refresh and reports health)
        if tok.get("refresh_token") and client_id and client_secret:
            print("[yt] refreshing access token…")
            tok = refresh(tok, client_id, client_secret)
        elif not tok.get("token"):
            sys.exit("token JSON has neither a usable access token nor refresh credentials")

    # token health probe (L-084): refresh dies silently — test it cheaply
    if a.check_token:
        try:
            refresh(tok, client_id, client_secret)
            print("[yt] token health: OK (refresh grant live)")
            return 0
        except Exception as e:  # noqa: BLE001
            body = getattr(getattr(e, "response", None), "text", "")
            reason = ""
            try:
                reason = json.loads(body).get("error", "")
            except Exception:  # noqa: BLE001
                pass
            print(f"[yt] token health: DEAD ({reason or e}) — re-run OAuth consent, mint a fresh token.json")
            return 1

    # thumbnail-only mode (boss 2026-11-09: #0002's 7.5/10 hook frame waiting)
    if a.set_thumbnail:
        vid, _, img = a.set_thumbnail.partition(":")
        img_p = Path(img)
        if not vid or not img_p.exists():
            sys.exit("--set-thumbnail expects VIDEO_ID:PATH_TO_IMAGE (image must exist)")
        set_thumbnail(vid, img_p, tok["token"])
        return 0

    vid = upload(file, tok["token"], {
        "title": a.title, "description": a.description,
        "tags": [t.strip() for t in a.tags.split(",") if t.strip()],
        "privacy": a.privacy, "categoryId": a.category, "contentType": a.content_type,
        "synthetic": not a.no_synthetic,
    })
    if a.id_file:
        Path(a.id_file).write_text(vid + "\n", encoding="utf-8")
    print(f"[yt] UPLOADED: https://youtu.be/{vid}")
    if not a.no_synthetic:
        print("[yt] altered/synthetic disclosure: set via API (containsSyntheticMedia=true)")
    else:
        print("[yt] NOW IN STUDIO: mark 'Altered or Synthetic Content' = YES")
    print("[yt] NEXT: record the video id in content/<slug>/published.json + today's ledger")
    return 0


if __name__ == "__main__":
    sys.exit(main())
