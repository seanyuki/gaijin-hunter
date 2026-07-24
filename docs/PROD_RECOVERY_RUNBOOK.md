# Production recovery runbook — July 24, 2026

Written after finding production serving **42-day-old data** while reporting
`/healthz` → `"status":"ok"`. Follow these steps in order; each has a check
that must pass before moving on.

## What was wrong

| | Local (after fixes) | Production (before this runbook) |
|---|---|---|
| Data age | 0 days | **42 days** (`last_seen_at: 2026-06-12`) |
| `/healthz` fields | `data_age_days`, `fresh_jobs` | missing — old build |
| Reported status | `ok` (correct) | `ok` (**wrong**) |

Three compounding causes:

1. **Production ran pre-checkpoint code.** Its `/healthz` lacked
   `data_age_days`/`fresh_jobs`, so the deployed build predated the
   launch-hardening work.
2. **Staleness alerting was silently broken.** Current code sets
   `status = "ok" if age_days <= 7 else "stale"` (`app.py`), but the deployed
   build had no age threshold — it reported `ok` on 42-day-old data forever.
3. **Nothing refreshed the data.** No crontab, no launchd agent, and the
   `cronJobs` block in `render.yaml` is commented out (gated on a first
   manual production scrape that never happened).

Separately, three scrapers had broken against upstream site changes and were
silently returning zero jobs — fixed in commit `f32808a`.

## Step 1 — Deploy the pushed code

Commits `5783cd5` (checkpoint) and `f32808a` (scraper repairs) are on
`origin/main`. Trigger the Render deploy (auto-deploy, or Manual Deploy →
Deploy latest commit).

**Check — the new build is live.** `data_age_days` must be present:

```bash
curl -s https://gaijinhunterjp.com/healthz
```

Expect a `data_age_days` field. Right after deploying it will read ~42 and
`"status":"stale"` — that is correct, and proves the freshness check now works.
If `data_age_days` is absent, the old build is still serving; do not continue.

## Step 1b — Snapshot, verify the path, drop YOLO Japan

**Snapshot first.** Use SQLite's `.backup`, NOT `cp` — `.backup` is atomic and
safe while gunicorn is reading the same file; a plain `cp` of a live SQLite DB
can capture a torn page or miss the WAL:

```bash
sqlite3 /var/data/jobs.db ".backup /var/data/jobs-$(date +%F).db"
```

Why it matters: `upsert_job`'s UPDATE branch (`db.py:369-373`) rewrites *every*
column except `scraped_at` from the scraper's dict, and `_derive_fields`
(`db.py:302-303`) re-derives `role_family` with the NEW classifier — writing
`NULL` when it declines to label. That is intended (5783cd5 shipped the
classifier rework) and every affected column is recomputable, but nothing takes
a snapshot before the first write. `backfill.py`'s own `.bak`
(`backfill.py:207-211`) only happens *after* `update.py` has already run.

**Verify the DB path.** `db.py:57` silently falls back to a repo-local
`jobs.db` if the var is unset, and `update.py` never logs which file it opened:

```bash
echo $JAPAN_JOBS_DB          # must print /var/data/jobs.db
```

**Drop YOLO Japan.** Deregistered in `b1200d4` as low-quality shift work; it was
~60% of all rows. The scraper can no longer add more, but existing rows remain
until deleted. Do this BEFORE the scrape so the resulting counts reflect the
real board:

```bash
sqlite3 /var/data/jobs.db "DELETE FROM jobs WHERE source='YOLO Japan'; VACUUM;"
```

Expect roughly 2570 → 1000-1300 rows. Note nothing in the application code
deletes rows — there is no `DELETE FROM`, `DROP TABLE` or `VACUUM` anywhere in
the tree — so this is a deliberate one-off, not something the scrape repeats.

## Step 2 — First manual production scrape

This is the gate `render.yaml` documents. Run from the Render **service shell**,
bounded first so a misbehaving source can't fill the disk:

```bash
python update.py --limit 25 --verbose
```

**Check — sane results.** In the output confirm:

- No `returned ZERO jobs` warnings for: gaijinpot, tokyodev, jobsinjapan,
  japandev, careercross, jobspy, greenhouse, ashby, workable,
  salesforce, microsoft, rakuten.
  - `yolojapan` must NOT appear at all. If it does, you are on `a548711` or
    earlier — deploy `b1200d4` or later first.
  - Expected zeros (not failures): `lever`, `smartrecruiters`, `recruitee` —
    thin `companies.json` config, no current Japan roles. `recruitee` has zero
    companies configured at all.
  - Known blocked: `robertwalters` — returns 403 to every request including a
    warmed full-browser session. Hard bot-block, ~5 jobs, not worth chasing.
- The DB actually grew and is on the persistent disk:

```bash
echo $JAPAN_JOBS_DB          # must be /var/data/jobs.db
curl -s https://gaijinhunterjp.com/healthz
```

`data_age_days` should now be ~0 and `status` back to `ok`.

**Important — the board is currently EMPTY, not merely stale.** All 2570
production rows are past `STALE_DAYS = 30` (`db.py:464`, filter at
`db.py:596-598`), so `/jobs` renders **zero** results right now — which is why
`fresh_jobs` is 0. The landing page's headline counters (`db.stats()`,
`db.py:795-805`) are *unfiltered* and still show the full row count, so the site
currently advertises thousands of jobs and then shows an empty list. The scrape
closes that gap; it does not widen it.

