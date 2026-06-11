"""
Japan Dev (japan-dev.com) scraper.

Japan Dev is a hand-curated board of English-friendly IT jobs in Japan, so it
overlaps closely with our foreigner-fit goal. The /jobs listing is
server-rendered: every card carries the job URL, title, company, a visa badge
("Residents Only" vs "Anywhere" / "Sponsors Visas"), a salary range (¥XM ~ ¥YM),
location, and remote tags. We parse that markup with BeautifulSoup, key off the
stable job-URL pattern (/jobs/<company>/<slug>) rather than brittle class names,
and upsert into the shared DB.

Design choices:
  * parse_listing(html) is isolated and pure so it can be unit-tested against a
    saved page without any network.
  * We never bypass anti-bot protection; this is a plain GET of a public,
    server-rendered HTML page (same approach as the Robert Walters scraper).

Usage:
    python japandev_scraper.py [--pages N] [--delay 1.0] [--dry-run] [-v]
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import time
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

import db
import inference
import salary_parser

SOURCE_NAME = "japandev"
BASE = "https://japan-dev.com"
LISTING_URL = "https://japan-dev.com/jobs"
# A job detail link looks like /jobs/<company-slug>/<job-slug-with-id>.
JOB_HREF_RE = re.compile(r"^/jobs/([^/?#]+)/([^/?#]+)/?$")
# Salary like "¥5M ~ ¥10M", "¥7M~¥9M", or "5 ~ 10mil".
SALARY_RE = re.compile(
    r"¥?\s*(\d+(?:\.\d+)?)\s*(?:M|mil|million|百万|万)?\s*[~〜\-–]\s*¥?\s*(\d+(?:\.\d+)?)\s*(?:M|mil|million|百万|万)?",
    re.IGNORECASE,
)
SINGLE_SALARY_RE = re.compile(r"¥\s*(\d+(?:\.\d+)?)\s*(?:M|mil|million)", re.IGNORECASE)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}

log = logging.getLogger("japandev")


def _norm(s: Optional[str]) -> str:
    return re.sub(r"\s+", " ", s).strip() if s else ""


def _titleize_slug(slug: str) -> str:
    s = re.sub(r"[-_]+", " ", slug).strip()
    # Keep short all-caps acronyms uppercase, title-case the rest.
    return " ".join(w.upper() if len(w) <= 3 else w.capitalize() for w in s.split())


def _millions_to_jpy(value: str) -> Optional[int]:
    try:
        return int(round(float(value) * 1_000_000))
    except (TypeError, ValueError):
        return None


def _parse_salary(text: str):
    """Return (min_jpy, max_jpy) from a card's text, or (None, None)."""
    if not text:
        return None, None
    m = SALARY_RE.search(text)
    if m:
        lo = _millions_to_jpy(m.group(1))
        hi = _millions_to_jpy(m.group(2))
        if lo and hi and lo > hi:
            lo, hi = hi, lo
        return lo, hi
    m = SINGLE_SALARY_RE.search(text)
    if m:
        v = _millions_to_jpy(m.group(1))
        return v, v
    return None, None


