"""
Salesforce careers scraper (Japan only).

Salesforce's careers site (salesforce.com/company/careers) is a static front-end
that loads every open requisition from public, unauthenticated JSON files on the
Salesforce CDN — a Workday report export:

    https://a.sfdcstatic.com/digital/xsf/careers/prod/jobs_1.json
    https://a.sfdcstatic.com/digital/xsf/careers/prod/jobs_2.json
    ... (jobs_N.json until a 404)

Each file has {"Report_Entry": [ {job}, ... ]}. We concatenate the files, keep
only postings whose primary location is in Japan, map them to our schema, and
upsert into the shared DB. (The public Eightfold API is bot-protected; these
static files are the same data the site itself reads, so we use them directly.)

Usage:
    python salesforce_scraper.py [--dry-run] [--limit N] [-v]
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from datetime import datetime, timezone
from typing import Optional

import requests
from bs4 import BeautifulSoup

import db
import inference

SOURCE_NAME = "salesforce"
COMPANY_NAME = "Salesforce"
COMPANY_NAME_JP = "株式会社セールスフォース・ジャパン"
CDN_TMPL = "https://a.sfdcstatic.com/digital/xsf/careers/prod/jobs_{n}.json"
MAX_FILES = 20  # safety cap; real count is ~2 today, loop stops on first 404

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

log = logging.getLogger("salesforce")


def _norm(s: Optional[str]) -> str:
    return re.sub(r"\s+", " ", s).strip() if s else ""


def _html_to_text(html_str: Optional[str], cap: int = 20_000) -> Optional[str]:
    if not html_str:
        return None
    soup = BeautifulSoup(html_str, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    # Keep paragraph/line structure readable.
    for br in soup.find_all("br"):
        br.replace_with("\n")
    text = soup.get_text("\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text).strip()
    return text[:cap] or None


def _format_location(primary: str) -> str:
    """'Japan - Tokyo' -> 'Tokyo, Japan'; 'Japan - Remote' -> 'Remote, Japan'."""
    parts = [p.strip() for p in (primary or "").split(" - ") if p.strip()]
    rest = [p for p in parts if p.lower() != "japan"]
    return (", ".join(rest) + ", Japan") if rest else "Japan"


def _employment_terms(job: dict) -> Optional[str]:
    et = (job.get("Employee_Type") or "").strip().lower()
    tt = (job.get("Time_Type") or "").strip().lower()
    if "intern" in et:
        return "Internship"
    if "contract" in et or "fixed" in et:
        return "Contract"
    if "part" in tt:
        return "Part-time"
    if "full" in tt:
        return "Full-time"
    return None


def _remote_ok(job: dict, body: str, location: str) -> Optional[int]:
    # Body signal wins (an explicit "onsite only" beats a flexible tag).
    inferred = inference.infer_remote(body)
    if inferred is not None:
        return inferred
    rt = (job.get("remoteType") or "").lower()
    if "remote" in rt or "remote" in location.lower():
        return 1
    if "flexible" in rt:  # Salesforce "Office - Flexible" == hybrid
        return 1
    return None


def map_job(job: dict) -> Optional[dict]:
    """Map one Salesforce requisition -> our schema dict. Japan only."""
    primary = str(job.get("Job_Requisition_Primary_Location") or "")
    location = _format_location(primary)
    if not (primary.startswith("Japan") or "Japan" in (job.get("Countries") or [])):
        return None
    if not inference.is_japan_location(location):
        return None

    title = _norm(job.get("Job_Posting_Title"))
    url = _norm(job.get("External_Job_Posting_Site"))
    if not title or not url:
        return None

    description = _html_to_text(job.get("Job_Description"))
    body = description or ""
    family = _norm(job.get("Job_Family_Group")) or None  # e.g. "Sales", "Customer Success"
    post_date = (job.get("External_Job_Posting_Start_Date") or "")[:10] or None
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    return {
        "source": SOURCE_NAME,
        "source_job_id": _norm(job.get("Job_Requisition_Ref_ID")) or None,
        "url": url,
        "application_url": url,
        "title": title,
        "company_name": COMPANY_NAME,
        "company_name_jp": COMPANY_NAME_JP,
        "location": location,
        "industries": family,
        "function": family,
        "work_type": None,
        "career_level": None,
        "employment_terms": _employment_terms(job),
        "employer_type": "Foreign-capital",
        "salary": None,  # Salesforce does not disclose JP salary in the feed
        "salary_period": None,
        "english_level": inference.infer_en_level(body),
        "japanese_level": inference.infer_jp_level(body),
        "other_language": None,
        "overseas_application_ok": inference.infer_visa_sponsorship(body),
        "remote_work_ok": _remote_ok(job, body, location),
        "has_video_presentation": None,
        "requirements": None,
        "description": description,
        "tags": family,
        "post_date": post_date,
        "last_modified_date": None,
        "scraped_at": now,
        "last_seen_at": now,
    }


def fetch_all_entries(session: requests.Session, timeout: int = 60) -> list[dict]:
    entries: list[dict] = []
    for n in range(1, MAX_FILES + 1):
        url = CDN_TMPL.format(n=n)
        try:
            resp = session.get(url, headers=HEADERS, timeout=timeout)
        except requests.RequestException as e:
            log.warning("jobs_%d.json fetch failed: %s", n, e)
            break
        if resp.status_code == 404:
            break
        if resp.status_code != 200:
            log.warning("jobs_%d.json -> HTTP %d, stopping", n, resp.status_code)
            break
        chunk = resp.json().get("Report_Entry", [])
        log.info("jobs_%d.json: %d entries", n, len(chunk))
        entries.extend(chunk)
    return entries


def _dedupe(entries: list[dict]) -> list[dict]:
    """The CDN ships a light index (jobs_1, no descriptions) and a full file
    (jobs_2) covering the same requisitions. Collapse to one record per req,
    keeping the entry with the richest Job_Description."""
    best: dict[str, dict] = {}
    for j in entries:
        key = j.get("Job_Requisition_Ref_ID") or j.get("External_Job_Posting_Site")
        if not key:
            continue
        cur = best.get(key)
        if cur is None or len(j.get("Job_Description") or "") > len(cur.get("Job_Description") or ""):
            best[key] = j
    return list(best.values())


def run(dry_run: bool, limit: Optional[int]) -> dict:
    session = requests.Session()
    entries = _dedupe(fetch_all_entries(session))
    log.info("fetched %d unique Salesforce requisitions", len(entries))

    stats = {"japan": 0, "inserted": 0, "updated": 0, "skipped": 0}
    with db.connect() as conn:
        for raw in entries:
            row = map_job(raw)
            if row is None:
                continue
            stats["japan"] += 1
            if limit and stats["japan"] > limit:
                stats["japan"] -= 1
                break
            if dry_run:
                stats["skipped"] += 1
                log.debug("would upsert: %s | %s", row["title"], row["location"])
                continue
            try:
                result = db.upsert_job(conn, row)
                stats[result] += 1
            except Exception as e:  # noqa: BLE001 — one bad row shouldn't kill the run
                log.warning("upsert failed for %s: %s", row.get("url"), e)
                stats["skipped"] += 1
        if not dry_run:
            conn.commit()
    return stats


def main() -> int:
    ap = argparse.ArgumentParser(description="Scrape Salesforce Japan jobs.")
    ap.add_argument("--dry-run", action="store_true", help="don't write to the DB")
    ap.add_argument("--limit", type=int, default=None, help="cap Japan jobs processed")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )
    stats = run(dry_run=args.dry_run, limit=args.limit)
    log.info("Salesforce Japan: %d found | inserted=%d updated=%d skipped=%d",
             stats["japan"], stats["inserted"], stats["updated"], stats["skipped"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
