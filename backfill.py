"""
Repeatable, conservative data-maintenance backfill.

    python backfill.py --dry-run                       # all targets, report only
    python backfill.py --only english-level --dry-run
    python backfill.py --only salary --dry-run
    python backfill.py --only posting-language --dry-run
    python backfill.py --only provenance --dry-run
    python backfill.py --only scores --dry-run
    python backfill.py --apply                         # all targets, with DB backup

Principles:
  * NEVER overwrite a non-null explicit value with an inferred one.
  * Inference is conservative — blank is better than a false claim.
  * A timestamped DB backup is written before any --apply.
  * Safe to rerun: every pass is idempotent.

Targets:
  english-level    Fill english_level ONLY where NULL, from explicit posting
                   language ("Business English required", …). Marks 'inferred'.
  salary           Fill salary fields ONLY where empty, from unambiguous
                   statements in title/description (¥6M–¥10M, 年収600万円,
                   月給30万円, 時給1,500円…). Marks 'inferred'.
  posting-language Recompute the section-aware posting-language label
                   (English/Japanese/Bilingual/Mixed/Unknown) for all rows.
  provenance       Fill *_source columns (explicit/inferred/not_stated) for
                   rows that predate the provenance system, using a per-source
                   map of which scrapers provide structured fields.
  scores           Recompute data_quality_score + foreigner_fit_score/reasons.
                   Run this after changing scoring rules in inference.py.
"""

from __future__ import annotations

import argparse
import shutil
import sqlite3
from collections import Counter
from datetime import datetime
from pathlib import Path

import db
import inference
import salary_parser

TARGETS = ["english-level", "salary", "posting-language", "provenance", "scores"]

# Which sources provide each field as STRUCTURED data (everything else that
# has a value for the field on an old row is treated as inferred).
_EXPLICIT_BY_FIELD = {
    "japanese_level": {"gaijinpot", "yolo japan", "tokyodev", "japandev", "careercross"},
    "english_level":  {"gaijinpot", "japandev"},
    "remote":         {"tokyodev", "japandev"},
    "abroad":         {"tokyodev", "japandev"},
    "visa":           set(),          # all visa flags so far came from text inference
}


def _body(row: dict) -> str:
    return " ".join(filter(None, [
        row.get("title"), row.get("description"),
        row.get("requirements"), row.get("salary_perks"),
    ]))


def pass_english_level(rows, stats, samples):
    updates = {}
    for r in rows:
        if r.get("english_level"):
            continue
        en = inference.infer_en_level(_body(r))
        if en:
            updates[r["id"]] = {"english_level": en, "english_level_source": "inferred"}
            stats["english_level_filled"] += 1
            if len(samples) < 5:
                samples.append((r["id"], (r.get("title") or "")[:50], "english_level", None, en))
        elif not r.get("english_level_source"):
            updates[r["id"]] = {"english_level_source": "not_stated"}
    return updates


def pass_salary(rows, stats, samples):
    updates = {}
    for r in rows:
        has = (r.get("salary") or "").strip() or r.get("salary_min_jpy") or r.get("salary_min_annual_jpy")
        if has:
            continue
        found = salary_parser.extract_from_text(_body(r))
        if found:
            u = {k: v for k, v in found.items()}
            u["salary_source"] = "inferred"
            updates[r["id"]] = u
            stats["salary_filled"] += 1
            if len(samples) < 5:
                samples.append((r["id"], (r.get("title") or "")[:50], "salary", None, found["salary"]))
    return updates


def pass_posting_language(rows, stats, samples):
    updates = {}
    for r in rows:
        new = inference.classify_posting_language(
            r.get("title"), r.get("description"), r.get("requirements"))
        if new != r.get("posting_language"):
            updates[r["id"]] = {"posting_language": new}
            stats[f"lang_{r.get('posting_language')}->{new}"] += 1
            if len(samples) < 5:
                samples.append((r["id"], (r.get("title") or "")[:50],
                                "posting_language", r.get("posting_language"), new))
    return updates


def pass_provenance(rows, stats, samples):
    updates = {}
    for r in rows:
        src = (r.get("source") or "").lower()
        employer = r.get("is_employer_post") == 1
        u = {}

        def fill(src_col, field_key, value_present):
            if r.get(src_col):           # never overwrite an existing claim
                return
            if not value_present:
                u[src_col] = "not_stated"
            elif employer:
                u[src_col] = "explicit"
            elif src in _EXPLICIT_BY_FIELD[field_key]:
                u[src_col] = "explicit"
            else:
                u[src_col] = "inferred"

        fill("japanese_level_source", "japanese_level", bool(r.get("japanese_level")))
        fill("english_level_source",  "english_level",  bool(r.get("english_level")))
        fill("remote_source",         "remote",         r.get("remote_work_ok") is not None)
        fill("abroad_source",         "abroad",         r.get("overseas_application_ok") is not None)
        fill("visa_source",           "visa",           r.get("visa_sponsorship_mentioned") is not None)
        # All salary present today came from structured source fields.
        if not r.get("salary_source"):
            has_sal = (r.get("salary") or "").strip() or r.get("salary_min_jpy") \
                      or r.get("salary_min_annual_jpy")
            u["salary_source"] = "explicit" if has_sal else "not_stated"

        if u:
            updates[r["id"]] = u
            stats["provenance_filled"] += 1
    return updates


