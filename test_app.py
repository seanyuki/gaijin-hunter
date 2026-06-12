"""
Lightweight smoke + unit tests. Run with:  python test_app.py
(no pytest dependency required; uses the live jobs.db read-only)
"""

from __future__ import annotations

import sys

failures = []


def check(name: str, cond: bool, detail: str = ""):
    status = "ok " if cond else "FAIL"
    print(f"  [{status}] {name}" + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        failures.append(name)
    # Real assertion so `pytest -q` actually fails on regressions. The
    # __main__ runner catches it to keep printing the rest of the suite.
    assert cond, f"{name} {detail}".strip()


def test_inference():
    import inference as inf
    print("inference:")
    check("visa: explicit yes", inf.infer_visa_sponsorship("We offer visa sponsorship") == 1)
    check("visa: visa support", inf.infer_visa_sponsorship("Visa support available") == 1)
    check("visa: explicit no", inf.infer_visa_sponsorship("No visa sponsorship offered") == 0)
    check("visa: must have visa", inf.infer_visa_sponsorship("Must have valid work visa") == 0)
    check("visa: residence boilerplate is NOT support",
          inf.infer_visa_sponsorship("Status of residence: Specified Skilled Worker") is None)
    check("visa: relocation is NOT visa",
          inf.infer_visa_sponsorship("Relocation assistance provided") is None)
    check("reloc: positive", inf.infer_relocation_support("Relocation assistance provided") == 1)
    check("level: None -> Not Required", inf.normalize_level_label("None") == "Not Required")
    check("level: Fluent Japanese", inf.normalize_level_label("Fluent Japanese") == "Native / Fluent")
    check("level: N2", inf.normalize_level_label("N2") == "Business / Professional")
    check("source quality: YOLO Japan", inf.source_quality("YOLO Japan") == "Job board")
    check("source quality: japandev", inf.source_quality("japandev") == "Curated")
    check("source quality: ashby", inf.source_quality("ashby") == "Direct ATS")
    score, reasons = inf.calculate_foreigner_fit({
        "title": "Software Engineer", "description": "x" * 300,
        "posting_language": "English", "japanese_level": "Not Required",
        "salary": "¥8M", "location": "Tokyo", "visa_sponsorship_mentioned": 1,
    })
    check("fit: strong profile scores >= 60", score >= 60, str(score))
    check("fit: reasons include visa", "visa_or_relocation_support" in reasons)
    score2, reasons2 = inf.calculate_foreigner_fit({
        "title": "Engineer", "description": "x" * 300, "location": "Tokyo",
        "salary": "¥6M", "visa_sponsorship_mentioned": 0,
    })
    check("fit: explicit no-visa penalized", "no_visa_sponsorship" in reasons2)


def test_en_level_inference():
    import inference as inf
    print("english-level inference (conservative):")
    check("native english", inf.infer_en_level("Native English speaker required") == "Native / Fluent")
    check("business english", inf.infer_en_level("Business English is a must") == "Business / Professional")
    check("conversational", inf.infer_en_level("Conversational English needed") == "Conversational")
    check("english required -> business", inf.infer_en_level("English required for this role") == "Business / Professional")
    check("english preferred", inf.infer_en_level("English skills preferred") == "Preferred")
    check("english not required", inf.infer_en_level("English is not required") == "Not Required")
    check("'English version' is NOT a requirement", inf.infer_en_level("See the English version of this page") is None)
    check("'English translation' ignored", inf.infer_en_level("English translation available on request") is None)
    check("'available in English' ignored", inf.infer_en_level("Menu available in English") is None)
    check("no signal -> None", inf.infer_en_level("Great team, free lunch, flexible hours") is None)


def test_posting_language():
    import inference as inf
    print("posting-language classifier:")
    en_text = "We are looking for a backend engineer to join our platform team. " * 8
    jp_text = "当社ではバックエンドエンジニアを募集しています。開発チームに参加してください。" * 8
    check("pure english", inf.classify_posting_language("Backend Engineer", en_text, "5 years Python") == "English")
    check("pure japanese", inf.classify_posting_language("エンジニア募集", jp_text, "Python経験5年以上") == "Japanese")
    check("english footer does not rescue japanese posting",
          inf.classify_posting_language("エンジニア募集", jp_text + " " +
              "Apply now. Equal opportunity employer. Privacy policy available in English.",
              "日本語ネイティブ") in ("Japanese", "Mixed"))
    check("bilingual duplicate posting",
          inf.classify_posting_language("Engineer / エンジニア", en_text + jp_text, None) == "Bilingual")
    check("english requirements lift mixed body",
          inf.classify_posting_language("Engineer", en_text + jp_text[:120],
              "5+ years of Python. Fluent English. Experience with AWS and Docker required.") in ("English", "Bilingual"))
    check("too short -> Unknown", inf.classify_posting_language("abc", "", None) == "Unknown")


def test_salary_extraction():
    import salary_parser as sp
    print("salary text extraction (conservative):")
    cases = [
        ("Salary: ¥6M - ¥10M DOE", (6000000, 10000000, "Year")),
        ("年収600万円〜1,000万円", (6000000, 10000000, "Year")),
        ("月給30万円", (300000, 300000, "Month")),
        ("時給1,500円", (1500, 1500, "Hour")),
        ("¥7,000,000 ~ ¥9,000,000 / year", (7000000, 9000000, "Year")),
        ("$120K per year", (18000000, 18000000, "Year")),
        ("We have 6,000,000 users", None),
        ("10+ years of experience", None),
        ("Founded 1999 with 2,000,000 yen capital revenue", None),
        ("Competitive salary", None),
    ]
    for text, want in cases:
        r = sp.extract_from_text(text)
        got = (r["salary_min_jpy"], r["salary_max_jpy"], r["salary_period"]) if r else None
        check(f"extract {text[:30]!r}", got == want, str(got))


def test_only_ids():
    import db
    print("only_ids (saved/applied) queries:")
    rows = db.query_jobs(limit=3)
    ids = [r["id"] for r in rows]
    sub = db.query_jobs(only_ids=ids, limit=25)
    check("only requested ids returned", {r["id"] for r in sub} <= set(ids) and len(sub) == 3)
    check("count matches", db.count_jobs(only_ids=ids) == 3)
    check("empty ids -> zero", db.count_jobs(only_ids=[]) == 0)


def test_provenance():
    import db
    print("provenance:")
    with db.connect() as conn:
        n = conn.execute("SELECT COUNT(*) FROM jobs WHERE visa_source IS NULL").fetchone()[0]
        check("all rows have visa provenance", n == 0, str(n))
        bad = conn.execute(
            "SELECT COUNT(*) FROM jobs WHERE visa_source NOT IN ('explicit','inferred','not_stated')"
        ).fetchone()[0]
        check("vocabulary respected", bad == 0, str(bad))
        # not_stated must mean the value is actually absent
        mism = conn.execute(
            "SELECT COUNT(*) FROM jobs WHERE japanese_level_source='not_stated' "
            "AND japanese_level IS NOT NULL AND japanese_level != ''"
        ).fetchone()[0]
        check("not_stated consistent with values", mism == 0, str(mism))


def test_yolo_classify():
    import yolojapan_scraper as yj
    print("yolojapan classify:")
    c = yj.classify("Ramen shop STAFF", "medical checkup provided, hospital nearby",
                    "Food and beverage / Ramen", "Part-time")
    check("ramen != care_work", c["category"] == "hospitality", c["category"])
    c = yj.classify("4 ton driver job", "no experience welcome",
                    "Light work, logistics, and drivers / Driver", "Full-time employee")
    check("driver -> warehouse/logistics", c["category"] == "warehouse_factory", c["category"])
    c = yj.classify("Nursing staff recruitment", "",
                    "Healthcare, welfare, and caregiving / Care home", None)
    check("nursing -> care_work", c["category"] == "care_work", c["category"])
    c = yj.classify("Web engineer", "", "IT and communications / Web", "Full-time employee")
    check("web engineer -> tech", c["category"] == "tech", c["category"])
    check("part-time flag", yj.classify("X", "part-time ok", "", "Part-time")["is_part_time"])


def test_db_queries():
    import db
    print("db queries:")
    total = db.count_jobs()
    check("active jobs > 0", total > 0, str(total))
    prof = db.count_jobs(professional_only=True)
    check("professional subset", 0 < prof < total, f"{prof}/{total}")
    rows = db.query_jobs(professional_only=True, limit=50)
    check("professional excludes part-time",
          all((r["employment_terms"] or "") not in ("Part-time", "Temporary") for r in rows))
    check("professional excludes service families",
          all((r["role_family"] or "") not in db.SERVICE_ROLE_FAMILIES for r in rows))
    rows = db.query_jobs(filters={"japanese_level": ["Not Required"]}, limit=50)
    check("jp filter exact", all(r["japanese_level"] == "Not Required" for r in rows)
          and len(rows) > 0, str(len(rows)))
    rows = db.query_jobs(flags={"visa_sponsorship_mentioned": True}, limit=50)
    check("visa flag filter", all(r["visa_sponsorship_mentioned"] == 1 for r in rows))
    rows = db.query_jobs(salary_min=8_000_000, limit=50)
    check("salary floor", all(
        (r["salary_max_annual_jpy"] or r["salary_min_annual_jpy"] or 0) >= 8_000_000
        for r in rows))
    rows = db.query_jobs(sort="recommended", limit=10)
    check("recommended sort runs", len(rows) > 0)
    # No YOLO part-time service job should outrank everything
    check("top recommended not part-time service",
          (rows[0]["employment_terms"] or "") != "Part-time", rows[0]["employment_terms"])


def test_upsert_not_null_defaults():
    """Regression: production scrape failed with `NOT NULL constraint failed:
    jobs.is_employer_post` for every scraper that didn't set the field
    explicitly (the INSERT names all columns, so SQL DEFAULTs never apply).
    Runs against a fresh schema in a temp DB — exactly the production case."""
    import importlib
    import os
    import tempfile

    print("upsert NOT NULL defaults (fresh schema, temp db):")
    fd, tmp = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    old = os.environ.get("JAPAN_JOBS_DB")
    os.environ["JAPAN_JOBS_DB"] = tmp
    import db
    importlib.reload(db)
    try:
        db.init_db()
        # 1) minimal scraped job — no is_employer_post / scraped_at / last_seen_at
        with db.connect() as conn:
            res = db.upsert_job(conn, {
                "source": "gaijinpot", "url": "https://example.com/job/1",
                "title": "Software Engineer", "company_name": "Example KK",
            })
            conn.commit()
        check("scraped job without is_employer_post inserts", res == "inserted", res)
        with db.connect() as conn:
            row = conn.execute("SELECT * FROM jobs WHERE url = ?",
                               ("https://example.com/job/1",)).fetchone()
        check("is_employer_post defaults to 0", row["is_employer_post"] == 0,
              str(row["is_employer_post"]))
        check("scraped_at auto-filled", bool(row["scraped_at"]))
        check("last_seen_at auto-filled", bool(row["last_seen_at"]))
        # 2) re-upsert (update path) must also survive missing fields
        with db.connect() as conn:
            res = db.upsert_job(conn, {
                "source": "gaijinpot", "url": "https://example.com/job/1",
                "title": "Software Engineer II", "company_name": "Example KK",
            })
            conn.commit()
        check("update path works without is_employer_post", res == "updated", res)
        # 3) employer post keeps is_employer_post = 1
        post = db.create_employer_post({
            "title": "Bilingual PM", "company_name": "Hiring Co",
            "description": "A real description of the role.",
            "location": "Tokyo", "employer_contact_email": "hr@example.com",
            "employer_contact_name": "HR Team",
            "application_url": "https://example.com/apply",
        })
        with db.connect() as conn:
            row = conn.execute("SELECT is_employer_post FROM jobs WHERE id = ?",
                               (post["id"],)).fetchone()
        check("employer post stays is_employer_post=1",
              row["is_employer_post"] == 1, str(row["is_employer_post"]))
        # 4) explicit 0/1 passed by a scraper is never overridden
        with db.connect() as conn:
            db.upsert_job(conn, {"source": "yolo", "url": "https://example.com/job/2",
                                 "title": "Cafe staff", "is_employer_post": 0})
            conn.commit()
            row = conn.execute("SELECT is_employer_post FROM jobs WHERE url = ?",
                               ("https://example.com/job/2",)).fetchone()
        check("explicit value preserved", row["is_employer_post"] == 0)
    finally:
        if old is None:
            os.environ.pop("JAPAN_JOBS_DB", None)
        else:
            os.environ["JAPAN_JOBS_DB"] = old
        importlib.reload(db)
        os.unlink(tmp)


def test_jobspy_sites_exclude_glassdoor():
    import jobspy_scraper as js
    print("jobspy defaults:")
    check("glassdoor not in DEFAULT_SITES (no Japan support)",
          "glassdoor" not in js.DEFAULT_SITES, str(js.DEFAULT_SITES))
    check("indeed/linkedin/google still default",
          {"indeed", "linkedin", "google"} <= set(js.DEFAULT_SITES))


def _jobposting(html):
    import json, re
    m = re.search(r'<script type="application/ld\+json">(\{.*?"@type": ?"JobPosting".*?\})</script>',
                  html, re.S)
    return json.loads(m.group(1)) if m else None


def test_job_posting_jsonld():
    import app, db
    print("JobPosting JSON-LD:")
    client = app.app.test_client()
    with db.connect() as conn:
        with_sal = conn.execute(
            "SELECT id FROM jobs WHERE salary_min_annual_jpy IS NOT NULL "
            "AND DATE(last_seen_at) >= DATE('now','-3650 days') LIMIT 1").fetchone()
        no_sal = conn.execute(
            "SELECT id FROM jobs WHERE salary_min_annual_jpy IS NULL "
            "AND (salary IS NULL OR salary = '') LIMIT 1").fetchone()
    jid = with_sal[0]
    data = _jobposting(client.get(f"/job/{jid}").get_data(as_text=True))
    check("JobPosting present", data is not None)
    check("required: @type", data and data.get("@type") == "JobPosting")
    check("required: title", bool(data and data.get("title")))
    check("required: datePosted", bool(data and data.get("datePosted")))
    check("has identifier", bool(data and data.get("identifier")))
    check("url is absolute", bool(data and data.get("url", "").startswith("http")))
    check("salary present when parsed", "baseSalary" in (data or {}))
    check("baseSalary currency JPY",
          (data or {}).get("baseSalary", {}).get("currency") == "JPY")
    if no_sal:
        d2 = _jobposting(client.get(f"/job/{no_sal[0]}").get_data(as_text=True))
        check("missing salary -> no baseSalary (still valid)",
              d2 is not None and "baseSalary" not in d2)
    # No invented validThrough / fake remote.
    check("no fabricated validThrough", "validThrough" not in (data or {}))


def test_jsonld_uses_base_url(monkeypatch=None):
    import importlib, os
    os.environ["FLASK_ENV"] = "production"
    os.environ["BASE_URL"] = "https://gaijinhunterjp.com"
    import config, app as appmod
    importlib.reload(config); importlib.reload(appmod)
    print("JSON-LD BASE_URL:")
    try:
        client = appmod.app.test_client()
        import db
        jid = db.query_jobs(limit=1)[0]["id"]
        data = _jobposting(client.get(f"/job/{jid}",
                                      headers={"Host": "gaijinhunterjp.com"}).get_data(as_text=True))
        check("JobPosting url uses BASE_URL",
              data and data["url"] == f"https://gaijinhunterjp.com/job/{jid}")
    finally:
        # Restore dev config so later tests aren't redirected.
        os.environ.pop("FLASK_ENV", None)
        os.environ.pop("BASE_URL", None)
        importlib.reload(config); importlib.reload(appmod)


def test_rate_limit():
    import importlib, config, app as appmod
    importlib.reload(config); importlib.reload(appmod)
    print("rate limiting:")
    client = appmod.app.test_client()
    codes = [client.post("/post-a-job", data={"title": "x"},
                         environ_overrides={"REMOTE_ADDR": "203.0.113.7"}).status_code
             for _ in range(7)]
    check("post-a-job throttles after 5/hour", 429 in codes, str(codes))
    gets = {client.get("/jobs").status_code for _ in range(8)}
    check("GET reads never throttled", gets == {200}, str(gets))
    check("healthz never throttled", client.get("/healthz").status_code == 200)


def test_routes():
    import app as appmod
    print("routes (Flask test client):")
    client = appmod.app.test_client()
    pages = [
        "/", "/jobs", "/jobs?professional_only=1", "/jobs?japanese_level=Not+Required",
        "/jobs?visa_sponsorship_mentioned=1&remote_work_ok=1",
        "/jobs?q=engineer&salary_min=8000000&sort=salary_desc",
        "/jobs?overseas_application_ok=1", "/jobs?page=2",
        "/jobs?visa_support=1", "/jobs?apply_from_abroad=1", "/jobs?remote=1",
        "/jobs?salary_min=junk&days_within=junk&page=junk",   # bad params must not 500
        "/resources", "/resources/applying-from-abroad", "/resources/visa-types",
        "/guides", "/tools", "/insights/salary", "/companies", "/reports",
        "/glossary", "/interview-prep", "/living", "/saved", "/applied",
        "/profile", "/tracker", "/resume", "/robots.txt",
        "/post-a-job", "/sitemap.xml", "/llms.txt", "/api/jobs.json?limit=5",
    ]
    for p in pages:
        r = client.get(p)
        check(f"GET {p}", r.status_code == 200, str(r.status_code))
    # a real job detail page + similar API
    import db
    row = db.query_jobs(limit=1)[0]
    r = client.get(f"/job/{row['id']}")
    check("GET /job/<id>", r.status_code == 200, str(r.status_code))
    check("job page has glance grid", b"gh-glance" in r.data)
    r = client.get(f"/api/similar/{row['id']}")
    check("GET /api/similar", r.status_code == 200 and b"jobs" in r.data)
    r = client.get("/job/99999999")
    check("missing job 404s", r.status_code == 404, str(r.status_code))
    r = client.get("/jobs")
    check("jobs page shows professional filter", b"Professional roles only" in r.data)
    check("jobs page has More filters disclosure", b"More filters" in r.data)
    # URL aliases actually filter (not just 200)
    import re as _re
    def total_of(path):
        m = _re.search(rb"<strong>(\d+)</strong> jobs", client.get(path).data)
        return int(m.group(1)) if m else -1
    check("?visa_support=1 filters", 0 < total_of("/jobs?visa_support=1") < total_of("/jobs"))
    check("?apply_from_abroad=1 filters", 0 < total_of("/jobs?apply_from_abroad=1") < total_of("/jobs"))
    r = client.get("/")
    check("landing shows visa stat", b"Visa support" in r.data)
    check("landing has no fake match feed", b"94%" not in r.data)
    check("landing top-jobs panel is real", b"Top-ranked jobs right now" in r.data)


def test_sitemap_and_healthz():
    import re as _re
    import xml.etree.ElementTree as ET

    import app as appmod
    import db
    print("sitemap + healthz:")
    client = appmod.app.test_client()

    r = client.get("/sitemap.xml")
    check("sitemap 200 + xml", r.status_code == 200 and "xml" in r.content_type,
          r.content_type)
    body = r.data.decode()
    ET.fromstring(body)
    check("sitemap is well-formed XML", True)
    # Active job detail pages included (they carry JobPosting JSON-LD)
    row = db.query_jobs(limit=1)[0]
    check("sitemap includes active job pages", f"/job/{row['id']}<" in body)
    job_lastmod = _re.search(
        r"<loc>[^<]*/job/\d+</loc><lastmod>\d{4}-\d{2}-\d{2}</lastmod>", body)
    check("job URLs carry a lastmod date", job_lastmod is not None)
    # Static pages must NOT claim they changed today (old fake-lastmod bug)
    jobs_entry = _re.search(
        r"<loc>[^<]+/jobs</loc>(<lastmod>[^<]+</lastmod>)?", body)
    check("static pages omit fabricated lastmod",
          jobs_entry is not None and jobs_entry.group(1) is None,
          jobs_entry.group(0) if jobs_entry else "no /jobs entry")
    locs = _re.findall(r"<loc>([^<]+)</loc>", body)
    check("sitemap has no duplicate URLs", len(locs) == len(set(locs)))

    r = client.get("/healthz")
    check("healthz 200", r.status_code == 200, str(r.status_code))
    data = r.get_json()
    check("healthz exposes freshness",
          {"status", "jobs", "fresh_jobs", "last_seen_at",
           "data_age_days"} <= set(data), str(sorted(data)))
    check("healthz status is ok|stale", data["status"] in ("ok", "stale"),
          str(data.get("status")))


if __name__ == "__main__":
    for fn in (test_inference, test_en_level_inference, test_posting_language,
               test_salary_extraction, test_yolo_classify, test_db_queries,
               test_only_ids, test_provenance, test_upsert_not_null_defaults,
               test_jobspy_sites_exclude_glassdoor, test_job_posting_jsonld,
               test_jsonld_uses_base_url, test_rate_limit, test_routes,
               test_sitemap_and_healthz):
        try:
            fn()
        except AssertionError:
            pass   # failure already recorded + printed; keep running the rest
    print(f"\n{'ALL PASS' if not failures else str(len(failures)) + ' FAILURES: ' + ', '.join(failures)}")
    sys.exit(1 if failures else 0)
