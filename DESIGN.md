---
name: Gaijin Hunter
description: A credible, Swiss-editorial career broadsheet for foreigners working in Japan.
version: 2.0 — consolidated canon (supersedes all token values elsewhere)
reference: design.html (visual companion — keep both in sync)
colors:
  vermilion: "#C93B2B"
  vermilion-dark: "#A82C1E"
  vermilion-soft: "#F6E2DE"
  vermilion-tint: "#FAEFEC"
  paper: "#F7F6F4"
  paper-deep: "#EFEDE9"
  card: "#FFFFFF"
  ink: "#111110"
  ink-soft: "#2C2B29"
  muted: "#79746C"
  muted-soft: "#98938B"
  line: "rgba(17,17,16,0.12)"
  line-soft: "rgba(17,17,16,0.07)"
  line-strong: "rgba(17,17,16,0.22)"
  good: "#2F7D5B"
  good-tint: "#EAF3EE"
  gold: "#B4690E"
  gold-tint: "#FBF1E3"
  ink-band: "#1B1813"
  ink-band-2: "#25201A"
  ink-band-card: "#2B251E"
  ink-band-fg: "#F6F2EA"
  ink-band-muted: "#B6AB9C"
  ink-band-link: "#F0B3AB"
typography:
  hero:
    fontFamily: "Barlow Condensed, Barlow, Arial, sans-serif"
    fontSize: "clamp(42px, 5.6vw, 72px)"
    fontWeight: 600
    lineHeight: 0.98
    letterSpacing: "-0.015em"
  display:
    fontFamily: "Barlow Condensed, Barlow, Arial, sans-serif"
    fontSize: "clamp(28px, 4vw, 40px)"
    fontWeight: 600
    lineHeight: 1.12
    letterSpacing: "-0.01em"
  h2:
    fontFamily: "Barlow Condensed, Barlow, Arial, sans-serif"
    fontSize: "clamp(21px, 2.4vw, 27px)"
    fontWeight: 600
    lineHeight: 1.18
  title:
    fontFamily: "Barlow, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "17px"
    fontWeight: 600
    lineHeight: 1.28
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Barlow, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.58
  label:
    fontFamily: "Barlow, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "11px"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.16em"
    textTransform: uppercase
  mono:
    fontFamily: "DM Mono, ui-monospace, SFMono-Regular, Menlo, monospace"
    fontSize: "12px"
    fontWeight: 500
    lineHeight: 1.4
    fontFeature: "tnum"
rounded:
  sm: "3px"
  md: "4px"
  lg: "6px"
  pill: "4px"
spacing:
  "2xs": "4px"
  xs: "8px"
  sm: "12px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  "2xl": "48px"
  "3xl": "64px"
  "4xl": "96px"
layout:
  content: "1100px"
  header: "1320px"
  measure: "68ch"
  breakpoints: ["560px", "740px", "900px", "1240px"]
shadows:
  ambient: "0 1px 1px rgba(17,17,16,0.04)"
  state: "0 2px 6px -2px rgba(17,17,16,0.10)"
  overlay: "0 10px 30px -16px rgba(17,17,16,0.22)"
motion:
  fast: "120ms"
  medium: "200ms"
  slow: "320ms"
  ease-standard: "cubic-bezier(0.2, 0, 0, 1)"
  ease-enter: "cubic-bezier(0.16, 1, 0.3, 1)"
  ease-exit: "cubic-bezier(0.4, 0, 1, 1)"
---

# Design System: Gaijin Hunter

**This file is the single source of truth.** Where any stylesheet, template, or older
document disagrees with a value here, this file wins. The visual companion is
`design.html` — every component documented here is rendered there. Update both
together or not at all.

## 1. Brand Personality

**Creative North Star: "The Bilingual Broadsheet."**

Gaijin Hunter behaves like a credible newspaper for the most disorienting decision of
someone's life — moving abroad to work in Japan. It is calm where job boards are
noisy, specific where relocation content is vague, and free of the account walls,
banner clutter, and recruiter-spam styling that make this category feel predatory.

Personality in five words: **credible, precise, warm, unhurried, generous.**

The product earns trust the way a good broadsheet does — through specific numbers set
in mono (¥9.5M, JLPT N2, 70/70 HSP points), through restraint with color, and through
typography and whitespace doing the work that gradients and mascots do in lesser
products. It never begs (no popups, no signup walls — there is no account at all),
never shouts (one accent color, rationed), and never decorates (no Japan kitsch; the
torii logomark is the single permitted motif, nowhere else).

