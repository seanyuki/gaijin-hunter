"""
Salary string -> (min_jpy, max_jpy) normalization.

Handles the formats we see in the wild:
    '¥6.9M ~ ¥11.0M'                  -> (6_900_000, 11_000_000)
    '¥6,900,000 ~ ¥11,004,000'        -> (6_900_000, 11_004_000)
    '¥6.4M ~ ¥13M'                    -> (6_400_000, 13_000_000)
    '6,000,000 yen / year'            -> (6_000_000, 6_000_000)
    '¥10,500 ~ ¥10,500 / Lesson'      -> (10_500, 10_500)
    '¥290,000 ~ ¥380,000 / Month'     -> (290_000, 380_000)   <- monthly
    '8,000,000 - 12,000,000 yen / year'   -> (8_000_000, 12_000_000)

When the period is monthly/weekly/daily/hourly, the returned values are NOT
converted to annual — callers should look at `period` if they want apples-to-
apples comparisons. We chose this to preserve the original number so the UI
can display it accurately; the sort/filter layer can compute an annualized
value separately.
"""

from __future__ import annotations

import re
from typing import Optional, Tuple


# ¥6.9M  ¥10K  ¥6.4M-¥13M  6900000  6,900,000
# Capture: number, optional unit (K / M / 万 / 億)
_NUM_RE = re.compile(
    r"(?P<num>\d+(?:,\d{3})*(?:\.\d+)?)"
    r"\s*(?P<unit>[KkMm万億]|million|thousand)?",
)

# Period detection in the original string.
# Don't use \b around alternations that start with '/' — '/' isn't a word
# character, so \b/ fails when the slash is preceded by whitespace.
_PERIOD_PATTERNS = [
    (r"(?:\bannual(?:ly)?\b|\byearly\b|per\s*year|/\s*ye?a?r?\b)", "Year"),
    (r"(?:\bmonthly\b|per\s*month|/\s*mo(?:nth)?\b)",              "Month"),
    (r"(?:\bweekly\b|per\s*week|/\s*we?e?k?\b)",                   "Week"),
    (r"(?:\bdaily\b|per\s*day|/\s*day\b)",                         "Day"),
    (r"(?:\bhourly\b|per\s*hour|/\s*ho?u?r?\b)",                   "Hour"),
    (r"/\s*lesson\b",                                              "Lesson"),
]


def _scale(unit: Optional[str]) -> int:
    if not unit:
        return 1
    u = unit.lower()
    if u in ("k", "thousand"):
        return 1_000
    if u in ("m", "million"):
        return 1_000_000
    if u == "万":   # 10,000
        return 10_000
    if u == "億":   # 100,000,000
        return 100_000_000
    return 1


def parse_period(raw: str) -> Optional[str]:
    if not raw:
        return None
    s = raw.lower()
    for pattern, label in _PERIOD_PATTERNS:
        if re.search(pattern, s):
            return label
    return None


def parse_range(raw: Optional[str]) -> Tuple[Optional[int], Optional[int]]:
    """Return (min_jpy, max_jpy). When only one number is present, both fields
    are the same. Returns (None, None) if no number can be parsed."""
    if not raw:
        return (None, None)

    # Find all (number, unit) pairs in the string
    matches = list(_NUM_RE.finditer(raw))
    nums: list[int] = []
    for m in matches:
        # Skip stray small numbers that come right after "/" (period markers
        # like "/ Year") — these aren't compensation. Easy check: if the digit
        # is preceded by '/', skip.
        start = m.start()
        if start > 0 and raw[max(0, start - 2):start].strip() == "/":
            continue
        try:
            n = float(m.group("num").replace(",", ""))
        except ValueError:
            continue
        scaled = int(round(n * _scale(m.group("unit"))))
        # Salary numbers in JPY are realistically >= 1,000.
        # Drop anything smaller — protects against years, IDs, etc.
        if scaled < 1_000:
            continue
        nums.append(scaled)

    if not nums:
        return (None, None)

    lo = min(nums)
    hi = max(nums)
    return (lo, hi)


def annualize(value: Optional[int], period: Optional[str]) -> Optional[int]:
    """Project a salary value to an annual figure for fair comparison.
    Used by the sort-by-salary feature. Returns None if either input is None."""
    if value is None:
        return None
    if not period or period == "Year":
        return value
    p = period.capitalize()
    multipliers = {
        "Month": 12, "Week": 52, "Day": 240,   # ~workdays/year
        "Hour": 240 * 8, "Lesson": 0,           # lessons are too irregular
    }
    mult = multipliers.get(p)
    if mult is None or mult == 0:
        return None
    return value * mult


