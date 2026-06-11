"""
TokyoDev scraper.

TokyoDev (https://www.tokyodev.com/jobs) lists all open positions on a single
server-rendered page, grouped by company. Every metadata field is a link whose
href encodes the field type:

    /jobs/salary-data            -> salary range (link text)
    /jobs/japanese-required      -> Japanese level required (Business/Conversational/Basic Japanese)
    /jobs/no-japanese-required   -> 'No Japanese required'
    /jobs/apply-from-abroad      -> overseas_application_ok = 1
    /jobs/residents-only         -> overseas_application_ok = 0
    /jobs/fully-remote           -> remote_work_ok = 1 (fully)
    /jobs/partially-remote       -> remote_work_ok = 1 (partial)
    /jobs/no-remote              -> remote_work_ok = 0
    /jobs/<anything else>        -> a tech tag (React, AWS, Python, ...)

Job-detail URL pattern: /companies/<company-slug>/jobs/<job-slug>
Company-link pattern:    /companies/<company-slug>   (without /jobs/...)

Strategy:
  1. One HTTP GET to the listing page (no pagination — they fit it all on one page).
  2. Walk the DOM linearly. Each time we see an anchor whose href is a company
     URL (no /jobs/...), update current company. Each time we see an anchor whose
     href is a job-detail URL, emit a new job. Subsequent metadata anchors
     between this job and the next job belong to this job.
  3. Bucket each metadata anchor by href category. Normalize the language level.
  4. Upsert via db.upsert_job with source='tokyodev'.

Usage:
    python tokyodev_scraper.py [--limit N] [--debug] [--dry-run] [-v]
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

import random

import requests
from bs4 import BeautifulSoup

import db
import proxies as proxy_mod
import salary_parser

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SOURCE_NAME = "tokyodev"
BASE = "https://www.tokyodev.com"
LISTING_URL = "https://www.tokyodev.com/jobs"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Patterns over href paths
JOB_URL_RE = re.compile(r"^/companies/([^/]+)/jobs/([^/?#]+)/?$")
COMPANY_URL_RE = re.compile(r"^/companies/([^/?#]+)/?$")

# Metadata href -> field bucket. Order matters for the language category, where
# we also need the link text to determine "Business Japanese" vs. "Basic".
META_PATHS = {
    "/jobs/salary-data":          "salary",
    "/jobs/japanese-required":    "jp_required",       # text gives the level
    "/jobs/no-japanese-required": "jp_none",
    "/jobs/apply-from-abroad":    "overseas_ok",
    "/jobs/residents-only":       "overseas_no",
    "/jobs/fully-remote":         "remote_full",
    "/jobs/partially-remote":     "remote_partial",
    "/jobs/no-remote":            "remote_no",
}

DEBUG_DIR = Path(__file__).parent / "debug"
log = logging.getLogger("tokyodev_scraper")


# ---------------------------------------------------------------------------
# Field normalization
# ---------------------------------------------------------------------------

# Match the JP-level normalization in scraper.py so filter dropdowns stay
# consistent across sources.
JP_LEVEL_NORMALIZE = {
    "business japanese":      "Business / Professional",
    "conversational japanese": "Conversational",
    "basic japanese":         "Basic / Beginner",
    "no japanese required":   "Not Required",
}


def normalize_jp_level(text: str) -> Optional[str]:
    key = text.strip().lower()
    return JP_LEVEL_NORMALIZE.get(key, text.strip() or None)


def _norm(s: Optional[str]) -> str:
    return re.sub(r"\s+", " ", s).strip() if s else ""


def _href_path(a) -> str:
    """Get the path portion of an anchor's href, dropping host/scheme/qs/frag."""
    href = (a.get("href") or "").strip()
    if not href:
        return ""
    parsed = urlparse(href)
    return parsed.path or ""


# Detail-page normalization for the emoji-bullet language line, e.g.
# "Business Japanese", "Native English", "No English required".
DETAIL_LANG_PATTERNS = [
    (r"\b(native|fluent)\b",         "Native / Fluent"),
    (r"\bbusiness\b",                "Business / Professional"),
    (r"\bconversational\b",          "Conversational"),
    (r"\bbasic\b",                   "Basic / Beginner"),
    (r"\b(no [a-z]+ required|not required)\b", "Not Required"),
]