def pass_scores(rows, stats, samples):
    updates = {}
    for r in rows:
        u = {}
        dq = inference.calculate_data_quality(r)
        score, reasons = inference.calculate_foreigner_fit(r)
        rs = ",".join(reasons) if reasons else None
        if dq != r.get("data_quality_score"):
            u["data_quality_score"] = dq
        if score != r.get("foreigner_fit_score") or rs != r.get("foreigner_fit_reasons"):
            u["foreigner_fit_score"] = score
            u["foreigner_fit_reasons"] = rs
            stats["fit_score_changed"] += 1
            if len(samples) < 5:
                samples.append((r["id"], (r.get("title") or "")[:50],
                                "fit", r.get("foreigner_fit_score"), score))
        if u:
            updates[r["id"]] = u
    return updates


PASSES = {
    "english-level":    pass_english_level,
    "salary":           pass_salary,
    "posting-language": pass_posting_language,
    "provenance":       pass_provenance,
    "scores":           pass_scores,
}


def snapshot_counts(conn) -> dict:
    q = lambda sql: conn.execute(sql).fetchone()[0]
    return {
        "english_level set":  q("SELECT COUNT(*) FROM jobs WHERE english_level IS NOT NULL AND english_level != ''"),
        "salary set":         q("SELECT COUNT(*) FROM jobs WHERE salary_min_annual_jpy IS NOT NULL OR (salary IS NOT NULL AND salary != '')"),
        "posting=English":    q("SELECT COUNT(*) FROM jobs WHERE posting_language = 'English'"),
        "posting=Bilingual":  q("SELECT COUNT(*) FROM jobs WHERE posting_language = 'Bilingual'"),
        "posting=Mixed":      q("SELECT COUNT(*) FROM jobs WHERE posting_language = 'Mixed'"),
        "posting=Japanese":   q("SELECT COUNT(*) FROM jobs WHERE posting_language = 'Japanese'"),
        "provenance filled":  q("SELECT COUNT(*) FROM jobs WHERE visa_source IS NOT NULL"),
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__.split("\n")[1],
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    ap.add_argument("--only", choices=TARGETS, default=None,
                    help="Run a single target instead of all.")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Report only (default).")
    mode.add_argument("--apply", action="store_true", help="Write changes (backs up DB first).")
    ap.add_argument("--db", default=None, help="Path to jobs.db (default: db.DB_PATH)")
    args = ap.parse_args()
    apply = args.apply

    db_path = Path(args.db) if args.db else db.DB_PATH
    db.init_db(db_path)   # ensures provenance columns exist via migrate()

    if apply:
        backup = db_path.with_name(
            db_path.name + ".bak_backfill_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
        shutil.copy2(db_path, backup)
        print(f"Backup: {backup}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    before = snapshot_counts(conn)
    rows = [dict(r) for r in conn.execute("SELECT * FROM jobs")]
    by_id = {r["id"]: r for r in rows}
    print(f"{len(rows)} rows · mode: {'APPLY' if apply else 'dry-run'}")

    targets = [args.only] if args.only else TARGETS
    stats = Counter()
    samples: list = []
    pending: dict[int, dict] = {}

    for t in targets:
        updates = PASSES[t](rows, stats, samples)
        for rid, u in updates.items():
            pending.setdefault(rid, {}).update(u)
            # keep in-memory rows current so later passes (scores) see changes
            by_id[rid].update(u)
        print(f"  {t:<18} {len(updates)} rows would change")

    if apply and pending:
        for rid, u in pending.items():
            cols = ", ".join(f"{c} = ?" for c in u)
            conn.execute(f"UPDATE jobs SET {cols} WHERE id = ?", list(u.values()) + [rid])
        conn.commit()

    after = snapshot_counts(conn) if apply else before
    conn.close()

    print("\n=== stats ===")
    for k, v in sorted(stats.items()):
        print(f"  {k:<40} {v}")
    print("\n=== before / after ===")
    for k in before:
        print(f"  {k:<22} {before[k]:>6} -> {after[k] if apply else '(dry-run)'}")
    if samples:
        print("\n=== sample changes ===")
        for rid, title, field, old, new in samples:
            print(f"  #{rid:<6} {field:<16} {old!r} -> {new!r}  | {title}")
    if not apply:
        print("\n(dry-run: nothing written; rerun with --apply)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
