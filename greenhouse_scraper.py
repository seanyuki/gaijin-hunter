"""
Greenhouse Job Board API scraper.

Greenhouse publishes a public, unauthenticated JSON endpoint for any board:

    https://boards-api.greenhouse.io/v1/boards/<slug>/jobs?content=true

This returns every open posting on that company's careers page in clean
JSON — including title, location, departments, offices, content (the
HTML description), updated_at, and absolute_url. Far better than scraping
the rendered HTML.

We iterate companies from companies.json -> "greenhouse", call each board,
filter to Japan-located jobs only, and upsert into the same shared DB.
Companies' slugs that 404 are logged and skipped (so a typo doesn't break
the whole run).

Usage:
    python greenhouse_scraper.py [--delay 1.0] [--limit-per-company N]
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
from typing import Optional

import requests
from bs4 import BeautifulSoup

import db
import inference
import salary_parser

SOURCE_NAME = "greenhouse"
API_URL_TMPL = "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
COMPANIES_PATH = Path(__file__).parent / "companies.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

log = logging.getLogger("greenhouse")


def _load_companies() -> list[dict]:
    with COMPANIES_PATH.open() as f:
        data = json.load(f)
    return data.get("greenhouse", [])


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
    """Best-effort location string from Greenhouse's various location fields."""
    parts: list[str] = []
    loc = job.get("location") or {}
    if isinstance(loc, dict) and loc.get("name"):
        parts.append(_norm(loc["name"]))
    for off in job.get("offices") or []:
        if isinstance(off, dict) and off.get("name"):
            parts.append(_norm(off["name"]))
    # Dedupe but preserve order
    seen, out = set(), []
    for p in parts:
        if p and p not in seen:
            seen.add(p); out.append(p)
    return " / ".join(out) if out else ""


def _job_post_date(job: dict) -> Optional[str]:
    for key in ("first_published", "updated_at"):
        v = job.get(key)
        if v:
            return str(v)[:10]
    return None


def _job_departments(job: dict) -> Optional[str]:
    depts = []
    for d in job.get("departments") or []:
        if isinstance(d, dict) and d.get("name"):
            depts.append(_norm(d["name"]))
    return ", ".join(depts) if depts else None


# Greenhouse exposes a `metadata` array with per-job custom fields. Some
# Japan-savvy boards (Mercari et al.) include "Japanese Level" / "English Level"
# entries here — surface them if present.
_LEVEL_KEY_RE = re.compile(r"(japanese|english)\s+(?:language\s+)?level", re.IGNORECASE)


def _metadata_levels(job: dict) -> tuple[Optional[str], Optional[str]]:
    jp_level = en_level = None
    for m in job.get("metadata") or []:
        if not isinstance(m, dict):
            continue
        name = m.get("name", "")
        value = m.get("value")
        if not name or value is None:
            continue
        mm = _LEVEL_KEY_RE.search(name)
        if not mm:
            continue
        lang = mm.group(1).lower()
        text = str(value) if not isinstance(value, list) else ", ".join(str(v) for v in value)
        if lang == "japanese" and not jp_level:
            jp_level = inference.normalize_level_label(text)
        elif lang == "english" and not en_level:
            en_level = inference.normalize_level_label(text)
    return jp_level, en_level


def map_job(company: dict, job: dict) -> Optional[dict]:
    """Map one Greenhouse posting -> our schema dict. Returns None if not Japan."""
    location = _job_location(job)
    if not inference.is_japan_location(location):
        return None

    title = _norm(job.get("title"))
    if not title:
        return None
    url = job.get("absolute_url") or ""
    description = _html_to_text(job.get("content"))

    body = description or ""
    jp_meta, en_meta = _metadata_levels(job)
    japanese_level = jp_meta or inference.infer_jp_level(body)
    english_level  = en_meta or inference.infer_en_level(body)
    overseas_application_ok = inference.infer_visa_sponsorship(body)
    # The body signal wins over the location string — "Onsite only" in the
    # description trumps a "Remote - Japan" tag. Use `is not None`, not `or`,
    # because explicit 0 (onsite) is a real value.
    inferred_remote = inference.infer_remote(body)
    if inferred_remote is not None:
        remote_work_ok = inferred_remote
    elif "remote" in location.lower():
        remote_work_ok = 1
    else:
        remote_work_ok = None

    # Greenhouse doesn't structure salary; try the body.
    salary_min, salary_max = salary_parser.parse_range(body[:2000])
    salary_period = salary_parser.parse_period(body[:2000])
    salary_raw = None
    if salary_min and salary_max and salary_min != salary_max:
        salary_raw = f"¥{salary_min:,} - ¥{salary_max:,}"
    elif salary_min:
        salary_raw = f"¥{salary_min:,}"

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {
        "source": SOURCE_NAME,
        "source_job_id": f"{company['slug']}/{job.get('id')}",
        "url": url,
        "title": title,
        "company_name": company["name"],
        "company_name_jp": None,
        "location": location,
        "industries": _job_departments(job),
        "function": None,
        "work_type": None,
        "career_level": None,
        "employment_terms": None,
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
        "tags": _job_departments(job),
        "post_date": _job_post_date(job),
        "last_modified_date": str(job.get("updated_at") or "")[:10] or None,
        "scraped_at": now,
        "last_seen_at": now,
    }


def fetch_board(slug: str, session: requests.Session, timeout: int = 30) -> Optional[dict]:
    url = API_URL_TMPL.format(slug=slug)
    try:
        r = session.get(url, headers=HEADERS, timeout=timeout)
    except requests.RequestException as e:
        log.warning("request failed for %s: %s", slug, e)
        return None
    if r.status_code == 404:
        log.warning("404 for slug %r (company moved off Greenhouse?)", slug)
        return None
    if r.status_code != 200:
        log.warning("non-200 for slug %r: %s", slug, r.status_code)
        return None
    try:
        return r.json()
    except ValueError:
        log.warning("non-JSON response for %r", slug)
        return None


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
        data = fetch_board(company["slug"], session)
        if data is None:
            stats["failed"] += 1
            continue
        stats["companies"] += 1
        jobs = data.get("jobs") or []
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
    p = argparse.ArgumentParser(description="Scrape Greenhouse public boards for Japan jobs.")
    p.add_argument("--delay", type=float, default=1.0)
    p.add_argument("--limit-per-company", type=int, default=None)
    p.add_argument("--only", type=str, default=None,
                   help="Only fetch the given slug.")
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
