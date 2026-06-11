"""
YOLO JAPAN (yolo-japan.com) scraper.

YOLO JAPAN is the largest foreigner-targeted job site in Japan. It carries a
lot of part-time / service / care / warehouse roles alongside some
professional ones, so we ingest broadly but CLASSIFY clearly (job category +
part-time / hourly / entry-level / foreigner-targeted flags folded into `tags`)
so these roles never silently pollute the professional experience.

Data path (robots-compliant — see robots.txt):
  * The main /recruit/job listing is client-rendered via an AJAX endpoint that
    robots.txt DISALLOWS (/recruit/job/ajax/). We do NOT touch it.
  * robots.txt ALLOWS /recruit/job/ and the per-prefecture sitemap landing
    pages (/en/sitemap/area/<id>) are fully server-rendered and list every job
    with title, company, location, posted date and a snippet.
  * Detail pages (/en/recruit/job/details/<id>) are also server-rendered and
    ALLOWED; we enrich from them (full description, explicit Japanese level,
    employment type, salary, industry, work hours, visa/foreigner signals).

No login, no captcha, no credentialed scraping, no AJAX endpoints. Polite
headers, timeouts, retry/backoff, low request rate.

Usage:
    python yolojapan_scraper.py --dry-run --limit 20 --verbose
    python yolojapan_scraper.py --dry-run --limit 20 --verbose --no-enrich
    python yolojapan_scraper.py --limit 100
"""

from __future__ import annotations

import argparse
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

SOURCE_NAME = "YOLO Japan"
BASE = "https://www.yolo-japan.com"
# These per-prefecture sitemap pages have NO working pagination: ?page=N is
# ignored (canonical strips it, content is identical). Large prefectures (Tokyo
# 746, Osaka 386) may cap the single-page list, so to guarantee completeness we
# crawl each prefecture PARTITIONED BY EMPLOYMENT TYPE. The five employment
# sub-pages sum exactly to the prefecture total (verified: Tokyo 243+239+170+73+
# 21 = 746; Okinawa 22+11+8+4 = 45), and each is smaller and robots-allowed.
AREA_EMP_URL_TMPL = "https://www.yolo-japan.com/en/sitemap/area/{area}/employment/{emp}"
AREA_URL_TMPL = "https://www.yolo-japan.com/en/sitemap/area/{area}"  # fallback / whole-area
JOB_HREF_RE = re.compile(r"/recruit/job/details/(\d+)")

# Employment buckets that partition each prefecture (slug -> normalized label).
EMPLOYMENT_BUCKETS = [
    ("fulltime", "Full-time"),
    ("parttime", "Part-time"),
    ("temporary", "Temporary"),       # 派遣社員 (dispatch)
    ("contract_employee", "Contract"),  # 契約社員
    ("subcontractor", "Contract"),    # Freelance / Outsourcing
]

# Prefecture ids ordered by job volume (so a small --limit samples the biggest,
# freshest markets first), then the remaining prefectures fill in.
_POPULOUS = [13, 27, 14, 11, 12, 23, 26, 28, 40, 22, 1, 8, 20, 47, 10, 15, 34, 21, 19, 9]
AREA_IDS = _POPULOUS + [a for a in range(1, 48) if a not in _POPULOUS]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}

log = logging.getLogger("yolojapan")


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


# --------------------------------------------------------------------------- #
# Polite fetch with retry/backoff
# --------------------------------------------------------------------------- #
def fetch(url: str, session: requests.Session, timeout: int = 30,
          retries: int = 3, backoff: float = 2.0) -> Optional[str]:
    for attempt in range(retries):
        try:
            r = session.get(url, headers=HEADERS, timeout=timeout)
        except requests.RequestException as e:
            log.debug("request error %s (attempt %d): %s", url, attempt + 1, e)
            time.sleep(backoff * (attempt + 1))
            continue
        if r.status_code == 200:
            return r.text
        if r.status_code in (429, 500, 502, 503, 504):
            log.debug("status %s for %s, backing off", r.status_code, url)
            time.sleep(backoff * (attempt + 1))
            continue
        if r.status_code in (404, 410):
            log.debug("gone (%s) %s", r.status_code, url)
            return None
        log.debug("status %s for %s", r.status_code, url)
        return None
    return None


