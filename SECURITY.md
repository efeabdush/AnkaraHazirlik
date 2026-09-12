# Security

- Never commit `.env`, `ADMIN_SECRET`, or `GEMINI_API_KEY`.
- Never commit any provider key (`OPENROUTER_API_KEY`, `OPENCODE_API_KEY`, or `GEMINI_API_KEY`).
- Do not paste secrets in GitHub issues.
- The public site must not expose `/api/admin/*` without the admin header.
- If you find a vulnerability, open a private report rather than a public issue when possible.

## Production guards

- Passwordless admin access is a localhost convenience only. It is disabled automatically when `APP_ENV=production` or `RAILWAY_ENVIRONMENT` is present.
- Every public deployment must set a long random `ADMIN_SECRET`; never expose it as a `NEXT_PUBLIC_*` variable.

- API usage counters are persisted in the mounted database in production. Client addresses are hashed before storage.
- AI calls have per-client hourly limits, a global daily ceiling, and a concurrency ceiling. Transcription has separate ceilings.
- Cloudflare Turnstile is optional. Set both `TURNSTILE_SITE_KEY` and `TURNSTILE_SECRET_KEY` to enable it; expensive AI and transcription endpoints then require a short-lived, signed, IP-bound verification session.
- Set `TURNSTILE_SESSION_SECRET` and `RATE_LIMIT_HASH_SECRET` to separate long random values in Railway. Never expose either to the frontend.
- Keep `CORS_ORIGINS` and `TURNSTILE_ALLOWED_HOSTNAMES` restricted to the real frontend hostnames.
