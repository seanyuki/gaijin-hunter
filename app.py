"""
Flask app for the Japan job board.

Routes:
    /                 — main board, all filters
    /saved            — only saved (starred) jobs; IDs come from localStorage,
                        so we accept an `ids` querystring on this route.
    /job/<id>         — detail page
    /api/jobs.json    — same query language as /, returns JSON
"""

from __future__ import annotations

import html as html_module
import logging
import math
import re
from urllib.parse import urlencode

from flask import Flask, abort, flash, jsonify, redirect, render_template, request, url_for

import config
import db

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = config.STATIC_MAX_AGE
PAGE_SIZE = 25

# ---------------------------------------------------------------------------
# Rate limiting (Flask-Limiter). In-memory storage is fine for a single
# gunicorn service; it resets on restart, which is acceptable for spam
# throttling. Behind Render's proxy the real client IP is in
# X-Forwarded-For, so we read the left-most entry rather than the proxy IP.
# ---------------------------------------------------------------------------
try:
    from flask_limiter import Limiter

    def _client_ip() -> str:
        xff = request.headers.get("X-Forwarded-For", "")
        if xff:
            return xff.split(",")[0].strip()
        return request.remote_addr or "127.0.0.1"

    limiter = Limiter(
        key_func=_client_ip,
        app=app,
        default_limits=["300 per hour"],   # generous global fallback (writes)
        storage_uri="memory://",
        headers_enabled=True,
        strategy="fixed-window",
    )

    @limiter.request_filter
    def _exempt_reads_and_health():
        # Reads are never throttled; /healthz must always answer for the
        # platform's health checks.
        return request.method in ("GET", "HEAD", "OPTIONS") or request.path == "/healthz"

    _HAS_LIMITER = True
except Exception:                                     # pragma: no cover
    logging.getLogger("app").exception("Flask-Limiter unavailable; running without rate limits")
    _HAS_LIMITER = False

    class _NoopLimiter:
        def limit(self, *a, **k):
            def deco(f):
                return f
            return deco

        def exempt(self, f):
            return f

        def request_filter(self, f):
            return f

    limiter = _NoopLimiter()

# Ensure schema exists on import — required when served by gunicorn, where
# the __main__ block never runs. init_db is idempotent and cheap.
try:
    db.init_db()
except Exception:                                     # pragma: no cover
    logging.getLogger("app").exception("init_db failed at startup")


def _base_url() -> str:
    """Public origin for absolute URLs (BASE_URL env, else request origin)."""
    return config.BASE_URL or request.url_root.rstrip("/")


@app.context_processor
def _inject_base_url():
    return {"base_url": _base_url()}


@app.before_request
def _canonicalize_host():
    """301 any non-canonical host (www., *.onrender.com) to BASE_URL.

    Only active when FLASK_ENV=production AND BASE_URL is set, so local
    development and tests are never redirected. /healthz is exempt — platform
    health checks hit the service via its internal/onrender hostname and must
    get a 200, not a redirect.
    """
    if not (config.IS_PRODUCTION and config.CANONICAL_HOST):
        return None
    if request.path == "/healthz":
        return None
    host = (request.host or "").split(":")[0]
    if host and host != config.CANONICAL_HOST:
        target = config.BASE_URL + request.full_path.rstrip("?")
        return redirect(target, code=301)
    return None


def _pagination_window(current: int, total: int, window: int = 2) -> list:
    """
    Build a list of page tokens to render in the pagination bar.

    Always includes: page 1, last page, current page, and `window` pages on
    each side of current. Inserts `None` (rendered as an ellipsis) wherever
    there's a numerical gap between adjacent tokens.

    Example: current=5, total=14, window=2  ->
        [1, None, 3, 4, 5, 6, 7, None, 14]
    """
    if total <= 1:
        return []
    pages = {1, total, current}
    for i in range(max(1, current - window), min(total, current + window) + 1):
        pages.add(i)
    sorted_pages = sorted(pages)
    out: list = []
    prev = 0
    for p in sorted_pages:
        if prev:
            if p - prev == 2:
                # Only one page in the gap — fill it instead of an ellipsis
                # (same visual width, less clicks for the user).
                out.append(prev + 1)
            elif p - prev > 2:
                out.append(None)   # multi-page gap → ellipsis
        out.append(p)
        prev = p
    return out

DROPDOWN_FILTERS = [
    ("role_family",      "Role family"),
    ("prefecture",       "Prefecture"),
    ("region",           "Region"),
    ("posting_language", "Posting language"),
    ("source_quality",   "Source quality"),
    ("english_level",    "English level"),
    ("japanese_level",   "Japanese level"),
    ("employment_terms", "Employment type"),
    ("career_level",     "Career level"),
    ("source",           "Source"),
]
# The four filters foreigners use constantly stay visible; the rest collapse
# under "More filters" so the search area reads like a product, not a control
# panel. (Both lists keep the same (col, label) shape as DROPDOWN_FILTERS.)
PRIMARY_DROPDOWNS   = [d for d in DROPDOWN_FILTERS
                       if d[0] in ("japanese_level", "role_family",
                                   "employment_terms", "prefecture")]
SECONDARY_DROPDOWNS = [d for d in DROPDOWN_FILTERS if d not in PRIMARY_DROPDOWNS]
CHECKBOX_FILTERS = [
    ("remote_work_ok",               "Remote Work OK"),
    ("overseas_application_ok",      "Overseas Application OK"),
    ("visa_sponsorship_mentioned",   "Visa support mentioned"),
    ("relocation_support_mentioned", "Relocation support mentioned"),
    ("has_video_presentation",       "Has Video Presentation"),
]
SORT_LABELS = [
    ("recommended", "Recommended"),
    ("fit",         "Foreigner Fit: high to low"),
    ("newest",      "Newest first"),
    ("salary_desc", "Salary: high to low"),
    ("salary_asc",  "Salary: low to high"),
    ("title",       "Title (A→Z)"),
    ("oldest",      "Oldest first"),
]
DAYS_OPTIONS = [
    ("",   "Any time"),
    ("7",  "Last 7 days"),
    ("30", "Last 30 days"),
    ("90", "Last 90 days"),
]
# Pre-built one-click chips. Each is a label + a dict of querystring overrides.
# Seven presets, one per real decision a foreign applicant makes. (Fit-floor,
# posting-language and recency chips were cut: those live in sort + filters.)
QUICK_CHIPS = [
    {"label": "Professional roles",   "params": {"professional_only": "1"}},
    {"label": "Visa support",         "params": {"visa_sponsorship_mentioned": "1"}},
    {"label": "Apply from abroad",    "params": {"overseas_application_ok": "1"}},
    {"label": "No Japanese required", "params": {"japanese_level": "Not Required"}},
    {"label": "Remote OK",            "params": {"remote_work_ok": "1"}},
    {"label": "¥8M+ salary",          "params": {"salary_min": "8000000"}},
    {"label": "Exclude teaching",     "params": {"exclude_teaching": "1"}},
]


def _read_filters_from_request() -> dict:
    """Parse filters and meta-params from the current request."""
    out = {
        "q":           request.args.get("q", "").strip() or None,
        "location":    request.args.get("location", "").strip() or None,
        "salary_min":  None,
        "days_within": None,
        "sort":        request.args.get("sort", db.DEFAULT_SORT),
        "page":        1,
        "include_archived": request.args.get("archived") == "1",
        "dropdowns":   {},
        "flags":       {},
    }
    try:
        out["salary_min"] = int(request.args.get("salary_min")) if request.args.get("salary_min") else None
    except ValueError:
        out["salary_min"] = None
    try:
        out["days_within"] = int(request.args.get("days_within")) if request.args.get("days_within") else None
    except ValueError:
        out["days_within"] = None
    try:
        out["page"] = max(1, int(request.args.get("page", "1")))
    except ValueError:
        out["page"] = 1
    if out["sort"] not in db.SORT_OPTIONS:
        out["sort"] = db.DEFAULT_SORT

    # Phase 1 filters
    try:
        out["foreigner_fit_min"] = (int(request.args.get("foreigner_fit_min"))
                                    if request.args.get("foreigner_fit_min") else None)
    except ValueError:
        out["foreigner_fit_min"] = None
    out["exclude_teaching"]      = request.args.get("exclude_teaching") == "1"
    out["exclude_japanese_only"] = request.args.get("exclude_japanese_only") == "1"
    out["salary_listed_only"]    = request.args.get("salary_listed_only") == "1"
    out["professional_only"]     = request.args.get("professional_only") == "1"
    if out["location"]:
        out["dropdowns"]["location"] = [out["location"]]
    for col, _ in DROPDOWN_FILTERS:
        vals = [v for v in request.args.getlist(col) if v]
        if vals:
            out["dropdowns"][col] = vals
    for col, _ in CHECKBOX_FILTERS:
        if request.args.get(col) == "1":
            out["flags"][col] = True
    # Human-friendly URL aliases (used in shared links and resource pages).
    for alias, col in (("visa_support", "visa_sponsorship_mentioned"),
                       ("apply_from_abroad", "overseas_application_ok"),
                       ("remote", "remote_work_ok")):
        if request.args.get(alias) == "1":
            out["flags"][col] = True
    return out


