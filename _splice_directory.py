"""Insert NEW_RESOURCE at end of RESOURCES list in content.py."""

import re
import sys
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR))

from _new_resource_directory import NEW_RESOURCE  # noqa: E402

CONTENT_PY = THIS_DIR / "content.py"

MARKER = "EXTERNAL_RESOURCES_DIRECTORY:v1"


def render_entry(entry: dict) -> str:
    lines = ["    {", f"    # {MARKER}"]
    for key, value in entry.items():
        if isinstance(value, str) and ("\n" in value or len(value) > 80):
            # Use triple-quoted string
            lines.append(f'        "{key}": """{value}""",')
        elif isinstance(value, list):
            if value and isinstance(value[0], tuple):
                # TOC list of tuples
                lines.append(f'        "{key}": [')
                for slug, label in value:
                    lines.append(f'            ({repr(slug)}, {repr(label)}),')
                lines.append("        ],")
            else:
                lines.append(f'        "{key}": {value!r},')
        else:
            lines.append(f'        "{key}": {value!r},')
    lines.append("    },")
    return "\n".join(lines) + "\n"


def main():
    src = CONTENT_PY.read_text(encoding="utf-8")
    if MARKER in src:
        print("Already inserted; skipping.")
        return
    backup = CONTENT_PY.with_suffix(".py.bak4")
    backup.write_text(src, encoding="utf-8")
    print(f"Backed up to {backup.name}")

    # Find RESOURCES list bounds
    m = re.search(r"^RESOURCES: list\[dict\] = \[$", src, re.MULTILINE)
    if not m:
        raise RuntimeError("RESOURCES list not found")
    start = src.find("\n", m.end()) + 1
    depth = 1
    i = start
    in_string = False
    while i < len(src) and depth > 0:
        c = src[i]
        # Skip triple-quoted strings
        if src[i:i + 3] == '"""':
            end_q = src.find('"""', i + 3)
            if end_q == -1:
                break
            i = end_q + 3
            continue
        if c == "[" or c == "{":
            depth += 1
        elif c == "]" or c == "}":
            depth -= 1
            if depth == 0:
                break
        i += 1
    # Walk back to start of the line containing the closing ']'
    line_start = src.rfind("\n", 0, i) + 1
    entry_text = render_entry(NEW_RESOURCE)
    new_src = src[:line_start] + entry_text + src[line_start:]
    CONTENT_PY.write_text(new_src, encoding="utf-8")
    print(f"Inserted external-resources entry (resources list closing at line {src[:i].count(chr(10)) + 1})")


if __name__ == "__main__":
    main()