# ===========================================================================
# Conservative free-text salary extraction (for rows with no structured
# salary — mainly JobSpy). Anchored patterns only; when in doubt, return None.
# ===========================================================================

# Words that mean a nearby number is NOT a salary.
_TEXT_FALSE_CONTEXT = re.compile(
    r"years?\s+of\s+experience|employees?|founded|established|revenue|"
    r"funding|members|users|customers|headcount|per\s+cent|percent|"
    r"\bvaluation\b|\bbudget\s+of\b",
    re.IGNORECASE,
)

_JPY_ANNUAL_BOUNDS  = (1_500_000, 100_000_000)
_JPY_MONTHLY_BOUNDS = (120_000, 3_000_000)
_JPY_HOURLY_BOUNDS  = (900, 10_000)
_JPY_DAILY_BOUNDS   = (5_000, 120_000)

_USD_JPY = 150  # deliberate, rough; flagged as inferred by callers


def _in(b, v):  # bounds check
    return v is not None and b[0] <= v <= b[1]


def _window_ok(text: str, start: int, end: int) -> bool:
    return not _TEXT_FALSE_CONTEXT.search(text[max(0, start - 50): end + 50])


def extract_from_text(text: Optional[str]) -> Optional[dict]:
    """Extract an explicit salary statement from free text.

    Returns {"salary": display_string, "salary_period": period,
             "salary_min_jpy", "salary_max_jpy",
             "salary_min_annual_jpy", "salary_max_annual_jpy"}
    or None when nothing unambiguous is found. Never guesses: a match needs a
    currency/salary anchor AND values inside sane bounds for its period.
    """
    if not text:
        return None
    s = str(text)

    def result(lo, hi, period, display):
        lo_a = annualize(lo, period)
        hi_a = annualize(hi, period)
        return {"salary": display, "salary_period": period,
                "salary_min_jpy": lo, "salary_max_jpy": hi,
                "salary_min_annual_jpy": lo_a, "salary_max_annual_jpy": hi_a}

    def to_int(numstr, unit=None):
        v = float(numstr.replace(",", ""))
        return int(v * _scale(unit))

    # --- 1. Japanese explicit forms -------------------------------------
    # 年収 600万円〜1,000万円 / 年収600万〜
    m = re.search(r"年収\s*([\d,.]+)\s*万?円?\s*[〜~\-–]\s*([\d,.]+)\s*万円", s)
    if m and _window_ok(s, m.start(), m.end()):
        lo, hi = to_int(m.group(1), "万"), to_int(m.group(2), "万")
        if _in(_JPY_ANNUAL_BOUNDS, lo) and _in(_JPY_ANNUAL_BOUNDS, hi) and lo <= hi:
            return result(lo, hi, "Year", f"¥{lo:,} – ¥{hi:,}")
    m = re.search(r"年収\s*([\d,.]+)\s*万円", s)
    if m and _window_ok(s, m.start(), m.end()):
        v = to_int(m.group(1), "万")
        if _in(_JPY_ANNUAL_BOUNDS, v):
            return result(v, v, "Year", f"¥{v:,}")
    # 6,000,000円〜10,000,000円 (annual magnitude)
    m = re.search(r"([\d]{1,3}(?:,\d{3})+)\s*円\s*[〜~\-–]\s*([\d]{1,3}(?:,\d{3})+)\s*円", s)
    if m and _window_ok(s, m.start(), m.end()):
        lo, hi = to_int(m.group(1)), to_int(m.group(2))
        if _in(_JPY_ANNUAL_BOUNDS, lo) and _in(_JPY_ANNUAL_BOUNDS, hi) and lo <= hi:
            return result(lo, hi, "Year", f"¥{lo:,} – ¥{hi:,}")
        if _in(_JPY_MONTHLY_BOUNDS, lo) and _in(_JPY_MONTHLY_BOUNDS, hi) and lo <= hi \
           and re.search(r"月給|月収|monthly", s[max(0, m.start()-20):m.end()+20], re.I):
            return result(lo, hi, "Month", f"¥{lo:,} – ¥{hi:,}/mo")
    # 月給30万円 / 月給 300,000円
    m = re.search(r"月[給収]\s*([\d,.]+)\s*(万)?円", s)
    if m and _window_ok(s, m.start(), m.end()):
        v = to_int(m.group(1), m.group(2))
        if _in(_JPY_MONTHLY_BOUNDS, v):
            return result(v, v, "Month", f"¥{v:,}/mo")
    # 時給1,500円
    m = re.search(r"時給\s*([\d,]+)\s*円", s)
    if m and _window_ok(s, m.start(), m.end()):
        v = to_int(m.group(1))
        if _in(_JPY_HOURLY_BOUNDS, v):
            return result(v, v, "Hour", f"¥{v:,}/hr")
    # 日給10,000円
    m = re.search(r"日給\s*([\d,]+)\s*円", s)
    if m and _window_ok(s, m.start(), m.end()):
        v = to_int(m.group(1))
        if _in(_JPY_DAILY_BOUNDS, v):
            return result(v, v, "Day", f"¥{v:,}/day")

    # --- 2. ¥xM – ¥yM (annual by JPY convention) ------------------------
    m = re.search(r"[¥￥]\s*(\d+(?:\.\d+)?)\s*[Mm]\s*(?:[〜~\-–]|to)\s*[¥￥]?\s*(\d+(?:\.\d+)?)\s*[Mm]\b", s)
    if m and _window_ok(s, m.start(), m.end()):
        lo, hi = to_int(m.group(1), "M"), to_int(m.group(2), "M")
        if _in(_JPY_ANNUAL_BOUNDS, lo) and _in(_JPY_ANNUAL_BOUNDS, hi) and lo <= hi:
            return result(lo, hi, "Year", f"¥{lo:,} – ¥{hi:,}")
    m = re.search(r"[¥￥]\s*(\d+(?:\.\d+)?)\s*[Mm]\b", s)
    if m and _window_ok(s, m.start(), m.end()):
        v = to_int(m.group(1), "M")
        if _in(_JPY_ANNUAL_BOUNDS, v):
            return result(v, v, "Year", f"¥{v:,}")

    # --- 3. ¥ full numbers with explicit period or annual magnitude -----
    m = re.search(r"[¥￥]\s*([\d]{1,3}(?:,\d{3})+)\s*(?:[〜~\-–]|to)\s*[¥￥]?\s*([\d]{1,3}(?:,\d{3})+)", s)
    if m and _window_ok(s, m.start(), m.end()):
        lo, hi = to_int(m.group(1)), to_int(m.group(2))
        ctx = s[max(0, m.start()-30): m.end()+30].lower()
        period = parse_period(ctx)
        if period is None and _in(_JPY_ANNUAL_BOUNDS, lo) and _in(_JPY_ANNUAL_BOUNDS, hi):
            period = "Year"
        bounds = {"Year": _JPY_ANNUAL_BOUNDS, "Month": _JPY_MONTHLY_BOUNDS,
                  "Hour": _JPY_HOURLY_BOUNDS, "Day": _JPY_DAILY_BOUNDS}.get(period)
        if bounds and _in(bounds, lo) and _in(bounds, hi) and lo <= hi:
            unit = {"Year": "", "Month": "/mo", "Hour": "/hr", "Day": "/day"}[period]
            return result(lo, hi, period, f"¥{lo:,} – ¥{hi:,}{unit}")

    # --- 4. "salary: 6,000,000 - 10,000,000 yen" ------------------------
    m = re.search(r"(?:salary|compensation)[:\s]{1,4}([\d]{1,3}(?:,\d{3})+)\s*(?:[〜~\-–]|to)\s*([\d]{1,3}(?:,\d{3})+)\s*(?:yen|jpy|円)",
                  s, re.IGNORECASE)
    if m and _window_ok(s, m.start(), m.end()):
        lo, hi = to_int(m.group(1)), to_int(m.group(2))
        if _in(_JPY_ANNUAL_BOUNDS, lo) and _in(_JPY_ANNUAL_BOUNDS, hi) and lo <= hi:
            return result(lo, hi, "Year", f"¥{lo:,} – ¥{hi:,}")

    # --- 5. Clearly-annual USD ("$120K per year", "USD 90,000/year") ----
    m = re.search(r"(?:\$|usd\s*)\s*(\d{2,3})[Kk]\b(?P<tail>.{0,30})", s)
    if m and _window_ok(s, m.start(), m.end()):
        if re.search(r"per\s+year|annual|/\s*yr|a\s+year", m.group("tail"), re.I):
            lo = int(m.group(1)) * 1000 * _USD_JPY
            if _in(_JPY_ANNUAL_BOUNDS, lo):
                return result(lo, lo, "Year", f"${m.group(1)}K/yr (≈¥{lo:,})")

    return None
