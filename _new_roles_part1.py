# New role guides — Part 1: Product Management, Marketing, Finance, Sales
# These are appended to GUIDES in content.py

NEW_ROLE_GUIDES = [

    # ============================================================ Product Management
    {
        "slug": "product-management",
        "category": "Role",
        "icon": "clipboard",
        "title": "Product management in Japan — the foreigner's guide",
        "summary": "PM jobs in Japan are scarcer than engineering — but bilingual PMs are heavily oversubscribed on the demand side. Who's actually hiring, what the comp looks like, and how to get in if you weren't already on the inside.",
        "updated": "May 2026",
        "read_time": "10 min",
        "toc": [
            ("market", "The 2026 PM market"),
            ("companies", "Companies hiring foreign PMs"),
            ("comp", "Compensation by level"),
            ("getting-in", "How foreigners actually get PM roles"),
            ("japanese", "Japanese language reality"),
            ("interview", "Interview process"),
            ("flavors", "PM flavors — product, growth, platform"),
            ("pivots", "Pivoting into PM from another role"),
        ],
        "body": """
<h2 id="market">The 2026 PM market</h2>
<p>Product management is a structurally smaller field in Japan than in the US — by
headcount, by job-post volume, and by recruiter coverage. Three reasons:</p>
<ul>
  <li><strong>Engineering-led culture.</strong> Most Japanese tech companies — including
      Rakuten, LINE Yahoo, Cybozu, Cyberagent — historically delegated product decisions
      to engineering managers or business-side <em>jigyō kikaku</em> (事業企画) planning
      roles, not standalone PMs.</li>
  <li><strong>Late adoption.</strong> Modern "Silicon Valley" PM came to Japan through
      Mercari, SmartNews, and the foreign-cap entrants (Google, Amazon, Stripe,
      Indeed). The function is roughly a decade younger than in the US.</li>
  <li><strong>Bilingual filter.</strong> Most PM roles outside FAANG Tokyo require
      working with Japanese stakeholders, so Japanese-language capacity narrows the
      candidate pool significantly relative to engineering.</li>
</ul>
<p>The flip side: demand is growing fast, and bilingual / Japan-experienced PMs are
heavily sought after. Mercari, PayPay, LINE Yahoo, and Cyberagent all expanded their
PM headcount through 2025 — and Robert Walters' 2026 sector report flags
<em>Senior Product Manager (bilingual)</em> as a top-five demand role in technology &
online.</p>

<h2 id="companies">Companies hiring foreign PMs</h2>
<h3>Tier 1 — actively hire foreign / bilingual PMs</h3>
<table>
  <thead><tr><th>Company</th><th>PM org size</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>Mercari</td><td>~80 PMs across product orgs</td>
        <td>Internal product language is English; some teams are 50%+ non-Japanese.</td></tr>
    <tr><td>PayPay</td><td>~60 PMs</td>
        <td>Bilingual PMs in heavy demand; recent JV with LINE Yahoo expanded scope.</td></tr>
    <tr><td>SmartNews</td><td>~25 PMs</td>
        <td>English-language product org; news distribution and LLM applications.</td></tr>
    <tr><td>Indeed Tokyo</td><td>~50 PMs</td>
        <td>Roughly 70% non-Japanese PMs; product language is English.</td></tr>
    <tr><td>Google Japan</td><td>varies</td>
        <td>APAC PM org based in Roppongi; comp at US-equivalent levels.</td></tr>
    <tr><td>Amazon Japan</td><td>varies</td>
        <td>Multiple product orgs (retail, AWS, Audible); bilingual preferred but
        English-only roles exist.</td></tr>
    <tr><td>Stripe Tokyo</td><td>small but growing</td>
        <td>Some product roles open to overseas applicants.</td></tr>
  </tbody>
</table>
<h3>Tier 2 — Japanese companies with growing PM functions</h3>
<ul>
  <li><strong>Cyberagent</strong> — large product org across gaming, ad-tech, media.
      Japanese-first but some teams welcome bilingual PMs.</li>
  <li><strong>DeNA</strong> — product across gaming, healthcare, mobility. Some
      bilingual divisions.</li>
  <li><strong>Money Forward</strong> — fintech B2B/B2C; PMs are mostly Japanese but
      English-friendly bilinguals are recruited.</li>
  <li><strong>Rakuten</strong> — officially English-as-corporate-language; PM roles
      span 70+ services. Japanese is helpful but not always required.</li>
  <li><strong>LINE Yahoo Japan</strong> — large product org post-merger; English-OK
      teams exist on the LINE side.</li>
</ul>
<h3>Tier 3 — startups</h3>
<p>Series B+ Japanese startups that hire foreign PMs include Autify, Helpfeel,
Algomatic, Atrae, Studist, and CADDi. Comp ranges are lower (¥7–11M at mid-level)
but equity packages can be meaningful.</p>

<h2 id="comp">Compensation by level</h2>
<table>
  <thead>
    <tr><th>Level</th><th>Years</th><th>Median TC (¥M/yr)</th><th>Top of band (¥M/yr)</th></tr>
  </thead>
  <tbody>
    <tr><td>Associate PM</td><td>0–2</td><td>6.5</td><td>9 (FAANG)</td></tr>
    <tr><td>PM</td><td>2–5</td><td>10</td><td>15 (FAANG)</td></tr>
    <tr><td>Senior PM</td><td>5–9</td><td>14</td><td>22 (FAANG)</td></tr>
    <tr><td>Group / Principal PM</td><td>9+</td><td>19</td><td>30 (FAANG)</td></tr>
    <tr><td>Director of Product</td><td>10+</td><td>25</td><td>40+ (FAANG)</td></tr>
  </tbody>
</table>
<p>FAANG Tokyo PM bands materially exceed Japanese-headquartered employer bands at
every level. The gap widens at senior and above — a Senior PM at Google Japan with
RSUs can clear ¥25M, while the same role at Mercari sits in the ¥14–18M band.</p>

<h2 id="getting-in">How foreigners actually get PM roles</h2>
<p>Three dominant entry paths:</p>
<ol>
  <li><strong>Internal pivot at a foreigner-friendly company.</strong> Mercari, PayPay,
      Indeed, and SmartNews regularly promote engineers and designers into PM roles.
      Entering as an engineer and pivoting after 1–2 years is the most common path.</li>
  <li><strong>Direct hire from abroad — FAANG.</strong> Google APAC, Amazon Japan, and
      Stripe Tokyo run global PM recruiting and accept overseas applications. Time-to-
      offer is 6–10 weeks with full visa relocation.</li>
  <li><strong>Bilingual hire from a competitor.</strong> Most domestic Japanese tech
      companies prefer to poach experienced PMs from peers (Mercari → Cyberagent,
      Cyberagent → DeNA) rather than train newcomers. Bilingual capacity opens this
      door.</li>
</ol>
<div class="callout">
  Two paths to avoid wasting time: (a) cold applying to a Japanese conglomerate for
  a "<em>sōgō shokku</em>" (総合職, all-rounder) track that won't translate to PM, and
  (b) joining a "product planning" (商品企画 / 事業企画) role at a non-tech firm that
  doesn't map to modern PM career capital outside Japan.
</div>

<h2 id="japanese">Japanese language reality</h2>
<table>
  <thead><tr><th>Company tier</th><th>Japanese required?</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>FAANG Tokyo</td><td>No (English OK)</td>
        <td>Stakeholder work happens in English; some teams have Japanese-speaking
        designers/engineers but PM communication norm is English.</td></tr>
    <tr><td>Mercari / SmartNews / PayPay</td><td>Useful, not required</td>
        <td>You can do the job in English; Japanese helps with cross-functional
        stakeholder meetings.</td></tr>
    <tr><td>Indeed Tokyo</td><td>No</td>
        <td>Documentation and most rituals in English.</td></tr>
    <tr><td>Cyberagent / DeNA / Rakuten</td><td>N3+ recommended</td>
        <td>You'll work with mostly Japanese teams; key meetings in Japanese.</td></tr>
    <tr><td>Domestic Japanese SaaS (Money Forward, Cybozu)</td><td>N2+ usually required</td>
        <td>Customer research is in Japanese; sales/CS handoffs are in Japanese.</td></tr>
  </tbody>
</table>
<p>Practical recommendation: aim for N3 by month 12 in Japan. It opens the Tier 2
employers and unlocks pay bumps via job changes.</p>

<h2 id="interview">Interview process</h2>
<p>The typical PM loop at a foreigner-friendly Japanese tech company:</p>
<ol>
  <li><strong>Recruiter screen</strong> (30 min) — English or Japanese, depending.
      Confirms PM track-record and visa status.</li>
  <li><strong>Hiring-manager interview</strong> (45–60 min) — PM career, why-this-
      company, why-PM, recent project deep-dive.</li>
  <li><strong>Product case study</strong> (60 min) — typically a take-home (1 week)
      followed by a 60-min walkthrough. Prepare for Japan-context cases (e.g.
      <em>"How would you improve onboarding in Mercari for first-time sellers?"</em>).</li>
  <li><strong>Cross-functional panel</strong> (45–60 min × 2–3) — meet engineering,
      design, data partners.</li>
  <li><strong>Leadership / bar-raiser</strong> (45 min) — VP of Product or equivalent.</li>
</ol>
<p>Average elapsed time: 3–5 weeks at gaishikei, 5–8 weeks at Japanese employers.
Mercari publishes a 4-week median for PM roles. Expect the case to be the highest-
leverage round — prepare 3 detailed PM stories using a structure like CIRCLES or
your own STAR variant, and be ready to defend metrics choices in Japanese-context
ambiguity.</p>

<h2 id="flavors">PM flavors — product, growth, platform</h2>
<ul>
  <li><strong>Core / Product PM</strong> — feature discovery, customer research, owning
      a slice of the product. Most common at Mercari, SmartNews, PayPay.</li>
  <li><strong>Growth PM</strong> — funnel, retention, conversion, A/B testing. Heavy
      data fluency required. Cyberagent, DeNA, and Mercari all run growth PM tracks.</li>
  <li><strong>Platform / Infrastructure PM</strong> — internal-facing products
      (developer platforms, payment rails, data infrastructure). Indeed, PayPay,
      and FAANG Tokyo all hire heavily here. Comp tends to be the highest of the three
      flavors.</li>
  <li><strong>B2B / Enterprise PM</strong> — Cybozu, Money Forward, Sansan, freee. Heavy
      customer interview cycles in Japanese; ramp curve is longer.</li>
  <li><strong>AI / ML PM</strong> — newest flavor, hottest demand. Sakana AI, PFN,
      Cyberagent's AI lab, and FAANG Tokyo's AI teams all hire.</li>
</ul>

<h2 id="pivots">Pivoting into PM from another role</h2>
<p>The 80/20 of internal pivots we've seen:</p>
<ul>
  <li><strong>Engineer → PM</strong> works best when you've shipped 2+ projects with
      meaningful product input. Ask to shadow your PM for one quarter, then propose
      owning one feature area.</li>
  <li><strong>Designer → PM</strong> works at design-led companies (SmartNews, Stripe).
      You'll need to ramp on metrics, A/B testing, and SQL.</li>
  <li><strong>Consultant → PM</strong> — common in Japan because top-of-class management
      consultants get poached into PM at Mercari and FAANG Tokyo. Strong
      structured-thinking signal, weak shipping signal — close the gap by side-
      projecting.</li>
  <li><strong>Sales / CS → PM</strong> harder but possible at B2B SaaS. You bring
      customer empathy and discovery rigor; you need to ramp on technical fluency and
      data.</li>
</ul>
<div class="callout">
  Build your career roadmap with the
  <a href="/roadmaps/product-management">Product Management roadmap</a> — five stages
  with explicit promotion criteria, salary bands, and Japan-specific notes.
</div>
""",
    },

    # ============================================================ Marketing & Growth
    {
        "slug": "marketing-growth",
        "category": "Role",
        "icon": "rocket",
        "title": "Marketing & growth in Japan — the foreigner's guide",
        "summary": "Foreigners can build strong marketing careers in Japan, but the playbook is different from the US/EU. Performance marketing, brand marketing, content, and growth — what's hiring, what pays, and what bilingual capacity unlocks.",
        "updated": "May 2026",
        "read_time": "10 min",
        "toc": [
            ("market", "The 2026 marketing market"),
            ("flavors", "Marketing flavors in Japan"),
            ("companies", "Companies actively hiring"),
            ("comp", "Compensation by level"),
            ("japanese", "Japanese language and culture"),
            ("channels", "Channel landscape — what's different in Japan"),
            ("entry", "How foreigners enter the field"),
            ("pivots", "Common pivots"),
        ],
        "body": """
<h2 id="market">The 2026 marketing market</h2>
<p>Japan's marketing industry is large — Dentsu, Hakuhodo, and ADK still dominate
ad spend — but the modern in-house digital marketing function is comparatively
young. The Robert Walters 2026 report flags marketing as one of three sectors with
the strongest hiring momentum, especially for bilingual digital marketers, brand
managers in luxury/FMCG, and performance marketing leaders.</p>
<p>Three structural shifts opening doors for foreigners:</p>
<ul>
  <li><strong>D2C and SaaS verticals.</strong> Modern in-house marketing teams at
      Mercari, PayPay, SmartNews, Money Forward, and freee mirror US-style growth
      orgs and welcome foreign talent.</li>
  <li><strong>Inbound tourism &amp; cross-border.</strong> Brands targeting overseas
      consumers (luxury, sake, retail tourism) hire foreign marketers for English /
      Chinese / Korean content production.</li>
  <li><strong>Foreign-cap entrants.</strong> Stripe, Notion, Figma, Datadog, Snowflake,
      HubSpot — most have Japan marketing teams now and recruit bilingual foreigners
      heavily.</li>
</ul>

<h2 id="flavors">Marketing flavors in Japan</h2>
<table>
  <thead><tr><th>Flavor</th><th>Typical employers</th><th>JP required?</th></tr></thead>
  <tbody>
    <tr><td>Performance / paid acquisition</td>
        <td>Mercari, PayPay, Cyberagent, SmartNews</td>
        <td>N2+ usually required for client / agency work</td></tr>
    <tr><td>Brand &amp; comms</td>
        <td>Luxury (LVMH brands, Burberry), FMCG (P&amp;G, Unilever Japan)</td>
        <td>Bilingual essential; Japanese press skills required</td></tr>
    <tr><td>Content / SEO</td>
        <td>SaaS, media, B2B</td>
        <td>Native-language production in target locale</td></tr>
    <tr><td>Product marketing (PMM)</td>
        <td>FAANG Tokyo, Stripe, Notion, Datadog</td>
        <td>Bilingual preferred, English OK at FAANG</td></tr>
    <tr><td>Growth / lifecycle</td>
        <td>Mercari, PayPay, Indeed, foreign-cap SaaS</td>
        <td>English-friendly at top tier</td></tr>
    <tr><td>Field / event marketing</td>
        <td>B2B SaaS, finance, consulting</td>
        <td>JP required for domestic events</td></tr>
    <tr><td>Inbound / cross-border</td>
        <td>Tourism boards, retail, hospitality</td>
        <td>JP helpful, English/CJK content prioritized</td></tr>
  </tbody>
</table>

<h2 id="companies">Companies actively hiring</h2>
<h3>Tier 1 — English-friendly, foreigner-receptive</h3>
<ul>
  <li><strong>Mercari</strong> — growth, product marketing, brand. English-OK on
      international team; Japanese for domestic.</li>
  <li><strong>PayPay</strong> — performance marketing, partnerships marketing.
      Bilingual preferred.</li>
  <li><strong>SmartNews</strong> — content, growth, brand. Strong international team.</li>
  <li><strong>Stripe Tokyo</strong> — PMM, content, partner marketing.</li>
  <li><strong>Notion Japan</strong> — content, community, partner marketing.</li>
  <li><strong>HubSpot Japan</strong> — growth, demand gen, content. Heavy bilingual hiring.</li>
  <li><strong>Datadog Japan</strong> — PMM, demand gen.</li>
  <li><strong>Snowflake Japan</strong> — field marketing, PMM, partner marketing.</li>
</ul>
<h3>Tier 2 — Japanese-first but foreigner-friendly</h3>
<ul>
  <li>Rakuten — large in-house marketing org spanning 70+ services.</li>
  <li>LINE Yahoo Japan — growth, partnerships.</li>
  <li>Cyberagent — performance and brand for AbemaTV, gaming, ads.</li>
  <li>Recruit (Indeed parent) — multi-brand portfolio.</li>
  <li>Sony Group — global brand, gaming, music marketing.</li>
</ul>
<h3>Luxury and FMCG</h3>
<ul>
  <li>LVMH Japan (LV, Dior, Tiffany, Bulgari), Richemont, Kering — bilingual brand managers.</li>
  <li>P&amp;G Japan (Kobe HQ historically) — global brand-management career track.</li>
  <li>Unilever Japan, Coca-Cola Japan, Nestlé Japan — bilingual brand and trade roles.</li>
</ul>

<h2 id="comp">Compensation by level</h2>
<table>
  <thead>
    <tr><th>Level</th><th>Years</th><th>Tech / SaaS (¥M)</th><th>Luxury / FMCG (¥M)</th></tr>
  </thead>
  <tbody>
    <tr><td>Coordinator / Specialist</td><td>0–3</td><td>4.5–7</td><td>4.5–6.5</td></tr>
    <tr><td>Manager</td><td>3–6</td><td>7–11</td><td>7–10</td></tr>
    <tr><td>Senior Manager</td><td>6–10</td><td>11–16</td><td>10–14</td></tr>
    <tr><td>Head of Marketing / Director</td><td>10+</td><td>16–25</td><td>14–22</td></tr>
    <tr><td>CMO / VP</td><td>15+</td><td>25–45</td><td>20–35</td></tr>
  </tbody>
</table>
<p>Performance marketing managers at FAANG Tokyo and PayPay can earn 25–30% premiums
over the tech median above. Brand managers at top-tier luxury (LVMH Maisons) earn
healthy bonuses (15–25% of base) and have generous expat-package elements if hired
from overseas.</p>

<h2 id="japanese">Japanese language and culture</h2>
<p>Marketing is more language-dependent than engineering. The split:</p>
<ul>
  <li><strong>If you market <em>to Japanese consumers</em></strong>, you need at least
      reading-level Japanese for competitive analysis, native copy review, and tone
      sensitivity. Practical floor: N2.</li>
  <li><strong>If you market <em>to overseas consumers from Japan</em></strong> (inbound
      tourism, B2B SaaS for APAC), English-native fluency is the asset and N3 is
      sufficient for stakeholder work.</li>
  <li><strong>Cultural fluency matters more than JLPT.</strong> Japanese consumer
      preferences (preference for understated tone, distrust of overt comparison
      claims, deep loyalty to local brands) shape every channel. Read a year of
      successful campaigns in your category before you propose your first one.</li>
</ul>

<h2 id="channels">Channel landscape — what's different in Japan</h2>
<ul>
  <li><strong>LINE — the dominant messaging and broadcast channel.</strong> 97M monthly
      active users in Japan. Brand accounts, LINE Ads Platform, LINE Official Accounts
      replace much of what Facebook/Instagram do elsewhere.</li>
  <li><strong>Yahoo! Japan — still 60M MAU.</strong> Yahoo Display Ads and Yahoo Search
      Ads remain meaningful spend channels alongside Google.</li>
  <li><strong>X (formerly Twitter)</strong> — disproportionately influential in Japan vs.
      most countries. Strong organic reach for B2C brands; campaigns often run on X
      first, Instagram second.</li>
  <li><strong>Instagram</strong> — dominant for lifestyle, food, fashion, beauty.</li>
  <li><strong>TikTok</strong> — growing fast for under-25 segments, particularly food,
      retail, and entertainment.</li>
  <li><strong>YouTube</strong> — strong for long-form content; Japanese YouTuber
      ecosystem is large.</li>
  <li><strong>Facebook</strong> — small reach in Japan, mostly older B2B segments.</li>
  <li><strong>Out-of-home</strong> — Tokyo Metro and JR train ads are still meaningful;
      Shibuya street and station ads are common for launches.</li>
  <li><strong>PR &amp; media relations</strong> — Japanese press has strong protocols
      (kisha club, embargo customs). Foreign PMMs typically partner with a local
      bilingual PR agency rather than going direct.</li>
</ul>

<h2 id="entry">How foreigners enter the field</h2>
<ol>
  <li><strong>Foreign-cap SaaS Japan launch teams</strong> — Stripe, Notion, Figma,
      Datadog, Snowflake, HubSpot, Asana, Miro all hire Japan PMMs. These are the
      easiest English-first entry points.</li>
  <li><strong>Bilingual brand management at FMCG / luxury</strong> — P&amp;G, Unilever,
      L'Oréal, LVMH all run global brand-manager grad programmes. Mostly recruit at
      MBA level.</li>
  <li><strong>Mercari / PayPay / SmartNews global team</strong> — apply directly through
      English careers pages; many roles open to overseas applicants.</li>
  <li><strong>Inbound tourism marketing</strong> — JNTO (Japan National Tourism
      Organisation), prefectural tourism boards, Hoshino Resorts, Tokyu — periodically
      hire English-native marketers for overseas-targeting roles.</li>
  <li><strong>Agency side first, in-house later</strong> — Dentsu D, Ogilvy, McCann
      Tokyo, R/GA hire foreign marketers and creatives; agency tenure builds bilingual
      capital before pivoting in-house.</li>
</ol>

<h2 id="pivots">Common pivots</h2>
<ul>
  <li><strong>Performance marketer → growth PM</strong> at Mercari, PayPay,
      Cyberagent.</li>
  <li><strong>Brand manager → general manager / country head</strong> at FMCG and
      luxury (P&amp;G grads in particular).</li>
  <li><strong>PMM → product manager</strong> at SaaS — common because PMM already owns
      a market segment and competitive narrative.</li>
  <li><strong>Content / SEO → in-house demand gen</strong> at B2B SaaS once the SEO
      muscle proves out.</li>
  <li><strong>In-house → founder</strong> — D2C founders in Japan often come from a
      brand-marketing or growth background.</li>
</ul>
<div class="callout">
  Build your career roadmap with the
  <a href="/roadmaps/marketing">Marketing roadmap</a> — five stages from coordinator
  to CMO, with salary bands and Japan-specific notes.
</div>
""",
    },

]