def _query_and_render(template: str, only_ids: list[int] | None = None,
                      include_only_archived: bool = False,
                      extra_ids: list[int] | None = None,
                      **extra) -> str:
    p = _read_filters_from_request()
    common_kwargs = dict(
        q=p["q"], filters=p["dropdowns"], flags=p["flags"],
        salary_min=p["salary_min"], days_within=p["days_within"],
        include_archived=p["include_archived"],
        include_only_archived=include_only_archived,
        foreigner_fit_min=p["foreigner_fit_min"],
        exclude_teaching=p["exclude_teaching"],
        exclude_japanese_only=p["exclude_japanese_only"],
        salary_listed_only=p["salary_listed_only"],
        professional_only=p["professional_only"],
    )
    # /saved and /applied: restrict the SQL query to the localStorage IDs
    # (WHERE id IN (...)) instead of scanning the table and filtering here.
    if only_ids is not None:
        common_kwargs["only_ids"] = only_ids
    total = db.count_jobs(**common_kwargs)
    jobs = db.query_jobs(
        **common_kwargs,
        sort=p["sort"],
        limit=PAGE_SIZE, offset=(p["page"] - 1) * PAGE_SIZE,
    )

    # /archived: union DB-stale rows with manually-hidden ids
    if extra_ids:
        already = {j["id"] for j in jobs}
        extras = [db.get_job(i) for i in extra_ids if i not in already]
        extras = [r for r in extras if r is not None]
        jobs = list(jobs) + extras
        total = total + len(extras)

    # Counts per dropdown option (respect other-filter context). Columns with
    # no active self-filter share one context -> a single bulk scan; only the
    # actively-filtered columns need their own no-self-filter query.
    ctx = dict(q=p["q"], flags=p["flags"], salary_min=p["salary_min"],
               days_within=p["days_within"], include_archived=p["include_archived"])
    filtered_cols = {c for c, _ in DROPDOWN_FILTERS if p["dropdowns"].get(c)}
    bulk_cols = [c for c, _ in DROPDOWN_FILTERS if c not in filtered_cols]
    counts = db.counts_bulk(bulk_cols, filters=p["dropdowns"], **ctx)
    for col in filtered_cols:
        counts[col] = db.counts_for(col, filters=p["dropdowns"], **ctx)
    dropdown_options = {col: db.distinct(col) for col, _ in DROPDOWN_FILTERS}
    selected = {col: set(p["dropdowns"].get(col, [])) for col, _ in DROPDOWN_FILTERS}

    n_pages = max(1, math.ceil(total / PAGE_SIZE))
    pagination = _pagination_window(p["page"], n_pages)
    # Foreigner-fit reason map (used by job-card "Why this fits" rendering).
    import inference as _inf
    fit_reason_labels = _inf.FIT_REASON_LABELS

    # Salary context per job: pay percentile (listed) or role estimate (missing).
    benchmarks = db.salary_benchmarks()
    salary_ctx = {j["id"]: db.salary_context_for_job(j, benchmarks) for j in jobs}

    return render_template(
        template,
        section="jobs",
        jobs=jobs, total=total, page=p["page"], n_pages=n_pages, page_size=PAGE_SIZE,
        pagination=pagination,
        fit_reason_labels=fit_reason_labels,
        salary_ctx=salary_ctx,
        foreigner_fit_min=p["foreigner_fit_min"] or "",
        exclude_teaching=p["exclude_teaching"],
        exclude_japanese_only=p["exclude_japanese_only"],
        salary_listed_only=p["salary_listed_only"],
        professional_only=p["professional_only"],
        q=p["q"] or "", location=p["dropdowns"].get("location", [""])[0] or "",
        sort=p["sort"], sort_labels=SORT_LABELS,
        days_within=p["days_within"], days_options=DAYS_OPTIONS,
        salary_min=p["salary_min"] or "",
        include_archived=p["include_archived"],
        dropdown_filters=DROPDOWN_FILTERS,
        primary_dropdowns=PRIMARY_DROPDOWNS,
        secondary_dropdowns=SECONDARY_DROPDOWNS,
        checkbox_filters=CHECKBOX_FILTERS,
        dropdown_options=dropdown_options,
        counts=counts,
        selected=selected,
        flags=p["flags"],
        undisclosed=db.UNDISCLOSED,
        quick_chips=QUICK_CHIPS,
        stats=db.stats(),
        request_args=request.args,
        **extra,
    )


def _parse_ids(raw: str) -> list[int]:
    return [int(x) for x in (raw or "").split(",") if x.strip().isdigit()]


@app.route("/")
def landing():
    """Marketing landing page — hero, value props, tool showcase, featured jobs,
    stories, live data strip, FAQ, final CTA."""
    import content, inference as _inf
    # Featured jobs: highest Foreigner Fit, exclude Japanese-only
    featured = db.query_jobs(limit=6, sort="recommended",
                             foreigner_fit_min=70,
                             exclude_japanese_only=True,
                             salary_listed_only=False)

    # Quick stats for the hero / data strip — computed cheaply
    with db.connect() as conn:
        company_count = conn.execute(
            "SELECT COUNT(DISTINCT company_name) AS n FROM jobs "
            "WHERE company_name IS NOT NULL AND company_name != ''"
        ).fetchone()["n"]
        english_count = conn.execute(
            "SELECT COUNT(*) AS n FROM jobs WHERE posting_language = 'English'"
        ).fetchone()["n"]
        visa_count = conn.execute(
            "SELECT COUNT(*) AS n FROM jobs WHERE visa_sponsorship_mentioned = 1"
        ).fetchone()["n"]
        remote_count = conn.execute(
            "SELECT COUNT(*) AS n FROM jobs WHERE remote_work_ok = 1"
        ).fetchone()["n"]
        overseas_count = conn.execute(
            "SELECT COUNT(*) AS n FROM jobs WHERE overseas_application_ok = 1"
        ).fetchone()["n"]
        # No-Japanese-required: canonical level OR the inference flag.
        no_japanese_count = conn.execute(
            "SELECT COUNT(*) AS n FROM jobs WHERE "
            "japanese_level = 'Not Required' "
            "OR foreigner_fit_reasons LIKE '%no_japanese_required%'"
        ).fetchone()["n"]
        # ¥8M+: either bound of the annualized salary reaches the threshold.
        high_salary_count = conn.execute(
            "SELECT COUNT(*) AS n FROM jobs WHERE "
            "COALESCE(salary_max_annual_jpy, 0) >= 8000000 "
            "OR COALESCE(salary_min_annual_jpy, 0) >= 8000000"
        ).fetchone()["n"]

    professional_count = db.count_jobs(professional_only=True)

    return render_template("landing.html",
                           latest_jobs=featured,
                           fit_reason_labels=_inf.FIT_REASON_LABELS,
                           stats=db.stats(),
                           company_count=company_count,
                           english_count=english_count,
                           visa_count=visa_count,
                           remote_count=remote_count,
                           overseas_count=overseas_count,
                           no_japanese_count=no_japanese_count,
                           high_salary_count=high_salary_count,
                           professional_count=professional_count)


