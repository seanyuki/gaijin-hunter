"""
JobSpy-backed source: Indeed Japan + LinkedIn Japan + Glassdoor Japan.

Wraps the public python-jobspy library (https://github.com/speedyapply/JobSpy)
which scrapes the big job boards concurrently and returns a normalized
DataFrame. We:

  1. Call jobspy.scrape_jobs() once per site (Indeed, LinkedIn, Glassdoor)
     with country_indeed='Japan' and location='Japan'. Each call returns
     up to `results_wanted` rows.
  2. Filter to Japan-located rows (LinkedIn especially returns global jobs
     even when location='Japan').
  3. Map JobSpy's schema onto our schema and upsert.

Proxy support: if proxies.txt or GAIJIN_HUNTER_PROXIES env var contains
proxies, they're passed straight through to jobspy.scrape_jobs(). LinkedIn
in particular rate-limits aggressively without proxies — JobSpy's docs say
"proxies are basically a must."

Heads-up on ToS: Indeed and LinkedIn don't permit scraping in their ToS.
This code uses JobSpy to do it on their behalf. The user (Sean) opted into
this knowingly — see the conversation that led to this file.

Usage:
    python jobspy_scraper.py [--sites indeed,linkedin] [--results 100]
                             [--hours-old 720] [--dry-run] [-v]
"""

from __future__ import annotations

import argparse
import logging
import math
import re
import sys
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

import db
import inference
import proxies as proxy_mod
import salary_parser

SOURCE_NAME = "jobspy"
log = logging.getLogger("jobspy_scraper")

# All sites JobSpy supports. Kept here for the CLI --help discoverability.
ALL_SITES = [
    "indeed", "linkedin", "glassdoor", "google",
    "zip_recruiter", "bayt", "naukri", "bdjobs",
]

# Sites we hit by default. zip_recruiter (US/Canada), bayt (Middle East),
# naukri (India), and bdjobs (Bangladesh) are intentionally excluded — they
# yield ~0 Japan rows but cost the same per API call. Glassdoor is excluded
# because JobSpy reports "Glassdoor is not available for JAPAN" (no Japan
# country support), so every call fails. Pass --sites <name> to override.
DEFAULT_SITES = ["indeed", "linkedin", "google"]

# How many raw rows we'll process per scrape_jobs() call. JobSpy paginates
# via `offset`, so each batch advances offset by this much.
BATCH_SIZE = 300

# Default upper bound on raw rows scanned per site, regardless of how many
# rows still need to clear our filters. Stops the loop from running away.
# Raised from 3000 → 5000 because we now run multiple queries per site.
DEFAULT_MAX_RAW_PER_SITE = 5000


# Broad job-category queries — each is generic enough that Indeed / LinkedIn /
# Glassdoor return a wide cross-section of Japan-located postings. The
# language-ratio filter (is_mostly_english) is what discriminates English
# postings from Japanese ones AFTER the rows come back.
#
# Picking queries this way rather than searching for the word "english"
# captures English-language postings whose body never explicitly says
# "English" (i.e. they're written in English so they don't need to).
#
# Override with --search-terms "a,b,c" or --search-term "single".
BROAD_JOB_QUERIES = [
    "engineer",     # all engineering disciplines
    "developer",    # software/web
    "manager",      # leadership / EM / PM
    "consultant",   # strategy / business
    "analyst",      # data / finance
    "designer",     # product / UX
    "specialist",   # niche / domain roles
]

# Legacy name kept so anything importing GAIJIN_FRIENDLY_QUERIES still works.
GAIJIN_FRIENDLY_QUERIES = BROAD_JOB_QUERIES

# When the language filter is enabled, this is the minimum Latin-letter ratio
# (0.0–1.0) the row's title + description must hit for the row to be accepted.
DEFAULT_ENGLISH_THRESHOLD = 0.6


