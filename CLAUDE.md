# CLAUDE.md — Gaijin Hunter

Flask + Jinja app (`app.py`, `templates/`, SQLite `jobs.db`). All shared CSS lives in
one consolidated `<style>` block in `templates/base.html`, built on the tokens in
`DESIGN.md`. There is no build step; pages may carry small page-specific `<style>`
blocks that must also use the tokens.

## Design-System Enforcement

1. **`DESIGN.md` is canonical.** Where any stylesheet, template, or other document
   disagrees with it, `DESIGN.md` wins.
2. **`design.html` is the visual reference.** Open it to see every token and
   component rendered; new UI must look like it belongs on that page.
3. **Before any frontend work, read `DESIGN.md`** — especially the named rules
   (One Voice, Mono-for-Money, Signal Budget, Hairline-Does-the-Work,
   Invert-Don't-Lift, Section-Variety, No-Naked-Numbers).
4. **Reuse what's documented**: tokens, components, typography scale, spacing scale,
   radii, shadows, motion timings/easings, and interaction states. Reference CSS
   variables (`--accent`, `--line`, `--radius`, `--motion-fast`, …) — never raw values.
5. **Do not invent** new colors, shadows, radii, font sizes, font families, or layout
   patterns unless the design system is being intentionally extended — in which case
   extend `DESIGN.md` first, then implement.
6. **Avoid generic AI-generated UI patterns**: no gradient-mesh heroes, glassmorphism,
   navy/purple SaaS palettes, icon-card feature grids, naked stat counters, bubbly
   rounded cards, side-stripe alerts, hover-lifts, or button glows. See
   `DESIGN.md` §13 for the full Do/Don't list.
7. **Keep the interface consistent across pages.** Same focus ring, same button
   variants, same badge language, same table treatment everywhere. If two pages solve
   the same problem differently, one of them is wrong.
8. **If `DESIGN.md` changes, update `design.html` in the same change** (and vice
   versa). They must never drift apart.
9. **After frontend changes, review the result against `DESIGN.md`** and fix any
   drift before finishing: check color usage (vermilion ≤10%), radii (3–6px only),
   decision numbers in DM Mono, hairlines over shadows, ≤3 signals per listing card.
10. **Prioritize accessibility, responsiveness, loading speed, and clarity** over
    decoration: visible focus states, ≥44px touch targets, 4.5:1 contrast floors,
    `prefers-reduced-motion` paths, the three-family font budget (Barlow, Barlow
    Condensed, DM Mono — nothing else), no render-blocking additions.
11. **No decorative animation.** Motion is allowed only when it improves orientation,
    feedback, or perceived quality; timings/easings come from the motion tokens and
    nothing exceeds 350ms.

## Project-Specific Rules

12. **Preserve core functionality** when touching templates or app code: scraping,
    filtering, saving (star), applied, hidden, archived/stale job handling, salary
    normalization, and JSON-LD parsing/emission. These flows have tests — run
    `python -m pytest` after changes and keep it green.
13. **No broad scattered CSS hacks.** Fix styles at the source (the token or the
    component rule in `base.html`), not with per-page patches.
14. **Prefer reusable components and clean tokenized CSS.** If a pattern appears on
    two pages, it belongs in `base.html` (and in `design.html` as a reference render).
15. **No broad `!important` override layers.** The old stacked-theme approach was
    removed on purpose. The only sanctioned `!important` usage is the small, clearly
    marked "legacy page-style shims" section in `base.html` — shrink it as page
    templates get cleaned; never grow it.
16. **No leftover duplicate/legacy theme values.** One `:root` token block, one font
    link (Barlow / Barlow Condensed / DM Mono), no Geist/Fraunces, no `#1c1a17`,
    `#c3382f`, or cool-slate/amber hexes. When editing a template's local styles,
    convert any stray hex values to tokens as you go.
