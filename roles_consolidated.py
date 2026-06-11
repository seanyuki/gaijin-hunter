"""
Consolidation of Role guides + Career roadmaps into a single page per role.

Goal (per product request): every professional role has ONE page that contains
both a written guide (like the SWE / Teaching guides) AND its career roadmap,
rendered on the same page.

How it works:
  * The role GUIDE is canonical, served at /guides/<slug>.
  * The matching ROADMAP (from content.ROADMAPS) is rendered to HTML and appended
    to the guide body as a "Career roadmap" section, with a TOC entry.
  * Three roles that previously existed only as roadmaps (Data/AI, Design,
    Engineering Management) get full new guides defined here.
  * /roadmaps and /roadmaps/<slug> redirect to the consolidated guide pages.

Nothing in the large content.py is edited; new guides and the merge logic live
here. Figures are 2025–26, grounded where researched (TokyoDev 2025 survey).
"""

import html as _html

# Map a guide slug -> the roadmap slug in content.ROADMAPS that belongs with it.
# (Most match 1:1; marketing-growth guide pairs with the 'marketing' roadmap.)
GUIDE_TO_ROADMAP_SLUG: dict[str, str] = {
    "software-engineering": "software-engineering",
    "product-management": "product-management",
    "finance-accounting": "finance-accounting",
    "sales-business-development": "sales-business-development",
    "marketing-growth": "marketing",
    "data-ai": "data-ai",
    "design": "design",
    "engineering-management": "engineering-management",
}

# Which guide slugs are *role* guides (used to decide whether to append a roadmap
# and for the "career roadmaps" grouping on the hub). Cities are excluded.
ROLE_GUIDE_SLUGS = list(GUIDE_TO_ROADMAP_SLUG.keys()) + ["teaching-english"]


# ---------------------------------------------------------------------------
# Three NEW role guides (previously roadmap-only). Full guide dicts, same shape
# as content.GUIDES entries: slug / category / icon / title / summary / updated
# / read_time / toc / body.
# ---------------------------------------------------------------------------