# --------------------------------------------------------------------------- #
# Listing parse (per-prefecture sitemap landing page)
# --------------------------------------------------------------------------- #
_COMPANY_RE = re.compile(r"Company name:\s*(.+?)\s*(?:Work Location:|Posted:|$)")
_LOC_RE = re.compile(r"Work Location:\s*(.+?)\s*(?:Posted:|$)")
_POSTED_RE = re.compile(r"Posted:\s*(\d{4}-\d{2}-\d{2})")


def parse_listing(html: str) -> list[dict]:
    """Pure parser: a prefecture sitemap page -> list of raw job dicts."""
    soup = BeautifulSoup(html, "lxml")
    out: list[dict] = []
    seen: set[str] = set()

    for a in soup.find_all("a", href=True):
        m = JOB_HREF_RE.search(a["href"])
        if not m:
            continue
        job_id = m.group(1)
        if job_id in seen:
            continue
        title = _norm(a.get_text(" ", strip=True))
        if not title:
            continue
        seen.add(job_id)

        # Climb to the smallest block that still contains only this job link.
        block = a
        while block.parent is not None:
            parent = block.parent
            ids = {JOB_HREF_RE.search(x["href"]).group(1)
                   for x in parent.find_all("a", href=True)
                   if JOB_HREF_RE.search(x["href"])}
            if len(ids) > 1:
                break
            block = parent
        btext = _norm(block.get_text(" ", strip=True))

        company = ""
        cm = _COMPANY_RE.search(btext)
        if cm:
            company = _norm(cm.group(1)).split("—")[0].split("|")[0].strip()
        location = ""
        lm = _LOC_RE.search(btext)
        if lm:
            location = _norm(lm.group(1))
        posted = None
        pm = _POSTED_RE.search(btext)
        if pm:
            posted = pm.group(1)
        # Snippet: text after the posted date (or after location), capped.
        snippet = ""
        if pm:
            snippet = _norm(btext[pm.end():])
        elif lm:
            snippet = _norm(btext[lm.end():])

        out.append({
            "job_id": job_id,
            "url": urljoin(BASE, f"/en/recruit/job/details/{job_id}"),
            "title": title,
            "company": company,
            "location": location,
            "posted": posted,
            "snippet": snippet[:2000],
        })
    return out


# --------------------------------------------------------------------------- #
# Detail parse (server-rendered detail page)
# --------------------------------------------------------------------------- #
_SECTION_LABELS = ("Company's strengths", "Work contents / remarks", "Work contents",
                   "Job Description")
_JP_LEVEL_RE = re.compile(
    r"Japanese level\s*(Not Required|None required|Beginner|Conversational|Daily conversation|"
    r"Business level[^#]*?|Native[^#]*?|Fluent[^#]*?)\s*(?:##|Employment|Industry|$)", re.I)
_EMP_RE = re.compile(r"Employment type\s*(Full-time employee|Part-time|Contract employee|"
                     r"派遣社員|Temporary|Dispatch|契約社員|アルバイト)", re.I)
_MONTH_SAL_RE = re.compile(r"Monthly [Ss]alary\s*¥?\s*([\d,]+)\s*(?:[~〜～\-–]\s*¥?\s*([\d,]+))?")
_HOUR_SAL_RE = re.compile(r"Hourly wage\s*¥?\s*([\d,]+)\s*(?:[~〜～\-–]\s*¥?\s*([\d,]+))?", re.I)
_DAY_SAL_RE = re.compile(r"Daily (?:wage|salary)\s*¥?\s*([\d,]+)\s*(?:[~〜～\-–]\s*¥?\s*([\d,]+))?", re.I)
_INDUSTRY_RE = re.compile(r"Industry\s*(.+?)\s*(?:##|Salary|Japanese level|Employment|$)")


def _to_int(s: Optional[str]) -> Optional[int]:
    if not s:
        return None
    try:
        return int(str(s).replace(",", "").strip())
    except ValueError:
        return None


