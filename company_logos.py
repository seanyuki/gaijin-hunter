"""Self-hosted company logos with a monogram fallback.

We don't store company domains, so logos are opt-in via a curated
name -> domain map of recognizable employers. `fetch_logos.py` downloads each
logo ONCE into static/logos/<slug>.png (so visitors' browsers never call a
third party — keeping the no-third-party-tracking promise). Templates call
`logo_url(name)`: it returns a local URL only when we actually have a file,
otherwise None and the UI shows the existing initials monogram.

Add a company by putting its (normalized) name -> domain here and re-running
`python fetch_logos.py`.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

_LOGO_DIR = Path(__file__).parent / "static" / "logos"

# Normalized company name -> domain. Keys are matched after _norm() (lowercased,
# company suffixes like 株式会社 / Inc. / K.K. stripped). Only confident,
# well-known domains — a wrong domain would show the wrong logo.
COMPANY_DOMAINS: dict[str, str] = {
    # Japan tech / startups
    "salesforce": "salesforce.com",
    "money forward": "moneyforward.com",
    "mercari": "mercari.com",
    "rakuten": "rakuten.com",
    "line yahoo": "lycorp.co.jp",
    "ly corporation": "lycorp.co.jp",
    "paypay": "paypay.ne.jp",
    "smartnews": "smartnews.com",
    "cybozu": "cybozu.com",
    "sansan": "sansan.com",
    "freee": "freee.co.jp",
    "hennge": "hennge.com",
    "exawizards": "exawizards.com",
    "rapyuta robotics": "rapyuta-robotics.com",
    "preferred networks": "preferred.jp",
    "sakana ai": "sakana.ai",
    "softbank": "softbank.jp",
    "sony": "sony.com",
    "nintendo": "nintendo.co.jp",
    "fast retailing": "fastretailing.com",
    "uniqlo": "uniqlo.com",
    "woven by toyota": "woven.toyota",
    "woven": "woven.toyota",
    "toyota": "toyota.com",
    "honda": "honda.com",
    "panasonic": "panasonic.com",
    "hitachi": "hitachi.com",
    "fujitsu": "fujitsu.com",
    "nec": "nec.com",
    "ntt data": "nttdata.com",
    "mufg": "mufg.jp",
    "nomura": "nomura.com",
    # Global tech in Japan
    "google": "google.com",
    "amazon": "amazon.com",
    "amazon web services": "aws.amazon.com",
    "aws": "aws.amazon.com",
    "microsoft": "microsoft.com",
    "indeed": "indeed.com",
    "stripe": "stripe.com",
    "datadog": "datadoghq.com",
    "notion": "notion.so",
    "hubspot": "hubspot.com",
    "canva": "canva.com",
    "wise": "wise.com",
    "apple": "apple.com",
    "meta": "meta.com",
    "netflix": "netflix.com",
    "spotify": "spotify.com",
    "airbnb": "airbnb.com",
    "uber": "uber.com",
    "ibm": "ibm.com",
    "oracle": "oracle.com",
    "sap": "sap.com",
    "adobe": "adobe.com",
    "cisco": "cisco.com",
    "nvidia": "nvidia.com",
    "intel": "intel.com",
    "openai": "openai.com",
    "agoda": "agoda.com",
    "booking.com": "booking.com",
    "expedia": "expedia.com",
    # Finance / consulting
    "goldman sachs": "goldmansachs.com",
    "morgan stanley": "morganstanley.com",
    "jpmorgan": "jpmorgan.com",
    "j.p. morgan": "jpmorgan.com",
    "jp morgan": "jpmorgan.com",
    "mckinsey": "mckinsey.com",
    "bcg": "bcg.com",
    "boston consulting group": "bcg.com",
    "bain": "bain.com",
    "deloitte": "deloitte.com",
    "accenture": "accenture.com",
    "pwc": "pwc.com",
    "kpmg": "kpmg.com",
    # Recruiting / staffing (recognizable)
    "robert walters": "robertwalters.co.jp",
    "michael page": "michaelpage.co.jp",
    "hays": "hays.co.jp",
    "en world": "enworld.com",
    "robert half": "roberthalf.com",
}

_SUFFIX_RE = re.compile(
    r"(株式会社|有限会社|合同会社|グループ|ジャパン|"
    r"\bco\.?,?\s*ltd\.?|\binc\.?|\bcorp(?:oration)?\.?|\bltd\.?|\bk\.?k\.?|"
    r"\bllc|\bgmbh|\bpte\.?|\bgroup\b|\bjapan\b)",
    re.IGNORECASE,
)


def _norm(name: Optional[str]) -> str:
    if not name:
        return ""
    s = _SUFFIX_RE.sub(" ", name.lower())
    s = re.sub(r"[^a-z0-9.぀-ヿ一-鿿 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def slug_for(name: Optional[str]) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", _norm(name)).strip("-")
    return s or "x"


def domain_for(name: Optional[str]) -> Optional[str]:
    return COMPANY_DOMAINS.get(_norm(name))


_available: Optional[set[str]] = None


def _scan() -> set[str]:
    global _available
    if _available is None:
        _available = {p.stem for p in _LOGO_DIR.glob("*.png")} if _LOGO_DIR.exists() else set()
    return _available


def logo_url(name: Optional[str]) -> Optional[str]:
    """Local URL for a self-hosted logo, or None (caller shows the monogram)."""
    if not domain_for(name):
        return None
    slug = slug_for(name)
    return f"/static/logos/{slug}.png" if slug in _scan() else None
