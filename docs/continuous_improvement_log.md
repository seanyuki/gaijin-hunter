# Continuous Improvement Log — Gaijin Hunter (gaijinhunterjp.com)

Maintained by the operating-system agent. Newest entry first.

---

## 2026-06-12 (later) — Hotfix: production scrape insert failure

**Symptom:** first production scrape loaded only YOLO Japan + JapanDev;
GaijinPot and JobSpy died with `sqlite3.IntegrityError: NOT NULL constraint
failed: jobs.is_employer_post`. JobSpy also logged "Glassdoor is not
available for JAPAN" on every Glassdoor call.

**Root cause:** `upsert_job` builds its INSERT/UPDATE by naming every column
explicitly, so SQL `DEFAULT 0` never applies — a job dict without
`is_employer_post` writes an explicit NULL into a NOT NULL column. Only
japandev_scraper and yolojapan_scraper set the field, which is exactly why
only those two sources loaded. (Local dev never hit it because the local DB
rows came from those sources/older schema states.)

**Fix (db.py `_derive_fields`, central — covers all 14 sources with zero
scraper edits):** default `is_employer_post=0` when None; also auto-fill
`scraped_at`/`last_seen_at` (the other NOT NULL bookkeeping columns) when
missing. Only None/missing is replaced — `create_employer_post` still writes
`is_employer_post=1` and explicit scraper values are preserved.

**Glassdoor:** removed from `DEFAULT_SITES` in jobspy_scraper.py (JobSpy has
no Japan support for it; every call failed). Still reachable via
`--sites glassdoor` if that ever changes.

**Tests:** new `test_upsert_not_null_defaults` reproduces the production
case against a *fresh-schema temp DB*: minimal scraped job inserts, defaults
to 0, update path survives, employer post stays 1, explicit values
preserved. New `test_jobspy_sites_exclude_glassdoor`. `pytest -q` → **15
passed**. Bounded `update.py --only gaijinpot/jobspy --limit 5 --verbose`
runs: no IntegrityError; network egress is blocked from this sandbox
(proxy 403), so re-verify inserts with the same commands from production.

---

## 2026-06-12 — Baseline audit + Batch 1

### Current app status

Flask app (~1.7k lines) with 60+ routes: job search/filters, job detail with
JobPosting JSON-LD, saved/applied/tracker (localStorage), resume suite
(rirekisho, shokumu keirekisho, CV, cover letter, bullets), 7 interactive
tools, guides/living/pillar content hubs, companies directory, salary
insights, post-a-job with employer self-manage tokens, newsletter capture,
/healthz, custom 404/429/500 pages, rate limiting (Flask-Limiter), canonical
host redirect, dynamic sitemap/robots/llms.txt. Tests: `test_app.py`,
12 pytest checks passing. Render blueprint (`render.yaml`) with persistent
disk at /var/data; cron refresh intentionally disabled until first manual
production scrape succeeds.

### Scraper/source coverage (DB snapshot 2026-06-12, 2,565 rows)

| Source | Rows | Last seen | Status |
|---|---|---|---|
| YOLO Japan | 1,994 | 06-11 | Working; robots-compliant sitemap crawl. 78% of DB — mostly part-time/service; handled by `professional_only` filter + "recommended" sort, but still skews stats |
| gaijinpot | 174 | 05-26 | Stale 17 days — auto-archives at 30 days |
| tokyodev | 168 | 05-26 | Stale 17 days; always-enrich (detail pages) |
| jobspy (Indeed/LinkedIn/Glassdoor) | 115 | 05-27 | Stale; English-ratio filter ≥0.6 guards false positives |
| japandev | 61 | 06-09 | Working |
| greenhouse | 53 | 05-26 | Stale; 10 companies in companies.json |
| jobsinjapan | 0 | — | Wired but never produced rows — needs a production-IP run to diagnose |
| careercross | 0 | — | Driven by saved-search URL; never produced rows |
| robertwalters | 0 | — | Sitemap-based, inference-labeled; never produced rows |
| lever | 0 | — | Only 1 company (Wise); board may list no Japan roles |
| ashby | 0 | — | 2 companies (OpenAI, Ramp); Japan filter may exclude all |
| workable / smartrecruiters / recruitee | 0 | — | **Placeholder "example-co" slugs only** — every run fires doomed requests |