def _annualize(amount: Optional[int], period: str) -> Optional[int]:
    if not amount:
        return None
    return {"Hour": amount * 2080, "Day": amount * 260,
            "Month": amount * 12, "Year": amount}.get(period, amount)


def parse_detail(html: str) -> dict:
    """Pure parser: detail-page HTML -> enrichment dict."""
    soup = BeautifulSoup(html, "lxml")
    out: dict = {}
    text = soup.get_text(" ", strip=True)

    # Description: the company's-strengths + work-contents body.
    start = None
    for label in _SECTION_LABELS:
        i = text.find(label)
        if i != -1:
            start = i
            break
    if start is not None:
        end = len(text)
        for marker in ("Work environment / atmosphere", "Status [Click here",
                       "The reasons why you should apply", "Job ID"):
            j = text.find(marker, start + 20)
            if j != -1:
                end = min(end, j)
        body = _norm(text[start:end])
        if len(body) > 60:
            out["description"] = body[:20_000]

    m = _JP_LEVEL_RE.search(text)
    if m:
        out["japanese_level"] = inference.normalize_level_label(_norm(m.group(1)))
    m = _EMP_RE.search(text)
    if m:
        out["employment_terms"] = _employment_label(m.group(1))
    m = _INDUSTRY_RE.search(text)
    if m:
        out["industry"] = _norm(m.group(1))[:120]

    # Salary: prefer monthly, then hourly, then daily.
    for rx, period in ((_MONTH_SAL_RE, "Month"), (_HOUR_SAL_RE, "Hour"), (_DAY_SAL_RE, "Day")):
        m = rx.search(text)
        if m:
            lo = _to_int(m.group(1))
            hi = _to_int(m.group(2)) or lo
            if lo:
                out["salary_min_jpy"] = lo
                out["salary_max_jpy"] = hi
                out["salary_period"] = period
                break

    low = text.lower()
    # Explicit visa-help language only. "Status of residence" / "specified
    # skill" are requirement boilerplate on every YOLO page — NOT support.
    out["_visa_support"] = bool(re.search(
        r"visa support|support .{0,20}visa|visa acquisition|visa.{0,15}renew", low))
    out["_foreigner_signal"] = bool(re.search(
        r"foreign|hiring foreign|foreign staff|多国籍|use your native language|"
        r"n[1-5]\b|jlpt", low))
    return out


def _employment_label(value: str) -> Optional[str]:
    s = str(value).lower()
    if "full" in s:
        return "Full-time"
    if "part" in s or "アルバイト" in value:
        return "Part-time"
    if "intern" in s:
        return "Internship"
    if "contract" in s or "契約" in value:
        return "Contract"
    if "派遣" in value or "dispatch" in s or "temporary" in s:
        return "Temporary"
    return _norm(value) or None


# --------------------------------------------------------------------------- #
# YOLO-specific classification
# --------------------------------------------------------------------------- #
# YOLO's "Industry" metadata field is structured and reliable ("Food and
# beverage / Ramen", "Healthcare, welfare, and caregiving / Home care", …).
# Classify from it FIRST; only fall back to title keywords. Never classify
# from the long description body — benefit boilerplate ("medical insurance",
# "hospital nearby") used to mis-tag ramen shops and forklift jobs as care work.
_INDUSTRY_CATEGORY: list[tuple[str, str]] = [
    ("healthcare, welfare",          "care_work"),
    ("nursing",                      "care_work"),
    ("caregiving",                   "care_work"),
    ("medical",                      "care_work"),
    ("food and beverage",            "hospitality"),
    ("hotels and accommodations",    "hospitality"),
    ("hotel",                        "hospitality"),
    ("restaurant",                   "hospitality"),
    ("manufacturing",                "warehouse_factory"),
    ("light work, logistics",        "warehouse_factory"),
    ("logistics",                    "warehouse_factory"),
    ("warehouse",                    "warehouse_factory"),
    ("civil engineering and construction", "construction"),
    ("construction",                 "construction"),
    ("agriculture",                  "agriculture"),
    ("fishery",                      "agriculture"),
    ("retail",                       "retail"),
    ("convenience store",            "retail"),
    ("supermarket",                  "retail"),
    ("sales and service",            "service"),
    ("cleaning",                     "service"),
    ("security",                     "service"),
    ("it ",                          "tech"),
    ("information technology",       "tech"),
    ("telecommunications",           "tech"),
    ("education",                    "teaching"),
    ("school",                       "teaching"),
    ("office work",                  "professional_office"),
    ("finance",                      "professional_office"),
    ("consulting",                   "professional_office"),
]

