"""
GaijinPot scraper.

Crawl strategy:
  1. Walk /en/job?page=N. Extract candidate detail URLs by URL pattern.
  2. For each detail URL, fetch the page and parse:
       title, company_name, company_name_jp, source_job_id, location,
       post_date, industries, function, work_type, career_level,
       employment_terms, employer_type,
       salary, salary_period, salary_perks,
       requirements (raw text + parsed english/japanese/other language levels),
       remote_work_ok, overseas_application_ok, has_video_presentation,
       description, last_modified_date,
       company_year_founded, company_size, company_about
  3. Upsert into SQLite. Re-running refreshes last_seen_at.

Field extraction uses three layered strategies so the scraper is resilient to
template changes:
  (a) schema.org microdata where present,
  (b) common class names,
  (c) generic "find the label text, return the immediately following text"
      which works whether the page uses <dt>/<dd>, <strong>label</strong>+text,
      label-span/value-span, or label-heading/value-paragraph.

Usage:
  python scraper.py --pages 2
  python scraper.py --pages 1 --limit 5 --debug -v
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterator, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, NavigableString
from dateutil import parser as dateparser

import db
import inference
import salary_parser

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SOURCE_NAME = "gaijinpot"
BASE = "https://jobs.gaijinpot.com"
LISTING_URLS = [
    "https://jobs.gaijinpot.com/en/job?page={page}",
    "https://jobs.gaijinpot.com/en/job",
]
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://jobs.gaijinpot.com/",
}

# A GaijinPot detail URL is /en/job/<id> (sometimes with a trailing slug).
# Require digits after job/ to exclude /en/job?page=2 and the filter URLs.
JOB_URL_RE = re.compile(r"/(?:en/)?job/(?:view/)?\d+(?:/[^?#\s]*)?", re.IGNORECASE)
JOB_ID_RE = re.compile(r"/job/(?:view/)?(\d+)", re.IGNORECASE)

DEBUG_DIR = Path(__file__).parent / "debug"

log = logging.getLogger("scraper")


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

class Fetcher:
    def __init__(self, delay: float = 1.5):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self._last_request: float = 0.0

    def get(self, url: str) -> Optional[str]:
        wait = self.delay - (time.monotonic() - self._last_request)
        if wait > 0:
            time.sleep(wait)
        self._last_request = time.monotonic()
        try:
            r = self.session.get(url, timeout=20)
        except requests.RequestException as e:
            log.warning("request failed: %s -> %s", url, e)
            return None
        if r.status_code != 200:
            log.warning("non-200: %s -> %s", url, r.status_code)
            return None
        return r.text


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------

def _norm(s: Optional[str]) -> str:
    return re.sub(r"\s+", " ", s).strip() if s else ""


def _text(node) -> str:
    return _norm(node.get_text(" ", strip=True)) if node else ""


def _first_text(soup: BeautifulSoup, selectors: list[str]) -> Optional[str]:
    for sel in selectors:
        node = soup.select_one(sel)
        if node:
            t = _text(node)
            if t:
                return t
    return None


# Label-matching: case-insensitive, trailing colon stripped, whitespace collapsed.
def _label_key(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower().rstrip(":")


# Elements that hold filter UI / non-content — labels and values inside these
# are NOT the job's data. Without this guard, GaijinPot's "Industries" filter
# dropdown bleeds its entire option list into the job's industries field.
SKIP_ANCESTORS = {"form", "select", "option", "optgroup", "input",
                  "button", "script", "style", "nav", "footer"}


def _in_skip_zone(node) -> bool:
    """True if this node lives inside a form / select / nav / etc."""
    if node is None:
        return False
    parent = getattr(node, "parent", None)
    while parent is not None:
        if getattr(parent, "name", None) in SKIP_ANCESTORS:
            return True
        parent = getattr(parent, "parent", None)
    return False


def find_value_after_label(soup: BeautifulSoup, labels: list[str]) -> Optional[str]:
    """
    Find the immediately-following text content after the first element whose
    text exactly matches one of `labels`. Handles every common label/value
    layout: <dt>/<dd>, <th>/<td>, <strong>Label</strong> + following text,
    label-span/value-span, header/paragraph stack, etc.

    Skips matches inside form-like elements so dropdown option lists don't get
    misread as the job's value (e.g. an "Industries" filter dropdown will list
    every industry — that is NOT the job's industry).
    """
    targets = {_label_key(l) for l in labels}

    for el in soup.find_all(string=True):
        if not isinstance(el, NavigableString):
            continue
        if _in_skip_zone(el):
            continue
        key = _label_key(str(el))
        if key not in targets:
            continue

        # Strategy 1: direct dt/dd or th/td sibling
        parent = el.parent
        if parent and parent.name in {"dt", "th", "strong", "b", "span", "div", "p", "h2", "h3", "h4", "h5", "label"}:
            sib = parent.find_next_sibling(["dd", "td", "span", "div", "p"])
            if sib and not _in_skip_zone(sib):
                t = _text(sib)
                if t and _label_key(t) not in targets:
                    return t

        # Strategy 2: next text node in document order, skipping our own label,
        # script/style, anything inside a skip-zone, and pure-label text.
        for nxt in el.find_all_next(string=True):
            if nxt is el:
                continue
            if _in_skip_zone(nxt):
                continue
            t = _norm(str(nxt))
            if not t:
                continue
            if _label_key(t) in targets:
                continue
            return t

    return None


def collect_list_after_label(soup: BeautifulSoup, labels: list[str]) -> list[str]:
    """
    Find a heading/label like 'Requirements' and collect bullet items from the
    next <ul>/<ol>. Falls back to any sibling list within the same section.
    """
    targets = {_label_key(l) for l in labels}
    for el in soup.find_all(string=True):
        if _label_key(str(el)) in targets:
            container = el.parent
            # Walk forward looking for a list
            for cand in (container.find_all_next(["ul", "ol"]) if container else []):
                items = [_text(li) for li in cand.find_all("li", recursive=False)]
                items = [i for i in items if i]
                if items:
                    return items
            break
    return []


# ---------------------------------------------------------------------------
# Listing page
# ---------------------------------------------------------------------------

def discover_job_urls(html: str) -> list[str]:
    """Return absolute, canonical (query-stripped) detail URLs from the listing."""
    soup = BeautifulSoup(html, "lxml")
    found: dict[str, None] = {}
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if JOB_URL_RE.search(href):
            absolute = urljoin(BASE, href)
            parsed = urlparse(absolute)
            canonical = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            found.setdefault(canonical, None)
    return list(found.keys())


def iter_listing_pages(fetch: Fetcher, max_pages: int) -> Iterator[tuple[int, str]]:
    for page in range(1, max_pages + 1):
        html = None
        for template in LISTING_URLS:
            url = template.format(page=page)
            log.info("listing: %s", url)
            html = fetch.get(url)
            if html and JOB_URL_RE.search(html):
                break
        if not html:
            log.warning("page %d: no html, stopping", page)
            return
        yield page, html


# ---------------------------------------------------------------------------
# Field extractors
# ---------------------------------------------------------------------------

def parse_source_job_id(url: str) -> Optional[str]:
    m = JOB_ID_RE.search(url)
    return m.group(1) if m else None


COMPANY_JP_RE = re.compile(r"^(.*?)\s*\(([^)]*[一-龯ぁ-んァ-ヶー][^)]*)\)\s*$")


def split_company_name(raw: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    """
    Split 'Cosmo Co., Ltd. (株式会社コスモ)' -> ('Cosmo Co., Ltd.', '株式会社コスモ').
    Returns (en, jp). If no Japanese-in-parens block, jp is None.
    """
    if not raw:
        return (None, None)
    raw = raw.strip()
    m = COMPANY_JP_RE.match(raw)
    if m:
        return (m.group(1).strip(), m.group(2).strip())
    return (raw, None)


SALARY_PERIOD_RE = re.compile(
    r"/\s*(Lesson|Hour|Day|Week|Month|Year|Project|hour|year|month|day|week|lesson)\b"
)


def parse_salary_period(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    m = SALARY_PERIOD_RE.search(raw)
    return m.group(1).capitalize() if m else None


# Language-level normalization. We keep the raw text in DB columns too, but
# normalize for filter dropdowns.
LEVEL_NORMALIZERS = [
    (r"\bn1\b|native|fluent", "Native / Fluent"),
    (r"\bn2\b|business|professional", "Business / Professional"),
    (r"\bn3\b|conversational|intermediate", "Conversational"),
    (r"\bn4\b|basic|beginner", "Basic / Beginner"),
    (r"\bn5\b", "N5"),
    (r"not\s+required|none\s+required|no\s+japanese|no\s+english", "Not Required"),
]


def normalize_level(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    s = raw.lower()
    for pattern, label in LEVEL_NORMALIZERS:
        if re.search(pattern, s):
            return label
    return raw.strip()


# "English: Fluent" / "Japanese: Business level" / "German: Native level"
REQUIREMENT_LANG_RE = re.compile(
    r"^\s*([A-Za-z][A-Za-z /-]*?)\s*[:：]\s*(.+?)\s*$"
)


def parse_requirements(items: list[str]) -> dict:
    """
    From a list like ['German: Native level', 'Japanese: Basic',
    'Must currently reside in Japan', 'Experience teaching German...']
    return english_level, japanese_level, other_language.
    """
    out = {"english_level": None, "japanese_level": None, "other_language": None}
    others: list[str] = []
    for item in items:
        m = REQUIREMENT_LANG_RE.match(item)
        if not m:
            continue
        lang, level = m.group(1).strip().lower(), m.group(2).strip()
        if lang == "english":
            out["english_level"] = level
        elif lang == "japanese":
            out["japanese_level"] = level
        elif lang in {"chinese", "korean", "french", "german", "spanish",
                      "portuguese", "italian", "russian", "vietnamese",
                      "thai", "indonesian", "tagalog", "arabic", "hindi"}:
            others.append(f"{m.group(1).strip()}: {level}")
    if others:
        out["other_language"] = "; ".join(others)
    return out


WORK_TYPE_TERMS = {
    "full time": "Full-time", "full-time": "Full-time",
    "part time": "Part-time", "part-time": "Part-time",
    "contract": "Contract", "temporary": "Temporary",
    "internship": "Internship", "freelance": "Freelance",
}


def parse_work_type(raw: Optional[str]) -> tuple[Optional[str], Optional[str], Optional[str]]:
    """
    GaijinPot's "Work Type" looks like 'Part Time / Experienced (Non-Manager)'.
    Return (work_type_raw, employment_terms, career_level).
    """
    if not raw:
        return (None, None, None)
    raw_lower = raw.lower()
    terms = next(
        (canonical for needle, canonical in WORK_TYPE_TERMS.items() if needle in raw_lower),
        None,
    )
    # career_level is everything after the first "/" if present
    career = None
    if "/" in raw:
        career = raw.split("/", 1)[1].strip()
    return (raw.strip(), terms, career)


def parse_post_date(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    raw = raw.strip()
    m = re.search(r"(\d+)\s+day", raw, re.IGNORECASE)
    if m:
        d = datetime.now(timezone.utc) - timedelta(days=int(m.group(1)))
        return d.date().isoformat()
    if "today" in raw.lower():
        return datetime.now(timezone.utc).date().isoformat()
    if "yesterday" in raw.lower():
        return (datetime.now(timezone.utc) - timedelta(days=1)).date().isoformat()
    try:
        return dateparser.parse(raw, fuzzy=True).date().isoformat()
    except (ValueError, OverflowError):
        return raw


# ---------------------------------------------------------------------------
# Detail page parser
# ---------------------------------------------------------------------------

def parse_job_detail(url: str, html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    body_text_lower = soup.get_text(" ", strip=True).lower()

    title = _first_text(soup, [
        "h1[itemprop='title']", "h1.job-title", "h1.entry-title",
        "h1.title", "article h1", "main h1", "h1",
    ])

    company_raw = (
        _first_text(soup, [
            "[itemprop='hiringOrganization']",
            ".company-name", ".company", ".employer-name",
            "a[href*='/company/']",
        ])
        or find_value_after_label(soup, ["Company", "Employer", "Company Name"])
    )
    company_en, company_jp = split_company_name(company_raw)

    source_job_id = (
        find_value_after_label(soup, ["Job ID", "Job Number", "Job Reference"])
        or parse_source_job_id(url)
    )

    location = (
        _first_text(soup, ["[itemprop='jobLocation']", ".job-location", ".location"])
        or find_value_after_label(soup, ["Location", "Work Location", "Office Location"])
    )

    post_raw = find_value_after_label(soup, ["Post date", "Posted", "Date Posted"])
    post_date = parse_post_date(post_raw)

    last_modified_raw = find_value_after_label(
        soup, ["Last modified", "Last modified on", "Updated", "Updated on"]
    )
    last_modified_date = parse_post_date(last_modified_raw)

    industries = find_value_after_label(soup, ["Industries", "Industry"])
    function = find_value_after_label(soup, ["Function", "Job Function"])

    work_type_raw = find_value_after_label(soup, ["Work Type", "Job Type", "Employment Type"])
    work_type, employment_terms, career_level = parse_work_type(work_type_raw)

    employer_type = find_value_after_label(soup, ["Employer Type"])

    salary_raw = (
        _first_text(soup, ["[itemprop='baseSalary']", ".salary", ".job-salary"])
        or find_value_after_label(soup, ["Salary", "Compensation", "Pay"])
    )
    salary_period = parse_salary_period(salary_raw) or salary_parser.parse_period(salary_raw or "")
    salary_min_jpy, salary_max_jpy = salary_parser.parse_range(salary_raw)
    salary_min_annual_jpy = salary_parser.annualize(salary_min_jpy, salary_period)
    salary_max_annual_jpy = salary_parser.annualize(salary_max_jpy, salary_period)

    # Salary perks: list items that often follow the salary line.
    salary_perk_items = collect_list_after_label(soup, ["Salary"])
    salary_perks = "; ".join(salary_perk_items) if salary_perk_items else None

    # Requirements: bullet list under "Requirements" heading.
    req_items = collect_list_after_label(soup, ["Requirements", "Requirement"])
    requirements = "\n".join(req_items) if req_items else None
    lang_levels = parse_requirements(req_items)

    # Fallbacks: explicit labels for English/Japanese proficiency.
    # NB: don't include the bare "Japanese"/"English" labels — they're ambiguous
    # and match the filter form's option-group labels.
    english_raw = lang_levels["english_level"] or find_value_after_label(
        soup, ["English Level", "English Proficiency", "English Ability"]
    )
    japanese_raw = lang_levels["japanese_level"] or find_value_after_label(
        soup, ["Japanese Level", "Japanese Proficiency", "Japanese Ability"]
    )
    other_language = lang_levels["other_language"]
    # Only fall back to a labeled "Other Language" field if the requirements
    # block didn't already give us one — and even then, the value must not be
    # the giant language-options list from a filter dropdown.
    if not other_language:
        candidate = find_value_after_label(soup, ["Other Language Requirement"])
        if candidate and len(candidate) < 200:
            other_language = candidate

    english_level = normalize_level(english_raw)
    japanese_level = normalize_level(japanese_raw)

    # Description body
    description_node = (
        soup.select_one("[itemprop='description']")
        or soup.select_one(".job-description")
        or soup.select_one(".description")
    )
    if not description_node:
        # Find a heading whose text contains 'Description' and use its parent block.
        for el in soup.find_all(string=True):
            if "description" in _label_key(str(el)):
                description_node = el.parent.parent if el.parent else None
                break
    description = _text(description_node) if description_node else ""
    # Strip the leading "Description" label if it's at the start
    description = re.sub(r"^\s*description\s*", "", description, flags=re.IGNORECASE)
    if len(description) > 20_000:
        description = description[:20_000] + " ..."

    # Tags / categories
    tag_set: list[str] = []
    for sel in [".tags a", ".job-tags a", ".categories a", "a[rel='tag']"]:
        for a in soup.select(sel):
            t = _text(a)
            if t:
                tag_set.append(t)
    tags_str = ", ".join(dict.fromkeys(tag_set)) if tag_set else None

    # Flags. The detail page embeds the job's true values as hidden form
    # inputs (name="remote_work_ok" / "overseas_application"). Use those —
    # never text presence across the whole page: the search-filter widget
    # prints "Remote Work OK" / "Overseas Application OK" as checkbox labels
    # on EVERY page, which used to mark all GaijinPot jobs remote+overseas.
    def _hidden_flag(*names: str) -> Optional[int]:
        for n in names:
            inp = soup.find("input", attrs={"name": n})
            if inp is not None and inp.get("value") in ("0", "1"):
                return int(inp["value"])   # authoritative 0/1 from the page
        return None

    job_text_lower = " ".join(filter(None, [
        description, requirements, salary_perks, tags_str,
    ])).lower()

    remote_work_ok = _hidden_flag("remote_work_ok")
    remote_source = "explicit" if remote_work_ok is not None else None
    if remote_work_ok is None:
        remote_work_ok = inference.infer_remote(job_text_lower)
        remote_source = "inferred" if remote_work_ok is not None else None
    overseas_application_ok = _hidden_flag("overseas_application", "overseas_application_ok")
    abroad_source = "explicit" if overseas_application_ok is not None else None
    if overseas_application_ok is None and (
        "overseas application ok" in job_text_lower
        or "applications from overseas" in job_text_lower
    ):
        overseas_application_ok = 1
        abroad_source = "inferred"
    has_video_presentation = int(
        "watch video presentation" in job_text_lower or "video presentation" in job_text_lower
    ) or None

    # Company sidebar
    company_year_founded = find_value_after_label(soup, ["Year Founded"])
    company_size = find_value_after_label(soup, ["Number of Employees", "Company Size", "Employees"])
    company_about = find_value_after_label(soup, ["About"])

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    return {
        "source": SOURCE_NAME,
        "source_job_id": source_job_id,
        "url": url,
        "title": title,
        "company_name": company_en,
        "company_name_jp": company_jp,
        "location": location,
        "industries": industries,
        "function": function,
        "work_type": work_type,
        "career_level": career_level,
        "employment_terms": employment_terms,
        "employer_type": employer_type,
        "salary": salary_raw,
        "salary_period": salary_period,
        "salary_perks": salary_perks,
        "salary_min_jpy": salary_min_jpy,
        "salary_max_jpy": salary_max_jpy,
        "salary_min_annual_jpy": salary_min_annual_jpy,
        "salary_max_annual_jpy": salary_max_annual_jpy,
        "english_level": english_level,
        "japanese_level": japanese_level,
        "other_language": other_language,
        "remote_work_ok": remote_work_ok,
        "remote_source": remote_source,
        "overseas_application_ok": overseas_application_ok,
        "abroad_source": abroad_source,
        "has_video_presentation": has_video_presentation,
        "requirements": requirements,
        "description": description,
        "tags": tags_str,
        "post_date": post_date,
        "last_modified_date": last_modified_date,
        "company_year_founded": company_year_founded,
        "company_size": company_size,
        "company_about": company_about,
        "scraped_at": now,
        "last_seen_at": now,
    }


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def run(pages: int, delay: float, debug: bool, dry_run: bool, limit: Optional[int]) -> dict:
    db.init_db()
    fetch = Fetcher(delay=delay)
    if debug:
        DEBUG_DIR.mkdir(exist_ok=True)

    all_urls: list[str] = []
    for page, html in iter_listing_pages(fetch, max_pages=pages):
        if debug:
            (DEBUG_DIR / f"listing_p{page}.html").write_text(html, encoding="utf-8")
        urls = discover_job_urls(html)
        log.info("page %d: discovered %d job urls", page, len(urls))
        all_urls.extend(urls)

    seen = set()
    job_urls = []
    for u in all_urls:
        if u not in seen:
            seen.add(u)
            job_urls.append(u)
    if limit:
        job_urls = job_urls[:limit]
    log.info("total unique job urls: %d", len(job_urls))

    stats = {"inserted": 0, "updated": 0, "failed": 0, "skipped": 0}

    with db.connect() as conn:
        for i, url in enumerate(job_urls, 1):
            html = fetch.get(url)
            if not html:
                stats["failed"] += 1
                continue
            if debug and i <= 3:
                slug = re.sub(r"[^a-z0-9]+", "_", url.lower())[-60:]
                (DEBUG_DIR / f"job_{slug}.html").write_text(html, encoding="utf-8")
            try:
                job = parse_job_detail(url, html)
            except Exception as e:
                log.exception("parse failed for %s: %s", url, e)
                stats["failed"] += 1
                continue
            if not job.get("title"):
                log.warning("no title parsed: %s", url)
                stats["skipped"] += 1
                continue
            if dry_run:
                log.info("[dry-run] %s | %s | %s",
                         job.get("title"), job.get("company_name"), job.get("location"))
                continue
            result = db.upsert_job(conn, job)
            stats[result] += 1
            log.info("[%d/%d] %s: %s", i, len(job_urls), result, job["title"])

    return stats


def main() -> int:
    p = argparse.ArgumentParser(description="Scrape GaijinPot job listings into SQLite.")
    p.add_argument("--pages", type=int, default=2)
    p.add_argument("--delay", type=float, default=1.5)
    p.add_argument("--limit", type=int, default=None)
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
        pages=args.pages, delay=args.delay,
        debug=args.debug, dry_run=args.dry_run, limit=args.limit,
    )
    log.info("done: %s", stats)
    return 0 if stats["inserted"] + stats["updated"] > 0 or args.dry_run else 1


if __name__ == "__main__":
    sys.exit(main())