def parse_listing(html: str) -> list[dict]:
    """Pure parser: HTML -> list of raw job dicts. No network, no DB."""
    soup = BeautifulSoup(html, "lxml")
    seen: set[str] = set()
    out: list[dict] = []

    for a in soup.find_all("a", href=True):
        m = JOB_HREF_RE.match(a["href"].split("?")[0])
        if not m:
            continue
        href = a["href"].split("?")[0].rstrip("/")
        company_slug, job_slug = m.group(1), m.group(2)
        if href in seen:
            continue

        # Find the card container: climb up while the subtree still contains only
        # THIS job's link. Stop before the ancestor merges in a sibling card. This
        # isolates one card without depending on class names.
        card = a
        while card.parent is not None:
            parent = card.parent
            distinct = {
                x["href"].split("?")[0].rstrip("/")
                for x in parent.find_all("a", href=True)
                if JOB_HREF_RE.match(x["href"].split("?")[0])
            }
            if len(distinct) > 1:
                break
            card = parent
        card_text = _norm(card.get_text(" ", strip=True))

        # Title: prefer a heading link with this href and non-empty text.
        title = _norm(a.get_text(" ", strip=True))
        if not title:
            for sib in card.find_all("a", href=True):
                if sib["href"].split("?")[0].rstrip("/") == href and _norm(sib.get_text(" ", strip=True)):
                    title = _norm(sib.get_text(" ", strip=True))
                    break
        if not title:
            continue
        if href in seen:
            continue
        seen.add(href)

        # Company: prefer a clean /companies/<slug> link text; else read the run
        # of text right after the title up to the first badge/salary/stop token;
        # else titleize the company slug. Keeps the company name from swallowing
        # the rest of the card.
        company = ""
        comp_link = card.find("a", href=re.compile(r"^/companies/"))
        if comp_link:
            company = _norm(comp_link.get_text(" ", strip=True))
        if not company and title in card_text:
            after = card_text.split(title, 1)[-1].lstrip(" |·・-•")
            # Cut at the first thing that is clearly NOT part of a company name.
            stop = re.search(
                r"(Japanese|English|Residents|Anywhere|Sponsors|Remote|Partial|Apply|"
                r"Visa|Level|¥|\d|🇯🇵|🌎|🏠|Tokyo|Osaka|Kyoto|Nagoya|Fukuoka|Yokohama|"
                r"Kanagawa|Sapporo|Kobe)", after)
            if stop:
                after = after[:stop.start()]
            company = _norm(after.split("・")[0].split("•")[0])
        if not company or len(company) > 50:
            company = _titleize_slug(company_slug)

        sal_min, sal_max = _parse_salary(card_text)

        # Visa: "Residents Only" => Japan residents only; "Anywhere"/"Sponsors Visas" => from abroad.
        low = card_text.lower()
        if "residents only" in low or "japanese required" in low and "not required" not in low:
            overseas_ok = 0
        elif "anywhere" in low or "sponsors visa" in low or "apply from overseas" in low:
            overseas_ok = 1
        else:
            overseas_ok = None

        remote = 1 if re.search(r"\bremote\b|partial remote|remote first", low) else None

        # Location: known JP cities mentioned in the card.
        location = ""
        for city in ("Tokyo", "Osaka", "Kyoto", "Nagoya", "Fukuoka", "Yokohama",
                     "Kanagawa", "Sapporo", "Kobe", "Remote"):
            if re.search(r"\b" + re.escape(city) + r"\b", card_text):
                location = city
                break

        out.append({
            "company_slug": company_slug,
            "job_slug": job_slug,
            "url": urljoin(BASE, href),
            "title": title,
            "company": company,
            "location": location,
            "salary_min_jpy": sal_min,
            "salary_max_jpy": sal_max,
            "overseas_application_ok": overseas_ok,
            "remote_work_ok": remote,
            "card_text": card_text[:2000],
        })
    return out


def _html_to_text(html_str: Optional[str], cap: int = 20_000) -> Optional[str]:
    if not html_str:
        return None
    text = BeautifulSoup(html_str, "lxml").get_text(" ", strip=True)
    text = _norm(text)
    if not text:
        return None
    return text if len(text) <= cap else text[:cap] + " …"


_DETAIL_STOP = ("Similar jobs you'll love", "Latest Tech Jobs", "Get Job Alerts",
                "More jobs from", "About ", "↑ Back to top")
_JP_RE = re.compile(r"Japanese:\s*(Not Required|Basic[\w /-]*|Conversational|Business[\w /-]*|Fluent|Native[\w /-]*)", re.I)
_EN_RE = re.compile(r"English:\s*(Not Required|Conversational|Business Level|Business[\w /-]*|Fluent|Native[\w /-]*)", re.I)
_APPLY_RE = re.compile(r"Apply from\s*\*?\*?\s*(Japan Only|Anywhere)", re.I)
_EXP_RE = re.compile(r"Minimum Experience\s*(Senior or above|Mid[\- ]level|Junior|New Grad)", re.I)
_EMP_RE = re.compile(r"\b(Full[\- ]time|Part[\- ]time|Contract|Internship)\b", re.I)


def _iter_jsonld(soup) -> list:
    out = []
    for tag in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(tag.string or tag.get_text() or "")
        except (ValueError, TypeError):
            continue
        items = data.get("@graph", [data]) if isinstance(data, dict) else (data if isinstance(data, list) else [])
        out.extend(i for i in items if isinstance(i, dict))
    return out