NEW_ROLE_GUIDES: list[dict] = [

    {
        "slug": "data-ai",
        "category": "Role",
        "icon": "database",
        "title": "Data & AI in Japan, the foreigner's guide",
        "summary": "Data science, ML engineering, analytics and the AI boom in Japan, who hires foreigners, the language reality, compensation that rivals software, and how to break in from abroad.",
        "updated": "June 2026",
        "read_time": "12 min",
        "key_takeaways": [
            "Data/AI is one of the <strong>most foreigner-accessible fields</strong>, technical, English-tolerant, and structurally short of talent, so visa sponsorship is normal.",
            "The closer to <strong>building models and infrastructure</strong>, the more English-first and better-paid; the closer to <strong>business analytics with Japanese stakeholders</strong>, the more Japanese needed.",
            "Employers: Japanese AI leaders (Preferred Networks, Sakana AI), data orgs at Mercari/LINE Yahoo/Rakuten, and global-tech Tokyo teams (Google, Amazon, Woven).",
            "Comp tracks software: <strong>¥7–11M</strong> mid-level, <strong>¥13M+</strong> at global tech, higher for strong ML engineers as generative AI pushes comp up.",
            "Break in with a <strong>portfolio</strong> (shipped models, open-source, papers) and a strong English CV + GitHub.",
        ],
        "faqs": [
            ("Is data science / AI a good field for foreigners in Japan?",
             "<p>Yes, it's among the most accessible, for the same reasons as software: the work is technical and English-tolerant, and Japan has a structural shortage of data scientists and ML engineers amid an aggressive corporate AI push. There's a visible homegrown scene (Preferred Networks, Sakana AI, Rinna) alongside every global cloud and AI lab building Tokyo teams, and demand outstrips local supply, which makes foreign hiring and visa sponsorship normal.</p>"),
            ("Do data and AI roles in Japan require Japanese?",
             "<p>Often not. At English-first product firms and global labs, JLPT is a nice-to-have, and ML/data <em>engineering</em> roles are frequently genuinely English-OK. The exception is <strong>analytics/BI embedded in Japanese business teams</strong>, where you present to Japanese stakeholders and N2+ helps a lot. If your Japanese is limited, target model- and infrastructure-building roles at English-first employers.</p>"),
            ("How much do data scientists and ML engineers earn in Japan?",
             "<p>Comp tracks software closely: roughly <strong>¥7–11M mid-level</strong> at Japanese product firms, <strong>¥13M+</strong> at global-tech Tokyo offices and for strong ML engineers, with the senior/research and no-Japanese-entity end stretching well beyond. The generative-AI surge has pushed top ML-engineer comp up sharply, specialised LLM and large-scale MLOps skills command a premium.</p>"),
        ],
        "toc": [
            ("overview", "Overview, a young, hungry market"),
            ("where-jobs", "Where the jobs are, named employers"),
            ("subfields", "The subfields and what they pay"),
            ("language", "The Japanese-language reality"),
            ("comp", "Compensation"),
            ("interview", "The interview loop"),
            ("breaking-in", "Breaking in from abroad"),
            ("skills", "Skills & stack in demand"),
        ],
        "body": """
<h2 id="overview">Overview, a young, hungry market</h2>
<p>Data and AI is one of the most foreigner-accessible fields in Japan, for the same reason as
software: the work is technical, English-tolerant, and talent is scarce. Japan has a structural
shortage of data scientists and ML engineers, an aggressive corporate push into generative AI, and a
visible homegrown AI scene (Preferred Networks, Sakana AI, Rinna) alongside every global cloud and
AI lab building Tokyo teams. Demand outstrips local supply, which is exactly the condition that makes
foreign hiring and visa sponsorship normal.</p>

<h2 id="where-jobs">Where the jobs are, named employers</h2>
<ul>
  <li><strong>Japanese AI/ML leaders:</strong> Preferred Networks (PFN), Sakana AI, Rinna, plus the
      data orgs at Mercari, LINE Yahoo, Rakuten, SmartNews, PayPay, CyberAgent.</li>
  <li><strong>Global tech with Tokyo data teams:</strong> Google, Amazon/AWS, Microsoft, Indeed,
      Woven by Toyota (autonomous-driving data), plus AI infra firms.</li>
  <li><strong>Foreign-capital & consulting:</strong> the data/AI practices of global consultancies,
      and foreign-capital firms standing up Japan analytics functions.</li>
  <li><strong>Fully remote (no Japanese entity):</strong> as with software, the highest-paying
      cohort, global AI/ML roles you do from Japan.</li>
</ul>

<h2 id="subfields">The subfields and what they pay</h2>
<table>
  <thead><tr><th>Subfield</th><th>What it is</th><th>Foreigner-friendly?</th></tr></thead>
  <tbody>
    <tr><td>ML / AI engineering</td><td>Building and shipping models, MLOps</td><td>★★★★★, most English-tolerant, highest paid</td></tr>
    <tr><td>Data science</td><td>Modeling, experimentation, inference</td><td>★★★★</td></tr>
    <tr><td>Data engineering</td><td>Pipelines, warehouses, platform</td><td>★★★★</td></tr>
    <tr><td>Analytics / BI</td><td>Dashboards, business stakeholder work</td><td>★★★, more Japanese, more stakeholder-facing</td></tr>
    <tr><td>Research scientist</td><td>Publishing, novel methods</td><td>★★★★ at AI labs; PhD-typical</td></tr>
  </tbody>
</table>
<div class="callout">The closer your role is to <strong>building models and infrastructure</strong>,
the more English-first and better-paid it is; the closer it is to <strong>business analytics with
Japanese stakeholders</strong>, the more Japanese it needs. Steer toward ML/data engineering if your
Japanese is limited.</div>

<h2 id="language">The Japanese-language reality</h2>
<p>At English-first product firms and global labs, JLPT is a nice-to-have. ML/data engineering roles
are often genuinely English-OK. The exception is <strong>analytics/BI embedded in Japanese business
teams</strong>, where you present to Japanese stakeholders and N2+ helps a lot. The pragmatic move
for a newcomer: target model/infra-building roles at English-first employers, and study Japanese
alongside to widen options later.</p>

<h2 id="comp">Compensation</h2>
<p>Data/AI comp tracks software closely and the same employer-type gap applies. Expect roughly
<strong>¥7–11M</strong> mid-level at Japanese product firms, <strong>¥13M+</strong> at global-tech
Tokyo offices and for strong ML engineers, and the senior/research and no-Japanese-entity end
stretching well beyond that. The generative-AI surge has pushed top ML-engineer comp up sharply, specialised skills (LLMs, MLOps at scale) command a premium. Check
<a href="/insights/salary">live salary insights</a> for current listings.</p>

<h2 id="interview">The interview loop</h2>
<p>Familiar to anyone who's interviewed for data roles globally: a technical screen (coding +
ML/stats fundamentals or a take-home), a modeling/case round, system/ML-system design for senior
roles, and behavioural. Research scientist roles weigh publications. At global firms it's English and
often fully remote for overseas candidates; expect a "why Japan" thread.</p>

<h2 id="breaking-in">Breaking in from abroad</h2>
<ol>
  <li>Target <strong>English-first employers</strong> (global tech, English-official Japanese product
      firms, AI labs) directly.</li>
  <li>Lead with a <strong>portfolio</strong>: shipped models, measurable impact, open-source, papers,
      Kaggle if relevant.</li>
  <li>A strong <strong>English CV + GitHub</strong> is usually enough, skip the Japanese-resume
      apparatus for these employers.</li>
  <li>Expect the standard <strong>2–4 month COE/visa timeline</strong> after offer
      (<a href="/living/coe-and-arrival">COE & arrival</a>).</li>
</ol>

<h2 id="skills">Skills & stack in demand</h2>
<p>Python is the lingua franca; PyTorch dominates research and increasingly production; SQL is
table stakes. In demand: <strong>LLMs / generative AI, MLOps (model deployment, monitoring), data
platform (Spark, dbt, cloud warehouses), and recommendation/ranking systems</strong> (huge at
Japan's consumer apps). Cloud (AWS/GCP) and the ability to take a model from notebook to production
are the differentiators that separate well-paid ML engineers from analysts.</p>
"""
    },

    {
        "slug": "design",
        "category": "Role",
        "icon": "pencil",
        "title": "Design in Japan, the foreigner's guide",
        "summary": "Product design, UX/UI, and the foreign designer's place in Japan, where English-first design teams exist, the bilingual research challenge, compensation, and how to break in.",
        "updated": "June 2026",
        "read_time": "11 min",
        "key_takeaways": [
            "Design is <strong>more language-sensitive than software</strong>, good product design depends on understanding (mostly Japanese) users, but a real, growing market exists at English-first firms.",
            "Most foreigner-friendly: <strong>product/UX and UI design, and especially design systems / design ops</strong> (least language-bound). UX research needs Japanese unless bilingual support exists.",
            "Employers: Mercari, SmartNews, LINE Yahoo, Rakuten, Money Forward, and global-tech Tokyo offices.",
            "Comp: <strong>¥6–9M</strong> mid-level, <strong>¥10–16M+</strong> senior/lead/design-management.",
            "<strong>Portfolio-first hiring</strong>, an outstanding portfolio opens doors a CV (and sometimes Japanese ability) can't.",
        ],
        "faqs": [
            ("Can foreign designers work in Japan?",
             "<p>Yes, though the market is narrower than engineering because design depends on understanding users, and most are Japanese. It's real and growing, concentrated at <strong>English-first product companies</strong> (Mercari, SmartNews, LINE Yahoo, Rakuten) and global-tech Tokyo offices. Foreign designers who thrive bring a strong portfolio plus either bilingual ability or a role where global/English product work dominates.</p>"),
            ("Which design roles are most open to foreigners in Japan?",
             "<p>The least language-bound are most accessible: <strong>design systems and design ops</strong> (★★★★★), then product/UX and UI design at English-first firms (★★★★). The hardest is <strong>UX research</strong>, interviewing Japanese users needs Japanese (or bilingual researchers/PMs), and brand/comms design for the Japanese market, which expects native-level cultural fluency. Steer toward craft, systems, and global-product work if your Japanese is limited.</p>"),
            ("Do I need a portfolio to get a design job in Japan?",
             "<p>Absolutely, more than any other role here, design hiring is portfolio-first. A foreign designer with a limited network but an outstanding portfolio can still get interviews at top Tokyo orgs. Show shipped products with your specific contribution, the problem and constraints, your process, and measurable outcomes. A strong portfolio with clear case studies beats both a fancy CV and (often) Japanese ability for English-first employers.</p>"),
        ],
        "toc": [
            ("overview", "Overview, a narrower but real market"),
            ("where-jobs", "Where the jobs are"),
            ("disciplines", "Disciplines & foreigner-friendliness"),
            ("language", "The language & user-research challenge"),
            ("comp", "Compensation"),
            ("portfolio", "The portfolio is everything"),
            ("interview", "The interview loop"),
            ("breaking-in", "Breaking in"),
        ],
        "body": """
<h2 id="overview">Overview, a narrower but real market</h2>
<p>Design is more language- and culture-sensitive than software, because good product design depends
on understanding users, and most of Japan's users are Japanese. That makes the foreign-designer
market narrower than engineering, but it's real and growing, concentrated at English-first product
companies and global tech. The foreign designers who thrive bring a <strong>strong portfolio plus
either bilingual ability or a role where global/English product work dominates</strong>.</p>

<h2 id="where-jobs">Where the jobs are</h2>
<ul>
  <li><strong>English-first Japanese product firms:</strong> Mercari, SmartNews, LINE Yahoo, Rakuten,
      Money Forward, mature design orgs that hire foreign designers and operate substantially in
      English.</li>
  <li><strong>Global tech Tokyo offices:</strong> Google, Amazon, Indeed, Microsoft, global design
      systems, English-first.</li>
  <li><strong>Foreign-capital SaaS & agencies:</strong> firms building global products from Tokyo, and
      design/branding agencies serving international clients.</li>
  <li><strong>Design systems / design ops / brand</strong> roles travel across language better than
      deep Japanese-user UX research.</li>
</ul>

<h2 id="disciplines">Disciplines & foreigner-friendliness</h2>
<table>
  <thead><tr><th>Discipline</th><th>Foreigner-friendly?</th><th>Note</th></tr></thead>
  <tbody>
    <tr><td>Product / UX design</td><td>★★★★ at English-first firms</td><td>Strong at Mercari-type orgs</td></tr>
    <tr><td>UI / visual design</td><td>★★★★</td><td>Craft travels across language</td></tr>
    <tr><td>Design systems / design ops</td><td>★★★★★</td><td>Least language-bound</td></tr>
    <tr><td>UX research</td><td>★★ unless bilingual</td><td>Interviewing Japanese users needs Japanese</td></tr>
    <tr><td>Brand / comms design (JP market)</td><td>★★</td><td>Native-level cultural fluency expected</td></tr>
  </tbody>
</table>

<h2 id="language">The language & user-research challenge</h2>
<p>The crux for foreign designers: <strong>you can design beautifully without Japanese, but you
can't research Japanese users without it</strong> (or without leaning on bilingual researchers/PMs).
At mature English-first design orgs this is solved, there are Japanese researchers and the team
operates in English. At smaller or domestic firms, the gap shows. If your Japanese is limited, target
companies with established bilingual design processes, and lean into craft, systems, and global-product
work where your output isn't gated by user-interview language.</p>

<h2 id="comp">Compensation</h2>
<p>Design comp runs below engineering but solid at the top firms: roughly <strong>¥6–9M</strong>
mid-level, <strong>¥10–16M+</strong> for senior/staff/lead and design management at English-first
product companies and global tech. Bilingual senior designers who can bridge global craft and the
Japanese market are scarce and command a premium. See <a href="/insights/salary">salary insights</a>.</p>

<h2 id="portfolio">The portfolio is everything</h2>
<p>More than any other role here, design hiring is <strong>portfolio-first</strong>. A foreign
designer with a limited network but an outstanding portfolio can still get interviews at top Tokyo
orgs. Make it: shipped products with your specific contribution called out, the problem/constraints,
your process, and measurable outcomes. A strong portfolio + clear case studies beats both a fancy CV
and (often) Japanese ability for the English-first employers.</p>

<h2 id="interview">The interview loop</h2>
<p>Expect a portfolio presentation (walk through 1–2 deep case studies), a design exercise/whiteboard
or take-home, a craft/critique round, and behavioural/collaboration rounds. At global and English-first
firms it's in English and often remote for overseas candidates. They probe how you work with PMs and
engineers and how you handle research and ambiguity.</p>

<h2 id="breaking-in">Breaking in</h2>
<ul>
  <li><strong>Lead with the portfolio</strong>, it opens doors a CV can't.</li>
  <li><strong>Target English-first design orgs</strong> (Mercari, SmartNews, global tech) and
      design-systems/ops roles if your Japanese is limited.</li>
  <li><strong>Internal transfer</strong> from your current company's global design team into Tokyo is
      a clean route.</li>
  <li><strong>Build some Japanese</strong>, it disproportionately widens the design market, where so
      much value is user-research-bound.</li>
</ul>
"""
    },

    {
        "slug": "engineering-management",
        "category": "Role",
        "icon": "users",
        "title": "Engineering management in Japan, the foreigner's guide",
        "summary": "Leading engineering teams in Japan as a foreigner, where EM roles open up, the language and cultural leadership challenge, compensation above the IC track, and the IC-vs-manager decision.",
        "updated": "June 2026",
        "read_time": "12 min",
        "key_takeaways": [
            "EM is well-paid but the <strong>most culture-sensitive role</strong> here, you lead people, navigate Japanese workplace norms, and often bridge a Japanese org and a global one.",
            "Foreign EMs thrive at <strong>English-first product companies and global-tech Tokyo offices</strong>, where the team operates in English and Western-style management is the norm.",
            "The <strong>IC track now reaches as high as management</strong> in level and pay, move into EM for a genuine love of people-leadership, not just the number.",
            "Comp: <strong>¥15–22M</strong> for line managers, higher for senior/director, often with equity at global firms.",
            "<strong>Internal promotion</strong> is the most common path; invest in Japanese and cultural fluency even where language isn't strictly required.",
        ],
        "faqs": [
            ("Can a foreigner be an engineering manager in Japan?",
             "<p>Yes, specifically at <strong>English-first product companies (Mercari, SmartNews, LINE Yahoo, Rakuten) and global-tech Tokyo offices</strong>, where the team operates in English and Western-style management is the norm. It's the most culture-sensitive role covered here, you handle performance conversations, conflict, and team morale, all deeply cultural, so foreign EMs are rarer and harder to place at traditional Japanese firms.</p>"),
            ("Should I go into management or stay an individual contributor in Japan?",
             "<p>At modern firms, the <strong>IC (individual contributor) track reaches as high as management</strong> in both level and pay, Staff/Principal engineers can out-earn line managers. So move into EM only if you genuinely prefer people-leadership. Management raises the Japanese/cultural stakes (you're leading people in context); the senior-IC path lets you reach high comp with lower language pressure if you'd rather keep building.</p>"),
            ("How much do engineering managers earn in Japan?",
             "<p>EM comp at English-first and global-tech firms runs roughly <strong>¥15–22M for line managers</strong>, higher for senior/group managers and directors, often with meaningful equity at global firms. It sits at or above the senior-IC band, but remember the IC track reaches similar numbers, so choose for the work, not just the figure.</p>"),
        ],
        "toc": [
            ("overview", "Overview, leadership across a culture gap"),
            ("where-jobs", "Where foreign EMs are hired"),
            ("ic-vs-em", "IC vs EM, the real trade-off"),
            ("language", "The language & cultural-leadership reality"),
            ("comp", "Compensation"),
            ("interview", "The interview loop"),
            ("breaking-in", "Getting into management here"),
            ("pitfalls", "Pitfalls for foreign managers"),
        ],
        "body": """
<h2 id="overview">Overview, leadership across a culture gap</h2>
<p>Engineering management is one of the higher-paid tracks in Japan, but it's also the most
culture-sensitive role in this set: you're leading people, navigating Japanese workplace norms,
giving feedback, and often bridging a Japanese organisation and a global one. Foreign EMs do well
specifically at <strong>English-first product companies and global-tech Tokyo offices</strong>, where
the team operates in English and Western-style management is the norm. At traditional Japanese firms,
foreign management is rarer and harder.</p>

<h2 id="where-jobs">Where foreign EMs are hired</h2>
<ul>
  <li><strong>English-first Japanese product firms:</strong> Mercari, SmartNews, LINE Yahoo, Rakuten,
      Money Forward, they run engineering in English and hire/promote foreign EMs.</li>
  <li><strong>Global-tech Tokyo offices:</strong> Google, Amazon, Indeed, Microsoft, Woven, global
      management culture, English-first.</li>
  <li><strong>Foreign-capital SaaS scaling Japan teams</strong>, needing a manager who bridges HQ
      and the local team.</li>
  <li><strong>Remote-leadership roles</strong> for global companies managing distributed teams from
      Japan.</li>
</ul>

<h2 id="ic-vs-em">IC vs EM, the real trade-off</h2>
<p>At modern firms, <strong>the IC (individual-contributor) track now reaches as high as
management</strong> in both level and pay, Staff/Principal engineers can out-earn line managers. So
the move into EM should be a genuine preference for people-leadership, not just a pay grab. Rough
comparison:</p>
<table>
  <thead><tr><th></th><th>Senior IC (Staff/Principal)</th><th>Engineering Manager</th></tr></thead>
  <tbody>
    <tr><td>Day-to-day</td><td>Deep technical work, architecture, influence</td><td>People, delivery, hiring, 1:1s, less coding</td></tr>
    <tr><td>Comp</td><td>¥13–22M+ at top firms</td><td>¥15–22M+, more at director level</td></tr>
    <tr><td>Language pressure</td><td>Lower</td><td><strong>Higher</strong>, leading people in context</td></tr>
    <tr><td>Best if</td><td>You love building</td><td>You love growing people & systems</td></tr>
  </tbody>
</table>

<h2 id="language">The language & cultural-leadership reality</h2>
<p>Management raises the Japanese stakes versus an IC role, because you're handling performance
conversations, conflict, stakeholder politics, and team morale, all deeply cultural. At English-first
orgs the working language is English and this is manageable; you still benefit enormously from
understanding Japanese workplace norms (indirect feedback, consensus-building / <em>nemawashi</em>,
face). At Japanese-language organisations, foreign EM roles are uncommon and typically require
business-to-fluent Japanese. Most successful foreign EMs operate in the English-first segment and
invest in cultural fluency even when language isn't strictly required.</p>

<h2 id="comp">Compensation</h2>
<p>EM comp at English-first and global-tech firms runs roughly <strong>¥15–22M</strong> for line
managers, higher for senior/group managers and directors, often with meaningful equity at global
firms. It sits at or above the senior-IC band, but remember the IC track reaches similar numbers, so
choose for the work, not just the number. See <a href="/insights/salary">salary insights</a>.</p>

<h2 id="interview">The interview loop</h2>
<p>Expect people-management rounds (how you grow, coach, and handle underperformance), delivery/
execution, technical depth (you still need credibility with engineers), cross-functional stakeholder
scenarios, and values/behavioural. In Japan, anticipate questions about <strong>leading across
cultures</strong> and managing a mixed Japanese/international team. English and often remote at global
firms.</p>

<h2 id="breaking-in">Getting into management here</h2>
<ul>
  <li><strong>Promote internally</strong>, the most common path; move into EM at your current
      English-first employer where you already understand the org and have the visa.</li>
  <li><strong>Transfer in as an EM</strong> from a global company's other office into its Tokyo team.</li>
  <li><strong>External EM hires</strong> happen at scaling firms, lead with shipped-team outcomes
      (teams grown, delivery, retention), not just technical CV.</li>
  <li><strong>Invest in Japanese & cultural fluency</strong> even at English-first firms, it's the
      difference between a manager the Japanese team tolerates and one they trust.</li>
</ul>

<h2 id="pitfalls">Pitfalls for foreign managers</h2>
<ul>
  <li><strong>Importing blunt Western feedback wholesale</strong>, direct public criticism lands
      harder in Japan; calibrate.</li>
  <li><strong>Skipping nemawashi</strong>, pushing decisions without quiet pre-alignment breeds
      resistance.</li>
  <li><strong>Assuming silence = agreement</strong>, it often isn't; create safe channels for dissent.</li>
  <li><strong>Neglecting the bilingual bridge</strong>, your job often includes translating between
      a Japanese team and a global HQ; do it deliberately.</li>
</ul>
"""
    },
]