@app.route("/jobs")
def index():
    return _query_and_render("index.html", view="all")


@app.route("/resources")
def resources():
    """Hub: lists every resource sub-page as a card."""
    import content
    return render_template("resources_hub.html", section="resources",
                           resources=content.RESOURCES)


@app.route("/resources/<slug>")
def resource_detail(slug):
    """Per-topic resource sub-page rendered from content.RESOURCES, with deep-dive
    extensions merged in from resources_extra (kept separate to avoid editing the
    large content.py in place)."""
    import content, resources_extra
    item = content.get_resource(slug)
    if not item:
        abort(404)
    item = resources_extra.merge_resource(item)
    return render_template("resource_detail.html", section="resources",
                           item=item, all_resources=content.RESOURCES)


@app.route("/tools")
def tools():
    """Hub for the interactive calculators."""
    return render_template("tools_hub.html", section="tools")


@app.route("/tools/visa-eligibility")
def tool_visa():
    return render_template("tool_visa_eligibility.html", section="tools")


@app.route("/tools/hsp-points")
def tool_hsp():
    return render_template("tool_hsp_points.html", section="tools")


@app.route("/tools/take-home-pay")
def tool_takehome():
    return render_template("tool_take_home_pay.html", section="tools")


@app.route("/guides")
def guides_hub():
    """City + role guides hub. Role guides now include the 3 former roadmap-only
    roles (data/AI, design, engineering management), consolidated here."""
    import content, roles_consolidated
    return render_template("guides_hub.html", section="guides",
                           guides=roles_consolidated.all_guides(content.GUIDES))


@app.route("/guides/<slug>")
def guide_detail(slug):
    """Per-guide page. Role guides get: (1) the deep-dive extension from
    guides_extra, and (2) the matching career roadmap appended on the same page
    (consolidation of the old /roadmaps section)."""
    import content, guides_extra, roles_consolidated
    item = content.get_guide(slug) or roles_consolidated.get_new_role_guide(slug)
    if not item:
        abort(404)
    item = guides_extra.merge_guide(item)
    item = roles_consolidated.consolidate_guide(item, content.ROADMAPS)
    return render_template("guide_detail.html", section="guides",
                           item=item,
                           all_guides=roles_consolidated.all_guides(content.GUIDES))


@app.route("/living")
def living_hub():
    """Relocation & settlement hub — the post-offer 'living in Japan' journey."""
    import living_content
    return render_template("living_hub.html", section="living",
                           guides=living_content.LIVING_GUIDES)


@app.route("/living/<slug>")
def living_detail(slug):
    import living_content
    item = living_content.get_living_guide(slug)
    if not item:
        abort(404)
    # Surface the FAQ section in the in-page TOC when present.
    if item.get("faqs") and not any(a == "faq" for a, _ in item.get("toc", [])):
        item = dict(item)
        item["toc"] = list(item.get("toc", [])) + [("faq", "FAQ")]
    return render_template("living_detail.html", section="living",
                           item=item, all_guides=living_content.LIVING_GUIDES)


@app.route("/tools/relocation-budget")
def tool_relocation_budget():
    return render_template("tool_relocation_budget.html", section="tools")


# ---------------------------------------------------------------------------
# Phase 5 routes
# ---------------------------------------------------------------------------

@app.route("/newsletter")
def newsletter():
    """Signup page."""
    stats = db.newsletter_stats()
    return render_template("newsletter.html", section="newsletter", stats=stats)


@app.route("/api/newsletter/subscribe", methods=["POST"])
@limiter.limit("10 per hour")
def api_newsletter_subscribe():
    """Accept signup via JSON or form POST."""
    payload = request.get_json(silent=True) or request.form
    email = (payload.get("email") or "").strip()
    role_families = payload.getlist("role_families") if hasattr(payload, "getlist") \
        else (payload.get("role_families") or [])
    if isinstance(role_families, str):
        role_families = [r.strip() for r in role_families.split(",") if r.strip()]
    salary_min = payload.get("salary_min") or None
    try:
        salary_min = int(salary_min) if salary_min else None
    except (TypeError, ValueError):
        salary_min = None
    locations = payload.get("preferred_locations") or ""
    if isinstance(locations, str):
        locations = [l.strip() for l in locations.split(",") if l.strip()]

    ok, token_or_err = db.newsletter_subscribe(
        email=email, role_families=role_families,
        salary_min=salary_min, preferred_locations=locations,
    )
    if not ok:
        return jsonify({"ok": False, "error": token_or_err}), 400
    return jsonify({"ok": True, "token": token_or_err,
                    "unsubscribe_url": f"/newsletter/unsubscribe?token={token_or_err}"})


@app.route("/newsletter/unsubscribe")
def newsletter_unsubscribe_view():
    token = (request.args.get("token") or "").strip()
    ok = db.newsletter_unsubscribe(token) if token else False
    return render_template("newsletter_unsubscribe.html", section="newsletter",
                           ok=ok, token_present=bool(token))


@app.route("/companies")
def companies_hub():
    """All companies with at least 2 active postings, sorted by job count."""
    cos = db.companies_list(min_jobs=2)
    return render_template("companies_hub.html", section="companies", companies=cos)


@app.route("/companies/<slug>")
def company_detail(slug):
    company = db.company_by_slug(slug)
    if not company:
        abort(404)
    import inference as _inf
    return render_template("company_detail.html", section="companies",
                           company=company, fit_reason_labels=_inf.FIT_REASON_LABELS)


@app.route("/reports")
def reports():
    """Public dashboards: aggregations on the jobs table."""
    return render_template("reports.html", section="reports",
                           data=db.report_data())


@app.route("/community")
def community():
    import content
    return render_template("community.html", section="community",
                           groups=content.COMMUNITY_GROUPS)


# ---------------------------------------------------------------------------
# Phase 6 routes
# ---------------------------------------------------------------------------

@app.route("/start")
def onboarding_quiz():
    return render_template("onboarding_quiz.html", section="start")


@app.route("/tools/jd-match")
def tool_jd_match():
    return render_template("tool_jd_match.html", section="tools")


@app.route("/tools/visa-timeline")
def tool_visa_timeline():
    return render_template("tool_visa_timeline.html", section="tools")


@app.route("/tools/col-comparator")
def tool_col_comparator():
    return render_template("tool_col_comparator.html", section="tools")


@app.route("/insights/salary")
def insights_salary():
    """Salary insights — combines:
    1. 2026 macro outlook + 11-sector industry data (from salary_data.py).
    2. Live percentiles computed from active job-board postings."""
    import salary_data
    # Live percentiles from the DB.
    families = {}
    with db.connect() as conn:
        rows = conn.execute(
            "SELECT role_family, salary_min_annual_jpy, salary_max_annual_jpy, "
            "       company_name, location, title, id "
            "FROM jobs "
            "WHERE salary_min_annual_jpy IS NOT NULL "
            "  AND salary_min_annual_jpy > 0 "
            "  AND role_family IS NOT NULL "
            "  AND DATE(last_seen_at) >= DATE('now', '-30 days')"
        ).fetchall()
    for r in rows:
        fam = r["role_family"]
        mn = r["salary_min_annual_jpy"]
        mx = r["salary_max_annual_jpy"] or mn
        mid = (mn + mx) / 2
        families.setdefault(fam, []).append({
            "mid": mid, "min": mn, "max": mx,
            "company": r["company_name"], "location": r["location"],
            "title": r["title"], "id": r["id"],
        })
    insights = []
    for fam, items in sorted(families.items(), key=lambda x: -len(x[1])):
        if len(items) < 3:
            continue
        mids = sorted(it["mid"] for it in items)
        def pct(p):
            k = (len(mids) - 1) * p
            f, c = int(k), min(int(k) + 1, len(mids) - 1)
            return int(mids[f] + (mids[c] - mids[f]) * (k - f))
        insights.append({
            "family": fam,
            "n": len(items),
            "p25": pct(0.25), "p50": pct(0.50),
            "p75": pct(0.75), "p90": pct(0.90),
            "min": int(mids[0]), "max": int(mids[-1]),
            "examples": items[:3],
        })

    # Pre-count total roles across all sectors for the hero stat.
    total_roles = sum(len(s.get("roles_east", [])) + len(s.get("roles_west", []))
                      for s in salary_data.SECTORS)

    return render_template("insights_salary.html", section="insights",
                           insights=insights,
                           sectors=salary_data.SECTORS,
                           outlook=salary_data.MARKET_OUTLOOK_2026,
                           total_roles=total_roles)


