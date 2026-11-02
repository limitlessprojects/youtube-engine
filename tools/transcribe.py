#!/usr/bin/env python3
"""transcribe.py — the "youtubecheck": get a transcript for a YouTube video.

Paths, in order (see docs/architecture.md stage B, ledger L-031):
  1. youtube-transcript-api (captions; optional proxy via YTA_PROXY env)
  2. yt-dlp auto-subs (cookies via YTDLP_COOKIES_FILE; client via YTDLP_PLAYER_CLIENT)
  3. Invidious mirror captions (mirror's IP talks to YouTube, ours talks to the mirror)
  4. Piped API subtitles (same mirror principle)
  5. local Whisper via faster-whisper on yt-dlp-fetched audio (best-effort)

Day-002 hardening: 3 -> 5 independent paths. The bot-wall (L-031) only sees our
IP on paths 1-2; paths 3-4 outsource the risky request to community mirrors
(17 instances in the default pools — instance health varies by time and by
requester, so breadth + the daily retry is the design, see ledger L-037).

Output: research/transcripts/<id>.json  (segments: start, duration, text)
        research/transcripts/<id>.txt   (plain text, one segment per line)

Exit codes: 0 = success, 3 = blocked/retryable (cloud-IP bot-wall), 1 = hard error.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "research" / "transcripts"
YT_ID = re.compile(r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})")


def video_id(url_or_id: str) -> str:
    m = YT_ID.search(url_or_id.strip())
    return m.group(1) if m else url_or_id.strip()


def via_transcript_api(vid: str) -> list[dict] | None:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        print("[t] youtube-transcript-api not installed", file=sys.stderr)
        return None
    proxy_config = None
    proxy = os.environ.get("YTA_PROXY", "").strip()
    if proxy:
        try:
            from youtube_transcript_api.proxies import GenericProxyConfig
        except ImportError:  # older versions re-export at top level
            from youtube_transcript_api import GenericProxyConfig  # type: ignore
        proxy_config = GenericProxyConfig(http_url=proxy, https_url=proxy)
        print(f"[t] using proxy {proxy}")
    api = YouTubeTranscriptApi(proxy_config=proxy_config) if proxy_config else YouTubeTranscriptApi()
    try:
        fetched = api.fetch(vid, languages=["en", "en-US", "en-GB"])
    except Exception as first_err:
        # fall back to any available language, then translate to English
        try:
            listing = api.list(vid)
            tr = next(iter(listing))
            try:
                fetched = tr.translate("en").fetch()
            except Exception:
                fetched = tr.fetch()
        except Exception as e:
            name = type(e).__name__
            print(f"[t] captions unavailable: {name}: {e}", file=sys.stderr)
            if any(k in name.lower() for k in ("ipblocked", "requestblocked", "blocked")):
                raise Blocked(f"captions blocked: {e}") from e
            return None
        else:
            _ = first_err
    return [
        {"start": round(s.start, 3), "duration": round(s.duration, 3), "text": s.text.replace("\n", " ").strip()}
        for s in fetched.snippets
    ]


def _parse_vtt(path: Path) -> list[dict]:
    return _parse_vtt_text(Path(path).read_text(encoding="utf-8", errors="ignore"))


def _parse_vtt_text(text: str) -> list[dict]:
    segs: list[dict] = []
    start = end = None

    def ts(v: str) -> float:
        parts = v.strip().replace(",", ".").split(":")
        sec = float(parts[-1])
        if len(parts) > 1:
            sec += int(parts[-2]) * 60
        if len(parts) > 2:
            sec += int(parts[-3]) * 3600
        return sec

    for raw in text.splitlines():
        if "-->" in raw:
            a, b = raw.split("-->")
            start, end = ts(a), ts(b.split()[0])
            continue
        line = raw.strip()
        if not line or line == "WEBVTT" or re.match(r"^\d+$", line) or start is None:
            continue
        line = re.sub(r"<[^>]+>", "", line)
        if not line:
            continue
        if segs and segs[-1]["text"] == line:
            segs[-1]["duration"] = round(end - segs[-1]["start"], 3)
            continue
        segs.append({"start": round(start, 3), "duration": round((end or start) - start, 3), "text": line})
    return segs


def via_ytdlp(vid: str) -> list[dict] | None:
    url = f"https://www.youtube.com/watch?v={vid}"
    OUT.mkdir(parents=True, exist_ok=True)
    tmpl = str(OUT / f"__tmp_{vid}")
    cmd = [sys.executable, "-m", "yt_dlp", "--skip-download", "--write-auto-subs", "--write-subs",
           "--sub-langs", "en.*,en", "--sub-format", "vtt/srt", "-o", tmpl, url]
    cookies = os.environ.get("YTDLP_COOKIES_FILE", "").strip()
    if cookies and Path(cookies).exists():
        cmd += ["--cookies", cookies]
    jsr = os.environ.get("YTDLP_JS_RUNTIME", "").strip()
    if jsr:
        cmd += ["--js-runtimes", jsr]
    pc = os.environ.get("YTDLP_PLAYER_CLIENT", "").strip()
    if pc:
        cmd += ["--extractor-args", f"youtube:player_client={pc}"]
    print("[t] yt-dlp:", " ".join(cmd[2:]))
    subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    vtt = sorted(OUT.glob(f"__tmp_{vid}*.vtt"))
    if not vtt:
        return None
    segs = _parse_vtt(vtt[0])
    vtt[0].unlink(missing_ok=True)
    return segs or None


# --- caption mirrors: outsource the risky request, keep our IP clean (L-031 fix) ---

INVIDIOUS_INSTANCES_DEFAULT = [
    "https://inv.nadeko.net",
    "https://invidious.nerdvpn.de",
    "https://yewtu.be",
    "https://iv.ggtyler.dev",
    "https://invidious.privacyredirect.com",
    "https://invidious.f5.si",
    "https://invidious.jing.rocks",
    "https://iv.melmac.space",
    "https://invidious.materialio.us",
    "https://inv.tux.pizza",
]
PIPED_INSTANCES_DEFAULT = [
    "https://pipedapi.kavin.rocks",
    "https://pipedapi.adminforge.de",
    "https://api.piped.private.coffee",
    "https://pipedapi.reallyaweso.me",
    "https://pipedapi.ducks.party",
    "https://pipedapi.leptons.xyz",
    "https://pipedapi.orangenet.cc",
]
_UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) youtube-engine/0.2"}


def _instances(env_key: str, defaults: list[str]) -> list[str]:
    raw = os.environ.get(env_key, "").strip()
    return [x.strip().rstrip("/") for x in raw.split(",") if x.strip()] or defaults


def _fetch_vtt_text(url: str) -> list[dict] | None:
    r = requests.get(url, timeout=15, headers=_UA)
    if r.status_code != 200 or "-->" not in r.text:
        return None
    return _parse_vtt_text(r.text) or None


def via_invidious(vid: str) -> list[dict] | None:
    for base in _instances("INVIDIOUS_INSTANCES", INVIDIOUS_INSTANCES_DEFAULT):
        try:
            r = requests.get(f"{base}/api/v1/captions/{vid}", timeout=10, headers=_UA)
            if r.status_code != 200:
                continue
            caps = (r.json() or {}).get("captions") or []
            pick = next((c for c in caps if str(c.get("languageCode", "")).startswith("en")),
                        caps[0] if caps else None)
            if not pick or not pick.get("url"):
                continue
            url = pick["url"]
            if url.startswith("/"):
                url = base + url
            segs = _fetch_vtt_text(url)
            if segs:
                print(f"[t] mirror hit: {base}")
                return segs
        except Exception as e:
            print(f"[t] invidious {base}: {type(e).__name__}", file=sys.stderr)
    return None


def via_piped(vid: str) -> list[dict] | None:
    for base in _instances("PIPED_INSTANCES", PIPED_INSTANCES_DEFAULT):
        try:
            r = requests.get(f"{base}/streams/{vid}", timeout=10, headers=_UA)
            if r.status_code != 200:
                continue
            subs = (r.json() or {}).get("subtitles") or []
            pick = next((s for s in subs if str(s.get("code", "")).startswith("en")),
                        subs[0] if subs else None)
            if not pick or not pick.get("url"):
                continue
            segs = _fetch_vtt_text(pick["url"])
            if segs:
                print(f"[t] mirror hit: {base}")
                return segs
        except Exception as e:
            print(f"[t] piped {base}: {type(e).__name__}", file=sys.stderr)
    return None


def via_whisper(vid: str) -> list[dict] | None:
    """Best-effort local Whisper on yt-dlp-fetched audio (needs faster-whisper)."""
    try:
        from faster_whisper import WhisperModel  # noqa: F401
    except ImportError:
        print("[t] faster-whisper not installed; vendored Youtube_transcriber path skipped "
              "(install locally: pip install faster-whisper, or use vendor/Youtube_transcriber app)", file=sys.stderr)
        return None
    url = f"https://www.youtube.com/watch?v={vid}"
    tmpl = str(OUT / f"__audio_{vid}.%(ext)s")
    cmd = [sys.executable, "-m", "yt_dlp", "-x", "--audio-format", "m4a", "-o", tmpl, url]
    subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    audio = next(iter(OUT.glob(f"__audio_{vid}*.m4a")), None)
    if not audio:
        return None
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _info = model.transcribe(str(audio), vad_filter=True)
    out = [{"start": round(s.start, 3), "duration": round(s.end - s.start, 3), "text": s.text.strip()}
           for s in segments]
    audio.unlink(missing_ok=True)
    return out or None


class Blocked(Exception):
    pass


def transcribe(vid: str) -> tuple[list[dict], str]:
    errors: list[str] = []
    for name, fn in (("captions", via_transcript_api), ("ytdlp-subs", via_ytdlp),
                     ("invidious-mirror", via_invidious), ("piped-mirror", via_piped),
                     ("whisper", via_whisper)):
        try:
            segs = fn(vid)
        except Blocked as e:
            # a block on one path (e.g. our IP) does NOT mean the mirrors are
            # blocked — fall through and let them try (Day-002 fix)
            errors.append(f"{name}: BLOCKED ({str(e)[:140]})")
            continue
        except Exception as e:
            errors.append(f"{name}: {type(e).__name__}: {e}")
            continue
        if segs:
            print(f"[t] OK via {name}: {len(segs)} segments")
            return segs, name
        errors.append(f"{name}: no segments")
    raise Blocked("all paths failed -> " + "; ".join(errors))


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: transcribe.py <video-url-or-id> [--force]", file=sys.stderr)
        return 1
    vid = video_id(sys.argv[1])
    out_json = OUT / f"{vid}.json"
    out_txt = OUT / f"{vid}.txt"
    if out_json.exists() and "--force" not in sys.argv:
        print(f"[t] already transcribed: {out_json}")
        return 0
    try:
        segs, path = transcribe(vid)
    except Blocked as e:
        print(f"[t] RETRYABLE (blocked): {e}", file=sys.stderr)
        return 3
    OUT.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps({"id": vid, "path": path, "segments": segs}, indent=1), encoding="utf-8")
    out_txt.write_text("\n".join(s["text"] for s in segs) + "\n", encoding="utf-8")
    words = sum(len(s["text"].split()) for s in segs)
    print(f"[t] wrote {out_json.name} ({len(segs)} segs, {words} words)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
