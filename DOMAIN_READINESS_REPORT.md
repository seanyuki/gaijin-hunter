# Domain readiness report — gaijinhunterjp.com (June 11, 2026)

## 1. Recommended canonical domain

**`https://gaijinhunterjp.com` (apex, no www).** Cleaner in links and
citations, Render supports apex directly via its A record, and one short
canonical keeps sitemap/OG/JSON-LD simple. `www.gaijinhunterjp.com` 301s to
the apex at two layers: Render's edge (add both domains to the service) and
the app itself — a new production-only host-canonicalization middleware
redirects ANY non-canonical host (www., *.onrender.com) to BASE_URL,
preserving path + query. `/healthz` is exempt so Render's health checks
(which arrive on the internal host) always get 200. Switching to www-canonical
later is one env change (`BASE_URL=https://www.gaijinhunterjp.com`).

## 2. Files changed

- `config.py` — `CANONICAL_HOST` derived from BASE_URL (hostname only; a port
  in BASE_URL previously caused a redirect loop — found and fixed in testing).
- `app.py` — `before_request` host canonicalization (prod-only, healthz exempt).
- `db.py` — employer-post placeholder URL `gaijinhunter.com` → BASE_URL /
  `gaijinhunterjp.com` (was a flagged blocker).
- `render.yaml` — real domain, `/var/data` disk, post-deploy domain steps.
- `.env.example` — production values for gaijinhunterjp.com.
- `DEPLOYMENT.md` — real domain/paths + **first-refresh scraper runbook**.
- `README.md` — doc links.
- New: `DOMAIN_SETUP.md`, `scripts/smoke_prod.sh`, this report.

## 3. Render deployment settings (render.yaml)

Web service `gaijin-hunter`, plan **starter** (free tier has no persistent
disk — that matters, see §6), build `pip install -r requirements.txt`, start
`gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60`,
health check `/healthz`, disk `data` mounted at `/var/data` (1 GB).
After first deploy: Settings → Custom Domains → add `gaijinhunterjp.com` and
`www.gaijinhunterjp.com`, then do DNS.

## 4. Squarespace DNS instructions

Full step-by-step in **DOMAIN_SETUP.md**: open Domains dashboard →
gaijinhunterjp.com → DNS Settings → **delete Squarespace's default site
records** (the four A records on `@`, any AAAA on `@`, the default www CNAME;
keep MX/TXT) → add Render's records:

| Record | Host | Value |
|---|---|---|
| A | `@` | Render-shown IP (currently `216.24.57.1`) |
| CNAME | `www` | `<your-service>.onrender.com` |

With explicit warnings about: conflicting A/AAAA/CNAME records, propagation
delays (minutes–48h, check with `dig`), Render SSL staying "Pending" until
DNS resolves, and using GET (not `curl -I`/HEAD) for route checks.

## 5. Environment variables needed (Render)

```
FLASK_ENV=production
BASE_URL=https://gaijinhunterjp.com
SECRET_KEY=<generated — render.yaml uses generateValue: true>
JAPAN_JOBS_DB=/var/data/jobs.db
```
(`PORT` is injected by Render; gunicorn binds to it.)

## 6. Persistent database plan

- **Mount path:** `/var/data` (Render disk `data`, 1 GB) — without it SQLite
  is wiped on every deploy.
- **DB path:** `JAPAN_JOBS_DB=/var/data/jobs.db`; the app creates the schema
  on startup if missing.
- **Seeding:** upload an existing `jobs.db` to `/var/data/` via the service
  shell, or run the first-refresh runbook.
- **Backups:** `sqlite3 /var/data/jobs.db ".backup /var/data/jobs-$(date +%F).db"`
  before any large refresh (documented in the runbook); `backfill.py`/`fix_data.py`
  also auto-backup before writing. Note: Render disks have no automatic
  off-box backup on starter — periodically download a backup copy.

## 7. Smoke-test commands

```bash
BASE_URL=https://gaijinhunterjp.com ./scripts/smoke_prod.sh
```
Plain GETs (follows canonical redirects, 20s timeout, clean PASS/FAIL, exit
code 0/1) across /healthz, /, /jobs, the three filter aliases,
applying-from-abroad, /privacy, /resume, sitemap/robots/llms, favicon/logo/
og-default.png, plus a healthz-body assertion (`status:ok`).
First-refresh scraper runbook (bounded japandev/yolojapan/gaijinpot runs with
`--limit 25 --verbose`, dry-run pass, then full refresh, then source- and
fit-distribution SQL checks) is in DEPLOYMENT.md.

## 8. Test results

- `python -m pytest -q` → **9 passed**.
- Dev server (`python app.py`) + `BASE_URL=http://127.0.0.1:5000 ./scripts/smoke_prod.sh`
  → **16/16 PASS**.
- Gunicorn production mode + smoke script → **16/16 PASS** (after fixing the
  port-in-BASE_URL redirect loop the test run itself uncovered).
- Canonicalization verified under gunicorn with `FLASK_ENV=production
  BASE_URL=https://gaijinhunterjp.com`:
  - `Host: www.gaijinhunterjp.com /jobs` → `301 https://gaijinhunterjp.com/jobs`
  - `Host: gaijin-hunter.onrender.com /jobs?visa_support=1` →
    `301 https://gaijinhunterjp.com/jobs?visa_support=1` (query preserved)
  - `Host: gaijinhunterjp.com /jobs` → 200 (no redirect)
  - `/healthz` on any host → 200 (exempt)
  - sitemap `<loc>` entries emit `https://gaijinhunterjp.com/...`

## 9. Remaining launch risks

1. **DNS/SSL not yet executed** — everything past the Render dashboard is
   instructions, not verified reality. The Render A-record IP must be taken
   from Render's panel at setup time (it can differ from the documented one).
2. **Scrapers still untested from Render's IP** (sandbox networking blocked
   real fetches in every pass). The bounded runbook exists precisely for this;
   GaijinPot/YOLO could behave differently toward datacenter IPs.
3. **No rate limiting** on /post-a-job and newsletter signup (carried over
   from the last report) — add before promoting those entry points.
4. **Render starter plan + SQLite**: single instance, no zero-downtime deploy
   guarantee for in-flight scrape writes; don't schedule cron refreshes during
   deploys, and download off-box DB backups periodically.
5. Squarespace occasionally re-adds default records when its site builder is
   touched — if the site suddenly shows a Squarespace page, re-check DNS.
