# Maintenance

## Refresh job data

```bash
python update.py                    # scrape all sources
python update.py --only gaijinpot   # one source
python update.py --limit 25 --dry-run
```

## Data-quality backfill (run after changing inference/scoring rules)

```bash
python backfill.py --dry-run                  # preview everything
python backfill.py --only english-level --dry-run
python backfill.py --only salary --dry-run
python backfill.py --only posting-language --dry-run
python backfill.py --only provenance --dry-run
python backfill.py --only scores --dry-run    # after scoring-rule changes
python backfill.py --apply                    # write (auto-backs-up jobs.db)
```

Guarantees: never overwrites non-null explicit values with inferred ones;
prints before/after counts and sample changed rows; idempotent, safe to rerun.
`python update.py --backfill` is an alias for `backfill.py --apply`.

## Provenance vocabulary

Per-field `*_source` columns (`visa_source`, `abroad_source`, `remote_source`,
`japanese_level_source`, `english_level_source`, `salary_source`):

- `explicit` — the source site stated it as structured data
- `inferred` — derived from posting text by conservative rules in `inference.py`
  / `salary_parser.extract_from_text`
- `not_stated` — we looked and found nothing (shown honestly in the UI)

## Tests

```bash
python test_app.py    # inference, classification, filters, routes
```

## Backups

`fix_data.py` and `backfill.py` write `jobs.db.bak_*` next to the DB before
applying. Delete old ones when disk space matters.

## Production

```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4
curl -s http://127.0.0.1:$PORT/healthz
```
See DEPLOYMENT.md for environment variables and Render setup.

## Scraper refresh examples

```bash
python update.py --dry-run                       # parse everything, write nothing
python update.py --only japandev --limit 50 -v   # bounded, verbose
python update.py --only yolojapan --limit 50 -v
python update.py                                 # full refresh (all sources)
```

## Troubleshooting

**Port 5000 already in use** — another `python app.py` (or macOS AirPlay
Receiver, which squats on 5000). `lsof -i :5000` then kill it, or run with
`PORT=5001 python app.py`.

**`curl -I` (HEAD) shows 403/405 but the site works** — some routes only
answer GET; always verify with GET:
`curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/`.

**Stale Flask reloader process** — the debug reloader forks; if changes don't
apply or the port is stuck, `pkill -f "python.*app.py"` and start again.

**DB backup/restore** — backfill/fix scripts auto-write `jobs.db.bak_*`.
Manual: `sqlite3 jobs.db ".backup jobs-$(date +%F).db"`. Restore by copying
the backup over `jobs.db` while the app and scrapers are stopped.

**Scraper blocked or zero jobs** — update.py warns per source. Reproduce with
`python update.py --only <source> --limit 5 --verbose`; check robots.txt and
whether the site changed markup. One failing source never aborts the run.

**Static asset looks stale after deploy** — production sends 7-day
Cache-Control for /static. Hard-reload, or bump the asset filename when
changing logo/og images.