def parse_detail(html: str) -> dict:
    """Pure parser: detail-page HTML -> enrichment dict. Prefers JobPosting
    JSON-LD for the description/date/employment, then supplements with Japan
    Dev's consistent on-page labels for JP/EN level, experience, and apply-from."""
    soup = BeautifulSoup(html, "lxml")
    out: dict = {}

    # 1) JobPosting JSON-LD (cleanest when present).
    for item in _iter_jsonld(soup):
        t = item.get("@type")
        types = t if isinstance(t, list) else [t]
        if "JobPosting" not in types:
            continue
        desc = _html_to_text(item.get("description"))
        if desc:
            out["description"] = desc
        if item.get("datePosted"):
            out["post_date"] = str(item["datePosted"])[:10]
        et = item.get("employmentType")
        if et:
            et = et[0] if isinstance(et, list) else et
            out["employment_terms"] = _employment_label(str(et))
        break

    text = soup.get_text(" ", strip=True)

    # 2) Description fallback: main content between the role body and the
    #    "About <company>" / similar-jobs sections.
    if "description" not in out:
        start = 0
        for marker in ("Role Overview", "Job Description", "Conditions"):
            i = text.find(marker)
            if i != -1:
                start = i
                break
        end = len(text)
        for marker in _DETAIL_STOP:
            i = text.find(marker, start + 20)
            if i != -1:
                end = min(end, i)
        body = _norm(text[start:end])
        if len(body) > 80:
            out["description"] = body[:20_000]

    # 3) On-page labels (Japan Dev specific).
    m = _JP_RE.search(text)
    if m:
        out["japanese_level"] = inference.normalize_level_label(_norm(m.group(1)))
    m = _EN_RE.search(text)
    if m:
        out["english_level"] = inference.normalize_level_label(_norm(m.group(1)))
    m = _EXP_RE.search(text)
    if m:
        out["career_level"] = _norm(m.group(1))
    m = _APPLY_RE.search(text)
    if m:
        out["overseas_application_ok"] = 0 if m.group(1).lower().startswith("japan") else 1
    if "employment_terms" not in out:
        m = _EMP_RE.search(text)
        if m:
            out["employment_terms"] = _employment_label(m.group(1))
    return out


def _employment_label(value: str) -> Optional[str]:
    s = str(value).lower()
    if "full" in s:
        return "Full-time"
    if "part" in s:
        return "Part-time"
    if "intern" in s:
        return "Internship"
    if "contract" in s or "temporary" in s:
        return "Contract"
    return _norm(value) or None


def fetch_detail(url: str, session: requests.Session, timeout: int = 30) -> Optional[str]:
    try:
        r = session.get(url, headers=HEADERS, timeout=timeout)
    except requests.RequestException as e:
        log.debug("detail request failed for %s: %s", url, e)
        return None
    if r.status_code != 200:
        log.debug("detail non-200 for %s: %s", url, r.status_code)
        return None
    return r.text


def map_job(raw: dict) -> Optional[dict]:
    """Normalize a parsed raw job -> our DB schema row. None if unusable."""
    title = _norm(raw.get("title"))
    if not title or not raw.get("url"):
        return None
    # Japan Dev is Japan-only by definition; trust the source, but keep a guard.
    location = _norm(raw.get("location")) or "Japan"

    # Prefer the enriched detail description; fall back to the listing card text.
    description = raw.get("description")
    body = description or raw.get("card_text") or ""

    # Explicit on-page levels (from detail enrichment) win over inference.
    english_level = raw.get("english_level") or inference.infer_en_level(body)
    japanese_level = raw.get("japanese_level") or inference.infer_jp_level(body)
    if japanese_level is None and "residents only" not in (raw.get("card_text") or "").lower():
        # Japan Dev curates English-friendly roles; absent a JP requirement,
        # default to not-required rather than leaving it blank.
        japanese_level = inference.normalize_level_label("Not Required")

    sal_min = raw.get("salary_min_jpy")
    sal_max = raw.get("salary_max_jpy")
    salary_raw = None
    if sal_min and sal_max and sal_min != sal_max:
        salary_raw = f"¥{sal_min:,} - ¥{sal_max:,}"
    elif sal_min:
        salary_raw = f"¥{sal_min:,}"

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {
        "source": SOURCE_NAME,
        "source_job_id": f"{raw['company_slug']}/{raw['job_slug']}",
        "url": raw["url"],
        "title": title,
        "is_employer_post": 0,
        "company_name": _norm(raw.get("company")) or None,
        "company_name_jp": None,
        "location": location,
        "industries": None,
        "function": None,
        "work_type": None,
        "career_level": _norm(raw.get("career_level")) or None,
        "employment_terms": raw.get("employment_terms"),
        "employer_type": None,
        "salary": salary_raw,
        "salary_period": "Year" if sal_min else None,
        "salary_perks": None,
        "salary_min_jpy": sal_min,
        "salary_max_jpy": sal_max,
        "salary_min_annual_jpy": sal_min,   # Japan Dev ranges are annual
        "salary_max_annual_jpy": sal_max,
        "english_level": english_level,
        "japanese_level": japanese_level,
        "other_language": None,
        "overseas_application_ok": raw.get("overseas_application_ok"),
        "remote_work_ok": raw.get("remote_work_ok"),
        "has_video_presentation": None,
        "requirements": None,
        "description": description,   # full text when detail-enriched, else None
        "tags": None,
        "post_date": _norm(raw.get("post_date")) or None,
        "last_modified_date": None,
        "scraped_at": now,
        "last_seen_at": now,
    }


