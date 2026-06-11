"""
Optional proxy support for scrapers.

Two ways to configure proxies:

  1. GAIJIN_HUNTER_PROXIES env var, comma-separated:
        export GAIJIN_HUNTER_PROXIES="user:pass@1.2.3.4:8080,5.6.7.8:3128"

  2. A `proxies.txt` file next to this module, one proxy per line. Lines
     starting with '#' are comments. Blank lines are ignored.

Each scraper that uses a `ProxyPool` will round-robin through the pool and
put a proxy on cooldown for COOLDOWN_SECONDS when it fails (request error,
or HTTP 403/429/503), so subsequent attempts try a different one.

Proxy formats accepted:
    host:port
    user:pass@host:port
    http://host:port
    socks5://host:port
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Optional

DEFAULT_COOLDOWN_SECONDS = 60


def _normalize(proxy: str) -> str:
    """Add http:// scheme when caller gave only host:port or user:pass@host:port."""
    proxy = proxy.strip()
    if not proxy:
        return ""
    if "://" in proxy:
        return proxy
    return f"http://{proxy}"


def load_proxies() -> list[str]:
    """Return a list of proxy URLs, or [] if no proxies configured."""
    # Env var first
    env = os.environ.get("GAIJIN_HUNTER_PROXIES", "").strip()
    if env:
        return [_normalize(p) for p in env.split(",") if p.strip()]

    # Then proxies.txt next to this module
    path = Path(__file__).parent / "proxies.txt"
    if path.exists():
        out: list[str] = []
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            out.append(_normalize(line))
        return out
    return []


class ProxyPool:
    """
    Round-robin proxy rotation with per-proxy cooldown.

    Typical usage in a scraper:

        pool = ProxyPool(load_proxies())
        for attempt in range(3):
            proxy = pool.next()
            try:
                r = session.get(url, **pool.requests_kwargs(proxy), timeout=20)
            except RequestException:
                if proxy: pool.mark_failed(proxy)
                continue
            if r.status_code in (403, 429, 503):
                if proxy: pool.mark_failed(proxy)
                continue
            ...

    `next()` returns None when the pool is empty (so the scraper falls back
    to direct connection) or when all proxies are currently on cooldown.
    """

    def __init__(self, proxies: Optional[list[str]] = None,
                 cooldown_seconds: int = DEFAULT_COOLDOWN_SECONDS):
        self.proxies: list[str] = [p for p in (proxies or []) if p]
        self.cooldown = cooldown_seconds
        self._available_at: dict[str, float] = {}   # proxy -> ts when usable again
        self._idx = 0

    def __len__(self) -> int:
        return len(self.proxies)

    def __bool__(self) -> bool:
        return bool(self.proxies)

    def next(self) -> Optional[str]:
        """Return the next proxy not on cooldown, or None if none available."""
        if not self.proxies:
            return None
        now = time.time()
        # Expire any cooldowns whose timer has lapsed
        self._available_at = {p: t for p, t in self._available_at.items() if t > now}
        # Walk the ring once
        n = len(self.proxies)
        for _ in range(n):
            p = self.proxies[self._idx % n]
            self._idx += 1
            if p not in self._available_at:
                return p
        return None  # everything is currently cooling down

    def mark_failed(self, proxy: str) -> None:
        if proxy:
            self._available_at[proxy] = time.time() + self.cooldown

    @staticmethod
    def requests_kwargs(proxy: Optional[str]) -> dict:
        """Build the kwargs dict to pass into `requests.Session.get()`."""
        if not proxy:
            return {}
        return {"proxies": {"http": proxy, "https": proxy}}