def normalize_detail_lang_level(line: str) -> Optional[str]:
    s = line.strip().lower()
    for pat, label in DETAIL_LANG_PATTERNS:
        if re.search(pat, s):
            return label
    return line.strip() or None


def _employment_terms_from_jsonld(et: str) -> Optional[str]:
    """Map schema.org employmentType (FULL_TIME, PART_TIME, ...) to our label."""
    if not et:
        return None
    et_lower = et.lower().replace("_", "-").replace(" ", "-")
    mapping = [
        ("full-time", "Full-time"), ("fulltime", "Full-time"),
        ("part-time", "Part-time"), ("parttime", "Part-time"),
        ("contractor", "Contract"), ("contract", "Contract"),
        ("temporary", "Temporary"),
        ("internship", "Internship"), ("intern", "Internship"),
        ("freelance", "Freelance"),
    ]
    for needle, label in mapping:
        if needle in et_lower:
            return label
    return et.title()


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_listing(html: str) -> list[dict]:
    """
    Walk the document linearly. Keep `current_company` updated from company
    anchors; emit a job dict each time we see a job-detail anchor that is
    inside a heading (h2/h3/h4) — these are the job titles, not in-body links.
    Metadata anchors after the current job (and before the next job/company)
    populate its fields.
    """
    soup = BeautifulSoup(html, "lxml")

    jobs: list[dict] = []
    current_company: Optional[dict] = None
    current_job: Optional[dict] = None

    for a in soup.find_all("a", href=True):
        path = _href_path(a)
        if not path:
            continue

        # Job-detail anchor inside a heading -> emit a new job
        m_job = JOB_URL_RE.match(path)
        if m_job and a.find_parent(["h2", "h3", "h4", "h5"]):
            company_slug, job_slug = m_job.group(1), m_job.group(2)
            current_job = {
                "source": SOURCE_NAME,
                "url": urljoin(BASE, path),
                "source_job_id": f"{company_slug}/{job_slug}",
                "title": re.sub(r"\s+", " ", a.get_text(" ", strip=True)),
                "company_name": (current_company or {}).get("name"),
                "company_name_jp": None,
                "salary": None,
                "japanese_level": None,
                "overseas_application_ok": None,
                "remote_work_ok": None,
                "remote_kind": None,
                "tags": [],
            }
            jobs.append(current_job)
            continue

        # Company anchor inside a heading -> update current company
        m_co = COMPANY_URL_RE.match(path)
        if m_co and a.find_parent(["h2", "h3", "h4", "h5"]):
            current_company = {
                "slug": m_co.group(1),
                "name": re.sub(r"\s+", " ", a.get_text(" ", strip=True)),
            }
            # The next emitted job inherits this company.
            continue

        # Metadata anchor — attach to current job if any.
        if current_job is None:
            continue

        bucket = META_PATHS.get(path)
        text = re.sub(r"\s+", " ", a.get_text(" ", strip=True))

        if bucket == "salary":
            current_job["salary"] = text
        elif bucket == "jp_required":
            current_job["japanese_level"] = normalize_jp_level(text)
        elif bucket == "jp_none":
            current_job["japanese_level"] = "Not Required"
        elif bucket == "overseas_ok":
            current_job["overseas_application_ok"] = 1
        elif bucket == "overseas_no":
            current_job["overseas_application_ok"] = 0
        elif bucket == "remote_full":
            current_job["remote_work_ok"] = 1
            current_job["remote_kind"] = "Fully remote"
        elif bucket == "remote_partial":
            current_job["remote_work_ok"] = 1
            current_job["remote_kind"] = "Partially remote"
        elif bucket == "remote_no":
            current_job["remote_work_ok"] = 0
            current_job["remote_kind"] = "Onsite"
        elif path.startswith("/jobs/") and not path.endswith("/"):
            # Generic tech tag (any other /jobs/<slug>). Ignore the meta-link
            # for the page's filter sidebar at the very top, by requiring a
            # current_job to be set (we already guarded above).
            tag = text.strip()
            if tag and tag not in current_job["tags"]:
                current_job["tags"].append(tag)

    # Finalize: turn tag lists into comma-strings, parse salary into numeric
    # columns (for sort/filter), fill required fields, timestamp.
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    out: list[dict] = []
    for j in jobs:
        if not j.get("title"):
            continue
        j["tags"] = ", ".join(j["tags"]) if j["tags"] else None
        # Numeric salary. TokyoDev listings don't specify period — assume
        # annual unless we later detect otherwise from the detail page.
        lo, hi = salary_parser.parse_range(j.get("salary"))
        j["salary_min_jpy"] = lo
        j["salary_max_jpy"] = hi
        # Annualized at Year (the listing default); detail page can override.
        j["salary_min_annual_jpy"] = lo
        j["salary_max_annual_jpy"] = hi
        if not j.get("salary_period") and lo:
            j["salary_period"] = "Year"
        j["scraped_at"] = now
        j["last_seen_at"] = now
        out.append(j)
    return out


