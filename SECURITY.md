# Security

## Secrets

- Never commit `.env`, a local database, provider credentials, private keys, or deployment exports.
- Keep `OPENROUTER_API_KEY`, `OPENCODE_API_KEY`, `GEMINI_API_KEY`, `RESEND_API_KEY`, `ADMIN_SECRET`, and Turnstile secrets on the backend only.
- Never expose a secret through a `NEXT_PUBLIC_*` variable, screenshot, issue, discussion, or log.
- Run `python scripts/check_secrets.py` before pushing. CI runs the same check automatically.
- If a credential was ever pasted into a chat, issue, log, or commit, revoke it at the provider and create a new one. Removing the text alone does not make the old credential safe.

`.env`, `backend/storage/`, databases, logs, certificates, and common deployment-state folders are ignored by Git. `.env.example` contains names and safe defaults only.

Keys entered in the local admin panel are stored in the ignored local SQLite database. They are not encrypted at rest, so do not copy or publish `backend/storage/`. Delete a key from the panel or remove the local database before giving that runtime folder to somebody else.

## Production guards

- Passwordless admin access is disabled by default in code. Copying `.env.example` opts into it for localhost development only; production mode disables it automatically.
- Every public deployment must set a long random `ADMIN_SECRET`; never expose it as a `NEXT_PUBLIC_*` variable.
- API usage counters are persisted in the mounted database in production. Client addresses are hashed before storage.
- AI calls have per-client hourly limits, a global daily ceiling, and a concurrency ceiling. Transcription has separate ceilings.
- Cloudflare Turnstile is optional. Set both `TURNSTILE_SITE_KEY` and `TURNSTILE_SECRET_KEY` to enable it; expensive AI and transcription endpoints then require a short-lived, signed, IP-bound verification session.
- Set `TURNSTILE_SESSION_SECRET` and `RATE_LIMIT_HASH_SECRET` to separate long random values in Railway. Never expose either to the frontend.
- Keep `CORS_ORIGINS` and `TURNSTILE_ALLOWED_HOSTNAMES` restricted to the real frontend hostnames.