## 2. Visual Direction

Swiss / Vignelli editorial on warm ground:

- A strict invisible grid; hairline rules do the structural work of shadows.
- Condensed display headlines (Barlow Condensed) against plain grotesque body
  (Barlow) — a *width* contrast, not a two-lookalike-sans pairing.
- Mono numerics (DM Mono, `tnum`) for every figure a user weighs a decision on.
- Exactly one color with opinions — Hinomaru Vermilion — behaving like a dateline
  or masthead rule, never a highlighter.
- Warm paper ground (`#F7F6F4`), warm near-black ink (`#111110`). Never pure black,
  never the cold slate of a SaaS dashboard.
- Flat at rest. When a moment demands drama, the page inverts to a dark sumi
  "ink-band" instead of stacking elevation.
- Tool-first density: this is a working product (job board, tracker, calculators,
  résumé builders), so tables can run long and panels can be dense — but every dense
  surface has a strict visual ranking (see The Signal Budget Rule).

Explicitly rejected: navy-and-purple generic SaaS; gradient-mesh heroes; glassmorphism;
identical icon-card grids; bubbly rounded cards; cherry blossoms, rising suns, anime,
decorative torii; stat counters without context; stock photography.

## 3. Typography

**Display:** Barlow Condensed (600–700) · **Body/UI:** Barlow (400–600) ·
**Data:** DM Mono (400–500). Load exactly these three families — nothing else.
(`Geist`, `Geist Mono`, and `Fraunces` are legacy; remove them from font loading.)

### Hierarchy
- **Hero** — Barlow Condensed 600, `clamp(42px, 5.6vw, 72px)`, line-height 0.98,
  `-0.015em`. Landing/hub mastheads only. One per page.
- **Display / H1** — Barlow Condensed 600, `clamp(28px, 4vw, 40px)`, `-0.01em`,
  `text-wrap: balance`. Page titles and major section heads.
- **H2** — Barlow Condensed 600, `clamp(21px, 2.4vw, 27px)`.
- **Title / H3** — Barlow 600, 17px. Card titles, panel labels.
- **Body** — Barlow 400, 14–15px, line-height 1.58. Reading measure capped at
  65–75ch (68ch default).
- **Label** — Barlow 600, 11–11.5px, `0.16em` tracked UPPERCASE. The `.eyebrow-rule`
  device and small field labels only — never per-section scaffolding.
- **Mono / Data** — DM Mono 500, 12–13px, `tnum`. Salaries, points, scores, dates,
  source tags, all comparative figures.

### Rules
- **The Mono-for-Money Rule.** Every decision number — yen, JLPT, HSP points,
  percentages, dates — is DM Mono with `tnum`. Prose numbers may stay in Barlow.
- **The Condensed-Heads Rule.** Headlines are Barlow Condensed; body and controls are
  Barlow. Never body copy or button labels in the condensed face; never a headline in
  the regular face. The width contrast *is* the system.
- **The One-Hero Rule.** One hero-size heading per page. If two things are set at
  hero scale, neither is the hero.

## 4. Color Palette

A near-monochrome warm ink-on-paper palette with one decisive vermilion.

### Primary
- **Hinomaru Vermilion** `#C93B2B` — the single brand voice: primary buttons,
  active-nav underline, masthead hairline, status dots, current pagination,
  `::selection`. Its rarity is the point.
- **Vermilion Dark** `#A82C1E` — hover/pressed for vermilion fills; the accessible
  prose-link color (body links are ink by default; underlined vermilion-dark for
  emphasis links in articles).
- **Vermilion Soft / Tint** `#F6E2DE` / `#FAEFEC` — faint washes for accent badges,
  chip hover, focus-ring glow. Never a large fill.

### Neutrals
- **Sumi Ink** `#111110` — all primary text. Warm near-black; never `#000`.
- **Ink Soft** `#2C2B29` — secondary text, ghost-button labels.
- **Muted** `#79746C` / **Muted Soft** `#98938B` — meta, captions, placeholders.
  `#79746C` (≈4.6:1 on paper) is the floor for anything users must read.
- **Paper** `#F7F6F4` (ground) · **Paper Deep** `#EFEDE9` (recessed sections, badge
  fills) · **Card** `#FFFFFF` (raised surfaces).
- **Hairlines** — ink-alpha: Line `rgba(17,17,16,0.12)`, Soft `0.07`, Strong `0.22`.

