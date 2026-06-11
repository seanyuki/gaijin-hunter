# Final pre-launch safety + SEO pass — June 11, 2026

## 1. Public write endpoints found

Audited every route in app.py. POST / write endpoints:

| Endpoint | Method | Purpose |
|---|---|---|
| `/post-a-job` | POST | employer-direct job submission (public form) |
| `/api/newsletter/subscribe` | POST | newsletter signup |
| `/employer/manage/<token>/withdraw` | POST | manage own post |
| `/employer/manage/<token>/reactivate` | POST | manage own post |
| `/employer/manage/<token>/extend` | POST | manage own post |
| `/employer/manage/<token>/edit` | POST | manage own post |
| `/api/employer/cleanup` | POST | internal cron-style cleanup |

No other user-input writes exist (saved/applied/tracker/profile/resume are all
client-side localStorage — nothing hits the server).

## 2. Rate limiting approach

**Flask-Limiter** (added to requirements.txt), in-memory storage (fine for the
single gunicorn service; resets on restart, acceptable for spam throttling).
Key is the real client IP from `X-Forwarded-For` left-most entry — correct
behind Render's proxy. Limits:

- `/post-a-job`: **5/hour**
- `/api/newsletter/subscribe`: **10/hour**
- employer manage + `/api/employer/cleanup`: **20/hour** each
- global default: **300/hour** (writes only)
- **All GET/HEAD/OPTIONS reads exempt**, and `/healthz` exempt (a
  `request_filter` guarantees health checks never get throttled).

Friendly **429 handler**: JSON `{"ok":false,"error":"Too many requests…"}` for
`/api/*` and JSON clients, branded error page ("Too many requests. Please try
again later.") for form posts. No stack traces (production debug is off).

If Flask-Limiter ever fails to import, a no-op limiter keeps the app running
(logged) rather than crashing — graceful degradation.

## 3. Validation / honeypot added

`/post-a-job` already had a CSS-hidden `website` honeypot (→ 400), required
fields, and maxlengths. Strengthened: a real email regex (`_valid_email`)
applied to both the contact email and the optional apply-by-email; http(s)
URL validation (`_valid_http_url`) on the application URL; per-field length
caps on title/company/company_jp/location/contact-name/requirements/
description/industries/salary; a visible error message for the application-URL
field (was validated but silently). Newsletter signup validation
(email format + length) already lived in `db.newsletter_subscribe`.

**Private-beta copy:** `/post-a-job` now shows a "Private beta — direct
employer posting is being trialled" badge and states it's free during beta,
posts may be reviewed, and it's "not a paid or self-serve product yet" — so
nothing implies a live paid posting product.

## 4. JobPosting JSON-LD fields implemented

`_job_posting_jsonld()` builds schema.org JobPosting from **real DB data only**;
every optional field is omitted when absent. Always present: `@context`,
`@type`, `title`, `datePosted` (post_date, else scraped date), `url`
(absolute, **BASE_URL**), `identifier` (source + source_job_id/id). Conditional:
`description`, `employmentType` (mapped to schema enums), `hiringOrganization`,
`jobLocation` (PostalAddress, country JP, region/locality when known),
`jobLocationType: TELECOMMUTE` + `applicantLocationRequirements` (only if
`remote_work_ok==1` / `overseas_application_ok==1`), `baseSalary` (MonetaryAmount
JPY, **only when a numeric annual salary is parsed**), `directApply: true`
(only employer posts with a real apply target). **No invented salary,
validThrough, or remote flag.** Emitted via the `jsonld` block; renders only
when data qualifies. Verified: full object for a salaried job, minimal-but-valid
for a no-salary job, BASE_URL used for canonical url.

## 5. Render cron recommendation

**Disabled by design.** `render.yaml` has a fully commented `cronJobs:` block;
`CRON_SETUP.md` documents the manual-first workflow: bounded verbose runs
(`--only japandev/yolojapan/gaijinpot --limit 25 --verbose`), a `--dry-run
--limit 10` pass, then a full `python update.py`, with source/fit distribution
checks — **before** uncommenting cron. Recommended schedule once validated:
`0 18 * * *` (daily ~03:00 JST), command `python update.py && python
backfill.py --apply` (there is no `--all --backfill` flag; this two-command
form is the supported equivalent), same `/var/data` disk mounted.

## 6. Files changed

- `app.py` — Flask-Limiter setup + per-route limits + 429 handler;
  `_valid_email`/`_valid_http_url`; stronger post-a-job validation;
  `_job_posting_jsonld()` + job_detail passes it.
- `templates/job.html` — JobPosting `jsonld` block.
- `templates/post_a_job.html` — private-beta banner/copy, apply-URL error +
  maxlength, meta description.
- `requirements.txt` — Flask-Limiter.
- `render.yaml` — commented cronJobs block.
- `test_app.py` — JobPosting, BASE_URL-in-JSON-LD, and rate-limit tests.
- New: `CRON_SETUP.md`, this report.

## 7. Tests run and results

- `python -m pytest -q` → **12 passed**.
- `python test_app.py` → ALL PASS (now includes JobPosting validity, "salary
  only when parsed", "no fabricated validThrough", BASE_URL canonical, and
  rate-limit 5/hour + reads/healthz exempt).
- Dev server + `scripts/smoke_prod.sh` → **16/16 PASS**; live `/job/1` carries
  JobPosting JSON-LD; `POST /post-a-job` returns `200 200 200 200 200 429`.
- Gunicorn production mode + smoke → **16/16 PASS**; `/healthz` 200 across 12
  rapid hits (rate-limit exempt); JobPosting present; production `DEBUG=False`
  confirmed (no stack-trace leakage).
- Cleaned up a test-created employer post so the DB count is back to 2565.

## 8. Remaining launch risks

1. **DNS/SSL + first production scrape still pending** (carried over) — must be
   done on the live box; the runbooks (DEPLOYMENT.md, CRON_SETUP.md) cover it.
2. **In-memory rate-limit store** resets on deploy/restart and isn't shared
   across instances. Fine for one starter instance; if you scale to multiple
   workers/instances and want strict limits, point Flask-Limiter at Redis
   (`storage_uri`). Current setup is per-process — adequate for spam control.
3. **Employer posts are auto-approved** (`moderation_status='approved'`). The
   beta copy now says posts may be reviewed, but there's no actual moderation
   queue/admin UI yet — add one before promoting /post-a-job widely.
4. **Newsletter** still collects addresses with no double-opt-in or sending
   pipeline — label "coming soon" or wire it up before relying on it.
5. JobPosting JSON-LD is only as good as the data; Google may flag postings
   with no salary/validThrough as lower quality, but they remain valid — we
   deliberately don't fabricate to satisfy the validator.