def fetch_listing(page: int, session: requests.Session, timeout: int = 30) -> Optional[str]:
    url = LISTING_URL if page <= 1 else f"{LISTING_URL}?page={page}"
    try:
        r = session.get(url, headers=HEADERS, timeout=timeout)
    except requests.RequestException as e:
        log.warning("request failed (page %d): %s", page, e)
        return None
    if r.status_code != 200:
        log.warning("non-200 (page %d): %s", page, r.status_code)
        return None
    return r.text


def run(pages: int = 1, delay: float = 1.0, debug: bool = False,
        dry_run: bool = False, limit: Optional[int] = None,
        enrich: bool = True, enrich_delay: float = 0.6) -> dict:
    db.init_db()
    session = requests.Session()
    stats = {"inserted": 0, "updated": 0, "failed": 0, "skipped": 0,
             "non_japan": 0, "enriched": 0}

    total_seen = 0
    for page in range(1, max(1, pages) + 1):
        if page > 1:
            time.sleep(delay)
        html = fetch_listing(page, session)
        if html is None:
            stats["failed"] += 1
            continue
        raws = parse_listing(html)
        log.info("page %d: parsed %d job cards", page, len(raws))
        if not raws:
            break  # no more pages / nothing parsed
        for raw in raws:
            if limit and total_seen >= limit:
                break
            total_seen += 1
            # Detail-page enrichment: fetch full description + explicit JP/EN
            # level, employment type, experience, apply-from, post date.
            if enrich:
                time.sleep(enrich_delay)
                detail_html = fetch_detail(raw["url"], session)
                if detail_html:
                    extra = parse_detail(detail_html)
                    if extra:
                        raw.update(extra)
                        stats["enriched"] += 1
            row = map_job(raw)
            if row is None:
                stats["skipped"] += 1
                continue
            if dry_run:
                log.info("  [dry-run] %s | %s | %s | %s | jp=%s en=%s desc=%dch",
                         row["title"], row["company_name"], row["location"], row["salary"],
                         row["japanese_level"], row["english_level"],
                         len(row["description"] or ""))
                continue
            try:
                with db.connect() as conn:
                    result = db.upsert_job(conn, row)
                stats[result] += 1
            except Exception as e:
                log.exception("upsert failed for %s: %s", row.get("url"), e)
                stats["failed"] += 1
        if limit and total_seen >= limit:
            break

    return stats


def main() -> int:
    p = argparse.ArgumentParser(description="Scrape Japan Dev (server-rendered listing) for Japan jobs.")
    p.add_argument("--pages", type=int, default=1)
    p.add_argument("--delay", type=float, default=1.0)
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--no-enrich", action="store_true",
                   help="Skip per-job detail fetch (faster, but lower-quality fit scores).")
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
                dry_run=args.dry_run, limit=args.limit, enrich=not args.no_enrich)
    log.info("done: %s", stats)
    return 0 if (stats["inserted"] + stats["updated"]) > 0 or args.dry_run else 1


if __name__ == "__main__":
    sys.exit(main())
