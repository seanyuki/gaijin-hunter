"""
Ashby Job Board API scraper.

Ashby publishes a public, unauthenticated JSON endpoint for any company that
hosts its careers page on Ashby:

    https://api.ashbyhq.com/posting-api/job-board/<board>?includeCompensation=true

Returns {"jobs": [...]} where each posting includes title, location,
secondaryLocations, department, team, employmentType, isRemote, address,
publishedAt, jobUrl/applyUrl, descriptionHtml/descriptionPlain, and (when
includeCompensation=true) a structured `compensation` block. When the
compensation is quoted in JPY we use it directly; otherwise we fall back to
parsing the body, exactly like the Greenhouse/Lever scrapers.

We iterate companies from companies.json -> "ashby", filter to Japan-located
jobs only, and upsert into the shared DB. Boards that 404 are logged and
skipped so a stale slug never breaks the run.

Usage:
    python ashby_scraper.py [--delay 1.0] [--limit-per-company N]
                            [--only <board>] [--debug] [--dry-run] [-v]
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

SOURCE_NAME = "ashby"
API_URL_TMPL = "https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true"
COMPANIES_PATH = Path(__file__).parent / "companies.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

log = logging.getLogger("ashby")


def _load_companies() -> list[dict]:
    with COMPANIES_PATH.open() as f:
        data = json.load(f)
    return data.get("ashby", [])


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


def _job_location(job: dict) -> str:
    """Best-effort location from Ashby's location string, secondaryLocations,
    and the structured postal address."""
    parts: list[str] = []
    primary = job.get("location")
    if isinstance(primary, str) and primary.strip():
        parts.append(_norm(primary))
    for sec in job.get("secondaryLocations") or []:
        if isinstance(sec, dict):
            name = sec.get("location") or sec.get("name")
            if name:
                parts.append(_norm(str(name)))
        elif isinstance(sec, str):
            parts.append(_norm(sec))
    # Structured address as a fallback/confirmation.
    addr = (job.get("address") or {}).get("postalAddress") or {}
    if isinstance(addr, dict):
        for k in ("addressLocality", "addressRegion", "addressCountry"):
            v = addr.get(k)
            if v:
                parts.append(_norm(str(v)))
    seen, out = set(), []
    for p in parts:
        if p and p.lower() not in seen:
            seen.add(p.lower()); out.append(p)
    return " / ".join(out) if out else ""


def _employment_terms(value: Optional[str]) -> Optional[str]:
    """Ashby employmentType: FullTime | PartTime | Intern | Contract | Temporary."""
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


def _interval_to_period(interval: Optional[str]) -> Optional[str]:
    if not interval:
        return None
    s = str(interval).upper()
    if "YEAR" in s or s in ("1 YEAR", "ANNUAL"):
        return "Year"
    if "MONTH" in s:
        return "Month"
    if "HOUR" in s:
        return "Hour"
    if "DAY" in s:
        return "Day"
    return None


def _ashby_salary(job: dict):
    """Pull a JPY salary out of Ashby's structured compensation, if present.
    Returns (min, max, period) or (None, None, None)."""
    comp = job.get("compensation")
    if not isinstance(comp, dict):
        return None, None, None
    for tier in comp.get("compensationTiers") or []:
        if not isinstance(tier, dict):
            continue
        for comp_part in tier.get("components") or []:
            if not isinstance(comp_part, dict):
                continue
            ctype = str(comp_part.get("compensationType") or "").lower()
            if ctype and "salary" not in ctype and "base" not in ctype:
                continue
            currency = str(comp_part.get("currencyCode") or "").upper()
            if currency and currency != "JPY":
                continue
            cmin = comp_part.get("minValue")
            cmax = comp_part.get("maxValue")
            try:
                cmin = int(cmin) if cmin is not None else None
                cmax = int(cmax) if cmax is not None else None
            except (TypeError, ValueError):
                cmin = cmax = None
            if cmin or cmax:
                period = _interval_to_period(comp_part.get("interval")) or "Year"
                return cmin, (cmax or cmin), period
    return None, None, None


def _post_date(job: dict) -> Optional[str]:
    for key in ("publishedAt", "publishedDate", "updatedAt"):
        v = job.get(key)
        if v:
            return str(v)[:10]
    return None


def map_job(company: dict, job: dict) -> Optional[dict]:
    """Map one Ashby posting -> our schema. Returns None if not a Japan job."""
    # Respect the board's own listed/published flags when present.
    if job.get("isListed") is False:
        return None

    location = _job_location(job)
    if not inference.is_japan_location(location):
        return None

    title = _norm(job.get("title"))
    if not title:
        return None
    url = job.get("jobUrl") or job.get("applyUrl") or ""
    description = _html_to_text(job.get("descriptionHtml")) or _norm(job.get("descriptionPlain")) or None

    body = description or ""
    japanese_level = inference.infer_jp_level(body)
    english_level = inference.infer_en_level(body)
    overseas_application_ok = inference.infer_visa_sponsorship(body)

    inferred_remote = inference.infer_remote(body)
    if inferred_remote is not None:
        remote_work_ok = inferred_remote
    elif job.get("isRemote") is True or "remote" in location.lower():
        remote_work_ok = 1
    elif job.get("isRemote") is False:
        remote_work_ok = 0
    else:
        remote_work_ok = None

    # Prefer Ashby's structured JPY compensation; else parse the body.
    salary_min, salary_max, salary_period = _ashby_salary(job)
    if not salary_min:
        salary_min, salary_max = salary_parser.parse_range(body[:2000])
        salary_period = salary_parser.parse_period(body[:2000])

    salary_raw = None
    if salary_min and salary_max and salary_min != salary_max:
        salary_raw = f"¥{salary_min:,} - ¥{salary_max:,}"
    elif salary_min:
        salary_raw = f"¥{salary_min:,}"

    dept = _norm(job.get("department")) or None
    team = _norm(job.get("team")) or None

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {
        "source": SOURCE_NAME,
        "source_job_id": f"{company['slug']}/{job.get('id')}",
        "url": url,
        "title": title,
        "company_name": company["name"],
        "company_name_jp": None,
        "location": location,
        "industries": dept,
        "function": team,
        "work_type": None,
        "career_level": None,
        "employment_terms": _employment_terms(job.get("employmentType")),
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
        "tags": dept or team,
        "post_date": _post_date(job),
        "last_modified_date": str(job.get("updatedAt") or "")[:10] or None,
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
        log.warning("404 for board %r (company moved off Ashby?)", slug)
        return None
    if r.status_code != 200:
        log.warning("non-200 for board %r: %s", slug, r.status_code)
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
        log.info("  board returned %d jobs", len(jobs))
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
    p = argparse.ArgumentParser(description="Scrape Ashby public boards for Japan jobs.")
    p.add_argument("--delay", type=float, default=1.0)
    p.add_argument("--limit-per-company", type=int, default=None)
    p.add_argument("--only", type=str, default=None, help="Only fetch the given board slug.")
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
