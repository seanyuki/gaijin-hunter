# Deployment

## TL;DR (any host)

```bash
pip install -r requirements.txt
export FLASK_ENV=production SECRET_KEY=$(python3 -c 'import secrets;print(secrets.token_hex(32))')
export BASE_URL=https://gaijinhunterjp.com     # canonical origin (apex; www 301s to it)
export JAPAN_JOBS_DB=/var/data/jobs.db         # SQLite on persistent storage
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60
```

`python app.py` stays the development command (debug on, 127.0.0.1:5000).
Debug is hard-disabled when `FLASK_ENV=production`.

## Environment variables

| Var | Required | Purpose |
|---|---|---|
| `FLASK_ENV` | prod: yes | `production` disables debug, enables static caching |
| `SECRET_KEY` | prod: yes | session/flash signing (ephemeral fallback + warning if missing) |
| `BASE_URL` | prod: yes | public origin for canonical/sitemap/OG/llms URLs |
| `JAPAN_JOBS_DB` | recommended | SQLite path; default `./jobs.db` |
| `HOST` / `PORT` | optional | bind for `python app.py` (gunicorn uses `--bind`) |

See `.env.example`.

## Render.com (blueprint included)

`render.yaml` defines the web service with `/healthz` health checks, a 1 GB
persistent disk mounted at `/data` for the SQLite DB, and generated
SECRET_KEY. BASE_URL is preset to https://gaijinhunterjp.com; add the custom domains in Render and follow DOMAIN_SETUP.md for Squarespace DNS.

Seeding data: open a Render shell and run `python update.py` (or upload an
existing `jobs.db` to `/var/data/`). Schedule refreshes with a Render cron job:
`python update.py && python backfill.py --apply`.

## Health & monitoring

- `GET /healthz` → `{"status":"ok","jobs":N,"last_seen_at":...,"env":...}`;
  500 + error JSON if the DB is unreachable. Point uptime checks here.
- 404/500 render friendly branded pages; 500s are logged with stack traces.
- `update.py` prints a per-source summary table and **warns loudly when a
  source returns zero jobs** (layout change / block).

## Notes & limits

- **SQLite + 2 workers is fine at this scale** (reads dominate; WAL mode is
  on; writes happen during scrapes). Don't run `update.py` from two places at
  once. If traffic grows, move scraping to a cron container writing to the
  same disk.
- The scrapers respect robots.txt; run them from a box whose IP you're happy
  with, and keep `--delay` at defaults or higher.
- The newsletter table contains subscriber emails — that's the only PII on the
  server. Back up `jobs.db` accordingly (`cp` while no scrape is running, or
  `sqlite3 jobs.db ".backup backup.db"`).

## First refresh on the live box (runbook)

The scrapers have never run from the production IP before launch. Start
bounded and verbose; never start with a full refresh.

```bash
# 0. Back up first (always before a large refresh)
sqlite3 /var/data/jobs.db ".backup /var/data/jobs-$(date +%F).db"

# 1. Bounded, verbose, one source at a time — watch for zero-jobs warnings
python update.py --only japandev  --limit 25 --verbose
python update.py --only yolojapan --limit 25 --verbose
python update.py --only gaijinpot --limit 25 --verbose

# 2. Optional: parse-only pass across everything
python update.py --dry-run --limit 10

# 3. Full refresh only after the bounded runs look healthy
python update.py
```

After the refresh, sanity-check the data:

```bash
curl -s https://gaijinhunterjp.com/healthz          # status ok, jobs count sane
# /jobs in a browser: cards render, filters work

# source distribution — no source should silently drop to zero
sqlite3 /var/data/jobs.db "SELECT source, COUNT(*) FROM jobs GROUP BY source;"

# fit-score distribution — should span roughly 0–100 with mass in 40–80
sqlite3 /var/data/jobs.db "SELECT foreigner_fit_score/10*10 AS bucket, COUNT(*)
                           FROM jobs GROUP BY bucket ORDER BY bucket;"

# after any scoring-rule change, preview the recompute first:
python backfill.py --dry-run
python backfill.py --apply
```

If a source returns zero jobs, update.py warns explicitly; reproduce with
`python update.py --only <source> --limit 5 --verbose` before re-enabling it
in cron.