# Title-only fallback patterns (kept tight; titles are short and literal).
_CATEGORY_RULES = [
    ("tech", r"\b(it engineer|web engineer|software|programmer|developer|infrastructure engineer|"
             r"network engineer|rpa|devops|web designer|ec site|data analysis|machine learning)\b"),
    ("teaching", r"\b(instructor|teacher|lecturer|teaching|語学|conversation instructor)\b"),
    ("care_work", r"\b(care staff|caregiv|care worker|home[- ]?help|nurse|nursing staff|dental|"
                  r"acupuncture|midwife|care manager)\b"),
    ("hospitality", r"\b(hotel|front desk|front staff|bell staff|concierge|restaurant|kitchen|hall staff|"
                    r"cook|chef|bartender|barista|patissier|dishwasher|cafe|ramen|izakaya)\b"),
    ("warehouse_factory", r"\b(manufactur|warehouse|factory|assembly|inspection|sorting|forklift|"
                          r"labor staff|picking|packing|logistic|processing|machine operator|welding|"
                          r"production|loading)\b"),
    ("construction", r"\b(construction|scaffold|carpenter|civil engineering|demolition|rebar)\b"),
    ("retail", r"\b(store staff|cashier|sales staff|stocking|convenience|retail|shop staff|counter staff)\b"),
    ("professional_office", r"\b(office work|accounting|marketing|consultant|finance|legal|translation|"
                            r"interpret|human resources|general affairs|business development|"
                            r"sales office|data entry)\b"),
    ("service", r"\b(cleaning|security guard|\bguard\b|driver|delivery|event staff|traffic control|"
                r"customer service|service staff|caddy)\b"),
]


def classify(title: str, snippet: str, industry: str, employment: Optional[str]) -> dict:
    """Industry-first, then title keywords. `snippet` is used only for the
    part-time / entry-level signals, never for the category itself."""
    category = "other"
    ind = (industry or "").lower()
    if ind:
        for prefix, cat in _INDUSTRY_CATEGORY:
            if prefix in ind:
                category = cat
                break
    if category == "other":
        t = (title or "").lower()
        for cat, pat in _CATEGORY_RULES:
            if re.search(pat, t):
                category = cat
                break
    text = f"{title} {snippet} {industry}".lower()
    emp = (employment or "").lower()
    is_part_time = "part" in emp or bool(re.search(r"\bpart[- ]?time\b|side job|アルバイト", text))
    is_temporary = "temporary" in emp or "派遣" in (employment or "")
    is_entry_level = bool(re.search(r"inexperienced|no experience|beginner|entry[- ]?level|first[- ]?time|未経験", text))
    return {
        "category": category,
        "is_part_time": is_part_time,
        "is_temporary": is_temporary,
        "is_entry_level": is_entry_level,
        "is_professional": category in ("tech", "professional_office", "teaching"),
    }


# role_family mapping for the classifications that map cleanly onto the app's taxonomy.
_ROLE_FAMILY = {
    "tech": "Software Engineering",
    "teaching": "Teaching / Education",
    "care_work": "Healthcare / Care",
    "hospitality": "Hospitality / Service",
    "service": "Hospitality / Service",
    "retail": "Retail / Sales",
    "warehouse_factory": "Logistics / Manufacturing",
    "construction": "Construction / Trades",
    "agriculture": "Agriculture / Fishery",
    "professional_office": "Office / Administration",
}