If that all holds, run a full pass and the data-quality backfill — **detached**,
because a full pass is 30-90 min and an ephemeral Render shell that drops takes
the run with it:

```bash
setsid nohup python update.py > /tmp/update.log 2>&1 &
tail -f /tmp/update.log
# when it finishes cleanly:
python backfill.py --apply
```

Most scrapers hold a single transaction for an entire source
(`jobspy_scraper.py:481`, `jobsinjapan_scraper.py:403`,
`salesforce_scraper.py:194`, `microsoft_scraper.py:257`), so a dropped shell
discards that source's rows. gaijinpot commits every 50 (`scraper.py:683`) and
rakuten every 25 (`rakuten_scraper.py:208-210`). Either way there is no
corruption — rollback is clean and `upsert_job` is idempotent on `url` — you
just lose the elapsed time.

**Never run two `update.py` at once.** There is no lockfile; the constraint is
documented in prose only (`DEPLOYMENT.md:49`). One shell, one operator.

**Expect `fresh_jobs` to stay well below `jobs`.** Production's existing rows
were written by `cf0480a`, whose `SOURCES` still included yolojapan and lacked
salesforce/microsoft/rakuten. Rows from retired sources can never be re-seen by
current code and stay permanently archived. After the YOLO deletion in Step 1b,
a realistic end state is `jobs` ≈ 2000-3000 with `fresh_jobs` ≈ 1000-2500. That
is correct, not damage.

### Abort signals

Stop immediately on any of these.

| Symptom | Meaning | Action |
|---|---|---|
| `OperationalError: no such column: X` on the first upsert | Real schema drift (audited as impossible — `COLUMNS` is byte-identical across every deployed commit, md5 `76feb2f29b9e`) | Stop. Nothing was written — `db.connect()` (`db.py:184-198`) skips the commit on exception. Run the missing-column check below and report before retrying |
| `echo $JAPAN_JOBS_DB` isn't `/var/data/jobs.db`, or backfill's `Backup:` line isn't under `/var/data` | Writing the wrong file | Stop, `export JAPAN_JOBS_DB=/var/data/jobs.db`, re-run. Production untouched |
| `/healthz` still shows `data_age_days` ~42 and `fresh_jobs` 0 after a clean-looking run | The write landed somewhere else | Stop before the full pass. Same fix as above |
| Every source logs `returned ZERO jobs`; exit code 1 | Egress block or mass upstream change | The `&&` already prevented backfill from running. Nothing written. Investigate one source: `python update.py --only gaijinpot --limit 5 --verbose` |
| `database is locked` | A second writer is active | Kill the duplicate. Rollback is clean; re-run |
| `disk I/O error` / `database or disk is full` | 1 GB disk (`render.yaml:32`) exhausted by `.bak` copies | SQLite rolls back — no corruption. `rm /var/data/jobs.db.bak_backfill_*` after verifying, re-run |
| Mass NULL `role_family`, scores collapsed | New classifier relabeled aggressively | Restore **with the web service stopped** (`MAINTENANCE.md:78-80`) so a live WAL can't replay over the restored file: `cp /var/data/jobs-$(date +%F).db /var/data/jobs.db`, then restart |

Missing-column check:

```bash
python -c "import sqlite3,db;c=sqlite3.connect('/var/data/jobs.db');have={r[1] for r in c.execute('PRAGMA table_info(jobs)')};print('MISSING:',sorted({n for n,_ in db.COLUMNS}-have))"
```

## Step 3 — Enable the refresh cron

**Only after Step 2 passes.** The gate exists because a cron job needs its own
mount of the *same* persistent disk — if that's misconfigured, an unattended
daily job writes to the wrong disk or errors on a schedule.

Uncomment the `cronJobs` block at the bottom of `render.yaml` (lines 42-54),
commit, push, and redeploy. Confirm in the block that:

- `disk.name` is `data` — the **same disk** as the web service
- `mountPath` is `/var/data`
- `JAPAN_JOBS_DB` is `/var/data/jobs.db`

Schedule is `0 18 * * *` (daily 18:00 UTC ≈ 03:00 JST). Use `0 6,18 * * *` for
twice daily.

**Check — the cron actually ran.** The morning after, `data_age_days` should be
< 1. If it climbs past 1, the cron isn't running or isn't writing to the shared
disk.

## Step 4 — Don't let this recur

`/healthz` deliberately returns HTTP 200 even when stale ("a stale board should
not take the site down"), so **nothing alerts on staleness** — it's only
visible if someone looks. Point an uptime monitor at the JSON body, not the
status code:

- Alert when `data_age_days > 2`, or when `status != "ok"`.
- Most uptime services (UptimeRobot, Better Stack, Render's own notifications)
  support a keyword/JSON-body assertion.

Without this, a future scraper break is invisible again — which is exactly how
the board reached 42 days stale.

## Reference — scraper health as of 2026-07-24

Verified live during the repair session:

| Source | Status |
|---|---|
| gaijinpot | fixed — needs full browser headers **and** warmed cookies (81 urls p1, 91 p2) |
| tokyodev | fixed — titles no longer in `<h2>`-`<h5>`; key off URL shape (156 jobs) |
| jobsinjapan | fixed — URLs moved to `/jobs/<id>/<slug>/`; anchored-regex pagination guard (33 urls) |
| japandev, yolojapan, careercross, jobspy, greenhouse, ashby, workable, salesforce, microsoft, rakuten | working |
| lever, smartrecruiters, recruitee | zero — config/coverage gap, not breakage |
| robertwalters | blocked — 403 to everything |