# ---------------------------------------------------------------------------
# Detail-page enrichment
# ---------------------------------------------------------------------------

def _extract_jsonld_jobposting(soup: BeautifulSoup) -> Optional[dict]:
    """Return the first schema.org/JobPosting JSON-LD object on the page."""
    for tag in soup.find_all("script", type="application/ld+json"):
        raw = tag.string or tag.get_text() or ""
        try:
            data = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            continue
        candidates = data if isinstance(data, list) else [data]
        # @graph wrapper is common
        flat = []
        for c in candidates:
            if isinstance(c, dict) and isinstance(c.get("@graph"), list):
                flat.extend(c["@graph"])
            else:
                flat.append(c)
        for d in flat:
            if not isinstance(d, dict):
                continue
            t = d.get("@type") or d.get("type")
            types = t if isinstance(t, list) else [t]
            if any(str(x) == "JobPosting" for x in types):
                return d
    return None


_HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5"}


def _collect_section_items(soup: BeautifulSoup, heading_text: str) -> list[str]:
    """
    Find a heading whose normalized text matches `heading_text` (case-insensitive)
    and return bullet items from the first <ul>/<ol> in that section. If there
    isn't a list, fall back to the section's paragraphs.

    Sections are bounded: iteration stops at the NEXT heading of any level so we
    never bleed into a sibling section's content (e.g. "About the position" must
    not steal items from the "Requirements" list that follows it).
    """
    target = heading_text.lower().strip()
    for el in soup.find_all(_HEADING_TAGS):
        if _norm(el.get_text()).lower() != target:
            continue
        items: list[str] = []
        paragraphs: list[str] = []
        for sib in el.find_all_next():
            if sib.name in _HEADING_TAGS:
                break  # next section starts here
            if sib.name in ("ul", "ol") and not items:
                items = [_norm(li.get_text(" ", strip=True))
                         for li in sib.find_all("li", recursive=False)]
                items = [i for i in items if i]
            elif sib.name == "p":
                t = _norm(sib.get_text(" ", strip=True))
                if t:
                    paragraphs.append(t)
        if items:
            return items
        if paragraphs:
            return paragraphs
        return []
    return []


# Career-level extraction: pull just the seniority label out of lines like
# "Senior level Unspecified years of experience" or "Mid-level 3+ years".
_CAREER_LEVEL_RE = re.compile(
    r"\b("
    r"entry[- ]level|junior(?:[- ]level)?|associate(?:[- ]level)?|"
    r"mid[- ]?level|intermediate|"
    r"senior(?:[- ]level)?|staff|lead|principal|"
    r"manager|director"
    r")\b",
    re.IGNORECASE,
)


def extract_career_level(line: str) -> Optional[str]:
    m = _CAREER_LEVEL_RE.search(line)
    if not m:
        return None
    raw = m.group(1).lower()
    # Canonicalize for clean filter dropdowns.
    canon = {
        "entry-level": "Entry level", "entry level": "Entry level",
        "junior": "Junior", "junior-level": "Junior", "junior level": "Junior",
        "associate": "Associate", "associate-level": "Associate", "associate level": "Associate",
        "mid-level": "Mid-level", "midlevel": "Mid-level", "mid level": "Mid-level",
        "intermediate": "Mid-level",
        "senior": "Senior", "senior-level": "Senior", "senior level": "Senior",
        "staff": "Staff", "lead": "Lead", "principal": "Principal",
        "manager": "Manager", "director": "Director",
    }
    return canon.get(raw, raw.title())


