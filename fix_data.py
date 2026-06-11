"""
One-pass data-quality repair for existing rows in jobs.db.

Fixes applied (all conservative — raw source text is never modified):

  1. YOLO Japan re-classification. The old classifier matched category
     keywords against the full description body, so benefit boilerplate
     ("medical insurance", "hospital nearby") tagged ramen shops, drivers and
     factory work as care_work / Healthcare. Re-classify from the structured
     Industry field first, title keywords second (yolojapan_scraper.classify).

  2. YOLO overseas/visa flags. "Status of residence" appears on ~every YOLO
     page as a requirements header and was misread as visa support, which also
     forced overseas_application_ok=1 on all ~2,000 rows. Both flags are reset
     and recomputed from explicit language only.

  3. GaijinPot remote/overseas flags. The old scraper searched the WHOLE page
     text, and the search-filter widget prints "Remote Work OK" / "Overseas
     Application OK" as checkbox labels on every page — so every GaijinPot job
     was marked remote + overseas. Recomputed from job content fields only.

  4. Language-level canonicalization ('None' -> 'Not Required',
     'Fluent Japanese' -> 'Native / Fluent', …) across all rows.

  5. Derived-field refresh for every non-employer row: source_quality (new
     complete map), visa/relocation flags (stricter patterns), data-quality
     and Foreigner Fit scores + reasons.

Usage:
    python fix_data.py            # applies fixes (backs up jobs.db first)
    python fix_data.py --dry-run  # report what would change, write nothing
"""

from __future__ import annotations

import argparse
import re
import shutil
import sqlite3
from collections import Counter
from datetime import datetime
from pathlib import Path

import db
import inference
import yolojapan_scraper as yj

OVERSEAS_RE = re.compile(
    r"appl(?:y|ication)s?\s+from\s+(?:overseas|abroad)|overseas\s+applicants?|"
    r"overseas\s+application\s+ok|"
    r"currently\s+(?:living|residing)\s+(?:overseas|abroad)|"
    r"recruit(?:ing|ment)?\s+from\s+(?:overseas|abroad)",
    re.IGNORECASE,
)


def _job_text(row: dict) -> str:
    return " ".join(filter(None, [
        row.get("title"), row.get("description"),
        row.get("requirements"), row.get("salary_perks"), row.get("tags"),
    ]))


def fix_yolo(row: dict) -> dict:
    """Return field updates for a YOLO Japan row."""
    updates: dict = {}
    cls = yj.classify(row.get("title") or "", row.get("description") or "",
                      row.get("industries") or "", row.get("employment_terms"))
    body = _job_text(row)
    visa_flag = inference.infer_visa_sponsorship(body)

    tags = [cls["category"]]
    if cls["is_part_time"]:
        tags.append("part-time")
    if cls["is_temporary"]:
        tags.append("temporary")
    if (row.get("salary_period") or "") == "Hour":
        tags.append("hourly")
    if cls["is_entry_level"]:
        tags.append("entry-level")
    if visa_flag == 1:
        tags.append("visa-support")
    tags.append("foreigner-targeted")
    updates["tags"] = ", ".join(dict.fromkeys(tags))
    updates["role_family"] = yj._ROLE_FAMILY.get(cls["category"])
    updates["overseas_application_ok"] = 1 if OVERSEAS_RE.search(body) else None
    return updates


def fix_gaijinpot(row: dict) -> dict:
    """Reset chrome-derived flags; recompute from job content only."""
    text = _job_text(row)
    remote = inference.infer_remote(text)
    overseas = 1 if OVERSEAS_RE.search(text) else None
    return {"remote_work_ok": remote, "overseas_application_ok": overseas}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--dry-run", action="store_true", help="Report only; write nothing.")
    ap.add_argument("--db", default=None, help="Path to jobs.db (default: db.DB_PATH)")
    args = ap.parse_args()

    db_path = Path(args.db) if args.db else db.DB_PATH
    if not args.dry_run:
        backup = db_path.with_name(
            db_path.name + ".bak_fix_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
        shutil.copy2(db_path, backup)
        print(f"Backup written: {backup}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = [dict(r) for r in conn.execute("SELECT * FROM jobs")]
    print(f"{len(rows)} rows loaded")

    stats = Counter()
    yolo_categories = Counter()

    for row in rows:
        updates: dict = {}
        src = (row.get("source") or "").lower()
        employer_post = row.get("is_employer_post") == 1

        # --- source-specific raw-flag repairs --------------------------------
        if src == "yolo japan":
            u = fix_yolo(row)
            yolo_categories[(u["tags"] or "").split(",")[0]] += 1
            if u["tags"] != row.get("tags"):
                stats["yolo_retagged"] += 1
            if u["role_family"] != row.get("role_family"):
                stats["yolo_role_family_changed"] += 1
            if u["overseas_application_ok"] != row.get("overseas_application_ok"):
                stats["yolo_overseas_reset"] += 1
            updates.update(u)
        elif src == "gaijinpot":
            u = fix_gaijinpot(row)
            if u["remote_work_ok"] != row.get("remote_work_ok"):
                stats["gaijinpot_remote_reset"] += 1
            if u["overseas_application_ok"] != row.get("overseas_application_ok"):
                stats["gaijinpot_overseas_reset"] += 1
            updates.update(u)

        # --- canonical language levels (all rows) ----------------------------
        for col in ("japanese_level", "english_level"):
            if row.get(col):
                norm = inference.normalize_level_label(row[col])
                if norm != row[col]:
                    updates[col] = norm
                    stats[f"{col}_normalized"] += 1

        # --- derived-field refresh (skip employer-entered rows) --------------
        merged = {**row, **updates}
        if not employer_post:
            haystack = " ".join(filter(None, [
                merged.get("title"), merged.get("description"),
                merged.get("requirements"), merged.get("salary_perks"),
            ]))
            new_visa = inference.infer_visa_support(haystack)
            new_reloc = inference.infer_relocation_support(haystack)
            new_quality = inference.source_quality(merged.get("source"))
            if new_visa != row.get("visa_sponsorship_mentioned"):
                stats["visa_flag_changed"] += 1
            updates["visa_sponsorship_mentioned"] = new_visa
            updates["relocation_support_mentioned"] = new_reloc
            if new_quality != row.get("source_quality"):
                stats["source_quality_changed"] += 1
            updates["source_quality"] = new_quality
            merged = {**row, **updates}

        updates["data_quality_score"] = inference.calculate_data_quality(merged)
        score, reasons = inference.calculate_foreigner_fit(merged)
        if score != row.get("foreigner_fit_score"):
            stats["fit_score_changed"] += 1
        updates["foreigner_fit_score"] = score
        updates["foreigner_fit_reasons"] = ",".join(reasons) if reasons else None

        if not args.dry_run and updates:
            cols = ", ".join(f"{c} = ?" for c in updates)
            conn.execute(f"UPDATE jobs SET {cols} WHERE id = ?",
                         list(updates.values()) + [row["id"]])
        stats["rows_processed"] += 1

    if not args.dry_run:
        conn.commit()
    conn.close()

    print("\n=== fix_data summary ===")
    for k, v in sorted(stats.items()):
        print(f"  {k:<32} {v}")
    if yolo_categories:
        print("\nYOLO categories after re-classification:")
        for cat, n in yolo_categories.most_common():
            print(f"  {cat:<22} {n}")
    if args.dry_run:
        print("\n(dry-run: no changes written)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
