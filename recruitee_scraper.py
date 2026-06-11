"""
Recruitee public Offers API scraper.

Recruitee publishes an unauthenticated offers endpoint per company:

    https://<company>.recruitee.com/api/offers/

Returns {"offers": [...]} where each offer carries title, slug, description
(HTML), requirements (HTML), location/city/country/country_code, department,
employment_type_code, careers_url, created_at, remote, and sometimes a
structured `salary` block. The description ships inline (single request, like
Greenhouse), so no per-offer detail call is needed.

We iterate companies from companies.json -> "recruitee", filter to Japan, and
upsert into the shared DB. Subdomains that 404 are logged and skipped.

Usage:
    python recruitee_scraper.py [--delay 1.0] [--limit-per-company N]
                                [--only <subdomain>] [--dry-run] [-v]
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

SOURCE_NAME = "recruitee"
API_URL_TMPL = "https://{slug}.recruitee.com/api/offers/"
COMPANIES_PATH = Path(__file__).parent / "companies.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

log = logging.getLogger("recruitee")


def _load_companies() -> list[dict]:
    with COMPANIES_PATH.open() as f:
        data = json.load(f)
    return data.get("recruitee", [])


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


def _is_japan(offer: dict, location_str: str) -> bool:
    cc = str(offer.get("country_code") or "").strip().upper()
    if cc == "JP":
        return True
    if str(offer.get("country") or "").strip().lower() in ("japan", "日本"):
        return True
    return inference.is_japan_location(location_str)


def _location_string(offer: dict) -> str:
    # Recruitee exposes a flat `location` plus city/country fields.
    loc = _norm(offer.get("location"))
    if loc:
        return loc
    parts = [offer.get("city"), offer.get("state_name") or offer.get("state_code"), offer.get("country")]
    out = [_norm(str(p)) for p in parts if p]
    if not out and offer.get("remote"):
        return "Remote"
    return ", ".join(dict.fromkeys(out))


def _employment_terms(code: Optional[str]) -> Optional[str]:
    if not code:
        return None
    s = str(code).lower()
    if "full" in s:
        return "Full-time"
    if "part" in s:
        return "Part-time"
    if "intern" in s:
        return "Internship"
    if "contract" in s or "freelance" in s or "temporary" in s:
        return "Contract"
    return _norm(str(code).replace("_", " ").title())


def _interval_to_period(unit: Optional[str]) -> Optional[str]:
    if not unit:
        return None
    s = str(unit).lower()
    if "year" in s or s in ("y", "yr", "annual"):
        return "Year"
    if "month" in s or s == "m":
        return "Month"
    if "hour" in s or s == "h":
        return "Hour"
    if "day" in s:
        return "Day"
    return None


def _recruitee_salary(offer: dict):
    """Best-effort JPY salary from Recruitee's optional structured salary block."""
    sal = offer.get("salary")
    if not isinstance(sal, dict):
        return None, None, None
    currency = str(sal.get("currency") or "").upper()
    if currency and currency != "JPY":
        return None, None, None
    try:
        smin = int(sal["min"]) if sal.get("min") not in (None, "") else None
        smax = int(sal["max"]) if sal.get("max") not in (None, "") else None
    except (TypeError, ValueError, KeyError):
        smin = smax = None
    if smin or smax:
        period = _interval_to_period(sal.get("unit") or sal.get("period")) or "Year"
        return smin, (smax or smin), period
    return None, None, None


def _build_description(offer: dict) -> Optional[str]:
    parts: list[str] = []
    desc = _html_to_text(offer.get("description"))
    if desc:
        parts.append(desc)
    reqs = _html_to_text(offer.get("requirements"))
    if reqs:
        parts.append(f"Requirements: {reqs}")
    out = "\n\n".join(parts)
    if not out:
        return None
    return out if len(out) <= 20_000 else out[:20_000] + " …"


def _offer_url(slug: str, offer: dict) -> str:
    return (offer.get("careers_url") or offer.get("careers_apply_url")
            or f"https://{slug}.recruitee.com/o/{offer.get('slug', '')}")


def map_offer(company: dict, offer: dict) -> Optional[dict]:
    if str(offer.get("status") or "published").lower() not in ("published", "open", "active", ""):
        return None

    location_str = _location_string(offer)
    if not _is_japan(offer, location_str):
        return None

    title = _norm(offer.get("title"))
    if not title:
        return None
    slug = company["slug"]
    url = _offer_url(slug, offer)
    description = _build_description(offer)

    body = description or ""
    japanese_level = inference.infer_jp_level(body)
    english_level = inference.infer_en_level(body)
    overseas_application_ok = inference.infer_visa_sponsorship(body)

    inferred_remote = inference.infer_remote(body)
    if inferred_remote is not None:
        remote_work_ok = inferred_remote
    elif offer.get("remote") is True or "remote" in location_str.lower():
        remote_work_ok = 1
    elif offer.get("remote") is False:
        remote_work_ok = 0
    else:
        remote_work_ok = None

    salary_min, salary_max, salary_period = _recruitee_salary(offer)
    if not salary_min:
        salary_min, salary_max = salary_parser.parse_range(body[:2000])
        salary_period = salary_parser.parse_period(body[:2000])
    salary_raw = None
    if salary_min and salary_max and salary_min != salary_max:
        salary_raw = f"¥{salary_min:,} - ¥{salary_max:,}"
    elif salary_min:
        salary_raw = f"¥{salary_min:,}"

    dept = _norm(offer.get("department")) or None
    post_date = str(offer.get("created_at") or offer.get("published_at") or "")[:10] or None

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {
        "source": SOURCE_NAME,
        "source_job_id": f"{slug}/{offer.get('id') or offer.get('slug')}",
        "url": url,
        "title": title,
        "company_name": company["name"],
        "company_name_jp": None,
        "location": location_str,
        "industries": dept,
        "function": None,
        "work_type": None,
        "career_level": None,
        "employment_terms": _employment_terms(offer.get("employment_type_code") or offer.get("employment_type")),
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


def fetch_offers(slug: str, session: requests.Session, timeout: int = 30) -> Optional[list]:
    url = API_URL_TMPL.format(slug=slug)
    try:
        r = session.get(url, headers=HEADERS, timeout=timeout)
    except requests.RequestException as e:
        log.warning("request failed for %s: %s", slug, e)
        return None
    if r.status_code == 404:
        log.warning("404 for company %r (not on Recruitee?)", slug)
        return None
    if r.status_code != 200:
        log.warning("non-200 for company %r: %s", slug, r.status_code)
        return None
    try:
        data = r.json()
    except ValueError:
        log.warning("non-JSON response for %r", slug)
        return None
    return data.get("offers") or []


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
        offers = fetch_offers(company["slug"], session)
        if offers is None:
            stats["failed"] += 1
            continue
        stats["companies"] += 1
        log.info("  company returned %d offers", len(offers))
        if limit_per_company:
            offers = offers[:limit_per_company]
        with db.connect() as conn:
            for offer in offers:
                row = map_offer(company, offer)
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
    p = argparse.ArgumentParser(description="Scrape Recruitee public offers for Japan jobs.")
    p.add_argument("--delay", type=float, default=1.0)
    p.add_argument("--limit-per-company", type=int, default=None)
    p.add_argument("--only", type=str, default=None, help="Only fetch the given subdomain.")
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