### Semantic (data, not decoration)
- **Good Green** `#2F7D5B` on `#EAF3EE` — high fit, visa-friendly, applied.
- **Caution Gold** `#B4690E` on `#FBF1E3` — mid fit, low-salary flags.
- **Vermilion soft** doubles as low-fit. Every semantic state pairs color with an
  icon, label, or mono value — never hue alone (color-blind safety).

### Ink-Band (inverted editorial surface)
`#1B1813 → #25201A` ground, `#2B251E` cards, `#F6F2EA` text, `#B6AB9C` muted,
`#F0B3AB` links. For hero drama and final CTAs, gridded with faint hairlines.

### Rules
- **The One Voice Rule.** Vermilion on ≤10% of any screen. If two elements are
  vermilion and only one is the primary action, one of them is wrong.
- **The Warm-Ink Rule.** No pure black, no cool slate/blue-gray. Cool gray reads as
  generic SaaS and is forbidden.

## 5. Spacing Scale

Base-4 scale. Use tokens, never arbitrary values:

`2xs 4px · xs 8px · sm 12px · md 16px · lg 24px · xl 32px · 2xl 48px · 3xl 64px · 4xl 96px`

- Card internal padding: `md–lg` (16–24px; the standard card is 18px 20px).
- Between related elements (label→input, title→meta): `2xs–xs`.
- Between siblings in a list/grid: `sm–md`.
- Between page sections: `2xl–3xl` desktop, `xl–2xl` mobile.
- Section rhythm is asymmetric on purpose: more space *above* a section head than
  below it (e.g. 64px above, 24px below), so heads bind to their content.

## 6. Border Radius

Low and precise — nothing bubbly: **sm 3px** (badges, chips, tags) · **md 4px**
(buttons, inputs, small controls) · **lg 6px** (cards, panels, dropdowns).
There is no true pill: the "pill" token is 4px. Never exceed 6px on any surface.
The single exception is the circular status dot / progress ring, which is data.

## 7. Shadows / Elevation

Flat, hairline-first. Surfaces are flat at rest; structure comes from 1px ink-alpha
borders and the grid. Shadows are a *response to state*, never resting decoration.

- **Ambient** `0 1px 1px rgba(17,17,16,0.04)` — faintest seat under filter panels.
- **State** `0 2px 6px -2px rgba(17,17,16,0.10)` — card/tool hover feedback.
- **Overlay** `0 10px 30px -16px rgba(17,17,16,0.22)` — dropdowns, command palette,
  toasts; things that genuinely float.
- **Accent glow: none.** Buttons never glow.

**The Hairline-Does-the-Work Rule.** If a boundary can be a rule, it is a rule.
**The Invert-Don't-Lift Rule.** For emphasis, switch to the ink-band; never pile on
shadow or scale.

## 8. Layout Principles

- **Content column:** 1100px max, 24px gutters (16px under 560px). Header runs wider
  at 1320px. Reading measure inside any column: ≤68ch.
- **Grid:** 12-column mental model; listings are single-column cards with a left
  monogram rail; hubs use 2–3 column card grids that collapse (3→2 at 1240px,
  2→1 at 740px).
- **Hairline architecture:** sections separate with 1px rules or a `paper-deep`
  band — never with decorative dividers, waves, or angle cuts.
- **Density with ranking:** dense surfaces are welcome, but every surface must have
  a single dominant scan path: title → decision numbers (mono) → action. If
  everything is emphasized, redesign the surface.
- **One editorial moment per page:** at most one ink-band and at most one hero per
  page. Everything else sits on paper.
- **The Section-Variety Rule.** Never stack more than two "template-shaped" sections
  (stat row, N-step icon row, FAQ accordion, CTA band) in sequence. Adjacent sections
  must differ in layout structure, not just content — this is the primary defense
  against the AI-template look.

## 9. Components

Reference renderings for all of these live in `design.html`.

### Buttons
- **Primary** — vermilion fill, white text, 1px vermilion border, 4px radius,
  600 weight, ~13px 24px padding. Hover → Vermilion Dark. No transform, no glow.
- **Secondary** — transparent, ink text, 1px line-strong border. Hover → paper-deep
  fill, border firms to ink.
- **Ghost** — text-only, ink-soft. Hover → vermilion-dark text.
- **On-ink** — white fill, ink text, for ink-band surfaces only.
- Sizes: default 13px 24px; compact 8px 14px (toolbars, inline actions).

