"""
CareerCross.com scraper.

CareerCross is a major bilingual-Japan job board. Its job-search results page
is server-rendered with each job card containing title, company, location,
job type, salary, and updated date — so we can scrape the listing directly
without fetching detail pages.

The "search URL" used as the listing root is configurable in companies.json
under careercross.search_url. It's normally a saved-search URL of the shape:

    https://www.careercross.com/en/job-search/result/<sid>

That sid encodes the filters the user picked on the site (English level,
location, recency, etc.), so each instance of this scraper targets a
specific filtered search. Pagination follows the `?page=N` query parameter.

Detail URL pattern on CareerCross: /en/job/detail-<id>

Usage:
    python careercross_scraper.py [--pages N] [--delay 1.5] [--limit N]
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
from urllib.parse import urljoin, urlparse, urlencode, parse_qsl

import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparser

import db
import inference
import salary_parser

SOURCE_NAME = "careercross"
BASE = "https://www.careercross.com"
COMPANIES_PATH = Path(__file__).parent / "companies.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.careercross.com/en/job-search",
}

# Detail-page URL pattern: /en/job/detail-1562644 (digits, optional query, etc.)
JOB_URL_RE = re.compile(r"^/en/job/detail-(\d+)", re.IGNORECASE)

DEBUG_DIR = Path(__file__).parent / "debug"
log = logging.getLogger("careercross")


def _load_search_url() -> str:
    with COMPANIES_PATH.open() as f:
        data = json.load(f)
    cc = data.get("careercross", {})
    url = cc.get("search_url") or "https://www.careercross.com/en/job-search"
    return url


def _norm(s: Optional[str]) -> str:
    return re.sub(r"\s+", " ", s).strip() if s else ""


def _text(node) -> str:
    return _norm(node.get_text(" ", strip=True)) if node else ""


def _strip_ordinal_suffix(text: str) -> str:
    """Turn 'May 27th, 2026' into 'May 27, 2026' so dateutil parses cleanly."""
    return re.sub(r"(\d+)(st|nd|rd|th)\b", r"\1", text, flags=re.IGNORECASE)


def parse_updated_date(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    cleaned = _strip_ordinal_suffix(raw.strip())
    try:
        return dateparser.parse(cleaned, fuzzy=True).date().isoformat()
    except (ValueError, OverflowError):
        return raw  # keep the raw string if parsing fails


def _page_url(base_url: str, page: int) -> str:
    """Add/replace `page=N` on a query string while preserving everything else."""
    parsed = urlparse(base_url)
    qs = dict(parse_qsl(parsed.query, keep_blank_values=True))
    qs["page"] = str(page)
    return parsed._replace(query=urlencode(qs)).geturl()


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
# Parsing helpers — extract the per-row metadata table inside a job card
# ---------------------------------------------------------------------------

def _table_kv(table) -> dict[str, str]:
    """
    CareerCross job-card metadata is rendered as a `<table>` of two-column rows.
    Each row is <th> label / <td> value. Return {label: value}.
    """
    out: dict[str, str] = {}
    if not table:
        return out
    for row in table.find_all("tr"):
        cells = row.find_all(["th", "td"])
        if len(cells) >= 2:
            key = _norm(cells[0].get_text(" ", strip=True)).rstrip(":")
            val = _norm(cells[1].get_text(" ", strip=True))
            if key:
                out[key] = val
    return out


def _find_card_meta(title_link) -> dict[str, str]:
    """
    Given a job-title anchor, walk up to the nearest container that holds the
    metadata table for this job, then return the {label: value} dict.
    """
    if title_link is None:
        return {}
    # Walk up looking for an ancestor that contains a <table> child somewhere
    # in its descendants (which holds the Hiring Company / Location / ... rows).
    parent = title_link
    for _ in range(8):
        parent = parent.parent
        if parent is None:
            return {}
        # Stop walking up at <article>, <li>, large containers, or just any
        # block that contains a table sibling to the heading.
        tables = parent.find_all("table", recursive=True)
        if tables:
            # Use the first table; merge multiple if needed
            merged: dict[str, str] = {}
            for t in tables:
                merged.update(_table_kv(t))
            return merged
    return {}


# ---------------------------------------------------------------------------
# Listing
# ---------------------------------------------------------------------------

def discover_jobs(html: str) -> list[dict]:
    """
    Parse a single listing HTML page and return a list of job dicts. Each
    job's data comes entirely from the listing (no detail-page fetch needed).
    """
    soup = BeautifulSoup(html, "lxml")
    jobs: list[dict] = []
    seen: set[str] = set()

    # Job titles live inside <h2>/<h3> containing a detail-URL anchor.
    for heading in soup.find_all(["h2", "h3", "h4"]):
        link = heading.find("a", href=True)
        if not link:
            continue
        href = link.get("href", "")
        m = JOB_URL_RE.match(urlparse(urljoin(BASE, href)).path)
        if not m:
            continue
        job_id = m.group(1)
        canonical_url = f"{BASE}/en/job/detail-{job_id}"
        if canonical_url in seen:
            continue
        seen.add(canonical_url)

        title = _norm(link.get_text(" ", strip=True))
        meta = _find_card_meta(link)
        jobs.append({"id": job_id, "url": canonical_url, "title": title, "meta": meta})
    return jobs


def map_job(entry: dict) -> dict:
    meta = entry.get("meta") or {}
    company_name = meta.get("Hiring Company") or meta.get("Company")
    location = meta.get("Location") or meta.get("Work Location")
    job_type = meta.get("Job Type")
    salary_raw = meta.get("Salary")
    updated_raw = meta.get("Updated") or meta.get("Last Updated") or meta.get("Date")

    # Employment-terms inference from job_type text
    employment_terms = None
    if job_type:
        s = job_type.lower()
        if "full" in s:
            employment_terms = "Full-time"
        elif "part" in s:
            employment_terms = "Part-time"
        elif "contract" in s:
            employment_terms = "Contract"
        elif "intern" in s:
            employment_terms = "Internship"
        else:
            employment_terms = _norm(job_type)

    # Numeric salary. CareerCross uses formats like "8 million yen ~ 11 million yen"
    # or "Negotiable, based on experience". When negotiable, parse returns None.
    salary_min, salary_max = salary_parser.parse_range(salary_raw)
    salary_period = salary_parser.parse_period(salary_raw or "") or (
        "Year" if salary_min else None
    )

    post_date = parse_updated_date(updated_raw)

    # The listing doesn't carry a job description, so language/visa/remote
    # inference has very little to chew on. Best-effort over title + salary.
    body = " ".join(filter(None, [entry.get("title"), salary_raw, location]))
    japanese_level = inference.infer_jp_level(body)
    english_level = inference.infer_en_level(body)
    overseas_application_ok = inference.infer_visa_sponsorship(body)
    inferred_remote = inference.infer_remote(body)
    if inferred_remote is not None:
        remote_work_ok = inferred_remote
    elif location and "remote" in location.lower():
        remote_work_ok = 1
    else:
        remote_work_ok = None

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {
        "source": SOURCE_NAME,
        "source_job_id": entry.get("id"),
        "url": entry.get("url"),
        "title": entry.get("title"),
        "company_name": company_name,
        "company_name_jp": None,
        "location": location,
        "industries": None,
        "function": None,
        "work_type": job_type,
        "career_level": None,
        "employment_terms": employment_terms,
        "employer_type": None,
        "salary": salary_raw,
        "salary_period": salary_period,
        "salary_perks": None,
        "salary_min_jpy": salary_min,
        "salary_max_jpy": salary_max,
        "salary_min_annual_jpy": salary_parser.annualize(salary_min, salary_period or "Year"),
        "salary_max_annual_jpy": salary_parser.annualize(salary_max, salary_period or "Year"),
        "english_level": english_level,
        "japanese_level": japanese_level,
        "other_language": None,
        "overseas_application_ok": overseas_application_ok,
        "remote_work_ok": remote_work_ok,
        "has_video_presentation": None,
        "requirements": None,
        "description": None,
        "tags": None,
        "post_date": post_date,
        "last_modified_date": post_date,
        "scraped_at": now,
        "last_seen_at": now,
    }


def iter_listing_pages(fetch: Fetcher, base_url: str, max_pages: int) -> Iterator[tuple[int, str]]:
    for page in range(1, max_pages + 1):
        url = _page_url(base_url, page)
        log.info("listing: %s", url)
        html = fetch.get(url)
        if not html:
            log.warning("page %d: no html, stopping", page)
            return
        if not JOB_URL_RE.search(html):
            log.warning("page %d: no job urls found, stopping", page)
            return
        yield page, html


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def run(pages: int = 3, delay: float = 1.5, debug: bool = False,
        dry_run: bool = False, limit: Optional[int] = None) -> dict:
    db.init_db()
    fetch = Fetcher(delay=delay)
    if debug:
        DEBUG_DIR.mkdir(exist_ok=True)

    base_url = _load_search_url()
    log.info("base search url: %s", base_url)

    all_entries: list[dict] = []
    for page, html in iter_listing_pages(fetch, base_url, pages):
        if debug:
            (DEBUG_DIR / f"careercross_listing_p{page}.html").write_text(html, encoding="utf-8")
        page_entries = discover_jobs(html)
        log.info("page %d: discovered %d jobs", page, len(page_entries))
        all_entries.extend(page_entries)

    # Dedupe across pages
    seen, deduped = set(), []
    for e in all_entries:
        if e["url"] not in seen:
            seen.add(e["url"]); deduped.append(e)
    if limit:
        deduped = deduped[:limit]
    log.info("total unique jobs: %d", len(deduped))

    stats = {"inserted": 0, "updated": 0, "failed": 0, "skipped": 0}
    with db.connect() as conn:
        for i, entry in enumerate(deduped, 1):
            try:
                row = map_job(entry)
            except Exception as e:
                log.exception("map failed for %s: %s", entry.get("url"), e)
                stats["failed"] += 1
                continue
            if not row.get("title"):
                stats["skipped"] += 1
                continue
            if dry_run:
                log.info("[dry-run] %s | %s | %s | salary=%s",
                         row["title"], row.get("company_name"),
                         row.get("location"), row.get("salary"))
                continue
            result = db.upsert_job(conn, row)
            stats[result] += 1
            if i % 25 == 0 or i == len(deduped):
                log.info("%d/%d processed", i, len(deduped))

    return stats


def main() -> int:
    p = argparse.ArgumentParser(description="Scrape CareerCross.com into SQLite.")
    p.add_argument("--pages", type=int, default=3)
    p.add_argument("--delay", type=float, default=1.5)
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--debug", action="store_true")
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
    return 0 if (stats["inserted"] + stats["updated"]) > 0 or args.dry_run else 1


if __name__ == "__main__":
    sys.exit(main())
