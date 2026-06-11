"""
SQLite layer for the Japan job board.

Single table `jobs`, deduplicated by `url` (unique). Schema mirrors the field set
GaijinPot exposes on its detail and search pages so we can support the same
filtering and display them faithfully. `init_db()` runs `migrate()`, which adds
any missing columns to existing databases via ALTER TABLE.
"""

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Optional

import inference

# Default DB location; override with JAPAN_JOBS_DB env var or by reassigning DB_PATH.
DB_PATH = Path(os.environ.get("JAPAN_JOBS_DB", Path(__file__).parent / "jobs.db"))


def _resolve(db_path: Optional[Path]) -> Path:
    """Resolve the DB path, deferring to the module-level DB_PATH when not given."""
    return Path(db_path) if db_path is not None else DB_PATH


# Each entry is (column_name, sql_type [+ defaults]).
# Order in this list is the canonical column order used by SELECT queries.
COLUMNS: list[tuple[str, str]] = [
    # Identity
    ("source",                     "TEXT    NOT NULL"),
    ("source_job_id",              "TEXT"),                 # e.g. GaijinPot job id 158635
    ("url",                        "TEXT    NOT NULL UNIQUE"),
    # Headline
    ("title",                      "TEXT    NOT NULL"),
    ("company_name",               "TEXT"),
    ("company_name_jp",            "TEXT"),
    ("location",                   "TEXT"),
    # Classification
    ("industries",                 "TEXT"),
    ("function",                   "TEXT"),
    ("work_type",                  "TEXT"),                 # e.g. "Part Time / Experienced (Non-Manager)"
    ("career_level",               "TEXT"),                 # derived from work_type
    ("employment_terms",           "TEXT"),                 # Full-time / Part-time / Contract
    ("employer_type",              "TEXT"),
    # Compensation
    ("salary",                     "TEXT"),
    ("salary_period",              "TEXT"),                 # Year / Month / Lesson / Hour
    ("salary_perks",               "TEXT"),                 # bullets after salary
    ("salary_min_jpy",             "INTEGER"),              # parsed minimum in JPY
    ("salary_max_jpy",             "INTEGER"),              # parsed maximum in JPY
    ("salary_min_annual_jpy",      "INTEGER"),              # min annualized for sort/filter
    ("salary_max_annual_jpy",      "INTEGER"),              # max annualized for sort/filter
    # Language requirements
    ("english_level",              "TEXT"),
    ("japanese_level",             "TEXT"),
    ("other_language",             "TEXT"),
    # Flags (0/1; nullable so we can distinguish "unknown")
    ("remote_work_ok",             "INTEGER"),
    ("overseas_application_ok",    "INTEGER"),
    ("has_video_presentation",     "INTEGER"),
    # Body
    ("requirements",               "TEXT"),                 # raw bullet list
    ("description",                "TEXT"),
    ("tags",                       "TEXT"),
    # Dates
    ("post_date",                  "TEXT"),                 # ISO date when parseable
    ("last_modified_date",         "TEXT"),
    # Company sidebar
    ("company_year_founded",       "TEXT"),
    ("company_size",               "TEXT"),                 # e.g. "21-50"
    ("company_about",              "TEXT"),
    # ===== Phase-1 enrichment fields (auto-derived in upsert_job) =====
    ("role_family",                "TEXT"),                 # Software Engineering / Teaching / …
    ("prefecture",                 "TEXT"),                 # canonical prefecture (normalized from location)
    ("region",                     "TEXT"),                 # Kanto / Kansai / … (derived from prefecture)
    ("posting_language",           "TEXT"),                 # English / Mixed / Japanese / Unknown
    ("english_ratio",              "REAL"),                 # 0.0–1.0
    ("data_quality_score",         "INTEGER"),              # 0–100
    ("foreigner_fit_score",        "INTEGER"),              # 0–100
    ("foreigner_fit_reasons",      "TEXT"),                 # comma-separated tags
    ("source_quality",             "TEXT"),                 # Direct ATS / Curated / Job board / Aggregator
    ("visa_sponsorship_mentioned", "INTEGER"),              # 0/1
    ("relocation_support_mentioned","INTEGER"),             # 0/1

    # ===== Field provenance (data-trust layer) =====
    # 'explicit'  — the source stated it as structured data
    # 'inferred'  — derived from posting text by our conservative rules
    # 'not_stated'— we looked and found nothing
    ("visa_source",                "TEXT"),
    ("abroad_source",              "TEXT"),
    ("remote_source",              "TEXT"),
    ("japanese_level_source",      "TEXT"),
    ("english_level_source",       "TEXT"),
    ("salary_source",              "TEXT"),

    # ===== Employer-direct posting fields =====
    # If is_employer_post=1, this row was created via the /post-a-job form,
    # not by a scraper. Direct-from-employer postings have a 45-day expiry,
    # a self-management token, and a contact email for the poster.
    ("is_employer_post",           "INTEGER NOT NULL DEFAULT 0"),
    ("employer_contact_email",     "TEXT"),                 # poster's email
    ("employer_contact_name",      "TEXT"),                 # poster's name
    ("employer_manage_token",      "TEXT"),                 # random hex for /employer/manage/<token>
    ("application_url",            "TEXT"),                 # where to apply (may differ from 'url')
    ("application_email",          "TEXT"),                 # apply-by-email address (optional)
    ("expires_at",                 "TEXT"),                 # ISO datetime when post expires
    ("moderation_status",          "TEXT    DEFAULT 'approved'"),  # approved / pending / rejected
    ("employer_post_status",       "TEXT    DEFAULT 'active'"),    # active / withdrawn / expired

    # Bookkeeping
    ("scraped_at",                 "TEXT    NOT NULL"),
    ("last_seen_at",               "TEXT    NOT NULL"),
]

CREATE_SQL = (
    "CREATE TABLE IF NOT EXISTS jobs (\n  "
    "id INTEGER PRIMARY KEY AUTOINCREMENT,\n  "
    + ",\n  ".join(f"{name:<26} {ddl}" for name, ddl in COLUMNS)
    + "\n)"
)