### Chips & Badges
- Small squared labels (3px radius), 1px hairline border, mono for data values.
- **Neutral badge:** paper-deep fill, ink-soft text.
- **Accent badge:** vermilion-tint fill + 6px vermilion status dot (remote, applied).
- **Fit badge:** mono `tnum`, semantic green/gold/vermilion-soft. Reads as data.
- **The Signal Budget Rule.** A listing card shows **at most 3 badge signals**:
  the fit score, one accessibility badge (visa support > apply-from-abroad >
  remote), and — in the archived view only — the archived marker. Everything else
  (language levels, contract type, industry tags, "new", source) scans as mono
  text in the facts row or lives on the detail page. If a fourth badge seems
  essential, one of the current ones isn't.

### Cards
- White surface, 1px line border, 6px radius, ~18px 20px padding, flat at rest.
- Hover: border firms to line-strong + State shadow. No lift, no scale.
- Nested cards are forbidden. Job cards lead with the company monogram rail
  (`.gh-mono` — rounded-square initial tile; real logo on a white tile when
  available), then title + fit badge, then one meta line (company in 600, then
  location · date · source), then the **facts row** (`.job-facts`) — the card's
  scan layer: salary leading in ink, then Japanese level, remote, apply-from-abroad,
  all DM Mono `tnum`; quiet extras trail in muted — then the ≤3 permitted badge
  signals, then actions.
- **Results bar** (`.results-bar`): above any listing, one quiet row — result
  count in mono + the sort control right-aligned. The count is the page's only
  bold number outside cards.

### Inputs
- White field, 1px line-strong border, 4px radius, 9px 11px padding. Native
  `<select>` normalized with an inline SVG caret so all controls match.
- Focus: vermilion border + 3px vermilion-tint ring — identical across input,
  search, textarea, select.
