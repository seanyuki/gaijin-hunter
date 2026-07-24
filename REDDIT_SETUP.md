# Auto-posting job digests to your own subreddit

`reddit_poster.py` posts a digest of the top 10 English-friendly roles from the
board to a subreddit. We're targeting **your own subreddit** — zero ban risk,
you own the rules, and it's safe to fully automate.

## Step 1 — create the subreddit (once)
1. Logged in on Reddit → **Create a community** (e.g. `r/GaijinHunter`).
2. Set it Public. In the community settings, allow **text posts**.
3. (Optional) Add a post flair like "Weekly digest" if you want them tagged.

## Step 2 — create the API app (once)
1. Go to <https://www.reddit.com/prefs/apps> → **create another app…**
2. Type **script**. Name it, set redirect URI to `http://localhost:8080`.
3. Note the **client_id** (the string under the app name) and **client_secret**.

## Step 3 — credentials (never commit these)
Put them in a local `.env` (already gitignored) or your host's secret store:
```bash
export REDDIT_CLIENT_ID=xxxxxxxx
export REDDIT_CLIENT_SECRET=xxxxxxxxxxxxxxxx
export REDDIT_USERNAME=your_reddit_user
export REDDIT_PASSWORD=your_reddit_password
export REDDIT_SUBREDDIT=GaijinHunter          # your sub, no "r/"
export BASE_URL=https://gaijinhunterjp.com     # so job links are absolute
```

## Step 4 — install + test
```bash
pip install praw                               # already in requirements.txt

# DRY RUN — prints the exact post, touches nothing:
python reddit_poster.py --no-teaching

# First real post, to r/test (Reddit's sandbox) to confirm creds work:
python reddit_poster.py --subreddit test --post

# Then the real thing, to your sub:
python reddit_poster.py --subreddit GaijinHunter --no-teaching --post
```
It remembers featured job IDs in `.reddit_posted.json`, so the next digest
pulls fresh roles. Use `--repeat-ok` to allow repeats, `--count N` to change
how many.

## Step 5 — schedule it

### Option A — local crontab (simplest)
Weekly, Monday 09:00 JST (00:00 UTC). `crontab -e`:
```cron
0 0 * * 1  cd /path/to/gaijinhunter && \
  set -a && . ./.env && set +a && \
  /usr/bin/python3 reddit_poster.py --subreddit GaijinHunter --no-teaching --post \
  >> reddit_poster.log 2>&1
```

### Option B — Render cron (matches your scraper cron in render.yaml)
Add a cron job alongside the scraper one:
```yaml
  - type: cron
    name: reddit-digest
    schedule: "0 0 * * 1"        # weekly, Monday 00:00 UTC
    startCommand: python reddit_poster.py --subreddit GaijinHunter --no-teaching --post
    envVars:
      - key: REDDIT_CLIENT_ID
        sync: false             # set in the Render dashboard, not in the repo
      - key: REDDIT_CLIENT_SECRET
        sync: false
      - key: REDDIT_USERNAME
        sync: false
      - key: REDDIT_PASSWORD
        sync: false
      - key: REDDIT_SUBREDDIT
        value: GaijinHunter
      - key: BASE_URL
        value: https://gaijinhunterjp.com
```
Set the four secret vars in the Render dashboard (sync:false keeps them out of
git). Post-frequency: weekly is plenty; daily digests to your own sub are fine
too but tend to look spammy even on your own turf.

## Growing the audience (optional, manual)
Your own sub is safe but small at first. To reach people, occasionally (as a
human, not the bot) share a single genuinely useful post or answer questions in
r/movingtojapan / r/japanlife **within their rules** — do NOT point the
auto-poster at those subs; aggregator/link posts there get removed and can
shadowban the account. Keep automation on your turf; do outreach by hand.
