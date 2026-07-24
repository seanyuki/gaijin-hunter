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

## Step 2 — First manual production scrape

This is the gate `render.yaml` documents. Run from the Render **service shell**,
bounded first so a misbehaving source can't fill the disk:

```bash
python update.py --limit 25 --verbose
```

**Check — sane results.** In the output confirm:

- No `returned ZERO jobs` warnings for: gaijinpot, tokyodev, jobsinjapan,
  japandev, yolojapan, careercross, jobspy, greenhouse, ashby, workable,
  salesforce, microsoft, rakuten.
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

If that all holds, run a full pass and the data-quality backfill:

```bash
python update.py && python backfill.py --apply
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
