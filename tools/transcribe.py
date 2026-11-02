#!/usr/bin/env python3
"""transcribe.py — the "youtubecheck": get a transcript for a YouTube video.

Paths, in order (see docs/architecture.md stage B, ledger L-031):
  1. youtube-transcript-api (captions; optional proxy via YTA_PROXY env)
  2. yt-dlp auto-subs (optional cookies via YTDLP_COOKIES_FILE env)
  3. local Whisper via faster-whisper on yt-dlp-fetched audio (best-effort)

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

    for raw in Path(path).read_text(encoding="utf-8", errors="ignore").splitlines():
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
    print("[t] yt-dlp:", " ".join(cmd[2:]))
    subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    vtt = sorted(OUT.glob(f"__tmp_{vid}*.vtt"))
    if not vtt:
        return None
    segs = _parse_vtt(vtt[0])
    vtt[0].unlink(missing_ok=True)
    return segs or None


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
    for name, fn in (("captions", via_transcript_api), ("ytdlp-subs", via_ytdlp), ("whisper", via_whisper)):
        try:
            segs = fn(vid)
        except Blocked as e:
            raise e
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