@app.route("/interview-prep")
def interview_prep():
    import content
    return render_template("interview_prep.html", section="interview-prep",
                           question_banks=content.INTERVIEW_QUESTIONS,
                           star_prompts=content.STAR_PROMPTS)


@app.route("/compare")
def job_compare():
    """Side-by-side job comparison. IDs come via ?ids=."""
    ids = _parse_ids(request.args.get("ids", ""))
    jobs = [db.get_job(i) for i in ids] if ids else []
    jobs = [j for j in jobs if j is not None]
    return render_template("job_compare.html", section="compare", jobs=jobs)


# Roadmaps were consolidated INTO the role guides. These routes now redirect to
# the matching guide (anchored to its Career roadmap section) so old links and
# bookmarks keep working.
_ROADMAP_TO_GUIDE = {
    "software-engineering": "software-engineering",
    "product-management": "product-management",
    "finance-accounting": "finance-accounting",
    "sales-business-development": "sales-business-development",
    "marketing": "marketing-growth",
    "data-ai": "data-ai",
    "design": "design",
    "engineering-management": "engineering-management",
}


@app.route("/roadmaps")
def roadmaps_hub():
    # The standalone roadmaps hub is gone; role guides hold the roadmaps now.
    return redirect(url_for("guides_hub"), code=301)


@app.route("/roadmaps/<slug>")
def roadmap_detail(slug):
    guide_slug = _ROADMAP_TO_GUIDE.get(slug)
    if guide_slug:
        return redirect(url_for("guide_detail", slug=guide_slug)
                        + "#career-roadmap", code=301)
    # Unknown roadmap slug → guides hub.
    return redirect(url_for("guides_hub"), code=301)


@app.route("/pillars/<slug>")
def pillar_guide(slug):
    import content
    item = next((p for p in content.PILLAR_GUIDES if p["slug"] == slug), None)
    if not item:
        abort(404)
    return render_template("pillar_guide.html", section="resources",
                           item=item, all_pillars=content.PILLAR_GUIDES)


@app.route("/glossary")
def glossary():
    import content
    return render_template("glossary.html", section="glossary",
                           terms=content.GLOSSARY)


@app.route("/sitemap.xml")
def sitemap_xml():
    """Dynamic sitemap covering all major routes + DB-driven detail pages.

    Includes priority + changefreq + lastmod hints to help crawlers
    prioritize the most-important and most-updated pages.
    """
    import content
    from datetime import date

    today = date.today().isoformat()

    # (path, priority, changefreq)
    static_pages = [
        # Top-tier landing pages
        ("/",                            "1.0", "daily"),
        ("/jobs",                        "1.0", "daily"),
        ("/companies",                   "0.9", "weekly"),
        ("/post-a-job",                  "0.8", "monthly"),
        ("/resources",                   "0.9", "weekly"),
        ("/guides",                      "0.9", "weekly"),
        ("/tools",                       "0.9", "weekly"),
        ("/insights/salary",             "0.9", "monthly"),
        # Calculators and tools — high-intent
        ("/tools/visa-eligibility",      "0.9", "monthly"),
        ("/tools/hsp-points",            "0.9", "monthly"),
        ("/tools/take-home-pay",         "0.9", "monthly"),
        ("/tools/jd-match",              "0.8", "monthly"),
        ("/tools/visa-timeline",         "0.8", "monthly"),
        ("/tools/col-comparator",        "0.8", "monthly"),
        ("/tools/relocation-budget",     "0.9", "monthly"),
        ("/interview-prep",              "0.8", "monthly"),
        # Living in Japan — relocation & settlement
        ("/living",                      "0.9", "weekly"),
        # Resume + templates
        ("/resume",                      "0.8", "monthly"),
        ("/resume/cv",                   "0.7", "monthly"),
        ("/resume/cover-letter",         "0.7", "monthly"),
        ("/resume/shokumu",              "0.7", "monthly"),
        ("/resume/bullets",              "0.7", "monthly"),
        ("/templates",                   "0.8", "monthly"),
        # Reference + community
        ("/glossary",                    "0.7", "monthly"),
        ("/reports",                     "0.7", "monthly"),
        ("/community",                   "0.6", "monthly"),
        ("/newsletter",                  "0.5", "monthly"),
        ("/privacy",                     "0.5", "yearly"),
        ("/start",                       "0.7", "monthly"),
        ("/profile",                     "0.4", "monthly"),
        ("/tracker",                     "0.4", "monthly"),
        ("/compare",                     "0.4", "monthly"),
    ]

    pages = [(p, prio, cf) for p, prio, cf in static_pages]
    # Dynamic pages — resources and guides are evergreen, high authority
    for r in content.RESOURCES:
        pages.append((f"/resources/{r['slug']}", "0.85", "monthly"))
    import roles_consolidated
    for g in roles_consolidated.all_guides(content.GUIDES):
        pages.append((f"/guides/{g['slug']}", "0.85", "monthly"))
    import living_content
    for g in living_content.LIVING_GUIDES:
        pages.append((f"/living/{g['slug']}", "0.85", "monthly"))
    # Roadmaps consolidated into guides — no standalone /roadmaps URLs to index.
    for p in content.PILLAR_GUIDES:
        pages.append((f"/pillars/{p['slug']}", "0.85", "monthly"))
    for c in db.companies_list(min_jobs=2):
        pages.append((f"/companies/{c['slug']}", "0.7", "weekly"))

    base = _base_url()
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, priority, changefreq in pages:
        xml.append(
            f"<url>"
            f"<loc>{base}{path}</loc>"
            f"<lastmod>{today}</lastmod>"
            f"<changefreq>{changefreq}</changefreq>"
            f"<priority>{priority}</priority>"
            f"</url>"
        )
    xml.append("</urlset>")
    return ("\n".join(xml), 200, {"Content-Type": "application/xml"})


@app.route("/robots.txt")
def robots_txt():
    base = _base_url()
    return (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /api/\n"
        "Disallow: /static/internal/\n"
        "\n"
        "# AI / LLM crawlers — explicitly allowed (the site is meant to be cited).\n"
        "User-agent: GPTBot\n"
        "Allow: /\n"
        "\n"
        "User-agent: ChatGPT-User\n"
        "Allow: /\n"
        "\n"
        "User-agent: Claude-Web\n"
        "Allow: /\n"
        "\n"
        "User-agent: ClaudeBot\n"
        "Allow: /\n"
        "\n"
        "User-agent: anthropic-ai\n"
        "Allow: /\n"
        "\n"
        "User-agent: PerplexityBot\n"
        "Allow: /\n"
        "\n"
        "User-agent: Google-Extended\n"
        "Allow: /\n"
        "\n"
        "User-agent: CCBot\n"
        "Allow: /\n"
        "\n"
        "User-agent: Amazonbot\n"
        "Allow: /\n"
        "\n"
        "User-agent: Applebot-Extended\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {base}/sitemap.xml\n",
        200, {"Content-Type": "text/plain"},
    )