Scraper architecture is sound: per-source failure isolation in update.py,
zero-jobs warnings, dedupe by unique URL, 30-day stale auto-archive,
provenance columns (visa_source, salary_source, …), dry-run/limit/only flags,
robots-compliance documented per scraper (YOLO avoids disallowed AJAX
endpoint; RW uses public sitemap). Sandbox networking blocks all scraper
targets (proxy 403), so live verification requires a production/local run —
this also blocked verifying any new ATS company slugs.

### SEO/content status

Strong: canonicals everywhere, BASE_URL-driven absolute URLs, robots.txt with
AI-crawler allowances + sitemap link, llms.txt, noindex on utility pages,
unique titles/metas on job pages, JobPosting JSON-LD on /job/<id> (implemented
since SEO_CHECKLIST was written — checklist is outdated), FAQPage/
Organization/WebSite JSON-LD, large genuine content library (guides, living,
pillars, glossary, tools) covering target queries (visa sponsorship, no
Japanese, rirekisho, shokumu keirekisho, apply from abroad, IT jobs, etc.).

Gaps:
1. **Sitemap `lastmod` is `today` for every URL on every request** — a known
   anti-pattern; crawlers learn to ignore lastmod entirely.
2. **Job detail pages are absent from the sitemap** — the pages carrying
   JobPosting JSON-LD (Google Jobs eligibility) rely on crawl discovery
   through the listing only.
3. OG image still old navy branding (cosmetic, deferred).

### UX/product status

Previously audited (UX_REPORT.md, screenshots at 390/768/1440). Landing page
with live counts, quick chips, fit-score "recommended" sort, professional-only
filter, empty states, tracker, similar-jobs API. No regressions spotted; no
UX changes in this batch — data freshness is the bigger user-facing problem.

### Production risks

1. **PII committed to git**: 7 `jobs.db.bak_*` files + `jobs.db.corrupt`
   (~50 MB) are tracked, and the backfill backups contain
   `newsletter_subscribers` emails. `.gitignore`'s `*.bak` doesn't match
   `jobs.db.bak_fix_*` style names. Also tracked junk: `content.py.bak2-4`
   (~950 KB), `_wtest.txt`, a stray `guides_extra.py"` (trailing-quote
   filename), `.DS_Store`; untracked empty `main` file.
2. **Data staleness**: 3 of 5 productive sources last ran 05-26/27. At 30
   days unseen, rows auto-archive — without a production scrape by ~06-25 the
   board collapses to YOLO part-time + japandev. Cron is still disabled.
3. Zero-row sources waste run time and mask real coverage gaps.
4. Newsletter collects emails with no double-opt-in/sending pipeline (known).
5. SQLite single-disk; backups manual (known, acceptable at this scale).

### Prioritized backlog

1. ~~Repo hygiene: untrack/delete DB backups (PII), .bak files, junk; fix .gitignore~~ → **Batch 1**
2. ~~Sitemap: real lastmod; include active job detail URLs~~ → **Batch 1**
3. ~~Remove placeholder ATS slugs from companies.json~~ → **Batch 1**
4. ~~healthz: expose data-age so stale data is visible to monitoring~~ → **Batch 1**
5. (Sean, production) First manual scrape from production IP; then enable cron (CRON_SETUP.md)
6. (Sean, optional) `git filter-repo` to purge PII from git history before repo is ever shared
7. Verify/expand ATS company lists (lever/ashby/workable/SR/recruitee) from a network-capable machine; diagnose jobsinjapan/careercross/robertwalters zero-row state
8. Extract ~150 KB inline CSS/JS from base.html to cached static files (perf)
9. Expired-job pages: 410/"posting expired" page with similar-jobs links instead of bare 404
10. Regenerate OG image in current warm palette
11. Newsletter: double-opt-in or "coming soon" label
12. Update SEO_CHECKLIST.md (JobPosting JSON-LD line is stale)

