"""
Microsoft careers scraper (Japan only).

Microsoft's careers site (apply.careers.microsoft.com) runs on Eightfold's
"PCSX" backend and exposes two public, unauthenticated JSON endpoints that the
site itself calls:

    .../api/pcsx/search?domain=microsoft.com&location=Japan&start=N   (10/page)
    .../api/pcsx/position_details?position_id=<id>&domain=microsoft.com

The search feed paginates the Japan postings (title, location, department,
posted date, apply URL); the details feed carries the HTML job description. We
page through search, fetch each description (throttled, with 429 back-off), map
to our schema, and upsert into the shared DB.

The endpoint rate-limits, so be polite: a delay between detail calls and an
exponential back-off on HTTP 429. A job whose description can't be fetched is
still stored (without the body) rather than dropped.

Usage:
    python microsoft_scraper.py [--dry-run] [--limit N] [--delay 1.2] [-v]
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
import time
from datetime import datetime, timezone
from typing import Optional

import requests
from bs4 import BeautifulSoup

import db
import inference

SOURCE_NAME = "microsoft"
COMPANY_NAME = "Microsoft"
COMPANY_NAME_JP = "日本マイクロソフト株式会社"
BASE = "https://apply.careers.microsoft.com"
SEARCH_URL = BASE + "/api/pcsx/search"
DETAILS_URL = BASE + "/api/pcsx/position_details"
PAGE_SIZE = 10

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Referer": BASE + "/careers",
}

log = logging.getLogger("microsoft")


def _norm(s: Optional[str]) -> str:
    return re.sub(r"\s+", " ", s).strip() if s else ""


def _html_to_text(html_str: Optional[str], cap: int = 20_000) -> Optional[str]:
    if not html_str:
        return None
    soup = BeautifulSoup(html_str, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    for br in soup.find_all("br"):
        br.replace_with("\n")
    text = soup.get_text("\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text).strip()
    return text[:cap] or None


def _get_json(session: requests.Session, url: str, params: dict,
              delay: float, retries: int = 4) -> Optional[dict]:
    """GET JSON with exponential back-off on HTTP 429 / transient errors."""
    for attempt in range(retries):
        try:
            r = session.get(url, params=params, headers=HEADERS, timeout=30)
        except requests.RequestException as e:
            log.debug("request error (%s); retrying", e)
            time.sleep(delay * (2 ** attempt))
            continue
        if r.status_code == 429:
            wait = delay * (2 ** (attempt + 1))
            log.info("429 rate-limited; backing off %.1fs", wait)
            time.sleep(wait)
            continue
        if r.status_code != 200:
            log.debug("HTTP %d for %s", r.status_code, url)
            return None
        try:
            return r.json()
        except ValueError:
            return None
    return None


def _format_location(pos: dict) -> str:
    """Build a clean 'City, Japan' from standardizedLocations like
    ['JP', 'Tokyo, Tokyo, JP', 'Osaka, Osaka, JP']."""
    std = pos.get("standardizedLocations") or []
    cities: list[str] = []
    for s in std:
        parts = [p.strip() for p in str(s).split(",") if p.strip()]
        if len(parts) >= 2 and parts[-1].upper() == "JP":
            city = parts[0]
            if city and city not in cities:
                cities.append(city)
    if cities:
        return ", ".join(cities[:3]) + ", Japan"
    # Fall back to the raw locations list (e.g. "Japan, Tokyo-to, Tokyo").
    raw = pos.get("locations") or []
    if raw:
        first = str(raw[0])
        if "multiple" in first.lower():
            return "Multiple Locations, Japan"
    return "Japan"


def _is_japan(pos: dict) -> bool:
    std = pos.get("standardizedLocations") or []
    if any(str(s).upper().endswith("JP") or str(s).upper() == "JP" for s in std):
        return True
    return "japan" in " ".join(str(x) for x in (pos.get("locations") or [])).lower()


def _employment_terms(emp) -> Optional[str]:
    if isinstance(emp, list):
        emp = emp[0] if emp else ""
    e = str(emp or "").strip().lower()
    if not e:
        return None
    if "intern" in e:
        return "Internship"
    if "part" in e:
        return "Part-time"
    if "full" in e:
        return "Full-time"
    if "contract" in e or "fixed" in e:
        return "Contract"
    return None


def _remote_ok(pos: dict, body: str) -> Optional[int]:
    inferred = inference.infer_remote(body)
    if inferred is not None:
        return inferred
    opt = (pos.get("workLocationOption") or "").lower()
    flex = str(pos.get("locationFlexibility") or "").lower()
    if "remote" in opt or "remote" in flex:
        return 1
    if "hybrid" in opt or "flex" in opt or "flex" in flex:
        return 1
    if opt == "onsite":
        return 0
    return None


def _post_date(ts) -> Optional[str]:
    try:
        return datetime.fromtimestamp(int(ts), tz=timezone.utc).date().isoformat()
    except (TypeError, ValueError, OSError):
        return None


def map_position(pos: dict, details: Optional[dict]) -> Optional[dict]:
    if not _is_japan(pos):
        return None
    title = _norm(pos.get("name"))
    rel = pos.get("positionUrl") or ""
    url = (BASE + rel) if rel.startswith("/") else (rel or "")
    if details and details.get("publicUrl"):
        url = details["publicUrl"]
    if not title or not url:
        return None

    det = details or {}
    description = _html_to_text(det.get("jobDescription"))
    body = description or ""
    location = _format_location(pos)
    department = _norm(pos.get("department")) or None
    emp = det.get("efcustomTextEmploymentType")
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    return {
        "source": SOURCE_NAME,
        "source_job_id": _norm(str(pos.get("displayJobId") or pos.get("atsJobId") or "")) or None,
        "url": url,
        "application_url": url,
        "title": title,
        "company_name": COMPANY_NAME,
        "company_name_jp": COMPANY_NAME_JP,
        "location": location,
        "industries": department,
        "function": department,
        "work_type": None,
        "career_level": None,
        "employment_terms": _employment_terms(emp),
        "employer_type": "Foreign-capital",
        "salary": None,  # Microsoft does not disclose JP salary in the feed
        "salary_period": None,
        "english_level": inference.infer_en_level(body),
        "japanese_level": inference.infer_jp_level(body),
        "other_language": None,
        "overseas_application_ok": inference.infer_visa_sponsorship(body),
        "remote_work_ok": _remote_ok(pos, body),
        "has_video_presentation": None,
        "requirements": None,
        "description": description,
        "tags": department,
        "post_date": _post_date(pos.get("postedTs")),
        "last_modified_date": None,
        "scraped_at": now,
        "last_seen_at": now,
    }


def fetch_positions(session: requests.Session, delay: float,
                    limit: Optional[int]) -> list[dict]:
    base_params = {
        "domain": "microsoft.com",
        "query": "",
        "location": "Japan",
        "sort_by": "distance",
        "filter_include_remote": 1,
    }
    positions: list[dict] = []
    start = 0
    total = None
    while True:
        params = dict(base_params, start=start)
        data = _get_json(session, SEARCH_URL, params, delay)
        if not data or "data" not in data:
            break
        d = data["data"]
        if total is None:
            total = d.get("count", 0)
            log.info("Microsoft Japan: %s positions reported", total)
        chunk = d.get("positions") or []
        if not chunk:
            break
        positions.extend(chunk)
        start += PAGE_SIZE
        if limit and len(positions) >= limit:
            break
        if total is not None and start >= total:
            break
        time.sleep(delay)
    return positions[: limit] if limit else positions


def run(dry_run: bool, limit: Optional[int], delay: float = 1.2) -> dict:
    session = requests.Session()
    positions = fetch_positions(session, delay, limit)
    log.info("fetched %d Microsoft Japan positions", len(positions))

    stats = {"japan": 0, "inserted": 0, "updated": 0, "skipped": 0, "no_desc": 0}
    with db.connect() as conn:
        for pos in positions:
            pid = pos.get("id")
            details = _get_json(
                session, DETAILS_URL,
                {"position_id": pid, "domain": "microsoft.com", "hl": "en",
                 "queried_location": "Japan"},
                delay,
            )
            details = (details or {}).get("data") if details else None
            if not (details and details.get("jobDescription")):
                stats["no_desc"] += 1
            row = map_position(pos, details)
            time.sleep(delay)
            if row is None:
                continue
            stats["japan"] += 1
            if dry_run:
                stats["skipped"] += 1
                log.debug("would upsert: %s | %s", row["title"], row["location"])
                continue
            try:
                stats[db.upsert_job(conn, row)] += 1
            except Exception as e:  # noqa: BLE001
                log.warning("upsert failed for %s: %s", row.get("url"), e)
                stats["skipped"] += 1
        if not dry_run:
            conn.commit()
    return stats


def main() -> int:
    ap = argparse.ArgumentParser(description="Scrape Microsoft Japan jobs.")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--delay", type=float, default=1.2, help="seconds between API calls")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )
    stats = run(dry_run=args.dry_run, limit=args.limit, delay=args.delay)
    log.info("Microsoft Japan: %d mapped | inserted=%d updated=%d skipped=%d no_desc=%d",
             stats["japan"], stats["inserted"], stats["updated"], stats["skipped"],
             stats["no_desc"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
