# UX/UI product-quality pass — June 11, 2026

Grounded in the three requested references, read directly from their repos before any
changes: **Impeccable** (full SKILL.md: card/chip restraint, no accent side-stripes, no
gradient text, hierarchy via fewer-but-stronger signals, secondary actions visually
secondary, empty states that teach, UX-writing economy), **UI UX Pro Max** (pre-delivery
checklist: contrast, tap targets, responsive at 375/768/1024/1440, no emoji-as-icon),
and **Design Motion Principles** (Emil-restraint lens for productivity tools; anti-slop
motion checklist). They could not be installed as session skills (read-only skill cache),
so the source material was fetched and applied directly.

A previous design pass had already given the site a strong foundation — warm ink/washi/
vermilion tokens, Fraunces/Geist type, restrained sub-350ms motion with reduced-motion
support, focus rings, mobile drawer, command palette. The brand was left untouched. The
problems were **composition and product-realness**, not the design system.

## 1. Audit findings, ranked by severity

**P0 — Jobs page control overload.** Measured on the rendered page: 11 quick chips +
a 10-dropdown filter wall + an always-visible saved-searches row (showing "(none yet…)"
to every new visitor) + 9 checkboxes, all before the first job. Job cards averaged
**8.6 badges (max 11)** — role family, posting language, employment, JP, EN, career
level, remote, abroad, visa, video, "Recommended" — drowning the three facts that
drive an apply/skip decision. Classic chip-spam tell.

**P0 — Fake dashboard on the homepage.** The hero showed a static "command center" with
invented jobs ("Backend Engineer, Mercari · 94% match") and a fake pipeline (5 saved /
3 applied / 2 interview / 1 offer). Exactly the kind of fabricated UI that makes a
product feel vibe-coded — and it sat next to *real* data we already had.

**P0 — Duplicate metric sections on the homepage.** A 7-item stats strip in the hero
*and* a dark "data strip" further down repeating four of the same numbers in a different
costume. Repeated generic sections, per the anti-vibe checklist.

**P1 — Job detail page ordered backwards.** The application-tracker form (a 10-field
panel) and "similar jobs" rendered *above* the job description. A badge row duplicated
the at-a-glance grid item-for-item. Users had to scroll past CRM furniture to read the
job they came for.

**P1 — Shared/typed URLs didn't work.** Natural URLs like `/jobs?visa_support=1` and
`/jobs?apply_from_abroad=1` (which even the product owner types) returned 200 but
silently ignored the filter — a hidden broken state.

**P2 — Part-time/service listings looked identical to professional roles** on cards,
making the YOLO inventory drag down perceived quality of the whole board.

**P2 — Smaller:** ranking explainer popover was unanchored; profile strength meter gave
a % but no next step; tracker kanban collapsed to an endless 1-column scroll on phones;
resume builder auto-saves but the UI implied manual saving; mixed emoji in chips.

**Solid as found (no churn):** profile page structure (numbered sections, sticky save
bar, privacy note), tracker's kanban/table/overdue logic, resume print CSS, glossary/
resources/guides hubs, SEO/JSON-LD, accessibility basics.

## 2. What was fixed

**Jobs page** (the core product):
- Filters now read in two tiers: the four decisions foreigners actually make
  (Japanese level, role family, employment type, prefecture) stay visible; the other
  six fold into a "More filters" disclosure that auto-opens when one is active.
- Quick chips cut 11 → 7, one per real decision, no emoji.
- Saved-searches row hidden until a search is saved; "Save search" moved into the form's
  action row as a quiet text button; prompts replaced alert() with toasts.
- Job cards rebuilt around decision hierarchy: title + fit → company · location ·
  **salary (bold, mono)** · date · source → only decision-critical badges (Japanese,
  visa, abroad, remote, English, non-full-time terms). Removed: role-family, career-level,
  posting-language (except a warning badge when the posting is in Japanese), video badge,
  redundant "Recommended" badge. Average badges per card: **8.6 → 4.3**.
- Part-time/temp jobs get a dashed, muted badge ("Part-time · entry-level") so service
  listings are identifiable at a glance and professional roles read as the default.
- "Why it fits" capped at 3 reasons, "Check:" at 2.
- Ranking explainer is a properly anchored popover with one-paragraph, plain-language copy.

**Job detail page:**
- Removed the badge row (duplicated the glance grid).
- Reordered to match how people decide: at-a-glance answers → apply/save/track actions
  (with the destination domain shown in mono under the Apply button for trust) →
  fit + salary context → profile match → **description/requirements** → similar jobs →
  tracker form last.

**Homepage:**
- Fake command center replaced with the **three real top-ranked jobs** (live titles,
  companies, fit scores, links) plus a one-line honest note on how ranking works.