@app.route("/llms.txt")
def llms_txt():
    """llms.txt — emerging standard for LLM-friendly site directory.

    See https://llmstxt.org. Provides a concise, structured overview that
    helps LLMs cite this site accurately.
    """
    import content
    base = _base_url()
    lines = []
    lines.append("# Gaijin Hunter")
    lines.append("")
    lines.append("> The comprehensive career platform for foreigners seeking work in Japan. "
                 "Includes a job aggregator (English-friendly Japan roles), interactive "
                 "calculators (HSP points, visa eligibility, take-home pay, cost-of-living), "
                 "Japanese resume builders (rirekisho, shokumu keirekisho, English CV, "
                 "cover letter), bilingual email templates, application tracker, and "
                 "research-backed guides on Japan's job market, visas, salary, JLPT, and culture.")
    lines.append("")
    lines.append("Audience: foreign professionals (software engineers, PMs, designers, "
                 "marketers, sales, finance, teachers, researchers) looking to work in "
                 "Japan or already living there. Data is updated for 2026.")
    lines.append("")
    lines.append("## Tools and calculators")
    lines.append("")
    lines.append(f"- [HSP Points Calculator]({base}/tools/hsp-points): Estimate your "
                 "Highly Skilled Professional visa points across academic background, "
                 "career, salary, age, and bonus factors. Free, runs in-browser.")
    lines.append(f"- [Visa Eligibility Checker]({base}/tools/visa-eligibility): Decision-tree "
                 "tool that maps your background to Japanese visa categories "
                 "(Engineer/Specialist, HSP, J-Skip, J-Find, Business Manager, Instructor, SSW).")
    lines.append(f"- [Take-home Pay Calculator]({base}/tools/take-home-pay): Computes net "
                 "monthly take-home pay in Japan after income tax, residence tax, social "
                 "insurance, and pension contributions, with 2026 rates.")
    lines.append(f"- [Cost-of-Living Comparator]({base}/tools/col-comparator): Side-by-side "
                 "comparison of cost of living in Tokyo, Osaka, Fukuoka, Sapporo, and other "
                 "Japanese cities.")
    lines.append(f"- [JD Match Analyzer]({base}/tools/jd-match): Paste a job description "
                 "and your CV; receive a match score with explanation.")
    lines.append(f"- [Visa Timeline & Checklist]({base}/tools/visa-timeline): Step-by-step "
                 "visa-application timeline with checklist for COE, embassy, and arrival.")
    lines.append(f"- [Salary Insights 2026]({base}/insights/salary): Interactive dashboard "
                 "of compensation across 11 sectors and ~589 roles, drawing on the 2026 "
                 "Robert Walters Japan Salary Survey and TokyoDev 2025 Developer Survey.")
    lines.append("")
    lines.append("## Resume and email builders")
    lines.append("")
    lines.append(f"- [Rirekisho (履歴書) Builder]({base}/resume): MHLW-standard Japanese "
                 "resume in proper layout, with English-to-Japanese auto-conversion of "
                 "common fields and inline guidance.")
    lines.append(f"- [Shokumu Keirekisho (職務経歴書) Builder]({base}/resume/shokumu): "
                 "Career history document in standard Japanese convention.")
    lines.append(f"- [English CV Builder]({base}/resume/cv): Optimised for foreign-cap "
                 "Japan employers (FAANG Tokyo, Mercari international, Indeed).")
    lines.append(f"- [Cover Letter Builder]({base}/resume/cover-letter): Customisable "
                 "by tone and target company.")
    lines.append(f"- [Resume Bullet Improver]({base}/resume/bullets): Rewrite your CV "
                 "bullets with stronger verbs, quantified outcomes.")
    lines.append(f"- [Email Templates Library]({base}/templates): 39 bilingual "
                 "(English + Japanese) templates across application, follow-up, interview, "
                 "offer, decline, onboarding, resignation, references, recruiter outreach.")
    lines.append("")
    lines.append("## Career resources (deep-research articles)")
    lines.append("")
    for r in content.RESOURCES:
        lines.append(f"- [{r['title']}]({base}/resources/{r['slug']}): {r['summary']}")
    lines.append("")
    lines.append("## City and role guides (each role guide includes its career roadmap)")
    lines.append("")
    import roles_consolidated
    for g in roles_consolidated.all_guides(content.GUIDES):
        lines.append(f"- [{g['title']}]({base}/guides/{g['slug']}): {g['summary']}")
    lines.append("")
    lines.append("## Living in Japan (relocation & settlement)")
    lines.append("")
    import living_content
    for g in living_content.LIVING_GUIDES:
        lines.append(f"- [{g['title']}]({base}/living/{g['slug']}): {g['summary']}")
    lines.append("")
    lines.append("## Long-form deep-dive guides (pillar pages)")
    lines.append("")
    for p in content.PILLAR_GUIDES:
        lines.append(f"- [{p['title']}]({base}/pillars/{p['slug']}): {p['summary']}")
    lines.append("")
    lines.append("## Reference")
    lines.append("")
    lines.append(f"- [Glossary of Japanese Hiring Terms]({base}/glossary): "
                 f"{len(content.GLOSSARY)} terms (rirekisho, shokumu, naitei, nemawashi, "
                 "and more) with English explanations.")
    lines.append(f"- [Companies Hiring Foreigners]({base}/companies): Vetted Japanese and "
                 "foreign-cap companies actively hiring international talent.")
    lines.append(f"- [Public Reports]({base}/reports): Aggregated job-market data, "
                 "salary trends, visa pipeline data.")
    lines.append(f"- [Community]({base}/community): Foreigner-focused Tokyo communities, "
                 "Slack workspaces, Reddit subs, meetups.")
    lines.append("")
    lines.append("## Site information")
    lines.append("")
    lines.append("- All tools run client-side; no signup required; data stays in browser.")
    lines.append("- Updated continuously; 2026 data reflects current Japanese policy and market.")
    lines.append("- Citations on every research-backed page; sources include the 2026 Robert "
                 "Walters Japan Salary Survey, TokyoDev 2025 Developer Survey, MHLW guidelines, "
                 "Immigration Services Agency of Japan publications, and curated foreign-worker "
                 "blogs / forums.")
    return ("\n".join(lines), 200, {"Content-Type": "text/plain; charset=utf-8"})


@app.route("/api/similar/<int:job_id>")
def api_similar_jobs(job_id: int):
    """Five similar jobs based on role_family and salary band."""
    job = db.get_job(job_id)
    if not job:
        return jsonify({"jobs": []})
    salary = job["salary_min_annual_jpy"] or 0
    band_low = max(0, int(salary * 0.7)) if salary else 0
    band_high = int(salary * 1.5) if salary else 99999999999
    role_family = job["role_family"]
    with db.connect() as conn:
        if role_family and salary:
            rows = conn.execute(
                "SELECT id, title, company_name, location, salary_min_annual_jpy, "
                "       foreigner_fit_score, role_family "
                "FROM jobs "
                "WHERE id != ? "
                "  AND role_family = ? "
                "  AND DATE(last_seen_at) >= DATE('now', '-30 days') "
                "  AND COALESCE(salary_min_annual_jpy, 0) BETWEEN ? AND ? "
                "ORDER BY ABS(COALESCE(salary_min_annual_jpy, 0) - ?) "
                "LIMIT 5",
                (job_id, role_family, band_low, band_high, salary),
            ).fetchall()
        elif role_family:
            rows = conn.execute(
                "SELECT id, title, company_name, location, salary_min_annual_jpy, "
                "       foreigner_fit_score, role_family "
                "FROM jobs WHERE id != ? AND role_family = ? "
                "  AND DATE(last_seen_at) >= DATE('now', '-30 days') "
                "ORDER BY COALESCE(foreigner_fit_score, 0) DESC LIMIT 5",
                (job_id, role_family),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, title, company_name, location, salary_min_annual_jpy, "
                "       foreigner_fit_score, role_family "
                "FROM jobs WHERE id != ? "
                "  AND DATE(last_seen_at) >= DATE('now', '-30 days') "
                "ORDER BY COALESCE(foreigner_fit_score, 0) DESC LIMIT 5",
                (job_id,),
            ).fetchall()
    return jsonify({"jobs": [dict(r) for r in rows]})


@app.route("/resume")
def resume():
    return render_template("resume.html", section="resume", resume_tool="rirekisho")


@app.route("/resume/shokumu")
def resume_shokumu():
    return render_template("shokumu.html", section="resume", resume_tool="shokumu")


@app.route("/resume/cv")
def resume_cv():
    """English / Western CV builder. Renders in browser, print to PDF."""
    return render_template("cv.html", section="resume", resume_tool="cv")


@app.route("/resume/cover-letter")
def resume_cover_letter():
    """Cover letter builder. Accepts ?company= and ?role= for deep-linking
    from /job/<id>."""
    return render_template("cover_letter.html",
                           section="resume", resume_tool="cover_letter",
                           prefill_company=request.args.get("company", ""),
                           prefill_role=request.args.get("role", ""))


