# Implementation report — June 11, 2026

## Summary

The audit found the app's UI already mature, but the underlying data badly broken in ways
that made the core foreigner-focused promises false. Three systemic data bugs were
corrupting filters, badges and ranking for ~85% of rows. This pass fixed the data layer,
re-scored everything, tightened ranking, added a professional-roles filter, made the
detail page answer the questions foreigners actually ask, and hardened the update pipeline.

## What was broken and why it mattered

1. **All 1,994 YOLO Japan jobs were flagged "Apply from abroad" + "visa support".**
   The scraper treated the boilerplate "Status of residence" header (present on ~every
   YOLO page; it means you usually need a visa *already*) as visa support, and then
   derived overseas-OK from it. The "Apply from abroad" filter — the single most
   important filter for overseas users — was 93% noise.

2. **All 174 GaijinPot jobs were flagged Remote + Apply-from-abroad.** The scraper
   searched the whole page text, and GaijinPot prints "Remote Work OK" / "Overseas
   Application OK" as *search-filter checkbox labels* on every page. The page actually
   embeds each job's true values as hidden form inputs — the scraper now reads those.

3. **90% of YOLO jobs were tagged `care_work` / "Healthcare / Care"** — including ramen
   shops, truck drivers and factory work — because the classifier matched keywords like
   "medical" and "hospital" against benefits boilerplate in the description. It now
   classifies from YOLO's structured Industry field first, title keywords second, and
   never from the description body.

4. Smaller issues: "relocation assistance" counted as visa sponsorship (now a separate
   signal); non-canonical language levels ('None', 'Fluent Japanese'); the source-quality
   map missing 8 of 14 sources (japandev/YOLO/ashby/etc. all "Unknown"); inflated fit
   scores ranking part-time service work above professional roles.

## Changes

### Data quality & normalization
- `yolojapan_scraper.py` — industry-first classification (new `_INDUSTRY_CATEGORY` map,
  title-only fallback), conservative explicit-language-only visa/overseas flags, two new
  role families (Construction / Trades, Agriculture / Fishery).
- `scraper.py` (GaijinPot) — remote/overseas/video flags now read from the page's hidden
  per-job inputs, falling back to inference over job content only (never page chrome).
- `inference.py` — stricter `infer_visa_sponsorship` (explicit-only positives, more
  negatives like "must have valid work visa"; relocation removed); complete source-quality
  map for all 14 sources (+ Recruiter tier); level canonicalization applied in
  `db._derive_fields` for every writer.
- `fix_data.py` (new) — one-pass repair of existing rows with automatic DB backup and
  `--dry-run`. Applied: 1,982 YOLO rows re-tagged, 1,591 role families corrected,
  2,167 false overseas/remote flags reset, 135 visa flags corrected, 19 levels
  normalized, all 2,565 fit scores recomputed.
  Result: Apply-from-abroad 1,994 → 141 (real), visa support → 223 (explicit only),
  remote → 237, care-work 1,802 → 290.

### Ranking
- `inference.py` — explicit "no visa sponsorship" now subtracts 10 points with a visible
  reason tag ("Explicitly no visa sponsorship") shown under Things to check.
- `db.py` — "Recommended" sort = Foreigner Fit plus small transparent adjustments:
  full-time +6, part-time/temp −8, salary disclosed +2, source trust 0–4. The jobs page
  now has a "how does this work?" explainer next to the result count.
- Outcome: the board's top is now curated full-time professional roles (engineering,
  data, consulting, ops) followed by solid full-time teaching, instead of mis-flagged
  part-time service listings.

### Search & filtering
- New **"Professional roles only"** filter (`professional_only=1`): excludes part-time /
  temporary / internship contracts and service / light-labor role families; unknowns pass
  through. Wired through db → app → UI checkbox, quick chip, active-filter chip, and a
  landing-page stat. All existing filters verified against actual DB values (canonical
  levels mean the "No Japanese required" chip now matches reality).

### Job detail page
- New **"at a glance" grid** answering the eight key questions directly — visa
  sponsorship, apply from abroad, Japanese required, English level, salary, work style,
  employment type, source — with honest "Not stated — ask" states for unknowns instead
  of silently hiding missing data.

### Landing page
- Stats strip now includes **Visa support** and **Professional roles** counts (both
  clickable presets); no-Japanese count query simplified to canonical values.

### Update pipeline
- `update.py` rewritten: `--dry-run`, `--limit N` (bounded runs), `--skip SOURCE`
  (repeatable), `--backfill` (runs fix_data), per-source timing + summary table,
  failures isolated per source, dry-run exits 0. Robots compliance unchanged.

### Content
- New resource: **/resources/applying-from-abroad** (realistic playbook: who hires from
  overseas, COE process, documents, remote interviews, 4–8-month timeline, checklist),
  added via `resources_new.py` so the giant content.py stays manageable. Auto-included
  in hub, sitemap and llms.txt.

### Tests
- `test_app.py` (new): 53 checks — visa/level/source inference, YOLO classification
  regression cases (ramen ≠ care work), filter correctness against the DB, recommended
  sort sanity, and 32 route smoke tests including bad-param handling. **All pass.**

## Files modified / added
Modified: `inference.py`, `yolojapan_scraper.py`, `scraper.py`, `db.py`, `app.py`,
`update.py`, `content.py` (3-line append), `templates/index.html`, `templates/job.html`,
`templates/landing.html`, `README.md`.
Added: `fix_data.py`, `resources_new.py`, `test_app.py`, `IMPLEMENTATION_REPORT.md`.
Database: repaired in place; backup at `jobs.db.bak_fix_<timestamp>`.

## Commands run
```
python fix_data.py --dry-run      # previewed changes
python fix_data.py                # applied (backup written first)
python test_app.py                # 53/53 pass
python app.py                     # manual checks on /, /jobs, filters, /job/<id>, resources
python update.py --only japandev --limit 2 --dry-run   # pipeline mechanics verified
```
Note: the scraper dry-run verified CLI plumbing, error isolation and the summary table;
actual network fetches were blocked by this sandbox's proxy and should be re-run locally.

## Remaining limitations / suggested next steps
- **jobspy rows (115) have no salary data** — the aggregator doesn't return it; consider
  enriching from description text or de-prioritizing further.
- GaijinPot remote/overseas backfill for *existing* rows used content inference (the
  hidden inputs are only available at scrape time); the next `python update.py` refresh
  will overwrite with exact values.
- `english_level` is missing on 90% of rows; an `infer_en_level` backfill pass over
  descriptions could close some of that, conservatively.
- The "Mixed" posting-language bucket is broad; a per-section ratio (requirements vs.
  boilerplate) would sharpen the english-friendliness signal.
- Consider a periodic `update.py --backfill` cron after scoring-rule changes.
