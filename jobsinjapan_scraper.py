"""
JobsInJapan.com scraper.

JobsInJapan is built on WordPress + WP Job Manager. Strategy:

  1. Walk paginated listing pages:
        https://jobsinjapan.com/jobs/?paged=N
     Detail URLs match /jobs/<slug>/ (single slug, distinguishes from category
     and employer pages like /job-category/<cat>/).

  2. For each detail page:
       (a) Prefer schema.org/JobPosting JSON-LD — WP Job Manager emits it by
           default and it has title/description/datePosted/employmentType/
           jobLocation/baseSalary cleanly typed.
       (b) Fall back to WP Job Manager class names (.job_listing-*).
       (c) Body-text regex for foreigner-specific signals not in JSON-LD:
           japanese_level / english_level / visa-sponsorship / remote.

  3. Upsert into our shared SQLite via db.upsert_job with source='jobsinjapan'.

Usage:
    python jobsinjapan_scraper.py [--pages N] [--delay 1.5] [--limit N]
                                  [--debug] [--dry-run] [-v]
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
from typing import Iterator, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

import db
import inference
import salary_parser

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SOURCE_NAME = "jobsinjapan"
BASE = "https://jobsinjapan.com"
LISTING_URL_TMPL = "https://jobsinjapan.com/jobs/?paged={page}"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://jobsinjapan.com/jobs/",
}

# Detail URL pattern: /jobs/<slug>/  (exactly one slug under /jobs/)
# Excludes /jobs/ itself, /jobs/?paged=2, /job-category/..., /job-region/...
JOB_URL_RE = re.compile(r"^/jobs/[^/?#]+/?$", re.IGNORECASE)

DEBUG_DIR = Path(__file__).parent / "debug"
log = logging.getLogger("jobsinjapan")


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

class Fetcher:
    def __init__(self, delay: float = 1.5):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self._last = 0.0

    def get(self, url: str) -> Optional[str]:
        wait = self.delay - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        self._last = time.monotonic()
        try:
            r = self.session.get(url, timeout=20)
        except requests.RequestException as e:
            log.warning("request failed: %s -> %s", url, e)
            return None
        if r.status_code != 200:
            log.warning("non-200: %s -> %s", url, r.status_code)
            return None
        return r.text


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _norm(s: Optional[str]) -> str:
    return re.sub(r"\s+", " ", s).strip() if s else ""


def _text(node) -> str:
    return _norm(node.get_text(" ", strip=True)) if node else ""


def _first_text(soup: BeautifulSoup, selectors: list[str]) -> Optional[str]:
    for sel in selectors:
        n = soup.select_one(sel)
        if n:
            t = _text(n)
            if t:
                return t
    return None


def _extract_jsonld_jobposting(soup: BeautifulSoup) -> Optional[dict]:
    """Return the first schema.org/JobPosting JSON-LD object on the page."""
    for tag in soup.find_all("script", type="application/ld+json"):
        raw = tag.string or tag.get_text() or ""
        try:
            data = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            continue
        candidates = data if isinstance(data, list) else [data]
        flat: list = []
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


# ---------------------------------------------------------------------------
# Body-text inference for foreigner-specific fields
# ---------------------------------------------------------------------------

# Body-text inference (JP/EN level, visa sponsorship, remote) lives in
# inference.py and is shared across scrapers.
_infer_level = lambda text, patterns: inference._match(text, patterns)
_infer_visa_sponsorship = inference.infer_visa_sponsorship
_infer_remote = inference.infer_remote
JP_LEVEL_BODY_PATTERNS = inference.JP_LEVEL_BODY_PATTERNS
EN_LEVEL_BODY_PATTERNS = inference.EN_LEVEL_BODY_PATTERNS


# ---------------------------------------------------------------------------
# Listing
# ---------------------------------------------------------------------------

def discover_job_urls(html: str) -> list[str]:
    """Find detail URLs (/jobs/<slug>/) in the listing HTML."""
    soup = BeautifulSoup(html, "lxml")
    out: dict[str, None] = {}
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Resolve to absolute and normalize
        absolute = urljoin(BASE, href)
        parsed = urlparse(absolute)
        if parsed.netloc and "jobsinjapan.com" not in parsed.netloc:
            continue
        if JOB_URL_RE.match(parsed.path):
            canonical = f"https://jobsinjapan.com{parsed.path}"
            out.setdefault(canonical, None)
    return list(out.keys())


def iter_listing_pages(fetch: Fetcher, max_pages: int) -> Iterator[tuple[int, str]]:
    for page in range(1, max_pages + 1):
        url = LISTING_URL_TMPL.format(page=page)
        log.info("listing: %s", url)
        html = fetch.get(url)
        if not html or not JOB_URL_RE.search(html):
            log.warning("page %d: no job urls found, stopping", page)
            return
        yield page, html


# ---------------------------------------------------------------------------
# Detail parsing
# ---------------------------------------------------------------------------

def _employment_terms_from_jsonld(et) -> Optional[str]:
    if not et:
        return None
    if isinstance(et, list):
        et = et[0] if et else None
        if not et:
            return None
    et = str(et).lower().replace("_", "-").replace(" ", "-")
    mapping = [
        ("full-time", "Full-time"), ("fulltime", "Full-time"),
        ("part-time", "Part-time"), ("parttime", "Part-time"),
        ("contractor", "Contract"), ("contract", "Contract"),
        ("temporary", "Temporary"),
        ("internship", "Internship"), ("intern", "Internship"),
        ("freelance", "Freelance"),
    ]
    for needle, label in mapping:
        if needle in et:
            return label
    return et.title()


def parse_job_detail(url: str, html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    # ---- Title / company / location: try JSON-LD, then WP selectors ----
    posting = _extract_jsonld_jobposting(soup)

    title = None
    company = None
    location = None
    description = None
    post_date = None
    employment_terms = None
    salary_raw = None
    salary_period_jsonld: Optional[str] = None  # set when JSON-LD provides unitText

    if posting:
        title = _norm(posting.get("title"))
        hiring = posting.get("hiringOrganization")
        if isinstance(hiring, dict):
            company = _norm(hiring.get("name"))
        loc = posting.get("jobLocation")
        if isinstance(loc, list) and loc:
            loc = loc[0]
        if isinstance(loc, dict):
            addr = loc.get("address", {}) if isinstance(loc.get("address"), dict) else {}
            parts = [addr.get("addressLocality"), addr.get("addressRegion"),
                     addr.get("addressCountry")]
            joined = ", ".join(p for p in parts if p)
            if joined:
                location = joined
        if posting.get("datePosted"):
            post_date = str(posting["datePosted"])[:10]
        employment_terms = _employment_terms_from_jsonld(posting.get("employmentType"))
        if posting.get("description"):
            desc_html = str(posting["description"])
            description = _norm(BeautifulSoup(desc_html, "lxml").get_text(" ", strip=True))[:20_000]
        bs = posting.get("baseSalary")
        if isinstance(bs, dict):
            val = bs.get("value") if isinstance(bs.get("value"), dict) else bs
            if isinstance(val, dict):
                lo, hi = val.get("minValue"), val.get("maxValue")
                if lo and hi:
                    currency = bs.get("currency", "JPY")
                    sign = "¥" if currency == "JPY" else f"{currency} "
                    salary_raw = f"{sign}{int(lo):,} - {sign}{int(hi):,}"
                unit = val.get("unitText")
                if unit:
                    salary_period_jsonld = str(unit).capitalize()

    # WP Job Manager fallbacks
    if not title:
        title = _first_text(soup, [
            "h1.entry-title", "h1.job_listing-title", "h1.page-title",
            "article h1", "main h1", "h1",
        ])
    if not company:
        company = _first_text(soup, [
            ".job_listing-company strong", ".job_listing-company .company",
            ".job_listing-company a", ".job_listing-company",
            ".company-name", "[itemprop='hiringOrganization']",
        ])
    if not location:
        location = _first_text(soup, [
            "[itemprop='jobLocation']",
            ".job_listing-location a", ".job_listing-location",
            ".location",
        ])
    if not description:
        node = (
            soup.select_one(".single_job_listing .job_description")
            or soup.select_one(".job_description")
            or soup.select_one("[itemprop='description']")
            or soup.select_one(".entry-content")
            or soup.select_one("article")
        )
        if node:
            description = _norm(node.get_text(" ", strip=True))[:20_000]
    if not employment_terms:
        et_text = _first_text(soup, [
            ".job-type", ".job_listing-type", "[itemprop='employmentType']",
        ])
        employment_terms = _employment_terms_from_jsonld(et_text)
    if not salary_raw:
        salary_raw = _first_text(soup, [
            "[itemprop='baseSalary']", ".job_listing-salary", ".salary",
        ])
    if not post_date:
        time_node = soup.select_one("time[datetime], [itemprop='datePosted']")
        if time_node:
            dt = time_node.get("datetime") or _text(time_node)
            post_date = str(dt)[:10] if dt else None

    # Body-text inference for foreigner-specific signals
    body = description or _text(soup.select_one("article")) or _text(soup.body)
    japanese_level = _infer_level(body, JP_LEVEL_BODY_PATTERNS)
    english_level = _infer_level(body, EN_LEVEL_BODY_PATTERNS)
    overseas_application_ok = _infer_visa_sponsorship(body)
    remote_work_ok = _infer_remote(body)

    # Tags from WP categories/job-category/tag-rel links
    tag_set: list[str] = []
    for sel in ["a[rel='tag']", ".job_listing-category a", ".job-category a",
                ".tagcloud a", ".categories a"]:
        for a in soup.select(sel):
            t = _text(a)
            if t and t not in tag_set:
                tag_set.append(t)
    tags_str = ", ".join(tag_set) if tag_set else None

    # Numeric salary. Period preference: JSON-LD unitText, then in-string regex.
    salary_period = salary_period_jsonld or salary_parser.parse_period(salary_raw or "")
    salary_min_jpy, salary_max_jpy = salary_parser.parse_range(salary_raw)
    salary_min_annual_jpy = salary_parser.annualize(salary_min_jpy, salary_period or "Year")
    salary_max_annual_jpy = salary_parser.annualize(salary_max_jpy, salary_period or "Year")

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {
        "source": SOURCE_NAME,
        "source_job_id": urlparse(url).path.rstrip("/").rsplit("/", 1)[-1],
        "url": url,
        "title": title,
        "company_name": company,
        "company_name_jp": None,
        "location": location,
        "employment_terms": employment_terms,
        "salary": salary_raw,
        "salary_period": salary_period,
        "salary_min_jpy": salary_min_jpy,
        "salary_max_jpy": salary_max_jpy,
        "salary_min_annual_jpy": salary_min_annual_jpy,
        "salary_max_annual_jpy": salary_max_annual_jpy,
        "english_level": english_level,
        "japanese_level": japanese_level,
        "overseas_application_ok": overseas_application_ok,
        "remote_work_ok": remote_work_ok,
        "description": description,
        "tags": tags_str,
        "post_date": post_date,
        "scraped_at": now,
        "last_seen_at": now,
    }


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def run(pages: int, delay: float, debug: bool, dry_run: bool,
        limit: Optional[int], enrich: bool = True) -> dict:
    """
    JobsInJapan listings are sparse on metadata, so we always fetch detail
    pages (no opt-out unlike TokyoDev). The `enrich` parameter is accepted
    for parity with the update.py runner contract.
    """
    db.init_db()
    if debug:
        DEBUG_DIR.mkdir(exist_ok=True)

    fetch = Fetcher(delay=delay)

    # 1. Walk listing pages, collect detail URLs.
    all_urls: list[str] = []
    for page, html in iter_listing_pages(fetch, max_pages=pages):
        if debug:
            (DEBUG_DIR / f"jobsinjapan_listing_p{page}.html").write_text(html, encoding="utf-8")
        urls = discover_job_urls(html)
        log.info("page %d: discovered %d job urls", page, len(urls))
        all_urls.extend(urls)

    # Dedupe
    seen, job_urls = set(), []
    for u in all_urls:
        if u not in seen:
            seen.add(u); job_urls.append(u)
    if limit:
        job_urls = job_urls[:limit]
    log.info("total unique job urls: %d", len(job_urls))

    stats = {"inserted": 0, "updated": 0, "failed": 0, "skipped": 0}

    # 2. Fetch each detail page and upsert.
    with db.connect() as conn:
        for i, url in enumerate(job_urls, 1):
            html = fetch.get(url)
            if not html:
                stats["failed"] += 1
                continue
            if debug and i <= 3:
                slug = re.sub(r"[^a-z0-9]+", "_", url.lower())[-60:]
                (DEBUG_DIR / f"jobsinjapan_job_{slug}.html").write_text(html, encoding="utf-8")
            try:
                job = parse_job_detail(url, html)
            except Exception as e:
                log.exception("parse failed for %s: %s", url, e)
                stats["failed"] += 1
                continue
            if not job.get("title"):
                log.warning("no title parsed: %s", url)
                stats["skipped"] += 1
                continue
            if dry_run:
                log.info("[dry-run] %s | %s | %s | jp=%s",
                         job.get("title"), job.get("company_name"),
                         job.get("location"), job.get("japanese_level"))
                continue
            result = db.upsert_job(conn, job)
            stats[result] += 1
            log.info("[%d/%d] %s: %s", i, len(job_urls), result, job["title"])

    return stats


def main() -> int:
    p = argparse.ArgumentParser(description="Scrape JobsInJapan.com into SQLite.")
    p.add_argument("--pages", type=int, default=2,
                   help="How many listing pages to walk (default 2).")
    p.add_argument("--delay", type=float, default=1.5,
                   help="Seconds between requests (default 1.5).")
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--debug", action="store_true",
                   help="Dump sample HTML to ./debug/")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--verbose", "-v", action="store_true")
    args = p.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    stats = run(pages=args.pages, delay=args.delay, debug=args.debug,
                dry_run=args.dry_run, limit=args.limit)
    log.info("done: %s", stats)
    return 0 if stats["inserted"] + stats["updated"] > 0 or args.dry_run else 1


if __name__ == "__main__":
    sys.exit(main())