@app.route("/resume/bullets")
def resume_bullets():
    """Resume-bullet improver — rule-based feedback on weak bullets."""
    return render_template("bullets.html", section="resume", resume_tool="bullets")


@app.route("/templates")
def email_templates():
    """Bilingual email-template library for applications, follow-ups, thanks,
    negotiation, accepting/declining offers. Copy-to-clipboard for each.
    Accepts ?company= and ?role= to prefill placeholders."""
    return render_template("email_templates.html",
                           section="templates",
                           prefill_company=request.args.get("company", ""),
                           prefill_role=request.args.get("role", ""))


@app.route("/saved")
def saved():
    ids = _parse_ids(request.args.get("ids", ""))
    if not ids:
        return render_template("empty_state.html", section="jobs", view="saved",
                               title="No saved jobs yet",
                               body="Click the ☆ on any job card to save it for later. "
                                    "Saved jobs live in your browser only — no account needed.")
    return _query_and_render("index.html", only_ids=ids, view="saved")


@app.route("/applied")
def applied():
    ids = _parse_ids(request.args.get("ids", ""))
    if not ids:
        return render_template("empty_state.html", section="jobs", view="applied",
                               title="No applied jobs yet",
                               body="Click \"✓ Applied\" on a job card after you've applied "
                                    "to it, and it'll show up here so you can keep track.")
    return _query_and_render("index.html", only_ids=ids, view="applied")


@app.route("/archived")
def archived():
    """Shows DB-stale rows + manually-hidden rows (passed via ?ids=)."""
    hidden_ids = _parse_ids(request.args.get("ids", ""))
    return _query_and_render(
        "index.html",
        include_only_archived=True,
        extra_ids=hidden_ids,           # union into the query, see _query_and_render
        view="archived",
    )


_SCHEMA_EMPLOYMENT_TYPE = {
    "Full-time": "FULL_TIME", "Part-time": "PART_TIME", "Contract": "CONTRACTOR",
    "Temporary": "TEMPORARY", "Internship": "INTERN", "Freelance": "CONTRACTOR",
}


def _job_posting_jsonld(job: dict) -> Optional[dict]:
    """Build schema.org JobPosting from REAL DB fields only.

    Every optional field is omitted unless the data is genuinely present.
    No invented salary, validThrough, remote flag, or apply-location. Returns
    None when the minimum (title + a date) isn't available.
    """
    title = (job.get("title") or "").strip()
    date_posted = job.get("post_date") or (job.get("scraped_at") or "")[:10]
    if not title or not date_posted:
        return None

    data = {
        "@context": "https://schema.org/",
        "@type": "JobPosting",
        "title": title,
        "datePosted": date_posted,
        "url": f"{_base_url()}/job/{job['id']}",
        "identifier": {
            "@type": "PropertyValue",
            "name": job.get("source") or "Gaijin Hunter",
            "value": str(job.get("source_job_id") or job["id"]),
        },
    }

    desc = (job.get("description") or job.get("requirements") or "").strip()
    if desc:
        data["description"] = desc[:5000]

    et = _SCHEMA_EMPLOYMENT_TYPE.get(job.get("employment_terms"))
    if et:
        data["employmentType"] = et

    company = (job.get("company_name") or "").strip()
    if company:
        org = {"@type": "Organization", "name": company}
        data["hiringOrganization"] = org

    # jobLocation only when we have a real place string.
    loc = (job.get("location") or "").strip()
    pref = (job.get("prefecture") or "").strip()
    if loc or (pref and pref not in ("Remote / Anywhere", "Other / Japan")):
        addr = {"@type": "PostalAddress", "addressCountry": "JP"}
        region = pref if pref and pref not in ("Remote / Anywhere", "Other / Japan") else None
        if region:
            addr["addressRegion"] = region
        if loc:
            addr["addressLocality"] = loc[:120]
        data["jobLocation"] = {"@type": "Place", "address": addr}

    # Remote: only when the posting explicitly says so (provenance == explicit
    # or inferred 1). Google wants TELECOMMUTE as jobLocationType.
    if job.get("remote_work_ok") == 1:
        data["jobLocationType"] = "TELECOMMUTE"
        data["applicantLocationRequirements"] = {"@type": "Country", "name": "Japan"}

    # Apply from abroad -> broaden applicant location requirement honestly.
    if job.get("overseas_application_ok") == 1:
        data["applicantLocationRequirements"] = {"@type": "Country", "name": "Anywhere"}

    # baseSalary ONLY when we have a confidently parsed numeric annual figure.
    mn = job.get("salary_min_annual_jpy")
    mx = job.get("salary_max_annual_jpy")
    if mn:
        value = {"@type": "QuantitativeValue", "unitText": "YEAR"}
        if mx and mx != mn:
            value["minValue"] = int(mn)
            value["maxValue"] = int(mx)
        else:
            value["value"] = int(mn)
        data["baseSalary"] = {
            "@type": "MonetaryAmount", "currency": "JPY", "value": value,
        }

    # directApply: true only for employer-direct posts with a real apply target.
    if job.get("is_employer_post") == 1 and (job.get("application_url") or job.get("application_email")):
        data["directApply"] = True

    return data


@app.route("/job/<int:job_id>")
def job_detail(job_id: int):
    job = db.get_job(job_id)
    if not job:
        abort(404)
    import inference as _inf
    salary_ctx = db.salary_context_for_job(job)
    job_jsonld = _job_posting_jsonld(dict(job))
    return render_template("job.html", job=job,
                           fit_reason_labels=_inf.FIT_REASON_LABELS,
                           salary_ctx=salary_ctx,
                           job_jsonld=job_jsonld)


@app.route("/profile")
def profile():
    """Local profile + preferences (all state lives in localStorage)."""
    return render_template("profile.html", section="profile")


@app.route("/jobs/tracker")
def jobs_tracker():
    """Application tracker — now a tab inside the Jobs section (pipeline view).
    Job IDs and statuses come from localStorage; the page hits /api/jobs_by_ids
    to hydrate the rows on the client side."""
    return render_template("tracker.html", section="jobs", view="tracker")


@app.route("/tracker")
def tracker():
    """Standalone application tracker (kanban + table). Same template as the
    in-Jobs pipeline view; query strings like ?filter=followup_due are honoured
    client-side."""
    return render_template("tracker.html", section="jobs", view="tracker")


@app.route("/data")
def data_page():
    """Export / import everything stored locally (profile, saved, tracker,
    hidden, resume + shokumu builder data). All client-side."""
    return render_template("data.html", section="profile")


@app.route("/api/jobs_by_ids")
def api_jobs_by_ids():
    """Hydrate a comma-separated list of job IDs into a small JSON payload.
    Used by /tracker so the JS can render the pipeline without per-row HTTP."""
    ids = _parse_ids(request.args.get("ids", ""))
    rows = [db.get_job(i) for i in ids]
    rows = [dict(r) for r in rows if r is not None]
    return jsonify({"count": len(rows), "jobs": rows})


@app.route("/api/jobs.json")
def api_jobs():
    p = _read_filters_from_request()
    jobs = db.query_jobs(
        q=p["q"], filters=p["dropdowns"], flags=p["flags"],
        salary_min=p["salary_min"], days_within=p["days_within"],
        include_archived=p["include_archived"],
        sort=p["sort"],
        limit=min(500, int(request.args.get("limit", 100))),
        offset=int(request.args.get("offset", 0)),
    )
    total = db.count_jobs(
        q=p["q"], filters=p["dropdowns"], flags=p["flags"],
        salary_min=p["salary_min"], days_within=p["days_within"],
        include_archived=p["include_archived"],
    )
    return jsonify({
        "total": total,
        "count": len(jobs),
        "jobs": [dict(j) for j in jobs],
        "filters": {
            "q": p["q"], "salary_min": p["salary_min"],
            "days_within": p["days_within"], "sort": p["sort"],
            "dropdowns": p["dropdowns"], "flags": p["flags"],
        },
    })


# ---------------------------------------------------------------------------
# Template filters
# ---------------------------------------------------------------------------