# ---------------------------------------------------------------------------
# URL normalization — strip tracking params so otherwise-identical postings
# don't end up as different DB rows. Indeed in particular returns the same
# posting under "sponsored", "organic", and tagged URLs that only differ in
# tracking parameters.
# ---------------------------------------------------------------------------
_TRACKING_PARAMS = {
    # Generic referrer params
    "ref",
    # utm_* is handled separately via prefix match
    # Indeed (jk is the substantive job key — keep)
    "from", "tk", "advn", "vjs", "alid", "jsa", "rgtk", "fccid", "iaal",
    "_ga", "psc", "spa", "co",
    # LinkedIn (currentJobId is substantive — keep)
    "trk", "trkCampaign", "refId", "lipi", "lici", "midToken", "midSig",
    # Glassdoor (jl IS the job ID — keep). Tracking-only params:
    "srs", "uido", "icid", "ja",
}


def normalize_url(url: Optional[str]) -> Optional[str]:
    """Strip tracking-only query params from a job URL so the canonical
    form deduplicates cleanly. Leaves substantive params (jk, currentJobId,
    etc.) alone."""
    if not url:
        return url
    try:
        p = urlparse(url)
    except ValueError:
        return url
    kept = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
            if k not in _TRACKING_PARAMS and not k.lower().startswith("utm_")]
    return urlunparse(p._replace(query=urlencode(kept), fragment=""))


def _normalize_text(s) -> str:
    """Lower-case, collapse whitespace, treat NaN/None/empty as ''."""
    if s is None:
        return ""
    try:
        if isinstance(s, float) and math.isnan(s):
            return ""
    except (TypeError, ValueError):
        pass
    return re.sub(r"\s+", " ", str(s).strip().lower())


def _extract_search_tokens(search_term: str) -> list[str]:
    """
    Pull the significant terms out of a JobSpy / Indeed-style search query.
    Drops quote characters, parentheses, boolean operators (AND / OR), and
    excluded-term tokens (prefix `-`). Returns a list of lower-cased tokens
    that MUST appear in title or description for a row to count as a hit.

        '"english bilingual" software -junior'
            -> ['english', 'bilingual', 'software']
    """
    if not search_term:
        return []
    cleaned = re.sub(r'[\"\(\)]', ' ', search_term)
    out: list[str] = []
    for tok in cleaned.split():
        if tok.startswith("-"):
            continue           # exclude-term, skip
        upper = tok.upper()
        if upper in ("AND", "OR", "NOT"):
            continue
        out.append(tok.lower())
    return out


def _matches_search(tokens: list[str], title: Optional[str],
                    description: Optional[str]) -> bool:
    """All tokens must appear (case-insensitive substring) in title or
    description. Empty token list → True (no filter)."""
    if not tokens:
        return True
    haystack = ((title or "") + " " + (description or "")).lower()
    return all(t in haystack for t in tokens)


def _dedupe_key(row: dict, site: str) -> Optional[tuple]:
    """
    Fallback dedup key used when a canonical URL isn't available:
        (source, title, company, location)

    Returns None when there's no title — without a title we can't claim
    uniqueness, so let the row through and rely on URL dedup instead.
    """
    title = _normalize_text(row.get("title"))
    if not title:
        return None
    company = _normalize_text(row.get("company"))
    location_parts = [_normalize_text(row.get(k)) for k in ("city", "state", "country")]
    location = ",".join(p for p in location_parts if p)
    return (_normalize_text(site), title, company, location)


# ---------------------------------------------------------------------------
# Mapping from JobSpy DataFrame row to our DB row
# ---------------------------------------------------------------------------

def _empty_to_none(v):
    """JobSpy uses pandas; empty strings, NaN, and None all show up. Normalize."""
    if v is None:
        return None
    # pandas NaN
    try:
        if isinstance(v, float) and math.isnan(v):
            return None
    except (TypeError, ValueError):
        pass
    s = str(v).strip()
    if not s or s.lower() == "nan" or s.lower() == "none":
        return None
    return s


def _build_location(row: dict) -> Optional[str]:
    """JobSpy's location is split across city/state/country."""
    parts = [_empty_to_none(row.get(k)) for k in ("city", "state", "country")]
    parts = [p for p in parts if p]
    return ", ".join(parts) if parts else None


