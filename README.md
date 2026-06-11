# Gaijin Hunter — Jobs and Careers in Japan

A scraper + tiny Flask UI for surfacing jobs from sources that cater to foreigners working in Japan. Currently aggregates **GaijinPot**, **TokyoDev**, **JobsInJapan.com**, **CareerCross.com** (driven by a configurable saved-search URL), direct **Greenhouse** and **Lever** company endpoints for foreigner-friendly Japan companies (Mercari, SmartNews, PayPay, Woven by Toyota, Wise, etc. — edit `companies.json` to add more), and **JobSpy** (Indeed Japan + LinkedIn Japan + Glassdoor Japan via the python-jobspy library). The schema and UI are source-agnostic so additional sites can plug in without schema changes.

### Optional: rotating proxies (for sites that 403 you)

TokyoDev's detail pages and LinkedIn aggressively rate-limit. To rotate through proxies:

- Set `GAIJIN_HUNTER_PROXIES="user:pass@host1:port,host2:port"` in your environment, **or**
- Create a `proxies.txt` file (one proxy per line, `#` for comments).

The scrapers detect this automatically and round-robin through the pool, with per-proxy cooldown when one returns 403/429/503. No proxies configured = direct connection (current behavior).

## Quick start

```bash
cd japan-jobs
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Refresh all sources in one command
python update.py                     # fast pass (~30s)
python update.py --enrich            # full pass with TokyoDev detail pages (~3 min)
python update.py --only tokyodev     # one source only
python update.py --skip jobspy       # everything except one or more sources
python update.py --limit 25          # bounded run (max N jobs per source)
python update.py --dry-run           # fetch + parse, write nothing
python backfill.py --dry-run         # preview data-quality maintenance passes
python backfill.py --apply           # english-level / salary / language /
                                     # provenance / score backfills (see MAINTENANCE.md)
python test_app.py                   # tests: inference, extraction, filters, routes
python screenshot_pass.py            # Playwright screenshots at 390/768/1440

# Run the web UI (development: debug on, 127.0.0.1:5000)
python app.py
#   → open http://127.0.0.1:5000

# Production (see DEPLOYMENT.md for env vars + Render blueprint)
FLASK_ENV=production gunicorn app:app --bind 0.0.0.0:8000
curl http://127.0.0.1:8000/healthz
```

Docs: [DEPLOYMENT.md](DEPLOYMENT.md) · [DOMAIN_SETUP.md](DOMAIN_SETUP.md) (Squarespace DNS → Render) · [MAINTENANCE.md](MAINTENANCE.md) ·
[SEO_CHECKLIST.md](SEO_CHECKLIST.md) · config via `.env.example`

### Features

- **All GaijinPot's filters**, plus quick-chip shortcuts for the queries foreigners use most ("No Japanese", "Remote OK", "Apply from abroad", "Posted this week", "¥8M+").
- **Multi-select with Undisclosed** on every filter dropdown, with live counts.
- **Sort** by newest / salary high→low / salary low→high / title.
- **Salary** is parsed into numeric min/max JPY columns (annualized so monthly/hourly compare cleanly), enabling salary-range filters and sort.
- **Posted-within** filter (7 / 30 / 90 days).
- **Save jobs** with a ⭐ — persisted in your browser via localStorage, no account needed.
- **Stale detection**: rows not seen in the last 30 days are auto-archived and hidden by default. Toggle "Show archived" to see them, or use `/archived`.
- **JSON API** at `/api/jobs.json` with the same query language as the UI.
- **Source-agnostic schema** — currently aggregates GaijinPot and TokyoDev; adding Daijob/CareerCross/Greenhouse endpoints is a new scraper module that writes the same dict shape.

## Project layout

```
japan-jobs/
├── scraper.py        # GaijinPot scraper (CLI)
├── db.py             # SQLite schema + queries
├── app.py            # Flask app
├── templates/
│   ├── base.html
│   ├── index.html    # list + filters
│   └── job.html      # detail page
├── requirements.txt
└── README.md
```

## Scraper

```
python scraper.py [--pages N] [--delay 1.5] [--limit N] [--debug] [--dry-run] [-v]
```

- `--pages` — number of listing pages to walk (default 2).
- `--delay` — seconds between requests (default 1.5). Keep this polite.
- `--limit` — cap total jobs processed (useful when iterating on selectors).
- `--debug` — write sample HTML to `./debug/` so you can eyeball selectors.
- `--dry-run` — parse but don't write to the DB.

The scraper:

1. Walks `https://jobs.gaijinpot.com/en/job/index/search/page/N`.
2. Finds candidate detail URLs by URL pattern (`/job/view/<id>/...`) instead of fragile class names.
3. Parses each detail page using layered selectors: schema.org microdata, then common class names, then label/value lookups (`<dt>/<dd>`, `<th>/<td>`, label-spans), then regex on body text for Japanese-level normalization.
4. Upserts into SQLite. Re-running refreshes `last_seen_at` on jobs we've already indexed.

If GaijinPot tweaks its template and a field stops parsing, run with `--debug` and inspect the dumped HTML in `./debug/`; add the new selector to the corresponding `_first_text(...)` list in `scraper.py`.

## Database

SQLite at `./jobs.db`, single table `jobs`, deduplicated by `url`. Columns:

`source, url, title, company, location, salary, japanese_level, english_level, employment_type, description, tags, posted_date, scraped_at, last_seen_at`.

Indexes on `source`, `japanese_level`, `location`, `last_seen_at`.

## Adding more sources later

`source` and `url` are the only required fields, so a Daijob scraper, a Lever JSON pull, or a TokyoDev RSS importer can write to the same table. Make each new scraper a separate module that produces dict rows of the same shape and reuses `db.upsert_job`.

## Notes on respectful scraping

- Real Chrome User-Agent (`HEADERS` in `scraper.py`).
- 1.5s delay between requests by default.
- Store snippet + link out in v1 — full description is captured for filtering/search but you should think about display before republishing other people's job copy verbatim.
- Re-crawl daily at most. Job listings don't change minute-to-minute.