# Boilerplate phrases worth stripping when they lead a scraped snippet. Kept
# deliberately short/conservative so we never eat real job description text.
_SNIPPET_BOILERPLATE = re.compile(
    r"^(?:job\s+description|about\s+the\s+role|about\s+the\s+job|role\s+overview|"
    r"position\s+overview|job\s+summary|summary|overview|description)\s*[:\-–—]\s*",
    re.IGNORECASE,
)


def clean_snippet_text(text: str, length: int = 220) -> str:
    """Display-only cleaner for scraped job snippets.

    Strips markdown artifacts, separator lines, HTML entities and excessive
    whitespace, trims a little leading boilerplate, then truncates to a word
    boundary near ``length`` (capped ~280). Never mutates stored data — this is
    purely for rendering job cards.
    """
    if not text:
        return ""

    # Decode HTML entities (e.g. &amp; &#39; &nbsp;) before anything else.
    text = html_module.unescape(str(text))

    # Drop fenced code markers and inline code backticks (keep the inner text).
    text = text.replace("```", " ").replace("`", "")

    # Strip markdown images/links, keeping link text: [label](url) -> label.
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)

    # Remove markdown heading hashes at the start of a line: '### Title' -> 'Title'.
    text = re.sub(r"(?m)^\s{0,3}#{1,6}\s*", "", text)

    # Remove blockquote markers and list bullets at line starts.
    text = re.sub(r"(?m)^\s{0,3}>\s?", "", text)
    text = re.sub(r"(?m)^\s{0,3}(?:[-*+•]|\d+[.)])\s+", "", text)

    # Strip bold/italic emphasis markers, keeping the inner text.
    text = re.sub(r"\*{1,3}([^*]+?)\*{1,3}", r"\1", text)
    text = re.sub(r"_{2,3}([^_]+?)_{2,3}", r"\1", text)
    # Single-underscore italics, but only with word boundaries so we never
    # mangle snake_case identifiers inside the text.
    text = re.sub(r"(?<!\w)_([^_\n]+?)_(?!\w)", r"\1", text)

    # Collapse horizontal-rule / separator lines (---, ___, ***, ====, repeated
    # dashes/underscores) into a space.
    text = re.sub(r"(?m)^\s*(?:[-_*=]\s*){2,}$", " ", text)
    text = re.sub(r"(?:--+|__+|\*\*+|==+)", " ", text)

    # Collapse all runs of whitespace (incl. newlines) into single spaces.
    text = re.sub(r"\s+", " ", text).strip()

    # Conservative leading-boilerplate trim (only an obvious leading label).
    text = _SNIPPET_BOILERPLATE.sub("", text).strip()

    if not text:
        return ""

    # Truncate at a word boundary at or before `length` (never overshoot, so
    # explicit small limits like snippet(40) stay tight). Soft window keeps the
    # break from landing too early when a long token sits near the cut.
    if len(text) > length:
        cut = text[:length]
        sp = cut.rfind(" ")
        if sp >= length * 0.6:
            cut = cut[:sp]
        text = cut.rstrip()
        # Drop trailing punctuation/separators before adding the ellipsis.
        text = re.sub(r"[\s\-–—,;:.]+$", "", text)
        text = text + "…"
    else:
        # Clean any messy trailing ellipsis already in the source.
        text = re.sub(r"\s*\.{3,}\s*$", "…", text)
        text = re.sub(r"\s*…+\s*$", "…", text)

    return text


@app.template_filter("snippet")
def snippet(text: str, length: int = 220) -> str:
    return clean_snippet_text(text, length)