### Batch 1 plan (this session)

Theme: data-safety + crawlability. No feature changes, no risky scraper edits.

1. **Repo hygiene (PII/safety)** — `git rm --cached` + delete: 7
   `jobs.db.bak_*`, `jobs.db.corrupt`, `content.py.bak2/3/4`, `_wtest.txt`,
   `guides_extra.py"`, `.DS_Store`, empty `main`. Tighten `.gitignore`
   (`jobs.db*`, `*.bak*`, `*.corrupt`, `main` not needed — keep specific).
2. **Sitemap improvements** (app.py): per-URL honest `lastmod` (job pages →
   `last_seen_at`; company pages → newest posting; static/content pages → no
   lastmod rather than a fake one); add active (non-archived) job detail
   URLs, excluding withdrawn/expired employer posts.
3. **companies.json**: drop "example-co"/"ExampleCompany" placeholders so
   workable/smartrecruiters/recruitee skip cleanly instead of firing doomed
   requests every run.
4. **healthz**: add `data_age_days` + `fresh_jobs` so monitoring can alert on
   staleness without failing the Render health check (always 200 when DB is
   readable).
5. **Tests**: extend test_app.py — sitemap contains job URLs + honest
   lastmod; healthz new fields.

Verification: `python -m pytest -q`, route checks (/, /jobs, /job/<id>,
/sitemap.xml, /robots.txt, /healthz, 404), static asset checks, sitemap XML
well-formedness, `update.py --backfill --dry-run`.

### Batch 1 results (implemented + verified)

1. **Repo hygiene/PII** — untracked and deleted 7 `jobs.db.bak_*` + 2 stray
   `-wal` files, `jobs.db.corrupt`, `content.py.bak2/3/4`, `_wtest.txt`,
   `guides_extra.py"`, `.DS_Store`, empty `main` (~52 MB, incl. newsletter
   PII). `.gitignore` now also covers `*.db.*`, `*.db-wal/-shm`, `*.bak*`,
   `*.corrupt`. NOTE: PII remains in git *history*; purge with
   `git filter-repo` before the repo is ever shared/made public.
2. **Sitemap** (app.py) — fabricated `lastmod=today` removed (static/content
   pages now omit lastmod); company pages get lastmod from their newest
   posting; **2,565 active job detail URLs added** with honest lastmod from
   `last_seen_at` (archived rows, withdrawn/expired/unapproved employer posts
   excluded). 2,888 URLs total, well-formed, zero duplicates.
3. **Company slug collision bug (found by new test, fixed in db.py)** —
   Japanese-named companies all collapsed to slug "company" (131 dupes;
   130 company pages unreachable). `_company_slug` now appends a stable
   8-char hash for non-ASCII names; ASCII slugs unchanged (no URL churn).
   Case-variant duplicates (Exawizards/ExaWizards) deduped in sitemap;
   lookup stays deterministic.
4. **companies.json** — removed `example-co`/`ExampleCompany` placeholders;
   workable/smartrecruiters/recruitee now no-op in 0.1 s instead of firing
   doomed requests every refresh.
5. **healthz** — now returns `fresh_jobs`, `data_age_days`, and
   `status: ok|stale` (stale when data older than 7 days) while always
   responding 200 when the DB is readable, so Render health checks never
   flap but external monitoring can alert before the 30-day archive window
   empties the board.
6. **Tests** — new `test_sitemap_and_healthz` (XML well-formedness, job URLs
   present with honest lastmod, no fabricated static lastmod, no duplicate
   URLs, healthz freshness fields).

Verification: `pytest -q` → **13 passed**. Route sweep (17 routes + 404) all
expected codes; static assets 200; job page renders JobPosting JSON-LD;
sitemap lastmod cross-checked against DB; robots.txt intact;
previously-unreachable Japanese-company pages now resolve;
`update.py --backfill --dry-run` clean; bounded `--dry-run` runs for
workable/recruitee clean. Live scraper fetches remain blocked from this
sandbox (proxy 403) — production-IP run still required.
