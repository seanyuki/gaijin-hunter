# Launch-readiness & production-hardening report — June 11, 2026

## 1. Production-readiness issues found

Severity-ordered, all confirmed before fixing:

1. **`app.run(debug=True)` hardcoded** — the Werkzeug debugger (remote code
   execution via debugger PIN) would have shipped to production.
2. **Broken OG image** — every page's `og:image` / `twitter:image` pointed to
   `/static/og-default.png`, which did not exist (only the .svg did). Social
   shares would have shown no card image.
3. **No SECRET_KEY** — Flask app had no secret key configured at all.
4. **Gunicorn would serve an uninitialized schema** — `db.init_db()` only ran
   under `__main__`; under gunicorn a fresh deploy would 500.
5. **Absolute URLs tied to the request host** — sitemap/canonical/OG/JSON-LD
   used `request.url_root` (76 occurrences across app + 22 templates), which
   behind a proxy/CDN yields wrong or mixed origins.
6. **No /healthz, no 404/500 pages, no gunicorn/Procfile**, no env-var config,
   no deployment docs.
7. **Index bloat risk** — /tracker, /profile, /data, /compare, /saved-applied
   views, unsubscribe and error pages were all indexable.
8. **`pytest -q` unusable** (collection recursion on this filesystem) and the
   test suite's `check()` didn't assert, so pytest would have trivially passed.
9. `/jobs` spent ~200ms running 10 separate GROUP BY count queries per view.

## 2. Files changed

New: `config.py`, `Procfile`, `runtime.txt`, `.env.example`, `render.yaml`,
`pytest.ini`, `templates/error.html`, `templates/privacy.html`,
`static/og-default.png` (rendered 1200×630 from the existing SVG),
`DEPLOYMENT.md`, `SEO_CHECKLIST.md`, this report.
Modified: `app.py` (config, healthz, error handlers, /privacy, base_url
everywhere, bulk counts, sitemap), `db.py` (`counts_bulk`), `update.py`
(zero-jobs warnings), `requirements.txt` (+gunicorn), `test_app.py` (real
assertions + runner), `templates/base.html` (footer trust links, base_url),
21 other templates (base_url in JSON-LD, noindex on user pages, job meta
description), `README.md`, `MAINTENANCE.md` (runbooks).

## 3. Deployment method supported

**Gunicorn** as the generic target (`Procfile`, documented command) plus a
**Render.com blueprint** (`render.yaml`: health-checked web service, generated
SECRET_KEY, 1 GB persistent disk at /data for SQLite). `python app.py` is
unchanged for local dev. Smoke-tested in this environment:
`FLASK_ENV=production gunicorn app:app --bind 127.0.0.1:8000` → /healthz 200
with `"env":"production"`, /jobs 200, sitemap + canonical built from BASE_URL,
static served with `Cache-Control: public, max-age=604800`.

## 4. Environment variables added

`FLASK_ENV` (production disables debug — debug can never be on in prod),
`SECRET_KEY` (ephemeral fallback + loud warning if unset in production),
`BASE_URL` (drives every absolute URL), `JAPAN_JOBS_DB` (already existed, now
documented + re-exported in config), `HOST`, `PORT`. All in `.env.example`
with safe local defaults — zero env vars needed for development.

## 5. Privacy/trust improvements

New **/privacy** page covering exactly the required points: localStorage-only
profile/tracker/resume data (with the clearing-browser-data caveat), the
newsletter as the single server-side exception, export/import/delete via
/data, job data provenance (public pages, links to original, inferred fields
labeled and fallible — "always verify visa/salary/language with the
employer"), and a clear not-legal/immigration-advice note. Footer now links
Privacy & data, Export your data, Source disclaimer, Contact & community.
/privacy is in the sitemap.

## 6. SEO fixes

OG image actually exists now; BASE_URL-driven canonical/sitemap/OG/JSON-LD
(verified emitting the configured origin under gunicorn); noindex on 9
user-specific/utility page types including saved/applied/archived views and
error pages; unique meta descriptions on job detail pages (title + company +
location + description snippet); /privacy added to sitemap; no duplicate
content routes (old /roadmaps 301s verified earlier). `SEO_CHECKLIST.md`
records what's done, the deploy-day steps (Search Console, rich-results
test, OG card check) and known trade-offs.

## 7. Performance fixes

`/jobs` dropdown counts collapsed from 10 GROUP BY queries into one bulk scan
(only actively-filtered columns get their own query), verified byte-identical
counts: **/jobs 218→110ms, /saved 263→74ms** in-process. Production static
caching (7 days) via `SEND_FILE_MAX_AGE_DEFAULT`; fonts already preconnected
with `display=swap`. Raw job query remains ~16ms at 2.5k rows with indexes on
every filterable column — headroom for tens of thousands of rows.

## 8. Docs added/updated

`DEPLOYMENT.md` (env table, gunicorn, Render, health checks, SQLite notes,
PII note for the newsletter table), `MAINTENANCE.md` (+production section,
scraper refresh examples, troubleshooting runbook: port 5000/AirPlay, HEAD vs
GET 403s, stale reloader, DB backup/restore, blocked scrapers, static cache),
`SEO_CHECKLIST.md`, `README.md` (dev vs prod commands, doc links),
`.env.example`.

## 9. Tests run and results

- `python -m pytest -q` → **9 passed** (now real: `check()` asserts, so pytest
  fails on regressions; `pytest.ini` fixes collection on this filesystem).
- `python test_app.py` → ALL PASS (90+ checks).
- Dev server GETs: all 12 routes from the brief + 404 page → expected codes.
- Static GETs: favicon/logo/og-default.svg/**og-default.png**/gh-state.js → 200.
- Gunicorn production smoke test → passed (see §3).
- `python update.py --backfill --dry-run` → clean, 0 pending changes.
- Empty-database boot test → all key pages 200, healthz reports honestly.

## 10. Remaining launch blockers — be honest

**Real blockers (do before announcing):**
1. **No domain decisions made** — BASE_URL, and the `gaijinhunter.com`
   placeholder inside employer-post canonical URLs (`db.create_employer_post`)
   should match the real domain.
2. **Scrapers have not run from a production IP.** Sandbox networking blocked
   real fetches in all of these passes; run `python update.py --limit 25 -v`
   from the deploy box and watch the zero-jobs warnings before trusting cron.
3. **No rate limiting** on POST endpoints (/post-a-job, newsletter subscribe).
   Honeypot exists, but a cheap spam run would pollute the board. Add
   Flask-Limiter or host-level rate limits before promoting /post-a-job.

**Acceptable for launch, fix soon:**
- Page HTML is heavy (~150KB inline CSS/JS in base.html on every page);
  extracting to a cached static file is the next perf win.
- The newsletter has no double-opt-in or sending pipeline — it collects
  addresses only; either wire it up or label it "coming soon".
- OG image uses the older navy branding (works, but off-brand).
- No JobPosting JSON-LD yet (Google Jobs eligibility).
- SQLite on a single disk = single point of failure; backups are manual/cron.
