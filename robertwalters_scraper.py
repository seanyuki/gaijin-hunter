"""
Robert Walters Japan scraper (sitemap + server-rendered detail pages).

Why this approach:
  - The search RESULTS page (jobs.html?...&language1=...) is JavaScript-rendered
    AND protected by PerimeterX bot detection (px-captcha). We do NOT attempt to
    bypass that. So the `language1=` Primary Language facet is unavailable to us.
  - The job SITEMAP (advert_links.xml) and the individual DETAIL pages ARE public
    and server-rendered, so we use those.

Because the detail page does NOT contain a "Primary Language" field, we CANNOT
claim a job is exactly "English - Native" or "English - Business Level". Instead
we do a conservative, clearly-labeled language INFERENCE from the English detail
page text and mark english_level as "Unknown / inferred" unless the page itself
states native/business English. Every Robert Walters row is labeled honestly as
inferred, not as an exact Primary Language filter match.

Pipeline:
  1. Read advert_links.xml for the full list of job detail URLs (+ lastmod).
  2. Fetch each English detail page (/en/...) with plain requests.
  3. Parse: title, salary, location, date posted, industry, specialism/focus,
     workplace type, experience level, description, consultant.
  4. Classify each job:
        excluded   -> Japanese native/fluent required AND no English signal
        inferred   -> English/bilingual/global/international signal present
        unclear    -> no clear language signal either way
     Only `inferred` jobs are ingested by default (use --include-unclear to add
     the unclear ones; excluded jobs are never ingested).

Usage:
    python robertwalters_scraper.py --dry-run -v     # classify + print buckets, no writes
    python robertwalters_scraper.py                  # ingest inferred English-friendly jobs
    python robertwalters_scraper.py --include-unclear   # also ingest language-unclear jobs
    python robertwalters_scraper.py --limit 50          # cap detail pages (testing)

Optional diagnostic only (NOT the scraper path; requires Playwright + a browser,
and will be blocked by px-captcha on this site — kept only to inspect rendering):
    python robertwalters_scraper.py --probe -v
"""

from __future__ import annotations

import argparse
import html
import logging
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

try:
    from dateutil import parser as dateparser
except ImportError:
    dateparser = None

import db
import salary_parser

SOURCE_NAME = "robertwalters"
SOURCE_LABEL = "Robert Walters"
BASE = "https://www.robertwalters.co.jp"
SITEMAP_URL = "https://www.robertwalters.co.jp/advert_links.xml"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.robertwalters.co.jp/en/jobs.html",
}

DEBUG_DIR = Path(__file__).parent / "debug"
log = logging.getLogger("robertwalters")

# Detail-page "About the job" labels (confirmed against the live English page:
# Contract Type / Specialism / Focus / Industry / Salary / Workplace Type /
# Experience Level / Location / Job Reference / Date posted / Consultant).
DETAIL_LABELS = [
    "Contract Type", "Specialism", "Specialization", "Focus", "Industry",
    "Salary", "Workplace Type", "Work Arrangement", "Experience Level",
    "Location", "Job Reference", "Reference", "Date posted", "Posted",
    "Consultant",
]
_LABEL_ALT = "|".join(re.escape(l) for l in DETAIL_LABELS)

# ---- Language-inference signal vocabularies (conservative) ----
_ENGLISH_SIGNALS = [
    "native english", "business english", "fluent english", "english native",
    "english (native", "english - native", "english speaking", "english-speaking",
    "bilingual", "english and japanese", "japanese and english",
    "global", "international", "english language", "in english",
    "english communication", "english proficiency", "english is required",
    "english required", "conversational english",
]
_NATIVE_ENGLISH_SIGNALS = [
    "native english", "native-level english", "native level english",
    "english native", "english - native", "english (native",
]
_BUSINESS_ENGLISH_SIGNALS = [
    "business english", "business-level english", "business level english",
    "professional english", "business english required",
]
# Japanese-heavy: native/fluent Japanese demanded.
_JAPANESE_REQUIRED_SIGNALS = [
    "native japanese", "native-level japanese", "native level japanese",
    "japanese native", "fluent japanese", "fluent in japanese",
    "japanese fluency", "business japanese required", "jlpt n1", "jlpt n2",
    "n1 level", "n1 required", "ネイティブ", "日本語",
]


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def _norm(s: Optional[str]) -> str:
    return re.sub(r"\s+", " ", (s or "").strip()).lower().replace("–", "-")


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update(HEADERS)
    return s