def enrich_from_detail(job: dict, html: str) -> None:
    """
    Update `job` in-place with fields from the detail page. Listing-derived
    fields (salary, japanese_level, remote_work_ok, etc.) are NOT clobbered;
    detail data only fills in what's missing.
    """
    soup = BeautifulSoup(html, "lxml")

    # ----- 1. JSON-LD JobPosting (preferred when present) -------------------
    posting = _extract_jsonld_jobposting(soup)
    if posting:
        if posting.get("description") and not job.get("description"):
            desc_text = BeautifulSoup(str(posting["description"]), "lxml").get_text(" ", strip=True)
            job["description"] = _norm(desc_text)[:20_000]
        if posting.get("datePosted") and not job.get("post_date"):
            job["post_date"] = str(posting["datePosted"])[:10]
        if posting.get("employmentType") and not job.get("employment_terms"):
            et = posting["employmentType"]
            if isinstance(et, list):
                et = et[0] if et else None
            if et:
                job["employment_terms"] = _employment_terms_from_jsonld(str(et))

        # Refine location with a more precise address than the listing has.
        loc = posting.get("jobLocation")
        if isinstance(loc, list) and loc:
            loc = loc[0]
        if isinstance(loc, dict):
            addr = loc.get("address", {})
            if isinstance(addr, dict):
                parts = [addr.get("addressLocality"), addr.get("addressRegion"),
                         addr.get("addressCountry")]
                joined = ", ".join(p for p in parts if p)
                if joined:
                    job["location"] = joined

        # Salary: each piece is filled in only if the listing didn't already
        # have it. salary_period in particular is rarely on the listing, so we
        # set it independently from salary.
        bs = posting.get("baseSalary")
        if isinstance(bs, dict):
            val = bs.get("value") if isinstance(bs.get("value"), dict) else bs
            if isinstance(val, dict):
                lo, hi = val.get("minValue"), val.get("maxValue")
                unit = val.get("unitText") or ""
                currency = bs.get("currency", "JPY")
                sign = "¥" if currency == "JPY" else f"{currency} "
                if lo and hi and not job.get("salary"):
                    job["salary"] = f"{sign}{int(lo):,} - {sign}{int(hi):,}"
                if unit and not job.get("salary_period"):
                    job["salary_period"] = str(unit).capitalize()

    # ----- 2. Emoji-bullet metadata: english_level, career_level, salary_period
    for li in soup.find_all("li"):
        lines = [_norm(s) for s in li.stripped_strings if _norm(s)]
        if not lines:
            continue
        joined_lower = " | ".join(lines).lower()

        # Language line: "Business Japanese" / "Business English" / "No English required"
        has_lang = ("japanese" in joined_lower or "english" in joined_lower)
        has_level = any(w in joined_lower for w in
                        ("native", "fluent", "business", "conversational", "basic",
                         "not required", "no japanese", "no english"))
        if has_lang and has_level:
            for line in lines:
                low = line.lower()
                if "japanese" in low and not job.get("japanese_level"):
                    job["japanese_level"] = normalize_detail_lang_level(line)
                if "english" in low and not job.get("english_level"):
                    job["english_level"] = normalize_detail_lang_level(line)

        # Career line: e.g. "Senior level Unspecified years of experience".
        # Strip the emoji and the years-of-experience tail; keep just the
        # canonical seniority label for clean filtering.
        if not job.get("career_level"):
            for line in lines:
                level = extract_career_level(line)
                if level:
                    job["career_level"] = level
                    break

        # Salary period in the salary line ("¥X ~ ¥Y annually" / "monthly")
        if not job.get("salary_period"):
            for line in lines:
                low = line.lower()
                if re.search(r"\bannually|per\s*year\b", low):
                    job["salary_period"] = "Year"
                    break
                if re.search(r"\bmonthly|per\s*month\b", low):
                    job["salary_period"] = "Month"
                    break
                if re.search(r"\bhourly|per\s*hour\b", low):
                    job["salary_period"] = "Hour"
                    break

    # If detail page revealed a non-annual period, re-annualize the numeric
    # salary columns so sort-by-salary stays apples-to-apples.
    period = job.get("salary_period")
    if period and period != "Year":
        if job.get("salary_min_jpy") is not None:
            job["salary_min_annual_jpy"] = salary_parser.annualize(job["salary_min_jpy"], period)
        if job.get("salary_max_jpy") is not None:
            job["salary_max_annual_jpy"] = salary_parser.annualize(job["salary_max_jpy"], period)

    # ----- 3. Requirements bullet list as its own field ---------------------
    req_items = _collect_section_items(soup, "Requirements")
    if req_items and not job.get("requirements"):
        job["requirements"] = "\n".join(req_items)

    # ----- 4. Description: assemble body sections if JSON-LD didn't fill it
    if not job.get("description"):
        sections = []
        for section in ("About the position", "Who We're Looking For",
                        "Responsibilities", "Tools Used", "Nice to haves",
                        "Compensation"):
            items = _collect_section_items(soup, section)
            if items:
                body = "\n".join(f"- {i}" for i in items)
                sections.append(f"{section}:\n{body}")
        if sections:
            job["description"] = "\n\n".join(sections)[:20_000]


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

