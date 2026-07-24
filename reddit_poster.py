"""
Post a digest of 10 job listings from the board to Reddit.

Pulls the top English-friendly roles from the DB, formats a Markdown post that
links back to each job's page on the site, and (optionally) submits it to a
subreddit via Reddit's official API. Remembers which job IDs it has already
posted so consecutive digests feature fresh roles.

SAFETY: by default this is a DRY RUN — it prints the exact post and does NOT
touch Reddit. It only submits when you pass --post AND valid credentials are
present in the environment. Read the "Reddit rules" note in the README section
below before you automate this: most subreddits restrict self-promotion and
automated posting can get an account banned/shadowbanned.

Setup (once):
  1. Create a Reddit "script" app at https://www.reddit.com/prefs/apps
     -> note the client_id (under the app name) and client_secret.
  2. pip install praw           (also add it to requirements.txt)
  3. Export credentials (e.g. in a .env you don't commit):
       export REDDIT_CLIENT_ID=...
       export REDDIT_CLIENT_SECRET=...
       export REDDIT_USERNAME=...
       export REDDIT_PASSWORD=...
       export REDDIT_SUBREDDIT=test        # start with r/test !
       export BASE_URL=https://gaijinhunterjp.com

Usage:
  python reddit_poster.py                      # DRY RUN: print the post only
  python reddit_poster.py --subreddit test --post   # actually submit to r/test
  python reddit_poster.py --count 10 --no-teaching  # tune the selection
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import db

SITE_NAME = "Gaijin Hunter"
STATE_PATH = Path(__file__).parent / ".reddit_posted.json"   # posted job-id memory

log = logging.getLogger("reddit_poster")


def _base_url() -> str:
    return (os.environ.get("BASE_URL") or "https://gaijinhunterjp.com").rstrip("/")


def _load_posted() -> set[int]:
    if STATE_PATH.exists():
        try:
            return set(json.loads(STATE_PATH.read_text()).get("posted_ids", []))
        except (ValueError, OSError):
            return set()
    return set()


def _save_posted(ids: set[int]) -> None:
    STATE_PATH.write_text(json.dumps({"posted_ids": sorted(ids)}, indent=0))


def select_jobs(count: int, exclude_teaching: bool,
                exclude_posted: bool) -> list[dict]:
    """Top English-friendly, board-visible roles, best fit first, freshest tiebreak."""
    posted = _load_posted() if exclude_posted else set()
    clauses = [
        "(moderation_status IS NULL OR moderation_status='approved')",
        "(employer_post_status IS NULL OR employer_post_status='published')",
        "posting_language IN ('English','Bilingual')",
        "title IS NOT NULL AND url IS NOT NULL",
    ]
    if exclude_teaching:
        clauses.append("(role_family IS NULL OR role_family <> 'Teaching / Education')")
    sql = (
        "SELECT id,title,company_name,location,salary,english_level,"
        "role_family,foreigner_fit_score,post_date "
        "FROM jobs WHERE " + " AND ".join(clauses) +
        " ORDER BY COALESCE(foreigner_fit_score,0) DESC, "
        "COALESCE(post_date, scraped_at) DESC LIMIT ?"
    )
    with db.connect() as conn:
        # Over-fetch so we can skip already-posted rows and still hit `count`.
        rows = [dict(r) for r in conn.execute(sql, (count * 6,)).fetchall()]
    out = [r for r in rows if r["id"] not in posted][:count]
    return out


def _fmt_salary(job: dict) -> str:
    s = (job.get("salary") or "").strip()
    return s if s else "Salary not listed"


def format_post(jobs: list[dict]) -> tuple[str, str]:
    """Return (title, markdown_body) for the Reddit submission."""
    base = _base_url()
    today = datetime.now(timezone.utc).strftime("%b %d, %Y")
    title = f"{len(jobs)} English-friendly jobs in Japan — {today}"

    lines = [
        f"A fresh batch of English-friendly roles in Japan, pulled from "
        f"[{SITE_NAME}]({base}). Each links to the listing with the original "
        f"source, salary, and Japanese-level info.\n",
    ]
    for i, j in enumerate(jobs, 1):
        url = f"{base}/job/{j['id']}"
        company = (j.get("company_name") or "").strip() or "Company on listing"
        loc = (j.get("location") or "Japan").strip()
        meta = [company, loc]
        if j.get("english_level"):
            meta.append(f"English: {j['english_level']}")
        sal = _fmt_salary(j)
        if sal != "Salary not listed":
            meta.append(sal)
        lines.append(f"**{i}. [{j['title'].strip()}]({url})**  \n"
                     f"{' · '.join(meta)}\n")
    lines.append(
        f"\n---\n\nSee the full board (filter by role, English level, visa "
        f"support, salary): **{base}/jobs**\n\n"
        f"*I run {SITE_NAME}; happy to answer questions in the comments.*"
    )
    return title, "\n".join(lines)


def submit(subreddit: str, title: str, body: str, flair: Optional[str]) -> str:
    import praw  # imported lazily so --dry-run works without praw installed
    missing = [k for k in ("REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET",
                           "REDDIT_USERNAME", "REDDIT_PASSWORD")
               if not os.environ.get(k)]
    if missing:
        raise SystemExit(f"Missing Reddit credentials in env: {', '.join(missing)}")
    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        user_agent=f"{SITE_NAME} job digest by u/{os.environ['REDDIT_USERNAME']}",
    )
    reddit.validate_on_submit = True
    sub = reddit.subreddit(subreddit)
    kwargs = {"title": title, "selftext": body}
    if flair:  # only if the sub requires/offers flair
        for tmpl in sub.flair.link_templates.user_selectable():
            if flair.lower() in tmpl["flair_text"].lower():
                kwargs["flair_id"] = tmpl["flair_template_id"]
                break
    post = sub.submit(**kwargs)
    return f"https://reddit.com{post.permalink}"


def main() -> int:
    ap = argparse.ArgumentParser(description="Post a 10-job digest to Reddit.")
    ap.add_argument("--count", type=int, default=10)
    ap.add_argument("--subreddit", default=os.environ.get("REDDIT_SUBREDDIT", "test"))
    ap.add_argument("--flair", default=os.environ.get("REDDIT_FLAIR"))
    ap.add_argument("--no-teaching", dest="teaching", action="store_false",
                    help="exclude English-teaching roles")
    ap.add_argument("--repeat-ok", action="store_true",
                    help="allow jobs featured in previous digests")
    ap.add_argument("--post", action="store_true",
                    help="actually submit to Reddit (default is a dry run)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(levelname)s %(message)s")

    jobs = select_jobs(args.count, exclude_teaching=(args.teaching is False),
                       exclude_posted=not args.repeat_ok)
    if len(jobs) < args.count:
        log.warning("only %d jobs matched (wanted %d)", len(jobs), args.count)
    if not jobs:
        log.error("no jobs to post"); return 1

    title, body = format_post(jobs)

    if not args.post:
        print("=" * 70)
        print("DRY RUN — nothing posted. Target subreddit:", args.subreddit)
        print("=" * 70)
        print("TITLE:", title, "\n")
        print(body)
        print("\n" + "=" * 70)
        print(f"Run with --post to submit to r/{args.subreddit}.")
        return 0

    url = submit(args.subreddit, title, body, args.flair)
    log.info("posted: %s", url)
    _save_posted(_load_posted() | {j["id"] for j in jobs})
    return 0


if __name__ == "__main__":
    sys.exit(main())