def _employment_terms(job_type: Optional[str]) -> Optional[str]:
    if not job_type:
        return None
    s = str(job_type).lower()
    if "full" in s:        return "Full-time"
    if "part" in s:        return "Part-time"
    if "contract" in s:    return "Contract"
    if "intern" in s:      return "Internship"
    if "temp" in s:        return "Temporary"
    return _empty_to_none(job_type)


def _salary_period(interval: Optional[str]) -> Optional[str]:
    if not interval:
        return None
    s = str(interval).lower()
    if "year" in s:    return "Year"
    if "month" in s:   return "Month"
    if "week" in s:    return "Week"
    if "day" in s:     return "Day"
    if "hour" in s:    return "Hour"
    return None


def _build_salary_str(lo, hi, interval, currency) -> Optional[str]:
    lo_n = _empty_to_none(lo); hi_n = _empty_to_none(hi)
    if not lo_n and not hi_n:
        return None
    cur = (_empty_to_none(currency) or "JPY").upper()
    sign = "¥" if cur == "JPY" else (cur + " ")
    try:
        if lo_n: lo_v = int(float(lo_n))
        else:    lo_v = None
        if hi_n: hi_v = int(float(hi_n))
        else:    hi_v = None
    except (TypeError, ValueError):
        return None
    parts = []
    if lo_v is not None and hi_v is not None and lo_v != hi_v:
        parts.append(f"{sign}{lo_v:,} - {sign}{hi_v:,}")
    elif lo_v is not None:
        parts.append(f"{sign}{lo_v:,}")
    elif hi_v is not None:
        parts.append(f"{sign}{hi_v:,}")
    period = _salary_period(interval)
    if period:
        parts.append(f"/ {period}")
    return " ".join(parts) if parts else None