def get_new_role_guide(slug: str):
    return next((g for g in NEW_ROLE_GUIDES if g["slug"] == slug), None)


def all_guides(base_guides: list) -> list:
    """Return the full guide list = content.GUIDES + the 3 new role guides,
    for the hub and the related-guides sidebar."""
    return list(base_guides) + NEW_ROLE_GUIDES


# ---------------------------------------------------------------------------
# Render a roadmap (content.ROADMAPS entry) to an HTML block appended to a guide.
# ---------------------------------------------------------------------------

def _esc(s) -> str:
    return _html.escape(str(s)) if s is not None else ""


def roadmap_html(roadmap: dict) -> str:
    """Render a roadmap dict to a self-contained HTML section (inline-styled)
    suitable for appending into a guide article body. Includes id="career-roadmap"
    so a TOC entry can link to it."""
    if not roadmap:
        return ""
    out = []
    out.append('<hr>')
    out.append('<h2 id="career-roadmap">Career roadmap, levels, pay & how to promote</h2>')
    out.append('<p>The guide above is the lay of the land; this is the ladder. Each level shows the '
               'typical years, salary band, the skills that define it, how to promote out of it, and '
               'Japan-specific notes.</p>')

    for st in roadmap.get("stages", []):
        out.append('<div style="background:var(--card); border:1px solid var(--line); '
                   'border:1px solid #eccfca; border-radius:10px; '
                   'padding:18px 20px; margin:14px 0;">')
        # header line: title + pills
        out.append('<div style="display:flex; justify-content:space-between; align-items:baseline; '
                   'flex-wrap:wrap; gap:8px; margin-bottom:8px;">')
        out.append(f'<strong style="font-size:17px;">{_esc(st.get("title"))}</strong>')
        out.append('<span style="display:flex; gap:6px; flex-wrap:wrap; font-size:12px;">')
        if st.get("years"):
            out.append(f'<span style="background:#eff6ff; color:#1e40af; padding:3px 10px; '
                       f'border-radius:999px; font-weight:600;">{_esc(st["years"])}</span>')
        if st.get("salary"):
            out.append(f'<span style="background:#ecfdf5; color:#166534; padding:3px 10px; '
                       f'border-radius:999px; font-weight:600;">{_esc(st["salary"])}</span>')
        out.append('</span></div>')
        # skills
        if st.get("skills"):
            out.append('<div style="font-size:12px; text-transform:uppercase; letter-spacing:0.05em; '
                       'color:var(--muted); margin:6px 0 4px;">Key skills</div>')
            out.append('<ul style="margin:0 0 6px; padding-left:20px;">')
            for s in st["skills"]:
                out.append(f'<li>{_esc(s)}</li>')
            out.append('</ul>')
        # promotion
        if st.get("promotion_to_next"):
            out.append('<div style="background:var(--warn-tint); border:1px solid #f0d9a8; '
                       'padding:8px 12px; border-radius:4px; margin-top:8px; font-size:13px; '
                       'color:#7c2d12; line-height:1.55;"><b>Promote out of this level:</b> '
                       f'{_esc(st["promotion_to_next"])}</div>')
        # japan specifics
        if st.get("japan_specifics"):
            out.append('<div style="background:var(--warn-tint); border:1px solid #f0d9a8; '
                       'padding:8px 12px; border-radius:4px; margin-top:8px; font-size:13px; '
                       'color:#78350f; line-height:1.55;"><b>Japan specifics:</b>'
                       '<ul style="margin:4px 0 0; padding-left:18px;">')
            for n in st["japan_specifics"]:
                out.append(f'<li>{_esc(n)}</li>')
            out.append('</ul></div>')
        out.append('</div>')

    # pivots
    if roadmap.get("common_pivots"):
        out.append('<h3 id="career-pivots">Common pivots from this track</h3>')
        out.append('<ul>')
        for p in roadmap["common_pivots"]:
            out.append(f'<li>{_esc(p)}</li>')
        out.append('</ul>')

    out.append('<div class="callout">Browse current openings on the '
               '<a href="/jobs">job board</a>, or check '
               '<a href="/insights/salary">live salary insights by role</a>.</div>')
    return "\n".join(out)


def consolidate_guide(item: dict, roadmaps: list) -> dict:
    """Append the matching roadmap (rendered HTML) + a TOC entry to a role guide.
    `roadmaps` is content.ROADMAPS. No-op for non-role guides (e.g. cities)."""
    if not item:
        return item

    def _with_faq_toc(d):
        # FAQ renders at the very bottom of every article, so its TOC entry is last.
        if d.get("faqs") and not any(a == "faq" for a, _ in d.get("toc", [])):
            d = dict(d)
            d["toc"] = list(d.get("toc", [])) + [("faq", "FAQ")]
        return d

    rm_slug = GUIDE_TO_ROADMAP_SLUG.get(item.get("slug"))
    if not rm_slug:
        # City / teaching guides: no roadmap, but still surface the FAQ in the TOC.
        return _with_faq_toc(item)
    roadmap = next((r for r in roadmaps if r["slug"] == rm_slug), None)
    if not roadmap:
        return _with_faq_toc(item)
    merged = dict(item)
    merged["toc"] = list(item.get("toc", [])) + [("career-roadmap", "Career roadmap, levels & pay")]
    merged["body"] = item.get("body", "") + roadmap_html(roadmap)
    return _with_faq_toc(merged)
