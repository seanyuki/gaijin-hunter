"""
Environment-driven configuration. Safe local defaults; production overrides
via environment variables (see .env.example).

    FLASK_ENV       "development" (default) or "production"
    SECRET_KEY      required in production (random fallback + warning if absent)
    JAPAN_JOBS_DB   path to the SQLite database (default: ./jobs.db)
    BASE_URL        public origin for canonical/sitemap/OG URLs,
                    e.g. https://gaijinhunter.jp (default: per-request)
    HOST / PORT     bind address for `python app.py` (default 127.0.0.1:5000)
"""

from __future__ import annotations

import logging
import os
import secrets

ENV = os.environ.get("FLASK_ENV", "development").lower()
IS_PRODUCTION = ENV == "production"

# Debug is ONLY ever on in development, and can be disabled there too.
DEBUG = (not IS_PRODUCTION) and os.environ.get("FLASK_DEBUG", "1") != "0"

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    # Random per-process key: fine for this app (no server-side sessions),
    # but warn loudly in production so it gets set properly.
    SECRET_KEY = secrets.token_hex(32)
    if IS_PRODUCTION:
        logging.getLogger("config").warning(
            "SECRET_KEY is not set; generated an ephemeral key. "
            "Set SECRET_KEY in the environment for production.")

# Public origin used for canonical URLs, sitemap, OG tags, llms.txt.
# Empty -> templates/views fall back to the per-request URL root.
# Production for this project: https://gaijinhunterjp.com (apex is canonical;
# www and the .onrender.com host 301 to it — see DOMAIN_SETUP.md).
BASE_URL = os.environ.get("BASE_URL", "").rstrip("/")

# Host derived from BASE_URL. When set (production), requests arriving on any
# other host (www., the Render *.onrender.com subdomain, …) are 301-redirected
# to the canonical origin by app.py. Never active in development.
CANONICAL_HOST = ""
if BASE_URL and "://" in BASE_URL:
    # Hostname only — ports are deployment plumbing, never canonicalization
    # input (comparing with a port caused redirect loops in local prod tests).
    CANONICAL_HOST = BASE_URL.split("://", 1)[1].split("/", 1)[0].split(":")[0]

HOST = os.environ.get("HOST", "127.0.0.1")
try:
    PORT = int(os.environ.get("PORT", "5000"))
except ValueError:
    PORT = 5000

# Static asset caching: long in production (assets are stable), off in dev.
STATIC_MAX_AGE = 60 * 60 * 24 * 7 if IS_PRODUCTION else 0

# Database path is owned by db.py (JAPAN_JOBS_DB env var) — re-exported here
# so docs/scripts have one place to look.
DB_PATH = os.environ.get("JAPAN_JOBS_DB", os.path.join(os.path.dirname(__file__), "jobs.db"))
