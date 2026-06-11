"""Splice new role guides, new roadmaps, and roadmap enrichments into content.py.

Idempotent: tracks inserted slugs and skips re-insertion. Backups content.py to
content.py.bak before writing.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

# Ensure local imports work
THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR))

from _new_roles_part1 import NEW_ROLE_GUIDES  # noqa: E402
from _new_roles_part2 import NEW_ROLE_GUIDES_2  # noqa: E402
from _new_roadmaps import NEW_ROADMAPS, ROADMAP_ENRICHMENTS  # noqa: E402

import pprint


CONTENT_PY = THIS_DIR / "content.py"


def pyfmt(obj: object) -> str:
    """Pretty-print a Python object with consistent indenting."""
    return pprint.pformat(obj, indent=4, width=100, sort_dicts=False)


def render_dict_entry(entry: dict, indent: str = "    ") -> str:
    """Render a single dict entry that matches the style used in content.py.

    Renders as `    {\n        "key": value,\n        ...\n    },\n`.
    """
    lines = [f"{indent}{{"]
    for key, value in entry.items():
        rendered = pyfmt(value)
        # Keep multi-line strings as-is. Use triple-quoted strings for long ones.
        if isinstance(value, str) and "\n" in value:
            rendered = '"""' + value + '"""'
        lines.append(f'{indent}    "{key}": {rendered},')
    lines.append(f"{indent}}},")
    return "\n".join(lines) + "\n"


def render_list_entries(entries: list[dict]) -> str:
    return "".join(render_dict_entry(e) for e in entries)


def splice_into_list(
    source: str, list_name: str, new_entries_source: str, marker: str
) -> str:
    """Find the closing ']' of `list_name` and insert new_entries_source before it.

    Uses a unique marker comment to detect prior insertion and make this idempotent.
    """
    if marker in source:
        print(f"  (marker {marker!r} already present — skipping insertion)")
        return source

    # Match the start of the named list assignment, then find the matching ']' at
    # column 0 (top-level closing bracket).
    list_start_re = re.compile(rf"^{list_name}: list\[dict\] = \[$", re.MULTILINE)
    match = list_start_re.search(source)
    if not match:
        raise RuntimeError(f"Could not find {list_name} assignment in content.py")

    # Scan forward to find the matching closing bracket.
    depth = 1
    i = source.find("\n", match.end()) + 1
    while i < len(source) and depth > 0:
        c = source[i]
        if c == "[" or c == "{":
            depth += 1
        elif c == "]" or c == "}":
            depth -= 1
            if depth == 0:
                # Walk back to start of this line so we insert before it.
                line_start = source.rfind("\n", 0, i) + 1
                insertion = f"\n    # {marker}\n" + new_entries_source
                return source[:line_start] + insertion + source[line_start:]
        i += 1
    raise RuntimeError(f"Could not find closing ']' for {list_name}")


def enrich_roadmap_stage(source: str, slug: str, stage_title: str, extra_skills: list[str], extra_jp: list[str]) -> str:
    """Find a roadmap by slug, then its stage by title, then append extra bullets.

    Marker is embedded as a comment after the inserted bullets so we don't double-insert.
    """
    marker = f"# ENRICH:{slug}:{stage_title}:v1"
    if marker in source:
        return source

    # Locate the roadmap block
    slug_re = re.compile(rf'"slug": "{re.escape(slug)}"')
    slug_match = slug_re.search(source)
    if not slug_match:
        print(f"  WARN: roadmap slug not found: {slug}")
        return source

    # Locate the stage title within this roadmap (between slug_match and next "slug":)
    next_slug = source.find('"slug":', slug_match.end())
    if next_slug == -1:
        next_slug = len(source)
    block = source[slug_match.start(): next_slug]

    stage_re = re.compile(rf'"title": "{re.escape(stage_title)}",')
    stage_match = stage_re.search(block)
    if not stage_match:
        print(f"  WARN: stage not found: {slug}/{stage_title}")
        return source

    # Find the skills list within this stage (until next "title":, "promotion_to_next", or end)
    abs_stage_start = slug_match.start() + stage_match.start()
    # Bound: next "title": in same block or end of block
    next_stage_in_block = stage_re.search(block, stage_match.end())
    end_of_stage_in_block = next_stage_in_block.start() if next_stage_in_block else len(block)
    stage_text = source[abs_stage_start: slug_match.start() + end_of_stage_in_block]

    def append_to_field(stage_text_local: str, field: str, extras: list[str]) -> str:
        # Find the closing bracket of "field": [ ... ]
        field_re = re.compile(rf'"{field}": \[')
        fm = field_re.search(stage_text_local)
        if not fm:
            return stage_text_local
        depth = 1
        i = fm.end()
        while i < len(stage_text_local) and depth > 0:
            c = stage_text_local[i]
            if c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        # Walk back to line start of the closing ']' to insert above
        line_start = stage_text_local.rfind("\n", 0, i) + 1
        new_lines = "".join(f'                    {repr(e)},\n' for e in extras)
        return stage_text_local[:line_start] + new_lines + stage_text_local[line_start:]

    new_stage_text = stage_text
    if extra_skills:
        new_stage_text = append_to_field(new_stage_text, "skills", extra_skills)
    if extra_jp:
        new_stage_text = append_to_field(new_stage_text, "japan_specifics", extra_jp)

    # Add marker as a comment right after the stage's opening '{'
    new_stage_text = new_stage_text.replace(
        f'"title": "{stage_title}",', f'"title": "{stage_title}",  {marker}', 1
    )

    return source[: abs_stage_start] + new_stage_text + source[slug_match.start() + end_of_stage_in_block :]


def enrich_roadmap_pivots(source: str, slug: str, extra_pivots: list[str]) -> str:
    marker = f"# ENRICH:{slug}:pivots:v1"
    if marker in source:
        return source

    slug_re = re.compile(rf'"slug": "{re.escape(slug)}"')
    slug_match = slug_re.search(source)
    if not slug_match:
        return source

    next_slug = source.find('"slug":', slug_match.end())
    if next_slug == -1:
        next_slug = len(source)
    block = source[slug_match.start(): next_slug]

    pivots_re = re.compile(r'"common_pivots": \[')
    pm = pivots_re.search(block)
    if not pm:
        return source

    depth = 1
    i = pm.end()
    while i < len(block) and depth > 0:
        c = block[i]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                break
        i += 1
    # Walk back to line start of the closing ']'
    line_start = block.rfind("\n", 0, i) + 1
    new_lines = "".join(f'            {repr(e)},  {marker}\n' for e in extra_pivots)
    new_block = block[:line_start] + new_lines + block[line_start:]
    return source[:slug_match.start()] + new_block + source[slug_match.start() + len(block):]


def main():
    src = CONTENT_PY.read_text(encoding="utf-8")
    backup = CONTENT_PY.with_suffix(".py.bak2")
    backup.write_text(src, encoding="utf-8")
    print(f"Backed up to {backup.name}")

    # Splice GUIDES
    all_new_roles = NEW_ROLE_GUIDES + NEW_ROLE_GUIDES_2
    guides_chunk = render_list_entries(all_new_roles)
    src = splice_into_list(src, "GUIDES", guides_chunk, "NEW_ROLE_GUIDES:v1")
    print(f"Inserted {len(all_new_roles)} new role guides into GUIDES")

    # Splice ROADMAPS
    roadmaps_chunk = render_list_entries(NEW_ROADMAPS)
    src = splice_into_list(src, "ROADMAPS", roadmaps_chunk, "NEW_ROADMAPS:v1")
    print(f"Inserted {len(NEW_ROADMAPS)} new roadmaps into ROADMAPS")

    # Enrichments
    for slug, payload in ROADMAP_ENRICHMENTS.items():
        stage_map = payload.get("stages", {})
        for stage_title, extras in stage_map.items():
            src = enrich_roadmap_stage(
                src, slug, stage_title,
                extras.get("skills", []),
                extras.get("japan_specifics", []),
            )
        if payload.get("common_pivots"):
            src = enrich_roadmap_pivots(src, slug, payload["common_pivots"])
        print(f"Enriched roadmap: {slug}")

    CONTENT_PY.write_text(src, encoding="utf-8")
    print("content.py written.")


if __name__ == "__main__":
    main()
