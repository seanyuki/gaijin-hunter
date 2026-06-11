"""
SmartRecruiters public Posting API scraper.

SmartRecruiters publishes an unauthenticated postings API per company:

    https://api.smartrecruiters.com/v1/companies/<companyId>/postings?limit=100&offset=0

The list response is paginated ({"content": [...], "totalFound", "limit",
"offset"}) and each item carries title, location {city,region,country,remote},
department, function, typeOfEmployment, experienceLevel, releasedDate. The list
does NOT include the description, so for each Japan-matched posting we make one
detail call:

    https://api.smartrecruiters.com/v1/companies/<companyId>/postings/<postingId>

which returns jobAd.sections.{jobDescription,qualifications,additionalInformation}
as HTML. To keep request counts sane we only fetch details for postings that
already pass the Japan location filter.

We iterate companies from companies.json -> "smartrecruiters", filter to Japan,
and upsert into the shared DB. companyIds that 404 are logged and skipped.

Usage:
    python smartrecruiters_scraper.py [--delay 1.0] [--limit-per-company N]
                                      [--only <companyId>] [--dry-run] [-v]
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

SOURCE_NAME = "smartrecruiters"
LIST_URL_TMPL = "https://api.smartrecruiters.com/v1/companies/{slug}/postings?limit={limit}&offset={offset}"
DETAIL_URL_TMPL = "https://api.smartrecruiters.com/v1/companies/{slug}/postings/{posting_id}"
PUBLIC_URL_TMPL = "https://jobs.smartrecruiters.com/{slug}/{posting_id}"
COMPANIES_PATH = Path(__file__).parent / "companies.json"
PAGE_SIZE = 100
MAX_POSTINGS = 1000  # safety cap per company

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

log = logging.getLogger("smartrecruiters")


def _load_companies() -> list[dict]:
    with COMPANIES_PATH.open() as f:
        data = json.load(f)
    return data.get("smartrecruiters", [])


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


def _location_string(loc: dict) -> str:
    if not isinstance(loc, dict):
        return ""
    country = _norm(str(loc.get("country") or ""))
    # SmartRecruiters often returns a bare 2-letter country code (e.g. "jp").
    if country.lower() == "jp":
        country = "Japan"
    elif len(country) == 2:
        country = ""  # unknown 2-letter code: drop rather than show "de"/"us"
    parts = [loc.get("city"), loc.get("region"), country]
    out = [_norm(str(p)) for p in parts if p]
    if not out and loc.get("remote"):
        return "Remote"
    return ", ".join(dict.fromkeys(out))


def _is_japan(loc: dict, location_str: str) -> bool:
    if isinstance(loc, dict):
        cc = str(loc.get("country") or loc.get("countryCode") or "").strip().lower()
        if cc in ("jp", "japan", "日本"):
            return True
    return inference.is_japan_location(location_str)


def _employment_terms(posting: dict) -> Optional[str]:
    toe = posting.get("typeOfEmployment") or {}
    label = toe.get("label") if isinstance(toe, dict) else toe
    if not label:
        return None
    s = str(label).lower()
    if "full" in s:
        return "Full-time"
    if "part" in s:
        return "Part-time"
    if "intern" in s:
        return "Internship"
    if "contract" in s or "temporary" in s:
        return "Contract"
    return _norm(str(label))


def _label(obj) -> Optional[str]:
    if isinstance(obj, dict):
        return _norm(obj.get("label")) or None
    return _norm(obj) or None


def _detail_description(detail: dict) -> Optional[str]:
    job_ad = detail.get("jobAd") or {}
    sections = job_ad.get("sections") or {}
    parts: list[str] = []
    for key in ("jobDescription", "qualifications", "additionalInformation"):
        sec = sections.get(key) or {}
        text = _html_to_text(sec.get("text"))
        if text:
            title = _norm(sec.get("title"))
            parts.append(f"{title}: {text}" if title and key != "jobDescription" else text)
    out = "\n\n".join(parts)
    if not out:
        return None
    return out if len(out) <= 20_000 else out[:20_000] + " …"


def fetch_detail(slug: str, posting_id: str, session: requests.Session,
                 timeout: int = 30) -> Optional[dict]:
    url = DETAIL_URL_TMPL.format(slug=slug, posting_id=posting_id)
    try:
        r = session.get(url, headers=HEADERS, timeout=timeout)
    except requests.RequestException as e:
        log.debug("detail request failed for %s/%s: %s", slug, posting_id, e)
        return None
    if r.status_code != 200:
        return None
    try:
        return r.json()
    except ValueError:
        return None


def map_posting(company: dict, posting: dict, detail: Optional[dict]) -> Optional[dict]:
    loc = posting.get("location") or {}
    location_str = _location_string(loc)
    if not _is_japan(loc, location_str):
        return None

    title = _norm(posting.get("name"))
    if not title:
        return None

    posting_id = posting.get("id") or posting.get("uuid")
    url = posting.get("postingUrl") or posting.get("applyUrl") \
        or PUBLIC_URL_TMPL.format(slug=company["slug"], posting_id=posting_id)

    description = _detail_description(detail) if detail else None

    body = description or ""
    japanese_level = inference.infer_jp_level(body)
    english_level = inference.infer_en_level(body)
    overseas_application_ok = inference.infer_visa_sponsorship(body)

    inferred_remote = inference.infer_remote(body)
    if inferred_remote is not None:
        remote_work_ok = inferred_remote
    elif loc.get("remote") is True or "remote" in location_str.lower():
        remote_work_ok = 1
    elif loc.get("remote") is False:
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

    dept = _label(posting.get("department"))
    func = _label(posting.get("function"))
    post_date = str(posting.get("releasedDate") or "")[:10] or None

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {
        "source": SOURCE_NAME,
        "source_job_id": f"{company['slug']}/{posting_id}",
        "url": url,
        "title": title,
        "company_name": company["name"],
        "company_name_jp": None,
        "location": location_str,
        "industries": dept,
        "function": func,
        "work_type": None,
        "career_level": _label(posting.get("experienceLevel")),
        "employment_terms": _employment_terms(posting),
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
        "tags": dept or func,
        "post_date": post_date,
        "last_modified_date": None,
        "scraped_at": now,
        "last_seen_at": now,
    }


def fetch_postings(slug: str, session: requests.Session, timeout: int = 30) -> Optional[list]:
    """Paginate the postings list endpoint. Returns a flat list or None on hard failure."""
    out: list[dict] = []
    offset = 0
    while offset < MAX_POSTINGS:
        url = LIST_URL_TMPL.format(slug=slug, limit=PAGE_SIZE, offset=offset)
        try:
            r = session.get(url, headers=HEADERS, timeout=timeout)
        except requests.RequestException as e:
            log.warning("request failed for %s (offset %d): %s", slug, offset, e)
            return out or None
        if r.status_code == 404:
            log.warning("404 for company %r (not on SmartRecruiters?)", slug)
            return None
        if r.status_code != 200:
            log.warning("non-200 for company %r: %s", slug, r.status_code)
            return out or None
        try:
            data = r.json()
        except ValueError:
            log.warning("non-JSON response for %r", slug)
            return out or None
        content = data.get("content") or []
        out.extend(content)
        total = data.get("totalFound", len(out))
        offset += PAGE_SIZE
        if len(content) < PAGE_SIZE or offset >= total:
            break
    return out


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
        postings = fetch_postings(company["slug"], session)
        if postings is None:
            stats["failed"] += 1
            continue
        stats["companies"] += 1
        log.info("  company returned %d postings", len(postings))
        if limit_per_company:
            postings = postings[:limit_per_company]

        with db.connect() as conn:
            for posting in postings:
                loc = posting.get("location") or {}
                if not _is_japan(loc, _location_string(loc)):
                    stats["non_japan"] += 1
                    continue
                # Japan match -> one detail call for the description.
                time.sleep(min(delay, 0.6))
                detail = fetch_detail(company["slug"], posting.get("id") or posting.get("uuid"), session)
                row = map_posting(company, posting, detail)
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
    p = argparse.ArgumentParser(description="Scrape SmartRecruiters public postings for Japan jobs.")
    p.add_argument("--delay", type=float, default=1.0)
    p.add_argument("--limit-per-company", type=int, default=None)
    p.add_argument("--only", type=str, default=None, help="Only fetch the given companyId.")
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
