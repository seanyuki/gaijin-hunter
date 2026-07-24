"""Re-derive the inference-based role_family labels with the improved classifier.

Safe and re-runnable:
  * Only touches labels the classifier "owns" — None/empty or one of
    inference.ROLE_FAMILIES. Source-provided sector categories (e.g.
    "Logistics / Manufacturing", "Healthcare / Care") are preserved.
  * Never un-labels: if the classifier is unsure (None), the existing label stays.
  * Only the role_family column is written.

Usage:
  python reclassify_roles.py --dry-run   # report only, no writes
  python reclassify_roles.py             # apply
"""
import sys
from collections import Counter

import db
import inference

OURS = set(inference.ROLE_FAMILIES)


def reclassify(dry_run: bool = False):
    changed = []
    with db.connect() as conn:
        rows = conn.execute(
            "SELECT id, title, description, industries, tags, role_family FROM jobs"
        ).fetchall()
        for r in rows:
            cur = (r["role_family"] or "").strip()
            # Preserve source sector categories the classifier doesn't produce.
            if cur and cur not in OURS:
                continue
            new = inference.classify_role_family(
                r["title"], r["description"],
                industries=r["industries"], tags=r["tags"])
            if new is None or new == cur:
                continue  # unsure -> keep existing; or already correct
            changed.append((r["id"], cur or None, new))
        if not dry_run and changed:
            conn.executemany(
                "UPDATE jobs SET role_family = ? WHERE id = ?",
                [(new, jid) for jid, _old, new in changed],
            )
            conn.commit()
    return changed


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    changed = reclassify(dry_run=dry)
    verb = "would change" if dry else "changed"
    print(f"{verb}: {len(changed)} rows\n")
    moves = Counter((old, new) for _id, old, new in changed)
    for (old, new), c in moves.most_common(30):
        print(f"  {c:4d}  {str(old):32s} -> {new}")
