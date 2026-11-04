# YouTube OAuth — setup state & how we publish

## Current state (2026-11-04)

- **FIRST UPLOAD SHIPPED**: Short #0001 → https://youtu.be/KKyrNUGZXcU
  (channel **Jack Blessed** @JackBlessed-u5x, id `UCo_p5nBuNe9KW_W_x90Nitg`,
  public, category 27, synthetic disclosure set via API — see below).
- Google Cloud project: **nura-health**
- OAuth client: **Desktop/installed** type, created 2026-11-02
  - Client ID: `370258738776-m1e1kfv35cg27dl39cg2vbephbg0nof6.apps.googleusercontent.com`
    (client ID is not a secret; the secret is never written here)
- Consent screen: **Testing mode** — only registered test users can authorize.
  ⚠️ The YouTube channel account must be added as a test user on the OAuth consent
  screen, or refresh will fail with `access_denied`.
- Scope granted: `https://www.googleapis.com/auth/youtube.upload` (upload only —
  channel READ calls (channels.list mine=true) return 403 insufficientPermissions;
  public monitoring goes through RSS + oEmbed instead, see L-053).
- `token.json` contains an access token + **refresh token**; it lives ONLY in:
  - local sandbox secrets dir (gitignored path, outside any repo)
  - GitHub Actions secret `YOUTUBE_TOKEN_JSON` (encrypted at rest by GitHub)

## ⏰ Time bomb (boss action needed)

Testing-mode OAuth apps issue refresh tokens that **expire after 7 days**
(Google policy). Our token was authorized 2026-11-02 → likely dies ~2026-11-09.
Fix (Google Cloud Console, nura-health project, needs the boss): OAuth consent
screen → **Publish app** (production status). youtube.upload is a sensitive
scope; verification may take days — until then, expect a re-auth every 7 days,
or upload via CI within each 7-day window.

## Secrets map (GitHub Actions secrets on this repo)

| Secret | Contents |
|---|---|
| `FISH_AUDIO_KEY` | Fish Audio API key (s2.1-pro-free; daily free quota) |
| `GOOGLE_CLIENT_ID` | OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | OAuth client secret |
| `YOUTUBE_TOKEN_JSON` | Full token.json (access + refresh + expiry) |

Optional, to defeat YouTube's cloud-IP bot-wall (L-031):

| Secret | Effect |
|---|---|
| `YTA_PROXY` | `http://user:pass@host:port` — used by youtube-transcript-api |
| `YTDLP_COOKIES_FILE` | Path is materialized from secret `YTDLP_COOKIES` at runtime |

## How upload works (tools/youtube_upload.py)

1. Load `YOUTUBE_TOKEN_JSON` (env in CI, `--token-file` locally).
2. If expired → POST refresh to `oauth2.googleapis.com/token` with client ID/secret.
3. Resumable upload to `youtube/v3/videos` with `snippet` + `status`
   (`privacyStatus`, `selfDeclaredMadeForKids: false`).
4. **Altered/Synthetic disclosure is now automated**: `youtube_upload.py` sends
   `status.containsSyntheticMedia: true` on every upload (studio policy: AI
   voice + AI visuals ⇒ disclose YES). Verified accepted by the API on
   2026-11-04 (Short #0001, first try — no 400, no fallback needed).
   **Operator checklist at upload time (what remains):**
   - Confirm title/thumbnail pay off honestly (no CTR bait we can't cash).
   - Schedule via Studio queue per cadence: Shorts daily, long-form 2×/week.

## Token hygiene rules

- Never commit `token.json` / `client_secret.json` (gitignored; L-032 is why).
- Never paste token contents into logs, prompts, or the ledger — reference the secret
  name instead.
- If a token leaks: revoke at https://myaccount.google.com/permissions and re-issue.
- Refresh tokens for desktop clients don't expire on use (only on revocation /
  6-month dormancy) — the CI refresh flow is safe to run daily.
