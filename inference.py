"""
Shared body-text inference for fields that source APIs don't structure: the
Japanese / English proficiency required, visa-sponsorship signal, remote-work
indicator, and Japan-location detection. Used by every scraper that has to
fall back to regex over a job description.
"""

from __future__ import annotations

import re
from typing import Optional


# Level patterns allow common filler words ("level", "fluency", "ability")
# between the level word and the language word.
JP_LEVEL_BODY_PATTERNS: list[tuple[str, str]] = [
    (r"\bnative\s+(?:level\s+)?japanese|\bjapanese[:\s]*native\b",                "Native / Fluent"),
    (r"\bfluent\s+(?:in\s+)?japanese|\bjapanese[:\s]*fluent\b",                   "Native / Fluent"),
    (r"\bbusiness\s+(?:level\s+)?japanese|\bjapanese[:\s]*business\b|\bn1\b",     "Business / Professional"),
    (r"\bjapanese[:\s]*n2\b|\bn2\b",                                              "Business / Professional"),
    (r"\bconversational\s+(?:level\s+)?japanese|\bjapanese[:\s]*conversational\b|\bn3\b", "Conversational"),
    (r"\bbasic\s+(?:level\s+)?japanese|\bjapanese[:\s]*basic\b|\bn4\b",           "Basic / Beginner"),
    (r"\bn5\b",                                                                    "Basic / Beginner"),
    (r"\bno\s+japanese\s+(?:is\s+)?required|japanese\s+(?:is\s+)?not\s+required", "Not Required"),
]

EN_LEVEL_BODY_PATTERNS: list[tuple[str, str]] = [
    (r"\bnative\s+(?:level\s+)?english|\benglish[:\s]*native\b",                  "Native / Fluent"),
    (r"\bfluent\s+(?:in\s+)?english|\benglish[:\s]*fluent\b",                     "Native / Fluent"),
    (r"\bbusiness\s+(?:level\s+)?english|\benglish[:\s]*business\b",              "Business / Professional"),
    (r"\bconversational\s+(?:level\s+)?english|\benglish[:\s]*conversational\b",  "Conversational"),
    (r"\bbasic\s+(?:level\s+)?english|\benglish[:\s]*basic\b",                    "Basic / Beginner"),
    (r"\benglish\s+is\s+required|english\s+proficiency\s+(?:is\s+)?required",     "Business / Professional"),
]

# Phrases where the word "english" describes a THING (a page, a document, a
# translation), not a requirement on the candidate. Any english-level match
# whose immediate context hits one of these is discarded.
_EN_FALSE_CONTEXT = re.compile(
    r"english\s+(?:page|version|translation|website|site|menu|subtitles?|"
    r"support\s+page|copy|text|ui|interface|manual|documentation|docs)\b|"
    r"(?:translated|available)\s+(?:in|into)\s+english|"
    r"this\s+(?:page|posting|description)\s+is\s+(?:in\s+)?english",
    re.IGNORECASE,
)


def _match(text: str, patterns: list[tuple[str, str]]) -> Optional[str]:
    if not text:
        return None
    s = text.lower()
    for pat, label in patterns:
        if re.search(pat, s):
            return label
    return None


def infer_jp_level(text: str) -> Optional[str]:
    return _match(text, JP_LEVEL_BODY_PATTERNS)


def infer_en_level(text: str) -> Optional[str]:
    """Conservative English-requirement inference from free text.

    Only explicit candidate-facing language counts. Returns one of the
    canonical level labels, "Preferred", "Not Required", or None (unknown).
    Window-based: each match is checked against false-positive contexts
    ("English version", "English translation", site chrome) before counting.
    """
    if not text:
        return None
    s = str(text).lower()

    def _clean_hit(pattern: str) -> bool:
        for m in re.finditer(pattern, s):
            window = s[max(0, m.start() - 40): m.end() + 40]
            if not _EN_FALSE_CONTEXT.search(window):
                return True
        return False

    # Explicit negations first.
    if _clean_hit(r"\benglish\s+(?:is\s+)?not\s+required\b|\bno\s+english\s+(?:is\s+)?(?:required|needed|necessary)\b"):
        return "Not Required"
    # Level-specific statements, strongest first.
    for pat, label in EN_LEVEL_BODY_PATTERNS:
        if _clean_hit(pat):
            return label
    # Generic requirement / preference, weakest signals last.
    if _clean_hit(r"\benglish\s+(?:skills?\s+|ability\s+|proficiency\s+)?(?:is\s+|are\s+)?required\b|"
                  r"\brequires?\s+english\b|\bmust\s+(?:be\s+able\s+to\s+)?(?:speak|read|write)\s+english\b"):
        return "Business / Professional"
    if _clean_hit(r"\benglish\s+(?:skills?\s+|ability\s+)?(?:is\s+)?(?:preferred|a\s+plus|advantageous|welcome|nice\s+to\s+have)\b"):
        return "Preferred"
    return None


