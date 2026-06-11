# Data-trust & UX-debt pass — June 11, 2026

Scope honored: no redesign, no brand changes, no unrelated scraper edits.
Every inference added in this pass is conservative — blank beats a false claim.

## 1. Data improvements made

**English-level inference (`inference.infer_en_level`, rewritten).** Window-based
matching with a false-context guard: "English version / translation / page /
menu / available in English" never count. Recognizes explicit levels (Native,
Business, Conversational, Basic), generic "English required" → Business,
"English preferred" → Preferred, and "English not required" → Not Required.
Filled only **12 of 2,316** missing rows — by design. Spot-checked hits were
real explicit statements ("Japanese and English required" on an izakaya
posting). 10 unit tests, including 4 false-positive guards.

**Posting-language classifier (`inference.classify_posting_language`, new).**
Section-aware: evaluates title, requirements, and body separately, discounting
the last 25% of long descriptions where boilerplate/footers live. Five labels:
English / Japanese / **Bilingual** (new) / Mixed / Unknown. Rules implemented
exactly as specified: mostly-English requirements count strongly toward
English; footer-only English never flatters a Japanese posting (guarded even
in the Bilingual check); Japanese title+requirements → Japanese or Mixed.
Result on real data: the over-broad **Mixed bucket went 34 → 2**, with 51
postings correctly reclassified as Bilingual. Bilingual postings now earn
+15 fit (vs +20 for pure English) with a visible reason tag. 6 tests.

**Salary extraction (`salary_parser.extract_from_text`, new).** Anchored
patterns only — 年収/月給/時給/日給 forms, ¥xM–¥yM, ¥-prefixed full numbers
with an explicit period or annual magnitude, "salary: N – N yen", and
clearly-annual USD (converted at a rough ¥150, labeled inferred). Per-period
sanity bounds (annual ¥1.5M–100M, monthly ¥120K–3M, hourly ¥900–10K) plus a
false-context window (employees / users / revenue / founded / years of
experience all reject). Filled **24** rows; "competitive salary" stays blank.
10 tests.

## 2. Backfill counts (before → after)

| Metric | Before | After |
|---|---|---|
| english_level set | 249 | 261 (+12, all explicit statements) |
| salary set | 2,273 | 2,297 (+24 extracted) |
| posting=Mixed | 34 | 2 |
| posting=Bilingual | 0 | 51 |
| posting=English | 2,426 | 2,402 |
| rows with provenance | 0 | 2,565 (all) |
| fit scores updated | — | 91 (bilingual bonus + new data) |

Idempotency verified: an immediate second `backfill.py --dry-run` reports
**0 pending changes** on every target.

## 3. Provenance approach