# HTTP status codes that mean "back off and try again" — these are the
# rate-limit / temporary-block codes TokyoDev (and Cloudflare) tend to emit.
_RETRYABLE_STATUS = {403, 408, 429, 502, 503, 504}


def _fetch(url: str, session: requests.Session, timeout: int = 20,
           pool: Optional["proxy_mod.ProxyPool"] = None,
           max_retries: int = 3) -> Optional[str]:
    """
    GET with retries-and-backoff and optional proxy rotation.

    For each attempt:
      • If a proxy pool is provided, pull the next available proxy. When it
        gets a retryable response, we mark it failed (cooldown) so the next
        attempt uses a different one.
      • If no proxy pool / all proxies cooling down, fall back to direct.
      • On retryable response, sleep `2 ** attempt + jitter` and retry.
      • On non-retryable non-200, return None immediately.
    """
    last_status = None
    for attempt in range(max_retries):
        proxy = pool.next() if pool else None
        kwargs = proxy_mod.ProxyPool.requests_kwargs(proxy) if proxy else {}
        try:
            r = session.get(url, headers=HEADERS, timeout=timeout, **kwargs)
        except requests.RequestException as e:
            log.warning("request error (attempt %d/%d, proxy=%s): %s -> %s",
                        attempt + 1, max_retries, proxy, url, e)
            if proxy and pool:
                pool.mark_failed(proxy)
            time.sleep(2 ** attempt + random.uniform(0, 1.0))
            continue

        if r.status_code == 200:
            return r.text

        last_status = r.status_code
        if r.status_code in _RETRYABLE_STATUS:
            log.warning("retryable %d (attempt %d/%d, proxy=%s): %s",
                        r.status_code, attempt + 1, max_retries, proxy, url)
            if proxy and pool:
                pool.mark_failed(proxy)
            # Exponential backoff with jitter
            time.sleep(2 ** attempt + random.uniform(0, 1.5))
            continue

        # Non-retryable non-200 — give up
        log.warning("non-200: %s -> %s", url, r.status_code)
        return None

    log.warning("all %d attempts failed for %s (last status=%s)",
                max_retries, url, last_status)
    return None


