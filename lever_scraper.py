"""
Lever Job Postings API scraper.

Lever publishes a public, unauthenticated JSON endpoint for any company:

    https://api.lever.co/v0/postings/<slug>?mode=json

Returns an array of postings with text (title), categories (team / location /
commitment), hostedUrl, descriptionPlain, description (HTML), createdAt
(epoch ms), additionalPlain, lists (the requirement bullets), etc.

We iterate companies from companies.json -> "lever", filter to Japan, and
upsert into the shared DB.

Usage:
    python lever_scraper.py [--delay 1.0] [--limit-per-company N]
                            [--only <slug>] [--debug] [--dry-run] [-v]
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

SOURCE_NAME = "lever"
API_URL_TMPL = "https://api.lever.co/v0/postings/{slug}?mode=json"
COMPANIES_PATH = Path(__file__).parent / "companies.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

log = logging.getLogger("lever")


def _load_companies() -> list[dict]:
    with COMPANIES_PATH.open() as f:
        data = json.load(f)
    return data.get("lever", [])


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


def _employment_terms_from_commitment(commitment: Optional[str]) -> Optional[str]:
    if not commitment:
        return None
    s = commitment.lower()
    if "full" in s:
        return "Full-time"
    if "part" in s:
        return "Part-time"
    if "contract" in s:
        return "Contract"
    if "intern" in s:
        return "Internship"
    return commitment


def _epoch_ms_to_iso_date(v) -> Optional[str]:
    try:
        n = int(v)
    except (TypeError, ValueError):
        return None
    # Lever uses milliseconds since epoch
    if n > 10**12:  # ms
        n = n // 1000
    try:
        return datetime.fromtimestamp(n, tz=timezone.utc).date().isoformat()
    except (ValueError, OverflowError, OSError):
        return None


def _build_description(posting: dict) -> Optional[str]:
    parts: list[str] = []
    if posting.get("descriptionPlain"):
        parts.append(_norm(posting["descriptionPlain"]))
    # Lever postings have a `lists` array of {text: <heading>, content: <HTML>}
    for lst in posting.get("lists") or []:
        if not isinstance(lst, dict):
            continue
        heading = _norm(lst.get("text"))
        content_text = _html_to_text(lst.get("content"))
        if heading and content_text:
            parts.append(f"{heading}: {content_text}")
        elif content_text:
            parts.append(content_text)
    if posting.get("additionalPlain"):
        parts.append(_norm(posting["additionalPlain"]))
    out = "\n\n".join(p for p in parts if p)
    if not out:
        return None
    return out if len(out) <= 20_000 else out[:20_000] + " …"


def map_posting(company: dict, posting: dict) -> Optional[dict]:
    """Map one Lever posting -> our schema. Returns None if not Japan."""
    cats = posting.get("categories") or {}
    if not isinstance(cats, dict):
        cats = {}
    location = _norm(cats.get("location") or "")
    country = _norm(posting.get("country") or "")
    if not (inference.is_japan_location(location) or inference.is_japan_location(country)):
        return None

    title = _norm(posting.get("text"))
    if not title:
        return None
    url = posting.get("hostedUrl") or ""
    description = _build_description(posting)

    body = description or ""
    japanese_level = inference.infer_jp_level(body)
    english_level = inference.infer_en_level(body)
    overseas_application_ok = inference.infer_visa_sponsorship(body)
    # Body signal takes precedence over location-based defaults; 0 means
    # explicit onsite-only so we must check `is not None`, not truthiness.
    inferred_remote = inference.infer_remote(body)
    if inferred_remote is not None:
        remote_work_ok = inferred_remote
    elif "remote" in location.lower():
        remote_work_ok = 1
    else:
        remote_work_ok = None

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
        "source_job_id": f"{company['slug']}/{posting.get('id')}",
        "url": url,
        "title": title,
        "company_name": company["name"],
        "company_name_jp": None,
        "location": location or country,
        "industries": _norm(cats.get("team")) or None,
        "function": _norm(cats.get("department")) or None,
        "work_type": None,
        "career_level": _norm(cats.get("level")) or None,
        "employment_terms": _employment_terms_from_commitment(cats.get("commitment")),
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
        "tags": _norm(cats.get("team")) or None,
        "post_date": _epoch_ms_to_iso_date(posting.get("createdAt")),
        "last_modified_date": None,
        "scraped_at": now,
        "last_seen_at": now,
    }


def fetch_postings(slug: str, session: requests.Session, timeout: int = 30) -> Optional[list]:
    url = API_URL_TMPL.format(slug=slug)
    try:
        r = session.get(url, headers=HEADERS, timeout=timeout)
    except requests.RequestException as e:
        log.warning("request failed for %s: %s", slug, e)
        return None
    if r.status_code == 404:
        log.warning("404 for slug %r (not on Lever?)", slug)
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
        postings = fetch_postings(company["slug"], session)
        if postings is None:
            stats["failed"] += 1
            continue
        stats["companies"] += 1
        log.info("  board returned %d postings", len(postings))
        if limit_per_company:
            postings = postings[:limit_per_company]
        with db.connect() as conn:
            for posting in postings:
                row = map_posting(company, posting)
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
    p = argparse.ArgumentParser(description="Scrape Lever public boards for Japan jobs.")
    p.add_argument("--delay", type=float, default=1.0)
    p.add_argument("--limit-per-company", type=int, default=None)
    p.add_argument("--only", type=str, default=None)
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
