# Playbook — Publish (stage 7 of 7)

> Purpose: put the approved video live with disclosure, record it, and keep the
> paper trail.
> Inputs: `<slug>.mp4` (gate-approved ONLY — rule G1), title/description/tags
> per `docs/registry.md` content formulas.
> Outputs: live video, `content/<slug>/published.json`, ledger + log + push.

## Commands

```bash
python3 tools/youtube_upload.py --file content/<slug>/<slug>.mp4 \
  --title "…" --description "…" --tags "what if,stickman,science" --privacy public \
  --token-file ~/.secrets/token.json
# then record:
#   content/<slug>/published.json  (see short-0003's for the shape)
# then views land nightly via tools/views_tracker.py (48h freshness rule).
```

The upload sends `status.containsSyntheticMedia: true` automatically (rule P1 —
AI voice + AI visuals ⇒ disclose YES; verified accepted by the API on #0001).
OAuth mechanics: token JSON via env `YOUTUBE_TOKEN_JSON` (CI) or `--token-file`
(local, gitignored); auto-refresh on expiry. Full state: `docs/_archive/` +
the tool docstring; secrets map below.

## Secrets (GitHub Actions secrets on this repo)

| Secret | Contents |
|---|---|
| `FISH_AUDIO_KEY` | Fish Audio API key (daily free quota) |
| `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` | OAuth client (Google Cloud project nura-health; app published → refresh token long-lived) |
| `YOUTUBE_TOKEN_JSON` | Full token.json (access + refresh) |
| `YTA_PROXY` / `YTDLP_COOKIES` (optional) | bot-wall softeners for the research ladder |

Local twin lives OUTSIDE the repo (`~/.secrets/`, mirrored in `upload/` which
recycles never touch — L-058). Never commit token material.

## Known failure modes

| Symptom | Cause | Fix |
|---|---|---|
| upload 401 after a "verified" refresh | key mismatch (`access_token` vs `token`) — L-067 | the tool has the bridge line; if it recurs, verify END-TO-END with a real upload (rule P2) |
| `channels.list` 403 | upload-only scope — expected | channel identity via oEmbed + handle page; views via RSS (`views_tracker.py`) |
| thumbnails.set 403 | channel needs PHONE VERIFICATION | boss action item (open); until then YouTube auto-picks a frame |
| new-channel RSS 404s | CDN lag after first upload | oEmbed is the instant oracle (L-055) |

## Acceptance check

- oEmbed confirms title + channel minutes after upload.
- `published.json` written; ledger line + log + commit + push done (rule R3).
- Views row appears in `logs/views.csv` on the next nightly run.
