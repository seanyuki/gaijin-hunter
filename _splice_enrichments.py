"""Splice resource and guide enrichments into content.py.

For each slug in RESOURCE_ENRICHMENTS and GUIDE_ENRICHMENTS:
  1. Add new (slug, label) tuples to the entry's toc list.
  2. Append new HTML to the entry's body, just before the closing triple-quote.

Idempotent: looks for "<!-- ENRICH_V2:slug -->" marker before inserting body content.

For resource entries, search starts from RESOURCES list. For guide entries, only from
GUIDES list (avoids collision with same-slug entries in ROADMAPS).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR))

from _enrichments_resources import RESOURCE_ENRICHMENTS  # noqa: E402
from _enrichments_guides import GUIDE_ENRICHMENTS  # noqa: E402

CONTENT_PY = THIS_DIR / "content.py"


def find_list_bounds(source: str, list_name: str) -> tuple[int, int]:
    """Return (start, end) absolute indices for the named top-level list assignment.

    start = index after the opening '['
    end   = index of the matching closing ']'
    """
    pattern = re.compile(rf"^{list_name}: list\[dict\] = \[$", re.MULTILINE)
    m = pattern.search(source)
    if not m:
        raise RuntimeError(f"Could not find {list_name} assignment")
    start = source.find("\n", m.end()) + 1
    depth = 1
    i = start
    while i < len(source) and depth > 0:
        c = source[i]
        if c == "[" or c == "{":
            depth += 1
        elif c == "]" or c == "}":
            depth -= 1
            if depth == 0:
                return start, i
        i += 1
    raise RuntimeError(f"Could not find closing ']' for {list_name}")


def find_entry_bounds(source: str, slug: str, list_start: int, list_end: int) -> tuple[int, int]:
    """Within source[list_start:list_end], find the entry whose 'slug' matches.

    Returns (start, end) absolute indices for the entry's outer {...},
    where start = index of the opening '{' and end = index of the closing '}'.
    """
    slug_re = re.compile(rf'"slug": "{re.escape(slug)}"')
    m = slug_re.search(source, list_start, list_end)
    if not m:
        raise RuntimeError(f"Slug not found in list: {slug}")
    # Walk back to find the '{' of this entry
    start = source.rfind("{", list_start, m.start())
    if start == -1:
        raise RuntimeError(f"Could not find opening '{{' for entry: {slug}")
    # Walk forward to find the matching '}'
    depth = 1
    i = start + 1
    while i < list_end and depth > 0:
        c = source[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return start, i
        elif c == '"' or c == "'":
            # Skip over string literals so braces inside HTML are ignored
            quote = c
            # Detect triple-quoted string
            if source[i:i + 3] == quote * 3:
                # find closing triple quote
                end_q = source.find(quote * 3, i + 3)
                if end_q == -1:
                    raise RuntimeError("Unterminated triple-quoted string")
                i = end_q + 3
                continue
            # Single-line string; find unescaped closing quote
            j = i + 1
            while j < list_end:
                if source[j] == "\\":
                    j += 2
                    continue
                if source[j] == quote:
                    i = j + 1
                    break
                j += 1
            else:
                raise RuntimeError("Unterminated single-line string")
            continue
        i += 1
    raise RuntimeError(f"Could not find closing '}}' for entry: {slug}")


def append_to_toc(entry_text: str, additions: list[tuple[str, str]]) -> str:
    """Add (slug, label) tuples to the entry's 'toc' list, before the closing ']'."""
    if not additions:
        return entry_text
    # Find "toc": [
    m = re.search(r'"toc": \[', entry_text)
    if not m:
        return entry_text
    depth = 1
    i = m.end()
    while i < len(entry_text) and depth > 0:
        c = entry_text[i]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                break
        i += 1
    # Check whether any of these have already been added (idempotency)
    existing = entry_text[m.end():i]
    insertion_lines = []
    for slug, label in additions:
        marker = f'("{slug}",'
        if marker in existing:
            continue
        insertion_lines.append(f'            ("{slug}", {repr(label)}),')
    if not insertion_lines:
        return entry_text
    # Insert before the line of the closing ']'
    line_start = entry_text.rfind("\n", 0, i) + 1
    insertion = "\n".join(insertion_lines) + "\n"
    return entry_text[:line_start] + insertion + entry_text[line_start:]


def append_to_body(entry_text: str, html: str, slug: str) -> str:
    """Append html to the body string (just before its closing triple-quote)."""
    marker = f"<!-- ENRICH_V2:{slug} -->"
    if marker in entry_text:
        return entry_text  # idempotent
    # Find "body": """
    m = re.search(r'"body": """', entry_text)
    if not m:
        return entry_text
    # Find the closing triple-quote
    close_idx = entry_text.find('"""', m.end())
    if close_idx == -1:
        return entry_text
    # Walk back to before the closing """, find where the body actually ends
    insertion_idx = close_idx
    return entry_text[:insertion_idx] + html.lstrip("\n") + "\n" + entry_text[insertion_idx:]


def splice(source: str, list_name: str, enrichments: dict) -> tuple[str, list[str]]:
    """For each slug in enrichments, splice in TOC + body additions."""
    notes = []
    list_start, list_end = find_list_bounds(source, list_name)
    # Process entries in reverse order to keep earlier indices stable
    items = list(enrichments.items())

    # Sort by position in file (descending) so insertions don't disturb subsequent positions
    items_with_pos = []
    for slug, payload in items:
        slug_re = re.compile(rf'"slug": "{re.escape(slug)}"')
        m = slug_re.search(source, list_start, list_end)
        if not m:
            notes.append(f"WARN: slug not found in {list_name}: {slug}")
            continue
        items_with_pos.append((m.start(), slug, payload))
    items_with_pos.sort(reverse=True)  # descending position

    for pos, slug, payload in items_with_pos:
        # Re-locate bounds because earlier insertions may have shifted things
        list_start, list_end = find_list_bounds(source, list_name)
        entry_start, entry_end = find_entry_bounds(source, slug, list_start, list_end)
        entry_text = source[entry_start: entry_end + 1]
        new_entry = entry_text
        new_entry = append_to_toc(new_entry, payload.get("toc_additions", []))
        new_entry = append_to_body(new_entry, payload.get("body_addition", ""), slug)
        if new_entry != entry_text:
            source = source[:entry_start] + new_entry + source[entry_end + 1:]
            notes.append(f"  spliced {list_name}/{slug}")
        else:
            notes.append(f"  no-op {list_name}/{slug} (already enriched)")
    return source, notes


def main():
    src = CONTENT_PY.read_text(encoding="utf-8")
    backup = CONTENT_PY.with_suffix(".py.bak3")
    backup.write_text(src, encoding="utf-8")
    print(f"Backed up to {backup.name}")

    src, notes = splice(src, "RESOURCES", RESOURCE_ENRICHMENTS)
    for n in notes:
        print(n)
    src, notes = splice(src, "GUIDES", GUIDE_ENRICHMENTS)
    for n in notes:
        print(n)

    CONTENT_PY.write_text(src, encoding="utf-8")
    print(f"\nWrote {CONTENT_PY.name} ({len(src)} bytes)")


if __name__ == "__main__":
    main()
