# Scheduled scraper refresh (Render cron)

**Status: disabled until the first manual production scrape succeeds.**
The cron block in `render.yaml` is commented out on purpose. Scrapers have
never run from Render's IP — enabling cron before a clean manual run risks
filling the live DB with empty/blocked results on a schedule.

## Step 1 — manual first run (required)

From the Render service **Shell** (Dashboard → service → Shell). Always back
up first; go bounded and verbose before any full run:

```bash
sqlite3 /var/data/jobs.db ".backup /var/data/jobs-$(date +%F).db"

python update.py --only japandev  --limit 25 --verbose
python update.py --only yolojapan --limit 25 --verbose
python update.py --only gaijinpot --limit 25 --verbose
python update.py --dry-run --limit 10            # parse-only across all sources

# Full run only once the bounded runs look healthy:
python update.py
python backfill.py --dry-run                      # preview; then:
python backfill.py --apply
```

Confirm afterwards:

```bash
curl -s https://gaijinhunterjp.com/healthz        # status ok, jobs count sane
sqlite3 /var/data/jobs.db "SELECT source, COUNT(*) FROM jobs GROUP BY source;"
```

No source should silently sit at zero. If one does, `update.py` already warns;
reproduce with `python update.py --only <source> --limit 5 --verbose`.

## Step 2 — enable cron (after Step 1 is clean)

Uncomment the `cronJobs:` block at the bottom of `render.yaml` and redeploy
(or create the cron job in the Render dashboard with the same settings):

- **Command:** `python update.py && python backfill.py --apply`
  (`update.py` already isolates per-source failures and prints a summary;
  `backfill.py --apply` re-runs the conservative english-level / salary /
  language / provenance / score passes and auto-backs-up the DB. There is no
  single `--all --backfill` flag — this two-command form is the supported way.)
- **Schedule:** `0 18 * * *` (daily, 18:00 UTC ≈ 03:00 JST — off-peak for JP
  sites). For twice daily use `0 6,18 * * *`.
- **Disk:** must mount the **same** `data` disk at `/var/data` so cron writes
  the DB the web service reads.
- **Env:** `JAPAN_JOBS_DB=/var/data/jobs.db`.

## Notes

- Don't run cron during a deploy or while another `update.py` is running —
  SQLite single-writer. Render runs cron in a separate instance; keep the
  schedule off your typical deploy windows.
- Keep `--delay` at defaults or higher to stay polite; scrapers respect
  robots.txt.
- After any change to scoring rules in `inference.py`, run
  `python backfill.py --only scores --dry-run` then `--apply` once.
