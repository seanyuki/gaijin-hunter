"""Download each mapped company's brand icon ONCE into static/logos/<slug>.png.

Source is a public favicon service (DuckDuckGo, with Google as fallback). Run
this at build/deploy time; visitors are then served logos from our own domain,
so no third-party request happens at view time. Re-runnable and idempotent
(skips files that already exist unless --force). Logos are used for company
identification only.

Usage:
  python fetch_logos.py            # fetch missing
  python fetch_logos.py --force    # re-download all
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import requests

import company_logos as cl

OUT_DIR = Path(__file__).parent / "static" / "logos"
SOURCES = [
    "https://icons.duckduckgo.com/ip3/{domain}.ico",
    "https://www.google.com/s2/favicons?domain={domain}&sz=128",
]
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; GaijinHunterBot/1.0)"}


def _fetch_one(domain: str, dest: Path) -> bool:
    for tmpl in SOURCES:
        url = tmpl.format(domain=domain)
        try:
            r = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
        except requests.RequestException:
            continue
        ctype = r.headers.get("content-type", "")
        # Reject HTML error pages and tiny 1x1 placeholders.
        if r.status_code == 200 and "image" in ctype and len(r.content) > 120:
            dest.write_bytes(r.content)
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch company logos to static/logos/")
    ap.add_argument("--force", action="store_true", help="re-download existing files")
    ap.add_argument("--delay", type=float, default=0.3)
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    seen: dict[str, str] = {}  # slug -> domain (dedupe aliases like aws/amazon web services)
    for name, domain in cl.COMPANY_DOMAINS.items():
        seen.setdefault(cl.slug_for(name), domain)

    ok = skip = fail = 0
    for slug, domain in sorted(seen.items()):
        dest = OUT_DIR / f"{slug}.png"
        if dest.exists() and not args.force:
            skip += 1
            continue
        if _fetch_one(domain, dest):
            ok += 1
            print(f"  ok    {slug:<26} <- {domain}")
        else:
            fail += 1
            print(f"  FAIL  {slug:<26} <- {domain}")
        time.sleep(args.delay)

    print(f"\nfetched={ok} skipped={skip} failed={fail} -> {OUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
