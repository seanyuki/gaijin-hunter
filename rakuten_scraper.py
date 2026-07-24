"""
Rakuten careers scraper (Japan, English-required roles only).

Rakuten's English careers site (japan-job-en.rakuten.careers) is a JS-only
Phenom front end, but it applies through Workday, whose public CXS JSON API
serves the same 670 postings cleanly:

    POST .../wday/cxs/rakuten/RakutenInc/jobs    {limit, offset, searchText}
    GET  .../wday/cxs/rakuten/RakutenInc<externalPath>   -> full description

Rakuten states the required language level in a structured form inside each
description, e.g. "English (Overall - 3 - Advanced)" / "(Overall - 4 - Fluent)".
By request we keep only roles that require English at Advanced (Level 3) or
Fluent (Level 4) — the same level the Japanese (Overall - N - …) clause is
ignored for. Roles that don't state an English level, or require only
Intermediate/Basic, are skipped.

Usage:
    python rakuten_scraper.py [--dry-run] [--limit N] [--delay 0.3]
                              [--min-english 3] [-v]
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

SOURCE_NAME = "rakuten"
COMPANY_NAME = "Rakuten"
COMPANY_NAME_JP = "楽天グループ株式会社"
CXS = "https://rakuten.wd1.myworkdayjobs.com/wday/cxs/rakuten/RakutenInc"
SITE = "https://rakuten.wd1.myworkdayjobs.com/en-US/RakutenInc"
PAGE_SIZE = 20

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

# Rakuten language level -> our english_level / japanese_level vocabulary.
_LEVEL_LABEL = {5: "Native", 4: "Fluent", 3: "Business / Professional",
                2: "Conversational", 1: "Basic"}
_ENGLISH_RE = re.compile(r"English\s*[\(（]\s*Overall\s*-\s*([1-5])", re.IGNORECASE)
_JAPANESE_RE = re.compile(r"Japanese\s*[\(（]\s*Overall\s*-\s*([1-5])", re.IGNORECASE)

log = logging.getLogger("rakuten")


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


def _level(regex: re.Pattern, text: str) -> Optional[int]:
    m = regex.search(text or "")
    return int(m.group(1)) if m else None


def fetch_list(session: requests.Session, delay: float,
               limit: Optional[int]) -> list[dict]:
    postings: list[dict] = []
    offset, total = 0, None
    while True:
        r = session.post(f"{CXS}/jobs", headers=HEADERS,
                         json={"appliedFacets": {}, "limit": PAGE_SIZE,
                               "offset": offset, "searchText": ""}, timeout=30)
        if r.status_code != 200:
            log.warning("list HTTP %d at offset %d", r.status_code, offset)
            break
        data = r.json()
        if total is None:
            total = data.get("total", 0)
            log.info("Rakuten: %s total postings", total)
        chunk = data.get("jobPostings") or []
        if not chunk:
            break
        postings.extend(chunk)
        offset += PAGE_SIZE
        if (limit and len(postings) >= limit) or offset >= (total or 0):
            break
        time.sleep(delay)
    return postings


def fetch_detail(session: requests.Session, external_path: str) -> Optional[dict]:
    try:
        r = session.get(f"{CXS}{external_path}", headers=HEADERS, timeout=30)
    except requests.RequestException as e:
        log.debug("detail error %s: %s", external_path, e)
        return None
    if r.status_code != 200:
        return None
    return (r.json() or {}).get("jobPostingInfo")


def map_job(posting: dict, info: dict, min_english: int) -> Optional[dict]:
    """Map a Workday posting+detail to our schema, or None if it doesn't
    require English at >= min_english (Advanced=3 / Fluent=4)."""
    description = _html_to_text(info.get("jobDescription"))
    body = description or ""
    en_lvl = _level(_ENGLISH_RE, body)
    if en_lvl is None or en_lvl < min_english:
        return None  # not an English-required role at the requested level

    title = _norm(info.get("title") or posting.get("title"))
    ext_path = posting.get("externalPath") or ""
    url = info.get("externalUrl") or (SITE + ext_path if ext_path else "")
    if not title or not url:
        return None

    jp_lvl = _level(_JAPANESE_RE, body)
    location = _norm(info.get("location") or posting.get("locationsText")) or "Japan"
    start = info.get("startDate") or info.get("postedOn")
    post_date = None
    if isinstance(start, str) and re.match(r"\d{4}-\d{2}-\d{2}", start):
        post_date = start[:10]
    time_type = (info.get("timeType") or "").lower()
    emp = "Part-time" if "part" in time_type else ("Full-time" if "full" in time_type else None)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    return {
        "source": SOURCE_NAME,
        "source_job_id": _norm(str(info.get("jobReqId") or info.get("jobPostingId") or "")) or None,
        "url": url,
        "application_url": url,
        "title": title,
        "company_name": COMPANY_NAME,
        "company_name_jp": COMPANY_NAME_JP,
        "location": location,
        "industries": None,
        "function": None,
        "work_type": None,
        "career_level": None,
        "employment_terms": emp,
        "employer_type": None,  # Rakuten is a Japanese company (not gaishikei)
        "salary": None,
        "salary_period": None,
        "english_level": _LEVEL_LABEL.get(en_lvl),
        "japanese_level": _LEVEL_LABEL.get(jp_lvl) if jp_lvl else inference.infer_jp_level(body),
        "other_language": None,
        "overseas_application_ok": inference.infer_visa_sponsorship(body),
        "remote_work_ok": inference.infer_remote(body),
        "has_video_presentation": None,
        "requirements": None,
        "description": description,
        "tags": None,
        "post_date": post_date,
        "last_modified_date": None,
        "scraped_at": now,
        "last_seen_at": now,
    }


def run(dry_run: bool, limit: Optional[int], delay: float = 0.3,
        min_english: int = 3) -> dict:
    session = requests.Session()
    postings = fetch_list(session, delay, limit)
    log.info("fetched %d postings; checking English level…", len(postings))

    stats = {"scanned": 0, "english_ok": 0, "inserted": 0, "updated": 0, "skipped": 0}
    with db.connect() as conn:
        for jp in postings:
            ext = jp.get("externalPath")
            if not ext:
                continue
            stats["scanned"] += 1
            info = fetch_detail(session, ext)
            time.sleep(delay)
            if not info:
                continue
            row = map_job(jp, info, min_english)
            if row is None:
                continue
            stats["english_ok"] += 1
            if dry_run:
                stats["skipped"] += 1
                log.debug("would upsert [%s]: %s", row["english_level"], row["title"])
                continue
            try:
                stats[db.upsert_job(conn, row)] += 1
                # Commit periodically so a long run survives interruption.
                if (stats["inserted"] + stats["updated"]) % 25 == 0:
                    conn.commit()
            except Exception as e:  # noqa: BLE001
                log.warning("upsert failed for %s: %s", row.get("url"), e)
                stats["skipped"] += 1
        if not dry_run:
            conn.commit()
    return stats


def main() -> int:
    ap = argparse.ArgumentParser(description="Scrape Rakuten English-required Japan jobs.")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=None, help="cap postings scanned")
    ap.add_argument("--delay", type=float, default=0.3, help="seconds between API calls")
    ap.add_argument("--min-english", type=int, default=3,
                    help="minimum English level to keep (3=Advanced, 4=Fluent)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )
    stats = run(dry_run=args.dry_run, limit=args.limit, delay=args.delay,
                min_english=args.min_english)
    log.info("Rakuten: scanned=%d | English>=%d: %d | inserted=%d updated=%d skipped=%d",
             stats["scanned"], args.min_english, stats["english_ok"],
             stats["inserted"], stats["updated"], stats["skipped"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