# --------------------------------------------------------------------------- #
# Normalize -> schema row
# --------------------------------------------------------------------------- #
def map_job(raw: dict) -> Optional[dict]:
    title = _norm(raw.get("title"))
    if not title or not raw.get("url"):
        return None
    location = _norm(raw.get("location")) or "Japan"
    # Skip vague postings with no useful location AND no company.
    if location in ("", "Japan") and not _norm(raw.get("company")):
        return None

    description = raw.get("description")
    snippet = raw.get("snippet") or ""
    body = description or snippet

    cls = classify(title, body, raw.get("industry") or "", raw.get("employment_terms"))

    english_level = inference.infer_en_level(body)
    english_level_source = "inferred" if english_level else None
    japanese_level = raw.get("japanese_level")
    japanese_level_source = "explicit" if japanese_level else None
    if not japanese_level:
        japanese_level = inference.infer_jp_level(body)
        japanese_level_source = "inferred" if japanese_level else None

    # Visa / overseas signals — explicit language only. "Status of residence"
    # appears on virtually every YOLO page (it's a requirements section header)
    # and means the OPPOSITE of sponsorship: you usually need a visa already.
    visa_flag = inference.infer_visa_sponsorship(body)
    visa_support = visa_flag == 1
    overseas_application_ok = None
    if re.search(
        r"appl(?:y|ication)s?\s+from\s+(?:overseas|abroad)|overseas\s+applicants?|"
        r"currently\s+(?:living|residing)\s+(?:overseas|abroad)|"
        r"recruit(?:ing|ment)?\s+from\s+(?:overseas|abroad)",
        body, re.IGNORECASE,
    ):
        overseas_application_ok = 1

    inferred_remote = inference.infer_remote(body)
    remote_work_ok = inferred_remote if inferred_remote is not None else None

    # Salary (detail-enriched: monthly/hourly/daily).
    sal_min = raw.get("salary_min_jpy")
    sal_max = raw.get("salary_max_jpy")
    period = raw.get("salary_period")
    if not sal_min:
        sal_min, sal_max = salary_parser.parse_range(body[:2000])
        period = salary_parser.parse_period(body[:2000]) or period
    salary_raw = None
    if sal_min and sal_max and sal_min != sal_max:
        unit = {"Hour": "/hr", "Month": "/mo", "Day": "/day"}.get(period, "")
        salary_raw = f"¥{sal_min:,} - ¥{sal_max:,}{unit}"
    elif sal_min:
        unit = {"Hour": "/hr", "Month": "/mo", "Day": "/day"}.get(period, "")
        salary_raw = f"¥{sal_min:,}{unit}"

    # Classification folded into tags (schema has no custom columns).
    tags = [cls["category"]]
    if cls["is_part_time"]:
        tags.append("part-time")
    if cls["is_temporary"]:
        tags.append("temporary")
    if period == "Hour":
        tags.append("hourly")
    if cls["is_entry_level"]:
        tags.append("entry-level")
    if visa_support:
        tags.append("visa-support")
    tags.append("foreigner-targeted")
    tags_str = ", ".join(dict.fromkeys(tags))

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {
        "source": SOURCE_NAME,
        "source_job_id": f"yolojapan/{raw['job_id']}",
        "url": raw["url"],
        "title": title,
        "company_name": _norm(raw.get("company")) or None,
        "company_name_jp": None,
        "location": location,
        "industries": _norm(raw.get("industry")) or _ROLE_FAMILY.get(cls["category"]),
        "function": None,
        "work_type": None,
        "career_level": None,
        "employment_terms": raw.get("employment_terms"),
        "employer_type": None,
        "is_employer_post": 0,
        "salary": salary_raw,
        "salary_period": period,
        "salary_perks": None,
        "salary_min_jpy": sal_min,
        "salary_max_jpy": sal_max,
        "salary_min_annual_jpy": _annualize(sal_min, period or "Year"),
        "salary_max_annual_jpy": _annualize(sal_max, period or "Year"),
        "english_level": english_level,
        "english_level_source": english_level_source,
        "japanese_level": japanese_level,
        "japanese_level_source": japanese_level_source,
        "other_language": None,
        "overseas_application_ok": overseas_application_ok,
        "abroad_source": "inferred" if overseas_application_ok is not None else None,
        "remote_work_ok": remote_work_ok,
        "has_video_presentation": None,
        "requirements": None,
        "description": description,
        "tags": tags_str,
        "role_family": _ROLE_FAMILY.get(cls["category"]),
        "post_date": _norm(raw.get("posted")) or None,
        "last_modified_date": None,
        "scraped_at": now,
        "last_seen_at": now,
    }


