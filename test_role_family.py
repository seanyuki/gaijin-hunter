"""Eval harness for inference.classify_role_family.

A small labelled set of (title, expected_family) cases that pins down the
classifier's behaviour and guards against regressions when the patterns are
tuned. `None` means "should not be confidently classified into the white-collar
taxonomy" (e.g. generic blue-collar postings that get a source category instead).

Run: pytest test_role_family.py -q
"""
from inference import classify_role_family

# (title, expected_family)
CASES: list[tuple[str, str | None]] = [
    # --- clear, title-driven ---
    ("Senior Software Engineer (Ruby)", "Software Engineering"),
    ("Full-Stack Developer", "Software Engineering"),
    ("Backend Engineer, Platform", "Software Engineering"),
    ("Site Reliability Engineer", "Software Engineering"),
    ("QA Automation Engineer", "Software Engineering"),
    ("Data Scientist, Recommendations", "Data / AI"),
    ("Machine Learning Engineer", "Data / AI"),
    ("Data Engineer (Spark / dbt)", "Data / AI"),
    ("Product Manager, Payments", "Product Management"),
    ("Senior Product Designer", "Design"),
    ("UX/UI Designer", "Design"),
    ("Performance Marketing Manager", "Marketing"),
    ("SEO Content Strategist", "Marketing"),
    ("Account Executive (SaaS)", "Sales / BD"),
    ("Sales Manager, Enterprise", "Sales / BD"),
    ("Business Development Representative", "Sales / BD"),
    ("Financial Controller", "Finance / Accounting"),
    ("Senior Accountant", "Finance / Accounting"),
    ("Management Consultant", "Consulting"),
    ("Supply Chain Operations Lead", "Operations"),
    ("Technical Recruiter", "HR / Recruiting"),
    ("Talent Acquisition Partner", "HR / Recruiting"),
    ("Recruitment Consultant (Bilingual Desk)", "HR / Recruiting"),
    ("Customer Success Manager", "Customer Support"),
    ("Full-Time English Teacher", "Teaching / Education"),
    ("ALT - Assistant Language Teacher", "Teaching / Education"),
    ("Japanese-English Translator", "Translation / Localization"),
    ("Hotel Front Desk Associate", "Hospitality / Tourism"),
    ("Legal Counsel, APAC", "Legal / Compliance"),

    # --- regressions / disambiguation (the bugs we set out to fix) ---
    # "recruiting" is the hiring verb here; the role is teaching.
    ("Now recruiting for mid hire ALT positions in Kyushu", "Teaching / Education"),
    # "Sales Engineer" is a sales role, not SWE.
    ("Sales Engineer", "Sales / BD"),

    # --- Japanese titles ---
    ("営業マネージャー（法人向け）", "Sales / BD"),
    ("経理スタッフ", "Finance / Accounting"),
    ("データサイエンティスト", "Data / AI"),
    ("英会話講師", "Teaching / Education"),
    ("人事・採用担当", "HR / Recruiting"),
    ("Webデザイナー", "Design"),

    # --- should NOT confidently classify into the white-collar taxonomy ---
    ("Warehouse Picker / Packer", None),
    ("Convenience Store Staff", None),
    ("Construction Site Helper", None),
]


def test_classifier_accuracy():
    wrong = []
    for title, expected in CASES:
        got = classify_role_family(title, None)
        if got != expected:
            wrong.append((title, expected, got))
    acc = 1 - len(wrong) / len(CASES)
    # Print a readable failure report when below target.
    msg = "\n".join(f"  {t!r}: expected {e!r}, got {g!r}" for t, e, g in wrong)
    assert acc >= 0.90, f"role-family accuracy {acc:.0%} ({len(wrong)} wrong):\n{msg}"


def test_recruiting_verb_does_not_become_hr():
    # The specific bug: a teaching job advertised with "recruiting" must not be HR.
    assert classify_role_family(
        "Now recruiting for mid hire ALT positions", None) == "Teaching / Education"


def test_title_outweighs_body_keywords():
    # A marketing role whose body mentions an engineering manager stays Marketing.
    title = "Marketing Manager, Growth"
    body = "You'll work closely with our engineering manager and the software team."
    assert classify_role_family(title, body) == "Marketing"


def test_low_signal_returns_none():
    # A single broad body keyword is not enough for a confident label.
    assert classify_role_family("General Staff", "Light work in a busy team.") is None


def test_tags_meta_signal():
    # Structured tags carry signal even when the title is generic.
    assert classify_role_family("Engineer", None, tags="backend, python, aws") == "Software Engineering"