INDEXES_SQL = """
CREATE INDEX IF NOT EXISTS idx_jobs_source              ON jobs(source);
CREATE INDEX IF NOT EXISTS idx_jobs_japanese_level      ON jobs(japanese_level);
CREATE INDEX IF NOT EXISTS idx_jobs_english_level       ON jobs(english_level);
CREATE INDEX IF NOT EXISTS idx_jobs_location            ON jobs(location);
CREATE INDEX IF NOT EXISTS idx_jobs_employment_terms    ON jobs(employment_terms);
CREATE INDEX IF NOT EXISTS idx_jobs_industries          ON jobs(industries);
CREATE INDEX IF NOT EXISTS idx_jobs_remote_work_ok      ON jobs(remote_work_ok);
CREATE INDEX IF NOT EXISTS idx_jobs_last_seen_at        ON jobs(last_seen_at);
CREATE INDEX IF NOT EXISTS idx_jobs_foreigner_fit        ON jobs(foreigner_fit_score);
CREATE INDEX IF NOT EXISTS idx_jobs_role_family          ON jobs(role_family);
CREATE INDEX IF NOT EXISTS idx_jobs_prefecture           ON jobs(prefecture);
CREATE INDEX IF NOT EXISTS idx_jobs_region               ON jobs(region);
CREATE INDEX IF NOT EXISTS idx_jobs_posting_language     ON jobs(posting_language);
CREATE INDEX IF NOT EXISTS idx_jobs_source_quality       ON jobs(source_quality);
CREATE INDEX IF NOT EXISTS idx_jobs_is_employer_post      ON jobs(is_employer_post);
CREATE INDEX IF NOT EXISTS idx_jobs_expires_at            ON jobs(expires_at);
CREATE INDEX IF NOT EXISTS idx_jobs_manage_token          ON jobs(employer_manage_token);
CREATE INDEX IF NOT EXISTS idx_jobs_employer_post_status  ON jobs(employer_post_status);
"""


@contextmanager
def connect(db_path: Optional[Path] = None):
    # timeout lets writers wait out a brief lock instead of erroring immediately.
    conn = sqlite3.connect(_resolve(db_path), timeout=30)
    conn.row_factory = sqlite3.Row
    # WAL is more robust than the default rollback journal on networked / FUSE
    # mounts, which can otherwise raise "disk I/O error" on journal fsync.
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=30000")
    except sqlite3.OperationalError:
        pass
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


NEWSLETTER_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS newsletter_subscribers (
  id                 INTEGER PRIMARY KEY AUTOINCREMENT,
  email              TEXT    NOT NULL UNIQUE,
  role_families      TEXT,
  salary_min         INTEGER,
  preferred_locations TEXT,
  unsubscribed       INTEGER NOT NULL DEFAULT 0,
  created_at         TEXT    NOT NULL,
  unsubscribed_at    TEXT,
  token              TEXT    NOT NULL UNIQUE
);
CREATE INDEX IF NOT EXISTS idx_newsletter_unsubscribed
  ON newsletter_subscribers(unsubscribed);