def map_row(row: dict, strict_japan: bool = False) -> Optional[dict]:
    """
    Convert a JobSpy DataFrame row (as a dict) into our schema. Returns None
    if the row isn't Japan-relevant or lacks a title/URL.

    `strict_japan=True` requires an unambiguous Japan signal in the row's
    location/country: disables the contains_japanese() fallback (kanji is
    shared with Chinese) and disables the "jp" ISO-code short match.
    """
    title = _empty_to_none(row.get("title"))
    url = normalize_url(_empty_to_none(row.get("job_url")))
    if not title or not url:
        return None

    location = _build_location(row)
    # Filter: must be Japan-located (LinkedIn returns globals)
    country = _empty_to_none(row.get("country"))
    company = _empty_to_none(row.get("company"))

    is_japan = (inference.is_japan_location(location, strict=strict_japan) or
                inference.is_japan_location(country,  strict=strict_japan))

    # Fallback: when JobSpy gives us no location AND no country, treat the row
    # as Japan if title or company contains Hiragana/Katakana/Kanji. Disabled
    # in strict mode because Kanji is shared with Chinese.
    if (not strict_japan and not is_japan and not location and not country):
        if inference.contains_japanese(title) or inference.contains_japanese(company):
            is_japan = True
            log.debug("japan-fallback via Japanese text: title=%r  company=%r",
                      title, company)
            if not location:
                # Stamp a sentinel so the UI shows something instead of blank.
                location = "Japan (inferred)"

    if not is_japan:
        # Helpful for diagnosing why a row got dropped — run with --verbose
        # to surface these.
        log.debug("rejected non-Japan row: title=%r  company=%r  location=%r  country=%r",
                  title, company, location, country)
        return None
    description = _empty_to_none(row.get("description"))
    is_remote = row.get("is_remote")
    if isinstance(is_remote, str):
        is_remote = is_remote.strip().lower() in ("true", "yes", "1")
    remote_work_ok = 1 if is_remote else None

    body_remote = inference.infer_remote(description or "")
    if body_remote is not None:
        remote_work_ok = body_remote

    overseas_application_ok = inference.infer_visa_sponsorship(description or "")
    japanese_level = inference.infer_jp_level(description or "")
    english_level = inference.infer_en_level(description or "")

    # Salary handling: JobSpy gives min_amount/max_amount/interval/currency
    salary_raw = _build_salary_str(
        row.get("min_amount"), row.get("max_amount"),
        row.get("interval"), row.get("currency")
    )
    salary_period = _salary_period(row.get("interval"))
    salary_min_jpy = salary_max_jpy = None
    try:
        if _empty_to_none(row.get("min_amount")):
            salary_min_jpy = int(float(row["min_amount"]))
        if _empty_to_none(row.get("max_amount")):
            salary_max_jpy = int(float(row["max_amount"]))
    except (TypeError, ValueError):
        pass
    salary_min_annual_jpy = salary_parser.annualize(salary_min_jpy, salary_period or "Year")
    salary_max_annual_jpy = salary_parser.annualize(salary_max_jpy, salary_period or "Year")

    employment_terms = _employment_terms(row.get("job_type"))
    site = _empty_to_none(row.get("site")) or "jobspy"
    post_date = _empty_to_none(row.get("date_posted"))
    if post_date:
        # JobSpy returns either ISO date string or datetime — normalize to YYYY-MM-DD
        post_date = str(post_date)[:10]

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {
        "source": SOURCE_NAME,
        "source_job_id": f"{site}/{re.sub(r'[^A-Za-z0-9_-]+', '_', url)[-60:]}",
        "url": url,
        "title": title,
        "company_name": company,
        "company_name_jp": None,
        "location": location,
        "industries": _empty_to_none(row.get("company_industry")),
        "function": None,
        "work_type": None,
        "career_level": _empty_to_none(row.get("job_level")),
        "employment_terms": employment_terms,
        "employer_type": None,
        "salary": salary_raw,
        "salary_period": salary_period,
        "salary_perks": None,
        "salary_min_jpy": salary_min_jpy,
        "salary_max_jpy": salary_max_jpy,
        "salary_min_annual_jpy": salary_min_annual_jpy,
        "salary_max_annual_jpy": salary_max_annual_jpy,
        "english_level": english_level,
        "japanese_level": japanese_level,
        "other_language": None,
        "overseas_application_ok": overseas_application_ok,
        "remote_work_ok": remote_work_ok,
        "has_video_presentation": None,
        "requirements": None,
        "description": description,
        "tags": f"via {site}" if site else None,
        "post_date": post_date,
        "last_modified_date": None,
        "scraped_at": now,
        "last_seen_at": now,
    }


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def run(sites: Optional[list[str]] = None,
        results_wanted: int = 300,
        max_raw_per_site: int = DEFAULT_MAX_RAW_PER_SITE,
        hours_old: Optional[int] = 720,
        search_terms: Optional[list[str]] = None,
        search_term: Optional[str] = None,   # back-compat alias for one query
        strict_japan: bool = False,
        english_threshold: float = DEFAULT_ENGLISH_THRESHOLD,
        dry_run: bool = False, verbose: int = 1) -> dict:
    """
    Iterative deep scan per site. `results_wanted` is the TARGET number of
    *accepted* jobs per site — rows that survive every filter (Japan-located,
    not a duplicate of an earlier row, contains the keyword tokens in title
    or description). We paginate JobSpy via its `offset` parameter, requesting
    BATCH_SIZE rows at a time, and stop a site when:

        • accepted_count >= target (we got what we wanted), OR
        • raw_seen >= max_raw_per_site (caller's cap), OR
        • the batch returned no new unique rows (source exhausted).

    Defaults are tuned for the foreigner-in-Japan use case:
      • location="Japan", country_indeed="Japan"
      • search_term="english" — title or description must contain "english"
      • results_wanted=300 accepted per site
      • max_raw_per_site=3000 — fail-safe cap on scanning
      • hours_old=720 (30 days) — matches the stale-archive cutoff in the UI
    """
    db.init_db()

    try:
        from jobspy import scrape_jobs  # type: ignore
    except ImportError:
        log.error("python-jobspy is not installed. Run: "
                  "pip install python-jobspy")
        return {"inserted": 0, "updated": 0, "failed": 1, "skipped": 0,
                "non_japan": 0}

    sites = sites or DEFAULT_SITES
    proxy_list = proxy_mod.load_proxies() or None
    if proxy_list:
        log.info("using %d proxies", len(proxy_list))

    target_per_site = results_wanted
    stats = {
        "raw_seen": 0, "accepted": 0,
        "inserted": 0, "updated": 0, "failed": 0, "skipped": 0,
        "non_japan": 0, "duplicates": 0,
        "keyword_miss": 0, "language_miss": 0,
    }

    # Resolve which list of queries to run. Precedence:
    #   1. explicit search_terms list (preferred)
    #   2. legacy single search_term (back-compat)
    #   3. the curated GAIJIN_FRIENDLY_QUERIES list (default)
    if search_terms is None:
        if search_term is not None:
            queries = [search_term]
        else:
            queries = list(GAIJIN_FRIENDLY_QUERIES)
    else:
        queries = list(search_terms)
    queries = [q for q in queries if q and q.strip()]
    if not queries:
        queries = list(GAIJIN_FRIENDLY_QUERIES)

    log.info("running %d query/queries per site: %s", len(queries), queries)
    log.info("target per site: %d accepted | max raw scan: %d | strict_japan=%s | "
             "english_threshold=%.2f", target_per_site, max_raw_per_site,
             strict_japan, english_threshold)

    for site in sites:
        # Per-site counters. Accumulate into global stats at end of site.
        site_raw = 0
        site_accepted = 0
        site_inserted = 0
        site_updated = 0
        site_dupes = 0
        site_non_japan = 0
        site_keyword_miss = 0
        site_language_miss = 0
        site_failed_batches = 0

        # Per-site dedup memory. Persists ACROSS queries within this site so
        # a row that "english" returned can't be re-counted from "bilingual".
        seen_urls: set[str] = set()
        seen_keys: set[tuple] = set()

        with db.connect() as conn:
            for q_idx, query in enumerate(queries, 1):
                if site_accepted >= target_per_site:
                    break  # already at target — no need for more queries
                if site_raw >= max_raw_per_site:
                    log.info("  %s: max_raw_per_site cap hit, skipping remaining queries", site)
                    break

                strict_tokens = _extract_search_tokens(query)
                log.info("[%s] query %d/%d: %r | accepted_before=%d  raw_before=%d",
                         site, q_idx, len(queries), query, site_accepted, site_raw)

                # Per-query offset (JobSpy paginates per-query, so each
                # new query starts at offset 0).
                query_offset = 0
                query_accepted_start = site_accepted

                while site_accepted < target_per_site and site_raw < max_raw_per_site:
                    remaining_cap = max_raw_per_site - site_raw
                    batch_size = min(BATCH_SIZE, remaining_cap)
                    if batch_size <= 0:
                        break

                    kwargs = dict(
                        site_name=[site],
                        search_term=query,
                        location="Japan",
                        country_indeed="Japan",
                        results_wanted=batch_size,
                        offset=query_offset,
                        hours_old=hours_old,
                        description_format="markdown",
                        proxies=proxy_list,
                        verbose=verbose,
                    )
                    if site == "google":
                        recency = ("since last month"
                                   if (hours_old or 0) >= 168 else "since last week")
                        kwargs["google_search_term"] = f"{query} jobs in Japan {recency}"

                    log.info("  querying %s q=%r (offset=%d, batch=%d, accepted=%d/%d, raw=%d/%d)",
                             site, query, query_offset, batch_size,
                             site_accepted, target_per_site,
                             site_raw, max_raw_per_site)
                    if site == "google":
                        log.info("    google_search_term: %r", kwargs["google_search_term"])

                    try:
                        df = scrape_jobs(**kwargs)
                    except Exception as e:
                        log.exception("scrape_jobs failed for %s q=%r: %s", site, query, e)
                        site_failed_batches += 1
                        break
                    try:
                        records = (df.to_dict("records")
                                   if hasattr(df, "to_dict") else list(df))
                    except Exception as e:
                        log.exception("could not iterate jobspy result: %s", e)
                        site_failed_batches += 1
                        break

                    if not records:
                        log.info("  %s q=%r: empty batch, advancing to next query", site, query)
                        break

                    new_uniques_this_batch = 0
                    for row in records:
                        site_raw += 1
                        query_offset += 1
                        if site_raw > max_raw_per_site:
                            break

                        norm_url = normalize_url(_empty_to_none(row.get("job_url")))
                        key = _dedupe_key(row, site)

                        # Dedup BEFORE map_row, mark seen IMMEDIATELY.
                        if norm_url and norm_url in seen_urls:
                            site_dupes += 1
                            log.debug("dup (canonical URL): %s | url=%s",
                                      _empty_to_none(row.get("title")), norm_url)
                            continue
                        if key and key in seen_keys:
                            site_dupes += 1
                            log.debug("dup (key=%s): %s @ %s",
                                      key, _empty_to_none(row.get("title")),
                                      _empty_to_none(row.get("company")))
                            continue
                        if norm_url:
                            seen_urls.add(norm_url)
                        if key:
                            seen_keys.add(key)
                        new_uniques_this_batch += 1

                        mapped = map_row(row, strict_japan=strict_japan)
                        if mapped is None:
                            site_non_japan += 1
                            continue

                        if not _matches_search(strict_tokens,
                                               mapped.get("title"),
                                               mapped.get("description")):
                            site_keyword_miss += 1
                            log.debug("keyword miss: tokens=%s  title=%r",
                                      strict_tokens, mapped.get("title"))
                            continue

                        # Language filter: must be predominantly English.
                        # Combine title + description; ratio of Latin letters
                        # to (Latin + Japanese) chars must clear the threshold.
                        combined = ((mapped.get("title") or "") + "  " +
                                    (mapped.get("description") or ""))
                        if not inference.is_mostly_english(combined, english_threshold):
                            site_language_miss += 1
                            ratio = inference.english_ratio(combined)
                            log.debug("language miss (ratio=%.2f < %.2f): title=%r",
                                      ratio, english_threshold, mapped.get("title"))
                            continue

                        # Accepted.
                        site_accepted += 1
                        if dry_run:
                            log.info("    [dry-run] %s | %s | %s",
                                     mapped.get("title"), mapped.get("company_name"),
                                     mapped.get("location"))
                        else:
                            try:
                                result = db.upsert_job(conn, mapped)
                                if result == "inserted":
                                    site_inserted += 1
                                else:
                                    site_updated += 1
                            except Exception as e:
                                log.exception("upsert failed: %s", e)
                                stats["failed"] += 1

                        if site_accepted >= target_per_site:
                            break

                    log.info("    %s q=%r: batch done — accepted=%d/%d, raw=%d/%d "
                             "(this batch: %d new unique, %d dupes)",
                             site, query, site_accepted, target_per_site,
                             site_raw, max_raw_per_site,
                             new_uniques_this_batch,
                             len(records) - new_uniques_this_batch)

                    if new_uniques_this_batch == 0:
                        log.info("  %s q=%r: no new uniques, advancing to next query",
                                 site, query)
                        break

                query_accepted = site_accepted - query_accepted_start
                log.info("[%s] query %d/%d done: %r contributed %d accepted",
                         site, q_idx, len(queries), query, query_accepted)

        # Per-site summary
        log.info("[%s] done: accepted=%d/%d  raw=%d  dupes=%d  non_japan=%d  "
                 "keyword_miss=%d  language_miss=%d  inserted=%d  updated=%d  "
                 "failed_batches=%d",
                 site, site_accepted, target_per_site, site_raw, site_dupes,
                 site_non_japan, site_keyword_miss, site_language_miss,
                 site_inserted, site_updated, site_failed_batches)

        # Accumulate into global stats
        stats["raw_seen"]      += site_raw
        stats["accepted"]      += site_accepted
        stats["inserted"]      += site_inserted
        stats["updated"]       += site_updated
        stats["duplicates"]    += site_dupes
        stats["non_japan"]     += site_non_japan
        stats["keyword_miss"]  += site_keyword_miss
        stats["language_miss"] += site_language_miss
        stats["failed"]        += site_failed_batches

    # Final summary
    if stats["duplicates"]:
        log.info("dedup summary: %d duplicate rows skipped across all sites",
                 stats["duplicates"])
    if strict_tokens and stats["keyword_miss"]:
        log.info("keyword summary: %d rows dropped because they didn't contain "
                 "all of %s in title/description", stats["keyword_miss"], strict_tokens)
    return stats