def run(delay: float, debug: bool, dry_run: bool, limit: Optional[int],
        enrich: bool = True, enrich_delay: float = 2.0) -> dict:
    """
    enrich defaults to True because the TokyoDev listing alone is missing
    English level, career level, post date, full description, and
    requirements — all of which live on detail pages. Pass enrich=False
    only for quick iteration / sanity checks.
    """
    db.init_db()
    if debug:
        DEBUG_DIR.mkdir(exist_ok=True)

    session = requests.Session()
    pool = proxy_mod.ProxyPool(proxy_mod.load_proxies())
    if pool:
        log.info("using %d proxies for rotation", len(pool))

    log.info("fetching %s", LISTING_URL)
    listing_html = _fetch(LISTING_URL, session, timeout=30, pool=pool)
    if not listing_html:
        return {"inserted": 0, "updated": 0, "enriched": 0, "failed": 1, "skipped": 0}

    if debug:
        (DEBUG_DIR / "tokyodev_listing.html").write_text(listing_html, encoding="utf-8")

    jobs = parse_listing(listing_html)
    log.info("parsed %d jobs from listing", len(jobs))
    if limit:
        jobs = jobs[:limit]

    stats = {"inserted": 0, "updated": 0, "enriched": 0, "failed": 0, "skipped": 0}

    # Optional: enrich each job with detail-page fields (english_level, career_level,
    # description, requirements, precise location, post_date, salary_period).
    if enrich:
        log.info("enriching %d jobs from detail pages (delay=%.1fs)…", len(jobs), enrich_delay)
        for i, j in enumerate(jobs, 1):
            time.sleep(enrich_delay) if i > 1 else None
            html = _fetch(j["url"], session, timeout=20, pool=pool)
            if not html:
                log.warning("enrich [%d/%d] FAILED: %s", i, len(jobs), j["url"])
                continue
            if debug and i <= 3:
                slug = re.sub(r"[^a-z0-9]+", "_", j["url"].lower())[-60:]
                (DEBUG_DIR / f"tokyodev_detail_{slug}.html").write_text(html, encoding="utf-8")
            try:
                enrich_from_detail(j, html)
                stats["enriched"] += 1
                if i % 25 == 0 or i == len(jobs):
                    log.info("enriched %d/%d", i, len(jobs))
            except Exception as e:
                log.exception("enrich failed for %s: %s", j["url"], e)

    if dry_run:
        for j in jobs:
            log.info("[dry-run] %s | %s | jp=%s | en=%s | career=%s | post=%s",
                     j.get("title"), j.get("company_name"),
                     j.get("japanese_level"), j.get("english_level"),
                     j.get("career_level"), j.get("post_date"))
        return stats

    with db.connect() as conn:
        for i, j in enumerate(jobs, 1):
            j.pop("remote_kind", None)  # informational only, not a column
            try:
                result = db.upsert_job(conn, j)
                stats[result] += 1
            except Exception as e:
                log.exception("upsert failed for %s: %s", j.get("url"), e)
                stats["failed"] += 1
            if i % 25 == 0:
                log.info("%d/%d upserted", i, len(jobs))

    return stats


def main() -> int:
    p = argparse.ArgumentParser(description="Scrape TokyoDev jobs into SQLite.")
    p.add_argument("--limit", type=int, default=None,
                   help="Cap total jobs processed (useful when --enrich is on).")
    p.add_argument("--delay", type=float, default=1.0,
                   help="(unused; listing is a single request)")
    # Enrichment is on by default — the listing is missing English level,
    # career level, post date, description, requirements. --no-enrich is for
    # fast iteration; --enrich is kept as a no-op for back-compat.
    p.add_argument("--enrich",    action="store_true", default=True,
                   help="(default) Fetch each detail page for full fields.")
    p.add_argument("--no-enrich", dest="enrich", action="store_false",
                   help="Skip detail-page enrichment (listing data only).")
    p.add_argument("--enrich-delay", type=float, default=2.0,
                   help="Seconds between detail-page fetches (default 2.0). "
                        "Crank this up if you're hitting 403s.")
    p.add_argument("--debug", action="store_true",
                   help="Dump listing HTML + first 3 detail HTMLs to ./debug/.")
    p.add_argument("--dry-run", action="store_true",
                   help="Parse (and optionally enrich) but don't write to the DB.")
    p.add_argument("--verbose", "-v", action="store_true")
    args = p.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    stats = run(
        delay=args.delay, debug=args.debug, dry_run=args.dry_run,
        limit=args.limit, enrich=args.enrich, enrich_delay=args.enrich_delay,
    )
    log.info("done: %s", stats)
    return 0 if stats["inserted"] + stats["updated"] > 0 or args.dry_run else 1


if __name__ == "__main__":
    sys.exit(main())