def _en_url(url: str) -> str:
    """English-locale variant of a job URL (path prefixed with /en/)."""
    if "/en/" in url:
        return url
    if url.startswith(BASE + "/"):
        return BASE + "/en/" + url[len(BASE) + 1:]
    if url.startswith("/"):
        return BASE + "/en" + url
    return url


def _canonical(url: str) -> str:
    """Strip /en/ + query/fragment so a job dedupes to one stable key."""
    u = url.split("#", 1)[0].split("?", 1)[0]
    u = u.replace(BASE + "/en/", BASE + "/")
    return u


_MILLIONS_RE = re.compile(r"¥?\s*([\d]+(?:\.\d+)?)\s*m", re.IGNORECASE)


def _parse_rw_salary(raw: Optional[str]):
    """RW salary is annual, in millions of yen. Returns (clean, min, max)."""
    if not raw or not raw.strip():
        return None, None, None
    clean = raw.strip()
    if _norm(clean) in ("negotiable", "competitive",
                        "negotiable, based on experience"):
        return clean, None, None
    nums = [int(round(float(m) * 1_000_000)) for m in _MILLIONS_RE.findall(clean)]
    if nums:
        mn = nums[0]
        mx = nums[1] if len(nums) > 1 else None
        if mx is not None and mx < mn:
            mn, mx = mx, mn
        return clean, mn, mx
    try:
        smin, smax = salary_parser.parse_range(clean)
        period = salary_parser.parse_period(clean)
        mn = salary_parser.annualize(smin, period) if smin else None
        mx = salary_parser.annualize(smax, period) if smax else None
        return clean, mn, mx
    except Exception:
        return clean, None, None


def _employment_terms(contract: Optional[str]) -> Optional[str]:
    c = _norm(contract)
    if not c:
        return None
    if "perm" in c or "full" in c:
        return "Full-time"
    if "contract" in c or "temp" in c or "interim" in c or "fixed" in c:
        return "Contract"
    if "part" in c:
        return "Part-time"
    return contract


def _field(flat: str, label: str) -> Optional[str]:
    """Pull a labeled field's value, stopping at the next known label or EOL."""
    pat = rf"{re.escape(label)}\s*:?\s*(.+?)\s*(?:(?:{_LABEL_ALT})\s*:|$)"
    m = re.search(pat, flat)
    if not m:
        return None
    return (m.group(1).strip(" :　-")) or None