"""


def init_db(db_path: Optional[Path] = None) -> None:
    with connect(db_path) as conn:
        conn.execute(CREATE_SQL)
        # Migrate before indexes — indexes reference columns added by migration.
        migrate(conn)
        conn.executescript(INDEXES_SQL)
        conn.executescript(NEWSLETTER_TABLE_SQL)


def migrate(conn: sqlite3.Connection) -> list[str]:
    """Add any columns from COLUMNS that are missing in an existing jobs table."""
    existing = {row["name"] for row in conn.execute("PRAGMA table_info(jobs)")}
    added = []
    for name, ddl in COLUMNS:
        if name not in existing:
            conn.execute(f"ALTER TABLE jobs ADD COLUMN {name} {ddl}")
            added.append(name)
    return added


# All fields a scraper writes (everything except autoincrement id).
_WRITE_FIELDS = [name for name, _ in COLUMNS]


def _derive_fields(job: dict) -> None:
    """
    Compute Phase-1 fit/quality fields IN PLACE on the job dict so every
    scraper benefits without code changes. Callers can pre-populate any of
    these to override (e.g. a scraper that has structured visa data).
    """
    title = job.get("title")
    desc = job.get("description")
    body_text = " ".join(filter(None, [
        title, desc, job.get("requirements"), job.get("salary_perks"),
    ]))

    # Canonicalize language-level labels so filters see one vocabulary
    # ('None' -> 'Not Required', 'Fluent Japanese' -> 'Native / Fluent', …).
    for _col in ("japanese_level", "english_level"):
        if job.get(_col):
            job[_col] = inference.normalize_level_label(job[_col])

    # ---- Provenance: language levels -----------------------------------
    # A scraper-provided value without a source claim is treated as explicit
    # (structured field on the source page). Anything WE fill in is inferred.
    if job.get("japanese_level"):
        job["japanese_level_source"] = job.get("japanese_level_source") or "explicit"
    else:
        job["japanese_level_source"] = "not_stated"
    if job.get("english_level") is None:
        en = inference.infer_en_level(body_text)
        if en:
            job["english_level"] = en
            job["english_level_source"] = "inferred"
        else:
            job["english_level_source"] = "not_stated"
    else:
        job["english_level_source"] = job.get("english_level_source") or "explicit"

    # ---- Provenance: salary (+ conservative free-text extraction) ------
    has_salary = bool((job.get("salary") or "").strip() or job.get("salary_min_jpy")
                      or job.get("salary_min_annual_jpy"))
    if has_salary:
        job["salary_source"] = job.get("salary_source") or "explicit"
    else:
        import salary_parser as _sp
        found = _sp.extract_from_text(body_text)
        if found:
            for k, v in found.items():
                if job.get(k) in (None, ""):
                    job[k] = v
            job["salary_source"] = "inferred"
        else:
            job["salary_source"] = "not_stated"

    # ---- Provenance: remote / abroad ------------------------------------
    for _col, _src in (("remote_work_ok", "remote_source"),
                       ("overseas_application_ok", "abroad_source")):
        if job.get(_col) is not None:
            job[_src] = job.get(_src) or "explicit"
        else:
            job[_src] = "not_stated"

    if job.get("role_family") is None:
        job["role_family"] = inference.classify_role_family(title, desc)

    if job.get("prefecture") is None:
        job["prefecture"] = inference.normalize_prefecture(job.get("location"))
    if job.get("region") is None:
        job["region"] = inference.region_for_prefecture(job.get("prefecture"))

    if job.get("posting_language") is None:
        job["posting_language"] = inference.classify_posting_language(
            title, desc, job.get("requirements"))

    if job.get("english_ratio") is None:
        combined = (title or "") + "  " + (desc or "")
        job["english_ratio"] = inference.english_ratio(combined)

    if job.get("source_quality") is None:
        job["source_quality"] = inference.source_quality(job.get("source"))

    if job.get("visa_sponsorship_mentioned") is None:
        v = inference.infer_visa_support(body_text)
        if v is not None:
            job["visa_sponsorship_mentioned"] = v
            job["visa_source"] = "inferred"
        else:
            job["visa_source"] = "not_stated"
    else:
        job["visa_source"] = job.get("visa_source") or "explicit"

    if job.get("relocation_support_mentioned") is None:
        r = inference.infer_relocation_support(body_text)
        if r is not None:
            job["relocation_support_mentioned"] = r

    if job.get("data_quality_score") is None:
        job["data_quality_score"] = inference.calculate_data_quality(job)

    if job.get("foreigner_fit_score") is None:
        score, reasons = inference.calculate_foreigner_fit(job)
        job["foreigner_fit_score"] = score
        job["foreigner_fit_reasons"] = ",".join(reasons) if reasons else None


def upsert_job(conn: sqlite3.Connection, job: dict) -> str:
    """
    Insert a new job or update an existing one (keyed on url).
    Returns 'inserted' or 'updated'.
    Auto-derives role_family / posting_language / fit scores etc.
    """
    _derive_fields(job)
    existing = conn.execute("SELECT id FROM jobs WHERE url = ?", (job["url"],)).fetchone()
    if existing:
        # Update everything except scraped_at (preserve first-seen timestamp).
        update_fields = [f for f in _WRITE_FIELDS if f != "scraped_at"]
        set_clause = ", ".join(f"{f} = ?" for f in update_fields)
        values = [job.get(f) for f in update_fields]
        values.append(job["url"])
        conn.execute(f"UPDATE jobs SET {set_clause} WHERE url = ?", values)
        return "updated"
    cols = ", ".join(_WRITE_FIELDS)
    placeholders = ", ".join("?" for _ in _WRITE_FIELDS)
    values = [job.get(f) for f in _WRITE_FIELDS]
    conn.execute(f"INSERT INTO jobs ({cols}) VALUES ({placeholders})", values)
    return "inserted"


def backfill_derived_fields(db_path: Optional[Path] = None,
                            only_missing: bool = True) -> int:
    """
    Recompute role_family / posting_language / fit scores for existing rows.
    Pass only_missing=False to recompute everything (useful after changing
    inference rules).
    Returns the number of rows updated.
    """
    with connect(db_path) as conn:
        if only_missing:
            rows = conn.execute(
                "SELECT * FROM jobs WHERE foreigner_fit_score IS NULL"
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM jobs").fetchall()

        n = 0
        for row in rows:
            job = dict(row)
            # Clear derived fields so _derive_fields recomputes
            for k in ("role_family", "prefecture", "region", "posting_language",
                      "english_ratio", "data_quality_score", "foreigner_fit_score",
                      "foreigner_fit_reasons", "source_quality",
                      "visa_sponsorship_mentioned",
                      "relocation_support_mentioned"):
                if not only_missing:
                    job[k] = None
            _derive_fields(job)
            conn.execute(
                "UPDATE jobs SET role_family=?, prefecture=?, region=?, "
                "posting_language=?, "
                "english_ratio=?, data_quality_score=?, "
                "foreigner_fit_score=?, foreigner_fit_reasons=?, "
                "source_quality=?, visa_sponsorship_mentioned=?, "
                "relocation_support_mentioned=? WHERE id=?",
                (
                    job.get("role_family"),
                    job.get("prefecture"),
                    job.get("region"),
                    job.get("posting_language"),
                    job.get("english_ratio"),
                    job.get("data_quality_score"),
                    job.get("foreigner_fit_score"),
                    job.get("foreigner_fit_reasons"),
                    job.get("source_quality"),
                    job.get("visa_sponsorship_mentioned"),
                    job.get("relocation_support_mentioned"),
                    row["id"],
                )
            )
            n += 1
    return n


# ---------------------------------------------------------------------------
# Read API used by the Flask app
# ---------------------------------------------------------------------------

# Columns the UI is allowed to filter on. Keep this in sync with the index form.
FILTERABLE_TEXT = {
    "japanese_level", "english_level", "other_language",
    "industries", "function", "work_type", "career_level",
    "employment_terms", "employer_type", "location", "source",
    "tags",
    # Phase 1 derived fields
    "role_family", "posting_language", "source_quality",
    # Normalized geography
    "prefecture", "region",
}
FILTERABLE_FLAG = {"remote_work_ok", "overseas_application_ok",
                   "has_video_presentation",
                   "visa_sponsorship_mentioned", "relocation_support_mentioned"}


# Sentinel a filter value can include to also match NULL/empty rows.
UNDISCLOSED = "__undisclosed__"

# Columns that use LIKE matching (substring) instead of exact equality.
LIKE_COLUMNS = {"location", "industries", "function", "tags"}

# A job whose last_seen_at is older than this is considered archived
# (probably no longer listed at source).
STALE_DAYS = 30

# Recommended ranking = Foreigner Fit score plus small, transparent
# adjustments (each one is also visible on the job card so users can see WHY
# something ranks). Kept deliberately small relative to the 0-100 fit score:
#   +6 full-time professional commitment   -8 part-time/temp/dispatch
#   +2 salary disclosed                    +0..4 source trust tier
_RECOMMENDED_SCORE_SQL = (
    "(COALESCE(foreigner_fit_score, 0)"
    " + CASE WHEN employment_terms = 'Full-time' THEN 6 ELSE 0 END"
    " - CASE WHEN employment_terms IN ('Part-time', 'Temporary') THEN 8 ELSE 0 END"
    " + CASE WHEN COALESCE(salary_min_annual_jpy, salary_max_annual_jpy) IS NOT NULL THEN 2 ELSE 0 END"
    " + CASE COALESCE(source_quality, 'Unknown')"
    "     WHEN 'Direct ATS' THEN 4 WHEN 'Direct from employer' THEN 4"
    "     WHEN 'Curated' THEN 3 WHEN 'Recruiter' THEN 2"
    "     WHEN 'Job board' THEN 1 ELSE 0 END"
    ")"
)

# Sort options the UI exposes. Keep these aligned with the dropdown.
SORT_OPTIONS = {
    # The default: foreigner-fit plus the adjustments above, freshness tiebreak.
    # This is what foreigners should see first.
    "recommended": (
        f"{_RECOMMENDED_SCORE_SQL} DESC, "
        "COALESCE(data_quality_score, 0) DESC, "
        "COALESCE(post_date, scraped_at) DESC"
    ),
    "fit":         "COALESCE(foreigner_fit_score, 0) DESC, "
                   "COALESCE(post_date, scraped_at) DESC",
    "newest":      "COALESCE(post_date, scraped_at) DESC",
    "oldest":      "COALESCE(post_date, scraped_at) ASC",
    "salary_desc": "COALESCE(salary_max_annual_jpy, salary_min_annual_jpy, 0) DESC, "
                   "COALESCE(post_date, scraped_at) DESC",
    "salary_asc":  "COALESCE(salary_min_annual_jpy, salary_max_annual_jpy, 99999999999) ASC, "
                   "COALESCE(post_date, scraped_at) DESC",
    "title":       "title COLLATE NOCASE ASC",
}
DEFAULT_SORT = "recommended"

# Role families flagged as "teaching" — used by the exclude_teaching filter.
TEACHING_ROLE_FAMILIES = ("Teaching / Education",)

# Service / light-labor families — excluded by the professional_only filter.
# These are real jobs (and stay fully searchable), but they're not what a
# bilingual professional means by "career role".
SERVICE_ROLE_FAMILIES = (
    "Hospitality / Service", "Retail / Sales", "Logistics / Manufacturing",
    "Healthcare / Care", "Construction / Trades", "Agriculture / Fishery",
)


def _build_where(
    q: Optional[str],
    filters: dict,
    flags: dict,
    salary_min: Optional[int],
    days_within: Optional[int],
    include_archived: bool,
    include_only_archived: bool,
    foreigner_fit_min: Optional[int] = None,
    exclude_teaching: bool = False,
    exclude_japanese_only: bool = False,
    salary_listed_only: bool = False,
    professional_only: bool = False,
    only_ids: Optional[list] = None,
) -> tuple[str, list]:
    clauses, params = [], []

    # Restrict to an explicit ID set (used by /saved and /applied, whose IDs
    # come from the visitor's localStorage). This keeps those pages from
    # scanning the whole table just to render a handful of rows.
    if only_ids is not None:
        ids = [int(i) for i in only_ids]
        if not ids:
            clauses.append("0 = 1")
        else:
            placeholders = ",".join("?" for _ in ids)
            clauses.append(f"id IN ({placeholders})")
            params.extend(ids)

    if q:
        clauses.append(
            "(title LIKE ? OR company_name LIKE ? OR description LIKE ? OR requirements LIKE ?)"
        )
        like = f"%{q}%"
        params.extend([like, like, like, like])

    for col, vals in (filters or {}).items():
        if col not in FILTERABLE_TEXT:
            continue
        if isinstance(vals, str):
            vals = [vals]
        vals = [v for v in (vals or []) if v is not None and str(v).strip() != ""]
        if not vals:
            continue
        include_null = UNDISCLOSED in vals
        concrete = [v for v in vals if v != UNDISCLOSED]
        parts = []
        if concrete:
            if col in LIKE_COLUMNS:
                parts.append("(" + " OR ".join(f"{col} LIKE ?" for _ in concrete) + ")")
                params.extend(f"%{v}%" for v in concrete)
            else:
                placeholders = ",".join("?" for _ in concrete)
                parts.append(f"{col} IN ({placeholders})")
                params.extend(concrete)
        if include_null:
            parts.append(f"({col} IS NULL OR {col} = '')")
        if parts:
            clauses.append("(" + " OR ".join(parts) + ")")

    for col, on in (flags or {}).items():
        if col in FILTERABLE_FLAG and on:
            clauses.append(f"{col} = 1")

    if salary_min:
        # A job matches if its TOP salary at least clears the user's floor.
        clauses.append("COALESCE(salary_max_annual_jpy, salary_min_annual_jpy) >= ?")
        params.append(int(salary_min))

    if days_within:
        # post_date is ISO YYYY-MM-DD when known; fall back to scraped_at.
        clauses.append(
            "DATE(COALESCE(post_date, scraped_at)) >= DATE('now', ?)"
        )
        params.append(f"-{int(days_within)} days")

    # Archive handling
    if include_only_archived:
        clauses.append("DATE(last_seen_at) < DATE('now', ?)")
        params.append(f"-{STALE_DAYS} days")
    elif not include_archived:
        clauses.append("DATE(last_seen_at) >= DATE('now', ?)")
        params.append(f"-{STALE_DAYS} days")

    # Employer-direct postings: filter out expired, withdrawn, or unmoderated rows.
    # Non-employer rows (is_employer_post=0) are always visible (subject to the
    # archive rule above).
    clauses.append(
        "("
          "is_employer_post = 0 "
          "OR ("
            "is_employer_post = 1 "
            "AND COALESCE(employer_post_status, 'active') = 'active' "
            "AND COALESCE(moderation_status, 'approved') = 'approved' "
            "AND (expires_at IS NULL OR datetime(expires_at) > datetime('now'))"
          ")"
        ")"
    )

    # Phase 1 filters
    if foreigner_fit_min is not None:
        clauses.append("COALESCE(foreigner_fit_score, 0) >= ?")
        params.append(int(foreigner_fit_min))

    if exclude_teaching:
        placeholders = ",".join("?" for _ in TEACHING_ROLE_FAMILIES)
        clauses.append(
            f"(role_family IS NULL OR role_family NOT IN ({placeholders}))"
        )
        params.extend(TEACHING_ROLE_FAMILIES)

    if exclude_japanese_only:
        clauses.append("(posting_language IS NULL OR posting_language != 'Japanese')")

    if salary_listed_only:
        clauses.append(
            "(salary_min_annual_jpy IS NOT NULL OR "
            "(salary IS NOT NULL AND salary != '' AND salary != 'Negotiable, based on experience'))"
        )

    if professional_only:
        # Career-track positions: no part-time / temp / dispatch contracts, and
        # no service / light-labor role families. Unknown values pass through —
        # the goal is removing obvious non-professional listings, not guessing.
        clauses.append(
            "COALESCE(employment_terms, '') NOT IN ('Part-time', 'Temporary', 'Internship')"
        )
        placeholders = ",".join("?" for _ in SERVICE_ROLE_FAMILIES)
        clauses.append(
            f"(role_family IS NULL OR role_family NOT IN ({placeholders}))"
        )
        params.extend(SERVICE_ROLE_FAMILIES)

    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    return where, params


def query_jobs(
    q: Optional[str] = None,
    filters: Optional[dict] = None,
    flags: Optional[dict] = None,
    salary_min: Optional[int] = None,
    days_within: Optional[int] = None,
    sort: str = DEFAULT_SORT,
    include_archived: bool = False,
    include_only_archived: bool = False,
    foreigner_fit_min: Optional[int] = None,
    exclude_teaching: bool = False,
    exclude_japanese_only: bool = False,
    salary_listed_only: bool = False,
    professional_only: bool = False,
    only_ids: Optional[list] = None,
    limit: int = 25,
    offset: int = 0,
) -> list[sqlite3.Row]:
    """
    q             : free-text LIKE across title, company, description, requirements.
    filters       : {column: [values]} multi-select, OR within col, AND across cols.
                    UNDISCLOSED value also matches NULL/empty.
    flags         : {column: True} for boolean checkbox filters.
    salary_min    : Minimum annualized JPY; a job matches if its max-annual >= this.
    days_within   : Posted within N days.
    sort          : Key from SORT_OPTIONS.
    include_archived : If False (default) exclude jobs not seen in STALE_DAYS days.
    include_only_archived : If True return ONLY archived (for the /archived view).
    """
    where, params = _build_where(
        q, filters or {}, flags or {}, salary_min, days_within,
        include_archived, include_only_archived,
        foreigner_fit_min=foreigner_fit_min,
        exclude_teaching=exclude_teaching,
        exclude_japanese_only=exclude_japanese_only,
        salary_listed_only=salary_listed_only,
        professional_only=professional_only,
        only_ids=only_ids,
    )
    order = SORT_OPTIONS.get(sort, SORT_OPTIONS[DEFAULT_SORT])
    sql = f"SELECT * FROM jobs {where} ORDER BY {order} LIMIT ? OFFSET ?"
    with connect() as conn:
        return conn.execute(sql, params + [limit, offset]).fetchall()


def count_jobs(
    q: Optional[str] = None,
    filters: Optional[dict] = None,
    flags: Optional[dict] = None,
    salary_min: Optional[int] = None,
    days_within: Optional[int] = None,
    include_archived: bool = False,
    include_only_archived: bool = False,
    foreigner_fit_min: Optional[int] = None,
    exclude_teaching: bool = False,
    exclude_japanese_only: bool = False,
    salary_listed_only: bool = False,
    professional_only: bool = False,
    only_ids: Optional[list] = None,
) -> int:
    """Total matching rows (for pagination summary)."""
    where, params = _build_where(
        q, filters or {}, flags or {}, salary_min, days_within,
        include_archived, include_only_archived,
        foreigner_fit_min=foreigner_fit_min,
        exclude_teaching=exclude_teaching,
        exclude_japanese_only=exclude_japanese_only,
        salary_listed_only=salary_listed_only,
        professional_only=professional_only,
        only_ids=only_ids,
    )
    sql = f"SELECT COUNT(*) AS n FROM jobs {where}"
    with connect() as conn:
        return conn.execute(sql, params).fetchone()["n"]


def counts_for(
    column: str,
    q: Optional[str] = None,
    filters: Optional[dict] = None,
    flags: Optional[dict] = None,
    salary_min: Optional[int] = None,
    days_within: Optional[int] = None,
    include_archived: bool = False,
) -> dict[str, int]:
    """
    Return {value: count} for the distinct values of `column`, respecting the
    current other-filter context EXCEPT the filter on this column itself.
    Used to render filter-dropdown counts like 'Senior (47)'.
    """
    if column not in FILTERABLE_TEXT:
        raise ValueError(f"counts_for() not allowed on column {column!r}")
    # Strip self-filter so options don't all collapse to currently-selected.
    other_filters = {k: v for k, v in (filters or {}).items() if k != column}
    where, params = _build_where(q, other_filters, flags or {}, salary_min,
                                 days_within, include_archived, False)
    # Add the non-null filter; group by column.
    extra = f"{'AND' if where else 'WHERE'} {column} IS NOT NULL AND {column} != ''"
    sql = (
        f"SELECT {column} AS v, COUNT(*) AS n FROM jobs {where} {extra} "
        f"GROUP BY {column}"
    )
    with connect() as conn:
        return {r["v"]: r["n"] for r in conn.execute(sql, params).fetchall()}


def counts_bulk(
    columns: list,
    q: Optional[str] = None,
    filters: Optional[dict] = None,
    flags: Optional[dict] = None,
    salary_min: Optional[int] = None,
    days_within: Optional[int] = None,
    include_archived: bool = False,
) -> dict[str, dict[str, int]]:
    """counts_for() for many UNFILTERED columns in a single table scan.

    Valid only for columns that have no active self-filter (their no-self
    context equals the shared context). The /jobs page uses this for the
    common case — 10 separate GROUP BY queries collapse into one SELECT.
    """
    cols = [c for c in columns if c in FILTERABLE_TEXT]
    if not cols:
        return {}
    where, params = _build_where(q, filters or {}, flags or {}, salary_min,
                                 days_within, include_archived, False)
    sql = f"SELECT {', '.join(cols)} FROM jobs {where}"
    out: dict[str, dict[str, int]] = {c: {} for c in cols}
    with connect() as conn:
        for row in conn.execute(sql, params):
            for c in cols:
                v = row[c]
                if v is not None and v != "":
                    out[c][v] = out[c].get(v, 0) + 1
    return out


def get_job(job_id: int) -> Optional[sqlite3.Row]:
    with connect() as conn:
        return conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()


def stats() -> dict:
    with connect() as conn:
        total = conn.execute("SELECT COUNT(*) AS n FROM jobs").fetchone()["n"]
        by_source = conn.execute(
            "SELECT source, COUNT(*) AS n FROM jobs GROUP BY source"
        ).fetchall()
        return {
            "total": total,
            "by_source": {r["source"]: r["n"] for r in by_source},
        }


def distinct(column: str) -> list[str]:
    """Distinct non-null values for a filter dropdown."""
    if column not in FILTERABLE_TEXT:
        raise ValueError(f"distinct() not allowed on column {column!r}")
    with connect() as conn:
        rows = conn.execute(
            f"SELECT DISTINCT {column} AS v FROM jobs "
            f"WHERE {column} IS NOT NULL AND {column} != '' ORDER BY v"
        ).fetchall()
    return [r["v"] for r in rows]


# ---------------------------------------------------------------------------
# Newsletter subscriptions  (Phase 5)
# ---------------------------------------------------------------------------

def newsletter_subscribe(email: str,
                         role_families: Optional[list[str]] = None,
                         salary_min: Optional[int] = None,
                         preferred_locations: Optional[list[str]] = None,
                         db_path: Optional[Path] = None) -> tuple[bool, str]:
    """
    Insert or re-activate a subscriber. Returns (ok, token_or_error).
    The token is a per-subscriber secret used in unsubscribe links so we
    never put the raw email in a query string.
    """
    import secrets
    from datetime import datetime, timezone
    email = (email or "").strip().lower()
    if not email or "@" not in email or len(email) > 200:
        return False, "Please enter a valid email."

    with connect(db_path) as conn:
        # Ensure table exists (covers fresh DBs that pre-date this migration).
        conn.executescript(NEWSLETTER_TABLE_SQL)
        now = datetime.now(timezone.utc).isoformat()
        existing = conn.execute(
            "SELECT id, token FROM newsletter_subscribers WHERE email = ?",
            (email,),
        ).fetchone()
        if existing:
            # Re-activate if previously unsubscribed; update preferences either way.
            conn.execute(
                "UPDATE newsletter_subscribers SET "
                "  role_families = ?, salary_min = ?, preferred_locations = ?, "
                "  unsubscribed = 0, unsubscribed_at = NULL "
                "WHERE id = ?",
                (
                    ",".join(role_families) if role_families else None,
                    salary_min,
                    ",".join(preferred_locations) if preferred_locations else None,
                    existing["id"],
                ),
            )
            return True, existing["token"]
        token = secrets.token_urlsafe(24)
        conn.execute(
            "INSERT INTO newsletter_subscribers "
            "(email, role_families, salary_min, preferred_locations, "
            " unsubscribed, created_at, token) "
            "VALUES (?, ?, ?, ?, 0, ?, ?)",
            (
                email,
                ",".join(role_families) if role_families else None,
                salary_min,
                ",".join(preferred_locations) if preferred_locations else None,
                now,
                token,
            ),
        )
        return True, token


def newsletter_unsubscribe(token: str, db_path: Optional[Path] = None) -> bool:
    from datetime import datetime, timezone
    if not token:
        return False
    with connect(db_path) as conn:
        conn.executescript(NEWSLETTER_TABLE_SQL)
        now = datetime.now(timezone.utc).isoformat()
        cur = conn.execute(
            "UPDATE newsletter_subscribers "
            "SET unsubscribed = 1, unsubscribed_at = ? "
            "WHERE token = ? AND unsubscribed = 0",
            (now, token),
        )
        return cur.rowcount > 0


def newsletter_stats(db_path: Optional[Path] = None) -> dict:
    with connect(db_path) as conn:
        conn.executescript(NEWSLETTER_TABLE_SQL)
        active = conn.execute(
            "SELECT COUNT(*) AS n FROM newsletter_subscribers WHERE unsubscribed = 0"
        ).fetchone()["n"]
        total = conn.execute(
            "SELECT COUNT(*) AS n FROM newsletter_subscribers"
        ).fetchone()["n"]
        return {"active": active, "total": total}


# ---------------------------------------------------------------------------
# Salary benchmarking
# ---------------------------------------------------------------------------

_BENCH_MIN_SAMPLE = 5


def _percentile(sorted_vals: list, p: float) -> float:
    """Linear-interpolated percentile of a pre-sorted list (p in 0..1)."""
    if not sorted_vals:
        return 0.0
    if len(sorted_vals) == 1:
        return float(sorted_vals[0])
    k = (len(sorted_vals) - 1) * p
    lo = int(k)
    hi = min(lo + 1, len(sorted_vals) - 1)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (k - lo)


def salary_benchmarks(db_path: Optional[Path] = None) -> dict:
    """Live salary distribution per role_family from active, salaried postings.

    Returns { role_family: {n, p10, p25, p50, p75, p90, mid_avg} }, using each
    job's salary midpoint so wide bands don't skew the distribution. Roles with
    fewer than _BENCH_MIN_SAMPLE samples are omitted.
    """
    out: dict = {}
    with connect(db_path) as conn:
        rows = conn.execute(
            "SELECT role_family, salary_min_annual_jpy AS mn, "
            "       salary_max_annual_jpy AS mx "
            "FROM jobs "
            "WHERE salary_min_annual_jpy IS NOT NULL AND salary_min_annual_jpy > 0 "
            "  AND role_family IS NOT NULL "
            "  AND DATE(last_seen_at) >= DATE('now', ?)",
            (f"-{STALE_DAYS} days",),
        ).fetchall()
    buckets: dict = {}
    for r in rows:
        mn = r["mn"]
        mx = r["mx"] or mn
        buckets.setdefault(r["role_family"], []).append((mn + mx) / 2.0)
    for role, vals in buckets.items():
        if len(vals) < _BENCH_MIN_SAMPLE:
            continue
        vals.sort()
        out[role] = {
            "n": len(vals),
            "p10": int(_percentile(vals, 0.10)),
            "p25": int(_percentile(vals, 0.25)),
            "p50": int(_percentile(vals, 0.50)),
            "p75": int(_percentile(vals, 0.75)),
            "p90": int(_percentile(vals, 0.90)),
            "mid_avg": int(sum(vals) / len(vals)),
        }
    return out


def salary_context_for_job(job, benchmarks: Optional[dict] = None,
                           db_path: Optional[Path] = None) -> Optional[dict]:
    """Place one job in its role's salary distribution.

    With a numeric salary -> {"kind":"actual", percentile, p25/p50/p75, label}.
    Without one but with a benchmarked role -> {"kind":"estimate", p25/p50/p75}.
    None when there's no role benchmark to compare against.
    """
    job = dict(job) if not isinstance(job, dict) else job
    role = job.get("role_family")
    if not role:
        return None
    if benchmarks is None:
        benchmarks = salary_benchmarks(db_path)
    b = benchmarks.get(role)
    if not b:
        return None

    mn = job.get("salary_min_annual_jpy")
    mx = job.get("salary_max_annual_jpy") or mn
    if mn:
        mid = (mn + mx) / 2.0
        anchors = [(10, b["p10"]), (25, b["p25"]), (50, b["p50"]),
                   (75, b["p75"]), (90, b["p90"])]
        if mid <= b["p10"]:
            pct = 10
        elif mid >= b["p90"]:
            pct = 95
        else:
            pct = 50
            for (plo, vlo), (phi, vhi) in zip(anchors, anchors[1:]):
                if vlo <= mid <= vhi and vhi > vlo:
                    pct = int(plo + (phi - plo) * (mid - vlo) / (vhi - vlo))
                    break
        top = 100 - pct
        if top <= 15:
            label = f"Top {max(5, top)}% pay for {role}"
        elif pct <= 25:
            label = f"Below typical for {role}"
        else:
            label = f"Around median for {role}"
        return {"kind": "actual", "role": role, "n": b["n"], "percentile": pct,
                "p25": b["p25"], "p50": b["p50"], "p75": b["p75"], "label": label}

    return {"kind": "estimate", "role": role, "n": b["n"],
            "p25": b["p25"], "p50": b["p50"], "p75": b["p75"],
            "label": f"Typical {role} pay"}


# ---------------------------------------------------------------------------
# Companies (aggregated from the jobs table)  (Phase 5)
# ---------------------------------------------------------------------------

def _company_slug(name: str) -> str:
    """URL-safe slug from a company name. Deterministic — used to look up by slug."""
    import re
    s = (name or "").lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s or "company"


def companies_list(min_jobs: int = 1,
                   include_archived: bool = False,
                   db_path: Optional[Path] = None) -> list[dict]:
    """All companies with at least `min_jobs` active postings, sorted by count."""
    where_extra = ""
    params: list = []
    if not include_archived:
        where_extra = " AND DATE(last_seen_at) >= DATE('now', ?)"
        params.append(f"-{STALE_DAYS} days")
    with connect(db_path) as conn:
        rows = conn.execute(
            "SELECT company_name AS name, "
            "       MAX(company_name_jp) AS name_jp, "
            "       MAX(company_size) AS company_size, "
            "       MAX(company_year_founded) AS company_year_founded, "
            "       COUNT(*) AS n_jobs, "
            "       MAX(source_quality) AS source_quality, "
            "       AVG(COALESCE(foreigner_fit_score, 0)) AS avg_fit "
            "FROM jobs "
            "WHERE company_name IS NOT NULL AND company_name != '' "
            + where_extra +
            " GROUP BY company_name "
            "HAVING n_jobs >= ? "
            "ORDER BY n_jobs DESC, name ASC",
            params + [min_jobs],
        ).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            d["slug"] = _company_slug(d["name"])
            d["avg_fit"] = round(d["avg_fit"] or 0)
            out.append(d)
        return out


def company_by_slug(slug: str,
                    include_archived: bool = False,
                    db_path: Optional[Path] = None) -> Optional[dict]:
    """Look up a company by slug. Returns the company info dict + its jobs."""
    cos = companies_list(min_jobs=1, include_archived=include_archived, db_path=db_path)
    match = next((c for c in cos if c["slug"] == slug), None)
    if not match:
        return None
    with connect(db_path) as conn:
        where_archive = ""
        params: list = [match["name"]]
        if not include_archived:
            where_archive = " AND DATE(last_seen_at) >= DATE('now', ?)"
            params.append(f"-{STALE_DAYS} days")
        jobs = conn.execute(
            "SELECT * FROM jobs WHERE company_name = ? "
            + where_archive +
            " ORDER BY COALESCE(foreigner_fit_score, 0) DESC, "
            "          COALESCE(post_date, scraped_at) DESC",
            params,
        ).fetchall()
        match["jobs"] = [dict(j) for j in jobs]
    return match


# ---------------------------------------------------------------------------
# Public reports  (Phase 5)
# ---------------------------------------------------------------------------

def report_data(db_path: Optional[Path] = None) -> dict:
    """Bundle of aggregations used by /reports. Cheap, single connection."""
    with connect(db_path) as conn:
        def rows(sql: str, params: tuple = ()):
            return [dict(r) for r in conn.execute(sql, params).fetchall()]

        total = conn.execute("SELECT COUNT(*) AS n FROM jobs").fetchone()["n"]

        fit_dist = rows("""
            SELECT
              CASE
                WHEN foreigner_fit_score IS NULL THEN 'Unscored'
                WHEN foreigner_fit_score >= 90 THEN '90-100 Excellent'
                WHEN foreigner_fit_score >= 75 THEN '75-89 Strong'
                WHEN foreigner_fit_score >= 60 THEN '60-74 Possible'
                WHEN foreigner_fit_score >= 40 THEN '40-59 Weak'
                ELSE '0-39 Poor'
              END AS bucket,
              COUNT(*) AS n
            FROM jobs
            GROUP BY bucket
            ORDER BY MIN(COALESCE(foreigner_fit_score, -1)) DESC
        """)

        role_family = rows("""
            SELECT COALESCE(role_family, '(Unknown)') AS family,
                   COUNT(*) AS n,
                   ROUND(AVG(COALESCE(salary_min_annual_jpy, 0))) AS avg_salary_min,
                   ROUND(AVG(COALESCE(foreigner_fit_score, 0))) AS avg_fit
            FROM jobs
            GROUP BY family
            HAVING n >= 3
            ORDER BY n DESC
            LIMIT 15
        """)

        source_quality = rows("""
            SELECT COALESCE(source_quality, 'Unknown') AS quality,
                   source, COUNT(*) AS n,
                   ROUND(AVG(COALESCE(foreigner_fit_score, 0))) AS avg_fit
            FROM jobs
            GROUP BY quality, source
            ORDER BY n DESC
        """)

        top_companies = rows("""
            SELECT company_name AS name, COUNT(*) AS n,
                   ROUND(AVG(COALESCE(foreigner_fit_score, 0))) AS avg_fit
            FROM jobs
            WHERE company_name IS NOT NULL AND company_name != ''
            GROUP BY company_name
            ORDER BY n DESC
            LIMIT 15
        """)

        posting_lang = rows("""
            SELECT COALESCE(posting_language, 'Unknown') AS lang,
                   COUNT(*) AS n
            FROM jobs
            GROUP BY lang
            ORDER BY n DESC
        """)

        jp_levels = rows("""
            SELECT COALESCE(japanese_level, '(Not specified)') AS lvl,
                   COUNT(*) AS n
            FROM jobs
            GROUP BY lvl
            ORDER BY n DESC
        """)

        salary_dist = rows("""
            SELECT
              CASE
                WHEN salary_min_annual_jpy IS NULL THEN 'Not listed'
                WHEN salary_min_annual_jpy < 4000000 THEN '< ¥4M'
                WHEN salary_min_annual_jpy < 6000000 THEN '¥4M – ¥6M'
                WHEN salary_min_annual_jpy < 8000000 THEN '¥6M – ¥8M'
                WHEN salary_min_annual_jpy < 10000000 THEN '¥8M – ¥10M'
                WHEN salary_min_annual_jpy < 15000000 THEN '¥10M – ¥15M'
                ELSE '¥15M+'
              END AS bucket,
              COUNT(*) AS n
            FROM jobs
            GROUP BY bucket
            ORDER BY MIN(COALESCE(salary_min_annual_jpy, 99999999999))
        """)

        return {
            "total": total,
            "fit_distribution": fit_dist,
            "role_family": role_family,
            "source_quality": source_quality,
            "top_companies": top_companies,
            "posting_language": posting_lang,
            "japanese_levels": jp_levels,
            "salary_distribution": salary_dist,
        }


# ---------------------------------------------------------------------------
# Employer-direct postings: /post-a-job submission flow
# ---------------------------------------------------------------------------

import secrets
from datetime import datetime, timedelta, timezone

EMPLOYER_POST_DURATION_DAYS = 45


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def create_employer_post(data: dict, db_path: Optional[Path] = None) -> dict:
    """
    Insert a direct-from-employer job posting into the jobs table.

    Required fields in `data`:
      - title (str)
      - company_name (str)
      - location (str)
      - description (str)
      - employer_contact_email (str)
      - employer_contact_name (str)

    Optional fields (any of these may be present):
      - employment_terms, work_type, role_family
      - salary, salary_min_annual_jpy, salary_max_annual_jpy
      - japanese_level, english_level
      - remote_work_ok (0/1), visa_sponsorship_mentioned (0/1)
      - requirements (str), application_url (str), application_email (str)
      - industries (str, comma-separated)

    Returns a dict with: {id, manage_token, expires_at, url}.
    """
    now = _utc_now()
    expires_at = now + timedelta(days=EMPLOYER_POST_DURATION_DAYS)
    manage_token = secrets.token_urlsafe(24)

    # Synthesise a unique URL for this posting. The application_url is where
    # candidates apply; the `url` column is our canonical identifier.
    import config as _config
    origin = _config.BASE_URL or "https://gaijinhunterjp.com"
    canonical_url = data.get("application_url") or f"{origin}/employer-job/{manage_token[:16]}"

    # Build the row using the same shape upsert_job expects.
    row = {
        "source": "Direct from employer",
        "source_job_id": manage_token[:12],
        "url": canonical_url,
        "title": data["title"],
        "company_name": data["company_name"],
        "company_name_jp": data.get("company_name_jp"),
        "location": data.get("location"),
        "industries": data.get("industries"),
        "function": data.get("function"),
        "work_type": data.get("work_type"),
        "career_level": data.get("career_level"),
        "employment_terms": data.get("employment_terms", "Full-time"),
        "employer_type": data.get("employer_type"),
        "salary": data.get("salary"),
        "salary_period": data.get("salary_period", "Year"),
        "salary_perks": data.get("salary_perks"),
        "salary_min_jpy": data.get("salary_min_jpy"),
        "salary_max_jpy": data.get("salary_max_jpy"),
        "salary_min_annual_jpy": data.get("salary_min_annual_jpy"),
        "salary_max_annual_jpy": data.get("salary_max_annual_jpy"),
        "english_level": data.get("english_level"),
        "japanese_level": data.get("japanese_level"),
        "other_language": data.get("other_language"),
        "remote_work_ok": data.get("remote_work_ok"),
        "overseas_application_ok": data.get("overseas_application_ok"),
        "has_video_presentation": 0,
        "requirements": data.get("requirements"),
        "description": data["description"],
        "tags": data.get("tags"),
        "post_date": now.date().isoformat(),
        "last_modified_date": now.date().isoformat(),
        "company_year_founded": data.get("company_year_founded"),
        "company_size": data.get("company_size"),
        "company_about": data.get("company_about"),
        "role_family": data.get("role_family"),
        "visa_sponsorship_mentioned": data.get("visa_sponsorship_mentioned"),
        "relocation_support_mentioned": data.get("relocation_support_mentioned"),
        "is_employer_post": 1,
        "employer_contact_email": data["employer_contact_email"],
        "employer_contact_name": data["employer_contact_name"],
        "employer_manage_token": manage_token,
        "application_url": data.get("application_url"),
        "application_email": data.get("application_email"),
        "expires_at": expires_at.isoformat(),
        "moderation_status": "approved",
        "employer_post_status": "active",
        "scraped_at": now.isoformat(),
        "last_seen_at": now.isoformat(),
    }

    with connect(db_path) as conn:
        # Source quality for employer posts is "Direct from employer" (high trust)
        row["source_quality"] = "Direct from employer"
        _derive_fields(row)
        # Re-apply source_quality after _derive_fields so it doesn't overwrite.
        row["source_quality"] = "Direct from employer"

        cols = ", ".join(_WRITE_FIELDS)
        placeholders = ", ".join("?" for _ in _WRITE_FIELDS)
        values = [row.get(f) for f in _WRITE_FIELDS]
        cursor = conn.execute(
            f"INSERT INTO jobs ({cols}) VALUES ({placeholders})", values
        )
        job_id = cursor.lastrowid

    return {
        "id": job_id,
        "manage_token": manage_token,
        "expires_at": expires_at.isoformat(),
        "url": canonical_url,
    }


def get_employer_post_by_token(token: str, db_path: Optional[Path] = None):
    """Return the jobs row for an employer-direct posting matched by manage token."""
    if not token:
        return None
    with connect(db_path) as conn:
        return conn.execute(
            "SELECT * FROM jobs WHERE employer_manage_token = ? AND is_employer_post = 1",
            (token,),
        ).fetchone()


def withdraw_employer_post(token: str, db_path: Optional[Path] = None) -> bool:
    """Mark an employer-direct posting as withdrawn (employer-initiated removal)."""
    with connect(db_path) as conn:
        cur = conn.execute(
            "UPDATE jobs SET employer_post_status = 'withdrawn' "
            "WHERE employer_manage_token = ? AND is_employer_post = 1",
            (token,),
        )
        return cur.rowcount > 0


def reactivate_employer_post(token: str, db_path: Optional[Path] = None) -> bool:
    """Un-withdraw a posting (only effective if it hasn't expired)."""
    with connect(db_path) as conn:
        cur = conn.execute(
            "UPDATE jobs SET employer_post_status = 'active' "
            "WHERE employer_manage_token = ? AND is_employer_post = 1",
            (token,),
        )
        return cur.rowcount > 0


def extend_employer_post(token: str, days: int = EMPLOYER_POST_DURATION_DAYS,
                         db_path: Optional[Path] = None) -> bool:
    """Extend an employer post's expiry by `days` days from NOW (not from prior expiry).

    Calling this from within the last 7 days of expiry is the recommended UX.
    """
    new_expiry = (_utc_now() + timedelta(days=days)).isoformat()
    with connect(db_path) as conn:
        cur = conn.execute(
            "UPDATE jobs SET expires_at = ?, employer_post_status = 'active' "
            "WHERE employer_manage_token = ? AND is_employer_post = 1",
            (new_expiry, token),
        )
        return cur.rowcount > 0


def update_employer_post(token: str, updates: dict,
                         db_path: Optional[Path] = None) -> bool:
    """Patch the editable fields of an employer post."""
    editable = {
        "title", "location", "description", "requirements",
        "salary", "salary_min_annual_jpy", "salary_max_annual_jpy",
        "employment_terms", "japanese_level", "english_level",
        "remote_work_ok", "visa_sponsorship_mentioned",
        "application_url", "application_email", "role_family",
    }
    cols = [k for k in updates.keys() if k in editable]
    if not cols:
        return False
    set_clause = ", ".join(f"{c} = ?" for c in cols)
    values = [updates[c] for c in cols] + [token]
    with connect(db_path) as conn:
        cur = conn.execute(
            f"UPDATE jobs SET {set_clause} "
            "WHERE employer_manage_token = ? AND is_employer_post = 1",
            values,
        )
        return cur.rowcount > 0


def cleanup_expired_employer_posts(db_path: Optional[Path] = None) -> int:
    """Mark expired employer posts as such (status = 'expired')."""
    with connect(db_path) as conn:
        cur = conn.execute(
            "UPDATE jobs SET employer_post_status = 'expired' "
            "WHERE is_employer_post = 1 "
            "AND employer_post_status = 'active' "
            "AND expires_at IS NOT NULL "
            "AND datetime(expires_at) <= datetime('now')"
        )
        return cur.rowcount


def employer_posts_count(db_path: Optional[Path] = None) -> int:
    """Number of currently-live employer-direct postings."""
    with connect(db_path) as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS n FROM jobs "
            "WHERE is_employer_post = 1 "
            "AND COALESCE(employer_post_status, 'active') = 'active' "
            "AND COALESCE(moderation_status, 'approved') = 'approved' "
            "AND (expires_at IS NULL OR datetime(expires_at) > datetime('now'))"
        ).fetchone()
        return row["n"]
