"""
One-command refresh: run every registered source scraper in sequence.

    python update.py                       # listing pulls only (fast)
    python update.py --enrich              # also fetch detail pages where supported
    python update.py --only tokyodev      # run a single source
    python update.py --skip jobspy        # run everything except one or more sources
    python update.py --pages 3            # paginated sources: how many listing pages
    python update.py --limit 25           # bounded run: at most N jobs per source
    python update.py --dry-run            # fetch + parse but write nothing to the DB
    python update.py --backfill           # no scraping; re-run data-quality repair
                                          # (fix_data.py) over existing rows

Each source is a (name, runner) entry. A runner is a callable that returns a
stats dict {inserted, updated, ...}; we accumulate and print a summary table.
A failing source never aborts the run — it's logged, counted under `failed`,
and the next source proceeds.
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from typing import Callable


def _run_gaijinpot(pages: int, delay: float, enrich: bool,
                   dry_run: bool = False, limit=None) -> dict:
    import scraper as gp
    return gp.run(pages=pages, delay=delay, debug=False, dry_run=dry_run, limit=limit)


def _run_tokyodev(pages: int, delay: float, enrich: bool,
                  dry_run: bool = False, limit=None) -> dict:
    """
    Always enrich for TokyoDev — the listing-only data is missing fields we
    care about (English level, career level, post date, full description,
    requirements). The global `enrich` flag is ignored here.
    """
    import tokyodev_scraper as td
    return td.run(delay=delay, debug=False, dry_run=dry_run, limit=limit,
                  enrich=True, enrich_delay=delay)


def _run_jobsinjapan(pages: int, delay: float, enrich: bool,
                     dry_run: bool = False, limit=None) -> dict:
    import jobsinjapan_scraper as jij
    return jij.run(pages=pages, delay=delay, debug=False, dry_run=dry_run, limit=limit)


def _run_japandev(pages: int, delay: float, enrich: bool,
                  dry_run: bool = False, limit=None) -> dict:
    """Japan Dev: hand-curated English-friendly IT jobs in Japan. Parses the
    server-rendered /jobs listing (no anti-bot bypass)."""
    import japandev_scraper as jd
    return jd.run(pages=max(pages, 1), delay=delay, debug=False, dry_run=dry_run,
                  limit=limit, enrich=True, enrich_delay=min(delay, 0.6))


def _run_yolojapan(pages: int, delay: float, enrich: bool,
                   dry_run: bool = False, limit=None) -> dict:
    """YOLO JAPAN: foreigner-targeted board (lots of part-time/service roles,
    clearly tagged). Crawls the robots-allowed per-prefecture sitemap pages +
    server-rendered detail pages. Never touches the disallowed AJAX endpoint.
    Returns a stats dict even if zero jobs or blocked, so --all stays safe."""
    import yolojapan_scraper as yj
    return yj.run(delay=max(delay, 1.5), debug=False, dry_run=dry_run, limit=limit,
                  enrich=True, enrich_delay=min(delay, 0.8))


def _run_greenhouse(pages: int, delay: float, enrich: bool,
                    dry_run: bool = False, limit=None) -> dict:
    import greenhouse_scraper as gh
    return gh.run(delay=delay, debug=False, dry_run=dry_run, limit_per_company=limit)


def _run_lever(pages: int, delay: float, enrich: bool,
               dry_run: bool = False, limit=None) -> dict:
    import lever_scraper as lv
    return lv.run(delay=delay, debug=False, dry_run=dry_run, limit_per_company=limit)


def _run_ashby(pages: int, delay: float, enrich: bool,
               dry_run: bool = False, limit=None) -> dict:
    import ashby_scraper as ab
    return ab.run(delay=delay, debug=False, dry_run=dry_run, limit_per_company=limit)


def _run_workable(pages: int, delay: float, enrich: bool,
                  dry_run: bool = False, limit=None) -> dict:
    import workable_scraper as wk
    return wk.run(delay=delay, debug=False, dry_run=dry_run, limit_per_company=limit)


def _run_smartrecruiters(pages: int, delay: float, enrich: bool,
                         dry_run: bool = False, limit=None) -> dict:
    import smartrecruiters_scraper as sr
    return sr.run(delay=delay, debug=False, dry_run=dry_run, limit_per_company=limit)


def _run_recruitee(pages: int, delay: float, enrich: bool,
                   dry_run: bool = False, limit=None) -> dict:
    import recruitee_scraper as rc
    return rc.run(delay=delay, debug=False, dry_run=dry_run, limit_per_company=limit)


def _run_careercross(pages: int, delay: float, enrich: bool,
                     dry_run: bool = False, limit=None) -> dict:
    import careercross_scraper as cc
    return cc.run(pages=pages, delay=delay, debug=False, dry_run=dry_run, limit=limit)


def _run_robertwalters(pages: int, delay: float, enrich: bool,
                       dry_run: bool = False, limit=None) -> dict:
    """Robert Walters Japan — public sitemap + server-rendered detail pages.
    The search facet (exact Primary Language) is behind bot protection, so we
    INGEST jobs whose detail text infers an English-friendly role and EXCLUDE
    Japanese-native-required ones. Labeled honestly as inferred, not exact."""
    import robertwalters_scraper as rw
    return rw.run(delay=min(delay, 0.5), dry_run=dry_run, limit=limit,
                  include_unclear=False)


def _run_jobspy(pages: int, delay: float, enrich: bool,
                dry_run: bool = False, limit=None) -> dict:
    """
    JobSpy aggregates Indeed Japan, LinkedIn Japan, Glassdoor Japan, and
    Google for Jobs. Runs broad job-category queries and accepts only rows
    whose title + description are written predominantly in English
    (Latin-letter ratio ≥ 0.6).
    """
    import jobspy_scraper as js
    return js.run(sites=None, results_wanted=min(limit or 300, 300),
                  max_raw_per_site=5000,
                  search_terms=None,   # use curated BROAD_JOB_QUERIES
                  english_threshold=0.6,
                  hours_old=720,
                  dry_run=dry_run, verbose=1)


SOURCES: dict[str, Callable] = {
    "gaijinpot":    _run_gaijinpot,
    "tokyodev":     _run_tokyodev,
    "jobsinjapan":  _run_jobsinjapan,
    "japandev":     _run_japandev,
    "yolojapan":    _run_yolojapan,
    "greenhouse":   _run_greenhouse,
    "lever":        _run_lever,
    "ashby":        _run_ashby,
    "workable":     _run_workable,
    "smartrecruiters": _run_smartrecruiters,
    "recruitee":    _run_recruitee,
    "careercross":  _run_careercross,
    "robertwalters": _run_robertwalters,
    "jobspy":       _run_jobspy,
}


def main() -> int:
    p = argparse.ArgumentParser(
        description="Refresh all source scrapers.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Each source")[0],
    )
    p.add_argument("--only", choices=sorted(SOURCES.keys()), default=None,
                   help="Run a single source instead of all.")
    p.add_argument("--skip", action="append", choices=sorted(SOURCES.keys()),
                   default=[], metavar="SOURCE",
                   help="Skip a source (repeatable).")
    p.add_argument("--enrich", action="store_true",
                   help="Pass --enrich through to sources that support it (TokyoDev).")
    p.add_argument("--pages", type=int, default=2,
                   help="How many listing pages to walk on paginated sources (GaijinPot).")
    p.add_argument("--limit", type=int, default=None,
                   help="Bounded run: cap jobs per source (or per company on ATS sources).")
    p.add_argument("--delay", type=float, default=1.5,
                   help="Seconds between requests (used for detail fetches and pagination).")
    p.add_argument("--dry-run", action="store_true",
                   help="Fetch and parse, but write nothing to the database.")
    p.add_argument("--backfill", action="store_true",
                   help="Skip scraping; re-run the data-quality repair pass "
                        "(fix_data.py) over existing rows, then exit.")
    p.add_argument("--verbose", "-v", action="store_true")
    args = p.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    log = logging.getLogger("update")

    if args.backfill:
        import backfill
        sys.argv = ["backfill.py"] + (["--dry-run"] if args.dry_run else ["--apply"])
        return backfill.main()

    sources = [args.only] if args.only else [s for s in SOURCES if s not in args.skip]
    grand_total = {"inserted": 0, "updated": 0, "enriched": 0, "failed": 0, "skipped": 0}
    per_source: list[tuple[str, dict, float]] = []

    for name in sources:
        log.info("=" * 50)
        log.info("source: %s%s", name, " (dry-run)" if args.dry_run else "")
        t0 = time.time()
        try:
            stats = SOURCES[name](pages=args.pages, delay=args.delay,
                                  enrich=args.enrich,
                                  dry_run=args.dry_run, limit=args.limit)
        except Exception as e:
            log.exception("source %s failed: %s", name, e)
            grand_total["failed"] += 1
            per_source.append((name, {"error": str(e)[:80]}, time.time() - t0))
            continue
        elapsed = time.time() - t0
        log.info("  -> %s (%.1fs)", stats, elapsed)
        touched = stats.get("inserted", 0) + stats.get("updated", 0)
        if touched == 0 and not args.dry_run:
            log.warning("source %s returned ZERO jobs — site layout change, "
                        "block, or network issue? Check with: "
                        "python update.py --only %s --limit 5 --verbose",
                        name, name)
        per_source.append((name, stats, elapsed))
        for k, v in stats.items():
            if isinstance(v, (int, float)):
                grand_total[k] = grand_total.get(k, 0) + v

    log.info("=" * 50)
    log.info("%-16s %8s %8s %8s %8s %7s", "source", "inserted", "updated", "failed", "skipped", "secs")
    for name, stats, secs in per_source:
        if "error" in stats:
            log.info("%-16s ERROR: %s", name, stats["error"])
        else:
            log.info("%-16s %8s %8s %8s %8s %7.1f", name,
                     stats.get("inserted", 0), stats.get("updated", 0),
                     stats.get("failed", 0), stats.get("skipped", 0), secs)
    log.info("grand total: %s", grand_total)

    if args.dry_run:
        return 0
    return 0 if grand_total["inserted"] + grand_total["updated"] > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