def _posted_iso(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    raw = raw.strip()
    if dateparser:
        try:
            return dateparser.parse(raw).date().isoformat()
        except (ValueError, TypeError, OverflowError):
            pass
    m = re.match(r"(\d{4}-\d{2}-\d{2})", raw)
    return m.group(1) if m else raw[:40]


def _clean_description(soup: BeautifulSoup) -> str:
    text = html.unescape(soup.get_text("\n"))
    m = re.search(r"About the Role", text)
    body = text[m.start():] if m else text
    for stop in ("How to Apply", "Apply now", "About the job", "Similar jobs",
                 "Save job", "Share", "© 20"):
        i = body.find(stop)
        if i > 200:
            body = body[:i]
            break
    return re.sub(r"\n{3,}", "\n\n", body).strip()[:20000]


# ---------------------------------------------------------------------------
# Language inference  (conservative, honest)
# ---------------------------------------------------------------------------

def classify_language(text: str) -> dict:
    """
    Conservative language inference from detail-page text.

    Returns:
      {
        "bucket": "inferred" | "excluded" | "unclear",
        "english_level": "Native / Fluent" | "Business / Professional"
                         | "Unknown / inferred",
        "tags": [ ... human-readable language tags ... ],
      }

    Rules (per spec):
      - Japanese native/fluent required AND no English signal -> excluded.
      - Any English / bilingual / global / international signal -> inferred
        (english-friendly).
      - Otherwise -> unclear.
      - english_level stays "Unknown / inferred" UNLESS the page clearly states
        native or business English.
    """
    t = _norm(text)
    has_english = any(sig in t for sig in _ENGLISH_SIGNALS)
    has_native_en = any(sig in t for sig in _NATIVE_ENGLISH_SIGNALS)
    has_business_en = any(sig in t for sig in _BUSINESS_ENGLISH_SIGNALS)
    has_jp_required = any(sig in t for sig in _JAPANESE_REQUIRED_SIGNALS)

    tags: list[str] = []
    if "bilingual" in t:
        tags.append("Bilingual")
    if has_english:
        tags.append("English mentioned")

    # Exclusion: Japanese native/fluent demanded and nothing English.
    if has_jp_required and not has_english:
        tags.append("Japanese-heavy (excluded)")
        return {"bucket": "excluded",
                "english_level": "Unknown / inferred",
                "tags": tags}

    if has_english:
        if has_native_en:
            level = "Native / Fluent"
        elif has_business_en:
            level = "Business / Professional"
        else:
            level = "Unknown / inferred"
        return {"bucket": "inferred", "english_level": level, "tags": tags}

    # No clear signal either way.
    tags.append("Language unclear")
    return {"bucket": "unclear",
            "english_level": "Unknown / inferred",
            "tags": tags}


# ---------------------------------------------------------------------------
# Sitemap enumeration + detail parse
# ---------------------------------------------------------------------------

def urls_from_sitemap(session: requests.Session) -> "list[tuple[str, Optional[str]]]":
    """Return (url, lastmod) for every job in advert_links.xml."""
    log.info("GET %s", SITEMAP_URL)
    try:
        r = session.get(SITEMAP_URL, timeout=30)
        r.raise_for_status()
    except requests.RequestException as e:
        log.error("sitemap fetch failed: %s", e)
        return []
    pairs: list[tuple[str, Optional[str]]] = []
    for m in re.finditer(r"<url>(.*?)</url>", r.text, re.S):
        block = m.group(1)
        loc = re.search(r"<loc>(.*?)</loc>", block)
        if not loc:
            continue
        url = html.unescape(loc.group(1).strip())
        lm = re.search(r"<lastmod>(.*?)</lastmod>", block)
        pairs.append((url, lm.group(1).strip() if lm else None))
    log.info("sitemap: %d job URLs", len(pairs))
    return pairs


def parse_detail(session: requests.Session, job_url: str,
                 lastmod: Optional[str] = None,
                 debug: bool = False) -> Optional[dict]:
    """Fetch the English detail page and parse fields + run language inference."""
    en = _en_url(job_url)
    log.info("GET %s", en)
    try:
        r = session.get(en, timeout=30)
    except requests.RequestException as e:
        log.warning("  detail fetch failed: %s", e)
        return None
    if r.status_code != 200:
        log.warning("  detail non-200 (%s)", r.status_code)
        return None
    htmltext = r.text

    if debug:
        DEBUG_DIR.mkdir(exist_ok=True)
        ref = re.search(r"/(\d{5,})-", job_url)
        name = (ref.group(1) if ref else str(abs(hash(job_url)))) + ".html"
        (DEBUG_DIR / f"rw_detail_{name}").write_text(htmltext[:200000])

    soup = BeautifulSoup(htmltext, "html.parser")
    flat = re.sub(r"[ \t]+", " ", soup.get_text(" "))

    # px-captcha / access-denied guard: skip cleanly, never try to evade.
    low = flat.lower()
    if "access to this page has been denied" in low or "px-captcha" in low:
        log.warning("  detail page blocked by bot protection — skipping")
        return None

    h1 = soup.find("h1")
    title = h1.get_text(" ", strip=True) if h1 else None
    if not title:
        t = soup.find("title")
        title = t.get_text(strip=True) if t else None
    if not title or _norm(title) == "access to this page has been denied":
        return None

    salary_clean, smin, smax = _parse_rw_salary(_field(flat, "Salary"))
    reference = _field(flat, "Job Reference") or _field(flat, "Reference")
    if reference:
        reference = re.sub(r"\D", "", reference) or None
    description = _clean_description(soup)

    lang = classify_language(f"{title}\n{description}")

    return {
        "url": _canonical(job_url),
        "title": title.strip(),
        "salary": salary_clean,
        "salary_min_annual_jpy": smin,
        "salary_max_annual_jpy": smax,
        "location": _field(flat, "Location"),
        "industries": _field(flat, "Industry"),
        "function": (_field(flat, "Specialism") or _field(flat, "Specialization")),
        "focus": _field(flat, "Focus"),
        "workplace_type": (_field(flat, "Workplace Type")
                           or _field(flat, "Work Arrangement")),
        "experience_level": _field(flat, "Experience Level"),
        "employment_terms": _employment_terms(_field(flat, "Contract Type")),
        "consultant": _field(flat, "Consultant"),
        "source_job_id": reference,
        "posted_date": _posted_iso(_field(flat, "Date posted")
                                   or _field(flat, "Posted") or lastmod),
        "description": description,
        # inference outputs
        "bucket": lang["bucket"],
        "english_level": lang["english_level"],
        "language_tags": lang["tags"],
    }


def _to_job_dict(detail: dict) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    # Honest tags: language inference + (focus/workplace/experience context).
    tag_bits = list(detail.get("language_tags") or [])
    tag_bits.append("Language: inferred (not exact RW Primary Language)")
    if detail.get("focus"):
        tag_bits.append(f"Focus: {detail['focus']}")
    if detail.get("workplace_type"):
        tag_bits.append(detail["workplace_type"])
    if detail.get("experience_level"):
        tag_bits.append(detail["experience_level"])

    wt = _norm(detail.get("workplace_type"))
    remote = 1 if ("remote" in wt or "hybrid" in wt) else None

    return {
        "source": SOURCE_NAME,
        "source_job_id": detail.get("source_job_id"),
        "url": detail["url"],
        "title": detail["title"],
        "company_name": None,            # RW client companies are confidential
        "location": detail.get("location"),
        "industries": detail.get("industries"),
        "function": detail.get("function"),
        "career_level": detail.get("experience_level"),
        "employment_terms": detail.get("employment_terms"),
        "salary": detail.get("salary"),
        "salary_min_annual_jpy": detail.get("salary_min_annual_jpy"),
        "salary_max_annual_jpy": detail.get("salary_max_annual_jpy"),
        "english_level": detail.get("english_level"),   # "Unknown / inferred" unless clear
        "remote_work_ok": remote,
        "description": detail.get("description"),
        "tags": " · ".join(tag_bits),
        "application_url": _en_url(detail["url"]),
        "post_date": detail.get("posted_date"),
        "scraped_at": now,
        "last_seen_at": now,
    }


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def collect(session: requests.Session, delay: float, limit: Optional[int],
            debug: bool) -> "dict[str, list[dict]]":
    """Walk the sitemap, parse details, bucket by language inference."""
    urls = urls_from_sitemap(session)
    buckets: dict[str, list[dict]] = {"inferred": [], "unclear": [],
                                      "excluded": [], "exact": []}
    seen: set = set()
    scanned = 0
    for jp_url, lastmod in urls:
        cu = _canonical(jp_url)
        if cu in seen:
            continue
        seen.add(cu)
        if limit and scanned >= limit:
            break
        detail = parse_detail(session, jp_url, lastmod=lastmod, debug=debug)
        scanned += 1
        if not detail:
            continue
        buckets[detail["bucket"]].append(detail)
        log.info("  [%-8s] %s", detail["bucket"], detail["title"][:60])
        time.sleep(delay)
    log.info("scanned %d detail pages", scanned)
    return buckets


def run(delay: float = 0.4, dry_run: bool = False, limit: Optional[int] = None,
        include_unclear: bool = False, debug: bool = False) -> dict:
    """Programmatic entry point used by update.py. Ingests inferred
    English-friendly jobs (plus unclear ones if include_unclear=True). Never
    ingests excluded (Japanese-heavy) jobs."""
    db.init_db()
    session = _session()
    buckets = collect(session, delay=delay, limit=limit, debug=debug)

    stats = {
        "inserted": 0, "updated": 0, "skipped": 0,
        "exact_primary_language": len(buckets["exact"]),   # always 0 — see notes
        "inferred_english_friendly": len(buckets["inferred"]),
        "excluded_japanese_heavy": len(buckets["excluded"]),
        "unclear": len(buckets["unclear"]),
    }
    if dry_run:
        return stats

    to_ingest = list(buckets["inferred"])
    if include_unclear:
        to_ingest += buckets["unclear"]

    with db.connect() as conn:
        seen: set = set()
        for detail in to_ingest:
            row = _to_job_dict(detail)
            if row["url"] in seen:
                continue
            seen.add(row["url"])
            status = db.upsert_job(conn, row)
            stats[status] = stats.get(status, 0) + 1
    return stats


# ---------------------------------------------------------------------------
# Optional diagnostic only — Playwright probe (NOT the scraper path).
# This site is protected by px-captcha, so this will be blocked; kept solely to
# inspect rendering if RW ever drops bot protection. We never try to evade it.
# ---------------------------------------------------------------------------

def probe_facets(headed: bool = False) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.stderr.write(
            "\n--probe needs Playwright (diagnostic only):\n"
            "    pip install playwright\n    playwright install chromium\n\n")
        raise SystemExit(2)

    facets = {
        "English-Native": "English - Native",
        "English-Business level": "English - Business Level",
    }
    tmpl = BASE + "/en/jobs.html?specialization=jobsroot&f=0&q=&language1={f}"
    DEBUG_DIR.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed)
        page = browser.new_context(
            user_agent=HEADERS["User-Agent"], locale="en-US").new_page()
        try:
            for facet, primary in facets.items():
                url = tmpl.format(f=requests.utils.quote(facet))
                print("\n" + "=" * 72)
                print(f"PROBE {facet}  ({primary})")
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=45000)
                    page.wait_for_timeout(4000)
                except Exception as e:
                    print("  navigation failed:", e)
                    continue
                hh = page.content()
                slug = re.sub(r"[^a-z0-9]+", "-", primary.lower()).strip("-")
                (DEBUG_DIR / f"rw_probe_{slug}.html").write_text(hh[:1_000_000])
                title = page.title()
                print("  final URL:", page.url)
                print("  page title:", repr(title))
                if "denied" in title.lower() or "px-captcha" in hh.lower():
                    print("  >> Blocked by bot protection (px-captcha). "
                          "Use the default sitemap scraper instead.")
                jobs = re.findall(r'/[^\s\"\'<>]*?/jobs/[^\s\"\'<>]*?\d{5,}[^\s\"\'<>]*?\.html', hh)
                print("  /jobs/ links:", len(set(jobs)))
                for h in list(dict.fromkeys(jobs))[:10]:
                    print("     ", h)
                print("  saved ->", DEBUG_DIR / f"rw_probe_{slug}.html")
        finally:
            browser.close()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Scrape Robert Walters Japan via public sitemap + detail pages.")
    ap.add_argument("--delay", type=float, default=0.4, help="seconds between fetches")
    ap.add_argument("--limit", type=int, default=None, help="cap detail pages scanned")
    ap.add_argument("--include-unclear", action="store_true",
                    help="also ingest language-unclear jobs (default: inferred only)")
    ap.add_argument("--dry-run", action="store_true",
                    help="classify + print buckets and first 5 inferred jobs, no writes")
    ap.add_argument("--probe", action="store_true",
                    help="OPTIONAL DIAGNOSTIC ONLY: Playwright render of the search "
                         "page (blocked by px-captcha on this site). Not the scraper.")
    ap.add_argument("--headed", action="store_true", help="(probe) show the browser")
    ap.add_argument("--debug", action="store_true", help="dump fetched HTML to ./debug/")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    if args.probe:
        probe_facets(headed=args.headed)
        return 0

    session = _session()
    if args.dry_run:
        buckets = collect(session, delay=args.delay, limit=args.limit, debug=args.debug)
        inferred, unclear = buckets["inferred"], buckets["unclear"]
        excluded, exact = buckets["excluded"], buckets["exact"]
        print("\n=== DRY RUN — Robert Walters (inferred, not exact Primary Language) ===")
        print(f"  exact Primary Language matches:   {len(exact)}   "
              f"(always 0 — detail pages don't carry Primary Language)")
        print(f"  inferred English-friendly jobs:   {len(inferred)}   (would be ingested)")
        print(f"  language-unclear jobs:            {len(unclear)}   "
              f"(ingested only with --include-unclear)")
        print(f"  excluded Japanese-heavy jobs:     {len(excluded)}   (never ingested)")
        print(f"\nFirst {min(5, len(inferred))} inferred English-friendly jobs:")
        for d in inferred[:5]:
            print(f"\n• {d['title']}")
            print(f"    english_level:    {d['english_level']}")
            print(f"    language tags:    {', '.join(d['language_tags']) or '(none)'}")
            print(f"    location:         {d.get('location')}")
            print(f"    salary:           {d.get('salary')} "
                  f"({d.get('salary_min_annual_jpy')}–{d.get('salary_max_annual_jpy')})")
            print(f"    industry:         {d.get('industries')}")
            print(f"    specialism/focus: {d.get('function')} / {d.get('focus')}")
            print(f"    workplace type:   {d.get('workplace_type')}")
            print(f"    experience level: {d.get('experience_level')}")
            print(f"    date posted:      {d.get('posted_date')}")
            print(f"    consultant:       {d.get('consultant')}")
            print(f"    source:           {SOURCE_LABEL}")
            print(f"    URL:              {_en_url(d['url'])}")
        print("\nDRY RUN — nothing written to the DB.")
        return 0

    stats = run(delay=args.delay, limit=args.limit,
                include_unclear=args.include_unclear, debug=args.debug)
    log.info("Done. %s", stats)
    return 0


if __name__ == "__main__":
    sys.exit(main())
