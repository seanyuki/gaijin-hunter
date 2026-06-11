"""
Workable Job Board API scraper.

Workable exposes a public, unauthenticated "widget" endpoint for any account
that hosts its careers page on Workable:

    https://apply.workable.com/api/v1/widget/accounts/<subdomain>?details=true

With details=true each posting includes title, shortcode, state, department,
url, application_url, employment_type, telecommuting, a structured `location`
({country, countryCode, region, city, ...}), created_at, and the HTML
`description`, `requirements`, and `benefits`. Workable does not publish a
structured salary, so we parse it out of the body like Greenhouse/Lever.

We iterate accounts from companies.json -> "workable", filter to Japan-located
jobs only, and upsert into the shared DB. Accounts that 404 are logged and
skipped so a stale subdomain never breaks the run.

Usage:
    python workable_scraper.py [--delay 1.0] [--limit-per-company N]
                               [--only <subdomain>] [--debug] [--dry-run] [-v]
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

import requests
from bs4 import BeautifulSoup

import db
import inference
import salary_parser

SOURCE_NAME = "workable"
API_URL_TMPL = "https://apply.workable.com/api/v1/widget/accounts/{slug}?details=true"
COMPANIES_PATH = Path(__file__).parent / "companies.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

log = logging.getLogger("workable")


def _load_companies() -> list[dict]:
    with COMPANIES_PATH.open() as f:
        data = json.load(f)
    return data.get("workable", [])


def _norm(s: Optional[str]) -> str:
    return re.sub(r"\s+", " ", s).strip() if s else ""


def _html_to_text(html_str: Optional[str], cap: int = 20_000) -> Optional[str]:
    if not html_str:
        return None
    text = BeautifulSoup(html_str, "lxml").get_text(" ", strip=True)
    text = _norm(text)
    if not text:
        return None
    return text if len(text) <= cap else text[:cap] + " …"


def _location_obj(job: dict) -> dict:
    loc = job.get("location")
    return loc if isinstance(loc, dict) else {}


def _is_japan(job: dict, location_str: str) -> bool:
    loc = _location_obj(job)
    cc = str(loc.get("countryCode") or "").upper()
    if cc == "JP":
        return True
    if str(loc.get("country") or "").strip().lower() in ("japan", "日本"):
        return True
    return inference.is_japan_location(location_str)


def _location_string(job: dict) -> str:
    loc = _location_obj(job)
    parts = [loc.get("city"), loc.get("region"), loc.get("country")]
    out = [_norm(str(p)) for p in parts if p]
    if not out and job.get("telecommuting"):
        return "Remote"
    return ", ".join(dict.fromkeys(out))  # dedupe, keep order


def _employment_terms(value: Optional[str]) -> Optional[str]:
    """Workable employment_type: 'Full-time' | 'Part-time' | 'Contract'
    | 'Temporary' | 'Internship' (occasionally lowercase / underscored)."""
    if not value:
        return None
    s = str(value).lower()
    if "full" in s:
        return "Full-time"
    if "part" in s:
        return "Part-time"
    if "intern" in s:
        return "Internship"
    if "contract" in s:
        return "Contract"
    if "temp" in s:
        return "Temporary"
    return _norm(value)


def _build_description(job: dict) -> Optional[str]:
    parts: list[str] = []
    for key in ("description", "requirements", "benefits"):
        text = _html_to_text(job.get(key))
        if text:
            label = {"requirements": "Requirements", "benefits": "Benefits"}.get(key)
            parts.append(f"{label}: {text}" if label else text)
    out = "\n\n".join(parts)
    if not out:
        return None
    return out if len(out) <= 20_000 else out[:20_000] + " …"


def _job_url(slug: str, job: dict) -> str:
    return (job.get("url") or job.get("application_url")
            or f"https://apply.workable.com/{slug}/j/{job.get('shortcode', '')}/")


def map_job(company: dict, job: dict) -> Optional[dict]:
    """Map one Workable posting -> our schema. Returns None if not a Japan job."""
    # Only published roles.
    state = str(job.get("state") or "").lower()
    if state and state not in ("published", "open", "active"):
        return None

    location_str = _location_string(job)
    if not _is_japan(job, location_str):
        return None

    title = _norm(job.get("title") or job.get("full_title"))
    if not title:
        return None
    slug = company["slug"]
    url = _job_url(slug, job)
    description = _build_description(job)

    body = description or ""
    japanese_level = inference.infer_jp_level(body)
    english_level = inference.infer_en_level(body)
    overseas_application_ok = inference.infer_visa_sponsorship(body)

    inferred_remote = inference.infer_remote(body)
    if inferred_remote is not None:
        remote_work_ok = inferred_remote
    elif job.get("telecommuting") is True or "remote" in location_str.lower():
        remote_work_ok = 1
    elif job.get("telecommuting") is False:
        remote_work_ok = 0
    else:
        remote_work_ok = None

    salary_min, salary_max = salary_parser.parse_range(body[:2000])
    salary_period = salary_parser.parse_period(body[:2000])
    salary_raw = None
    if salary_min and salary_max and salary_min != salary_max:
        salary_raw = f"¥{salary_min:,} - ¥{salary_max:,}"
    elif salary_min:
        salary_raw = f"¥{salary_min:,}"

    dept = _norm(job.get("department")) or None
    post_date = str(job.get("created_at") or job.get("published_on") or "")[:10] or None

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {
        "source": SOURCE_NAME,
        "source_job_id": f"{slug}/{job.get('shortcode') or job.get('id')}",
        "url": url,
        "title": title,
        "company_name": company["name"],
        "company_name_jp": None,
        "location": location_str,
        "industries": dept,
        "function": None,
        "work_type": None,
        "career_level": None,
        "employment_terms": _employment_terms(job.get("employment_type")),
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
        "description": description,
        "tags": dept,
        "post_date": post_date,
        "last_modified_date": None,
        "scraped_at": now,
        "last_seen_at": now,
    }


def fetch_board(slug: str, session: requests.Session, timeout: int = 30) -> Optional[list]:
    url = API_URL_TMPL.format(slug=slug)
    try:
        r = session.get(url, headers=HEADERS, timeout=timeout)
    except requests.RequestException as e:
        log.warning("request failed for %s: %s", slug, e)
        return None
    if r.status_code == 404:
        log.warning("404 for account %r (not on Workable?)", slug)
        return None
    if r.status_code != 200:
        log.warning("non-200 for account %r: %s", slug, r.status_code)
        return None
    try:
        data = r.json()
    except ValueError:
        log.warning("non-JSON response for %r", slug)
        return None
    return data.get("jobs") or []


def run(delay: float = 1.0, debug: bool = False, dry_run: bool = False,
        limit_per_company: Optional[int] = None,
        only_company: Optional[str] = None) -> dict:
    db.init_db()
    session = requests.Session()
    companies = _load_companies()
    if only_company:
        companies = [c for c in companies if c["slug"] == only_company]

    stats = {"inserted": 0, "updated": 0, "failed": 0, "skipped": 0,
             "companies": 0, "non_japan": 0}

    for i, company in enumerate(companies):
        if i > 0:
            time.sleep(delay)
        log.info("[%d/%d] %s (%s)", i + 1, len(companies), company["name"], company["slug"])
        jobs = fetch_board(company["slug"], session)
        if jobs is None:
            stats["failed"] += 1
            continue
        stats["companies"] += 1
        log.info("  account returned %d jobs", len(jobs))
        if limit_per_company:
            jobs = jobs[:limit_per_company]
        with db.connect() as conn:
            for job in jobs:
                row = map_job(company, job)
                if row is None:
                    stats["non_japan"] += 1
                    continue
                if dry_run:
                    log.info("  [dry-run] %s | %s", row["title"], row["location"])
                    continue
                try:
                    result = db.upsert_job(conn, row)
                    stats[result] += 1
                except Exception as e:
                    log.exception("upsert failed for %s: %s", row.get("url"), e)
                    stats["failed"] += 1

    return stats


def main() -> int:
    p = argparse.ArgumentParser(description="Scrape Workable public boards for Japan jobs.")
    p.add_argument("--delay", type=float, default=1.0)
    p.add_argument("--limit-per-company", type=int, default=None)
    p.add_argument("--only", type=str, default=None, help="Only fetch the given account subdomain.")
    p.add_argument("--debug", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--verbose", "-v", action="store_true")
    args = p.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    stats = run(
        delay=args.delay, debug=args.debug, dry_run=args.dry_run,
        limit_per_company=args.limit_per_company, only_company=args.only,
    )
    log.info("done: %s", stats)
    return 0 if (stats["inserted"] + stats["updated"]) > 0 or args.dry_run else 1


if __name__ == "__main__":
    sys.exit(main())