- Disabled: 55% opacity, paper-deep fill, `not-allowed` cursor.
- Error: gold border + gold-tint ring + message with icon below the field. Vermilion
  is *not* the error color (it's the brand voice); gold flags caution, and a
  destructive/blocking error uses vermilion-dark text with an icon, not a red field.

### Navigation
- Sticky white header on a 1px line, topped by the signature 3px vermilion→gold
  masthead hairline. Hover-reveal dropdowns (fast, origin-aware).
- Links ink-soft; hover → paper-deep fill; active → vermilion with 2px vermilion
  underline. Below 900px: right-side drawer with hamburger.

### Tables / Listings
- Hairline row separators only (no zebra striping). Column heads in Label style
  (tracked caps 11px). All numeric columns mono + right-aligned. Row hover:
  paper-deep wash. Long tables are a feature, not a problem.

### Empty States
- Paper-deep panel, 1px line, one Display-size line, one body line, one primary
  action. No illustrations, no sad mascots. Empty states may show a useful next step
  (e.g. "3 saved searches will appear here — start from the jobs board").

### Status / Feedback
- **Success:** good-green text + icon on good-tint wash.
- **Warning:** gold + icon on gold-tint.
- **Error:** vermilion-dark text + icon on vermilion-tint (text-level, not a wall
  of red).
- **Toast:** sumi-ink pill, bottom-right (bottom-stretch mobile), `aria-live`,
  blur-in enter, auto-dismiss, reduced-motion safe.
- Never a full-width colored banner with a side-stripe; use tint wash + icon + text.

### Signature Devices
- **Logomark** — geometric abstracted torii on sumi rounded square. The single
  permitted Japan motif; never repeated as decoration.
- **Eyebrow rule** — short vermilion bar + tracked-caps label. A deliberate section
  marker, rationed.
- **Ink-band** — the inverted editorial surface (one per page max).
- **Company monogram** — initial tile anchoring job cards.

## 10. Hover / Focus / Active States

Every interactive element defines all four states; the language is uniform:

- **Hover** — value shift, not motion: fills darken one step (vermilion→vermilion-
  dark), transparent surfaces gain paper-deep, borders firm one step, cards gain the
  State shadow. Never translate/scale on hover.
- **Focus-visible** — one language everywhere: vermilion border/outline + 3px
  vermilion-tint ring. Keyboard focus is never removed, only styled.
- **Active/pressed** — uniform `scale(0.97)` at 120ms. The only transform in the
  system.
- **Selected/current** — vermilion: nav underline, active tab border, current page.
- **Disabled** — 55% opacity, no hover response, `not-allowed`.

### Interaction Contracts
Every component of a given kind honors the same behavioral contract:

- **Dialog contract** (drawers, sheets, palettes): `role="dialog"` +
  `aria-modal`, Tab trapped inside, Escape closes, body scroll locked, and on
  close focus returns to the trigger. Implemented once as `ghFocusContract()`
  in `base.html` — never re-implement per surface.
- **Toggle contract** (save star, mark-applied, any on/off control):
  `aria-pressed` kept in sync with visual state wherever the class toggles.
- **Pending contract** (any async/submit action): set `aria-busy="true"` on
  the button — the shared rule dims it, blocks re-press, and shows a progress
  cursor. Never disable the button (that drops focus).
- **Error contract** (form fields): `aria-invalid="true"` on the field (gold
  border/ring via the shared rule, never vermilion) + a `.field-error` message
  linked with `aria-describedby`.
- **Menu contract** (hover dropdowns): trigger carries `aria-haspopup` +
  `aria-expanded`; opens on hover/focus-within, Escape closes and refocuses
  the trigger.
- **Current-page contract**: active nav/tab links carry `aria-current="page"`,
  not just the `.active` class.
- **Touch contract**: on coarse pointers every tap control clears ~44px
  (shared `@media (pointer: coarse)` block).
- Assistive-only text uses the `.visually-hidden` utility; `title` alone is
  never the only explanation of a value.

## 11. Motion

Motion conveys state; it never decorates.

- **120ms** taps, presses, hovers · **200ms** dropdowns, expanders, card state ·
  **320ms** toasts, larger reveals. Nothing exceeds 350ms.
- Easing: `ease-enter cubic-bezier(0.16,1,0.3,1)` for arrivals,
  `ease-standard cubic-bezier(0.2,0,0,1)` for state change,
  `ease-exit cubic-bezier(0.4,0,1,1)` for departures. No bounce, no elastic.
- No orchestrated page-load sequences, no scroll-triggered entrance animations, no
  parallax. Content is present when the page is.
- Every animation has a `prefers-reduced-motion` path: durations collapse to ~0,
  end states remain.

## 12. Mobile Responsiveness

Breakpoints: **1240px** (3→2 col grids, header compresses) · **900px** (nav → drawer)
· **740px** (2→1 col, header CTA moves into drawer, filters collapse to a sheet) ·
**560px** (16px gutters, type steps down via the existing clamps).

- Touch targets ≥44px; card actions get full-width tap areas on mobile.
- The jobs filter bar collapses to a single "Filters" button opening a bottom sheet;
  applied filters render as removable chips above results.
- Tables that can't reflow become stacked label/value cards — never horizontal
  scroll for primary content.
- Sticky elements are rationed on mobile: header only. No sticky CTAs covering
  content.
- Hero type uses the clamps defined in §3 — never a separate mobile font ladder.
- Toasts stretch bottom-full-width. Drawers and sheets respect safe-area insets.

## 13. Do / Don't — Anti-Generic Guardrails

### Do
- Keep vermilion ≤10% of any screen (One Voice Rule).
- Set every decision number in DM Mono `tnum` (Mono-for-Money Rule).
- Reach for a 1px hairline before a shadow (Hairline-Does-the-Work Rule).
- Invert to ink-band for drama (Invert-Don't-Lift Rule).
- Cap listing cards at 3 signals (Signal Budget Rule).
- Give every stat a unit and a context label — "2,565 jobs indexed · updated daily",
  never a naked counter row (No-Naked-Numbers Rule).
- Vary adjacent section layouts (Section-Variety Rule).
- Keep radii 3–6px; pair every semantic color with icon/label/value.
- Use the identical vermilion focus ring on every control.

### Don't
- Don't look like generic SaaS: no navy-and-purple, gradient-mesh heroes,
  hero-metric templates, identical icon-card grids, or three-column
  feature-with-icon rows.
- Don't use gradient text, glassmorphism, decorative blurs, or pure-black/cold-slate
  neutrals.
- Don't add job-board clutter: no banner density, popups, urgency ribbons
  ("3 people viewing!"), or signup walls. There is no account; never render
  account-shaped UI.
- Don't use Japan kitsch: no cherry blossoms, rising suns, anime, decorative torii,
  vertical-text ornaments, or hanko stamps. The logomark is the only motif.
- Don't use colored side-stripe borders on cards/alerts; use full border, tint wash,
  status dot, or monogram.
- Don't put the eyebrow label above every section — it's a device, not scaffolding.
- Don't set body/buttons in Barlow Condensed or headlines in regular Barlow.
- Don't animate on scroll, lift on hover, or glow under buttons.
- Don't exceed 3 badges on a listing card, ever — density is organized, not loud.
- Don't ship a page whose sections could be swapped into any startup template
  without anyone noticing. If a section looks like a template block, restructure it
  around the actual content (a real salary table beats a "trusted by" strip).