def main() -> int:
    p = argparse.ArgumentParser(description="Scrape Indeed/LinkedIn/Glassdoor "
                                            "Japan jobs via JobSpy.")
    p.add_argument("--sites", type=str, default=",".join(DEFAULT_SITES),
                   help="Comma-separated site names. Supported: "
                        "indeed, linkedin, glassdoor, google, "
                        "zip_recruiter, bayt, naukri, bdjobs. "
                        "Default (deeper scan): " + ",".join(DEFAULT_SITES) +
                        " — the low-yield 4 (zip_recruiter, bayt, naukri, bdjobs) "
                        "are excluded by default. Pass --sites manually to include them.")
    p.add_argument("--results", type=int, default=300,
                   help="Target ACCEPTED jobs per site (after Japan-location, "
                        "dedup, and keyword filters). The scraper paginates "
                        "until this many accepted rows are collected, or "
                        "--max-raw-per-site is hit, whichever comes first. "
                        "Default 300.")
    p.add_argument("--max-raw-per-site", type=int, default=DEFAULT_MAX_RAW_PER_SITE,
                   help=f"Safety cap on raw rows scanned per site "
                        f"(default {DEFAULT_MAX_RAW_PER_SITE}). Prevents the "
                        "loop from running away on sites with low accept rates.")
    p.add_argument("--search-terms", type=str, default=None,
                   help="Comma-separated list of search queries to run per site. "
                        "Each query runs as its own JobSpy pass with its own strict "
                        "keyword filter; results accumulate (with dedup) across queries. "
                        "Default: curated gaijin-friendly list — " +
                        ",".join(GAIJIN_FRIENDLY_QUERIES) + ".")
    p.add_argument("--search-term", type=str, default=None,
                   help="(Back-compat) Single search keyword. Equivalent to "
                        "--search-terms with one item. If both are set, "
                        "--search-terms wins.")
    p.add_argument("--strict-japan", action="store_true",
                   help="Require an unambiguous Japan signal in the row's "
                        "location or country (e.g. 'Japan', 'Tokyo', 'Osaka'). "
                        "Disables the Kanji-fallback for rows missing location, "
                        "and disables the 'jp' ISO-code short match. "
                        "Use this if you want maximum confidence that no "
                        "non-Japan rows slip through.")
    p.add_argument("--english-threshold", type=float, default=DEFAULT_ENGLISH_THRESHOLD,
                   help=f"Min ratio of Latin letters to (Latin + Japanese) "
                        f"characters in title + description for a row to be "
                        f"accepted as an English-language posting. "
                        f"Default {DEFAULT_ENGLISH_THRESHOLD}. "
                        "Raise to 0.8+ for English-only; lower to 0.4 to "
                        "allow more bilingual postings.")
    p.add_argument("--hours-old", type=int, default=720,
                   help="Jobs posted within the last N hours (default 720 = 30 days).")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--verbose", "-v", action="store_true")
    args = p.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    sites = [s.strip() for s in args.sites.split(",") if s.strip()]
    search_terms = None
    if args.search_terms:
        search_terms = [s.strip() for s in args.search_terms.split(",") if s.strip()]
    stats = run(sites=sites, results_wanted=args.results,
                max_raw_per_site=args.max_raw_per_site,
                hours_old=args.hours_old,
                search_terms=search_terms,
                search_term=args.search_term,
                strict_japan=args.strict_japan,
                english_threshold=args.english_threshold,
                dry_run=args.dry_run, verbose=2 if args.verbose else 1)
    log.info("done: %s", stats)
    return 0 if (stats["inserted"] + stats["updated"]) > 0 or args.dry_run else 1


if __name__ == "__main__":
    sys.exit(main())