- Stats strip cut 7 → 5 (all indexed, no Japanese, abroad, visa, professional — each a
  clickable real filter); the duplicate dark "data strip" section deleted along with its
  dead CSS. FAQ and all JSON-LD untouched.

**Profile:** strength meter is now actionable — "62% complete · Looking good · Next:
add your Japanese level and whether you need visa sponsorship."

**Tracker:** phones default to the table view (1-column kanban was an endless scroll);
applications in Applied/Screen/Interview with no follow-up date show a "Set a follow-up
date" nudge linking to the job's tracker panel — the missing "next action" cue.

**Resume builder:** input side only — "Save now" + "Auto-saves to this browser as you
type" so users trust the persistence model. Print layout untouched.

**Resource (/resources/applying-from-abroad):** "Start here" action box at the top
linking the three live filters (apply-from-abroad, visa support, professional+visa).

**URLs:** `?visa_support=1`, `?apply_from_abroad=1`, `?remote=1` are now real aliases
that filter (verified: 2,565 → 223 / 141 results).

## 3. Files changed

`app.py` (primary/secondary filter split, chips, URL aliases), `templates/index.html`,
`templates/job.html`, `templates/landing.html`, `templates/profile.html`,
`templates/tracker.html`, `templates/resume.html` (6 lines), `resources_new.py`,
`test_app.py` (new checks). No scrapers, no data logic, no brand tokens, no print CSS,
no SEO/JSON-LD, no new dependencies, no custom select controls.

## 4. Screens/pages checked

Rendered and inspected (server + test client; Playwright is unavailable in this sandbox,
so evidence was rendered HTML + the responsive CSS at every breakpoint): `/`, `/jobs`,
`/jobs?professional_only=1`, `/jobs?visa_support=1`, `/jobs?apply_from_abroad=1`,
YOLO detail (#575), JapanDev detail (#519), `/profile`, `/tracker`, `/resources`,
`/resources/applying-from-abroad`, `/resume`. Breakpoint behavior verified in CSS:
1440/1024 (filter grid 6→2 cols, detail 2→1 col at 900px), 768 and 390 (single-column
filters, in-flow multi-select panels, 2-col glance grid via auto-fit minmax(160px),
1-col hero, table-default tracker, 44px tap targets on primary actions).

## 5. Before / after, in one paragraph

Before: a visitor hit a wall of 11 chips, 10 dropdowns, and cards shouting 9 badges
each; the homepage showed an invented dashboard; a job page buried its description
under a CRM form; and the "honest data" story (Not stated vs stated) was undermined by
URLs that silently dropped filters. After: the jobs page leads with four filters and
seven presets, cards read title → salary → three decisive facts in under five seconds,
part-time service work is visibly secondary, the homepage hero shows three real
top-ranked jobs with real fit scores, the detail page answers "should I apply?" before
asking you to track anything, and every promoted URL actually filters.

## 6. Tests run and results

- `python test_app.py` — **60 checks, all pass** (inference, YOLO classification
  regressions, filter correctness incl. alias filtering and More-filters presence,
  homepage no-fake-feed assertions, 33 route checks).
- `python -m pytest -q` hits a RecursionError during *collection* in this sandbox
  (FUSE-mount artifact files, unrelated to the app); `python test_app.py` is the
  canonical runner.
- Live-server curl: all 13 URLs from the brief return **200**.
- Duplicate-ID scan across jobs/detail/home/tracker/profile: none.
- Manual: filters (professional/visa/abroad: 561/223/141 results), YOLO + JapanDev
  detail pages render with honest "Not stated" states, save/applied/hide/tracker JS
  untouched (same IDs/classes), localStorage schema unchanged, print CSS untouched.

## 7. Remaining UX debt (blunt)

- **The homepage is still long**: journey band + 6 value props + 8 tool cards + featured
  jobs + FAQ. It's all real content now, but it's a brochure; a future pass could cut it
  to hero + jobs + one proof section and let the nav carry the rest.
- **Value-prop and tool-card grids are uniform icon-card grids** — exactly the pattern
  Impeccable warns about. Real, but visually templated.
- The **`?ids=` localStorage pattern for /saved and /applied** re-queries 10k rows to
  count — fine at this scale, inelegant beyond it.
- **No screenshots** were possible in this environment; a real-browser pass (390px
  especially) should confirm the multi-select panels and sticky apply bar feel right.
- **Inferred vs explicit data** is only partially distinguished (visa "Mentioned" vs
  "Not stated"); a per-field "stated in posting / inferred from text" marker would be
  the next trust upgrade.
- The mobile drawer nav lists every section; fine, but order could be usage-weighted
  (Jobs/Tracker first).
