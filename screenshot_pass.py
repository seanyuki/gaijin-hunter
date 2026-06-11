"""
Real-browser screenshot pass (Playwright Chromium).

    python screenshot_pass.py            # captures key pages at 390/768/1440
    python screenshot_pass.py --width 390

Writes PNGs to screenshots/ (gitignored) and prints basic layout checks:
horizontal-overflow detection and console errors per page.
"""

from __future__ import annotations

import argparse
import sqlite3
import threading
import time
from pathlib import Path

import app as appmod

WIDTHS = [390, 768, 1440]
OUT = Path(__file__).parent / "screenshots"
PORT = 5077


def pages() -> list[tuple[str, str]]:
    conn = sqlite3.connect(Path(__file__).parent / "jobs.db")
    jid = conn.execute(
        "SELECT id FROM jobs WHERE DATE(last_seen_at) >= DATE('now','-30 days') "
        "ORDER BY COALESCE(foreigner_fit_score,0) DESC LIMIT 1").fetchone()[0]
    return [
        ("home",      "/"),
        ("jobs",      "/jobs"),
        ("jobs_prof", "/jobs?professional_only=1"),
        ("job",       f"/job/{jid}"),
        ("profile",   "/profile"),
        ("tracker",   "/tracker"),
        ("resume",    "/resume"),
    ]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=int, default=None)
    args = ap.parse_args()
    widths = [args.width] if args.width else WIDTHS

    OUT.mkdir(exist_ok=True)
    (OUT / ".gitignore").write_text("*\n")

    t = threading.Thread(
        target=lambda: appmod.app.run(port=PORT, debug=False, use_reloader=False),
        daemon=True)
    t.start()
    time.sleep(2)

    from playwright.sync_api import sync_playwright
    issues = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for w in widths:
            ctx = browser.new_context(viewport={"width": w, "height": 844})
            page = ctx.new_page()
            errors: list[str] = []
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append(str(e)))
            for name, path in pages():
                errors.clear()
                page.goto(f"http://127.0.0.1:{PORT}{path}", wait_until="networkidle")
                page.screenshot(path=OUT / f"{name}_{w}.png", full_page=True)
                overflow = page.evaluate(
                    "document.documentElement.scrollWidth - document.documentElement.clientWidth")
                height = page.evaluate("document.documentElement.scrollHeight")
                flag = ""
                if overflow > 2:
                    flag += f"  !! horizontal overflow {overflow}px"
                    issues.append(f"{name}@{w}: overflow {overflow}px")
                if errors:
                    flag += f"  !! {len(errors)} console errors: {errors[:2]}"
                    issues.append(f"{name}@{w}: {errors[:2]}")
                print(f"  {name:<10} {w:>5}px  height={height:<6} {flag}")
            ctx.close()
        browser.close()
    print("\n" + ("ISSUES:\n  " + "\n  ".join(issues) if issues else "No overflow / console errors detected."))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