# Standalone level string -> canonical label. Used when the source has already
# isolated the language (e.g. a metadata key like "Japanese Language Level"
# with a value like "Business level" or "N2") so we don't need the language
# word in the haystack.
def normalize_level_label(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    s = str(text).strip().lower()
    if re.search(r"\b(native|fluent)\b", s):              return "Native / Fluent"
    if re.search(r"\b(business|professional)\b", s):      return "Business / Professional"
    if re.search(r"\b(conversational|intermediate)\b", s): return "Conversational"
    if re.search(r"\b(basic|beginner|elementary)\b", s):  return "Basic / Beginner"
    if re.search(r"\bn1\b", s):                            return "Native / Fluent"
    if re.search(r"\bn2\b", s):                            return "Business / Professional"
    if re.search(r"\bn3\b", s):                            return "Conversational"
    if re.search(r"\b(n4|n5)\b", s):                       return "Basic / Beginner"
    if re.search(r"not\s+required|\bnone\b", s):           return "Not Required"
    return text.strip() or None


def infer_visa_sponsorship(text: str) -> Optional[int]:
    """1 = sponsor, 0 = explicitly NO sponsorship, None = unknown.

    Conservative on purpose: only explicit visa-sponsorship language counts.
    Relocation support is tracked separately (infer_relocation_support) and
    generic boilerplate like "status of residence" does NOT count — every
    Japanese job ad mentions residence status without implying sponsorship.
    """
    if not text:
        return None
    s = text.lower()
    if re.search(
        r"\bno\s+visa\s+sponsorship\b|\bvisa\s+sponsorship[:\s]*(?:no|not)\b|"
        r"\bno\s+sponsorship\b|\b(?:cannot|can\s*not|unable\s+to)\s+sponsor\b|"
        r"\bmust\s+(?:already\s+)?(?:have|hold|possess)\s+(?:a\s+)?valid\s+(?:work\s+)?visa\b|"
        r"\bno\s+visa\s+support\b",
        s,
    ):
        return 0
    if re.search(
        r"\bvisa\s+sponsorship\b|\bwill\s+sponsor\b|\bsponsorship\s+(?:is\s+)?available\b|"
        r"\bsponsor\s+(?:a\s+|your\s+)?(?:work\s+)?visa\b|\bvisa\s+support(?:ed)?\b|"
        r"\bsupport\s+(?:with|for)\s+(?:your\s+)?(?:work\s+)?visa\b|"
        r"\bwork\s+visa\s+(?:provided|arranged|obtained)\b|\bvisa\s+(?:acquisition|renewal)\s+support\b",
        s,
    ):
        return 1
    return None


def infer_remote(text: str) -> Optional[int]:
    """1 = remote OK, 0 = explicitly onsite-only, None = unknown."""
    if not text:
        return None
    s = text.lower()
    # Negative patterns first to take precedence.
    if re.search(r"\bno\s+remote\b|\bon[- ]?site\s+only\b|\bin[- ]?office\s+only\b|\bonsite\s+only\b", s):
        return 0
    if re.search(r"\bfully\s+remote\b|\bremote\s+ok\b|\bwork\s+from\s+home\b|\bremote\s+work\b|\bfully[- ]remote\b|\bremote[- ]first\b", s):
        return 1
    return None


# Japan-location detection: used to filter Greenhouse/Lever postings (which
# include worldwide jobs) down to Japan-relevant ones.
JAPAN_LOCATION_TOKENS = {
    # Country
    "japan", "jp", "日本",
    # Major cities
    "tokyo", "osaka", "kyoto", "yokohama", "nagoya", "fukuoka",
    "sapporo", "sendai", "kobe", "hiroshima", "kawasaki", "saitama",
    "chiba", "okinawa", "naha",
    # Tokyo wards / business hubs
    "shibuya", "shinjuku", "minato", "meguro", "setagaya",
    "shinagawa", "chiyoda", "chuo", "taito", "sumida",
    "roppongi", "akihabara", "ebisu", "marunouchi",
}


def is_japan_location(text: Optional[str], strict: bool = False) -> bool:
    """
    Check whether a location/country string indicates Japan.

    `strict=True` excludes the short 2-letter ISO code "jp" from accepted
    matches — strict mode demands an unambiguous human-readable signal
    ("Japan", "Tokyo", "Osaka", or a ward name).
    """
    if not text:
        return False
    s = str(text).lower()
    for token in JAPAN_LOCATION_TOKENS:
        if len(token) <= 2:
            # In strict mode, skip only the ASCII 2-letter tokens like "jp"
            # (could appear in noise like "jp-en"). 日本 is unambiguous,
            # keep it regardless.
            if strict and token.isascii():
                continue
            if re.search(rf"(?:^|[^a-z]){re.escape(token)}(?:$|[^a-z])", s):
                return True
        else:
            if token in s:
                return True
    return False


# Japanese-character detection: Hiragana, Katakana (full- and half-width),
# CJK Unified Ideographs (Kanji), and CJK Extension A. Used as a fallback
# Japan-relevance signal when explicit location/country are missing.
#
# Caveat: Kanji are shared with Chinese (and to a lesser extent Korean), so
# a kanji-only string can be a false positive for a Chinese-language posting.
# We accept that — this is only consulted when no other location data exists.
_JAPANESE_CHAR_RE = re.compile(
    "["
    "぀-ゟ"   # Hiragana          (e.g. ひらがな)
    "゠-ヿ"   # Katakana          (e.g. カタカナ)
    "ｦ-ﾟ"   # Halfwidth Katakana
    "一-鿿"   # CJK Unified Ideographs / Kanji
    "㐀-䶿"   # CJK Extension A
    "]"
)


def contains_japanese(text: Optional[str]) -> bool:
    """Return True if `text` contains any Hiragana, Katakana, or Kanji character."""
    if not text:
        return False
    return bool(_JAPANESE_CHAR_RE.search(str(text)))


# Inline char-range check used by `is_mostly_english`. Same ranges as
# _JAPANESE_CHAR_RE but as a function so we can count per-character without
# allocating a regex match object for every char.
def _is_japanese_char(c: str) -> bool:
    o = ord(c)
    return (
        0x3040 <= o <= 0x309F or   # Hiragana
        0x30A0 <= o <= 0x30FF or   # Katakana
        0xFF66 <= o <= 0xFF9F or   # Halfwidth Katakana
        0x4E00 <= o <= 0x9FFF or   # CJK Unified Ideographs (Kanji)
        0x3400 <= o <= 0x4DBF      # CJK Extension A
    )


def is_mostly_english(text: Optional[str], threshold: float = 0.6) -> bool:
    """
    Return True when `text` is predominantly written in English (Latin letters)
    rather than Japanese. The check ignores digits, punctuation, whitespace —
    only Latin letters and Japanese characters count toward the ratio.

        is_mostly_english("Senior Software Engineer")            -> True
        is_mostly_english("保育補助")                             -> False
        is_mostly_english("Senior Engineer | バイリンガル必要")  -> depends on ratio
        is_mostly_english("")                                     -> False

    `threshold=0.6` means at least 60% of the meaningful characters must be
    Latin letters. Tune higher (≥0.8) for "only English" or lower (≤0.4) to
    let in more bilingual postings.
    """
    if not text:
        return False
    latin = 0
    japanese = 0
    for ch in str(text):
        if ch.isascii() and ch.isalpha():
            latin += 1
        elif _is_japanese_char(ch):
            japanese += 1
    total = latin + japanese
    if total == 0:
        # No meaningful letters at all — symbols/digits only. Reject.
        return False
    return (latin / total) >= threshold


def english_ratio(text: Optional[str]) -> float:
    """Same scoring as is_mostly_english but returns the raw ratio (0.0–1.0).
    Returns 0.0 when there are no meaningful chars to score."""
    if not text:
        return 0.0
    latin = japanese = 0
    for ch in str(text):
        if ch.isascii() and ch.isalpha():
            latin += 1
        elif _is_japanese_char(ch):
            japanese += 1
    total = latin + japanese
    if total == 0:
        return 0.0
    return latin / total


# ===========================================================================
# Phase 1 derived-field helpers
# ===========================================================================

# Role-family taxonomy. Each family maps to a list of regex patterns that
# (case-insensitive) match in title or description. The family with the most
# matches wins; ties broken by list order.
_ROLE_FAMILY_PATTERNS: list[tuple[str, list[str]]] = [
    ("Software Engineering", [
        r"\bsoftware\s+engineer", r"\bbackend", r"\bfront[\s-]?end", r"\bfull[\s-]?stack",
        r"\bdeveloper\b", r"\bdevops\b", r"\bsre\b", r"\bsite reliability",
        r"\bplatform engineer", r"\bsystems engineer", r"\bprogrammer\b",
        r"\biOS\b", r"\bandroid\b", r"\bmobile engineer", r"\bembedded\b",
    ]),
    ("Data / AI", [
        r"\bdata\s+scientist", r"\bdata\s+engineer", r"\bdata\s+analyst",
        r"\bml\s+engineer", r"\bmachine\s+learning", r"\bai\s+engineer",
        r"\banalytics\b", r"\bllm\b", r"\bnlp\b", r"\bcomputer\s+vision",
    ]),
    ("Product Management", [
        r"\bproduct\s+manager", r"\bpm\b", r"\bpdm\b",
        r"\bproduct\s+owner", r"\bproduct\s+lead",
    ]),
    ("Design", [
        r"\bdesigner\b", r"\bux\b", r"\bui\b", r"\bui[\s/]+ux",
        r"\bproduct\s+design", r"\bvisual\s+design", r"\bgraphic\s+design",
        r"\binteraction\s+design",
    ]),
    ("Marketing", [
        r"\bmarketing\b", r"\bgrowth\b", r"\bseo\b", r"\bsem\b", r"\bcontent\b",
        r"\bbrand\b", r"\bsocial\s+media", r"\bperformance\s+marketing",
    ]),
    ("Sales / BD", [
        r"\bsales\b", r"\baccount\s+executive", r"\bbusiness\s+development",
        r"\b\s*bd\s*\b", r"\bsdr\b", r"\bbdr\b", r"\bsales\s+manager",
    ]),
    ("Finance / Accounting", [
        r"\bfinance\b", r"\baccountant\b", r"\baccounting\b", r"\bcfo\b",
        r"\bcontroller\b", r"\btreasur", r"\binvestment\b", r"\baudit\b",
    ]),
    ("Consulting", [
        r"\bconsultant\b", r"\bconsulting\b", r"\bstrateg(y|ist)\b",
        r"\badvisory\b", r"\bsenior\s+associate",
    ]),
    ("Operations", [
        r"\boperations\b", r"\bops\b", r"\bsupply\s+chain", r"\blogistics\b",
        r"\bproject\s+manager", r"\bprogram\s+manager",
    ]),
    ("HR / Recruiting", [
        r"\bhr\b", r"\bhuman\s+resources", r"\brecruit(er|ing|ment)\b",
        r"\btalent\s+(acquisition|partner)", r"\bpeople\s+ops",
    ]),
    ("Customer Support", [
        r"\bcustomer\s+(support|success|service)", r"\bsupport\s+engineer",
        r"\btechnical\s+support", r"\bhelp\s+desk", r"\bcs\b",
    ]),
    ("Teaching / Education", [
        r"\bteacher\b", r"\bteaching\b", r"\binstructor\b",
        r"\beikaiwa\b", r"\bcurriculum\b", r"\bprofessor\b", r"\btutor\b",
        r"\beslteacher\b", r"\besl\b", r"\balt\b", r"\bassistant\s+language",
    ]),
    ("Translation / Localization", [
        r"\btranslator\b", r"\btranslation\b", r"\blocalization\b",
        r"\binterpret(er|ation)\b", r"\bi18n\b", r"\bl10n\b",
    ]),
    ("Hospitality / Tourism", [
        r"\bhotel\b", r"\bhospitality\b", r"\btourism\b", r"\bconcierge\b",
        r"\brestaurant\b", r"\bchef\b", r"\bfront\s+desk", r"\btravel\b",
    ]),
    ("Legal / Compliance", [
        r"\blegal\b", r"\blawyer\b", r"\battorney\b", r"\bparalegal\b",
        r"\bcompliance\b", r"\bgovernance\b",
    ]),
]


def classify_role_family(title: Optional[str], description: Optional[str]) -> Optional[str]:
    """Best-effort taxonomy mapping. Returns None when no signal matches."""
    if not title and not description:
        return None
    text = ((title or "") + "  " + (description or "")).lower()
    best_family = None
    best_count = 0
    for family, patterns in _ROLE_FAMILY_PATTERNS:
        count = sum(1 for p in patterns if re.search(p, text))
        if count > best_count:
            best_count = count
            best_family = family
    return best_family


# Posting language: English / Mixed / Japanese / Unknown — based on
# english_ratio thresholds AND minimum char counts so very short titles
# without descriptions don't get a confident label.
def detect_posting_language(title: Optional[str],
                            description: Optional[str]) -> str:
    combined = ((title or "") + "  " + (description or ""))
    meaningful = sum(1 for ch in combined
                     if (ch.isascii() and ch.isalpha()) or _is_japanese_char(ch))
    if meaningful < 20:
        return "Unknown"
    r = english_ratio(combined)
    if r >= 0.70:
        return "English"
    if r >= 0.35:
        return "Mixed"
    return "Japanese"


def _lang_counts(text: Optional[str]) -> tuple[int, int]:
    """(latin_letters, japanese_chars) in text."""
    latin = japanese = 0
    for ch in (text or ""):
        if ch.isascii() and ch.isalpha():
            latin += 1
        elif _is_japanese_char(ch):
            japanese += 1
    return latin, japanese


def classify_posting_language(title: Optional[str],
                              description: Optional[str],
                              requirements: Optional[str] = None) -> str:
    """Section-aware posting-language classifier.

    Evaluates title, the requirements section, and the main body separately,
    discounting the tail of the description (where boilerplate/footer text —
    often the only English on a Japanese posting — tends to live).

    Returns: "English" | "Japanese" | "Bilingual" | "Mixed" | "Unknown".

      English   — what the candidate must read is (almost) all English.
      Japanese  — title + requirements + body lead are Japanese; an
                  English footer does NOT rescue a posting.
      Bilingual — substantial full text in BOTH languages (e.g. the posting
                  is duplicated EN + JP), neither merely decorative.
      Mixed     — genuinely interleaved, no clear winner. Lower confidence.
    """
    title = title or ""
    desc = description or ""
    reqs = requirements or ""

    # Body lead vs tail: the last 25% of a long description is most likely
    # company boilerplate / application instructions / footer chrome.
    if len(desc) > 400:
        cut = int(len(desc) * 0.75)
        body_lead, body_tail = desc[:cut], desc[cut:]
    else:
        body_lead, body_tail = desc, ""

    core = title + "  " + reqs + "  " + body_lead   # what the candidate must read
    core_latin, core_jp = _lang_counts(core)
    meaningful = core_latin + core_jp
    if meaningful < 20:
        return "Unknown"

    core_r  = core_latin / meaningful
    title_r = english_ratio(title) if _lang_counts(title) != (0, 0) else None
    req_r   = english_ratio(reqs)  if _lang_counts(reqs)  != (0, 0) else None

    # Clear single-language cases on the core text.
    if core_r >= 0.85:
        return "English"
    if core_r <= 0.10:
        return "Japanese"

    # Requirements mostly English is a strong English-friendly signal —
    # the section that gates the candidate is readable.
    if req_r is not None and req_r >= 0.70 and core_r >= 0.45:
        return "English"

    # Title AND requirements Japanese -> Japanese, regardless of an English
    # tail/footer. (Footer-only English must not flatter a posting.)
    if (title_r is not None and title_r <= 0.30) and \
       (req_r is None or req_r <= 0.30) and core_r <= 0.45:
        return "Japanese"

    # Bilingual: substantial full text in BOTH languages. Checked over the
    # whole posting (a duplicated EN+JP body often puts the second language
    # in the tail) — but only after the Japanese guard above, so a long
    # English footer can't flatter a Japanese posting into "Bilingual".
    full_latin, full_jp = _lang_counts(title + "  " + reqs + "  " + desc)
    if full_latin >= 200 and full_jp >= 200 and \
       0.20 <= full_latin / max(1, full_latin + full_jp) <= 0.80:
        return "Bilingual"

    # English body with a Japanese-ish remainder, or vice versa.
    if core_r >= 0.70:
        return "English"
    if core_r <= 0.20:
        return "Japanese"
    return "Mixed"


# Visa-support and relocation-support: extend the existing visa-sponsorship
# inference with additional patterns. Returns 1 / 0 / None.
def infer_visa_support(text: Optional[str]) -> Optional[int]:
    return infer_visa_sponsorship(text)


_RELOCATION_POS = re.compile(
    r"\brelocation\s+(?:support|assistance|package|allowance|paid|provided)\b|"
    r"\bwe\s+(?:will\s+)?(?:provide|cover|pay\s+for)\s+relocation\b|"
    r"\brelocation\s+covered\b",
    re.IGNORECASE,
)


def infer_relocation_support(text: Optional[str]) -> Optional[int]:
    if not text:
        return None
    # Negative patterns take precedence so "No relocation support" reads as 0,
    # not 1 (otherwise the positive "relocation support" pattern fires first).
    if re.search(r"\bno\s+relocation\b", text, re.IGNORECASE):
        return 0
    if _RELOCATION_POS.search(text):
        return 1
    return None


# Source-quality mapping. Higher is better.
_SOURCE_QUALITY: dict[str, str] = {
    "greenhouse":      "Direct ATS",
    "lever":           "Direct ATS",
    "ashby":           "Direct ATS",
    "workable":        "Direct ATS",
    "smartrecruiters": "Direct ATS",
    "recruitee":       "Direct ATS",
    "tokyodev":        "Curated",
    "japandev":        "Curated",
    "gaijinpot":       "Job board",
    "jobsinjapan":     "Job board",
    "careercross":     "Job board",
    "yolo japan":      "Job board",
    "yolojapan":       "Job board",
    "robertwalters":   "Recruiter",
    "jobspy":          "Aggregator",
}


def source_quality(source: Optional[str]) -> str:
    if not source:
        return "Unknown"
    key = str(source).lower().strip()
    return _SOURCE_QUALITY.get(key, _SOURCE_QUALITY.get(key.replace(" ", ""), "Unknown"))


# Numeric weight per tier — used in the recommended-sort score.
_SOURCE_QUALITY_WEIGHT = {
    "Direct ATS":           1.0,
    "Direct from employer": 1.0,
    "Curated":              0.9,
    "Recruiter":            0.8,
    "Job board":            0.7,
    "Aggregator":           0.5,
    "Unknown":              0.4,
}


def source_quality_weight(quality: Optional[str]) -> float:
    return _SOURCE_QUALITY_WEIGHT.get(quality or "", 0.4)


# ===========================================================================
# Data-quality score (0–100)
# ===========================================================================
def calculate_data_quality(job: dict) -> int:
    """Reward jobs that have the fields foreigners actually need to decide
    whether to apply. Pure rule-based — no AI."""
    score = 0
    if (job.get("title") or "").strip():
        score += 15
    desc = (job.get("description") or "").strip()
    if desc:
        score += 25 if len(desc) > 200 else 10
    if (job.get("salary") or "").strip() or job.get("salary_min_jpy"):
        score += 15
    if (job.get("location") or "").strip():
        score += 10
    if (job.get("company_name") or "").strip():
        score += 10
    if job.get("post_date"):
        score += 10
    if job.get("japanese_level"):
        score += 5
    if job.get("english_level"):
        score += 5
    if (job.get("url") or "").strip():
        score += 5
    return min(100, score)


# ===========================================================================
# Foreigner Fit score (0–100) with reason tags
# ===========================================================================
# A row's foreigner-fit score is the sum of weighted signals capped at 0..100.
# `reasons` is a comma-separated string surfaced in the UI.
_JP_LEVEL_NEGATIVE = {"Native / Fluent", "Business / Professional"}
_JP_LEVEL_NEUTRAL  = {"Conversational"}
_JP_LEVEL_POSITIVE = {"Basic / Beginner", "Not Required"}


def calculate_foreigner_fit(job: dict) -> tuple[int, list[str]]:
    """
    Compute the 0–100 score AND a list of human-readable reason tags.
    Pure rule-based to keep it predictable.

    Positive signals (add):
      +20  posting mostly in English
      +20  Japanese not required / basic only
      +15  apply from abroad
      +15  visa sponsorship / relocation support
      +10  salary present
      +10  remote or hybrid available
      +5   source is direct ATS
      +5   recent posting (post_date or last_seen within 30 days)

    Negative signals (subtract):
      -20  posting predominantly Japanese
      -15  no location data
      -15  salary missing
      -20  no description

    Final result clamped to 0..100. Reasons returned in order they applied.
    """
    score = 0
    reasons: list[str] = []

    pl = job.get("posting_language") or detect_posting_language(
        job.get("title"), job.get("description"))
    if pl == "English":
        score += 20; reasons.append("english_posting")
    elif pl == "Bilingual":
        score += 15; reasons.append("bilingual_posting")
    elif pl == "Japanese":
        score -= 20; reasons.append("japanese_heavy_posting")

    jp_level = job.get("japanese_level") or ""
    if jp_level in _JP_LEVEL_POSITIVE or "not required" in jp_level.lower():
        score += 20; reasons.append("no_japanese_required")
    elif jp_level in _JP_LEVEL_NEGATIVE:
        # Don't subtract here — already implicit in language signal;
        # but document it as a reason so the UI can show it.
        reasons.append("japanese_required")
    elif jp_level in _JP_LEVEL_NEUTRAL:
        score += 5; reasons.append("conversational_japanese")

    if job.get("overseas_application_ok") == 1:
        score += 15; reasons.append("apply_from_abroad")

    visa = job.get("visa_sponsorship_mentioned")
    reloc = job.get("relocation_support_mentioned")
    if visa == 1 or reloc == 1:
        score += 15; reasons.append("visa_or_relocation_support")
    elif visa == 0:
        # Posting explicitly says NO sponsorship — fine for residents,
        # a hard blocker for applicants who need a visa.
        score -= 10; reasons.append("no_visa_sponsorship")

    salary_present = bool((job.get("salary") or "").strip()
                          or job.get("salary_min_jpy"))
    if salary_present:
        score += 10; reasons.append("salary_listed")
    else:
        score -= 15; reasons.append("salary_missing")

    if job.get("remote_work_ok") == 1:
        score += 10; reasons.append("remote_or_hybrid")

    sq = job.get("source_quality") or source_quality(job.get("source"))
    if sq == "Direct ATS":
        score += 5; reasons.append("direct_source")
    elif sq == "Curated":
        score += 3; reasons.append("curated_source")
    elif sq == "Aggregator":
        # No subtraction — but signals lower trust.
        reasons.append("aggregator_source")

    # Freshness
    last_seen = job.get("last_seen_at") or ""
    post_date = job.get("post_date") or ""
    fresh_signal = post_date or last_seen
    if fresh_signal:
        try:
            from datetime import datetime, timezone, timedelta
            d = datetime.fromisoformat(fresh_signal.replace("Z", "+00:00"))
            if d.tzinfo is None:
                d = d.replace(tzinfo=timezone.utc)
            if (datetime.now(timezone.utc) - d) <= timedelta(days=30):
                score += 5; reasons.append("recent_posting")
        except (ValueError, TypeError):
            pass

    if not (job.get("location") or "").strip():
        score -= 15; reasons.append("no_location")
    if not (job.get("description") or "").strip():
        score -= 20; reasons.append("no_description")

    score = max(0, min(100, score))
    return score, reasons


# ---------------------------------------------------------------------------
# Location normalization
# ---------------------------------------------------------------------------
# Raw location strings from aggregators are wildly inconsistent: "Tokyo, Japan",
# "Tokyo, Japan / Tokyo", "港区, Tokyo, Japan", "All Kanto, Tokyo, Japan", etc.
# We collapse each to a canonical prefecture so filtering/faceting works. The
# 47 prefectures, plus a "Remote / Anywhere" and "Other / Japan" bucket.

# Each prefecture maps to a list of lowercase substrings that imply it. Order
# matters: we check the more specific prefectures' tokens first, but since each
# token list is prefecture-specific, simple membership is enough.
_PREFECTURE_TOKENS: list[tuple[str, tuple[str, ...]]] = [
    ("Tokyo",      ("tokyo", "東京", "shibuya", "shinjuku", "minato", "chiyoda",
                    "setagaya", "bunkyo", "chuo", "shinagawa", "meguro", "ota-ku",
                    "adachi", "kita-ward", "kita-ku", "koto", "江東", "港区", "渋谷",
                    "新宿", "ebisu", "kiba", "fuchu", "ginza", "akihabara")),
    ("Osaka",      ("osaka", "大阪", "umeda", "namba", "fujiidera", "hirakata")),
    ("Kanagawa",   ("kanagawa", "神奈川", "yokohama", "kawasaki", "fujisawa",
                    "kamakura", "sagamihara")),
    ("Aichi",      ("aichi", "愛知", "nagoya", "名古屋", "toyota")),
    ("Hyogo",      ("hyogo", "兵庫", "kobe", "神戸", "himeji")),
    ("Kyoto",      ("kyoto", "京都", "higashiyama")),
    ("Fukuoka",    ("fukuoka", "福岡", "hakata")),
    ("Hokkaido",   ("hokkaido", "北海道", "sapporo", "札幌")),
    ("Chiba",      ("chiba", "千葉", "funabashi", "narita")),
    ("Saitama",    ("saitama", "埼玉", "omiya", "kawagoe")),
    ("Gunma",      ("gunma", "群馬", "takasaki", "maebashi")),
    ("Ibaraki",    ("ibaraki", "茨城", "tsukuba", "mito")),
    ("Tochigi",    ("tochigi", "栃木", "utsunomiya")),
    ("Shizuoka",   ("shizuoka", "静岡", "hamamatsu")),
    ("Hiroshima",  ("hiroshima", "広島")),
    ("Miyagi",     ("miyagi", "宮城", "sendai", "仙台")),
    ("Niigata",    ("niigata", "新潟")),
    ("Nagano",     ("nagano", "長野", "matsumoto")),
    ("Okinawa",    ("okinawa", "沖縄", "naha")),
    ("Nara",       ("nara", "奈良")),
    ("Mie",        ("mie", "三重", "yokkaichi")),
    ("Gifu",       ("gifu", "岐阜")),
    ("Okayama",    ("okayama", "岡山")),
    ("Kumamoto",   ("kumamoto", "熊本")),
    ("Kagoshima",  ("kagoshima", "鹿児島")),
    ("Ishikawa",   ("ishikawa", "石川", "kanazawa")),
    ("Toyama",     ("toyama", "富山")),
    ("Fukui",      ("fukui", "福井")),
    ("Yamanashi",  ("yamanashi", "山梨")),
    ("Wakayama",   ("wakayama", "和歌山")),
    ("Shiga",      ("shiga", "滋賀")),
    ("Ehime",      ("ehime", "愛媛", "matsuyama")),
    ("Kagawa",     ("kagawa", "香川", "takamatsu")),
    ("Tokushima",  ("tokushima", "徳島")),
    ("Kochi",      ("kochi", "高知")),
    ("Oita",       ("oita", "大分")),
    ("Nagasaki",   ("nagasaki", "長崎")),
    ("Saga",       ("saga", "佐賀")),
    ("Miyazaki",   ("miyazaki", "宮崎")),
    ("Yamaguchi",  ("yamaguchi", "山口")),
    ("Shimane",    ("shimane", "島根")),
    ("Tottori",    ("tottori", "鳥取")),
    ("Yamagata",   ("yamagata", "山形")),
    ("Akita",      ("akita", "秋田")),
    ("Iwate",      ("iwate", "岩手", "morioka")),
    ("Aomori",     ("aomori", "青森")),
    ("Fukushima",  ("fukushima", "福島", "koriyama")),
]

# Region groupings (used for "All Kanto", "Nationwide", etc. and for browse UI).
REGIONS: dict[str, tuple[str, ...]] = {
    "Kanto":    ("Tokyo", "Kanagawa", "Chiba", "Saitama", "Gunma", "Ibaraki",
                 "Tochigi"),
    "Kansai":   ("Osaka", "Kyoto", "Hyogo", "Nara", "Shiga", "Wakayama", "Mie"),
    "Chubu":    ("Aichi", "Shizuoka", "Nagano", "Niigata", "Ishikawa", "Toyama",
                 "Fukui", "Yamanashi", "Gifu"),
    "Tohoku":   ("Miyagi", "Fukushima", "Yamagata", "Akita", "Iwate", "Aomori"),
    "Chugoku":  ("Hiroshima", "Okayama", "Yamaguchi", "Shimane", "Tottori"),
    "Shikoku":  ("Ehime", "Kagawa", "Tokushima", "Kochi"),
    "Kyushu":   ("Fukuoka", "Kumamoto", "Kagoshima", "Nagasaki", "Saga",
                 "Miyazaki", "Oita"),
    "Hokkaido": ("Hokkaido",),
    "Okinawa":  ("Okinawa",),
}


def normalize_prefecture(location: Optional[str]) -> Optional[str]:
    """
    Collapse a raw location string to a single canonical Japanese prefecture.

    Returns the prefecture name (e.g. "Tokyo"), or "Remote / Anywhere" for
    nationwide/remote signals, or "Other / Japan" when it's clearly a Japan
    posting we can't pin down, or None when there's no usable signal.

    Where a string names multiple prefectures (e.g. a multi-city posting), the
    FIRST prefecture matched in _PREFECTURE_TOKENS order wins, which biases
    toward the major metros foreigners search for.
    """
    if not location:
        return None
    s = str(location).lower()

    # Nationwide / remote signals → a single anywhere bucket.
    if any(t in s for t in ("nationwide", "anywhere", "all japan", "remote",
                            "全国", "japan locations")):
        # But if a concrete prefecture is also named, prefer it below.
        anywhere = True
    else:
        anywhere = False

    for pref, tokens in _PREFECTURE_TOKENS:
        for tok in tokens:
            if tok.isascii():
                # Word-ish boundary for short ascii tokens to avoid noise.
                if re.search(rf"(?:^|[^a-z]){re.escape(tok)}(?:$|[^a-z])", s):
                    return pref
            elif tok in s:
                return pref

    if anywhere:
        return "Remote / Anywhere"

    # "Japan (inferred)", "Japan", bare 日本 → generic bucket.
    if is_japan_location(location):
        return "Other / Japan"
    return None


def region_for_prefecture(pref: Optional[str]) -> Optional[str]:
    """Map a canonical prefecture to its region (Kanto, Kansai, …)."""
    if not pref:
        return None
    for region, prefs in REGIONS.items():
        if pref in prefs:
            return region
    return None


def foreigner_fit_label(score: Optional[int]) -> str:
    if score is None:
        return "Unscored"
    if score >= 90: return "Excellent"
    if score >= 75: return "Strong"
    if score >= 60: return "Possible"
    if score >= 40: return "Weak"
    return "Poor"


# Human-readable mapping of reason codes → short user-facing labels.
FIT_REASON_LABELS = {
    "english_posting":           "Posting is mostly English",
    "bilingual_posting":         "Posting in both English and Japanese",
    "japanese_heavy_posting":    "Posting is mostly Japanese",
    "no_japanese_required":      "No Japanese required",
    "japanese_required":         "Japanese proficiency required",
    "conversational_japanese":   "Conversational Japanese expected",
    "apply_from_abroad":         "Apply from abroad",
    "visa_or_relocation_support":"Visa or relocation support mentioned",
    "no_visa_sponsorship":       "Explicitly no visa sponsorship",
    "salary_listed":             "Salary listed",
    "salary_missing":            "Salary not listed",
    "remote_or_hybrid":          "Remote or hybrid OK",
    "direct_source":             "Direct company ATS",
    "curated_source":            "Curated source",
    "aggregator_source":         "Aggregator source — verify at original page",
    "recent_posting":            "Recently posted",
    "no_location":               "Location not stated",
    "no_description":            "No description",
}