Six nullable TEXT columns added via the existing safe ALTER-TABLE migration:
`visa_source`, `abroad_source`, `remote_source`, `japanese_level_source`,
`english_level_source`, `salary_source`, vocabulary
`explicit | inferred | not_stated`. Going forward, `db._derive_fields` stamps
provenance at write time (scraper-provided structured values → explicit;
anything our rules fill → inferred; nothing found → not_stated), and the
GaijinPot/YOLO scrapers pass their own source claims (e.g. GaijinPot's hidden
remote/overseas inputs → explicit; its text fallback → inferred). Existing
rows were backfilled from a per-source map of which scrapers provide which
fields structurally — current GaijinPot remote/overseas flags are honestly
marked `inferred` (limitation #2) and will flip to `explicit` on the next real
scrape automatically. Distribution sanity-checked (e.g. all visa flags are
`inferred` — none of our sources state sponsorship as structured data — while
2,260 Japanese levels are `explicit`).

**UI:** the job-detail "at a glance" grid shows a quiet sub-label under each
known value — "stated in posting", "inferred from posting text", or
"extracted from description" for salaries; unknowns keep their honest
"Not stated" treatment. Job cards stay clean: value only, no provenance chips.

## 4. Homepage sections removed / kept

Removed: the 5-stage "journey band" (→ replaced), the **6-card value-prop
grid**, the **8-card tools showcase**, 3 of 7 FAQ items, plus their dead CSS.
Replaced with: a 3-step "How it works" (Find jobs → Check fit → Track
applications) and one compact toolkit panel — a single featured resume-builder
block beside a plain link list of five tools/guides (no icon-card grid).
Kept: hero with the real top-3-ranked-jobs panel, 5-stat real-count trust
strip, featured jobs, 4-question FAQ, final CTA. All JSON-LD untouched.
Rendered height at 1440px is now ~3,000px (jobs page content unchanged).

## 5. Saved/applied performance fix

`/saved` and `/applied` previously fetched a page of results, post-filtered in
Python, and ran a second `limit=10_000` full-table query just to compute the
count. `_build_where` now takes `only_ids` and emits `WHERE id IN (…)`;
both `query_jobs` and `count_jobs` accept it and the route passes localStorage
IDs straight to SQL. Empty-state, filters and pagination behavior preserved
(verified: 3 ids → 3 cards, count 3; no ids → teaching empty state). Tests added.

## 6. Mobile screenshot findings (Playwright, real Chromium)

`screenshot_pass.py` (new) captures /, /jobs, /jobs?professional_only=1, a
real job detail, /profile, /tracker, /resume at 390/768/1440 into a
gitignored `screenshots/`, and asserts on horizontal overflow + console errors.

Findings: **a real bug** — every page had a 46px horizontal overflow at 390px,
caused by the off-canvas mobile drawer (`translateX(100%)`) extending the
scrollable area. Fixed with `html, body { overflow-x: clip }` (clip, not
hidden, so `position: sticky` keeps working). After the fix: zero overflow on
all 21 page/width combinations. Only remaining console message is the Google
Fonts request, blocked by this sandbox's network proxy — not an app issue.
Visual review of the PNGs: filters stack to one column at 390px, the glance
grid wraps to two columns, the sticky apply bar doesn't cover content, the
homepage reads hero → jobs → proof in two screens, tracker/resume forms usable.

## 7. Files changed

`inference.py` (en-level, posting language, bilingual fit bonus),
`salary_parser.py` (text extraction), `db.py` (provenance columns + derive
logic + `only_ids`), `app.py` (`only_ids` pass-through), `scraper.py` +
`yolojapan_scraper.py` (provenance claims only), `update.py` (`--backfill` →
backfill.py), `templates/job.html` (provenance labels),
`templates/landing.html` (shortened), `templates/base.html` (drawer order +
overflow fix), `test_app.py` (+31 checks).
New: `backfill.py`, `screenshot_pass.py`, `MAINTENANCE.md`, `screenshots/`
(gitignored). README updated.

## 8. Tests run and results

- `python test_app.py` — **91 checks, ALL PASS** (en-level incl. 4
  false-positive guards, posting-language incl. footer/bilingual cases, salary
  extraction incl. 4 must-reject cases, only_ids, provenance consistency, all
  routes). `python -m pytest -q` still trips a collection RecursionError on
  this FUSE mount (environment artifact, documented previously) — test_app.py
  remains the canonical runner and is plain-assert convertible.
- `python backfill.py --dry-run` / `--apply` — counts above; auto-backup
  written; second dry-run clean.
- Live-server GETs: all 14 routes from the brief → **200** (including the
  `?visa_support=1` / `?apply_from_abroad=1` aliases, which filter to 223/141).
- Screenshot pass: 21/21 captures, zero overflow, zero app console errors.

## 9. Remaining limitations

- JobSpy salary coverage improved by only 24 rows — most JobSpy descriptions
  genuinely contain no salary statement; correctly left blank.
- GaijinPot remote/overseas stay `inferred` until the next real scrape
  (the scraper now records `explicit` from the page's hidden inputs).
- USD conversion uses a fixed ¥150 and is marked inferred; a rate config would
  be nicer.
- `english_level` is still absent on ~90% of rows — that is the honest truth
  of the postings, now visible as "Not stated" rather than papered over.
- Provenance for pre-existing rows is source-level mapping, not per-row; rows
  re-scraped in future get exact per-row provenance.
- The pytest collection issue on FUSE mounts is unresolved (cosmetic; CI on a
  normal filesystem would not hit it).