# --------------------------------------------------------------------------- #
# Runner
# --------------------------------------------------------------------------- #
def run(pages: int = 1, delay: float = 1.5, debug: bool = False,
        dry_run: bool = False, limit: Optional[int] = None,
        enrich: bool = True, enrich_delay: float = 0.8,
        areas: Optional[list] = None,
        max_pages_per_area: int = 10) -> dict:
    """Crawl YOLO jobs by (prefecture x employment-type) sub-pages.

    `max_pages_per_area` caps how many employment sub-pages we fetch per
    prefecture (there are 5; default 10 = all). `areas` limits to specific
    prefecture ids (e.g. [13] for Tokyo-only). `limit` caps total jobs globally.
    Job ids are deduped across all sub-pages.
    """
    db.init_db()
    session = requests.Session()
    stats = {"inserted": 0, "updated": 0, "failed": 0, "skipped": 0,
             "non_japan": 0, "enriched": 0, "pages": 0}

    area_ids = areas if areas is not None else AREA_IDS
    seen_ids: set[str] = set()
    total = 0
    first_request = True

    for area in area_ids:
        if limit and total >= limit:
            break
        pages_this_area = 0
        for emp_slug, emp_label in EMPLOYMENT_BUCKETS:
            if limit and total >= limit:
                break
            if pages_this_area >= max_pages_per_area:
                break
            if not first_request:
                time.sleep(delay)          # polite delay between every sub-page
            first_request = False
            pages_this_area += 1
            stats["pages"] += 1

            url = AREA_EMP_URL_TMPL.format(area=area, emp=emp_slug)
            html = fetch(url, session)
            if html is None:
                stats["failed"] += 1
                continue
            raws = parse_listing(html)
            log.info("area %s / %s: parsed %d job cards", area, emp_slug, len(raws))

            for raw in raws:
                if raw["job_id"] in seen_ids:
                    continue              # dedupe across areas/employment buckets
                if limit and total >= limit:
                    break
                seen_ids.add(raw["job_id"])
                total += 1
                # Employment type from the bucket (detail enrichment may refine it).
                raw["employment_terms"] = emp_label

                if enrich:
                    time.sleep(enrich_delay)
                    detail_html = fetch(raw["url"], session)
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
                    log.info("  [dry-run] %s | %s | %s | %s | jp=%s | emp=%s | tags=%s",
                             row["title"][:42], row["company_name"], row["location"],
                             row["salary"], row["japanese_level"], row["employment_terms"], row["tags"])
                    continue
                try:
                    with db.connect() as conn:
                        result = db.upsert_job(conn, row)
                    stats[result] += 1
                except Exception as e:
                    log.exception("upsert failed for %s: %s", row.get("url"), e)
                    stats["failed"] += 1

    stats["unique_jobs"] = len(seen_ids)
    return stats


def main() -> int:
    p = argparse.ArgumentParser(description="Scrape YOLO JAPAN (server-rendered, robots-compliant) for Japan jobs.")
    p.add_argument("--delay", type=float, default=1.5)
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--areas", type=str, default=None,
                   help="Comma-separated prefecture ids to crawl (e.g. 13 for Tokyo, 27 for Osaka).")
    p.add_argument("--max-pages-per-area", type=int, default=10,
                   help="Max employment-type sub-pages to fetch per prefecture (there are 5).")
    p.add_argument("--no-enrich", action="store_true",
                   help="Skip per-job detail fetch (faster, thinner data).")
    p.add_argument("--debug", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--verbose", "-v", action="store_true")
    args = p.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    areas = None
    if args.areas:
        areas = [int(x) for x in args.areas.split(",") if x.strip().isdigit()]
    stats = run(delay=args.delay, debug=args.debug, dry_run=args.dry_run,
                limit=args.limit, enrich=not args.no_enrich,
                areas=areas, max_pages_per_area=args.max_pages_per_area)
    log.info("done: %s", stats)
    return 0 if (stats["inserted"] + stats["updated"]) > 0 or args.dry_run else 1


if __name__ == "__main__":
    sys.exit(main())