@app.template_filter("yen_short")
def yen_short(value) -> str:
    """3000000 -> '¥3.0M', 250000 -> '¥250K'."""
    try:
        n = int(value)
    except (TypeError, ValueError):
        return ""
    if n >= 1_000_000:
        return f"¥{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"¥{n // 1_000}K"
    return f"¥{n}"


@app.template_filter("keep_querystring")
def keep_querystring(args, **overrides):
    pairs = []
    skip_overridden = {k for k in overrides}
    for k, v in args.items(multi=True):
        if k in skip_overridden:
            continue
        if v:
            pairs.append((k, v))
    for k, v in overrides.items():
        if v is None or v == "":
            continue
        pairs.append((k, v))
    return urlencode(pairs)


@app.template_filter("remove_value")
def remove_value(args, key: str, value: str) -> str:
    """Drop a single (key, value) pair from the querystring, preserving every
    other param — including other values of the same multi-select key. Also
    strips `page` so removing a filter returns to page 1."""
    pairs = []
    for k, v in args.items(multi=True):
        if k == "page":
            continue
        if k == key and v == value:
            continue
        if v:
            pairs.append((k, v))
    return urlencode(pairs)


@app.template_filter("chip_querystring")
def chip_querystring(args, params: dict) -> str:
    """Build a querystring that takes the current args and applies chip params on top."""
    pairs = []
    override_keys = set(params.keys())
    for k, v in args.items(multi=True):
        if k in override_keys or k == "page":
            continue
        if v:
            pairs.append((k, v))
    for k, v in params.items():
        if v:
            pairs.append((k, v))
    return urlencode(pairs)


# ---------------------------------------------------------------------------
# Employer-direct job posting flow (/post-a-job + /employer/manage/<token>)
# ---------------------------------------------------------------------------

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _valid_email(value: str) -> bool:
    value = (value or "").strip()
    return bool(value) and len(value) <= 200 and bool(_EMAIL_RE.match(value))


def _valid_http_url(value: str) -> bool:
    value = (value or "").strip()
    if not value or len(value) > 2000:
        return False
    try:
        from urllib.parse import urlparse
        u = urlparse(value)
        return u.scheme in ("http", "https") and bool(u.netloc)
    except (ValueError, TypeError):
        return False


def _parse_optional_int(val):
    if not val:
        return None
    try:
        return int(str(val).replace(",", "").strip())
    except (ValueError, TypeError):
        return None


def _checkbox_to_int(val):
    """Form checkbox: '1', 'on', 'true' -> 1; anything else (including missing) -> None."""
    if val is None:
        return None
    s = str(val).strip().lower()
    if s in ("1", "on", "true", "yes"):
        return 1
    if s in ("0", "off", "false", "no"):
        return 0
    return None


# Common select option lists for the employer form
EMPLOYMENT_TERMS_OPTIONS = ["Full-time", "Part-time", "Contract", "Internship", "Freelance"]
JAPANESE_LEVEL_OPTIONS = [
    "None required", "Basic / N5", "Conversational / N4",
    "Business / N3", "Business / N2", "Native / N1", "Fluent / N1+",
]
ENGLISH_LEVEL_OPTIONS = [
    "None required", "Basic", "Conversational", "Business", "Fluent / Native",
]
ROLE_FAMILY_OPTIONS = [
    "Software Engineering", "Data & AI", "Product Management", "Design / UX",
    "Marketing & Growth", "Sales & Business Development", "Finance & Accounting",
    "Customer Success / Support", "Operations", "HR / Talent",
    "Teaching / Education", "Engineering (Hardware)", "Research", "Other",
]


@app.route("/post-a-job", methods=["GET"])
def post_a_job_form():
    return render_template(
        "post_a_job.html",
        section="post-a-job",
        employment_terms=EMPLOYMENT_TERMS_OPTIONS,
        japanese_levels=JAPANESE_LEVEL_OPTIONS,
        english_levels=ENGLISH_LEVEL_OPTIONS,
        role_families=ROLE_FAMILY_OPTIONS,
        duration_days=db.EMPLOYER_POST_DURATION_DAYS,
    )


@app.route("/post-a-job", methods=["POST"])
@limiter.limit("5 per hour")
def post_a_job_submit():
    form = request.form

    # Honeypot: legitimate users never fill 'website' (CSS-hidden in the form).
    if form.get("website", "").strip():
        abort(400)

    # Required field validation
    required = ["title", "company_name", "location", "description",
                "employer_contact_email", "employer_contact_name"]
    errors = {}
    for f in required:
        if not form.get(f, "").strip():
            errors[f] = "Required"

    email = form.get("employer_contact_email", "").strip()
    if email and not _valid_email(email):
        errors["employer_contact_email"] = "Enter a valid email address"

    apply_email = form.get("application_email", "").strip()
    if apply_email and not _valid_email(apply_email):
        errors["application_email"] = "Enter a valid email address"

    # Length sanity per field (prevents oversized payloads / junk).
    for field, cap in (("title", 200), ("company_name", 200), ("company_name_jp", 200),
                       ("location", 200), ("employer_contact_name", 120),
                       ("requirements", 20000), ("description", 20000),
                       ("industries", 300), ("salary", 120)):
        v = form.get(field, "")
        if v and len(v) > cap:
            errors[field] = f"Maximum {cap:,} characters"

    # Validate optional URLs (apply link must be http/https if provided).
    for field in ("application_url",):
        v = form.get(field, "").strip()
        if v and not _valid_http_url(v):
            errors[field] = "Enter a valid http(s) URL"

    if errors:
        return render_template(
            "post_a_job.html",
            section="post-a-job",
            employment_terms=EMPLOYMENT_TERMS_OPTIONS,
            japanese_levels=JAPANESE_LEVEL_OPTIONS,
            english_levels=ENGLISH_LEVEL_OPTIONS,
            role_families=ROLE_FAMILY_OPTIONS,
            duration_days=db.EMPLOYER_POST_DURATION_DAYS,
            errors=errors,
            form=form,
        )

    data = {
        "title": form["title"].strip(),
        "company_name": form["company_name"].strip(),
        "company_name_jp": (form.get("company_name_jp") or "").strip() or None,
        "location": form["location"].strip(),
        "description": form["description"].strip(),
        "requirements": (form.get("requirements") or "").strip() or None,
        "employer_contact_email": email,
        "employer_contact_name": form["employer_contact_name"].strip(),
        "employment_terms": form.get("employment_terms") or "Full-time",
        "japanese_level": form.get("japanese_level") or None,
        "english_level": form.get("english_level") or None,
        "role_family": form.get("role_family") or None,
        "salary": (form.get("salary") or "").strip() or None,
        "salary_min_annual_jpy": _parse_optional_int(form.get("salary_min")),
        "salary_max_annual_jpy": _parse_optional_int(form.get("salary_max")),
        "industries": (form.get("industries") or "").strip() or None,
        "remote_work_ok": _checkbox_to_int(form.get("remote_work_ok")),
        "visa_sponsorship_mentioned": _checkbox_to_int(form.get("visa_sponsorship")),
        "overseas_application_ok": _checkbox_to_int(form.get("overseas_application_ok")),
        "application_url": (form.get("application_url") or "").strip() or None,
        "application_email": (form.get("application_email") or "").strip() or None,
    }

    result = db.create_employer_post(data)

    # Redirect to the confirmation/manage page so the employer sees their token URL
    return redirect(url_for("employer_manage", token=result["manage_token"]))


@app.route("/employer/manage/<token>", methods=["GET"])
def employer_manage(token):
    post = db.get_employer_post_by_token(token)
    if not post:
        abort(404)
    return render_template(
        "employer_manage.html",
        section="employer",
        post=dict(post),
        token=token,
        employment_terms=EMPLOYMENT_TERMS_OPTIONS,
        japanese_levels=JAPANESE_LEVEL_OPTIONS,
        english_levels=ENGLISH_LEVEL_OPTIONS,
        role_families=ROLE_FAMILY_OPTIONS,
        duration_days=db.EMPLOYER_POST_DURATION_DAYS,
    )


@app.route("/employer/manage/<token>/withdraw", methods=["POST"])
@limiter.limit("20 per hour")
def employer_withdraw(token):
    if not db.get_employer_post_by_token(token):
        abort(404)
    db.withdraw_employer_post(token)
    return redirect(url_for("employer_manage", token=token, msg="withdrawn"))


@app.route("/employer/manage/<token>/reactivate", methods=["POST"])
@limiter.limit("20 per hour")
def employer_reactivate(token):
    if not db.get_employer_post_by_token(token):
        abort(404)
    db.reactivate_employer_post(token)
    return redirect(url_for("employer_manage", token=token, msg="reactivated"))


@app.route("/employer/manage/<token>/extend", methods=["POST"])
@limiter.limit("20 per hour")
def employer_extend(token):
    if not db.get_employer_post_by_token(token):
        abort(404)
    db.extend_employer_post(token, days=db.EMPLOYER_POST_DURATION_DAYS)
    return redirect(url_for("employer_manage", token=token, msg="extended"))


@app.route("/employer/manage/<token>/edit", methods=["POST"])
@limiter.limit("20 per hour")
def employer_edit(token):
    if not db.get_employer_post_by_token(token):
        abort(404)
    form = request.form
    updates = {
        "title": form.get("title", "").strip() or None,
        "location": form.get("location", "").strip() or None,
        "description": form.get("description", "").strip() or None,
        "requirements": form.get("requirements", "").strip() or None,
        "salary": (form.get("salary") or "").strip() or None,
        "salary_min_annual_jpy": _parse_optional_int(form.get("salary_min")),
        "salary_max_annual_jpy": _parse_optional_int(form.get("salary_max")),
        "employment_terms": form.get("employment_terms") or None,
        "japanese_level": form.get("japanese_level") or None,
        "english_level": form.get("english_level") or None,
        "role_family": form.get("role_family") or None,
        "remote_work_ok": _checkbox_to_int(form.get("remote_work_ok")),
        "visa_sponsorship_mentioned": _checkbox_to_int(form.get("visa_sponsorship")),
        "application_url": (form.get("application_url") or "").strip() or None,
        "application_email": (form.get("application_email") or "").strip() or None,
    }
    # Drop Nones for fields where the value should remain as-is
    updates = {k: v for k, v in updates.items() if v is not None or k in {
        "remote_work_ok", "visa_sponsorship_mentioned",
    }}
    db.update_employer_post(token, updates)
    return redirect(url_for("employer_manage", token=token, msg="updated"))


@app.route("/api/employer/cleanup", methods=["POST"])
@limiter.limit("20 per hour")
def employer_cleanup():
    """Internal endpoint: mark expired employer posts as expired.

    Intended to be called by cron. Returns count of rows updated.
    """
    n = db.cleanup_expired_employer_posts()
    return jsonify({"expired": n})


# ---------------------------------------------------------------------------
# Health, errors, privacy
# ---------------------------------------------------------------------------

@app.route("/healthz")
def healthz():
    """Liveness + basic data freshness for deploy health checks."""
    try:
        with db.connect() as conn:
            total = conn.execute("SELECT COUNT(*) AS n FROM jobs").fetchone()["n"]
            last = conn.execute("SELECT MAX(last_seen_at) AS t FROM jobs").fetchone()["t"]
        return jsonify({"status": "ok", "jobs": total, "last_seen_at": last,
                        "env": config.ENV}), 200
    except Exception as e:                                # pragma: no cover
        logging.getLogger("app").exception("healthz failed")
        return jsonify({"status": "error", "error": str(e)[:200]}), 500


@app.route("/privacy")
def privacy():
    return render_template("privacy.html", section="privacy")


@app.errorhandler(429)
def too_many_requests(e):
    msg = "Too many requests. Please try again later."
    # JSON for API/XHR callers, a friendly page for form posts.
    if request.path.startswith("/api/") or "application/json" in request.headers.get("Accept", ""):
        return jsonify({"ok": False, "error": msg}), 429
    return render_template("error.html", code=429,
                           title="Too many requests",
                           message=msg + " If you're filling out a form, wait a "
                                   "few minutes before submitting again."), 429


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", code=404,
                           title="Page not found",
                           message="That page doesn't exist — it may have been "
                                   "moved, or the job may no longer be listed."), 404


@app.errorhandler(500)
def server_error(e):                                      # pragma: no cover
    logging.getLogger("app").exception("500 on %s", request.path)
    return render_template("error.html", code=500,
                           title="Something went wrong",
                           message="An unexpected error occurred. It's been "
                                   "logged. Your saved jobs, tracker and resume "
                                   "data live in your browser and are unaffected."), 500


if __name__ == "__main__":
    db.init_db()
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
