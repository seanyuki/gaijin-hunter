"""
Static content registries for Phase 4, resource pages, city/role guides.

Each entry is a dict the templates render directly. The hub pages iterate
over the registry; the detail pages look up by slug and render a single entry.

Keeping these in Python (not templates) means we can: enumerate them for
the hub, link to them by slug, and ensure the slug → title mapping is
unambiguous. Content stays plain markdown-ish HTML.
"""

# ---------------------------------------------------------------------------
# Career-resource pages: split from the old monolithic /resources page.
# Each entry's `body` is raw HTML, the resources_detail template wraps it
# in a styled article container.
# ---------------------------------------------------------------------------

RESOURCES: list[dict] = [

    # ------------------------------------------------------------------ visa
    {
        "slug": "visa-types",
        "icon": "badge",
        "title": "Work visas in Japan, every category for foreign professionals",
        "summary": "Engineer/Specialist, HSP, J-Skip, J-Find, Business Manager, Instructor, Spouse, Working Holiday, what each is for, who qualifies, and what changed in 2024–25.",
        "updated": "May 2026",
        "read_time": "11 min",
        "toc": [
            ("overview", "Overview: 8 work visa categories"),
            ("engineer", "Engineer / Specialist in Humanities"),
            ("hsp", "Highly Skilled Professional (HSP)"),
            ("j-skip", "J-Skip, Special Highly Skilled (2023+)"),
            ("j-find", "J-Find, recent graduates (2023+)"),
            ("business-manager", "Business Manager (October 2025 reform)"),
            ("instructor", "Instructor"),
            ("ssw", "Specified Skilled Worker (SSW)"),
            ("spouse", "Spouse of Japanese / PR"),
            ("working-holiday", "Working Holiday"),
            ("pr", "Path to permanent residence"),
            ("pitfalls", "Common pitfalls"),
            ("apr-2026-update", 'April 2026, Engineer/Specialist language requirement'),
            ("oct-2025-bizmgr", 'October 2025, Business Manager visa reform'),
            ("jesta", "JESTA, Japan's new ESTA-style pre-screening"),
            ("changing-status", 'Changing status, practical timelines'),
            ("dependents", 'Dependent visas, spouse and child'),
        ],
        "body": """
<h2 id="overview">Overview: 8 work visa categories</h2>
<p>Japan has 27 statuses of residence, but the ones that matter for foreign professionals
break down into eight categories. Picking the right one upfront is the single biggest
decision in your move, it sets your minimum salary floor, dictates which jobs you can
take, and decides when you become eligible for permanent residence.</p>
<table>
  <thead>
    <tr><th>Visa</th><th>Salary floor</th><th>PR eligibility</th></tr>
  </thead>
  <tbody>
    <tr><td>Engineer / Specialist in Humanities</td>
        <td>≈ ¥250K/mo (¥3M/yr min, must match Japanese-national pay)</td>
        <td>10 yrs continuous residence</td></tr>
    <tr><td>Highly Skilled Professional (HSP), points-based</td>
        <td>¥3M/yr absolute minimum</td>
        <td>3 yrs (70+ pts) or 1 yr (80+ pts)</td></tr>
    <tr><td>J-Skip, Special HSP</td>
        <td>¥20M/yr (researchers / specialists) or ¥40M/yr (managers)</td>
        <td>1 yr</td></tr>
    <tr><td>J-Find, job-hunting status</td>
        <td>Personal savings of ¥200K to enter</td>
        <td>Convert to work visa first</td></tr>
    <tr><td>Business Manager (reformed Oct 2025)</td>
        <td>¥30M capital + 1 FT employee + JLPT N2</td>
        <td>10 yrs (or HSP path)</td></tr>
    <tr><td>Instructor (K-12 only)</td>
        <td>≈ ¥250K/mo</td>
        <td>10 yrs</td></tr>
    <tr><td>Specified Skilled Worker (SSW)</td>
        <td>Industry-specific, sets ~equivalent to Japanese workers</td>
        <td>SSW(ii): 10 yrs (PR eligible). SSW(i): not eligible.</td></tr>
    <tr><td>Spouse / dependant of Japanese / PR</td>
        <td>No floor, unrestricted work rights</td>
        <td>3 yrs (married 3+ yrs, resident 1+ yr) or 5 yrs</td></tr>
  </tbody>
</table>
<div class="callout">
  Not sure which you qualify for? Run the <a href="/tools/visa-eligibility">eligibility
  checker</a> in under two minutes. If HSP looks possible, score your points exactly with
  the <a href="/tools/hsp-points">HSP points calculator</a>.
</div>

<h2 id="engineer">Engineer / Specialist in Humanities / International Services</h2>
<p>The most common work visa for foreign professionals, covers software engineering,
finance, marketing, design, translation, and language teaching at eikaiwa or corporate
training providers. About 60% of new working-visa approvals fall here.</p>
<h3>Eligibility</h3>
<ul>
  <li><strong>Bachelor's degree</strong> (or higher) in a field relevant to the role, <em>or</em></li>
  <li><strong>10+ years of relevant practical experience</strong> (harder to prove; you need
      employment certificates and tax records).</li>
  <li>For language-teaching specifically: bachelor's in <em>any</em> subject + proven proficiency.</li>
  <li>A Japanese employer sponsors the application, you can't apply speculatively.</li>
</ul>
<h3>Salary floor</h3>
<p>No fixed monthly minimum in the immigration law itself, but Immigration uses the
"equivalent to Japanese national" rule: roughly ¥250,000/month base for entry-level, scaling
with role. <strong>Immigration began tightening salary checks in 2025</strong> to prevent
underpayment of foreign workers, offers under ¥3M/year for full-time professional roles are
now reliably rejected.</p>
<h3>Duration and renewal</h3>
<p>Granted in 1, 3, or 5-year increments. Renewable indefinitely as long as you remain
employed in a qualifying role. Your residence card carries the period of stay; renew at
your regional Immigration Services Agency office 3 months before expiry.</p>

<h2 id="hsp">Highly Skilled Professional (HSP), Type 1(b)</h2>
<p>Points-based "fast lane" visa for technical specialists, business managers, and
researchers. Score 70+ points and you get the 5-year visa plus accelerated PR; score 80+
and PR drops to a single year of residence.</p>
<h3>How the points work</h3>
<p>You collect points across education (10–30), experience (5–20), age (5–15),
salary (5–40), and bonus categories (JLPT, Japan-issued degree, top-uni grad, research
output, etc.). The breakeven for most foreign engineers in their late 20s and early 30s
is around ¥7–8M annual salary with a bachelor's degree.</p>
<h3>Benefits worth knowing</h3>
<ul>
  <li><strong>Spouse can work full-time</strong> without a separate work visa.</li>
  <li>You can <strong>employ a foreign domestic worker</strong> (a perk most foreign
      workers can't access).</li>
  <li>Your parents can join you in Japan if your annual income exceeds ¥8M.</li>
  <li>Preferential immigration processing, applications typically clear in 5–10 days
      rather than 4–10 weeks.</li>
</ul>
<div class="callout">
  Run the <a href="/tools/hsp-points">HSP points calculator</a> with your specific numbers.
  The page covers every bonus category, including the ones most online guides miss.
</div>

<h2 id="j-skip">J-Skip, Special Highly Skilled Professionals (introduced April 2023)</h2>
<p>The newest fast-track visa, aimed at very senior specialists and executives. Skips the
points system entirely if you meet either an education-plus-income threshold or an
experience-plus-income threshold.</p>
<h3>Type 1(a)/(b), Researchers and technical specialists</h3>
<ul>
  <li>Master's degree or higher <strong>AND</strong> annual income ≥ ¥20M, <em>or</em></li>
  <li>10+ years of relevant work experience <strong>AND</strong> annual income ≥ ¥20M.</li>
</ul>
<h3>Type 1(c), Business managers</h3>
<ul>
  <li>5+ years of business management experience <strong>AND</strong> annual income ≥ ¥40M.</li>
</ul>
<h3>What you get</h3>
<p>Five-year period of stay from the start, eligible to apply for permanent residence
after just <strong>one year</strong> of continuous residence. Same family-and-spouse perks
as standard HSP.</p>
<div class="warn">
  The ¥20M and ¥40M income thresholds are <em>contracted</em> annual income from your Japan
  job, not your global compensation. Immigration verifies via your employment contract and
  tax records.
</div>

<h2 id="j-find">J-Find, Future Creation Individual Visa (job-hunting status, 2023+)</h2>
<p>Lets recent graduates of designated top universities enter Japan without a job offer to
look for work. Designed to compete with Singapore and the EU for international graduate
talent.</p>
<h3>Eligibility</h3>
<ul>
  <li>Bachelor's, master's, or doctoral degree from one of the <strong>94 designated
      universities</strong> (as of January 2025), the list includes most QS Top 100 and
      THE Top 200 universities globally.</li>
  <li>Graduated within the last <strong>5 years</strong>.</li>
  <li>Personal savings of <strong>≥ ¥200,000</strong> at entry.</li>
  <li>An activity plan describing your job search.</li>
</ul>
<h3>What you get</h3>
<p>Six-month initial period, renewable up to a total of two years. You may take part-time
work to support yourself during the search and convert to a full work visa once you land
an offer.</p>

<h2 id="business-manager">Business Manager (significantly tightened October 2025)</h2>
<p>For founders and executives of a Japan-registered company. The October 2025 reform was
a major tightening, the old ¥5M capital threshold is now ¥30M, you must hire at least
one full-time non-foreign employee, and you must demonstrate JLPT N2-level Japanese
(roughly CEFR B2).</p>
<h3>Updated requirements (post-October 2025)</h3>
<ul>
  <li><strong>¥30M minimum capital</strong> deposited and verifiable.</li>
  <li>A <strong>real commercial office</strong>, virtual offices and home addresses are
      rejected. Immigration may physically visit.</li>
  <li><strong>≥ 1 full-time employee</strong> who is a Japanese citizen, PR holder, or
      long-term resident.</li>
  <li><strong>JLPT N2 or equivalent Japanese ability.</strong> This is the new bar.</li>
  <li>A credible 1–3 year business plan with financial projections.</li>
</ul>
<div class="danger">
  <strong>If you started planning under the old rules:</strong> applications submitted
  before the reform date were grandfathered. Anything filed after October 2025 falls under
  the tightened requirements. Talk to a registered immigration lawyer (<em>gyōseishoshi</em>)
  before committing capital.
</div>

<h2 id="instructor">Instructor</h2>
<p>Specifically for K–12 teaching at recognised Japanese schools, elementary, junior
high, high school, and certain vocational schools.</p>
<h3>What it does NOT cover</h3>
<ul>
  <li>Eikaiwa conversation schools (NOVA, ECC, AEON), those use Engineer/Specialist.</li>
  <li>ALT positions via private dispatch companies (Interac, Heart, Borderlink), also
      Engineer/Specialist.</li>
  <li>Corporate language training, Engineer/Specialist.</li>
  <li>Tutoring or freelance teaching without a sponsoring school.</li>
</ul>
<p>If you're confused about which visa your teaching offer falls under, ask the employer
directly which status of residence they'll sponsor.</p>

<h2 id="ssw">Specified Skilled Worker (SSW), sectoral visas</h2>
<p>Introduced in 2019 to address acute labour shortages in 14 specified sectors including
nursing care, construction, food service, hospitality, agriculture, and manufacturing.
Hiring under SSW has expanded rapidly post-2023 and the government is on track to admit
820,000 SSW workers between 2024 and 2029.</p>
<h3>Two tiers</h3>
<ul>
  <li><strong>SSW(i):</strong> Up to 5 years total. Cannot bring family members. Pass a
      sector-specific skills test plus the JFT-Basic or JLPT N4 Japanese test.</li>
  <li><strong>SSW(ii):</strong> Renewable indefinitely, family members may join, eligible
      for PR after 10 years. Available in a growing list of sectors (construction,
      shipbuilding, hospitality, others).</li>
</ul>
<p>SSW is rarely the right visa for white-collar foreign professionals, it's designed
for sectoral labour-shortage hiring. But if you're already in Japan on a Technical Intern
Trainee visa, transitioning to SSW is the standard upgrade path.</p>

<h2 id="spouse">Spouse / dependant of Japanese national or PR holder</h2>
<p>If you marry a Japanese citizen or someone with permanent residence, you can hold the
Spouse or Long-Term Resident status. <strong>Unrestricted work rights</strong>, you can
take any job, change employers without notifying Immigration, run a business, and so on.</p>
<h3>PR fast-track</h3>
<ul>
  <li>Married 3+ years <strong>and</strong> resident in Japan 1+ years → PR eligible.</li>
  <li>Married less than 3 years → PR eligible after 3 years of residence.</li>
</ul>

<h2 id="working-holiday">Working Holiday</h2>
<p>Bilateral agreement, age 18–30 (18–25 for a few countries), up to 6–12 months in Japan
with permission to work part-time across most industries. Best treated as a long
"try-Japan-out" trip rather than a career launch, but the standard conversion path is
Working Holiday → Engineer/Specialist once you've found a sponsor.</p>
<h3>Partner countries (as of 2026)</h3>
<p>Australia, Argentina, Austria, Canada, Chile, Czech Republic, Denmark, Estonia, France,
Germany, Hong Kong, Hungary, Iceland, Ireland, Italy, Korea, Lithuania, Netherlands,
New Zealand, Norway, Poland, Portugal, Slovakia, Spain, Sweden, Taiwan, UK, Uruguay, and
expanding. Check the embassy of your country for current details.</p>

<h2 id="pr">Path to permanent residence, what's actually required</h2>
<table>
  <thead>
    <tr><th>Your route</th><th>Continuous residence required</th></tr>
  </thead>
  <tbody>
    <tr><td>Standard work visa</td><td>10 years (5+ on a work visa)</td></tr>
    <tr><td>HSP 70+ points</td><td>3 years</td></tr>
    <tr><td>HSP 80+ points</td><td>1 year</td></tr>
    <tr><td>J-Skip (Special HSP)</td><td>1 year</td></tr>
    <tr><td>Spouse of Japanese / PR (married 3+ yrs)</td><td>1 year</td></tr>
    <tr><td>Spouse of Japanese / PR (married &lt; 3 yrs)</td><td>3 years</td></tr>
  </tbody>
</table>
<h3>The 2024–25 rule change you must know about</h3>
<p>From <strong>2024</strong> onwards, you must hold the maximum period of stay permitted
under your visa category at the time you file your PR application. For most professional
visas that means a <strong>5-year</strong> status of residence. A transitional grace
period applies until <strong>March 31, 2027</strong>, during which 3-year-visa holders are
still assessed under the old rules, but plan for the new standard once that window closes.</p>
<p>Other PR requirements you can't skip: clean tax and pension record (pay
<em>everything</em> on time for the last 24 months), no criminal record, demonstrated
ability to support yourself, and a Japanese national or PR-holder guarantor.</p>
<div class="callout">
  Build the full visa timeline for your category with the
  <a href="/tools/visa-timeline">visa timeline tool</a>, document checklists, realistic
  durations, and the order things actually happen in.
</div>

<h2 id="pitfalls">Common pitfalls, what gets foreign applicants refused</h2>
<ul>
  <li><strong>Degree-job mismatch.</strong> A computer-science grad applying for a
      marketing-only role gets refused under Engineer/Specialist. You'd need 10+ years of
      marketing experience to compensate.</li>
  <li><strong>Underpayment.</strong> Offers below the Japanese-national equivalent for the
      role are now actively rejected. Immigration cross-references your contract against
      ward-office wage data.</li>
  <li><strong>Working before the COE arrives.</strong> Illegal. Wait until you have the
      physical document.</li>
  <li><strong>Quitting your sponsoring employer.</strong> You have <strong>3 months</strong>
      to find a new sponsor before your visa is at risk. Apply for the
      "Designated Activities" job-search status if you need more time.</li>
  <li><strong>Status-of-residence mismatch.</strong> Doing a job your visa doesn't permit
      (e.g. tutoring English on an Engineer visa) can trigger refusal of future renewals.</li>
  <li><strong>Unpaid pension contributions.</strong> The single biggest reason PR
      applications get refused, Immigration pulls your 24-month pension payment record.</li>
</ul>
<!-- ENRICH_V2:visa-types -->
<h2 id="apr-2026-update">April 2026, Engineer/Specialist language requirement</h2>
<p>Effective April 15, 2026, Japan's most common foreign-worker visa, Engineer /
Specialist in Humanities / International Services, added a Japanese-language
requirement for applicants whose roles involve substantive Japanese-language
interaction. The Immigration Services Agency now categorises sponsoring employers
into four tiers based on size, tax history, and prior compliance. For Category 3 and
Category 4 employers (generally smaller or newer companies), applicants in roles
requiring Japanese interpersonal work must now submit proof of Japanese ability at
roughly CEFR B2 / JLPT N2 level.</p>
<p>Category 1 and 2 employers, most large Japanese corporations, established
foreign-cap firms, and listed companies, are largely exempt from the documentation
upgrade. The practical impact:</p>
<ul>
  <li><strong>Mercari, Indeed, PayPay, Rakuten, FAANG Tokyo:</strong> no change. Visa
      processing under prior norms.</li>
  <li><strong>Series-A/B Japanese startups, smaller foreign-cap entrants:</strong>
      expect to provide JLPT N2 certification or equivalent during application if the
      role description mentions client / stakeholder interaction in Japanese.</li>
  <li><strong>Pure-English roles</strong> at any size of employer remain unaffected, software engineering, research, and other roles that don't require Japanese
      interpersonal work are exempt.</li>
</ul>

<h2 id="oct-2025-bizmgr">October 2025, Business Manager visa reform</h2>
<p>The Business Manager (経営・管理) visa underwent its largest tightening in years
in October 2025:</p>
<ul>
  <li><strong>Minimum capital raised from ¥5M to ¥30M</strong>, a 6× increase. The
      new threshold aligns Japan with established global norms and was driven by
      concerns about shell-company visas.</li>
  <li><strong>One full-time Japanese-rooted employee required</strong>, either a
      Japanese national, permanent resident, spouse-of-Japanese, or long-term resident.
      The previous standard allowed any nationality.</li>
  <li><strong>JLPT N2 requirement</strong>, at least one person (the applicant or
      the required local employee) must hold JLPT N2 or higher.</li>
  <li><strong>Substantive office space</strong>, virtual offices no longer count;
      Immigration now expects a verifiable physical office with signage and
      operational hours.</li>
</ul>
<p>If you were considering Japan's Business Manager visa to set up a one-person
freelance company, that path is effectively closed unless you can raise ¥30M and
hire a qualifying local employee. Most foreigners who chose Business Manager
historically (consultants, e-commerce sellers, small shop owners) should now
investigate either the Highly Skilled Professional visa or a regular employed
Engineer/Specialist sponsorship instead.</p>

<h2 id="jesta">JESTA, Japan's new ESTA-style pre-screening</h2>
<p>Japan is rolling out a Japan Electronic System for Travel Authorization (JESTA)
in 2026–27 for short-term visa-waiver travellers (the 71 countries currently eligible
for visa-free entry). JESTA is not a work visa and won't affect job-hunters with
J-Find, HSP, or Engineer/Specialist visas, but it does mean:</p>
<ul>
  <li>Short-term business trips ("recruiting trip", "interview week") will require
      a JESTA application around 72 hours before flying. Fees are expected at
      roughly ¥1,000–¥3,000.</li>
  <li>Job seekers on visa-waiver entry should plan timelines around the JESTA
      window, especially for back-to-back trips.</li>
</ul>

<h2 id="changing-status">Changing status, practical timelines</h2>
<p>Most foreign professionals will change status of residence at least once in their
career in Japan (e.g., from Student to Engineer, from Engineer to HSP, from
Engineer to Spouse). Realistic 2025–26 timelines:</p>
<table>
  <thead><tr><th>Change</th><th>Realistic timeline</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>Student → Engineer/Specialist</td><td>4–8 weeks</td>
        <td>Apply during your final year; gap month between graduation and start is
        fine if Status of Residence remains valid.</td></tr>
    <tr><td>Engineer/Specialist → HSP</td><td>4–6 weeks</td>
        <td>Submit point-calculation sheet, certificates, and tax records.</td></tr>
    <tr><td>HSP → Permanent Resident (after 1 yr at 80+ pts)</td><td>3–6 months</td>
        <td>Background check is the slow step; gather residence-tax certificates for
        all years.</td></tr>
    <tr><td>HSP → Permanent Resident (after 3 yrs at 70+ pts)</td><td>4–7 months</td>
        <td>Same documents; slightly longer review.</td></tr>
    <tr><td>Engineer → Spouse/Family</td><td>2–4 weeks</td>
        <td>Marriage certificate translation must be apostilled if from non-Hague
        country.</td></tr>
  </tbody>
</table>

<h2 id="dependents">Dependent visas, spouse and child</h2>
<p>If you bring family on a Dependent visa, expect these realities:</p>
<ul>
  <li><strong>Spouse working rules.</strong> Dependents may work up to 28 hours/week
      with prior "permission for activities other than that permitted" (資格外活動許可)
      from Immigration. Full-time work requires the spouse to change to their own
      Status of Residence (Engineer, etc.), there's no automatic carry-over.</li>
  <li><strong>HSP family privileges.</strong> HSP holders' spouses can work full-time
      without restriction (special advantage). HSPs can also bring a parent if a child
      under 7 is in the household.</li>
  <li><strong>School enrolment.</strong> Most foreign children attend public elementary
      and junior-high schools by default. International schools (¥2.5–3M+/yr) like
      ASIJ, BST, Aoba-Japan, Yokohama International, are concentrated in Tokyo,
      Yokohama, Kobe, and Nagoya.</li>
  <li><strong>National Health Insurance.</strong> Dependents automatically join the
      employee's health-insurance plan; no additional premium per dependent.</li>
</ul>

""",
    },

    # ------------------------------------------------------------------ JLPT
    {
        "slug": "jlpt-levels",
        "icon": "translate",
        "title": "JLPT levels, what each really means for hiring",
        "summary": "What employers actually expect at N5 through N1, how to self-assess honestly, when to apply below your listed level, and the alternative tests (BJT, JFT-Basic) you may not know about.",
        "updated": "May 2026",
        "read_time": "8 min",
        "toc": [
            ("overview", "What JLPT is and isn't"),
            ("levels", "Levels and what employers expect"),
            ("by-role", "Japanese requirements by role family"),
            ("by-company", "What specific companies actually require"),
            ("alt-tests", "JFT-Basic, BJT, the other tests"),
            ("apply-below", "When to apply at a level above your JLPT"),
            ("study-pace", "Realistic study timelines"),
            ("salary-impact", 'Salary impact by JLPT level, real numbers'),
            ("jft-basic", 'JFT-Basic vs JLPT, what employers actually accept'),
            ("alternatives", 'BJT, J.TEST, and other employer-recognised tests'),
            ("study-timelines", 'Realistic study timelines from N5 to N1'),
            ("how-to-prep", 'How working professionals actually pass each level'),
        ],
        "body": """
<h2 id="overview">What JLPT is and isn't</h2>
<p>The Japanese-Language Proficiency Test (日本語能力試験) is the standard certification
for non-native Japanese speakers, read-and-listen, multiple choice, no speaking or writing
component. Five levels from N5 (most basic) to N1 (near-native reading). Held twice a year
in Japan and most major cities worldwide (early July and early December).</p>
<p>It's the certification that <em>employers</em> care about. Real workplace Japanese
involves a lot of speaking and writing, the test doesn't measure either directly, but
having an N-level on your CV is the single most common hiring proxy.</p>

<h2 id="levels">The five levels, what employers actually expect</h2>
<table>
  <thead>
    <tr><th>Level</th><th>What you can do</th><th>Hours of study (typical)</th></tr>
  </thead>
  <tbody>
    <tr><td><strong>N5</strong></td>
        <td>Recognise basic kanji (~100), read hiragana/katakana fluently, follow simple
            conversations about everyday topics.</td>
        <td>250–400</td></tr>
    <tr><td><strong>N4</strong></td>
        <td>Read short passages on familiar topics, handle basic daily interactions in
            Japanese.</td>
        <td>550–700</td></tr>
    <tr><td><strong>N3</strong></td>
        <td>Read newspapers with effort, follow workplace small-talk, write basic emails.
            The "minimum viable" level for most domestic Japanese employers.</td>
        <td>900–1,000</td></tr>
    <tr><td><strong>N2</strong></td>
        <td>Hold business meetings, read business documents, write formal emails. The
            de facto floor for most "bilingual" job postings.</td>
        <td>1,400–2,000</td></tr>
    <tr><td><strong>N1</strong></td>
        <td>Comfortable with formal documents, idioms, business keigo, complex written
            Japanese. Required for senior client-facing roles at Japanese corporations.</td>
        <td>2,500–4,500</td></tr>
  </tbody>
</table>
<p>Hour estimates assume zero prior Asian-language background. Native speakers of Chinese
typically reach N2 in roughly 60–70% of the time because they already read most kanji.</p>

<h2 id="by-role">Japanese requirements by role family</h2>
<ul>
  <li><strong>Software engineering, design, data science (at international companies):</strong>
      None required at most postings. Mercari, SmartNews, Indeed Tokyo, Stripe Tokyo,
      Sakura AI, Cybozu all hire engineers without Japanese. Conversational Japanese (N3)
      becomes valuable around year 2 as you start interacting with non-engineering teams.</li>
  <li><strong>Software engineering at domestic Japanese companies (Rakuten partial
      exception):</strong> N2 typical. Rakuten officially operates in English as a company
      language since 2010, but local-team workflows still skew Japanese.</li>
  <li><strong>Product management, business development, sales:</strong> N2 minimum,
      N1 preferred. The conversation matters more than the certificate.</li>
  <li><strong>Marketing, communications, PR:</strong> Native or N1, you're writing
      Japanese for Japanese consumers.</li>
  <li><strong>Finance and accounting:</strong> N2 minimum for non-bilingual roles; the
      Big Four accounting firms and major banks have English-speaking teams but expect
      N2 within 1–2 years.</li>
  <li><strong>Legal:</strong> N1 + bengoshi-qualified is the gold standard. Bilingual
      English-Japanese legal counsel with the bengoshi qualification routinely receives
      multiple competing offers.</li>
  <li><strong>Teaching English (eikaiwa, ALT):</strong> None required. Job descriptions
      sometimes prefer "basic Japanese for daily life" but it's almost never a hard filter.</li>
</ul>

<h2 id="by-company">What specific companies actually require</h2>
<table>
  <thead>
    <tr><th>Company</th><th>Engineering</th><th>Non-engineering</th></tr>
  </thead>
  <tbody>
    <tr><td>Mercari</td><td>None, actively bilingual workplace</td><td>N2+</td></tr>
    <tr><td>SmartNews</td><td>None</td><td>N2+</td></tr>
    <tr><td>Indeed Tokyo</td><td>None (~80% non-Japanese eng team)</td><td>N1 typical</td></tr>
    <tr><td>LINE Yahoo Japan</td><td>N3 preferred</td><td>N2+</td></tr>
    <tr><td>PayPay</td><td>None</td><td>N2+</td></tr>
    <tr><td>Rakuten</td><td>None (English-as-corporate-language)</td><td>None</td></tr>
    <tr><td>Cybozu</td><td>None for most teams</td><td>N3+</td></tr>
    <tr><td>Google / Amazon / Microsoft / Meta Tokyo</td><td>None</td><td>N2 preferred</td></tr>
    <tr><td>Goldman Sachs / Morgan Stanley Tokyo</td><td>–</td><td>N1 preferred for client-facing</td></tr>
    <tr><td>Toyota / Honda / Sony / Panasonic / Mitsubishi (traditional zaibatsu)</td>
        <td>N2 minimum, N1 strongly preferred</td>
        <td>N1 expected</td></tr>
  </tbody>
</table>

<h2 id="alt-tests">JFT-Basic and BJT, the other tests employers may accept</h2>
<h3>JFT-Basic (Japan Foundation Test for Basic Japanese)</h3>
<p>Computer-based, offered year-round, results in 3–5 weeks. Roughly equivalent to JLPT N4.
The mandatory language test for the Specified Skilled Worker (SSW) visa in most sectors, you'll only encounter it if you're applying via the SSW path.</p>
<h3>BJT (Business Japanese Proficiency Test)</h3>
<p>Scored 0–800. Used by larger Japanese corporations (banks, trading houses) as a hiring
proxy when JLPT N1 is "too general":</p>
<ul>
  <li>BJT 480+ counts as 15 HSP points (same as JLPT N1).</li>
  <li>BJT 400–479 counts as 10 HSP points (same as N2).</li>
</ul>
<p>If you're applying for HSP and have N2, sitting BJT can sometimes give you the same
10 points without retaking JLPT.</p>

<h2 id="apply-below">When to apply for jobs that list a level above yours</h2>
<p>Postings often over-state the Japanese level required, Japanese HR departments tend
to default to "業務レベル" (business level / N2) for any client-touching role even when the
actual day-to-day work needs less. Three situations where applying one level below is
worth the email:</p>
<ul>
  <li><strong>You're a meaningfully better fit on technical skills.</strong> The hiring
      manager will lobby HR if you're the right candidate.</li>
  <li><strong>You're at most one level below.</strong> N2 listed, you have N3 → reasonable.
      N1 listed, you have N4 → don't waste the recruiter's time.</li>
  <li><strong>You have an active study plan with a clear next-test target.</strong>
      "Currently N3; sitting N2 in December" is much stronger than "I'm studying".</li>
</ul>
<div class="warn">
  <strong>Don't inflate your level on the rirekisho.</strong> Japanese interviewers will
  switch to Japanese mid-conversation to test you. Getting caught means an immediate
  rejection, not a polite "let's try in English".
</div>

<h2 id="study-pace">Realistic study timelines</h2>
<p>For someone working full-time, expect these pacings to N2 (the most useful level for
employment in Japan):</p>
<table>
  <thead>
    <tr><th>Starting point</th><th>Hours/week</th><th>Time to N2</th></tr>
  </thead>
  <tbody>
    <tr><td>Zero background</td><td>10 hrs/week</td><td>3–4 years</td></tr>
    <tr><td>Zero background</td><td>20 hrs/week (intensive)</td><td>2 years</td></tr>
    <tr><td>Already N4</td><td>10 hrs/week</td><td>18–24 months</td></tr>
    <tr><td>Already N3</td><td>8 hrs/week</td><td>12–14 months</td></tr>
    <tr><td>Already N2, going to N1</td><td>10 hrs/week</td><td>12–18 months</td></tr>
  </tbody>
</table>
<p>Most foreigners working in Japan plateau between N3 and N2 unless they actively force
themselves into Japanese-only environments, paid tutoring 2x/week, work-language switching,
or a Japanese partner who insists on Japanese at home all dramatically accelerate.</p>
<!-- ENRICH_V2:jlpt-levels -->
<h2 id="salary-impact">Salary impact by JLPT level, real numbers</h2>
<p>The relationship between JLPT level and pay is consistent across multiple 2026
surveys (TokyoDev, Robert Walters, Japan-Dev). The pattern, controlling for role
and years of experience:</p>
<table>
  <thead><tr><th>JLPT level</th><th>Typical premium vs no-Japanese</th><th>Roles unlocked</th></tr></thead>
  <tbody>
    <tr><td>None / N5</td><td>Baseline (¥3.5–4.5M entry)</td>
        <td>English-only engineering at FAANG Tokyo, Mercari international, Indeed.</td></tr>
    <tr><td>N4</td><td>+5–10% (¥4–5M entry)</td>
        <td>SSW (Specified Skilled Worker) eligibility; minor convenience advantage at
        Japanese-headquartered firms but rarely a hiring differentiator.</td></tr>
    <tr><td>N3</td><td>+10–15% (¥4.5–5.5M entry)</td>
        <td>Day-to-day office life becomes possible; teams open up at Cyberagent,
        DeNA, GMO. Most foreigner-friendly Japanese tech firms ask for N3 by
        end-of-year-2.</td></tr>
    <tr><td>N2</td><td>+15–25%</td>
        <td>The practical floor for management track, B2B SaaS sales, customer-
        facing PM, finance, consulting. Daijob and Robert Walters flag N2 as the
        single biggest comp lever in the 2026 market.</td></tr>
    <tr><td>N1</td><td>+25–35% over no-Japanese baseline</td>
        <td>Executive-track roles, client-facing M&amp;A, private banking,
        government/policy work. Bilingual engineers with N1 see ¥6–8M base at junior
        levels and ¥18–25M at senior at Japanese employers.</td></tr>
  </tbody>
</table>
<p>The TokyoDev 2025 survey of 989 international engineers confirmed: engineers
who can bridge between technical architecture and Japanese stakeholders (N2/N1)
carry a roughly 20% premium over monolingual peers, and the gap widens with
seniority. The premium is smaller at pure-English shops (FAANG Tokyo, Indeed)
where Japanese isn't part of the job.</p>

<h2 id="jft-basic">JFT-Basic vs JLPT, what employers actually accept</h2>
<p>JFT-Basic (Japan Foundation Test for Basic Japanese) is the newer, faster
alternative to JLPT, but it's not a JLPT replacement at the levels relevant to
professional employment. The honest comparison:</p>
<table>
  <thead><tr><th></th><th>JLPT</th><th>JFT-Basic</th></tr></thead>
  <tbody>
    <tr><td>Levels</td><td>N5 → N1</td><td>One level only (A2-equivalent, ≈ N4)</td></tr>
    <tr><td>Frequency</td><td>2× / year</td><td>6× / year (Asia region)</td></tr>
    <tr><td>Format</td><td>Paper, in 80 countries</td><td>Computer-based test (CBT)</td></tr>
    <tr><td>Results</td><td>~2 months after test</td><td>Same day, certificate in 5 business days</td></tr>
    <tr><td>Cost</td><td>¥6,500 (Japan) / varies overseas</td><td>¥7,000 / overseas varies</td></tr>
    <tr><td>Visa recognition</td><td>SSW(i), HSP points, white-collar work visas</td>
        <td>SSW(i) only</td></tr>
    <tr><td>Employer recognition</td><td>Universal at every employer level</td>
        <td>Minimal outside SSW context</td></tr>
  </tbody>
</table>
<p>If you're aiming at professional / engineering / management roles, take the JLPT.
JFT-Basic is the right choice only if (a) you need a fast result for an SSW(i) visa
application, or (b) you're in a country where JLPT isn't easily accessible. For
HSP-track or white-collar roles, JLPT N2/N1 is the recognised currency.</p>

<h2 id="alternatives">BJT, J.TEST, and other employer-recognised tests</h2>
<ul>
  <li><strong>BJT (Business Japanese Proficiency Test)</strong>, 8 levels, focused on
      business situations. Companies like Tokio Marine, Tokyo Gas, and large
      sōgō shōsha specifically value BJT J2/J1. HSP points: BJT 480+ = 10 pts,
      BJT 400-479 = 15 pts.</li>
  <li><strong>J.TEST</strong>, practical 6-level test popular among SE Asian
      candidates. Widely accepted in Japan for SSW and Engineer/Specialist purposes.</li>
  <li><strong>NAT-TEST</strong>, administered monthly, parallels JLPT levels.
      Less prestigious than JLPT but useful for interim certification.</li>
  <li><strong>Kanji Kentei (漢検)</strong>, Japanese-language kanji test; only
      relevant for very advanced learners who want to demonstrate native-level reading
      depth. Not used in standard hiring criteria.</li>
</ul>

<h2 id="study-timelines">Realistic study timelines from N5 to N1</h2>
<p>Self-reported study hours from successful test-takers in 2024–25:</p>
<table>
  <thead><tr><th>Level</th><th>Total study hours</th><th>Calendar time @ 10 hrs/wk</th></tr></thead>
  <tbody>
    <tr><td>N5</td><td>250–400 hrs</td><td>6–9 months</td></tr>
    <tr><td>N4</td><td>500–700 hrs</td><td>12–15 months</td></tr>
    <tr><td>N3</td><td>900–1,300 hrs</td><td>2–2.5 years</td></tr>
    <tr><td>N2</td><td>1,500–2,200 hrs</td><td>3–4 years</td></tr>
    <tr><td>N1</td><td>2,700–4,000+ hrs</td><td>5–7 years</td></tr>
  </tbody>
</table>
<p>For working professionals already in Japan, immersion shortens N3 and N4
materially, speaking, listening, and contextual vocabulary build faster than book
study can simulate. Reading and grammar levels (where most JLPT points sit) still
require deliberate study.</p>

<h2 id="how-to-prep">How working professionals actually pass each level</h2>
<ul>
  <li><strong>Anki for vocab.</strong> Tango N5 / N4 / N3 / N2 / N1 decks (~10,000
      words total to N1) are the standard. 30 min/day for two years gets most
      professionals to N2 vocab.</li>
  <li><strong>Bunpro or Tofugu for grammar.</strong> Most working professionals can't
      sustain textbook grammar drilling; SRS-based grammar tools fit better.</li>
  <li><strong>NHK Easy News / Asahi Shōgakusei</strong> for reading practice at
      N3/N2 level.</li>
  <li><strong>Shadowing / iTalki tutors</strong> 1–2 hr/week for speaking. The JLPT
      doesn't test speaking, but speaking ability is what your employer actually
      values.</li>
  <li><strong>Mock tests in the final 2 months</strong>, Shin Kanzen Master and Sou
      Matome series are the gold-standard prep books for each level.</li>
  <li><strong>Take the test even if you fail.</strong> The fail-and-retake cycle
      gives you exam pacing, which is half the test.</li>
</ul>


<div class="callout">
  Looking for boards, recruiters, or language tools? See our
  <a href="/resources/external-resources">curated external-resources
  directory</a> for 60+ vetted sites with honest usage notes.
</div>
""",
    },

    # ------------------------------------------------------------------ resume
    {
        "slug": "japanese-resume-formats",
        "icon": "document",
        "title": "Japanese resume formats, rirekisho and shokumu keirekisho explained",
        "summary": "Japan uses two distinct resume documents. Get the format, date conventions, photo specs, and the specific mistakes that get foreign applicants screened out.",
        "updated": "May 2026",
        "read_time": "9 min",
        "toc": [
            ("two-doc-system", "Why Japan uses two documents"),
            ("rirekisho", "Rirekisho (履歴書), the standardised form"),
            ("shokumu", "Shokumu keirekisho (職務経歴書), the career CV"),
            ("photo", "The photo, spec, sourcing, common errors"),
            ("dates", "Dates and the Western / imperial calendar"),
            ("mistakes", "Specific mistakes that get applications screened"),
            ("submission", "Submission format and etiquette"),
            ("digital-submission", 'Digital submission, PDF, photo files, naming'),
            ("photo-rules", 'Photo rules, 2025 specifics'),
            ("photo-skip", 'When you can skip the photo'),
            ("english-vs-japanese", 'English CV vs. rirekisho, when to send which'),
            ("ats-considerations", 'ATS / applicant tracking systems in Japan'),
            ("common-mistakes", '10 common rirekisho mistakes foreigners make'),
        ],
        "body": """
<h2 id="two-doc-system">Why Japan uses two documents</h2>
<p>Japanese job applications routinely require two resumes, not one. The split is
deliberate: the <strong>rirekisho</strong> is a standardised personal-history form
modelled after government identity documents and gives HR a fast, structured view of
"who you are." The <strong>shokumu keirekisho</strong> is the flexible career-narrative
document where you actually pitch yourself.</p>
<p>Most Japanese employers expect both. Submitting only one signals you don't understand
the local hiring process, a meaningful demerit at traditional companies. International
companies and most startups will accept just a Western CV in English; check the listing
before assuming.</p>
<div class="callout">
  Build both from the same data using the <a href="/resume">free rirekisho builder</a> and
  <a href="/resume/shokumu">shokumu keirekisho builder</a>. Fill in English on the left,
  export Japanese A4 PDFs.
</div>

<h2 id="rirekisho">Rirekisho (履歴書), the standardised form</h2>
<p>The format is largely fixed and follows the template published by the
<strong>Ministry of Health, Labour and Welfare (MHLW)</strong>. The MHLW version became
the de facto national standard in 2021. Each section has its expected ordering:</p>
<ol>
  <li><strong>Header bar:</strong> the date you wrote the document (西暦 or 令和), name
      in kanji (or katakana for foreigners), furigana reading in hiragana, date of birth,
      age, gender (optional since 2021), photo.</li>
  <li><strong>Address block:</strong> current address with postal code (郵便番号), phone,
      email. Optionally a separate contact address if different.</li>
  <li><strong>Education and work history (学歴・職歴):</strong> chronological from oldest
      to newest. Education first (start with high school entry, yes really), then jobs.
      Each entry on its own row with year, month, and event.</li>
  <li><strong>Licenses and certifications (免許・資格):</strong> JLPT, driver's license,
      professional licenses. Chronological by date acquired.</li>
  <li><strong>Motivation, special skills, self-PR (志望の動機・特技・自己PR):</strong> a
      free-text block, this is where you actually pitch.</li>
  <li><strong>Personal wishes (本人希望記入欄):</strong> commute time tolerance, start
      date constraints, etc. For most professionals just write 貴社規定に従います ("I will
      follow your company's standards").</li>
</ol>
<h3>Length</h3>
<p>One A3 sheet folded in half, or two A4 sheets stapled together. Always fits on two
A4 pages.</p>

<h2 id="shokumu">Shokumu keirekisho (職務経歴書), the career CV</h2>
<p>The flexible document. No mandated template, but a strong convention exists, and
deviating from it (without obvious reason) signals you haven't done your homework.</p>
<h3>Standard structure</h3>
<ol>
  <li><strong>Title bar:</strong> document type, your name, date.</li>
  <li><strong>Career summary (職務要約):</strong> 3–5 lines summarising your trajectory.
      This is the only section a busy hiring manager will read in full.</li>
  <li><strong>Work history (職務経歴):</strong> reverse chronological, one section per
      employer. Each section: company name, dates, headcount and capital (yes, including
      capital, 資本金, Japanese employers want to know company size), your role,
      responsibilities, and concrete achievements with numbers.</li>
  <li><strong>Skills (活かせるスキル):</strong> bulleted list. Tech stacks for engineers,
      tools and methodologies for non-engineers.</li>
  <li><strong>Self-PR (自己PR):</strong> 2–4 short paragraphs. This is more substantive
      than the rirekisho self-PR, explain how your experience maps to the target role.</li>
</ol>
<h3>Length</h3>
<p>Two A4 pages is standard for 5–10 years of experience. Three for 10–20 years.
Four pages is the absolute ceiling and usually means too much detail.</p>

<h2 id="photo">The photo (証明写真), spec, sourcing, common errors</h2>
<table>
  <thead>
    <tr><th>Spec</th><th>Required value</th></tr>
  </thead>
  <tbody>
    <tr><td>Dimensions</td><td>3 cm × 4 cm (vertical)</td></tr>
    <tr><td>Background</td><td>Plain blue, light grey, or white</td></tr>
    <tr><td>Age</td><td>Taken within the last <strong>3 months</strong></td></tr>
    <tr><td>Attire</td><td>Business attire, suit jacket and white shirt for men,
                          conservative blouse or jacket for women</td></tr>
    <tr><td>Hair</td><td>Out of your face; visible ears and forehead recommended</td></tr>
    <tr><td>Expression</td><td>Neutral or very slight smile; no teeth showing</td></tr>
    <tr><td>Glasses</td><td>OK; remove reflections</td></tr>
  </tbody>
</table>
<h3>Where to get one in Japan</h3>
<ul>
  <li><strong>ID photo booths (証明写真機):</strong> ¥800–¥1,500. Available at most major
      JR stations, convenience stores, and shopping centres. The standard option.</li>
  <li><strong>Photo studios:</strong> ¥3,000–¥8,000 with retouching. Worth it for senior
      roles where presentation matters.</li>
  <li><strong>Apps:</strong> <em>shomeishashin app</em> on iOS/Android lets you self-shoot,
      then print at convenience-store kiosks. Acceptable but quality varies.</li>
</ul>

<h2 id="dates">Dates and the calendar, Western vs. imperial</h2>
<p>Japan uses two parallel calendars on official documents:</p>
<ul>
  <li><strong>Western (西暦):</strong> 2026.</li>
  <li><strong>Japanese imperial (和暦):</strong> Reiwa 8 (令和8年). The current era is
      Reiwa, which began on 1 May 2019 when Emperor Naruhito ascended.</li>
</ul>
<p>Either is acceptable on a rirekisho, but you <strong>must be consistent</strong>
throughout the entire document. Mixing Western years for some events and imperial years
for others is one of the most common mistakes and is read as careless. Pick one and use
it everywhere.</p>
<div class="callout">
  <strong>Recommendation for foreign applicants:</strong> use Western years (西暦)
  throughout. Imperial-era conversion is error-prone and Japanese HR staff are entirely
  fluent in Western dates.
</div>

<h2 id="mistakes">Specific mistakes that get applications screened</h2>
<ul>
  <li><strong>Inconsistent dates between rirekisho and shokumu keirekisho.</strong>
      The two documents must agree exactly on every employer, every role, every date.
      HR specifically cross-checks.</li>
  <li><strong>Generic self-PR.</strong> "I am hardworking and detail-oriented" is the
      strongest signal that you didn't research the company. Reference something specific, a product, a recent announcement, a value from their hiring page.</li>
  <li><strong>Tasks listed instead of results.</strong> Japanese hiring is less
      number-driven than US hiring, but specific outcomes (revenue, scale, percentages,
      team size, deadlines hit) move the needle hard.</li>
  <li><strong>Missing the company-size fields in shokumu keirekisho.</strong> Japanese
      hiring managers want to know whether you came from a 30-person startup or a
      3,000-person corporate. Always include 従業員数 (employee count) and 資本金 (capital)
      per employer.</li>
  <li><strong>Skipping high school in education history.</strong> The rirekisho convention
      is to start from junior high or high school entry (中学校卒業 / 高校入学). Starting
      from university looks like you're hiding something.</li>
  <li><strong>Wrong photo aspect ratio.</strong> A square LinkedIn-style headshot looks
      out of place, use the 3×4 cm vertical proportion or your application looks lazy.</li>
  <li><strong>English in the rirekisho.</strong> Unless the listing explicitly says
      English documents are acceptable, write in Japanese. The shokumu keirekisho can be
      bilingual for international companies.</li>
</ul>

<h2 id="submission">Submission format and etiquette</h2>
<ul>
  <li><strong>PDF</strong> unless the company specifies otherwise. Filename in romaji:
      <code>RIREKISHO_LastName_FirstName.pdf</code> and
      <code>SHOKUMU_LastName_FirstName.pdf</code>.</li>
  <li><strong>Email body</strong> in plain Japanese (or English if applying via an English
      pipeline). Keep it short, three or four sentences identifying yourself, naming the
      position, listing attached files, and signing off with name + contact.</li>
  <li><strong>Hardcopy submissions</strong> (rarer now, but still happens for senior roles)
      go in an unsealed A4 envelope, with 履歴書在中 written in red on the front.</li>
</ul>
<!-- ENRICH_V2:japanese-resume-formats -->
<h2 id="digital-submission">Digital submission, PDF, photo files, naming</h2>
<p>In 2025–26, the majority of Japanese employers, even traditional Japanese
corporates, accept rirekisho and shokumu keirekisho as PDF email attachments or
through application portals (Workday, Greenhouse, Lever, Yappli, HRMOS). The
conventions:</p>
<ul>
  <li><strong>File format:</strong> PDF is universal. Word (.docx) is acceptable but
      less common; older companies may also accept Excel templates downloaded from
      MHLW or Hello Work.</li>
  <li><strong>File naming:</strong> follow the format
      <code>履歴書_姓名_YYYYMMDD.pdf</code> (e.g., <code>履歴書_山田太郎_20260615.pdf</code>).
      For foreigners,
      <code>履歴書_FAMILYNAME_GIVENNAME_YYYYMMDD.pdf</code>
      or
      <code>Rirekisho_FAMILYNAME_GIVENNAME_YYYYMMDD.pdf</code>
      is widely accepted.</li>
  <li><strong>Two documents bundled:</strong> rirekisho + shokumu keirekisho should
      typically be submitted as two separate PDFs (not combined). Some companies
      explicitly state this; if unsure, follow this convention.</li>
  <li><strong>Photo embedded in PDF:</strong> the photo should be embedded in the
      rirekisho PDF itself, don't send it as a separate attachment unless the company
      explicitly requests it.</li>
</ul>

<h2 id="photo-rules">Photo rules, 2025 specifics</h2>
<p>Detailed photo conventions:</p>
<ul>
  <li><strong>Size:</strong> 30mm × 40mm (3 × 4 cm), portrait orientation. Digital
      files should be roughly 360 × 480 pixels at 300dpi, saved as JPG or PNG, file
      size under 2MB.</li>
  <li><strong>Background:</strong> plain white or light blue. Light grey is
      borderline-acceptable; busy backgrounds are a hard no.</li>
  <li><strong>Attire:</strong> business suit (recruit suit if entry-level), white
      shirt, conservative tie for men; women typically wear a dark jacket and
      light blouse.</li>
  <li><strong>Expression:</strong> closed-mouth, slight smile is acceptable; many
      candidates choose neutral. Wide grins are off-message.</li>
  <li><strong>Hair, accessories:</strong> hair off the face; no hats. Earrings should
      be small and conservative.</li>
  <li><strong>Where to take it:</strong> photo booths (証明写真機, ~¥800) are
      everywhere in train stations. Professional photo studios (¥3,000–¥6,000) take
      30 minutes and produce noticeably better results. Online services like
      xpassportphoto.com generate digital files from a phone selfie for ~¥500 if
      lighting allows, usable for digital submission but not for printed
      applications.</li>
  <li><strong>How recent:</strong> photo must be within the last 3 months.</li>
</ul>

<h2 id="photo-skip">When you can skip the photo</h2>
<p>Increasingly common, but not universal. Companies that explicitly state
"photograph not required" (写真不要) in 2025–26 include:</p>
<ul>
  <li>Mercari (most roles), SmartNews, Indeed Tokyo, most FAANG Tokyo offices,
      Stripe Tokyo, Notion Japan, Datadog Japan, Snowflake Japan, HubSpot Japan.</li>
  <li>Many international SaaS companies operating under their global ATS (Greenhouse,
      Lever) skip the photo entirely because the platform doesn't support it.</li>
</ul>
<p>For traditional Japanese employers (banks, sōgō shōsha, large manufacturers),
keep the photo unless instructed otherwise. Including it doesn't hurt; omitting it
can read as not understanding norms.</p>

<h2 id="english-vs-japanese">English CV vs. rirekisho, when to send which</h2>
<table>
  <thead><tr><th>Situation</th><th>What to send</th></tr></thead>
  <tbody>
    <tr><td>FAANG Tokyo, Stripe, Notion, foreign-cap SaaS</td>
        <td>English CV only</td></tr>
    <tr><td>Mercari, SmartNews, PayPay (English career page)</td>
        <td>English CV; shokumu keirekisho if requested in JP</td></tr>
    <tr><td>Rakuten, Cyberagent, LINE Yahoo</td>
        <td>Both, rirekisho + shokumu keirekisho + English CV</td></tr>
    <tr><td>Banks, sōgō shōsha, traditional manufacturers</td>
        <td>Rirekisho + shokumu keirekisho. Japanese only.</td></tr>
    <tr><td>Japanese SaaS scale-ups (Sansan, freee, Money Forward)</td>
        <td>Rirekisho + shokumu keirekisho preferred; English CV acceptable as supplement.</td></tr>
    <tr><td>Eikaiwa and ALT dispatch companies</td>
        <td>English CV; cover letter; rirekisho if Japanese is part of the role.</td></tr>
  </tbody>
</table>

<h2 id="ats-considerations">ATS / applicant tracking systems in Japan</h2>
<p>Common Japan-side ATS platforms and how they behave:</p>
<ul>
  <li><strong>Greenhouse / Lever / Workday</strong>, used by most foreign-cap firms.
      Standard CV upload; usually skip rirekisho.</li>
  <li><strong>HRMOS</strong> (BizReach), Japan's largest enterprise ATS.
      Custom-formatted application forms; sometimes accept PDF rirekisho upload.</li>
  <li><strong>SmartHR / SmartHR Recruiting</strong>, used by Series-A/B startups.
      Generally accepts PDF rirekisho.</li>
  <li><strong>Yappli HR / Talentio</strong>, Japan-specific. Sometimes asks for
      structured form-fill in addition to PDF upload.</li>
  <li><strong>Wantedly</strong>, feed-style profile; the platform substitutes for
      rirekisho if you fill out the profile completely. Used heavily by Tokyo
      startups.</li>
  <li><strong>LinkedIn Easy Apply</strong>, direct CV upload; commonly used by
      Indeed Tokyo, foreign-cap Tokyo offices, and a growing number of Japanese
      employers.</li>
</ul>

<h2 id="common-mistakes">10 common rirekisho mistakes foreigners make</h2>
<ol>
  <li>Writing the date as the application <em>submission</em> date instead of the day
      you'll mail/email it.</li>
  <li>Using the wrong era, recent rirekisho can use either Western (2026) or
      Reiwa era (令和8); pick one and use it consistently throughout.</li>
  <li>Leaving "Reasons for resignation" (退職理由) blank for past jobs, most
      companies want at least "自己都合により退職" (resigned for personal reasons) or
      "契約満了" (contract completion).</li>
  <li>Mixing fonts within the document. MS Mincho or Yu Mincho for body, MS Gothic
      for headings, applied consistently.</li>
  <li>Listing the wrong "Date of issue" (発行日) on certificates, should match
      what the issuing institution shows.</li>
  <li>Skipping the "Hobbies and special skills" (趣味・特技) section. Japanese
      hiring managers read this carefully as a personality signal.</li>
  <li>Adding negative justifications in self-PR ("I struggle with X but...").
      Self-PR in Japanese context should be uniformly positive.</li>
  <li>Misformatting phone numbers, should be 090-XXXX-XXXX, not international
      format.</li>
  <li>Writing the family name first AND in lowercase. Should be UPPERCASE family
      name first when written in romaji.</li>
  <li>Forgetting to handwrite (or carefully sign) the document if submitted on
      paper. Even with digital submission, signature-style fields are sometimes
      expected.</li>
</ol>

""",
    },

    # ------------------------------------------------------------------ interview etiquette
    {
        "slug": "interview-etiquette",
        "icon": "users",
        "title": "Japanese interview etiquette, the rules that aren't on the job listing",
        "summary": "Arrive 5–10 minutes early, knock three times, bow on entry, present meishi with both hands. What actually matters at gaishikei vs. traditional Japanese employers.",
        "updated": "May 2026",
        "read_time": "7 min",
        "toc": [
            ("before", "Before you arrive"),
            ("arrival", "Arrival and entering the room"),
            ("greetings", "Greetings, bowing, and meishi"),
            ("during", "During the interview, what to do and avoid"),
            ("questions", "Questions you must be ready to answer"),
            ("ask-back", "Questions you should ask"),
            ("gaishikei", "Gaishikei vs. domestic, what changes"),
            ("after", "After the interview, thank-you etiquette"),
            ("online-interview", 'Online and video interview etiquette'),
            ("reverse-interview", 'Reverse interview, questions you should ask'),
            ("body-language", 'Body language and pacing'),
            ("difficult-questions", 'Difficult questions and how to handle them'),
            ("post-interview", 'Post-interview, thank-you emails and follow-up'),
            ("multi-round", 'Multi-round interviews, what changes at each stage'),
        ],
        "body": """
<h2 id="before">Before you arrive</h2>
<ul>
  <li><strong>Confirm the format.</strong> Reply to the invitation email with your
      preferred slot. Address the recruiter as ご担当者様 or by surname + 様 ("Tanaka-sama").</li>
  <li><strong>Plan a 15-minute buffer.</strong> Arriving exactly on time is treated as
      "late" at Japanese companies, but arriving more than 10 minutes early forces the
      interviewer to receive you before they're ready.</li>
  <li><strong>Dress like you mean it.</strong> Dark suit (black, navy, or charcoal), white
      shirt, plain tie for men or a conservative neutral-colour blouse for women. Even at
      "casual" startups, first interviews skew formal. You can dress down at later rounds
      once you've confirmed the culture.</li>
  <li><strong>Bring multiple printed copies</strong> of your rirekisho and shokumu
      keirekisho in an A4 clear folder, typically 3 copies (some interviewers won't have
      had a chance to print). Plus a notebook and pen.</li>
  <li><strong>Re-read the company's careers page</strong> and at least one recent press
      release. Japanese interviewers <em>always</em> ask "why our company specifically?"
      and reject vague answers.</li>
</ul>

<h2 id="arrival">Arrival and entering the room</h2>
<ol>
  <li>Arrive at reception 5–10 minutes early. Give your name, the time of your interview,
      and the name of the person meeting you.</li>
  <li>Wait standing or seated where directed. <strong>Don't pull out your phone</strong>, reception staff routinely report behaviour to the hiring team.</li>
  <li>When you reach the interview room: <strong>knock exactly three times.</strong>
      Two knocks is the toilet-check signal in Japan and will land badly. Wait for a
      "どうぞ" or "Please come in" before opening.</li>
  <li>Open the door, step in, close it gently while facing it, then turn to face the
      interviewers and bow at roughly 30°.</li>
  <li>Don't sit until the interviewer says どうぞお掛けください or similar. When seated,
      your bag goes on the floor beside the chair, not on the table.</li>
</ol>

<h2 id="greetings">Greetings, bowing, and meishi (business cards)</h2>
<h3>The opening greeting</h3>
<p>Standard opener: <strong>本日はよろしくお願いいたします</strong>
(<em>honjitsu wa yoroshiku onegai itashimasu</em>), "thank you for having me today."
Bow at ~30° on the お願い part.</p>
<h3>Meishi (business cards)</h3>
<p>If you have business cards, present them at the start. Hold the card with both hands,
your name facing the recipient. Bow slightly as you offer it. Receive their card the same
way, with both hands, and study it briefly before placing it on the table in front of
you (never directly into a pocket).</p>
<p>Most foreign applicants don't have business cards before their first interview, which
is completely fine. The Japanese person typically presents theirs first; receive politely.</p>
<h3>Bow angles in practice</h3>
<ul>
  <li><strong>15°</strong> casual greeting / passing a colleague</li>
  <li><strong>30°</strong> standard for entering an interview, greetings to hiring managers</li>
  <li><strong>45°</strong> formal apology or addressing executives</li>
</ul>

<h2 id="during">During the interview, what to do and what to avoid</h2>
<ul>
  <li><strong>Frame achievements as team efforts.</strong> Japanese interviewers find pure
      "I, I, I" framing off-putting. "Our team shipped X, my contribution was Y" lands
      stronger than "I built X."</li>
  <li><strong>Don't interrupt.</strong> Wait until the interviewer finishes their question
      before responding. Even pauses are part of the conversation.</li>
  <li><strong>Keep answers concise.</strong> 30–60 seconds is the target for most
      questions. Going long signals poor judgment.</li>
  <li><strong>Use respectful Japanese where you can.</strong> Even minimal keigo, ございます endings, 御社 (onsha) for "your company", signals cultural awareness.</li>
  <li><strong>Acknowledge weaknesses honestly.</strong> "My Japanese isn't yet at business
      level, but I'm studying X hours per week and targeting JLPT N2 in December" lands
      far better than minimising or deflecting.</li>
</ul>

<h2 id="questions">Questions you must be ready to answer</h2>
<ol>
  <li><strong>Why our company specifically?</strong> Name a product, a value, a recent
      news event, or a person whose work you've read. Generic "I admire your culture"
      lands as research-failure.</li>
  <li><strong>Why Japan?</strong> Genuine, specific reasons. "I want to live in a country
      with X cultural feature, and your industry has Y opportunities I can't access where I
      am" works. "I love anime and want to try Japan" doesn't.</li>
  <li><strong>Why are you leaving your current role?</strong> Forward-looking framing.
      Never bash your current employer.</li>
  <li><strong>Walk me through your career so far.</strong> 3–5 minutes max. Prepare a
      narrative that lands the "why this role" pitch at the end.</li>
  <li><strong>Tell me about a failure.</strong> Real, recent, with a concrete lesson.
      Avoid "I work too hard" framing.</li>
  <li><strong>Where do you see yourself in five years?</strong> Japanese companies value
      long tenures. "Still growing in this kind of role" works; "I'll have started my own
      company by then" usually doesn't.</li>
  <li><strong>What's your current and expected compensation?</strong> Give a range, not
      a single number. The recruiter will negotiate down regardless.</li>
</ol>
<div class="callout">
  See <a href="/interview-prep">interview prep</a> for role-specific question banks with
  what interviewers are actually looking for in each answer.
</div>

<h2 id="ask-back">Questions you should ask</h2>
<p>Always prepare 3–5 questions. The depth of your questions signals seriousness more than
the cleverness of your answers does.</p>
<ul>
  <li>What does success in this role look like at 3, 6, 12 months?</li>
  <li>What's the team structure and who would I report to?</li>
  <li>How does the team handle [specific challenge from the JD or recent news]?</li>
  <li>What's the typical career path from this position over 3–5 years?</li>
  <li>How does feedback work day-to-day? How do you handle mistakes?</li>
  <li>(For senior roles) What does the next planning cycle look like for this team?</li>
</ul>
<p>Skip the salary, vacation, and overtime questions in the first round. Those come up
after the offer, not before. Asking too early flags you as fixated on benefits over fit.</p>

<h2 id="gaishikei">Gaishikei (foreign-affiliated) vs. domestic Japanese, what changes</h2>
<table>
  <thead>
    <tr><th>Aspect</th><th>Gaishikei</th><th>Domestic Japanese</th></tr>
  </thead>
  <tbody>
    <tr><td>Self-promotion</td>
        <td>Direct, individual achievements OK</td>
        <td>Team-framed; modesty valued</td></tr>
    <tr><td>Salary discussion</td>
        <td>Often raised by recruiter early</td>
        <td>Avoided until offer stage</td></tr>
    <tr><td>Language</td>
        <td>English-first usually; Japanese optional</td>
        <td>Japanese-default; English at higher-level roles</td></tr>
    <tr><td>Process speed</td>
        <td>2–4 weeks, 3–4 rounds</td>
        <td>4–8 weeks, 4–6 rounds</td></tr>
    <tr><td>Dress code (first round)</td>
        <td>Business or business-casual</td>
        <td>Suit and tie still standard</td></tr>
    <tr><td>Decision driver</td>
        <td>Individual capability, output</td>
        <td>Team fit, long-term commitment</td></tr>
  </tbody>
</table>
<p>Most foreign hires at Mercari, SmartNews, PayPay, and similar fall into a hybrid: more
direct than legacy zaibatsu but more team-framed than US tech companies.</p>

<h2 id="after">After the interview, thank-you etiquette</h2>
<ul>
  <li><strong>Send a thank-you email within 24 hours.</strong> Address it to your
      interviewer(s) by name with surname + 様. Reference one specific topic discussed, this signals you were actually listening.</li>
  <li>One email per interviewer for multi-round panels. Personalised, not copy-pasted.</li>
  <li>Keep it short, 4–6 sentences in Japanese (or English if your interview was in
      English). The <a href="/templates">bilingual email templates</a> include
      ready-made versions.</li>
  <li>If you decide to withdraw, do it promptly and politely. Use the
      <a href="/templates#decline">decline / withdraw template</a>. Don't ghost, Japan's
      hiring community is small and recruiters talk.</li>
</ul>
<!-- ENRICH_V2:interview-etiquette -->
<h2 id="online-interview">Online and video interview etiquette</h2>
<p>By 2025, more than 70% of Japanese companies use at least one online round, most
commonly via Zoom, Google Meet, Teams, or LINE. The conventions:</p>
<ul>
  <li><strong>Log in 5 minutes early.</strong> Earlier is rude (forces interviewer to
      wait in the meeting room with you); later is unprofessional.</li>
  <li><strong>Display-name format:</strong> "山田 太郎 / Taro Yamada" or
      "Taro YAMADA (last name capitalised)". Avoid handles or nicknames.</li>
  <li><strong>Camera at eye level.</strong> A stack of books under a laptop is the
      simplest fix. Looking down at the camera reads as inattentive.</li>
  <li><strong>Background:</strong> plain wall preferred. Virtual backgrounds are
      acceptable if blurring artefacts are minimal. A messy room visible behind you
      is a strong negative signal.</li>
  <li><strong>Attire:</strong> full suit even though only the top half is visible.
      Same dress code as in-person.</li>
  <li><strong>Bow to the camera</strong> when greeting and ending. This isn't
      affected, onscreen presence still expects the cultural gesture.</li>
  <li><strong>Use proper closing:</strong> <em>"本日はお時間をいただきありがとうございました.
      引き続きどうぞよろしくお願いいたします."</em></li>
  <li><strong>Don't disconnect first.</strong> Wait for the interviewer to end the
      call. If you must leave first, ask politely.</li>
  <li><strong>Connection backup plan.</strong> Have a phone number ready in case
      video fails. Mention it in your reply when scheduling.</li>
</ul>

<h2 id="reverse-interview">Reverse interview, questions you should ask</h2>
<p>Japanese interviews almost always end with "最後に、何かご質問はありますか?" (Any
final questions?). Skipping this question or saying "No, I think I have all the
information" is a notable negative signal, it reads as lack of preparation or
interest. Good questions ladder up to seniority:</p>
<h3>For team-level interviewers (engineer / manager)</h3>
<ul>
  <li>"このポジションで成功するために、3ヶ月後にどんな成果を出していれば良いと思われますか?"
      (What does success at 3 months look like in this position?)</li>
  <li>"チームが現在直面している最大の課題は何ですか?"
      (What's the team's biggest current challenge?)</li>
  <li>"〇〇さんがこの会社で一番気に入っている点は何ですか?"
      (What do <em>you</em> personally like most about this company?)</li>
</ul>
<h3>For hiring manager / director-level</h3>
<ul>
  <li>"このチームの今後1–2年のロードマップを教えていただけますか?"
      (Could you share the team's 1–2 year roadmap?)</li>
  <li>"このポジションの優先順位の1番は何になるでしょうか?"
      (What's priority #1 for this role?)</li>
  <li>"経営層は、このチームに今後どのような期待をされていますか?"
      (What are executive expectations for this team going forward?)</li>
</ul>
<h3>For HR / culture-fit final rounds</h3>
<ul>
  <li>"昇給や昇進の評価サイクルはどのようになっていますか?"
      (How does the evaluation cycle for raises / promotions work?)</li>
  <li>"中途入社の方は、入社後どのようにオンボーディングされるのでしょうか?"
      (How are mid-career hires onboarded?)</li>
  <li>"外国人エンジニアの方は、これまでどの程度ご活躍されていますか?"
      (How have other foreign engineers fared at the company?)</li>
</ul>

<h2 id="body-language">Body language and pacing</h2>
<ul>
  <li><strong>Sit up straight; hands resting on lap or table.</strong> Avoid leaning
      back, crossing arms, or excessive gesturing.</li>
  <li><strong>Eye contact</strong> should be regular but not constant. Looking down
      occasionally to consult notes is acceptable. Constant unwavering eye contact
      reads as confrontational.</li>
  <li><strong>Pacing.</strong> Japanese interviewers often pause longer than Western
      interviewers between question and answer. Don't rush to fill silences. Take a
      breath, structure your answer, then speak.</li>
  <li><strong>Volume and clarity.</strong> Speak slightly more slowly than your
      natural pace if working in Japanese. Native speakers will appreciate clarity
      over speed.</li>
  <li><strong>Aizuchi (相槌).</strong> Quiet acknowledgements, "はい",
      "そうですね", "なるほど", while listening are expected. Silence while the
      interviewer is speaking reads as inattentive.</li>
</ul>

<h2 id="difficult-questions">Difficult questions and how to handle them</h2>
<table>
  <thead><tr><th>Question</th><th>What it's really testing</th><th>How to handle it</th></tr></thead>
  <tbody>
    <tr><td>"前職を辞めた理由は?" (Why did you leave your last job?)</td>
        <td>Stability, attitude toward conflict</td>
        <td>Positive framing only, never blame employer or peers. Focus on
        what you want to learn next.</td></tr>
    <tr><td>"5年後どうなりたいですか?" (Where do you want to be in 5 years?)</td>
        <td>Commitment, planning ability</td>
        <td>Show ambition tied to growth at this employer, not "I'll have my own
        company in 5 years".</td></tr>
    <tr><td>"なぜ日本で働きたいのですか?" (Why work in Japan?)</td>
        <td>Genuine interest, longevity</td>
        <td>Concrete reasons, language study, career fit, family, culture
        specifically. Avoid generic "I love anime".</td></tr>
    <tr><td>"あなたの弱みは?" (Your weakness?)</td>
        <td>Self-awareness</td>
        <td>Acknowledge a real weakness; pair it with the specific action you take
        to mitigate it.</td></tr>
    <tr><td>"日本語はどのくらい話せますか?" (How well do you speak Japanese?)</td>
        <td>Honesty, self-assessment</td>
        <td>Specific JLPT level + honest functional description ("daily life N3,
        technical N2"). Never oversell.</td></tr>
    <tr><td>"残業は大丈夫ですか?" (Are you OK with overtime?)</td>
        <td>Compliance, work attitude</td>
        <td>Affirm flexibility; if you have hard constraints (childcare, etc.) say
        them clearly. Don't pretend to be infinitely available.</td></tr>
    <tr><td>"いつまで日本に住む予定ですか?" (How long do you plan to live in Japan?)</td>
        <td>Long-term intention</td>
        <td>"長期的に" (long-term) or specific multi-year plan. Don't say "1–2 years
        and back home" unless that's truly your plan.</td></tr>
  </tbody>
</table>

<h2 id="post-interview">Post-interview, thank-you emails and follow-up</h2>
<p>Thank-you emails after interviews are increasingly common in Japan (especially at
foreigner-friendly tech firms), but not universal. The convention:</p>
<ul>
  <li><strong>Send within 24 hours.</strong> Same day if possible.</li>
  <li><strong>Address to the most senior interviewer.</strong> Or to HR/recruiter
      with cc to the interviewer.</li>
  <li><strong>Keep brief.</strong> 100–200 Japanese characters / 50–100 English
      words. Three parts: thank-you, one specific takeaway from the conversation,
      next-step acknowledgement.</li>
  <li><strong>Don't use templates.</strong> Reference one specific thing the
      interviewer said.</li>
  <li><strong>Subject line</strong> in Japanese:
      <em>"本日の面接のお礼 / [Your Name]"</em>.</li>
</ul>
<p>For follow-up after no response: wait 7 business days, then send a polite
inquiry to your recruiter or HR contact. Don't escalate further; multiple follow-ups
read negatively.</p>

<h2 id="multi-round">Multi-round interviews, what changes at each stage</h2>
<table>
  <thead><tr><th>Round</th><th>Length</th><th>Goal</th><th>Tone</th></tr></thead>
  <tbody>
    <tr><td>1: HR / recruiter screen</td><td>30 min</td>
        <td>Logistics, salary expectations, visa</td>
        <td>Friendly, conversational</td></tr>
    <tr><td>2: Hiring manager</td><td>45–60 min</td>
        <td>Role fit, motivation, technical depth</td>
        <td>Probing, focused</td></tr>
    <tr><td>3: Technical / case</td><td>60–90 min</td>
        <td>Skills validation</td>
        <td>Working session, problem-solving</td></tr>
    <tr><td>4: Cross-functional panel</td><td>45–60 min × 2–3</td>
        <td>Peer fit, collaboration</td>
        <td>Two-way; ask questions of each</td></tr>
    <tr><td>5: Executive / bar-raiser</td><td>30–45 min</td>
        <td>Final endorsement, alignment</td>
        <td>Strategic, big-picture</td></tr>
    <tr><td>6: Offer call (sometimes a meeting)</td><td>30 min</td>
        <td>Sell the offer</td>
        <td>Warm, negotiation-aware</td></tr>
  </tbody>
</table>
<p>Foreign-cap Tokyo employers typically compress to 4 rounds; Japanese banks
and sōgō shōsha can stretch to 6–7 rounds plus a written test. Mercari publishes
a median 4-week elapsed time; Goldman Sachs Japan IB averages 8 weeks for
analyst-class.</p>

""",
    },

    # ------------------------------------------------------------------ salary
    {
        "slug": "salary",
        "icon": "currency-yen",
        "title": "Salary expectations in Japan, real 2026 numbers by role",
        "summary": "Real salary bands by role family for foreign hires in 2026, junior to executive, plus how Japanese comp structures (base + 2× bonus + RSU) actually work.",
        "updated": "May 2026",
        "read_time": "9 min",
        "toc": [
            ("comp-structure", "How Japanese comp packages work"),
            ("bands", "Salary bands by role (2026, Tokyo)"),
            ("by-employer", "By employer type, gaishikei vs. domestic"),
            ("inflation", "Real wage growth in 2024–26"),
            ("take-home", "What ¥X actually pays you after tax"),
            ("negotiation", "Negotiation, what works in Japan"),
            ("shunto-2026", '2026 Shunto wage growth in context'),
            ("bilingual-premium", 'Bilingual premium, real numbers'),
            ("asking-for-raise", 'How to ask for a raise in Japan'),
            ("benefits-translate", 'How to compare benefits, Japan vs overseas offers'),
            ("offer-negotiation", 'Offer negotiation tactics'),
            ("equity-stock", 'Equity, RSUs, and stock options in Japan'),
        ],
        "body": """
<h2 id="comp-structure">How Japanese comp packages actually work</h2>
<p>Most Japan job listings show 年収 (<em>nenshu</em>), annual income, but the
underlying structure differs from the typical US package:</p>
<ul>
  <li><strong>Base salary (基本給):</strong> the monthly fixed pay, ×12.</li>
  <li><strong>Bonus (賞与):</strong> paid twice a year in summer (July) and winter
      (December). Total bonus typically ranges from <strong>2–6 months of base</strong>
      at established companies. Some startups pay annual or no bonus.</li>
  <li><strong>Allowances (手当):</strong> commuting reimbursement (almost universal,
      typically ¥10–20K/mo), family allowance for dependants (at older Japanese firms),
      housing allowance (mostly at gaishikei and senior roles).</li>
  <li><strong>RSUs / equity:</strong> common at FAANG Tokyo, pre-IPO startups, and major
      gaishikei. Almost never at traditional Japanese companies. Vest schedules vary, Google Japan uses standard 4-year with 1-year cliff; Mercari has its own scheme.</li>
</ul>
<div class="warn">
  <strong>The "annual income" number can include or exclude bonus depending on context.</strong>
  Always ask: "Is the figure base × 12 only, or does it include expected bonus at target
  performance?" Job listings most commonly state base × 12 + target bonus.
</div>

<h2 id="bands">Salary bands by role (2026, Tokyo, foreigner-friendly employers)</h2>
<p>Based on 2025 placement data and the TokyoDev 2025 developer survey (median
software engineer compensation was ¥9.5M, up ¥1M from 2024).</p>
<h3>Software engineering</h3>
<table>
  <thead><tr><th>Level</th><th>Years</th><th>Total comp (¥M/yr)</th></tr></thead>
  <tbody>
    <tr><td>Junior</td><td>0–2</td><td>4–7</td></tr>
    <tr><td>Mid</td><td>2–5</td><td>7–11</td></tr>
    <tr><td>Senior</td><td>5–9</td><td>10–16</td></tr>
    <tr><td>Staff / Tech Lead</td><td>9+</td><td>14–22</td></tr>
    <tr><td>Principal / Distinguished</td><td>12+</td><td>18–35+ (FAANG: ¥35M+ with RSUs)</td></tr>
  </tbody>
</table>
<h3>Data / AI / ML</h3>
<table>
  <thead><tr><th>Level</th><th>Total comp (¥M/yr)</th></tr></thead>
  <tbody>
    <tr><td>Junior analyst / engineer</td><td>4.5–7</td></tr>
    <tr><td>Mid scientist / engineer</td><td>7–12</td></tr>
    <tr><td>Senior / staff ML</td><td>12–20</td></tr>
    <tr><td>Research scientist (PhD)</td><td>15–30+ at PFN, Sakana AI, FAANG</td></tr>
  </tbody>
</table>
<h3>Product / business / marketing</h3>
<table>
  <thead><tr><th>Level</th><th>Total comp (¥M/yr)</th></tr></thead>
  <tbody>
    <tr><td>Associate PM</td><td>5–8</td></tr>
    <tr><td>Mid PM</td><td>8–13</td></tr>
    <tr><td>Senior / Group PM</td><td>13–20</td></tr>
    <tr><td>Director of Product</td><td>18–30</td></tr>
    <tr><td>Bilingual marketing manager</td><td>8–14</td></tr>
    <tr><td>Marketing director</td><td>15–25</td></tr>
  </tbody>
</table>
<h3>Teaching</h3>
<table>
  <thead><tr><th>Role</th><th>Total comp (¥M/yr)</th></tr></thead>
  <tbody>
    <tr><td>JET Programme ALT (year 1)</td><td>3.36 (~3.96 by year 4)</td></tr>
    <tr><td>JET Programme ALT (from April 2025 in higher-cost areas)</td><td>4.02–4.32</td></tr>
    <tr><td>Eikaiwa instructor (NOVA, AEON, ECC)</td><td>2.8–3.84</td></tr>
    <tr><td>Dispatch ALT (Interac, Heart)</td><td>2.3–3.5</td></tr>
    <tr><td>International-school teacher (with credential)</td><td>5–9</td></tr>
  </tbody>
</table>

<h2 id="by-employer">By employer type, what gaishikei pays vs. domestic</h2>
<p>The same role pays very differently depending on who you work for. The TokyoDev 2025
survey makes this stark for engineers:</p>
<table>
  <thead><tr><th>Employer type</th><th>Median engineer comp</th></tr></thead>
  <tbody>
    <tr><td>Foreign company without a Japan entity (remote)</td><td>¥13.5M</td></tr>
    <tr><td>Foreign company with a Japan entity (FAANG Tokyo, etc.)</td><td>¥13.5M</td></tr>
    <tr><td>Japanese-headquartered company</td><td>¥8.5M</td></tr>
  </tbody>
</table>
<p>The roughly ¥5M premium for gaishikei reflects three things: RSU/equity, more
aggressive market benchmarking, and faster promotion velocity. The premium is largest at
junior and mid levels; at senior and staff levels the bands converge.</p>

<h2 id="inflation">Real wage growth in 2024–26</h2>
<ul>
  <li>The 2025 spring wage negotiations (春闘 / <em>shunto</em>) settled at an average
      <strong>5.4% headline raise</strong>, the third consecutive year of 5%+ headline
      growth and the strongest sustained nominal wage rises in over 30 years.</li>
  <li>However, headline CPI has run at 2–3% over the same period, so real wage growth
      has been modest. 55% of companies plan further raises in 2026.</li>
  <li>Job-changer raises are running 7–15% on average, up to 20–30% for in-demand
      bilinguals in fintech, cloud security, AI, and senior PM roles.</li>
</ul>

<h2 id="take-home">What ¥X actually pays you after tax</h2>
<p>Japan's effective tax + social-insurance burden is roughly 25–30% for typical earners.
Quick reference (single, no dependants, year 2 in Japan):</p>
<table>
  <thead><tr><th>Gross annual</th><th>Net annual</th><th>Effective rate</th></tr></thead>
  <tbody>
    <tr><td>¥6M</td><td>¥4.6M</td><td>23% deducted</td></tr>
    <tr><td>¥8M</td><td>¥6.1M</td><td>24%</td></tr>
    <tr><td>¥10M</td><td>¥7.3M</td><td>27%</td></tr>
    <tr><td>¥15M</td><td>¥10.2M</td><td>32%</td></tr>
    <tr><td>¥20M</td><td>¥13.0M</td><td>35%</td></tr>
  </tbody>
</table>
<div class="callout">
  Run your specific offer through the <a href="/tools/take-home-pay">take-home pay
  calculator</a>, Japan's tax stack (social insurance + national income tax +
  reconstruction surtax + residence tax) needs all the pieces to be accurate.
</div>

<h2 id="negotiation">Negotiation, what works in Japan</h2>
<ul>
  <li><strong>Wait for the offer.</strong> Never propose a number in the first interview.
      "I'd like to learn more about the role before discussing compensation" is the
      standard answer.</li>
  <li><strong>Ask for 10–15% above the offer.</strong> Beyond 20% requires hard
      justification (competing written offer, market comparable, current comp).</li>
  <li><strong>Anchor with specifics.</strong> "Based on my competing offer at COMPETITOR
      of ¥XM, I was hoping for ¥YM" lands. "I think I'm worth more" doesn't.</li>
  <li><strong>Non-cash is often easier than base.</strong> Signing bonus, RSU refresh,
      remote-work days, relocation package, training budget, vesting acceleration, these
      are typically negotiable even when base is fixed.</li>
  <li><strong>Don't bluff.</strong> Japanese recruiters check claimed competing offers
      more often than you'd expect. Getting caught burns the offer and your reputation.</li>
</ul>
<div class="callout">
  The <a href="/pillars/negotiation-playbook">salary negotiation playbook</a> includes
  Japan-specific scripts and the
  <a href="/templates#offer">bilingual email templates</a> have ready-made counter-offer
  drafts.
</div>
<!-- ENRICH_V2:salary -->
<h2 id="shunto-2026">2026 Shunto wage growth in context</h2>
<p>Japan's 2026 Shunto (spring labour-management wage negotiations) delivered a 5.26%
average wage increase, the third consecutive year over 5%, and the strongest
sustained wage growth Japan has seen in three decades. Three forces underwrite this:</p>
<ul>
  <li><strong>Demographic crunch.</strong> Japan's working-age population has been
      shrinking ~0.6%/year for a decade. The labour shortage is now systemic, not
      cyclical.</li>
  <li><strong>Sustained inflation.</strong> Core inflation has stayed near 2% since
      late 2023, ending Japan's deflationary equilibrium. Unions can credibly demand
      real-wage growth instead of nominal-only catch-up.</li>
  <li><strong>BoJ policy shift.</strong> The Bank of Japan ended negative interest
      rates in 2024 and continues moving toward normalisation. Higher policy rates
      filter through to bank lending margins and corporate hiring budgets.</li>
</ul>
<p>The practical impact for foreigners:</p>
<ul>
  <li>Job-changers in 2026 typically see 15–25% raises on a move at mid-level,
      25–40% at senior. Internal raises remain conservative at 5–7%.</li>
  <li>Bilingual professionals see the strongest leverage, Robert Walters' 2026
      report flags bilingual roles in tech, finance, and consulting as the top of
      the salary momentum curve.</li>
  <li>Small and mid-size Japanese employers (SMEs) have not kept pace; their wage
      hikes average 3–4%. If you're at an SME, job-changing to a larger employer
      is the comp lever.</li>
</ul>

<h2 id="bilingual-premium">Bilingual premium, real numbers</h2>
<p>Cross-referencing TokyoDev 2025, Daijob 2026, and Robert Walters 2026, the
bilingual premium by role and JLPT level:</p>
<table>
  <thead><tr><th>Role family</th><th>No JP / N5</th><th>N3</th><th>N2</th><th>N1</th></tr></thead>
  <tbody>
    <tr><td>Software engineering (senior)</td><td>¥10–15M</td><td>¥11–17M</td>
        <td>¥13–20M</td><td>¥15–24M</td></tr>
    <tr><td>Product management (mid)</td><td>¥8–12M</td><td>¥10–14M</td>
        <td>¥12–17M</td><td>¥14–20M</td></tr>
    <tr><td>Sales (enterprise AE)</td><td>¥10–16M OTE (rare)</td><td>¥13–20M</td>
        <td>¥18–28M</td><td>¥25–40M+</td></tr>
    <tr><td>Marketing manager</td><td>¥7–10M</td><td>¥8–12M</td>
        <td>¥10–14M</td><td>¥12–18M</td></tr>
    <tr><td>Finance VP</td><td>¥18–25M</td><td>¥22–30M</td>
        <td>¥28–40M</td><td>¥35–55M+</td></tr>
    <tr><td>Consulting (senior consultant)</td><td>¥10–14M</td><td>¥12–17M</td>
        <td>¥15–22M</td><td>¥18–28M</td></tr>
  </tbody>
</table>
<p>The premium curve is steepest between N3 and N2, that's where the management
track typically opens. Above N2, the additional value depends heavily on whether
the role is genuinely customer / stakeholder facing.</p>

<h2 id="asking-for-raise">How to ask for a raise in Japan</h2>
<p>Asking for a raise in Japan is culturally different from the US/UK approach.
Practical guidance:</p>
<ol>
  <li><strong>Time the conversation.</strong> Most Japanese companies have formal
      review cycles in April (start of fiscal year) and/or October. Raising the
      topic 6–8 weeks before review is realistic; bringing it up in February or
      August is unproductive.</li>
  <li><strong>Frame around contribution, not market data.</strong> Lead with what
      you've delivered, not what competitors pay. Even if you privately reference
      market benchmarks, the conversation should sound like recognition for delivered
      value.</li>
  <li><strong>Quantify in their currency.</strong> Use the same KPIs your manager
      reports to <em>their</em> boss. "I delivered project X 2 weeks early and
      reduced costs by ¥Y" lands better than "I'm a great team player".</li>
  <li><strong>Be specific about the amount.</strong> Concrete numbers ("I'd like to
      bring my base to ¥X") work better than "I'd like a raise". Aim 10–20% above
      current as opening ask; expect counter-offers at 5–10%.</li>
  <li><strong>Have BATNA.</strong> The strongest leverage is a competing offer.
      Mercari, PayPay, FAANG Tokyo, and most foreign-cap firms will counter-match
      if they value you. But don't bluff, if you walk in with a competing offer,
      be willing to take it.</li>
  <li><strong>Be patient with the answer.</strong> Most managers can't grant a raise
      unilaterally; the conversation triggers HR and director-level escalation.
      Expect 2–4 weeks to get an answer.</li>
</ol>

<h2 id="benefits-translate">How to compare benefits, Japan vs overseas offers</h2>
<p>Total comp comparisons between Japan and overseas offers should account for:</p>
<ul>
  <li><strong>Income tax.</strong> Japan's progressive rate peaks at 45% national +
      10% local = 55% top marginal. For ¥10M income, effective tax is ~22–25%.
      Compare to US (federal + state) or UK/EU equivalents.</li>
  <li><strong>National Health Insurance.</strong> Effectively universal at low cost
      compared to US private insurance. Premium tied to income; cap around
      ¥980,000/year.</li>
  <li><strong>Pension contribution.</strong> Employee + employer combine at 18.3% of
      salary; employer matches half. Employer's half is effectively additional comp.</li>
  <li><strong>13-month / bonus structure.</strong> Many Japanese employers pay a
      summer (June/July) and winter (December) bonus, typically 1–3 months of base
      each. If quoted as "annual base ¥8M", confirm whether bonuses are included.</li>
  <li><strong>Commuter allowance (通勤手当).</strong> Standard in Japan, typically
      ¥10–50K/month covering train pass. Tax-free up to ¥150,000/month.</li>
  <li><strong>Housing allowance (住宅手当)</strong>, older corporates pay
      ¥20–80K/month. Most modern tech firms have phased this out, rolled into base.</li>
  <li><strong>Relocation package</strong>, international moves should include
      flights, shipping, temporary housing (1–2 months), and lump-sum for setup
      (¥500K–¥2M range). Mercari, Indeed, Stripe, FAANG Tokyo offer these as
      standard for overseas hires.</li>
</ul>

<h2 id="offer-negotiation">Offer negotiation tactics</h2>
<ul>
  <li><strong>Don't accept the first offer.</strong> Most Japanese employers expect
      one round of negotiation. Failing to negotiate signals you're not commercially
      aware. Push back with a specific counter-offer.</li>
  <li><strong>Negotiate base, not bonus.</strong> Base compounds at every future
      raise; bonus is one-time. Push for base first.</li>
  <li><strong>Signing bonus is real.</strong> Mercari, PayPay, LINE Yahoo, FAANG
      Tokyo, and several Japanese SaaS routinely pay ¥1–5M signing bonuses for
      senior hires. Ask.</li>
  <li><strong>RSU / equity grants</strong> are negotiable at FAANG Tokyo and many
      foreign-cap firms, increasingly so at Mercari, PayPay, SmartNews. Ask for an
      explicit grant value.</li>
  <li><strong>Start date.</strong> Pushing your start date 1–2 months later gives the
      previous employer time to pay your remaining bonuses. Useful when leaving a
      Japanese employer with annual bonuses tied to attendance dates.</li>
  <li><strong>Get everything in writing.</strong> Verbal offers in Japan are
      genuinely binding socially, but documented offers (内定通知書) are necessary
      for visa applications and to prevent post-hoc disputes.</li>
</ul>

<h2 id="equity-stock">Equity, RSUs, and stock options in Japan</h2>
<ul>
  <li><strong>RSUs at FAANG Tokyo.</strong> 4-year vest with 1-year cliff is standard;
      grant sizes scale with level. A Senior SWE at Google Japan typically receives
      ¥15–40M in RSU grants over 4 years.</li>
  <li><strong>Stock options at Japanese startups.</strong> Pre-IPO startups offer
      options under a Japanese tax-qualified plan (税制適格ストックオプション).
      Strike price + exercise window matter; ask for the cap table and last
      preferred round price.</li>
  <li><strong>Mercari, freee, Sansan public RSUs.</strong> Now offer RSUs to senior
      engineers and PMs. Grant sizes are smaller than FAANG (typically ¥3–10M over
      4 years) but real.</li>
  <li><strong>Tax treatment.</strong> RSU vesting is taxed as ordinary income in
      Japan. Sale-of-stock gains are taxed separately at 20.315% (national 15.315%
      + local 5%). Reporting on annual tax filing is required if you hold US
      brokerage assets.</li>
  <li><strong>The dollar trap.</strong> RSUs at US-headquartered firms are typically
      USD-denominated. When yen strengthens, your yen-equivalent RSU value drops.
      Some FAANG Tokyo offices offer JPY-pegged grants as an option; ask.</li>
</ul>


<div class="callout">
  Looking for boards, recruiters, or language tools? See our
  <a href="/resources/external-resources">curated external-resources
  directory</a> for 60+ vetted sites with honest usage notes.
</div>
""",
    },

    # ------------------------------------------------------------------ cost of living
    {
        "slug": "cost-of-living",
        "icon": "building",
        "title": "Cost of living in Japan, real 2025–26 numbers, ward by ward",
        "summary": "Real Tokyo rent prices by ward, utilities, groceries, transport, healthcare. Including the deposit, key money, and guarantor fees that catch foreigners off guard.",
        "updated": "May 2026",
        "read_time": "8 min",
        "toc": [
            ("monthly", "Monthly cost breakdown"),
            ("rent-by-ward", "Tokyo rent by ward, actual 2025 numbers"),
            ("moving-in", "Moving-in costs, the foreigner sticker shock"),
            ("utilities", "Utilities and bills"),
            ("groceries", "Groceries, food, eating out"),
            ("transport", "Transport"),
            ("outside-tokyo", "Outside Tokyo, Osaka, Fukuoka, smaller cities"),
            ("hidden", "Hidden costs no one tells you about"),
            ("2026-rent-updates", '2026 rent changes by ward'),
            ("hidden-move-in", 'Hidden move-in costs explained'),
            ("utilities-deep", 'Utilities, what they actually cost'),
            ("foreigner-friendly-landlords", 'Foreigner-friendly real estate agents'),
            ("monthly-budgets", 'Realistic monthly budgets for different lifestyles'),
            ("regional-deltas", 'Tokyo vs Osaka vs Fukuoka vs Sapporo'),
        ],
        "body": """
<h2 id="monthly">Monthly cost breakdown, single professional, Tokyo, 2025–26</h2>
<table>
  <thead><tr><th>Category</th><th>Modest</th><th>Comfortable</th><th>Upscale</th></tr></thead>
  <tbody>
    <tr><td>Rent (1K / 1LDK)</td><td>¥85K</td><td>¥150K</td><td>¥280K</td></tr>
    <tr><td>Utilities (gas / electric / water)</td><td>¥10K</td><td>¥18K</td><td>¥25K</td></tr>
    <tr><td>Internet (home fibre)</td><td>¥5K</td><td>¥5.5K</td><td>¥6K</td></tr>
    <tr><td>Mobile (MVNO)</td><td>¥2K</td><td>¥3K</td><td>¥6K (major carrier)</td></tr>
    <tr><td>Groceries (home cooking)</td><td>¥30K</td><td>¥45K</td><td>¥70K</td></tr>
    <tr><td>Eating out / coffee</td><td>¥15K</td><td>¥35K</td><td>¥80K+</td></tr>
    <tr><td>Transport (commuter pass usually reimbursed)</td><td>¥10K leisure</td><td>¥15K</td><td>¥25K</td></tr>
    <tr><td>National Health Insurance (employed)</td><td>~5% of salary, deducted</td><td>–</td><td>–</td></tr>
    <tr><td>Misc (entertainment, clothing)</td><td>¥20K</td><td>¥40K</td><td>¥100K</td></tr>
    <tr><td><strong>Total (excluding NHI)</strong></td><td><strong>¥177K</strong></td><td><strong>¥311K</strong></td><td><strong>¥592K+</strong></td></tr>
  </tbody>
</table>
<p>The "comfortable" column maps to roughly ¥6M gross annual income for a single person
with no dependants. "Upscale" maps to ¥12M+.</p>

<h2 id="rent-by-ward">Tokyo rent by ward, actual 2025 numbers</h2>
<p>Studio (1R / 1K) average rent in central Tokyo wards was around ¥95,000/mo in mid-2025;
in Minato, Chiyoda, or Shibuya it rises to ¥135–150K. Larger units (1LDK) show much wider
spread, Shibuya 1LDK runs ¥230–300K while Setagaya runs ¥180–230K for similar size.</p>
<table>
  <thead><tr><th>Ward</th><th>1K / 1R</th><th>1LDK</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>Minato (Roppongi, Azabu)</td><td>¥140–180K</td><td>¥270–400K</td><td>Embassies, foreign HQs</td></tr>
    <tr><td>Chiyoda (Marunouchi, Kanda)</td><td>¥130–170K</td><td>¥250–350K</td><td>Big-corp HQ belt</td></tr>
    <tr><td>Shibuya</td><td>¥130–160K</td><td>¥230–300K</td><td>Tech, startups; foreigner-friendly</td></tr>
    <tr><td>Shinjuku</td><td>¥110–140K</td><td>¥190–260K</td><td>Mixed; nightlife</td></tr>
    <tr><td>Meguro / Nakameguro</td><td>¥110–135K</td><td>¥200–270K</td><td>Trendy, walkable</td></tr>
    <tr><td>Setagaya (Sangenjaya, Shimokita)</td><td>¥85–110K</td><td>¥180–230K</td><td>Family-friendly; 3 min to Shibuya from Sangenjaya</td></tr>
    <tr><td>Shinagawa</td><td>¥100–130K</td><td>¥190–250K</td><td>Excellent shinkansen access</td></tr>
    <tr><td>Toshima (Ikebukuro)</td><td>¥90–120K</td><td>¥160–220K</td><td>Busy, slightly cheaper</td></tr>
    <tr><td>Nakano</td><td>¥75–100K</td><td>¥140–190K</td><td>Quiet, 5 min to Shinjuku</td></tr>
    <tr><td>Suginami (Koenji, Asagaya)</td><td>¥75–100K</td><td>¥140–190K</td><td>Quiet residential, JR Chuo</td></tr>
    <tr><td>Nerima / Itabashi</td><td>¥65–85K</td><td>¥120–170K</td><td>Suburban, 30 min to Shinjuku</td></tr>
    <tr><td>Yokohama (across the prefecture line)</td><td>¥60–85K</td><td>¥110–170K</td><td>30–50 min to central Tokyo</td></tr>
  </tbody>
</table>
<div class="callout">
  <strong>The Setagaya trick:</strong> Sangenjaya station is 3 minutes from Shibuya on
  the Den-en-toshi line, but rents drop 30–40% the moment you cross the ward boundary.
  Setagaya, Suginami, and Nakano are the "stealth" wards most foreigners eventually move
  to after their first year.
</div>

<h2 id="moving-in">Moving-in costs, the foreigner sticker shock</h2>
<p>Initial costs on a Japanese rental routinely total <strong>3–5 months of rent</strong>
upfront. For a ¥150K/mo apartment, budget ¥450–750K cash on signing.</p>
<table>
  <thead><tr><th>Item</th><th>Typical amount</th></tr></thead>
  <tbody>
    <tr><td>First month's rent (前家賃)</td><td>1 month</td></tr>
    <tr><td>Deposit (敷金 / shikikin)</td><td>1–2 months (refundable, mostly)</td></tr>
    <tr><td>Key money (礼金 / reikin)</td><td>0–2 months (non-refundable gift to landlord)</td></tr>
    <tr><td>Agent fee (仲介手数料)</td><td>1 month + 10% tax</td></tr>
    <tr><td>Guarantor company fee (保証会社)</td><td>30–100% of one month's rent</td></tr>
    <tr><td>Fire insurance (火災保険)</td><td>¥15–25K for 2 years</td></tr>
    <tr><td>Lock change (鍵交換)</td><td>¥15–30K</td></tr>
  </tbody>
</table>
<p>Foreigner-friendly agencies (GaijinPot Housing, Apartment Japan, Ken Real Estate,
E-Housing) skip key money on most properties, which can save you 1–2 months upfront.
Sakura House and similar share-house operators offer short-term stays with no key money
and no guarantor required, useful for your first 3–6 months.</p>
<div class="warn">
  <strong>The guarantor problem.</strong> Most Japanese landlords require a Japanese
  citizen or PR-holder as your personal guarantor. If you don't have one, you'll go
  through a guarantor company, fee 30–100% of one month's rent, plus an annual fee of
  ~10% of one month thereafter. Always built into the price quotes from foreigner-friendly
  agencies.
</div>

<h2 id="utilities">Utilities and bills, single person in Tokyo</h2>
<table>
  <thead><tr><th>Bill</th><th>Monthly cost</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>Electricity</td><td>¥4–10K (winter peaks)</td><td>TEPCO is default; new entrants slightly cheaper</td></tr>
    <tr><td>Gas</td><td>¥3–6K</td><td>Toho Gas; turns on heating + hot water</td></tr>
    <tr><td>Water</td><td>¥2–4K (billed every 2 months)</td><td>Tokyo Water Works</td></tr>
    <tr><td>Internet (home fibre)</td><td>¥4–6K</td><td>NURO, eo, Hikari, install 2–4 weeks</td></tr>
    <tr><td>Mobile (MVNO)</td><td>¥1.5–4K</td><td>IIJmio, povo, mineo, Sakura Mobile</td></tr>
    <tr><td>NHK fee (mandatory if you have a TV)</td><td>¥1,225/mo</td><td>Legal obligation if you own a TV; collected by NHK agents door-to-door</td></tr>
  </tbody>
</table>

<h2 id="groceries">Groceries, food, eating out</h2>
<ul>
  <li><strong>Supermarkets:</strong> Seiyu, OK Store, Maruetsu (mid-range); Life, Inageya
      (slightly pricier); Aeon (suburban superstore); Gyomu Super (bulk + frozen, foreign
      ingredients).</li>
  <li><strong>Eating out (single meal):</strong> ¥600–1,200 for a casual lunch set, ¥800–
      1,500 for ramen or curry, ¥2,000–4,000 for dinner at an izakaya.</li>
  <li><strong>Convenience stores</strong> (7-Eleven, FamilyMart, Lawson) are heavily used, bentou ¥500–700, decent coffee ¥150, snacks ¥150–300.</li>
  <li><strong>Foreign ingredients:</strong> National Azabu, Nissin World Delicatessen,
      Kaldi, and select Aeon stores carry imported groceries at 1.5–3× the price of
      Japanese equivalents.</li>
</ul>

<h2 id="transport">Transport</h2>
<ul>
  <li><strong>Commuter pass (通勤定期):</strong> universally reimbursed by employers.
      Typically ¥10–25K/mo depending on commute distance.</li>
  <li><strong>Leisure transport:</strong> Suica or PASMO IC card. Typical fares ¥150–300
      within central Tokyo, ¥300–500 cross-ward.</li>
  <li><strong>Taxis:</strong> ¥500 base + ¥120 per ~250m. Tokyo taxis are clean but pricier
      than ride-share. Uber covers Tokyo, mostly via taxi partnerships.</li>
  <li><strong>JR Pass:</strong> No longer worth it for residents (eligibility check is
      strict). Use IC card for daily transit; book shinkansen tickets separately as needed.</li>
</ul>

<h2 id="outside-tokyo">Outside Tokyo, Osaka, Fukuoka, smaller cities</h2>
<table>
  <thead><tr><th>City</th><th>1LDK rent</th><th>COL vs. Tokyo</th></tr></thead>
  <tbody>
    <tr><td>Osaka</td><td>¥75–120K</td><td>~75%</td></tr>
    <tr><td>Yokohama</td><td>¥100–180K</td><td>~85%</td></tr>
    <tr><td>Nagoya</td><td>¥65–110K</td><td>~70%</td></tr>
    <tr><td>Fukuoka</td><td>¥55–90K</td><td>~65%</td></tr>
    <tr><td>Sapporo</td><td>¥45–80K</td><td>~60% (high winter utility bills)</td></tr>
    <tr><td>Sendai / Kyoto</td><td>¥55–90K</td><td>~70%</td></tr>
  </tbody>
</table>
<div class="callout">
  Run an actual side-by-side comparison on the
  <a href="/tools/col-comparator">cost-of-living comparator</a>, accounts for tax rates,
  effective purchasing power, and FX.
</div>

<h2 id="hidden">Hidden costs no one tells you about</h2>
<ul>
  <li><strong>Hanko (印鑑):</strong> ¥3–10K for a personal seal. You'll need one
      eventually for banking, lease signing, or any government paperwork.</li>
  <li><strong>Lease renewal (更新料):</strong> typically 1 month of rent every 2 years.
      Standard at most apartments; some landlords waive it.</li>
  <li><strong>Aircon cleaning:</strong> required if you stay 3+ years. ¥10–20K per unit
      every 2–3 years for professional cleaning.</li>
  <li><strong>NHK enforcer:</strong> the public broadcaster sends collectors door-to-door
      to enforce TV fees. Legal obligation if you own a TV; many foreigners skip a TV
      entirely to avoid this.</li>
  <li><strong>Health insurance ramp-up.</strong> You'll pay ~5% of salary into 健康保険
      from your first paycheck, even though you've used nothing yet. It's pre-tax and
      automatic for employed workers.</li>
  <li><strong>Residence tax (住民税) in year 2.</strong> You pay zero residence tax in
      year 1 because Japan bills the previous year's income. From May/June of year 2
      onwards, expect ~10% of last year's income deducted monthly.</li>
</ul>
<!-- ENRICH_V2:cost-of-living -->
<h2 id="2026-rent-updates">2026 rent changes by ward</h2>
<p>Tokyo rents continued upward through 2025 and into 2026, driven by inbound
tourism, foreign-worker inflows, and the broader Tokyo population concentration.
Year-over-year increases by ward (2025 vs 2026, 1LDK average):</p>
<table>
  <thead><tr><th>Ward</th><th>2025 avg 1LDK</th><th>2026 avg 1LDK</th><th>YoY change</th></tr></thead>
  <tbody>
    <tr><td>Minato (Roppongi, Akasaka)</td><td>¥260K</td><td>¥285K</td><td>+9.6%</td></tr>
    <tr><td>Shibuya</td><td>¥230K</td><td>¥255K</td><td>+10.9%</td></tr>
    <tr><td>Shinjuku</td><td>¥190K</td><td>¥210K</td><td>+10.5%</td></tr>
    <tr><td>Meguro (Ebisu, Nakameguro)</td><td>¥210K</td><td>¥230K</td><td>+9.5%</td></tr>
    <tr><td>Chiyoda (Marunouchi)</td><td>¥250K</td><td>¥275K</td><td>+10.0%</td></tr>
    <tr><td>Setagaya (Sangenjaya, Yoga)</td><td>¥175K</td><td>¥195K</td><td>+11.4%</td></tr>
    <tr><td>Suginami (Asagaya, Koenji)</td><td>¥150K</td><td>¥168K</td><td>+12.0%</td></tr>
    <tr><td>Nakano</td><td>¥155K</td><td>¥172K</td><td>+11.0%</td></tr>
    <tr><td>Toshima (Ikebukuro)</td><td>¥145K</td><td>¥162K</td><td>+11.7%</td></tr>
    <tr><td>Koto (Toyosu, Kachidoki)</td><td>¥170K</td><td>¥188K</td><td>+10.6%</td></tr>
    <tr><td>Adachi / Katsushika</td><td>¥110K</td><td>¥122K</td><td>+10.9%</td></tr>
  </tbody>
</table>
<p>The cheapest commuter-friendly options for foreigners willing to add 20–30 minutes
to the commute: Nerima, Itabashi, Adachi, Katsushika, Edogawa wards (¥100–150K
1LDK). Saitama-side Kawaguchi, Toda, Warabi (¥90–130K 1LDK) are also viable for
Marunouchi/Ikebukuro-based jobs.</p>

<h2 id="hidden-move-in">Hidden move-in costs explained</h2>
<p>Tokyo rentals carry significant upfront costs that catch newcomers off-guard.
For a ¥180,000/month apartment, expect ¥900K–¥1.1M total move-in cost:</p>
<table>
  <thead><tr><th>Cost component</th><th>Typical range</th><th>What it is</th></tr></thead>
  <tbody>
    <tr><td>Deposit (敷金, shikikin)</td><td>1–2 months rent</td>
        <td>Refunded at end of contract minus cleaning. Often only partially refunded.</td></tr>
    <tr><td>Key money (礼金, reikin)</td><td>0–2 months rent</td>
        <td>Non-refundable "thank you" payment to landlord. Increasingly negotiable;
        2026 deals more often waive this.</td></tr>
    <tr><td>Agency fee (仲介手数料)</td><td>1 month rent + tax</td>
        <td>Real-estate agent commission. Sometimes negotiable down to half a month.</td></tr>
    <tr><td>Guarantor company fee (保証会社)</td><td>50–100% of one month, then ¥10K/year</td>
        <td>Replaces personal guarantor. Standard for foreigners.</td></tr>
    <tr><td>Fire insurance (火災保険)</td><td>¥15–25K / 2 years</td>
        <td>Required, sold through real-estate agent.</td></tr>
    <tr><td>Lock change (鍵交換)</td><td>¥15–25K</td>
        <td>Charged at move-in to replace lock from prior tenant.</td></tr>
    <tr><td>Cleaning fee (ハウスクリーニング)</td><td>¥30–80K</td>
        <td>Pre-paid at signing; covers post-move-out cleaning.</td></tr>
    <tr><td>First month + prorated current month</td><td>1–2 months</td>
        <td>Standard prorate if you move mid-month.</td></tr>
  </tbody>
</table>
<p>2025–26 trend: increasing share of "敷礼ゼロ" (zero deposit, zero key money)
properties, especially foreigner-friendly chains like Sumitomo Real Estate Villa,
Leopalace, Oakhouse, and apartments listed on GaijinPot Housing. These reduce
move-in by ¥300–500K but may have higher monthly rent or stricter exit cleaning fees.</p>

<h2 id="utilities-deep">Utilities, what they actually cost</h2>
<table>
  <thead><tr><th>Utility</th><th>Typical 1LDK / month</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>Electricity (TEPCO Tokyo)</td><td>¥4,500–9,000</td>
        <td>Higher in summer (AC) and winter (heating). Worst month can hit ¥15K.</td></tr>
    <tr><td>Gas</td><td>¥3,500–6,500</td>
        <td>"Propane" buildings (LPG) are noticeably more expensive than city gas.</td></tr>
    <tr><td>Water</td><td>¥2,500–4,000</td>
        <td>Billed every 2 months; relatively stable.</td></tr>
    <tr><td>Internet (NTT Flets / au Hikari / Nuro)</td><td>¥4,500–6,500</td>
        <td>Most new contracts include 1 Gbps fiber. Nuro is fastest (2 Gbps) in
        eligible areas.</td></tr>
    <tr><td>Mobile (Y!Mobile / UQ / IIJmio / Rakuten Mobile)</td><td>¥1,500–4,500</td>
        <td>MVNO options are widely available. Big-3 carriers (Docomo, au, SoftBank)
        run ¥6,500+/month.</td></tr>
    <tr><td>NHK fee</td><td>¥1,225 (terrestrial) / ¥2,170 (satellite) / month</td>
        <td>Legally required if you have a TV; not actively enforced for foreigners
        but expect collectors to ring.</td></tr>
  </tbody>
</table>

<h2 id="foreigner-friendly-landlords">Foreigner-friendly real estate agents</h2>
<p>Mainstream Japanese real-estate agents often quietly refuse to show properties
to foreigners (typically citing "the landlord's preference"). Agents to use
instead:</p>
<ul>
  <li><strong>GaijinPot Housing / Apartments.com Japan</strong>, large foreigner-friendly
      listings, English-language support.</li>
  <li><strong>Sakura House / Oakhouse</strong>, share-houses and short-term
      apartments aimed at foreigners. Easy to set up; higher monthly rent but
      minimal move-in.</li>
  <li><strong>Tokyo Apartment Inc / Real Tokyo Estate</strong>, bilingual brokers
      with experience handling foreigner applications.</li>
  <li><strong>Plaza Homes</strong>, long-established serviced-apartment broker;
      historically luxury-focused but useful for executive relocations.</li>
  <li><strong>Ken Corporation</strong>, high-end foreigner-focused; specialises in
      Roppongi / Hiroo / Azabu market.</li>
  <li><strong>Apaman Shop / Mini Mini / Able</strong>, large Japanese chains; less
      foreigner-friendly but worth trying if you can apply with a JP-speaking friend.</li>
</ul>
<p>For 2026, increasingly common alternative: Mercari Real Estate, Smartrent
(foreigner-friendly), and Square (instant lease) apps offer rentals with online
application, no in-person visits required.</p>

<h2 id="monthly-budgets">Realistic monthly budgets for different lifestyles</h2>
<table>
  <thead><tr><th>Category</th><th>Frugal (¥250K/mo)</th><th>Comfortable (¥400K/mo)</th><th>Premium (¥700K+/mo)</th></tr></thead>
  <tbody>
    <tr><td>Rent</td><td>¥80K (1R, Itabashi)</td><td>¥180K (1LDK, Setagaya)</td><td>¥380K (2LDK, Minato)</td></tr>
    <tr><td>Utilities + internet + mobile</td><td>¥12K</td><td>¥18K</td><td>¥30K</td></tr>
    <tr><td>Food (groceries + eating out)</td><td>¥45K</td><td>¥85K</td><td>¥160K</td></tr>
    <tr><td>Transport</td><td>¥12K (employer pays)</td><td>¥15K (employer pays + occasional taxi)</td><td>¥30K (taxis common)</td></tr>
    <tr><td>Health insurance + pension (employee share)</td><td>¥20K (¥4M salary)</td><td>¥40K (¥8M salary)</td><td>¥75K (¥15M+ salary)</td></tr>
    <tr><td>Misc / entertainment / clothing</td><td>¥30K</td><td>¥60K</td><td>¥150K</td></tr>
    <tr><td>Gym, hobbies, classes</td><td>¥7K (city gym)</td><td>¥15K (Anytime Fitness)</td><td>¥30K (boutique studio)</td></tr>
    <tr><td>Total approx</td><td>¥206K</td><td>¥413K</td><td>¥855K</td></tr>
  </tbody>
</table>

<h2 id="regional-deltas">Tokyo vs Osaka vs Fukuoka vs Sapporo</h2>
<table>
  <thead><tr><th>Metric</th><th>Tokyo</th><th>Osaka</th><th>Fukuoka</th><th>Sapporo</th></tr></thead>
  <tbody>
    <tr><td>1LDK rent (central)</td><td>¥180K</td><td>¥110K</td><td>¥85K</td><td>¥75K</td></tr>
    <tr><td>Eating out (cheap lunch)</td><td>¥1,200</td><td>¥1,000</td><td>¥900</td><td>¥900</td></tr>
    <tr><td>Eating out (mid-range dinner)</td><td>¥4,000</td><td>¥3,500</td><td>¥3,000</td><td>¥3,000</td></tr>
    <tr><td>Foreigner-friendly job pool</td><td>Massive</td><td>Modest</td><td>Small but growing</td><td>Very small</td></tr>
    <tr><td>Salary gap vs Tokyo</td><td>–</td><td>−5–10%</td><td>−15–25%</td><td>−20–30%</td></tr>
    <tr><td>English-speaking healthcare</td><td>Many options</td><td>Some</td><td>Few</td><td>Very few</td></tr>
    <tr><td>International schools</td><td>20+ options</td><td>4–5</td><td>1–2</td><td>1</td></tr>
  </tbody>
</table>
<p>For families with two incomes and one needing English-medium school, Tokyo's
premium pays off. For solo workers in remote-friendly roles, Fukuoka or Sapporo
can give back ¥80K/month in rent alone while keeping ¥10M+ tech comp on the
table.</p>

""",
    },

    # ------------------------------------------------------------------ interview phrases
    {
        "slug": "interview-phrases",
        "icon": "message",
        "title": "Useful Japanese for interviews, phrases by interview stage",
        "summary": "30+ phrases organised by interview stage, entering the room, self-introduction, answering common questions, asking questions back, and closing politely. With romaji and English glosses.",
        "updated": "May 2026",
        "read_time": "6 min",
        "toc": [
            ("entering", "Entering the room and greetings"),
            ("intro", "Self-introduction"),
            ("answering", "Answering common questions"),
            ("asking", "Asking questions back"),
            ("closing", "Closing and thank-you"),
            ("uncertain", "When you don't understand"),
            ("keigo-errors", 'Common keigo errors foreigners make'),
            ("tough-question-phrases", 'Phrases for tough questions'),
            ("salary-discussion", 'Phrases for salary discussions'),
            ("declining-clarifying", 'Phrases for declining or clarifying'),
            ("video-specific", 'Phrases specific to video interviews'),
        ],
        "body": """
<p>You don't need to be fluent to use a handful of Japanese phrases in your interview, even a few well-deployed lines signal cultural awareness and respect. Use these alongside
your normal English (or Japanese) answers.</p>

<h2 id="entering">Entering the room and greetings</h2>
<table>
  <thead><tr><th>Japanese</th><th>Romaji</th><th>When to use</th></tr></thead>
  <tbody>
    <tr><td>失礼いたします。</td><td>Shitsurei itashimasu.</td><td>Entering or leaving the room (literally "excuse me")</td></tr>
    <tr><td>本日はよろしくお願いいたします。</td><td>Honjitsu wa yoroshiku onegai itashimasu.</td><td>Opening greeting after sitting down</td></tr>
    <tr><td>お忙しいところお時間をいただき、ありがとうございます。</td><td>O-isogashii tokoro o-jikan o itadaki, arigatō gozaimasu.</td><td>"Thank you for taking time despite being busy", graceful opener</td></tr>
    <tr><td>失礼いたします。</td><td>Shitsurei itashimasu.</td><td>Before sitting down (after you're invited)</td></tr>
    <tr><td>頂戴いたします。</td><td>Chōdai itashimasu.</td><td>When receiving a business card</td></tr>
  </tbody>
</table>

<h2 id="intro">Self-introduction (自己紹介 / jiko-shōkai)</h2>
<table>
  <thead><tr><th>Japanese</th><th>Romaji</th><th>Meaning</th></tr></thead>
  <tbody>
    <tr><td>自己紹介させていただきます。</td><td>Jiko-shōkai sasete itadakimasu.</td><td>"Please allow me to introduce myself"</td></tr>
    <tr><td>〜と申します。</td><td>~ to mōshimasu.</td><td>"My name is ~" (formal)</td></tr>
    <tr><td>〜の出身です。</td><td>~ no shusshin desu.</td><td>"I'm from ~"</td></tr>
    <tr><td>前職では〜として働いておりました。</td><td>Zenshoku de wa ~ toshite hataraite orimashita.</td><td>"At my previous role, I worked as ~"</td></tr>
    <tr><td>〜の経験があります。</td><td>~ no keiken ga arimasu.</td><td>"I have experience in ~"</td></tr>
    <tr><td>〜に取り組んでまいりました。</td><td>~ ni torikunde mairimashita.</td><td>"I have been working on ~" (humble form)</td></tr>
    <tr><td>本日はどうぞよろしくお願いいたします。</td><td>Honjitsu wa dōzo yoroshiku onegai itashimasu.</td><td>Closing the self-introduction</td></tr>
  </tbody>
</table>

<h2 id="answering">Answering common questions</h2>
<table>
  <thead><tr><th>Japanese</th><th>Romaji</th><th>Meaning</th></tr></thead>
  <tbody>
    <tr><td>御社で働きたい理由は〜です。</td><td>Onsha de hatarakitai riyū wa ~ desu.</td><td>"My reason for wanting to work at your company is ~"</td></tr>
    <tr><td>御社の〜という製品に強く共感しております。</td><td>Onsha no ~ to iu seihin ni tsuyoku kyōkan shite orimasu.</td><td>"I strongly identify with your company's ~ product" (for "why this company?")</td></tr>
    <tr><td>これまでの経験を活かして、〜に貢献したいと考えております。</td><td>Kore made no keiken o ikashite, ~ ni kōken shitai to kangaete orimasu.</td><td>"Using my past experience, I'd like to contribute to ~"</td></tr>
    <tr><td>長期的にキャリアを築きたいと考えております。</td><td>Chōkiteki ni kyaria o kizukitai to kangaete orimasu.</td><td>"I want to build a long-term career" (good answer to "where in 5 years?")</td></tr>
    <tr><td>強みは〜です。</td><td>Tsuyomi wa ~ desu.</td><td>"My strength is ~"</td></tr>
    <tr><td>課題は〜と考えており、現在〜に取り組んでおります。</td><td>Kadai wa ~ to kangaete ori, genzai ~ ni torikunde orimasu.</td><td>"I see ~ as a challenge and am currently working on ~" (weaknesses)</td></tr>
  </tbody>
</table>

<h2 id="asking">Asking questions back</h2>
<table>
  <thead><tr><th>Japanese</th><th>Romaji</th><th>Meaning</th></tr></thead>
  <tbody>
    <tr><td>一点伺ってもよろしいでしょうか。</td><td>Itten ukagatte mo yoroshii deshō ka.</td><td>"May I ask one question?"</td></tr>
    <tr><td>このポジションで成功している方の共通点を教えていただけますか。</td><td>Kono pojishon de seikō shite iru kata no kyōtsūten o oshiete itadakemasu ka.</td><td>"What do successful people in this role have in common?"</td></tr>
    <tr><td>入社後の最初の3ヶ月で期待される成果は何でしょうか。</td><td>Nyūsha-go no saisho no san-ka-getsu de kitai sareru seika wa nan deshō ka.</td><td>"What outcomes are expected in the first 3 months after joining?"</td></tr>
    <tr><td>チームの構成について教えていただけますでしょうか。</td><td>Chīmu no kōsei ni tsuite oshiete itadakemasu deshō ka.</td><td>"Could you tell me about the team's structure?"</td></tr>
    <tr><td>評価制度について伺ってもよろしいでしょうか。</td><td>Hyōka seido ni tsuite ukagatte mo yoroshii deshō ka.</td><td>"May I ask about the evaluation system?"</td></tr>
  </tbody>
</table>

<h2 id="closing">Closing and thank-you</h2>
<table>
  <thead><tr><th>Japanese</th><th>Romaji</th><th>Meaning</th></tr></thead>
  <tbody>
    <tr><td>本日は貴重なお時間をいただき、ありがとうございました。</td><td>Honjitsu wa kichō na o-jikan o itadaki, arigatō gozaimashita.</td><td>"Thank you for your valuable time today"</td></tr>
    <tr><td>引き続き、よろしくお願いいたします。</td><td>Hikitsuzuki, yoroshiku onegai itashimasu.</td><td>"I look forward to continuing the process"</td></tr>
    <tr><td>失礼いたします。</td><td>Shitsurei itashimasu.</td><td>Final phrase as you leave the room</td></tr>
  </tbody>
</table>

<h2 id="uncertain">When you don't understand</h2>
<table>
  <thead><tr><th>Japanese</th><th>Romaji</th><th>Meaning</th></tr></thead>
  <tbody>
    <tr><td>恐れ入りますが、もう一度お願いできますでしょうか。</td><td>Osoreirimasu ga, mō ichido onegai dekimasu deshō ka.</td><td>"I'm sorry, could you say that again?" (formal)</td></tr>
    <tr><td>もう少しゆっくりお願いできますでしょうか。</td><td>Mō sukoshi yukkuri onegai dekimasu deshō ka.</td><td>"Could you speak a little more slowly, please?"</td></tr>
    <tr><td>申し訳ございませんが、英語でお答えしてもよろしいでしょうか。</td><td>Mōshiwake gozaimasen ga, eigo de o-kotae shite mo yoroshii deshō ka.</td><td>"My apologies, may I answer in English?"</td></tr>
    <tr><td>少し考える時間をいただいてもよろしいでしょうか。</td><td>Sukoshi kangaeru jikan o itadaite mo yoroshii deshō ka.</td><td>"May I have a moment to think?"</td></tr>
  </tbody>
</table>
<!-- ENRICH_V2:interview-phrases -->
<h2 id="keigo-errors">Common keigo errors foreigners make</h2>
<p>The 10 most common keigo (Japanese honorific language) errors in interviews:</p>
<table>
  <thead><tr><th>Wrong</th><th>Right</th><th>Why</th></tr></thead>
  <tbody>
    <tr><td>御社の社長</td><td>御社の社長様 (or "社長の〇〇様")</td>
        <td>Use 様 with the title or name; bare title is informal.</td></tr>
    <tr><td>御社で頑張りたい</td><td>御社で貢献したい</td>
        <td>頑張る is colloquial; 貢献する shows intent to add value.</td></tr>
    <tr><td>御社のサービスを使ってます</td><td>御社のサービスを使わせていただいております</td>
        <td>The humble form acknowledges privilege of using the service.</td></tr>
    <tr><td>分かりました</td><td>承知いたしました or かしこまりました</td>
        <td>分かりました is fine for peers but too plain for interviewers.</td></tr>
    <tr><td>すみません (everything)</td><td>申し訳ございません / 失礼いたしました</td>
        <td>すみません is informal; reserve for very minor things.</td></tr>
    <tr><td>大丈夫です</td><td>問題ございません or 結構です</td>
        <td>大丈夫 is fine in daily life but too plain for interviews.</td></tr>
    <tr><td>あなたの会社</td><td>御社 (in speech) / 貴社 (in writing)</td>
        <td>あなた is too direct in this context.</td></tr>
    <tr><td>させてもらう</td><td>させていただく</td>
        <td>させていただく is the proper humble version.</td></tr>
    <tr><td>うちの会社</td><td>弊社 or 当社</td>
        <td>うち is too casual when speaking to outsiders.</td></tr>
    <tr><td>聞かせていただけませんか</td><td>お聞かせいただけませんか or お聞かせ願えませんか</td>
        <td>Add お to make it more polite.</td></tr>
  </tbody>
</table>

<h2 id="tough-question-phrases">Phrases for tough questions</h2>
<h3>When you don't know an answer</h3>
<ul>
  <li><em>"申し訳ございません、その点については存じ上げません. 入社後にぜひ学ばせていただきたいと思います."</em><br>
      ("I apologise, I'm not familiar with that point. I'd very much like to learn
      about it after joining.")</li>
  <li><em>"〇〇については経験がございませんが、近い経験として△△を御紹介させていただけますでしょうか."</em><br>
      ("I don't have experience with X, but may I share related experience with Y?")</li>
</ul>
<h3>When discussing past failures</h3>
<ul>
  <li><em>"当時は〇〇の課題があり、解決のため△△を試みましたが、結果としては□□となりました.
      その経験を踏まえ、現在は◇◇の点に注意するようにしております."</em><br>
      (Structure: there was X challenge; I tried Y; result was Z; based on that
      experience I now pay attention to W.)</li>
</ul>
<h3>When explaining a gap in your career</h3>
<ul>
  <li><em>"〇〇から△△までの期間は、家族の事情で一時帰国しておりました."</em>
      (Family reasons.)</li>
  <li><em>"資格取得 / スキルアップのための学習期間としておりました."</em>
      (Studying for certifications / upskilling.)</li>
</ul>

<h2 id="salary-discussion">Phrases for salary discussions</h2>
<ul>
  <li><em>"希望年収は、〇〇万円から△△万円を想定しております."</em><br>
      ("My expected annual is in the range of ¥X to ¥Y.")</li>
  <li><em>"前職の年収を参考に、貢献度に応じた評価をいただければと考えております."</em><br>
      ("Based on my previous annual, I would appreciate compensation that reflects
      my contribution.")</li>
  <li><em>"具体的な金額については、御社の規定とご相談させていただければと存じます."</em><br>
      ("I would like to discuss the specific amount based on your company's
      compensation structure.")</li>
  <li><em>"福利厚生も含めた総合的な条件で検討させていただきたいと考えております."</em><br>
      ("I would like to evaluate the offer including total benefits.")</li>
</ul>

<h2 id="declining-clarifying">Phrases for declining or clarifying</h2>
<h3>Declining a question politely</h3>
<ul>
  <li><em>"申し訳ございませんが、その件については現在お話しできる状況にございません."</em><br>
      ("I apologise, but I'm not in a position to discuss that at the moment.")</li>
</ul>
<h3>Asking for clarification</h3>
<ul>
  <li><em>"恐れ入りますが、もう一度お伺いしてもよろしいでしょうか."</em><br>
      ("Excuse me, could I ask you to repeat that?")</li>
  <li><em>"〇〇という理解でよろしいでしょうか."</em><br>
      ("Is my understanding correct that... X?")</li>
</ul>
<h3>Indicating you need to think</h3>
<ul>
  <li><em>"少し考えるお時間をいただけますか."</em><br>
      ("May I have a moment to think?")</li>
</ul>

<h2 id="video-specific">Phrases specific to video interviews</h2>
<ul>
  <li>Opening: <em>"本日はオンラインでの面接の機会をいただき、ありがとうございます."</em>
      ("Thank you for the online interview opportunity today.")</li>
  <li>Audio/video issues: <em>"申し訳ございません、音声が少し聞き取りづらかったのですが、
      もう一度お願いできますでしょうか."</em>
      ("I apologise, the audio was hard to hear; could you repeat?")</li>
  <li>Ending: <em>"本日は貴重なお時間をいただき、誠にありがとうございました.
      引き続きどうぞよろしくお願いいたします."</em>
      ("Thank you for your valuable time today. I look forward to continuing the
      process.")</li>
  <li>Hanging up: <em>"それでは、失礼いたします."</em>
      ("Then, please excuse me."), wait for the interviewer to hang up first.</li>
</ul>

""",
    },

    # ------------------------------------------------------------------ red flags
    {
        "slug": "red-flags",
        "icon": "flag",
        "title": "Red flags, how to spot a black company before you sign",
        "summary": "Black companies (ブラック企業) are real and disproportionately affect foreign workers. The specific warning signs in job listings, interview questions to flush them out, and the labour-law violations to know about.",
        "updated": "May 2026",
        "read_time": "9 min",
        "toc": [
            ("what", "What a black company actually is"),
            ("listing-flags", "Red flags in the job listing"),
            ("interview-flags", "Red flags during the interview"),
            ("legal", "What Japanese labour law actually requires"),
            ("post-offer", "Pre-signing checks, contract clauses to watch"),
            ("if-stuck", "If you're already there"),
            ("foreign-specific", "Risks specific to foreign workers"),
            ("hidden-flags", 'Hidden red flags in modern job posts'),
            ("remote-flags", 'Remote-work and post-pandemic red flags'),
            ("forum-due-diligence", 'Forum due-diligence, Reddit, Glassdoor, OpenWork'),
            ("contract-flags", 'Contract / offer-letter red flags'),
            ("escape-plan", "If you're already in a black company, your exit plan"),
        ],
        "body": """
<h2 id="what">What a "black company" (ブラック企業 / burakku kigyō) actually is</h2>
<p>The term emerged in the early 2000s to describe employers that systematically violate
Japanese labour law, especially around working hours and unpaid overtime, and treat
employees as expendable. The phenomenon is widespread enough that the Ministry of Health,
Labour and Welfare maintains a public database of repeat-offender employers, and the
2018 Work Style Reform Law capped overtime at 100 hours/month and 720 hours/year in part
to address it.</p>
<p>Common-sector concentrations: IT services (especially SI / system-integration), food
service, construction, retail, low-end eikaiwa, and the "blackest" of all, certain
healthcare staffing firms. Tech product companies, foreign-affiliated firms, and the
major Japanese employers run by lifetime-employment culture are generally not in this
bucket.</p>

<h2 id="listing-flags">Red flags in the job listing itself</h2>
<ul>
  <li><strong>"Family-like atmosphere" (アットホームな職場) / "We're a family":</strong>
      almost universally signals that boundaries don't exist. The team will expect after-
      hours drinking, weekend events, and personal-life intrusion.</li>
  <li><strong>"Hard-workers welcome" (ガッツのある方) / "passionate people":</strong>
      Japanese HR code for "we don't pay enough but we want long hours anyway."</li>
  <li><strong>"Energetic young workplace":</strong> read as either "we discriminate against
      older candidates" or "we burn through people quickly."</li>
  <li><strong>Vague salary ("経験により" / "based on experience" / "negotiable"):</strong>
      sometimes legitimate at senior roles, but a foreign-friendly employer will give you
      a written range before scheduling an interview. Always ask.</li>
  <li><strong>"Comprehensive overtime included" (固定残業代込み / 月20時間分の残業手当):</strong>
      A fixed overtime amount baked into the salary. If you exceed that hidden hour cap
      you should be paid for the excess, many black companies "forget" to do this. Always
      ask in writing how the fixed hours are calculated and what happens beyond them.</li>
  <li><strong>"Probation period" of 6+ months:</strong> legal max is typically 3–6 months;
      anything longer is a warning sign that they intend to fire freely.</li>
  <li><strong>Listings that have been posted for 6+ months continuously:</strong> the role
      is a revolving door. Cross-check with the company's hiring page archive.</li>
</ul>

<h2 id="interview-flags">Red flags during the interview</h2>
<ul>
  <li><strong>They can't articulate the team structure or your direct manager.</strong>
      Disorganised reporting lines often track with disorganised everything else.</li>
  <li><strong>They dodge questions about overtime.</strong> Standard answer at a healthy
      company: "We have a soft 40-hour week. Crunch happens occasionally and we pay for
      it." Black-company answer: "Our employees are passionate; everyone pitches in."</li>
  <li><strong>The interviewer arrives late, cancels last-minute, or no-shows.</strong>
      One time can be a fluke. Twice is a pattern.</li>
  <li><strong>They pressure you to decide same-day or next-day.</strong> Reasonable
      employers give you a week. Compressed timelines are how black companies prevent you
      from comparing offers or talking to people who'd warn you.</li>
  <li><strong>You meet only the founder and no team members.</strong> Especially at small
      companies, the team being shielded from candidates is a strong signal.</li>
  <li><strong>They ask intrusive personal questions.</strong> Marital status, fertility
      plans, family wealth, blood type, all illegal under the Equal Employment Opportunity
      Act but still happens at older Japanese firms. Walk.</li>
  <li><strong>Salary suddenly drops between verbal offer and written contract.</strong>
      Aggressive pattern, they bait with a high verbal number then trim 10–20% on paper.
      Never sign immediately; ask for 48 hours to review.</li>
</ul>

<h2 id="legal">What Japanese labour law actually requires (your protections)</h2>
<ul>
  <li><strong>Working hours:</strong> standard week is 40 hours, 8 hours/day. Anything
      beyond is overtime and must be paid at <strong>+25%</strong> for the first
      60 hours/month, <strong>+50%</strong> beyond that (since the 2023 amendment applied
      this to SMEs as well).</li>
  <li><strong>Overtime cap:</strong> 45 hours/month normal, with an absolute ceiling of
      100 hours/month or 720 hours/year under special agreement (the "36 agreement /
      36協定"). Exceeding these limits is criminal, not just civil.</li>
  <li><strong>Paid leave (有給休暇):</strong> minimum 10 days after 6 months of employment,
      rising with tenure. Since 2019, employers must <em>force</em> employees to take at
      least 5 days/year, refusing your paid leave is illegal.</li>
  <li><strong>Resignation notice:</strong> 14 days by law if you're on an indefinite
      contract. Any contract clause demanding more than 14 days' notice is
      <em>unenforceable</em>. You can leave; they can sue but won't win.</li>
  <li><strong>Wage payment:</strong> must be in cash (bank transfer counts) on time every
      month. Delayed or partial wages are immediate violations.</li>
  <li><strong>Service overtime (サービス残業 / sābisu zangyō):</strong> unpaid overtime is
      <em>illegal</em>. Records of hours worked are legally required and you can demand
      copies.</li>
</ul>
<div class="callout">
  If you're being denied your legal rights, the
  <a href="https://www.mhlw.go.jp/" target="_blank" rel="noopener">Labour Standards
  Inspection Office (労働基準監督署)</a> takes complaints from foreign workers in English
  and Japanese. Filing is free. Major cities also have multilingual labour consultation
  hotlines.
</div>

<h2 id="post-offer">Pre-signing checks, contract clauses to watch</h2>
<ul>
  <li><strong>Fixed overtime amount</strong> (固定残業代 / みなし残業), confirm in writing
      how many hours it covers and the per-hour rate beyond.</li>
  <li><strong>Salary breakdown:</strong> base + allowances should be itemised. A flat
      "monthly salary ¥X" with no breakdown often hides included overtime.</li>
  <li><strong>Probationary period (試用期間):</strong> 3–6 months is standard. Confirm
      the salary during probation matches the post-probation salary.</li>
  <li><strong>Non-compete clauses (競業避止義務):</strong> Japan's courts uphold these
      only if narrow in scope, time, and geography, and only if you're compensated. Broad
      "you can't work in this industry for 2 years anywhere in Japan" is unenforceable.</li>
  <li><strong>Mandatory transfer clause (転勤命令権):</strong> Older Japanese contracts
      include the right to move you to any office in the country. Foreign-friendly
      employers and modern startups usually drop this; check it's not buried in a clause
      labelled 勤務地 (work location).</li>
  <li><strong>"Resignation cooperation" clauses:</strong> any wording suggesting you must
      "obtain company consent" to resign is unenforceable but signals an employer that
      will try to make leaving difficult.</li>
</ul>

<h2 id="if-stuck">If you're already at a black company</h2>
<ol>
  <li><strong>Document everything.</strong> Keep a daily log of arrival and departure
      times. Screenshot Slack/Teams messages outside hours. These are evidence.</li>
  <li><strong>Pay into a separate savings account every month</strong>, having 6 months
      of runway means you can resign without immediate financial pressure.</li>
  <li><strong>Get medical attention if you're seeing physical symptoms.</strong> Stress-
      induced illness is a documented basis for emergency resignation and is sometimes
      treated as workplace injury.</li>
  <li><strong>Resign by registered mail (内容証明郵便).</strong> Sent to the company's
      official address with delivery confirmation. They cannot refuse it. The 14-day
      clock starts the day they receive it.</li>
  <li><strong>Talk to a labour lawyer if the company won't release your final paycheck,
      pension records, or 離職票 (resignation certificate).</strong> Initial consultation
      is often free.</li>
</ol>

<h2 id="foreign-specific">Risks specific to foreign workers</h2>
<ul>
  <li><strong>Visa pressure.</strong> Some black-company employers tell foreign workers
      "if you quit, you lose your visa." False, you have <strong>3 months</strong> to
      find a new sponsor after a job change before your visa is at risk, and you can apply
      for a "Designated Activities" job-search status to extend that. Quitting does not
      automatically cancel your visa.</li>
  <li><strong>"We hold your passport."</strong> This is a serious crime under Japanese
      law (involuntary servitude). If an employer suggests this, even informally, immediately contact your embassy.</li>
  <li><strong>Tied housing.</strong> Some employers offer company-provided housing tied
      to employment. Eviction with 1 week's notice is common when you resign. Plan an
      independent rental before you give notice.</li>
  <li><strong>"Cooperation pay" deductions.</strong> A few unethical employers deduct
      "training cost recovery" from your final paycheck if you quit before some date.
      This is illegal under Article 16 of the Labour Standards Act, which prohibits
      contracts that fix penalties for quitting.</li>
</ul>
<!-- ENRICH_V2:red-flags -->
<h2 id="hidden-flags">Hidden red flags in modern job posts</h2>
<p>The classic black-company signals (long hours, abusive bosses, withheld wages)
still apply, but the modern set of subtle red flags in job postings:</p>
<ul>
  <li><strong>"アットホームな職場" (family-like workplace).</strong> The most-reliable
      single red flag. Often translates to "no boundaries, expect to socialise after
      hours, weekend events".</li>
  <li><strong>"やりがい重視" (we value fulfilment).</strong> Code for "low pay, but
      meaningful work". Healthy employers offer both pay <em>and</em> meaning;
      employers who emphasise meaning over pay are signaling they can't compete on
      comp.</li>
  <li><strong>"若手活躍中" (young employees thriving).</strong> Often means high
      turnover, only young employees because mid-career ones have left.</li>
  <li><strong>"未経験歓迎" + senior salary on offer.</strong> Suspicious mismatch.
      Either the role is mis-described (it's actually low-skill) or the pay is
      contingent on impossible performance.</li>
  <li><strong>"完全週休二日制" not stated; only "週休二日制" stated.</strong>
      週休二日制 means "two days off in some weeks but not necessarily every week".
      Companies that mean "every weekend" specifically say 完全週休二日制. If they
      don't, expect to work some Saturdays.</li>
  <li><strong>"みなし残業" (overtime included in base) with no specified hours.</strong>
      みなし残業 ("deemed overtime") is legal but must specify the number of hours
      included. If the listing says "残業代込み" with no number, assume unlimited.</li>
  <li><strong>"裁量労働制" without specifics.</strong> Discretionary work systems
      are legal for specific job categories but commonly abused to avoid paying OT.</li>
  <li><strong>No salary range, only "応相談" (negotiable).</strong> Increasingly
      considered a red flag, employers who refuse to share salary ranges typically
      pay below market.</li>
  <li><strong>"自己啓発" (self-development) mentioned as a job duty.</strong> Often
      means "we expect you to attend training on weekends or after hours, unpaid".</li>
  <li><strong>Always-hiring on every platform.</strong> Same job listing posted
      continuously for 6+ months on Indeed, Wantedly, LinkedIn, GaijinPot, Daijob, means people keep quitting.</li>
</ul>

<h2 id="remote-flags">Remote-work and post-pandemic red flags</h2>
<ul>
  <li><strong>"Flexible / hybrid" but no clarity on how many days.</strong> Press for
      specifics. "Flexible" with no policy often means "manager's discretion" which
      becomes "5 days in office".</li>
  <li><strong>Surveillance software requirement.</strong> If they require Hubstaff,
      Time Doctor, ActivTrak, or screenshot-based monitoring, strong negative
      signal regardless of nominal flexibility.</li>
  <li><strong>"Always-on" expectations.</strong> Slack DM responses required within
      15 minutes? Saturday client calls? Both red flags even at high-pay roles.</li>
  <li><strong>No equipment stipend.</strong> A modern remote role at any reasonable
      employer covers laptop, monitor budget, internet allowance. Asking employees
      to expense back through reimbursement (or not at all) signals stinginess.</li>
  <li><strong>"Return-to-office" planned without notice.</strong> Ask explicitly:
      "What's the policy on RTO, and what's the change-notice period?" Mercari /
      PayPay / Rakuten have all had unannounced RTO changes, being aware is the
      protection.</li>
</ul>

<h2 id="forum-due-diligence">Forum due-diligence, Reddit, Glassdoor, OpenWork</h2>
<p>Before signing, run the company through these checks:</p>
<ul>
  <li><strong>Glassdoor</strong>, global; many Japan companies have ratings here.
      Look at the "Pros / Cons" patterns over multiple years.</li>
  <li><strong>OpenWork (旧Vorkers)</strong>, Japan-specific. Free with one review
      contribution. Long-form Japanese reviews; translate with a tool if necessary.
      Most accurate single source for Japanese-language workplace culture.</li>
  <li><strong>en-Lighthouse</strong>, En Japan's Japanese-language review platform;
      strong for traditional Japanese corporates.</li>
  <li><strong>Reddit r/japanlife</strong>, search the company name. Strong honest
      sentiment, especially for English-teaching and IT firms.</li>
  <li><strong>Reddit r/teachinginjapan</strong>, eikaiwa- and ALT-specific; search
      the company.</li>
  <li><strong>TokyoDev forum / Slack</strong>, search the company. Many tech
      employees post candid impressions.</li>
  <li><strong>LinkedIn, search current employees.</strong> Are most employees
      <2 years tenure? Are senior people leaving in clusters? These are tell-tale
      patterns.</li>
  <li><strong>Hello Work labor inspector records</strong>, if a company has had
      labor violations published, the prefectural labor bureau may list them.
      Less accessible but worth checking for serious cases.</li>
</ul>

<h2 id="contract-flags">Contract / offer-letter red flags</h2>
<p>When you receive an offer, the contract / 雇用契約書 should specify these clearly:</p>
<ul>
  <li><strong>Salary breakdown:</strong> base + bonus structure + any allowances.
      "Annual salary" alone is insufficient; ask for the breakdown.</li>
  <li><strong>Working hours:</strong> start, end, lunch break, OT policy.</li>
  <li><strong>Paid holidays:</strong> minimum 10 days in year 1 (legal minimum); 20
      days is standard at modern employers; "consume by year-end" rules should be
      stated.</li>
  <li><strong>Resignation notice:</strong> 30 days is legal default; some employers
      contractually require 60 or 90. Check.</li>
  <li><strong>Non-compete clauses:</strong> increasingly enforced in 2025–26.
      Standard restrictions: 6–12 months, named-competitor list, paid garden leave.
      Unpaid 2-year non-compete? Red flag.</li>
  <li><strong>Probation period:</strong> 3 months standard; some employers extend to
      6. Probation salary should match permanent salary, not be reduced.</li>
  <li><strong>Visa sponsorship</strong> should be explicit. The offer letter must
      state the employer commits to sponsoring the COE / visa application.</li>
  <li><strong>Bonus formula:</strong> "decided by company discretion" is normal but
      historic ranges should be honest. Ask: "What was the bonus paid to people in
      this role last year?"</li>
  <li><strong>Termination clauses:</strong> Japan provides strong worker protection.
      A clause allowing summary termination for "loss of company confidence" is
      legally weak but signals litigious employer culture.</li>
</ul>

<h2 id="escape-plan">If you're already in a black company, your exit plan</h2>
<p>The 6-step exit plan:</p>
<ol>
  <li><strong>Quiet preparation (Month 1–2).</strong> Update CV, rirekisho, English
      LinkedIn. Don't tell co-workers. Apply through personal email only.</li>
  <li><strong>Document everything (Month 1–3).</strong> Save copies of payslips, work
      schedules, overtime hours. If you have unpaid OT or harassment claims, these
      records are your evidence.</li>
  <li><strong>Apply broadly (Month 2–3).</strong> Mercari, PayPay, foreign-cap SaaS,
      Indeed Tokyo, FAANG Tokyo all hire continuously. Aim for 30+ applications.</li>
  <li><strong>Interview during PTO.</strong> Take paid leave for interview rounds, it's your legal right.</li>
  <li><strong>Get the offer in writing (Month 3–4).</strong> Wait until you have a
      signed offer before resigning. Don't accept verbal-only offers.</li>
  <li><strong>Resign formally (Month 4).</strong> Submit 退職届 (taishokutodoke,
      resignation letter) at least 30 days before exit date, by law that's all
      you owe. Use the formal phrase: <em>"一身上の都合により、〇月〇日をもって退職
      させていただきます."</em></li>
</ol>
<p>If you're being harassed, threatened, or owed back-wages: contact the
<strong>Labour Standards Inspection Office</strong> (労働基準監督署) at your
prefecture. Free, multilingual support is available at Tokyo Labour Bureau's
foreign-worker advice service (Mon–Fri, English / Chinese / Portuguese / Vietnamese
/ Tagalog). Backed by Article 5 of the Labour Standards Act, your employer cannot
retaliate for filing.</p>
<div class="callout">
  Sources for this section: alata.media black-company guide (Sep 2025),
  r/japanlife discussion threads on labour issues 2024–25, MHLW labor law summary.
</div>


<div class="callout">
  Looking for boards, recruiters, or language tools? See our
  <a href="/resources/external-resources">curated external-resources
  directory</a> for 60+ vetted sites with honest usage notes.
</div>
""",
    },

    # ------------------------------------------------------------------ this remained near previous (keep slot)
    {
    # EXTERNAL_RESOURCES_DIRECTORY:v1
        "slug": 'external-resources',
        "icon": 'link',
        "title": 'Curated external resources, job boards, agencies, blogs, learning tools',
        "summary": """A vetted directory of the external sites foreigners use to job-hunt and learn Japanese, with honest notes on when each is actually useful, who it's for, and which to skip.""",
        "updated": 'May 2026',
        "read_time": '8 min',
        "toc": [
            ('how-to-use', 'How to use this directory'),
            ('starter-guides', 'Starter career guides for foreigners'),
            ('english-boards', 'English-friendly job boards'),
            ('ja-boards', 'Japanese-language job boards'),
            ('recruiters-agencies', 'Recruiters & specialist agencies'),
            ('tech-specific', 'Tech-specific boards & communities'),
            ('teaching-specific', 'Teaching-specific boards'),
            ('finance-specific', 'Finance & professional services boards'),
            ('learning-japanese', 'Resources for learning Japanese'),
            ('communities-forums', 'Communities & forums'),
            ('salary-data', 'Salary data & benchmarking'),
            ('visa-immigration', 'Visa & immigration resources'),
            ('life-admin', 'Daily life, banking, housing, healthcare'),
            ('how-to-spot-quality', "How to evaluate a job-board listing's quality"),
        ],
        "body": """
<p>This directory pulls together the sites foreigners actually use to find work and
build a life in Japan. Each entry includes a brief note on what it's good for and
who it's wrong for, links without honest notes waste your time, so we've added
ours.</p>

<h2 id="how-to-use">How to use this directory</h2>
<p>The honest advice for a foreigner job-hunting in Japan:</p>
<ul>
  <li><strong>Apply through 3–5 channels in parallel.</strong> One job board is never
      enough. The successful foreigners we see use 1–2 English-friendly boards
      (TokyoDev, JapanDev for tech; Daijob for general), 1 Japanese-domestic board
      (BizReach, Doda) via a recruiter, and 1 direct-applications channel (Mercari,
      Indeed careers pages).</li>
  <li><strong>Use boards by signal-to-noise.</strong> TokyoDev and JapanDev are heavily
      curated and high quality for tech. GaijinPot has high volume but mixed quality.
      Indeed has the broadest coverage but you'll see many low-paying or stale
      postings.</li>
  <li><strong>Recruiters add value at senior levels.</strong> Robert Walters,
      Computer Futures, Pro-Recruitment, JAC Recruitment, en world, Hays, meaningful at ¥9M+ roles, less useful for entry-level.</li>
  <li><strong>Don't sign exclusive contracts.</strong> Some Japanese recruiters ask
      for exclusivity; politely refuse. Multiple recruiters = better outcomes.</li>
</ul>

<h2 id="starter-guides">Starter career guides for foreigners</h2>
<p>Long-form articles worth reading once before starting your job hunt:</p>
<ul>
  <li><a href="https://www.japanlivingguide.com/career/findjobs/jobsearch-japan/"
      target="_blank" rel="noopener noreferrer">Japan Living Guide, Job Search in
      Japan</a>. Lifestyle-oriented introduction to the job-hunt landscape; useful
      orientation for first-timers, especially on visa basics.</li>
  <li><a href="https://www.linkedin.com/pulse/how-get-job-japan-from-overseas-common-questions-i-am-edmund-ho-9lqjc/"
      target="_blank" rel="noopener noreferrer">How to Get a Job in Japan from Overseas, Edmund Ho (LinkedIn)</a>. Practical FAQ format on visa, applying from abroad,
      what to expect; written by an active recruiter.</li>
  <li><a href="https://medium.com/@mpbuquet/so-you-want-to-work-in-japan-ae4fe2de58fb"
      target="_blank" rel="noopener noreferrer">So You Want to Work in Japan
      (M.P. Buquet, Medium)</a>. Honest first-person account; addresses why the
      foreigner-friendly tech pocket of Japan is different from broader Japanese
      labour market.</li>
  <li><a href="https://www.relocate.world/en/destinations/japan/how-to-find-job-in-japan"
      target="_blank" rel="noopener noreferrer">Relocate.World, How to Find a Job
      in Japan</a>. Relocation-firm perspective; useful for visa, tax, and
      relocation-logistics overview.</li>
  <li><a href="https://japan-dev.com/blog/software-developer-salaries-in-japan-the-ultimate-guide"
      target="_blank" rel="noopener noreferrer">Japan Dev, Software Developer Salaries
      in Japan (Ultimate Guide)</a>. The most-frequently-updated single salary guide
      for foreign engineers; cross-references TokyoDev survey and company glassdoor
      data.</li>
  <li><a href="https://www.tokyodev.com/articles/software-developer-salaries-in-japan"
      target="_blank" rel="noopener noreferrer">TokyoDev, Software Developer Salaries
      in Japan</a>. Annual survey-based salary report; the highest-trust single
      source for foreign engineer comp in Japan.</li>
</ul>

<h2 id="english-boards">English-friendly job boards</h2>
<p>Boards where English-language listings are first-class citizens:</p>
<table>
  <thead><tr><th>Board</th><th>Best for</th><th>Honest note</th></tr></thead>
  <tbody>
    <tr>
      <td><a href="https://gaijinpot.com/" target="_blank" rel="noopener noreferrer">
          GaijinPot Jobs</a></td>
      <td>General foreign-hire roles, broad coverage</td>
      <td>High volume; quality varies. Skews toward eikaiwa, hospitality, ALT roles, tech is thin. Free.</td>
    </tr>
    <tr>
      <td><a href="https://japan-dev.com/" target="_blank" rel="noopener noreferrer">
          Japan Dev</a></td>
      <td>Software engineering, visa-sponsoring, English-OK</td>
      <td>Heavily curated; only foreigner-friendly tech companies. Smaller pool but
          near-zero noise. Free.</td>
    </tr>
    <tr>
      <td><a href="https://www.tokyodev.com/" target="_blank" rel="noopener noreferrer">
          TokyoDev</a></td>
      <td>Tech engineering jobs in Tokyo</td>
      <td>The single highest-quality tech board for foreigners. Smaller pool than
          JapanDev but companies are vetted. Free. Runs an annual developer survey
          worth reading.</td>
    </tr>
    <tr>
      <td><a href="https://linkedin.com/jobs" target="_blank" rel="noopener noreferrer">
          LinkedIn Jobs (Japan)</a></td>
      <td>Mid- to senior- level roles at foreign-cap companies</td>
      <td>Set country to Japan. Foreign-cap firms (FAANG, Stripe, Datadog, Notion)
          post here heavily. Premium account ($30/mo) noticeably improves
          recruiter-inbound flow.</td>
    </tr>
    <tr>
      <td><a href="https://www.daijob.com/en/" target="_blank" rel="noopener noreferrer">
          Daijob</a></td>
      <td>Bilingual professional roles, finance, consulting, marketing</td>
      <td>Reputable Japanese-domestic board with a strong bilingual focus. Better
          for ¥8M+ bilingual roles than entry-level.</td>
    </tr>
    <tr>
      <td><a href="https://www.careercross.com/en" target="_blank" rel="noopener noreferrer">
          CareerCross</a></td>
      <td>Bilingual professional roles, particularly finance and consulting</td>
      <td>One of the longest-running bilingual boards. Heavier on Japanese-headquartered
          and traditional foreign-cap (banks, consulting); lighter on modern tech.</td>
    </tr>
    <tr>
      <td><a href="https://www.yolo-japan.com/en/" target="_blank" rel="noopener noreferrer">
          YOLO Japan</a></td>
      <td>Part-time, entry-level, and hospitality roles for foreigners</td>
      <td>Good for short-term and gig roles. Lower quality for career-track
          professional jobs.</td>
    </tr>
    <tr>
      <td><a href="https://www.indeed.com/q-japan-jobs.html" target="_blank" rel="noopener noreferrer">
          Indeed Japan</a></td>
      <td>Volume, every role in Japan eventually appears here</td>
      <td>Use it for breadth, not first-pass quality. Indeed aggregates; many
          postings are stale or duplicated.</td>
    </tr>
    <tr>
      <td><a href="https://www.roberthalf.com/jp/en/jobs" target="_blank" rel="noopener noreferrer">
          Robert Half Japan</a></td>
      <td>Finance, accounting, tech, recruiter-mediated</td>
      <td>Specialist recruiter with strong bilingual finance / IT coverage. Best for
          ¥8M+ professional roles.</td>
    </tr>
    <tr>
      <td><a href="https://jobsinjapan.com/jobs/" target="_blank" rel="noopener noreferrer">
          Jobs in Japan</a></td>
      <td>English-teaching, eikaiwa, general foreign-friendly roles</td>
      <td>Wide ALT and eikaiwa coverage; also some general English-OK roles. Mid-tier
          quality.</td>
    </tr>
    <tr>
      <td><a href="https://www.skillhouse.co.jp/en" target="_blank" rel="noopener noreferrer">
          Skillhouse</a></td>
      <td>IT contract and contract-to-perm roles</td>
      <td>Long-standing English-friendly IT contractor placement. Specialty: bilingual
          devs and SREs at foreign-cap firms.</td>
    </tr>
  </tbody>
</table>

<h2 id="ja-boards">Japanese-language job boards</h2>
<p>If you have JLPT N2+ Japanese, these dramatically expand your access. Many are
domestic-only and have no English UI. Use a translator extension if needed.</p>
<table>
  <thead><tr><th>Board</th><th>Best for</th><th>Honest note</th></tr></thead>
  <tbody>
    <tr>
      <td><a href="https://doda.jp/" target="_blank" rel="noopener noreferrer">
          Doda</a></td>
      <td>Mid-career professionals, every sector</td>
      <td>One of Japan's largest job boards. Doubles as a recruiter platform: a Doda
          career advisor will be assigned after you register.</td>
    </tr>
    <tr>
      <td><a href="https://employment.en-japan.com/" target="_blank" rel="noopener noreferrer">
          en-japan / en転職</a></td>
      <td>Mid-career professionals, every sector</td>
      <td>Mass-market board for Japanese candidates. Some bilingual filtering exists
          but English UI is limited.</td>
    </tr>
    <tr>
      <td><a href="https://www.baitoru.com/lp/foreigner/en/" target="_blank" rel="noopener noreferrer">
          Baitoru (foreign-resident version)</a></td>
      <td>Part-time and hourly work, hospitality, retail, dining</td>
      <td>Pivoted recently with an English-language landing for foreign residents.
          Useful for student / dependent / spouse visa holders looking for hourly
          income.</td>
    </tr>
    <tr>
      <td><a href="https://arigato-work.com/en" target="_blank" rel="noopener noreferrer">
          Arigato Work</a></td>
      <td>SSW visa, blue-collar and specialised-skill workers</td>
      <td>Designed for Specified Skilled Worker visa holders. Coverage spans
          construction, agriculture, food service, manufacturing.</td>
    </tr>
    <tr>
      <td><a href="https://www.bizreach.jp/" target="_blank" rel="noopener noreferrer">
          BizReach</a></td>
      <td>Mid-to-senior professional roles, ¥7M+</td>
      <td>Recruiter platform with paid candidate subscription (¥5,500/month). Most
          serious Japanese-domestic recruiters source candidates here. Premium
          membership unlocks scout messages from C-suite-level roles.</td>
    </tr>
    <tr>
      <td><a href="https://www.geekly.co.jp/" target="_blank" rel="noopener noreferrer">
          Geekly</a></td>
      <td>IT and game-industry engineering</td>
      <td>Specialist IT recruiter for the Japanese-domestic tech market. Strong on
          Japanese gaming and IT consulting; weaker on foreign-cap firms.</td>
    </tr>
    <tr>
      <td><a href="https://wantedlyinc.com/ja/careers/jobs" target="_blank" rel="noopener noreferrer">
          Wantedly</a></td>
      <td>Tokyo startups and modern tech employers</td>
      <td>Story-driven posts with company culture front and centre; the de facto
          board for Tokyo startups. Set up a full bilingual profile to attract
          inbound.</td>
    </tr>
    <tr>
      <td><a href="https://www.robertwalters.co.jp/en/jobs.html" target="_blank" rel="noopener noreferrer">
          Robert Walters Japan</a></td>
      <td>Bilingual professional placements, finance, marketing, sales, legal</td>
      <td>The leading specialist bilingual recruiter in Japan. Strong network with
          foreign-cap firms; publishes the most-quoted annual salary survey.</td>
    </tr>
    <tr>
      <td><a href="https://nextinjapan.com/" target="_blank" rel="noopener noreferrer">
          Next in Japan</a></td>
      <td>SSW-visa hospitality, food, manufacturing, care</td>
      <td>Specialist board for Specified Skilled Worker positions. Good search filters
          by visa category.</td>
    </tr>
    <tr>
      <td><a href="https://ag.global.mynavi.jp/en/top_en/" target="_blank" rel="noopener noreferrer">
          Mynavi Global</a></td>
      <td>Bilingual mid-career roles across sectors</td>
      <td>Mynavi's global-talent recruiter arm. Strong bilingual coverage especially
          at Japanese conglomerates and traditional industrial firms.</td>
    </tr>
    <tr>
      <td><a href="https://townwork.net/" target="_blank" rel="noopener noreferrer">
          TownWork</a></td>
      <td>Local / hourly / part-time across Japan</td>
      <td>Recruit Holdings' mass-market local-job board. Useful for spouse / dependent
          visa holders looking for part-time near home. Japanese only.</td>
    </tr>
    <tr>
      <td><a href="https://corp.en-japan.com/en/services/desc_enAgent.html" target="_blank" rel="noopener noreferrer">
          en agent</a></td>
      <td>Mid-career bilingual roles via en-japan group</td>
      <td>The recruiter-side of en-japan. Solid bilingual coverage in IT, finance,
          and engineering.</td>
    </tr>
    <tr>
      <td><a href="https://www.skillhouse.co.jp/" target="_blank" rel="noopener noreferrer">
          Skillhouse (Japanese-language)</a></td>
      <td>IT contract / permanent placements</td>
      <td>Same firm as the English Skillhouse listing above; the Japanese-language
          site has broader coverage.</td>
    </tr>
  </tbody>
</table>

<h2 id="recruiters-agencies">Recruiters &amp; specialist agencies</h2>
<p>Specialist recruiters worth registering with at senior levels (¥9M+):</p>
<ul>
  <li><strong>Robert Walters Japan</strong>, bilingual professional, finance,
      consulting, marketing, legal. The most prolific senior placer.</li>
  <li><strong>Michael Page Japan</strong>, finance, legal, marketing, sales,
      property. Strong at ¥10M+.</li>
  <li><strong>Hays Japan</strong>, finance, accounting, IT, legal. Mid-market focus.</li>
  <li><strong>Robert Half Japan</strong>, finance and accounting specialty; also
      tech.</li>
  <li><strong>en world Japan</strong>, bilingual mid-to-senior; broad sector
      coverage.</li>
  <li><strong>JAC Recruitment</strong>, Japan's largest domestic bilingual recruiter.
      Strong at Japanese-headquartered firms.</li>
  <li><strong>Pro-Recruitment Group (Pasona Tech, RGF, Pro-Recruitment Network)</strong>, bilingual professional placements.</li>
  <li><strong>Computer Futures / SThree Japan</strong>, IT contractors and
      permanent.</li>
  <li><strong>Morgan McKinley Japan</strong>, finance specialist.</li>
  <li><strong>Spring Professional (Adecco group)</strong>, bilingual professional
      across sectors.</li>
  <li><strong>JAC International</strong>, premium executive search.</li>
  <li><strong>Wahl &amp; Case</strong>, tech specialist; senior IC and management
      placements.</li>
  <li><strong>Tokyo Connect</strong>, boutique tech / startup recruiter.</li>
</ul>

<h2 id="tech-specific">Tech-specific boards &amp; communities</h2>
<ul>
  <li><a href="https://www.tokyodev.com/" target="_blank" rel="noopener noreferrer">
      TokyoDev</a>, already mentioned. Pair the board with the
      <a href="https://www.tokyodev.com/articles" target="_blank" rel="noopener noreferrer">
      TokyoDev articles</a> and the
      <a href="https://www.tokyodev.com/community" target="_blank" rel="noopener noreferrer">
      TokyoDev Slack community</a>, the latter is the best foreign-engineer
      community in Japan.</li>
  <li><a href="https://japan-dev.com/" target="_blank" rel="noopener noreferrer">
      JapanDev</a>, already mentioned; pair with the company-detail pages.</li>
  <li><a href="https://nikkei.itmedia.co.jp/" target="_blank" rel="noopener noreferrer">
      ITmedia Engineer</a>, Japanese-language tech career news.</li>
  <li><a href="https://qiita.com/jobs" target="_blank" rel="noopener noreferrer">
      Qiita Jobs</a>, engineer-community job board; Japanese-language but vetted
      tech roles.</li>
  <li><a href="https://findy-code.io/" target="_blank" rel="noopener noreferrer">
      Findy</a>, Japanese tech recruiter using GitHub activity for matching.
      Useful if your GitHub is active.</li>
  <li><a href="https://forkwell.com/" target="_blank" rel="noopener noreferrer">
      Forkwell</a>, Japanese-language engineering board with a strong startup
      pipeline.</li>
  <li><a href="https://www.green-japan.com/" target="_blank" rel="noopener noreferrer">
      Green</a>, Japanese-language IT job board; mid-market employer focus.</li>
  <li><a href="https://www.lapras.com/" target="_blank" rel="noopener noreferrer">
      Lapras</a>, Japanese-language engineering platform; useful if you have
      Japanese GitHub / Qiita visibility.</li>
</ul>

<h2 id="teaching-specific">Teaching-specific boards</h2>
<ul>
  <li><a href="https://jetprogramme.org/" target="_blank" rel="noopener noreferrer">
      JET Programme</a>, the official Japanese Exchange and Teaching programme.
      Annual application October–November.</li>
  <li><a href="https://www.ohayosensei.com/" target="_blank" rel="noopener noreferrer">
      O-Hayo Sensei</a>, a long-running aggregator of English-teaching listings;
      free, biweekly newsletter.</li>
  <li><a href="https://jobsinjapan.com/teaching-jobs/" target="_blank" rel="noopener noreferrer">
      Jobs in Japan, Teaching</a>, broad ALT, eikaiwa, university coverage.</li>
  <li><a href="https://www.searchassociates.com/" target="_blank" rel="noopener noreferrer">
      Search Associates</a>, international school recruitment fair (credentialed
      teachers).</li>
  <li><a href="https://www.iss.edu/" target="_blank" rel="noopener noreferrer">
      ISS, International Schools Services</a>, another international school
      recruitment fair operator.</li>
  <li><a href="https://www.thecouncil.com/" target="_blank" rel="noopener noreferrer">
      The Council of International Schools (CIS)</a>, placement for credentialed
      teachers.</li>
  <li><a href="https://www.jrec-in.jst.go.jp/" target="_blank" rel="noopener noreferrer">
      JREC-IN</a>, Japan Research Career Information Network. Official university
      and research-position board; English UI available.</li>
</ul>

<h2 id="finance-specific">Finance &amp; professional services boards</h2>
<ul>
  <li><strong>eFinancialCareers Japan</strong>, finance specialist board.</li>
  <li><strong>Robert Walters Japan</strong> (also listed above).</li>
  <li><strong>Michael Page Japan</strong> (also listed above).</li>
  <li><strong>Direct application via firm careers pages</strong>: Goldman Sachs
      Japan, Morgan Stanley MUFG, JPMorgan Securities Japan, BofA Securities Japan,
      Citi Japan, UBS Japan, Deutsche Bank Tokyo, Barclays Japan, Nomura, Daiwa,
      Mizuho Securities, MUFG Securities, SMBC Nikko, each runs its own graduate
      and lateral hiring.</li>
  <li><strong>Big Four Japan careers pages</strong>: KPMG AZSA, Deloitte Touche
      Tohmatsu, EY ShinNihon, PwC Aarata.</li>
  <li><strong>Consulting firm careers</strong>: McKinsey Tokyo, BCG Tokyo, Bain
      Tokyo, Accenture Japan, Deloitte Consulting, EY Strategy &amp; Transactions,
      ZS Associates, ADL.</li>
</ul>

<h2 id="learning-japanese">Resources for learning Japanese</h2>
<table>
  <thead><tr><th>Tool</th><th>Best for</th><th>Honest note</th></tr></thead>
  <tbody>
    <tr>
      <td><a href="https://www.tokiniandy.com/" target="_blank" rel="noopener noreferrer">
          Tokini Andy</a></td>
      <td>Beginner → intermediate; structured video learning</td>
      <td>Free Genki I/II walkthrough plus paid premium courses. Andy's pace and
          warmth are ideal for self-learners.</td>
    </tr>
    <tr>
      <td><a href="https://www.wanikani.com/" target="_blank" rel="noopener noreferrer">
          WaniKani</a></td>
      <td>Kanji + vocab via SRS</td>
      <td>The single highest-leverage tool for kanji. ¥10,000/year or lifetime
          ¥30,000. Plan for 18–24 months to reach the equivalent of N3 kanji.</td>
    </tr>
    <tr>
      <td><a href="https://www.tofugu.com/learn-japanese/" target="_blank" rel="noopener noreferrer">
          Tofugu</a></td>
      <td>Article-style learning; grammar deep-dives</td>
      <td>Sister site to WaniKani. Best free single source for Japanese-grammar
          explainers in English.</td>
    </tr>
    <tr>
      <td><a href="https://bunpro.jp/" target="_blank" rel="noopener noreferrer">
          Bunpro</a></td>
      <td>Grammar SRS, N5 → N1</td>
      <td>The best paid (¥6,000/yr) grammar SRS tool. Pairs perfectly with WaniKani.</td>
    </tr>
    <tr>
      <td><a href="https://www.reddit.com/r/LearnJapanese/" target="_blank" rel="noopener noreferrer">
          r/LearnJapanese</a></td>
      <td>Community, recommendations, motivation</td>
      <td>Active subreddit; weekly question thread is the easiest entry point to ask
          for advice.</td>
    </tr>
    <tr>
      <td><a href="https://www.jlpt.jp/e/" target="_blank" rel="noopener noreferrer">
          JLPT Official Site</a></td>
      <td>Test registration, levels, dates</td>
      <td>Twice-yearly test; registration windows close 3 months ahead. Confirm
          local test centre.</td>
    </tr>
    <tr>
      <td><a href="https://www.italki.com/" target="_blank" rel="noopener noreferrer">
          iTalki</a></td>
      <td>1-on-1 Japanese tutors</td>
      <td>$10–25/hr for community tutors; $25–40/hr for professional teachers. The
          single best leverage for conversation fluency.</td>
    </tr>
    <tr>
      <td><a href="https://anki.app/" target="_blank" rel="noopener noreferrer">
          Anki</a></td>
      <td>Custom SRS vocab decks</td>
      <td>Free desktop and Android; iOS app is paid. Most foreign learners pair Tango
          N5–N1 decks with Anki for 10,000-word coverage by N1.</td>
    </tr>
    <tr>
      <td><a href="https://www3.nhk.or.jp/news/easy/" target="_blank" rel="noopener noreferrer">
          NHK Easy News</a></td>
      <td>Reading practice at N3–N2 level</td>
      <td>Free; daily news in furigana-annotated easier Japanese.</td>
    </tr>
    <tr>
      <td><a href="https://jisho.org/" target="_blank" rel="noopener noreferrer">
          Jisho</a></td>
      <td>Online Japanese dictionary</td>
      <td>Free; cross-referenced kanji + vocab. The standard look-up tool.</td>
    </tr>
    <tr>
      <td><a href="https://en.wikipedia.org/wiki/Shin_Kanzen_Master" target="_blank" rel="noopener noreferrer">
          Shin Kanzen Master series</a></td>
      <td>JLPT exam prep, N5 to N1</td>
      <td>The gold-standard Japanese-language JLPT prep textbooks. Buy at Kinokuniya
          or via Amazon.</td>
    </tr>
    <tr>
      <td><a href="https://en.wikipedia.org/wiki/Sō_Matome_(textbook_series)" target="_blank" rel="noopener noreferrer">
          So Matome series</a></td>
      <td>JLPT prep, gentler than Shin Kanzen Master</td>
      <td>The "lighter" version of Shin Kanzen. Better for first attempts; pair with
          Shin Kanzen for the retake.</td>
    </tr>
  </tbody>
</table>

<h2 id="communities-forums">Communities &amp; forums</h2>
<ul>
  <li><strong>r/japanlife</strong>, most-active English-language Japan
      living/working subreddit. Search before posting.</li>
  <li><strong>r/cscareerquestionsJP</strong>, tech career questions specific to
      Japan.</li>
  <li><strong>r/teachinginjapan</strong>, ALT, eikaiwa, university teaching
      reviews and questions.</li>
  <li><strong>r/movingtojapan</strong>, visa, relocation, and first-year
      questions.</li>
  <li><strong>r/LearnJapanese</strong>, language-learning community.</li>
  <li><strong>TokyoDev Slack</strong>, foreign engineer community.</li>
  <li><strong>Tokyo Indies / GDG Tokyo / PyCon Japan / JaSST Tokyo</strong>, Tokyo-based developer meetups; in-person + Slack.</li>
  <li><strong>InterNations Tokyo</strong>, broad international community, monthly
      mixers.</li>
  <li><strong>Tokyo Mesh</strong>, founder/operator community.</li>
  <li><strong>JapanFinance Discord / r/JapanFinance</strong>, tax, investing,
      mortgages, NISA in Japan.</li>
</ul>

<h2 id="salary-data">Salary data &amp; benchmarking</h2>
<ul>
  <li><strong>TokyoDev annual developer survey</strong>, the most-trusted single
      source for foreign engineer comp in Japan.</li>
  <li><strong>Robert Walters Japan Salary Survey</strong>, comprehensive annual
      report across 11 sectors, 589 roles. Free PDF after registration.</li>
  <li><strong>Hays Salary Guide Japan</strong>, annual benchmark across sectors.</li>
  <li><strong>JapanDev salary guide</strong>, frequently-updated rolling guide;
      cross-references survey and company data.</li>
  <li><strong>Levels.fyi</strong>, for FAANG Tokyo specifically (Google Japan,
      Amazon Japan, Microsoft Japan offered comp). User-submitted.</li>
  <li><strong>Glassdoor Japan</strong>, broad; quality varies by company.</li>
  <li><strong>OpenWork (旧Vorkers)</strong>, Japan-specific Glassdoor equivalent;
      Japanese-language but highly accurate workplace reviews.</li>
</ul>

<h2 id="visa-immigration">Visa &amp; immigration resources</h2>
<ul>
  <li><strong>Immigration Services Agency of Japan</strong>
      (<a href="https://www.moj.go.jp/isa/" target="_blank" rel="noopener noreferrer">
      official site</a>), visa categories, application forms, processing times.</li>
  <li><strong>MOFA (Ministry of Foreign Affairs)</strong>
      (<a href="https://www.mofa.go.jp/" target="_blank" rel="noopener noreferrer">
      mofa.go.jp</a>), visa application info, especially HSP and J-Find.</li>
  <li><strong>JNTO J-Find programme info</strong>, 2-year job-hunt visa for top
      global university graduates.</li>
  <li><strong>FRESC (Foreign Residents' Support Center, Roppongi)</strong>, multilingual visa, labour, and life-support consultations.</li>
  <li><strong>Wevisa.io</strong>, private platform for HSP point calculation and
      tracking.</li>
  <li><strong>r/JapanResidency</strong>, community with detailed status-change and
      PR application discussion.</li>
</ul>

<h2 id="life-admin">Daily life, banking, housing, healthcare</h2>
<ul>
  <li><strong>SBI Shinsei Bank</strong>, foreigner-friendly bilingual online banking.</li>
  <li><strong>SMBC Trust (PRESTIA)</strong>, full-service bilingual bank with
      multi-currency accounts.</li>
  <li><strong>Rakuten Bank / Sony Bank</strong>, online-first; foreign-friendly
      account opening.</li>
  <li><strong>Wise</strong>, international transfers at low cost.</li>
  <li><strong>GaijinPot Housing / Sakura House / Oakhouse</strong>, foreigner-friendly rental listings.</li>
  <li><strong>Tokyo Medical and Surgical Clinic, Tokyo Midtown Clinic, King
      Clinic</strong>, English-language medical services (Tokyo).</li>
  <li><strong>Japan Healthcare Info</strong>, bilingual medical translation
      service.</li>
  <li><strong>Pasonal (旧Pasona Career)</strong>, career and life-admin advisory
      for foreigners.</li>
</ul>

<h2 id="how-to-spot-quality">How to evaluate a job-board listing's quality</h2>
<p>Before applying to any listing, run it through these checks:</p>
<ol>
  <li><strong>Salary range disclosed?</strong> Listings without a stated range or
      with only "応相談" (negotiable) are 30–50% more likely to underpay than listings
      with explicit ranges.</li>
  <li><strong>Visa sponsorship explicit?</strong> The phrase "visa sponsorship
      available" should appear in writing. Vague language like "depending on
      candidate" often means no.</li>
  <li><strong>"Always hiring" pattern.</strong> Search the job title + company
      name on Indeed and LinkedIn. If the same role has been live for 6+ months,
      assume high turnover.</li>
  <li><strong>Company Glassdoor / OpenWork rating.</strong> Under 3.0 average is a
      strong warning. Read the cons sections, not the pros.</li>
  <li><strong>Recent funding announcements (for startups).</strong> Lapras /
      ForStartups / TechCrunch Japan publish funding events. A startup hiring 18
      months after their last funding round on a vague salary is a risk.</li>
  <li><strong>Foreign employees on LinkedIn.</strong> Search "company name" plus
      country names. Companies with foreign employees who've stayed 3+ years are
      almost always safe; ones with no current foreigners or very short tenures are
      uncertain.</li>
  <li><strong>Cross-check with our</strong> <a href="/companies">companies registry
      </a>, the firms profiled there have been pre-vetted for visa sponsorship and
      foreigner-friendliness.</li>
</ol>

<div class="callout">
  Missing a resource? Send us a note via the <a href="/community">community page</a>.
  We update this directory quarterly.
</div>
""",
    },
]


# ---------------------------------------------------------------------------
# City + role guides, focused destination pages.
# ---------------------------------------------------------------------------

GUIDES: list[dict] = [

    # ------------------------------------------------------------------ Tokyo
    {
        "slug": "tokyo",
        "category": "City",
        "icon": "building",
        "title": "Tokyo, the foreign professional's guide",
        "summary": "Where the foreigner-friendly jobs are, which wards to live in, real 2025 rent numbers, transit network, and the practical stuff (banks, phones, hanko) that you'll deal with in week one.",
        "updated": "May 2026",
        "read_time": "10 min",
        "toc": [
            ("why-tokyo", "Why Tokyo concentrates foreign roles"),
            ("job-clusters", "Where the jobs cluster, by ward"),
            ("neighborhoods", "Where foreigners actually live"),
            ("salary-vs-rent", "Salary vs. rent, what's affordable"),
            ("transit", "Transit basics"),
            ("week-one", "Week-one practical checklist"),
            ("communities", "Foreign communities in Tokyo"),
            ("new-hiring-districts", 'New hiring districts, Azabudai, Toranomon Hills'),
            ("commute-reality", 'Commute reality and the BRT effect'),
            ("foreign-services-2026", 'Foreigner-friendly services, banks, doctors, dentists'),
            ("childcare-schools", 'Childcare and schools, practical 2026'),
            ("nightlife-social", 'Nightlife and social life for foreign professionals'),
            ("safety-emergencies", 'Safety, emergencies, and the practical safety net'),
        ],
        "body": """
<h2 id="why-tokyo">Why Tokyo concentrates foreign roles</h2>
<p>Roughly 70% of foreigner-friendly job postings in Japan are in Tokyo's 23 wards. Three
forces drive this concentration:</p>
<ul>
  <li><strong>Headquarters density.</strong> Almost every major Japanese corporation
      and every foreign company entering Japan opens its HQ in Tokyo. Mercari, SmartNews,
      LINE Yahoo Japan, PayPay, Rakuten, Cyberagent, all Tokyo. Foreign offices for Google,
      Amazon, Microsoft, Meta, Stripe, Indeed, Salesforce, all Tokyo.</li>
  <li><strong>Foreign community.</strong> About 600,000 foreign residents in Tokyo as of
      2025, far more than any other Japanese city. Bilingual services (banking, real
      estate, healthcare) cluster here.</li>
  <li><strong>Network effects.</strong> Recruiters, accelerators, conference circuits,
      and meetups concentrate where the talent is. Job-hopping is easier when there are
      40 alternatives in the same metro than three across the country.</li>
</ul>

<h2 id="job-clusters">Where the jobs cluster, by ward</h2>
<table>
  <thead><tr><th>Ward / area</th><th>Dominant industries</th><th>Anchor employers</th></tr></thead>
  <tbody>
    <tr><td>Roppongi / Akasaka (Minato)</td>
        <td>Finance, consulting, foreign-cap tech</td>
        <td>Goldman Sachs, McKinsey, Google, Indeed Tokyo (Roppongi Hills)</td></tr>
    <tr><td>Shibuya</td>
        <td>Tech, consumer internet, design, startups</td>
        <td>Mercari, GMO, Cyberagent, DeNA, Stripe Tokyo</td></tr>
    <tr><td>Ebisu / Daikanyama (Shibuya ward)</td>
        <td>Design-led tech, media, fashion</td>
        <td>SmartNews (recently moved), creative agencies</td></tr>
    <tr><td>Marunouchi / Otemachi (Chiyoda)</td>
        <td>Banking, insurance, large enterprise</td>
        <td>Mitsubishi UFJ, Mizuho, Mitsui & Co., Marubeni</td></tr>
    <tr><td>Shinjuku</td>
        <td>Mixed, gaming, traditional Japanese giants, some tech</td>
        <td>Square Enix area, Mitsui Fudosan, Tokyo Tobu</td></tr>
    <tr><td>Shinagawa / Konan</td>
        <td>Pharma, manufacturing JP HQs, logistics</td>
        <td>Microsoft Japan, Sony HQ, Canon</td></tr>
    <tr><td>Toranomon / Kamiyacho (Minato)</td>
        <td>Newer corporate HQ towers, hospitality</td>
        <td>Toranomon Hills tenants, foreign-cap firms</td></tr>
    <tr><td>Nihonbashi (Chuo)</td>
        <td>Pharma, established Japanese corporates</td>
        <td>Pfizer Japan, Bristol-Myers, Nomura</td></tr>
  </tbody>
</table>

<h2 id="neighborhoods">Where foreigners actually live</h2>
<p>The neighbourhoods most foreign professionals pick balance three things: commute time,
English-friendliness of local services, and rent. The pattern by life stage:</p>
<h3>Single, mid-career professionals (most common)</h3>
<ul>
  <li><strong>Setagaya, Sangenjaya, Shimokitazawa, Yoga, Komazawa-Daigaku:</strong>
      30–40 minutes from work, 1LDK ¥180–230K, family-friendly, low-key. Sangenjaya is
      3 minutes from Shibuya on the Den-en-toshi line at 30–40% lower rent than equivalent
      space in Shibuya itself. Setagaya is the single most popular ward for foreigners.</li>
  <li><strong>Meguro / Nakameguro / Naka-Meguro:</strong> trendy, walkable cherry-blossom
      neighbourhoods. Slightly pricier (¥200–270K for 1LDK) but commute is excellent.</li>
  <li><strong>Suginami, Asagaya, Koenji:</strong> quieter, more Japanese, ¥140–190K
      1LDK. JR Chuo line takes you to Shinjuku in 10 minutes.</li>
  <li><strong>Nakano:</strong> 5 minutes from Shinjuku, ¥140–180K 1LDK. Less hip than
      Setagaya, very functional.</li>
</ul>
<h3>Families with kids</h3>
<ul>
  <li><strong>Setagaya, Yoga, Sakurashinmachi, Futako-Tamagawa:</strong> family-magnet
      neighbourhoods. Multiple international schools nearby (American School in Japan
      Chofu campus, K International, Tokyo International).</li>
  <li><strong>Minato / Hiroo:</strong> closest to embassies and Tokyo's main international
      community. International school district. Rents start at ¥350K for 2LDK and rise
      sharply.</li>
  <li><strong>Yokohama, especially Minato Mirai and Motomachi:</strong> 30–50 minutes
      from central Tokyo, much larger apartments, strong international-school options
      (Yokohama International School), 60–70% of central-Tokyo rent.</li>
</ul>
<h3>Embassies, executives, $$$</h3>
<ul>
  <li><strong>Hiroo / Azabu-Juban / Azabu-Dai (Minato):</strong> embassy belt. 1LDK starts
      ¥250K, 2LDK ¥400–600K, 3LDK ¥700K+.</li>
  <li><strong>Akasaka, Aoyama:</strong> closer to corporate HQ, slightly more accessible
      pricing than Hiroo.</li>
</ul>

<h2 id="salary-vs-rent">Salary vs. rent, what's actually affordable</h2>
<p>The standard rule in Japan is rent should be 25–30% of net (post-tax) income.
Translated into gross salary, the practical pairings:</p>
<table>
  <thead><tr><th>Gross income (¥/yr)</th><th>Net (¥/mo)</th><th>Affordable rent</th><th>Realistic neighbourhoods</th></tr></thead>
  <tbody>
    <tr><td>4M</td><td>¥255K</td><td>¥65–80K</td><td>Nerima, Itabashi, Saitama border</td></tr>
    <tr><td>6M</td><td>¥385K</td><td>¥95–115K</td><td>Setagaya 1K, Suginami, Nakano</td></tr>
    <tr><td>8M</td><td>¥500K</td><td>¥125–150K</td><td>Setagaya 1LDK, Meguro</td></tr>
    <tr><td>12M</td><td>¥720K</td><td>¥180–215K</td><td>Shibuya, Naka-Meguro, central Setagaya</td></tr>
    <tr><td>18M</td><td>¥1.05M</td><td>¥260–315K</td><td>Hiroo, Roppongi, Aoyama</td></tr>
  </tbody>
</table>
<div class="callout">
  Run your actual gross-to-net with the <a href="/tools/take-home-pay">take-home pay
  calculator</a>, Japan's tax stack varies by age, dependants, and year of residence.
</div>

<h2 id="transit">Transit basics</h2>
<ul>
  <li><strong>JR Yamanote line</strong> is the central loop, 29 stations, runs every 2–4
      minutes. Memorise it; it's the spine of central Tokyo.</li>
  <li><strong>Tokyo Metro and Toei Subway</strong> together cover everywhere the Yamanote
      doesn't. Top transit apps: Yahoo! Norikae, Google Maps (very good), Navitime.</li>
  <li><strong>Commuter pass (定期券):</strong> your employer reimburses the cost between
      home and work. Apply for it within your first 1–2 weeks.</li>
  <li><strong>IC card</strong> (Suica or PASMO) for everything else. Now natively supported
      on iPhone (Apple Pay) and most Android phones.</li>
  <li><strong>Don't bother with a car.</strong> Parking is ¥30–60K/mo on top of car costs;
      transit gets you everywhere faster.</li>
</ul>

<h2 id="week-one">Week-one practical checklist</h2>
<ol>
  <li><strong>Pick up your residence card</strong> at the airport on arrival (Narita,
      Haneda, Kansai, and some others issue it on the spot; smaller airports mail it).</li>
  <li><strong>Buy a Suica/PASMO IC card</strong> at the airport before you leave, transit is on-demand from day one.</li>
  <li><strong>Set up an MVNO phone plan</strong> (povo, IIJmio, mineo, or Sakura Mobile
      for English-speaking onboarding). You need a Japanese phone number for the rest of
      the steps.</li>
  <li><strong>Register your address at the ward office within 14 days.</strong> Legally
      required. Brings address to your residence card and triggers National Health
      Insurance if you're not yet employed.</li>
  <li><strong>Open a bank account.</strong> Foreigner-friendly: Shinsei (English UI),
      Sony Bank, JP Post Bank (universally accepted), SBI Sumishin (online).</li>
  <li><strong>Order a hanko (印鑑)</strong> if not already done. ¥3–10K online; you'll
      need it for the apartment lease and any government paperwork.</li>
</ol>
<div class="callout">
  Full step-by-step in the <a href="/pillars/first-90-days">First 90 Days in Japan</a>
  pillar guide, every form, every line, in order.
</div>

<h2 id="communities">Foreign communities in Tokyo</h2>
<ul>
  <li><strong>Tokyo Dev Slack</strong>, 5,000+ English-speaking software engineers.
      Highest-signal tech community in Tokyo.</li>
  <li><strong>JapanDev community</strong>, newer, engineering-focused, salary
      transparency culture.</li>
  <li><strong>Tokyo Tech Mafia</strong>, invite-only senior engineers and leaders.</li>
  <li><strong>r/Tokyo, r/japanlife</strong>, broad foreigner-in-Japan general questions,
      apartment hunting, paperwork.</li>
  <li><strong>InterNations Tokyo</strong>, professional events, expat-heavy.</li>
  <li><strong>Tokyo American Club, Foreign Correspondents' Club of Japan</strong>, higher-end professional networks; paid membership.</li>
  <li><strong>Embassy-based clubs</strong> (Tokyo British Club, Tokyo French Lyceum
      alumni, etc.), community by national origin.</li>
</ul>
<!-- ENRICH_V2:tokyo -->
<h2 id="new-hiring-districts">New hiring districts, Azabudai, Toranomon Hills</h2>
<p>Tokyo's hiring geography has shifted noticeably since 2023. The largest new
concentrations of foreigner-friendly jobs:</p>
<ul>
  <li><strong>Azabudai Hills (opened Nov 2023)</strong>, Mori Building's 330m
      mixed-use complex. Tenants include several foreign-cap financial services
      firms, premium consulting offices, and TeamLab's permanent installation drives
      visitor footfall. Bilingual hospitality and creative-industry roles concentrate
      here.</li>
  <li><strong>Toranomon Hills Station Tower (opened Oct 2023)</strong>, directly
      connected to Toranomon Hills station on the Hibiya line. Tenants include
      several international firms relocating from older Otemachi buildings.</li>
  <li><strong>Shibuya Sakura Stage (2024)</strong>, Tokyu's newest Shibuya tower
      complex, just south of Shibuya station. Houses Tokyu Group HQ, several
      startups, and global tech firm satellite offices.</li>
  <li><strong>Yaesu / Tokyo Midtown Yaesu (2023)</strong>, adjacent to Tokyo Station,
      attracting consulting (Bain Yaesu) and financial firms.</li>
  <li><strong>Otemachi One Tower (2023)</strong>, banking and asset management,
      Mitsubishi/MUFG anchor.</li>
</ul>
<p>The older Roppongi Hills / Akasaka cluster remains the largest foreign-firm
concentration, but Azabudai is competing aggressively for new tenants.</p>

<h2 id="commute-reality">Commute reality and the BRT effect</h2>
<p>Tokyo's public transit is the city's defining asset. Practical reality:</p>
<ul>
  <li><strong>Average foreign professional commute:</strong> 40–55 min door-to-door.
      Living within 30 min of work is a luxury; living within 60 min is normal.</li>
  <li><strong>Rush hour crowding:</strong> the Saikyo Line, Tozai Line, Den-en-toshi
      Line, and Yamanote Line peak at 140–180% capacity 7:30–8:30am. The Tozai Line
      between Toyo-cho and Otemachi is historically the worst in Tokyo.</li>
  <li><strong>The Tokyo BRT (Bus Rapid Transit) since 2022</strong> connects Shimbashi
      / Toranomon to Toyosu / Harumi / Olympic Village area. Useful if you live in
      Tsukishima or Toyosu and work in Toranomon, bypasses Shimbashi crush.</li>
  <li><strong>JR Joban Line / Senju area</strong> is rapidly gentrifying, Kitasenju
      now offers 30-minute Otemachi commute at 50% Setagaya rent.</li>
  <li><strong>Yamanote Line halving</strong>, the new Takanawa Gateway station (since
      2020) provides easier southern Tokyo access. Shinagawa area workers now have
      meaningfully shorter walks.</li>
  <li><strong>Hybrid work patterns</strong>, most foreigner-friendly tech firms run
      2–3 days/week in office. Living a bit further out is more tolerable than it
      was pre-pandemic.</li>
</ul>

<h2 id="foreign-services-2026">Foreigner-friendly services, banks, doctors, dentists</h2>
<h3>Banks with English-language support</h3>
<ul>
  <li><strong>SMBC Trust Bank (PRESTIA)</strong>, English-speaking branches in
      Aoyama, Hiroo, Roppongi, Yokohama. Foreign-friendly account opening; multi-
      currency accounts available.</li>
  <li><strong>Shinsei Bank (now SBI Shinsei)</strong>, bilingual online and ATM
      experience; foreigner-friendly history.</li>
  <li><strong>Sony Bank</strong>, online-first; English interface; popular with
      tech foreigners.</li>
  <li><strong>Rakuten Bank</strong>, fully online; English ATM cards; ¥0 fee
      transfers to other Rakuten accounts.</li>
  <li><strong>MUFG / SMBC / Mizuho main banks</strong>, Japanese-only branches but
      bilingual support at Tokyo flagship branches; useful for large account
      relationships.</li>
  <li><strong>Wise (formerly TransferWise)</strong>, for international transfers;
      foreigners commonly maintain a Wise account alongside a Japanese bank.</li>
</ul>
<h3>English-speaking medical clinics</h3>
<ul>
  <li><strong>Tokyo Medical and Surgical Clinic (Roppongi)</strong>, long-established
      foreigner-focused clinic, English-speaking GPs.</li>
  <li><strong>Tokyo Midtown Clinic (Roppongi)</strong>, English support, premium
      facilities.</li>
  <li><strong>King Clinic (Hiroo, Roppongi)</strong>, bilingual GP, paediatrics.</li>
  <li><strong>Sakura Clinic / Tokyo British Clinic</strong>, Hiroo; British-staffed.</li>
  <li><strong>National Center Hospital Otemachi clinic</strong>, emergency English
      support available.</li>
  <li><strong>St. Luke's International Hospital (Tsukiji)</strong>, major hospital
      with strong English-language services.</li>
</ul>
<h3>English-friendly dentists</h3>
<ul>
  <li>Park Side Dental Clinic (Roppongi), Smile and Cure (Aoyama),
      Tokyo Yamanote Dental (Shibuya), Royal Dental Office (Roppongi).</li>
</ul>

<h2 id="childcare-schools">Childcare and schools, practical 2026</h2>
<ul>
  <li><strong>Hoikuen (保育園, public daycare):</strong> heavily subsidised
      (¥0–¥80K/month depending on income). Wait lists are still real in central wards
      (Minato, Chuo, Shibuya); Setagaya has eased substantially. Apply 6–12 months
      ahead of intended start.</li>
  <li><strong>Yochien (幼稚園, public kindergarten):</strong> ages 3–5; half-day
      programmes; mostly Japanese-language. Free under government policy.</li>
  <li><strong>International preschools:</strong> Tokyo International School,
      Sunshine International, Aoba-Japan, GOA, Komazawa Park International School.
      Tuition ¥1.5–3M/year.</li>
  <li><strong>K–12 international schools:</strong> ASIJ (¥3.5M/year), British School
      Tokyo (¥3M), Tokyo International School (¥2.8M), Aoba-Japan Bilingual,
      Yokohama International, K. International School, Seisen International Girls,
      Saint Maur Yokohama.</li>
  <li><strong>Bilingual / international tracks within Japanese schools:</strong>
      Setagaya International School (Japanese-language curriculum with English
      support), some Chuo and Minato municipal elementary schools have foreign-
      support classrooms.</li>
  <li><strong>After-school care:</strong> gakudo (学童) is heavily subsidised in
      public schools; private alternatives include Kids Duo (English immersion), Be
      Studio, and Kumon.</li>
</ul>

<h2 id="nightlife-social">Nightlife and social life for foreign professionals</h2>
<ul>
  <li><strong>Tokyo Tech Meetups</strong>, Tokyo Indies, Tokyo iOS Meetup, GDG
      Tokyo, Tokyo PyCon, JaSST Tokyo. Hosted at GMO Yours, Cybozu, Mercari,
      Cookpad.</li>
  <li><strong>Tokyo Dev community</strong>, Slack workspace + meetups; the largest
      and most active foreign-engineer community in Japan.</li>
  <li><strong>InterNations Tokyo</strong>, monthly mixers; broad international
      crowd.</li>
  <li><strong>Tokyo Mesh</strong>, startup-founder and operator community; private
      events.</li>
  <li><strong>SIDE Tokyo / The Hive</strong>, co-working with substantial foreign
      member base.</li>
  <li><strong>Tokyo Stylish Foreigners (Facebook) / Tokyo Cheapo (newsletter)</strong>, broad social listings.</li>
  <li><strong>Sports clubs:</strong> Tokyo Run Club, Wesley Football Club (rugby),
      Tokyo International Football Club. Most are bilingual / English-OK.</li>
  <li><strong>Language exchange:</strong> Mixxer Tokyo, Tokyo Language Exchange
      Cafe, Meetup.com Japanese-English groups. Free to ¥1,000/event.</li>
  <li><strong>Specific neighbourhoods for nightlife:</strong> Roppongi (international
      bars), Ebisu / Daikanyama (sophisticated, mid-range), Shimokitazawa (indie,
      music, smaller bars), Shibuya / Shinjuku Golden Gai (traditional izakaya).</li>
</ul>

<h2 id="safety-emergencies">Safety, emergencies, and the practical safety net</h2>
<ul>
  <li><strong>Emergency numbers:</strong> 110 (police), 119 (fire / ambulance), 118
      (maritime). All accept basic English; if you need detailed translation, the
      operator can connect you to a translation service within minutes.</li>
  <li><strong>NHK World disaster radio</strong>, for earthquakes, tsunamis,
      typhoons. Available on smartphones via the NHK World app.</li>
  <li><strong>Earthquake kit:</strong> 3 days of water, food, medication, flashlight,
      battery pack. Most central-Tokyo apartments have stairwell emergency lockers.</li>
  <li><strong>Japan Helpline (toll-free)</strong>, 0570-000-911. 24/7 English
      crisis support.</li>
  <li><strong>Tokyo English Lifeline (TELL)</strong>, 03-5774-0992. Mental health,
      crisis, counselling in English.</li>
  <li><strong>Foreign-resident hotline (FRESC, Roppongi)</strong>, Immigration +
      labour issues for foreigners. Multilingual.</li>
  <li><strong>Earthquake insurance</strong> is sold separately from fire insurance
      (rentals include fire by default). Earthquake premium is ¥1,500–3,000/year
      for typical 1LDK contents.</li>
</ul>

""",
    },

    # ------------------------------------------------------------------ Osaka
    {
        "slug": "osaka",
        "category": "City",
        "icon": "building",
        "title": "Osaka, Japan's second city for foreign professionals",
        "summary": "Osaka pays roughly 85% of Tokyo for the same role but costs 60–70% as much. Where the jobs are, which wards to live in, and what the post-Expo 2025 hiring market looks like.",
        "updated": "May 2026",
        "read_time": "8 min",
        "toc": [
            ("why-osaka", "Why Osaka, the trade-offs vs. Tokyo"),
            ("industries", "Industries and employers in Kansai"),
            ("neighborhoods", "Where to live"),
            ("salary", "Salary realities"),
            ("post-expo", "Post-Expo 2025 hiring market"),
            ("culture", "Cultural differences vs. Tokyo"),
            ("kansai-tech-2026", "Kansai tech scene 2026, what's actually growing"),
            ("osaka-vs-tokyo", 'Osaka vs Tokyo, the real trade-offs'),
            ("osaka-companies-deep", 'Companies hiring foreigners, by sector'),
            ("osaka-comp", 'Osaka compensation, vs Tokyo'),
            ("osaka-life", 'Daily life, Osaka peculiarities'),
            ("osaka-expo-2025", 'Post-Expo 2025 dynamics'),
        ],
        "body": """
<h2 id="why-osaka">Why Osaka, the trade-offs vs. Tokyo</h2>
<p>Osaka is Japan's third-largest city (after Tokyo and Yokohama), the commercial heart
of the Kansai region, and home to roughly 270,000 foreign residents as of 2024. For
foreign professionals weighing it against Tokyo, three things matter:</p>
<ul>
  <li><strong>Cost of living is ~60–70% of Tokyo.</strong> A 1LDK that runs ¥230K in
      central Shibuya is ¥85–120K in central Osaka. A typical professional lifestyle
      costs roughly ¥250K/mo modest, ¥400K/mo comfortable, about 25–35% less than Tokyo
      equivalents.</li>
  <li><strong>Salaries are roughly 85% of Tokyo</strong> for the same role at the same
      seniority. A Tokyo engineer at ¥10M would typically be offered ¥8–9M for the same
      job in Osaka. The cost-of-living math still favours Osaka net.</li>
  <li><strong>Fewer English-language roles, more Japanese-required roles.</strong> The
      Kansai economy is more manufacturing- and traditional-business-heavy, with smaller
      tech and gaishikei concentrations. English-only postings are 20–30% of what they
      are in Tokyo.</li>
</ul>

<h2 id="industries">Industries and employers in Kansai</h2>
<p>Manufacturing dominates the Kansai economy. Automotive, pharmaceutical, chemical,
heavy machinery, and food production are all concentrated here, with hospitality and
retail forming the next layer.</p>
<table>
  <thead><tr><th>Industry</th><th>Major employers</th></tr></thead>
  <tbody>
    <tr><td>Pharma / life sciences</td>
        <td>Takeda (HQ Osaka), Sumitomo Pharma, Otsuka Pharmaceutical, Shionogi</td></tr>
    <tr><td>Electronics / manufacturing</td>
        <td>Panasonic (HQ Osaka), Sharp, Daikin, Kyocera (Kyoto), Murata (Kyoto), Omron (Kyoto)</td></tr>
    <tr><td>Automotive / mobility</td>
        <td>Suzuki (Hamamatsu, adjacent), Hino, Yamaha (Hamamatsu)</td></tr>
    <tr><td>Trading / banking</td>
        <td>Sumitomo Corporation, Itochu, Sumitomo Mitsui Banking (SMBC)</td></tr>
    <tr><td>Retail / consumer goods</td>
        <td>Asics, Mizuno, Nidec, Glico, House Foods</td></tr>
    <tr><td>Tech / digital (smaller cluster)</td>
        <td>Capcom (Osaka), Hatena, Cybozu Osaka office, some Rakuten Osaka presence</td></tr>
  </tbody>
</table>

<h2 id="neighborhoods">Where to live</h2>
<table>
  <thead><tr><th>Area</th><th>1LDK rent</th><th>Foreigner appeal</th></tr></thead>
  <tbody>
    <tr><td>Umeda / Kita-ku (central business district)</td>
        <td>¥130–200K</td>
        <td>Walking to Umeda offices; trade-off is small apartments</td></tr>
    <tr><td>Honmachi (corporate centre)</td>
        <td>¥120–180K</td>
        <td>Mid-size Japanese corporate proximity</td></tr>
    <tr><td>Tennoji / Abeno</td>
        <td>¥80–130K</td>
        <td>Family-friendly, 15 min to Umeda; many international families</td></tr>
    <tr><td>Esaka / Senri-chuo (Suita / Toyonaka)</td>
        <td>¥75–110K</td>
        <td>Foreigner heart of Kansai, Osaka International School in Senri</td></tr>
    <tr><td>Namba / Minami</td>
        <td>¥85–130K</td>
        <td>Nightlife and retail; younger crowd</td></tr>
    <tr><td>Toyonaka / Ikeda</td>
        <td>¥70–100K</td>
        <td>Quiet residential; near Osaka International Airport (domestic)</td></tr>
    <tr><td>Kobe (across prefecture line, 30 min)</td>
        <td>¥90–150K</td>
        <td>Sea views, port-city character; historic foreign settlement</td></tr>
  </tbody>
</table>

<h2 id="salary">Salary realities</h2>
<p>For the same role and seniority, expect roughly 85% of Tokyo bands. Some practical
examples for 2026:</p>
<ul>
  <li>Mid software engineer at a Japanese manufacturer: ¥6–9M (vs. ¥7–10M in Tokyo).</li>
  <li>Senior engineer at a tech company with Kansai presence: ¥9–13M (vs. ¥10–16M in Tokyo).</li>
  <li>Mid PM at a Japanese manufacturer: ¥7–10M.</li>
  <li>Senior data scientist (pharma): ¥9–13M.</li>
  <li>Marketing director at a Kansai consumer brand: ¥12–18M.</li>
</ul>
<p>Compare any specific offer with the <a href="/insights/salary">salary insights
dashboard</a>, Robert Walters Japan 2026 data has separate East/West Japan splits for
most role families.</p>

<h2 id="post-expo">Post-Expo 2025 hiring market</h2>
<p>The Osaka-Kansai Expo, which ran April–October 2025, drove a hiring spike in
hospitality, tourism, retail, and event-related services. Approximately 20,000 temporary
workers entered the market when the Expo wrapped, which has softened hiring across those
categories through early 2026.</p>
<p>However, certain segments saw lasting structural demand from the Expo's infrastructure
build:</p>
<ul>
  <li><strong>Data centre engineering</strong>, Osaka and the wider Kansai region became
      a secondary data-centre cluster on the back of Expo-related cloud build-outs.
      Demand for facility, mechanical, and network engineers stays strong into 2027.</li>
  <li><strong>English-speaking hospitality leadership</strong>, luxury hotel chains
      (Four Seasons, Conrad, Waldorf-Astoria) entered Osaka around the Expo and are
      hiring bilingual managers at premium rates.</li>
  <li><strong>Construction project management</strong>, the post-Expo redevelopment of
      Yumeshima island and the IR (integrated resort) planned to open 2030 are pulling
      bilingual PM talent.</li>
</ul>

<h2 id="culture">Cultural differences vs. Tokyo</h2>
<ul>
  <li><strong>Osaka is famously friendlier to outsiders.</strong> The local language
      (Kansai-ben) is warmer, social distance is shorter, small-talk is normal. Many
      foreigners report finding it easier to integrate socially.</li>
  <li><strong>Working hours are slightly shorter on average.</strong> Manufacturing-heavy
      economy means fixed shifts, less of the Tokyo white-collar overtime culture.</li>
  <li><strong>Less English in daily life.</strong> Restaurant menus, ward office staff,
      and even bank branches have noticeably less English support than Tokyo. Plan to
      learn basic Japanese faster than you would in Tokyo.</li>
  <li><strong>U-turn candidates (returning Kansai natives) are a growing trend.</strong>
      Many companies are widening their geographic reach to attract Tokyo-trained
      professionals who want to return to Kansai for family or lifestyle reasons.</li>
</ul>
<!-- ENRICH_V2:osaka -->
<h2 id="kansai-tech-2026">Kansai tech scene 2026, what's actually growing</h2>
<p>Kansai (Osaka–Kyoto–Kobe metro area, ~19M people) is a substantial economy but a
small tech hub relative to Tokyo. The honest 2026 picture:</p>
<ul>
  <li><strong>Sakura Internet</strong>, Osaka HQ; ramping AI-infrastructure
      hiring after winning a 2024 government AI compute contract. The biggest single
      foreigner-friendly tech employer in Kansai.</li>
  <li><strong>Nintendo (Kyoto)</strong>, global powerhouse but historically very
      Japanese-only. Some international-team roles open in 2024–25 (mostly senior).</li>
  <li><strong>Capcom (Osaka)</strong>, game development; bilingual roles in
      programming and art.</li>
  <li><strong>Panasonic Holdings (Osaka HQ)</strong>, large industrial company.
      Bilingual roles concentrated in cross-border B2B, AI/IoT divisions.</li>
  <li><strong>Sharp (Osaka)</strong>, under Foxconn ownership; some global team
      English-language roles.</li>
  <li><strong>Murata Manufacturing (Kyoto)</strong>, components manufacturer; some
      English-language R&amp;D and corporate-development roles.</li>
  <li><strong>Daikin Industries (Osaka)</strong>, air-conditioning global leader;
      international team for North America, Europe, India business.</li>
  <li><strong>Rakuten Mobile / Securities (Kobe + Osaka)</strong>, large Rakuten
      satellite operations; English-friendly engineering at the Mobile arm.</li>
  <li><strong>Sansan (Kobe)</strong>, has Kobe office; B2B SaaS.</li>
</ul>

<h2 id="osaka-vs-tokyo">Osaka vs Tokyo, the real trade-offs</h2>
<table>
  <thead><tr><th>Dimension</th><th>Tokyo advantage</th><th>Osaka advantage</th></tr></thead>
  <tbody>
    <tr><td>Job pool size</td><td>~10× more foreigner-friendly roles</td><td>–</td></tr>
    <tr><td>Pay level</td><td>5–15% premium across roles</td><td>–</td></tr>
    <tr><td>Rent</td><td>–</td><td>30–45% cheaper for equivalent neighbourhood</td></tr>
    <tr><td>Food cost</td><td>–</td><td>15–20% cheaper eating out</td></tr>
    <tr><td>Foreign community</td><td>600K+ residents, broad infrastructure</td>
        <td>~50–60K residents, smaller but tight-knit</td></tr>
    <tr><td>Local culture</td><td>Cosmopolitan, less personality</td>
        <td>Strong regional identity, friendlier, more humour</td></tr>
    <tr><td>International schools</td><td>20+ choices</td><td>4–5 choices</td></tr>
    <tr><td>Healthcare in English</td><td>Many specialised options</td>
        <td>A few central hospitals; otherwise Japanese-only</td></tr>
    <tr><td>Transit</td><td>Most extensive network globally</td>
        <td>Smaller, simpler, easier to navigate</td></tr>
    <tr><td>Career transitions</td><td>Far easier, 40+ employer alternatives within
        a 30-min commute</td>
        <td>5–10 employer alternatives; smaller pool means slower job moves</td></tr>
  </tbody>
</table>
<p>The honest summary: Osaka works well for foreign professionals who (a) want lower
cost of living, (b) have a remote-first or Osaka-anchored role, (c) appreciate the
Kansai social scene, and (d) don't anticipate needing frequent employer changes.
For foreigners actively career-changing, Tokyo's job density usually wins.</p>

<h2 id="osaka-companies-deep">Companies hiring foreigners, by sector</h2>
<h3>Technology / IT</h3>
<ul>
  <li>Sakura Internet (Osaka HQ, AI compute, hosting)</li>
  <li>NTT West (Osaka HQ, telco)</li>
  <li>Rakuten Mobile (Kobe operations)</li>
  <li>Yahoo Osaka (LINE Yahoo's Kansai engineering office)</li>
  <li>Cybozu Osaka (smaller satellite office)</li>
  <li>OMRON (Kyoto, automation, healthcare)</li>
</ul>
<h3>Manufacturing / industrial</h3>
<ul>
  <li>Panasonic (Osaka, energy, B2B, AI)</li>
  <li>Sharp (Osaka, displays, IoT)</li>
  <li>Daikin Industries (Osaka, HVAC global)</li>
  <li>Murata Manufacturing (Kyoto, electronic components)</li>
  <li>Komatsu Construction Equipment (Osaka divisions)</li>
  <li>Kawasaki Heavy Industries (Kobe, aerospace, ships)</li>
  <li>Kubota Corporation (Osaka, agricultural equipment)</li>
</ul>
<h3>Gaming / entertainment</h3>
<ul>
  <li>Nintendo (Kyoto)</li>
  <li>Capcom (Osaka)</li>
  <li>Universal Studios Japan (Osaka, operations + creative)</li>
</ul>
<h3>Pharma / biotech</h3>
<ul>
  <li>Takeda Pharmaceutical (Osaka HQ, global pharma)</li>
  <li>Shionogi (Osaka, pharma R&amp;D)</li>
  <li>Sumitomo Pharma (Osaka)</li>
</ul>
<h3>Trading / logistics</h3>
<ul>
  <li>Itochu Shoji (Osaka office)</li>
  <li>Sumitomo Corporation (Osaka office)</li>
  <li>Nippon Express (Osaka logistics hub)</li>
</ul>

<h2 id="osaka-comp">Osaka compensation, vs Tokyo</h2>
<p>Real 2026 ranges, with Tokyo equivalents for comparison:</p>
<table>
  <thead><tr><th>Role</th><th>Osaka</th><th>Tokyo</th><th>Delta</th></tr></thead>
  <tbody>
    <tr><td>Junior software engineer</td><td>¥4.2M–¥5.5M</td><td>¥5M–¥8M</td><td>−15%</td></tr>
    <tr><td>Mid software engineer</td><td>¥6.5M–¥9M</td><td>¥8M–¥13M</td><td>−15%</td></tr>
    <tr><td>Senior software engineer</td><td>¥10M–¥14M</td><td>¥12M–¥20M</td><td>−15%</td></tr>
    <tr><td>Sales / BD manager</td><td>¥7M–¥10M</td><td>¥9M–¥13M</td><td>−15%</td></tr>
    <tr><td>Marketing manager</td><td>¥6M–¥9M</td><td>¥7M–¥11M</td><td>−10%</td></tr>
    <tr><td>Pharma R&amp;D scientist</td><td>¥8M–¥14M</td><td>¥9M–¥15M</td><td>−5%</td></tr>
    <tr><td>Finance / controllership</td><td>¥7M–¥11M</td><td>¥8M–¥14M</td><td>−10%</td></tr>
    <tr><td>Eikaiwa teacher</td><td>¥2.8M–¥3.8M</td><td>¥2.8M–¥3.8M</td><td>=</td></tr>
    <tr><td>JET ALT</td><td>¥4M (national rate)</td><td>¥4M (national rate)</td><td>=</td></tr>
  </tbody>
</table>
<p>Net of cost-of-living, Osaka often comes out ahead. A ¥9M senior engineer in
Osaka with ¥110K rent has more net disposable than a ¥12M senior in Tokyo with
¥220K rent.</p>

<h2 id="osaka-life">Daily life, Osaka peculiarities</h2>
<ul>
  <li><strong>Kansai-ben (関西弁)</strong> is the regional dialect. Standard Tokyo
      Japanese is universally understood, but you'll pick up Osaka-specific phrases
      (おおきに for thanks, あかん for no good, ほんま for really).</li>
  <li><strong>Food culture is Osaka's largest export.</strong> Eating out is cheaper
      and arguably better. Takoyaki, okonomiyaki, kushikatsu are local specialties.
      Dotonbori is the tourist epicentre; locals eat in Tenma, Tenjinbashi, Namba.</li>
  <li><strong>Public-transit etiquette</strong> differs slightly. The "stand on the
      right" escalator rule (opposite of Tokyo's "stand on the left") is famously
      Osaka-specific.</li>
  <li><strong>Foreigner-friendly neighbourhoods:</strong>
      <ul>
        <li>Umeda / Tenma / Nakatsu, central business; mixed foreign / Japanese.</li>
        <li>Namba / Shinsaibashi, entertainment district; busy.</li>
        <li>Tennoji / Abeno, quieter, family-friendly.</li>
        <li>Honmachi / Yodoyabashi, business district.</li>
        <li>Kyobashi, middle-class residential.</li>
      </ul></li>
  <li><strong>International community hubs:</strong> Osaka Tech Meetup, Kansai DevDay
      (annual), Hacker Dojo Osaka, Osaka International House.</li>
  <li><strong>Distance to Tokyo:</strong> Tokaido Shinkansen, 2h22m. Companies with
      Tokyo and Osaka offices often have a "monthly Tokyo visit" expectation built
      into Osaka roles.</li>
</ul>

<h2 id="osaka-expo-2025">Post-Expo 2025 dynamics</h2>
<p>The Osaka Kansai Expo 2025 (April–October 2025) drove a wave of infrastructure
investment in Osaka, particularly around Yumeshima island. Post-Expo, the legacy:</p>
<ul>
  <li><strong>Yumeshima integrated resort (IR) and casino</strong> on track to open
      ~2030; meaningful hospitality and operations hiring through late 2020s.</li>
  <li><strong>Improved transit:</strong> Osaka Metro Chuo line extension to Yumeshima;
      Yumeshima Sakurazima ferry; faster Itami / Kansai airport connections.</li>
  <li><strong>Foreign business influx:</strong> several global firms opened or
      expanded Osaka satellite offices during the Expo period (consulting, hospitality,
      luxury retail). Some of these have stuck.</li>
  <li><strong>Tourism numbers</strong> remain elevated post-Expo; cross-border
      hospitality / English-speaking service roles are growing.</li>
</ul>

""",
    },

    # ------------------------------------------------------------------ Software engineering
    {
        "slug": "software-engineering",
        "category": "Role",
        "icon": "cpu",
        "title": "Software engineering in Japan, the deep dive",
        "summary": "The highest-paying foreigner-friendly track in Japan. Who's hiring, what stacks pay best, real 2026 comp bands from the TokyoDev survey, and the practical realities of the engineering scene.",
        "updated": "May 2026",
        "read_time": "11 min",
        "toc": [
            ("market", "The 2026 market"),
            ("companies", "Companies actively hiring foreigners"),
            ("comp", "Compensation, real 2026 numbers"),
            ("stacks", "Stacks that actually pay"),
            ("levels", "Levels and progression"),
            ("interview", "Interview process"),
            ("remote", "Remote / hybrid reality"),
            ("getting-in", "Getting in from overseas"),
            ("tokyodev-2026", 'TokyoDev 2025–26 survey deep dive'),
            ("ai-infra-boom", 'AI infrastructure hiring boom'),
            ("nikkei-engineer", "Nikkei vs gaishikei, the engineer's choice"),
            ("interview-prep-deep", 'Interview prep, concrete resources'),
            ("after-2-years", 'What changes after 2 years in Tokyo'),
            ("contractor-track", 'Contractor / freelance / consulting tracks'),
        ],
        "body": """
<h2 id="market">The 2026 market</h2>
<p>Software engineering is the most foreigner-friendly career track in Japan, by a wide
margin. The 2025 TokyoDev developer survey of 989 international engineers found:</p>
<ul>
  <li>Median engineer compensation: <strong>¥9.5M</strong>, up ¥1M from 2024.</li>
  <li>57% of respondents had a compensation increase in the last year; only 6% had a decrease.</li>
  <li>60% of respondents hold an engineer-track or HSP-track residence status, meaning
      their work permit is tied directly to a tech job.</li>
  <li>Hybrid work overtook fully-flexible remote work: 43% hybrid (up from 37%), 32%
      free-choice remote (down from 38%).</li>
</ul>
<p>The market is in a strong year, bilingual engineers are getting 15–25% raises on job
changes, and the FAANG Tokyo offices have aggressively scaled hiring through 2025–26.</p>

<h2 id="companies">Companies actively hiring foreigners</h2>
<h3>Tier 1, actively hire abroad, sponsor visas, no Japanese required</h3>
<table>
  <thead><tr><th>Company</th><th>Engineering size</th><th>Notable</th></tr></thead>
  <tbody>
    <tr><td>Mercari</td><td>~1,200</td>
        <td>Bilingual engineering org; English documentation by default; signing bonuses ¥1–3M for senior hires</td></tr>
    <tr><td>SmartNews</td><td>~250</td>
        <td>Mostly English engineering; news distribution + LLM applications</td></tr>
    <tr><td>PayPay</td><td>~700</td>
        <td>Payments at scale; English-first eng documentation; 50%+ non-Japanese engineering</td></tr>
    <tr><td>LINE Yahoo Japan</td><td>~5,000</td>
        <td>Many English-speaking teams; pay tiers vary by team</td></tr>
    <tr><td>Indeed Tokyo</td><td>~700</td>
        <td>Roughly 80%+ non-Japanese engineering; sister office to Indeed US</td></tr>
    <tr><td>Rakuten</td><td>~6,000</td>
        <td>Officially English-as-corporate-language since 2010; mixed in practice</td></tr>
    <tr><td>Cybozu</td><td>~700</td>
        <td>Bilingual; B2B SaaS; lower base pay but excellent work-life balance reputation</td></tr>
    <tr><td>Studist</td><td>~80</td>
        <td>Bilingual mid-stage startup; B2B procedure-management product</td></tr>
    <tr><td>Autify</td><td>~80</td>
        <td>Bilingual founder team; test automation</td></tr>
  </tbody>
</table>
<h3>Tier 1.5, FAANG and big-tech Tokyo offices</h3>
<ul>
  <li>Google Japan (Roppongi Hills), ¥18–35M+ total comp at senior levels with RSUs.</li>
  <li>Amazon Japan (Meguro), slightly lower base than Google but aggressive sign-ons.</li>
  <li>Microsoft Japan (Shinagawa), Azure focus; very international team.</li>
  <li>Meta Japan, Stripe Tokyo, Apple Japan, smaller Tokyo engineering teams but
      premium comp.</li>
</ul>
<h3>Tier 2, Japanese companies with English-friendly engineering teams</h3>
<ul>
  <li>Cyberagent (large game and advertising tech), N3+ preferred.</li>
  <li>DeNA (gaming + healthcare tech), bilingual teams in specific divisions.</li>
  <li>GMO Group (commerce infrastructure), historic gaijin-friendly culture.</li>
  <li>Sakura Internet (hosting + AI infrastructure), Osaka-based.</li>
  <li>Sakana AI (Tokyo-based AI lab founded 2023), high-end research engineering, English OK.</li>
  <li>Preferred Networks (PFN, deep learning), research labs are very international.</li>
</ul>

<h2 id="comp">Compensation, real 2026 numbers</h2>
<table>
  <thead>
    <tr><th>Level</th><th>Years</th><th>Median TC (¥M/yr)</th><th>Top of band (¥M/yr)</th></tr>
  </thead>
  <tbody>
    <tr><td>Junior</td><td>0–2</td><td>5.5</td><td>8 (FAANG)</td></tr>
    <tr><td>Mid</td><td>2–5</td><td>8.5</td><td>13 (FAANG)</td></tr>
    <tr><td>Senior</td><td>5–9</td><td>12</td><td>20 (FAANG)</td></tr>
    <tr><td>Staff / Tech Lead</td><td>9+</td><td>17</td><td>30 (FAANG)</td></tr>
    <tr><td>Principal / Distinguished</td><td>12+</td><td>22</td><td>35–50 (FAANG)</td></tr>
  </tbody>
</table>
<p>The TokyoDev 2025 survey found respondents at companies <em>without</em> a Japan entity
(i.e. fully remote international employer) and those at foreign companies <em>with</em>
a Japan entity (FAANG Tokyo) both clustered at ¥13.5M median, meaningfully above the
¥8.5M median at Japanese-headquartered employers.</p>

<h2 id="stacks">Stacks that actually pay</h2>
<p>The premium-paying stacks at foreigner-friendly Japanese companies in 2026:</p>
<ul>
  <li><strong>Go</strong>, Mercari, SmartNews, PayPay all run on Go for core services.</li>
  <li><strong>TypeScript + Next.js</strong>, universal frontend stack at most modern
      Japanese tech companies.</li>
  <li><strong>Kotlin / Java</strong>, banking, fintech, established Japanese corporates.</li>
  <li><strong>Python (Django / FastAPI)</strong>, data, ML, internal tooling.</li>
  <li><strong>Swift / Kotlin</strong> for mobile, high demand at consumer-internet
      players.</li>
</ul>
<p>Niche but high-paying:</p>
<ul>
  <li><strong>Rust</strong>, small but growing pool; some payments and infrastructure
      teams use it.</li>
  <li><strong>Cloud security + DevOps</strong>, bilingual SREs see 15–30% job-change
      raises in 2026.</li>
  <li><strong>AI/ML productionisation</strong>, taking off the back of LLM adoption;
      premium tier at Sakana AI, PFN, FAANG.</li>
</ul>
<p>Almost universally, AWS is the cloud of choice (with GCP a distinct second). Azure is
rare outside enterprise/banking. Knowing AWS deeply is a meaningful comp lever.</p>

<h2 id="levels">Levels and progression</h2>
<p>Most foreigner-friendly companies use a US-style levelling system rather than the
traditional Japanese seniority-based promotion ladder. Roughly:</p>
<ul>
  <li><strong>L3 / Junior / Associate Engineer (0–2 yrs):</strong> ship small features
      with mentorship.</li>
  <li><strong>L4 / Mid Engineer (2–5 yrs):</strong> own features end-to-end; some
      cross-team coordination.</li>
  <li><strong>L5 / Senior Engineer (5–9 yrs):</strong> drive multi-engineer projects;
      design subsystems; mentor.</li>
  <li><strong>L6 / Staff / Tech Lead (9+):</strong> set technical direction across teams;
      partner with product/design at director level.</li>
  <li><strong>L7+ / Principal:</strong> rare; typically named technical-authority on a
      domain across the org.</li>
</ul>
<p>Promotion velocity at gaishikei is fast (2–3 years per level on average). At Japanese
companies, even the modern ones, expect 3–4 years.</p>

<h2 id="interview">Interview process</h2>
<p>At foreigner-friendly Japanese tech companies (Mercari, SmartNews, PayPay), the typical
loop:</p>
<ol>
  <li><strong>Recruiter screen</strong> (30 min), English or Japanese, depending on team.
      Confirms basic fit, salary expectations, visa status.</li>
  <li><strong>Technical screen</strong> (60–90 min), live coding or take-home. Often
      using HackerRank, Coderpad, or a custom problem. English OK.</li>
  <li><strong>System design</strong> (45–60 min), for L5+. Whiteboard or virtual
      whiteboard. English.</li>
  <li><strong>Team / behavioural</strong> (45–60 min × 2–3 rounds), meet your prospective
      manager and 1–2 teammates. Some Japanese small-talk; technical conversation in
      English.</li>
  <li><strong>Bar-raiser / final</strong> (30–60 min), senior engineer outside the team.
      Often the last hire/no-hire vote.</li>
</ol>
<p>Total elapsed time: 2–4 weeks at gaishikei, 4–8 weeks at Japanese employers. Mercari
publishes the time-to-offer median around 3 weeks.</p>

<h2 id="remote">Remote / hybrid reality</h2>
<p>The pandemic-era full-remote era is largely over. From the TokyoDev 2025 survey:</p>
<ul>
  <li>43% of engineers now work hybrid (up from 37%).</li>
  <li>32% have free-choice remote (down from 38%).</li>
  <li>25% are fully on-site (up modestly).</li>
</ul>
<p>Typical hybrid policies require 2–3 days/week in office. Gaishikei tend to be more
flexible than domestic Japanese companies, with notable exceptions: Rakuten requires
return-to-office; Mercari is hybrid with strong autonomy; most FAANG Tokyo are 3
days/week.</p>

<h2 id="getting-in">Getting in from overseas</h2>
<ul>
  <li><strong>Apply directly</strong> to companies you've actually used as a consumer.
      Mercari, SmartNews, PayPay all have English-language careers pages and accept
      overseas applications.</li>
  <li><strong>Skip the agencies</strong> for the first round, most Japanese tech
      recruiters bias toward Japanese-speaking candidates and skip the foreigner-friendly
      tier in their outreach.</li>
  <li><strong>Have an English-language portfolio.</strong> A clean GitHub, a personal site
      with 2–3 written project case studies, and an English LinkedIn. Japan's tech
      recruiters look at all three.</li>
  <li><strong>Visa is rarely the blocker.</strong> At companies on the Tier 1 list above,
      visa sponsorship is the default. The "ability to work from abroad" filter is more
      useful than the "visa sponsorship" filter, abroad-accepting companies have already
      streamlined their visa pipeline.</li>
  <li><strong>Join Tokyo Dev Slack</strong> before applying. The community-driven referral
      flow is meaningful, many roles in the #referrals channel never get posted publicly.</li>
</ul>
<div class="callout">
  Build your career roadmap with the <a href="/roadmaps/software-engineering">Software
  Engineering roadmap</a>, five stages from junior to principal, with promotion criteria
  and Japan-specific notes at each level.
</div>
<!-- ENRICH_V2:software-engineering -->
<h2 id="tokyodev-2026">TokyoDev 2025–26 survey deep dive</h2>
<p>TokyoDev's annual developer survey (989 international engineers in 2025; ~1,100
in early 2026) is the most reliable single benchmark for foreigners in Japan tech.
The 2025–26 findings:</p>
<ul>
  <li><strong>Median total comp:</strong> ¥9.5M (2025 survey), trending toward
      ¥10–10.5M in the 2026 update. Job-changers see 18–25% raises on switch.</li>
  <li><strong>Distribution by employer type:</strong>
      <ul>
        <li>Japanese-headquartered employer: median ¥8.5M</li>
        <li>Foreign-cap Japan office (FAANG, Stripe, etc.): median ¥13.5M</li>
        <li>Fully-remote foreign employer (no Japan entity): median ¥13.5M</li>
      </ul></li>
  <li><strong>JLPT distribution among working engineers:</strong> N5/no Japanese 22%,
      N4 18%, N3 24%, N2 24%, N1 12%. The N3 → N2 jump is associated with the
      largest pay step.</li>
  <li><strong>Hybrid/remote split:</strong> 43% hybrid, 32% fully remote, 25% on-site.
      Hybrid trending up; pure-remote trending down vs 2023.</li>
  <li><strong>Top employers by satisfaction:</strong> Stripe Tokyo, Mercari,
      Indeed Tokyo, Google Japan, Cybozu, SmartNews (consistent over 3+ years).</li>
  <li><strong>Visa types:</strong> 60% on Engineer/Specialist, 25% on HSP, 8% on
      PR/Spouse, 7% other. HSP track is dominant for senior engineers.</li>
  <li><strong>Average tenure in Japan among respondents:</strong> 6.3 years
      (foreign engineer pool is no longer a "1-year tourist" demographic).</li>
</ul>

<h2 id="ai-infra-boom">AI infrastructure hiring boom</h2>
<p>Three drivers are creating an AI-infra hiring wave in Tokyo through 2025–26:</p>
<ul>
  <li><strong>Government AI compute program.</strong> METI awarded large compute
      subsidies in 2024 to Sakura Internet, KDDI, Preferred Networks, and Softbank.
      Each is now scaling AI-infrastructure engineering teams.</li>
  <li><strong>Sakana AI (Tokyo, founded 2023)</strong>, ex-Google Brain researchers
      David Ha and Llion Jones; raised $214M Series A in 2024 (Lux Capital + Khosla).
      Open job pool is small but high-paying, ¥18–35M for senior research
      engineers.</li>
  <li><strong>Foreign AI lab expansion.</strong> OpenAI Tokyo office opened in 2024;
      Anthropic announced Tokyo presence in 2025; Google DeepMind Tokyo, Amazon
      Science Tokyo, and Microsoft Research Asia (Tokyo expansion) all scaling.</li>
</ul>
<p>What this means for foreign engineers:</p>
<ul>
  <li>The premium for AI-infrastructure skills (CUDA, TPU/HBM-aware Python, large-
      model training pipelines) has materially increased in Tokyo. Roles that paid
      ¥15M in 2023 routinely pay ¥22–28M in 2026.</li>
  <li>The supply is small. Tokyo has perhaps 200–300 engineers with serious
      large-model production experience. Companies bid hard for this pool.</li>
  <li>Remote / hybrid is more common in AI roles than in typical Tokyo tech, Sakana
      AI, OpenAI Tokyo, and Anthropic offer significant flexibility.</li>
</ul>

<h2 id="nikkei-engineer">Nikkei vs gaishikei, the engineer's choice</h2>
<p>The Tokyo engineering universe splits into <em>nikkei</em> (Japanese-headquartered)
and <em>gaishikei</em> (foreign-headquartered) employers. The trade-offs:</p>
<table>
  <thead><tr><th>Dimension</th><th>Nikkei (Mercari, Cyberagent, Rakuten)</th><th>Gaishikei (FAANG, Stripe, Datadog)</th></tr></thead>
  <tbody>
    <tr><td>Pay</td><td>Lower base, smaller equity</td><td>Higher base, significant RSUs</td></tr>
    <tr><td>Promotion</td><td>Slower; tenure matters</td><td>Faster; performance-driven</td></tr>
    <tr><td>Language requirement</td><td>JP helpful, sometimes essential</td><td>Mostly English; JP not required</td></tr>
    <tr><td>Stability</td><td>Very stable; layoffs uncommon</td><td>Less stable; HQ layoffs hit Tokyo offices</td></tr>
    <tr><td>Tech stack modernity</td><td>Modern at tier-1 (Mercari, SmartNews)</td><td>Modern everywhere</td></tr>
    <tr><td>Work-life balance</td><td>Generally good</td><td>Variable; FAANG Tokyo can be intense</td></tr>
    <tr><td>Onboarding for foreigners</td><td>Varies dramatically</td><td>Excellent</td></tr>
    <tr><td>PR / permanent-residence path</td><td>Sponsorship typically supported</td><td>Generally supported</td></tr>
    <tr><td>Career capital outside Japan</td><td>Mid, Mercari brand carries internationally; smaller Japan firms less so</td><td>High, FAANG Tokyo tenure is globally portable</td></tr>
  </tbody>
</table>

<h2 id="interview-prep-deep">Interview prep, concrete resources</h2>
<h3>Algorithms / coding</h3>
<ul>
  <li><strong>Neetcode 150</strong>, the standard problem list for FAANG-style
      coding interviews.</li>
  <li><strong>Cracking the Coding Interview</strong>, classic reference.</li>
  <li><strong>LeetCode</strong>, 2 problems/day for 8 weeks brings you to FAANG
      interview level.</li>
</ul>
<h3>System design</h3>
<ul>
  <li><strong>System Design Interview Volume 1 &amp; 2 (Alex Xu)</strong>, the
      most-cited prep book.</li>
  <li><strong>"Designing Data-Intensive Applications" (Martin Kleppmann)</strong>, deep technical foundation.</li>
  <li><strong>ByteByteGo newsletter</strong>, bite-sized system-design content.</li>
  <li><strong>Hello Interview</strong>, modern system-design prep platform.</li>
</ul>
<h3>Japan-specific</h3>
<ul>
  <li><strong>TokyoDev articles</strong>, detailed company guides; interview reports.</li>
  <li><strong>JapanDev career blog</strong>, company-specific deep dives.</li>
  <li><strong>Japan-Refactor</strong>, salary negotiation tactics.</li>
  <li><strong>Reddit r/japanlife / r/cscareerquestionsJP</strong>, recent
      interview experience reports.</li>
</ul>
<h3>Japanese language for interviews</h3>
<ul>
  <li><strong>Bunpro</strong>, grammar SRS; very effective for N3–N1.</li>
  <li><strong>WaniKani</strong>, kanji SRS; pairs well with Bunpro.</li>
  <li><strong>iTalki Japanese tutor</strong>, 1–2 hr/week for speaking practice.</li>
  <li><strong>Common technical terms in JP</strong>, work through "Japanese for IT
      Engineers" (J-OS Press).</li>
</ul>

<h2 id="after-2-years">What changes after 2 years in Tokyo</h2>
<p>The first 2 years and the years after are very different. Practical guide to
what to expect at each stage:</p>
<ul>
  <li><strong>Year 1:</strong> establishing tax residency, getting a hanko, opening
      a bank account, getting health insurance, finding apartment, learning the
      commute. JLPT N4–N3 if studying.</li>
  <li><strong>Year 2:</strong> first job change (typically +20–30% pay). Considering
      HSP visa. JLPT N3–N2 if studying.</li>
  <li><strong>Year 3:</strong> HSP visa applied. Some engineers apply for PR via
      HSP fast track (1 year at 80+ pts). Buying property becomes realistic.</li>
  <li><strong>Year 4–5:</strong> PR application processing (3 years at 70+ pts is
      common path). Senior promotion if at a good company.</li>
  <li><strong>Year 5+:</strong> PR granted for most; mortgage rates improve to
      Japanese-resident rates (1.0–1.4% for fixed 30-year). Career inflection point, Staff or Tech Lead promotion, founder potential, deeper community engagement.</li>
</ul>

<h2 id="contractor-track">Contractor / freelance / consulting tracks</h2>
<p>The independent-contractor path is meaningfully harder in Japan than in the US/UK
but it exists. Key facts:</p>
<ul>
  <li><strong>Visa.</strong> Freelance work requires either Engineer/Specialist with
      employer sponsorship, HSP with self-employment activity permitted, PR, or
      Spouse visa. There's no general "freelance visa" but HSP and PR both work.</li>
  <li><strong>Tax setup.</strong> Register as kojinjigyou (個人事業主) at your local
      tax office (~30 minutes, free). File annual blue/white tax return (青色申告).</li>
  <li><strong>Rates.</strong> Bilingual senior engineers contract at ¥8,000–
      ¥15,000/hour or ¥1.2–2.5M/month for full-time engagement. Higher rates for
      AI/ML specialists.</li>
  <li><strong>Standard platforms / agencies:</strong> Lapras, Levtech Freelance,
      Geechs, Tech Stock, ProConnect, MidWorks. Foreign-friendly: Octo, MGS,
      JapanRise.</li>
  <li><strong>Direct contracts.</strong> Most lucrative; usually word-of-mouth.
      Mercari, PayPay, smaller Japanese SaaS regularly hire foreign contractors
      direct.</li>
  <li><strong>Consumption tax.</strong> If revenue exceeds ¥10M/year, you become
      taxable for consumption tax (currently 10%). Plan accordingly.</li>
  <li><strong>Health insurance/pension.</strong> Switches from employer-based
      Shakai Hoken to National Health Insurance + National Pension. Net cost
      typically lower for senior earners.</li>
</ul>


<div class="callout">
  Looking for boards, recruiters, or language tools? See our
  <a href="/resources/external-resources">curated external-resources
  directory</a> for 60+ vetted sites with honest usage notes.
</div>
""",
    },

    # ------------------------------------------------------------------ Teaching English
    {
        "slug": "teaching-english",
        "category": "Role",
        "icon": "mortar-board",
        "title": "Teaching English in Japan, the honest breakdown",
        "summary": "JET vs. eikaiwa vs. dispatch ALT, what each actually pays, what working conditions look like, why most people leave within 3 years, and the paths from teaching into other careers.",
        "updated": "May 2026",
        "read_time": "10 min",
        "toc": [
            ("market", "The teaching market in 2026"),
            ("jet", "JET Programme"),
            ("eikaiwa", "Eikaiwa (conversation schools)"),
            ("dispatch-alt", "Dispatch ALT companies"),
            ("intl-schools", "International schools"),
            ("comparison", "Side-by-side comparison"),
            ("reality", "The honest realities"),
            ("exit-paths", "Exit paths into other careers"),
            ("jet-2026", 'JET 2026, pay raise and current intake'),
            ("eikaiwa-shakeout", 'Eikaiwa shake-out, NOVA, AEON, ECC in 2026'),
            ("intl-schools-deep", 'International schools, the better paid track'),
            ("university-track", 'University teaching, the underrated path'),
            ("pivots-deep", 'Pivots from teaching, concrete paths and timelines'),
            ("survival-finance", 'Surviving on teaching pay, practical financial guide'),
        ],
        "body": """
<h2 id="market">The teaching market in 2026</h2>
<p>Teaching English in Japan remains the most accessible career path for native English
speakers without specialised degrees or Japanese ability. The market splits into four
distinct tracks with very different conditions, salaries, and trajectories.</p>
<ul>
  <li><strong>JET Programme</strong> (government-run): ~5,900 participants from 54
      countries as of July 2025.</li>
  <li><strong>Eikaiwa</strong> (private conversation schools): largest segment by
      headcount.</li>
  <li><strong>Dispatch ALT</strong> (private companies placing teachers in public
      schools): growing share, often the most precarious.</li>
  <li><strong>International schools</strong> (English-medium K-12): smallest segment by
      headcount, highest pay and conditions.</li>
</ul>
<p>The 2024–25 trend: dispatch ALT pay has stagnated, JET pay was raised meaningfully
(April 2025 brought a band to ¥4.02–4.32M for higher-cost placements, up from the
historical ¥3.36M), and international-school hiring has tightened due to expat-family
mobility being lower post-pandemic.</p>

<h2 id="jet">JET Programme (Japanese Exchange and Teaching)</h2>
<p>The government-run programme, established 1987, places foreign graduates in public
schools and government offices across all 47 prefectures.</p>
<h3>Roles</h3>
<ul>
  <li><strong>ALT (Assistant Language Teacher):</strong> ~85% of JETs. Placed in public
      elementary, junior high, or high schools.</li>
  <li><strong>CIR (Coordinator for International Relations):</strong> ~10%. Government
      offices, translation/interpretation, intercultural exchange work. Requires N2-level
      Japanese.</li>
  <li><strong>SEA (Sports Education Advisor):</strong> small number. Sports coaching at
      public schools.</li>
</ul>
<h3>Salary (2025–26)</h3>
<table>
  <thead><tr><th>Year</th><th>Salary band</th></tr></thead>
  <tbody>
    <tr><td>Year 1</td><td>¥3.36M (standard) or ¥4.02M (higher-cost areas, April 2025+)</td></tr>
    <tr><td>Year 2</td><td>¥3.60M / ¥4.20M</td></tr>
    <tr><td>Year 3</td><td>¥3.90M / ¥4.32M</td></tr>
    <tr><td>Year 4–5</td><td>¥3.96M / ¥4.32M</td></tr>
  </tbody>
</table>
<p>Plus: housing assistance (typically subsidised significantly by the placement
authority), paid sick leave, ~20 paid vacation days/year, plus the standard Japanese
national holidays.</p>
<h3>Application</h3>
<p>Annual cycle: applications open October, close November/December. Interviews at the
Japanese consulate/embassy in your home country in February. Acceptance notifications
April–May. Placement details May–July. Departure late July or early August.
Acceptance rate roughly 25%.</p>
<h3>Pros and cons</h3>
<ul>
  <li><strong>Pros:</strong> highest pay in entry-level teaching, government backing,
      housing support, real vacation days, strong cohort community.</li>
  <li><strong>Cons:</strong> placement is rarely in your top-3 choices (most JETs land
      rural), single-year contracts, no career progression within the programme, max 5
      years total tenure.</li>
</ul>

<h2 id="eikaiwa">Eikaiwa (private conversation schools)</h2>
<p>Private language schools running after-hours and weekend classes. The "Big 3":
NOVA, AEON, ECC. Plus dozens of smaller chains and independents.</p>
<h3>Salary at major chains (2025–26)</h3>
<table>
  <thead><tr><th>Company</th><th>Monthly base</th><th>Annual</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>NOVA</td><td>¥280–320K</td><td>¥3.36–3.84M</td><td>Largest chain; high turnover</td></tr>
    <tr><td>AEON</td><td>¥275K fixed</td><td>¥3.30M</td><td>Base ¥255K + ¥20K fixed overtime allowance</td></tr>
    <tr><td>ECC</td><td>¥250–270K</td><td>¥3.00–3.24M</td><td>Strong training program, conservative dress code</td></tr>
    <tr><td>Berlitz</td><td>¥255–290K</td><td>¥3.06–3.48M</td><td>Corporate / business English-focused</td></tr>
    <tr><td>Smaller / independent eikaiwa</td><td>¥230–280K</td><td>¥2.76–3.36M</td><td>Vary widely</td></tr>
  </tbody>
</table>
<h3>Working conditions</h3>
<ul>
  <li><strong>Schedule:</strong> typically Tuesday–Saturday or Wednesday–Sunday, since
      students attend evenings and weekends. You will work at least one weekend day,
      often both.</li>
  <li><strong>Class load:</strong> usually 5–8 classes per day, 40–50 minutes each,
      back-to-back with short prep breaks.</li>
  <li><strong>Paid leave:</strong> usually 10 days/year (legal minimum), plus standard
      Japanese national holidays. Eikaiwa generally honour paid leave.</li>
  <li><strong>Visa:</strong> sponsored under Engineer/Specialist in Humanities (not
      Instructor).</li>
</ul>

<h2 id="dispatch-alt">Dispatch ALT companies</h2>
<p>Private companies (Interac, Heart Corporation, Borderlink, Joytalk, and many smaller
operators) that win contracts with municipal boards of education to staff public schools
with ALTs. Lower pay than JET, more precarious than direct hires.</p>
<h3>Salary (2025–26)</h3>
<table>
  <thead><tr><th>Company</th><th>Monthly</th><th>Annual</th></tr></thead>
  <tbody>
    <tr><td>Interac (largest dispatcher)</td><td>¥190–240K</td><td>¥2.28–2.88M</td></tr>
    <tr><td>Heart Corporation</td><td>¥200–260K</td><td>¥2.40–3.12M</td></tr>
    <tr><td>Borderlink</td><td>¥190–230K</td><td>¥2.28–2.76M</td></tr>
  </tbody>
</table>
<h3>Why dispatch pays less than JET</h3>
<p>The municipal board of education pays the dispatch company per teacher placed. The
company takes its margin off the top. Most dispatch teachers are placed in the same
public schools as JETs, doing the same work, for substantially less money, sometimes
working alongside a JET who earns 50% more.</p>
<h3>Major issues</h3>
<ul>
  <li><strong>"You're only paid for hours in school."</strong> Many dispatchers don't pay
      for prep time or non-class hours within the contracted school day.</li>
  <li><strong>Summer/winter contract gaps.</strong> Some dispatchers pause pay during
      school holidays (illegal in many cases, challenge it).</li>
  <li><strong>Three-year cap.</strong> A dispatch worker cannot stay with the same
      dispatcher for more than three years unless converted to a direct/permanent
      contract, which is rare.</li>
  <li><strong>Limited support.</strong> The dispatcher is often hours away by train; if
      something goes wrong at school, you're on your own.</li>
</ul>
<div class="warn">
  <strong>If you're choosing between JET and dispatch:</strong> the salary gap is real
  and the working conditions are noticeably worse at dispatchers. Apply to JET first;
  fall back to dispatch only if JET is closed or you didn't make it through.
</div>

<h2 id="intl-schools">International schools</h2>
<p>Real K-12 schools serving expat families and a growing Japanese-international
population. Pay 60–150% higher than eikaiwa, real career progression, and significantly
more autonomy.</p>
<h3>Requirements</h3>
<ul>
  <li><strong>Real teaching credential</strong>, a PGCE (UK), state teaching license
      (US), or equivalent. International schools rarely hire untrained native speakers.</li>
  <li><strong>2+ years of classroom experience</strong> in your home country usually
      required for serious roles.</li>
  <li><strong>Often a specific subject specialisation</strong> (math, science, English
      lit, history) rather than generalist "English teaching."</li>
</ul>
<h3>Salary</h3>
<p>¥5–9M for classroom teachers; ¥9–14M for heads of department; ¥12–20M for principals
and senior administrators. Many international schools include housing allowances and
flight allowances for international hires.</p>
<h3>Major employers</h3>
<p>American School in Japan (ASIJ, Chofu), British School in Tokyo, Tokyo International
School, K International (Tokyo), Yokohama International School, Saint Maur (Yokohama),
Osaka International School (Senri), Kobe Canadian Academy.</p>

<h2 id="comparison">Side-by-side comparison</h2>
<table>
  <thead><tr><th>Track</th><th>Pay (yr 1)</th><th>Hours</th><th>Visa</th><th>Path</th></tr></thead>
  <tbody>
    <tr><td>JET</td><td>¥3.36–4.32M</td><td>Standard school week</td><td>Instructor or Specified Activities</td><td>Max 5 yrs in program</td></tr>
    <tr><td>Eikaiwa (NOVA / AEON / ECC)</td><td>¥3.00–3.84M</td><td>Evenings + weekends</td><td>Engineer/Specialist</td><td>2–4 yrs typical</td></tr>
    <tr><td>Dispatch ALT</td><td>¥2.28–3.12M</td><td>School day</td><td>Engineer/Specialist</td><td>Max 3 yrs same dispatcher</td></tr>
    <tr><td>International school</td><td>¥5–9M</td><td>Standard school week</td><td>Instructor</td><td>Long-term career</td></tr>
  </tbody>
</table>

<h2 id="reality">The honest realities</h2>
<ul>
  <li><strong>The ceiling is low.</strong> Most teaching jobs cap around ¥4M without
      moving into management, training design, or international schools. Compared to
      ¥9.5M median for engineers, the financial gap widens every year.</li>
  <li><strong>Burnout is real.</strong> 5–8 back-to-back conversation classes, week after
      week, especially with children, wears people down. Industry-wide turnover at
      eikaiwa runs 30–50% annually.</li>
  <li><strong>The visa is portable but the skills aren't easily transferable</strong>
      back home. Three years of eikaiwa teaching translates to "ESL teacher" on a Western
      resume, useful for some roles, irrelevant for most.</li>
  <li><strong>Japanese improves but slowly.</strong> Most eikaiwa and ALT workers reach
      survival Japanese (N4-N3) by year 2 and plateau. Real fluency requires deliberate
      study outside work hours that few find time for.</li>
  <li><strong>Living is comfortable enough.</strong> ¥3M/yr buys a basic but workable
      life in suburban Tokyo or any of the smaller cities. International school income is
      genuinely solid.</li>
</ul>

<h2 id="exit-paths">Exit paths into other careers</h2>
<p>Most foreign teachers leave Japan or move into a different career within 3 years. The
common transition paths:</p>
<ul>
  <li><strong>Teaching → corporate training / curriculum design.</strong> Same skills
      applied to a higher-paying B2B context. Companies like Beyond Language Learning,
      Berlitz Corporate, and various in-house language departments pay ¥5–8M for
      experienced corporate trainers.</li>
  <li><strong>Teaching → bilingual sales / customer success.</strong> If your Japanese
      has reached N2+, your communication skills translate. Many SaaS companies pay
      ¥6–10M for foreign customer success managers.</li>
  <li><strong>Teaching → tech via self-study.</strong> A small but real cohort breaks
      into software engineering after a year or two of focused self-study. JET savings
      help fund the transition. See the
      <a href="/stories/marco-eikaiwa-to-engineering">Marco eikaiwa-to-engineering story</a>
      for a representative path.</li>
  <li><strong>Teaching → translation / interpretation.</strong> Requires N1 + specialised
      skills. Pays ¥4–8M for full-time staff roles.</li>
  <li><strong>Teaching → starting your own school or business.</strong> Requires the
      Business Manager visa (post-October 2025: ¥30M capital, full-time staff, JLPT N2)
      so this is a long-term play, not a quick exit.</li>
</ul>
<div class="callout">
  If you came to Japan via teaching and want to keep going long-term, start exit-planning
  in your first six months. The longer you stay in eikaiwa specifically, the harder the
  transition tends to get, both because of skill atrophy and because Japanese hiring
  managers begin reading your CV as "career teacher."
</div>
<!-- ENRICH_V2:teaching-english -->
<h2 id="jet-2026">JET 2026, pay raise and current intake</h2>
<p>The JET (Japan Exchange and Teaching) Programme increased its pay across all
appointments effective April 2026, the largest single-cycle raise in a decade:</p>
<table>
  <thead><tr><th>Year</th><th>Pre-tax annual (¥)</th><th>Monthly (¥)</th></tr></thead>
  <tbody>
    <tr><td>1st appointment</td><td>¥4,020,000</td><td>¥335,000</td></tr>
    <tr><td>2nd appointment</td><td>¥4,140,000</td><td>¥345,000</td></tr>
    <tr><td>3rd appointment</td><td>¥4,260,000</td><td>¥355,000</td></tr>
    <tr><td>4th &amp; 5th appointment (exceptional)</td><td>¥4,320,000</td><td>¥360,000</td></tr>
  </tbody>
</table>
<p>Practical notes:</p>
<ul>
  <li>JET is a contracted-employee programme administered by the local Board of
      Education (Kyōikuiinkai 教育委員会); your employer is technically the
      municipality, not the central JET programme. Some boards are wonderful
      employers; others are bureaucratic.</li>
  <li>Annual leave is 20+ days; sick leave is generous.</li>
  <li>JET is the only English-teaching gig where the employer regularly covers
      flights to/from Japan (round-trip on first arrival, plus one-way home on
      completion).</li>
  <li>Application cycles: October–November application window for August arrival
      the following year. The 11-month timeline catches many people by surprise.</li>
  <li>Annual intake in 2026: approximately 6,000 ALTs and 200 CIRs (Coordinator for
      International Relations, bilingual track).</li>
  <li>Placement: rural placements (Hokkaido, Shimane, Kochi, etc.) make up the
      majority. Tokyo placements exist but are competitive.</li>
</ul>

<h2 id="eikaiwa-shakeout">Eikaiwa shake-out, NOVA, AEON, ECC in 2026</h2>
<p>The eikaiwa (英会話) industry is in long-term structural decline due to declining
birthrate and remote-learning displacement. Where the major chains stand in 2026:</p>
<table>
  <thead><tr><th>Chain</th><th>Approx schools</th><th>Pay (entry)</th><th>Reputation</th></tr></thead>
  <tbody>
    <tr><td>NOVA</td><td>~400 schools</td><td>¥230–270K/mo</td>
        <td>Lower-pay, more flexible scheduling; under post-bankruptcy management
        since 2007; mixed reviews on r/teachinginjapan.</td></tr>
    <tr><td>AEON</td><td>~200 schools</td><td>¥255–285K/mo</td>
        <td>More structured; better training; better-paying than NOVA but more
        demanding schedule.</td></tr>
    <tr><td>ECC</td><td>~140 schools</td><td>¥250–280K/mo</td>
        <td>Mid-tier; reasonable pay; mid-tier reputation.</td></tr>
    <tr><td>Berlitz</td><td>~50 schools</td><td>¥1,800–2,500/lesson</td>
        <td>Hourly model; foreigners can earn ¥250K+/mo if you take 25+ lessons/wk.</td></tr>
    <tr><td>Gaba</td><td>~40 schools</td><td>¥1,500–2,000/lesson</td>
        <td>1-on-1 model; flexible scheduling but lesson-rate compensation.</td></tr>
    <tr><td>Peppy Kids Club</td><td>~1,400 small classes</td><td>¥240–290K/mo</td>
        <td>Children-focused; high-turnover.</td></tr>
  </tbody>
</table>
<p>Key 2024–26 trends:</p>
<ul>
  <li><strong>Online English schools</strong> (DMM Eikaiwa, Cambly, Rarejob) hire
      remote foreign instructors at $5–15/hr, typically not a primary income but
      useful side gig.</li>
  <li><strong>NOVA-AEON merger talks</strong> have surfaced periodically; consolidation
      is likely.</li>
  <li><strong>Visa sponsorship at chain eikaiwa</strong> remains routine but tightening, chains increasingly prefer candidates already in Japan.</li>
  <li><strong>Black eikaiwa lists</strong> circulate on r/teachinginjapan. Search the
      specific chain plus "review" before signing.</li>
</ul>

<h2 id="intl-schools-deep">International schools, the better paid track</h2>
<p>International schools are the highest-paying English-teaching track in Japan,
typically requiring credentials beyond bachelor's:</p>
<ul>
  <li><strong>Requirements:</strong> Teaching credential (state certification in
      home country) is mandatory at top schools. Master's in Education is preferred.
      2–5 years prior international or home-country teaching experience.</li>
  <li><strong>Pay:</strong> ¥7–13M for early-career; ¥13–22M for experienced /
      department heads. Many schools include housing allowance (¥150–300K/month)
      and tuition for 1–2 children.</li>
  <li><strong>Top-tier Tokyo schools:</strong> American School in Japan (Chofu),
      British School in Tokyo, Tokyo International School, Aoba-Japan,
      K. International School, Seisen International. Tuition ¥3M+/year per child.</li>
  <li><strong>Mid-tier Tokyo schools:</strong> Yokohama International School,
      Saint Maur Yokohama, International School of the Sacred Heart, Christian
      Academy in Japan.</li>
  <li><strong>Application cycle:</strong> September–December application for August
      start. International recruitment fairs (Search Associates, ISS, GRC, AISH)
      are the primary channel.</li>
  <li><strong>Visa:</strong> Instructor visa (sponsored by school); typically 3- or
      5-year tracks.</li>
</ul>

<h2 id="university-track">University teaching, the underrated path</h2>
<p>University teaching of English (and other subjects in English) is the most
under-discussed comfortable career path for foreigners in Japan. The track:</p>
<ul>
  <li><strong>Adjunct / non-tenure-track ESL instructor:</strong> ¥3.5–5.5M/year for
      8–12 contact hours/week. Common entry point. Most Japanese universities (Sophia,
      Waseda, Keio, ICU, Temple Japan) hire English instructors regularly.</li>
  <li><strong>Tenure-track foreign faculty:</strong> ¥7–14M/year; tenure decision
      typically 4–6 years. Requires PhD in most cases. Excellent work-life balance
      (~16 contact hours/week + research).</li>
  <li><strong>English-medium graduate programs</strong> at top universities (Keio
      Graduate School of Media Design, Tokyo Tech, University of Tokyo's GraSPP)
      hire foreign professors for specialised teaching at ¥10–18M tenure-track.</li>
  <li><strong>Public universities</strong> (Tokyo, Tohoku, Kyoto, Hokkaido, Kyushu)
      tend to be most prestigious; private universities (Waseda, Keio, Sophia, ICU)
      tend to pay best.</li>
  <li><strong>Pivot from JET to university</strong> often works via 1–2 years adjunct
      while pursuing Master's; many JET alumni go this route.</li>
</ul>

<h2 id="pivots-deep">Pivots from teaching, concrete paths and timelines</h2>
<table>
  <thead><tr><th>Destination</th><th>Realistic timeline</th><th>How to prepare</th></tr></thead>
  <tbody>
    <tr><td>Software engineering</td>
        <td>1.5–2.5 years</td>
        <td>Bootcamp (Le Wagon Tokyo, Code Chrysalis) + portfolio + JLPT N3. Many
        successful pivots into Mercari / PayPay / foreign-cap entry roles.</td></tr>
    <tr><td>UX / Product design</td>
        <td>1–2 years</td>
        <td>Portfolio with 3 case studies + Figma fluency + design exercises.
        Goodpatch, SmartNews, Mercari all hire from this pivot.</td></tr>
    <tr><td>Tech recruiting</td>
        <td>6–12 months</td>
        <td>Bilingual recruiters in heavy demand; entry-level openings at Robert
        Walters, Computer Futures, JAC Recruitment, Computer People.</td></tr>
    <tr><td>Content writing / SEO</td>
        <td>3–9 months</td>
        <td>Build a portfolio of 3–5 published pieces; pitch directly to foreign-cap
        Japan blogs (HubSpot, Notion, Stripe, Datadog).</td></tr>
    <tr><td>Translation / localisation</td>
        <td>1–2 years</td>
        <td>JLPT N1 + technical / specialist domain. Lower pay than peers think
        (¥4–7M typical) but stable.</td></tr>
    <tr><td>Customer success at SaaS</td>
        <td>6–12 months</td>
        <td>Bilingual N2+ CSMs in demand at Salesforce, HubSpot, Notion, Snowflake
        Japan. ¥7–11M entry.</td></tr>
    <tr><td>Account executive (sales)</td>
        <td>9–18 months (typically via SDR first)</td>
        <td>SDR programmes at SaaS Japan (Salesforce, HubSpot, Datadog) hire
        bilingual ESL teachers regularly.</td></tr>
    <tr><td>International school teacher (credentialed)</td>
        <td>2–4 years (credentialing)</td>
        <td>State teaching certification or PGCE + experience. Higher pay than any
        eikaiwa or ALT track.</td></tr>
    <tr><td>University adjunct → tenure-track</td>
        <td>2–6 years (Master's + adjunct + tenure decision)</td>
        <td>Concurrent Master's while teaching; build research/publication record.</td></tr>
  </tbody>
</table>

<h2 id="survival-finance">Surviving on teaching pay, practical financial guide</h2>
<p>If you're on ¥3M–¥4.5M (eikaiwa or first-year JET), the practical budget:</p>
<ul>
  <li><strong>Rent:</strong> aim for ¥60–90K (1R or 1K outside central). Setagaya,
      Suginami, Itabashi, Adachi, or Kawaguchi/Toda. Avoid central wards unless
      sharing.</li>
  <li><strong>Food:</strong> ¥35–50K with home cooking 5+ nights/week. Cheap supermarkets
      (Gyomu Super, Aeon, Maruetsu Petit) for staples; convenience-store eating
      adds up quickly.</li>
  <li><strong>Transport:</strong> employer covers commute (most teaching jobs).
      Tokyo Subway 24-hour pass (¥800) for weekend exploration.</li>
  <li><strong>Phone:</strong> MVNO at ¥1,500–3,000/month (IIJmio, Rakuten Mobile,
      LINEMO). Avoid big-3 carriers.</li>
  <li><strong>Health:</strong> Shakai Hoken covers most; the foreign-resident clinic
      network (English-speaking) costs ¥3,000–5,000/visit out of pocket.</li>
  <li><strong>Savings:</strong> on ¥3.5M, expect ¥30–60K/month possible. On ¥4M,
      ¥60–100K possible.</li>
  <li><strong>Tax:</strong> file every year, even if it's simple. First-year tax
      filing is at the prefecture office; subsequent years can be done online via
      e-Tax with a MyNumber card.</li>
  <li><strong>Investment:</strong> if you'll stay long-term, open a NISA (新NISA,
      2024+) account at Rakuten Securities or SBI. ¥3.6M annual contribution cap;
      tax-free gains for 20 years.</li>
</ul>


<div class="callout">
  Looking for boards, recruiters, or language tools? See our
  <a href="/resources/external-resources">curated external-resources
  directory</a> for 60+ vetted sites with honest usage notes.
</div>
""",
    },

    # NEW_ROLE_GUIDES:v1
    {
        "slug": "product-management",
        "category": 'Role',
        "icon": 'clipboard',
        "title": "Product management in Japan, the foreigner's guide",
        "summary": ('PM jobs in Japan are scarcer than engineering, but bilingual PMs are heavily oversubscribed on '
 "the demand side. Who's actually hiring, what the comp looks like, and how to get in if you "
 "weren't already on the inside."),
        "updated": 'May 2026',
        "read_time": '10 min',
        "toc": [   ('market', 'The 2026 PM market'),
    ('companies', 'Companies hiring foreign PMs'),
    ('comp', 'Compensation by level'),
    ('getting-in', 'How foreigners actually get PM roles'),
    ('japanese', 'Japanese language reality'),
    ('interview', 'Interview process'),
    ('flavors', 'PM flavors, product, growth, platform'),
            ("apm-programs", 'APM programmes in Japan'),
            ("pm-portfolio", 'PM portfolio essentials for Japan'),
            ("salary-deep", 'Bilingual PM salary, deep dive'),
            ("pm-ja-cultural", "What's culturally different about Japan PM"),
            ("pm-tools", 'Tools used by Japan PM teams'),
    ('pivots', 'Pivoting into PM from another role')],
        "body": """
<h2 id="market">The 2026 PM market</h2>
<p>Product management is a structurally smaller field in Japan than in the US, by
headcount, by job-post volume, and by recruiter coverage. Three reasons:</p>
<ul>
  <li><strong>Engineering-led culture.</strong> Most Japanese tech companies, including
      Rakuten, LINE Yahoo, Cybozu, Cyberagent, historically delegated product decisions
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
PM headcount through 2025, and Robert Walters' 2026 sector report flags
<em>Senior Product Manager (bilingual)</em> as a top-five demand role in technology &
online.</p>

<h2 id="companies">Companies hiring foreign PMs</h2>
<h3>Tier 1, actively hire foreign / bilingual PMs</h3>
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
<h3>Tier 2, Japanese companies with growing PM functions</h3>
<ul>
  <li><strong>Cyberagent</strong>, large product org across gaming, ad-tech, media.
      Japanese-first but some teams welcome bilingual PMs.</li>
  <li><strong>DeNA</strong>, product across gaming, healthcare, mobility. Some
      bilingual divisions.</li>
  <li><strong>Money Forward</strong>, fintech B2B/B2C; PMs are mostly Japanese but
      English-friendly bilinguals are recruited.</li>
  <li><strong>Rakuten</strong>, officially English-as-corporate-language; PM roles
      span 70+ services. Japanese is helpful but not always required.</li>
  <li><strong>LINE Yahoo Japan</strong>, large product org post-merger; English-OK
      teams exist on the LINE side.</li>
</ul>
<h3>Tier 3, startups</h3>
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
every level. The gap widens at senior and above, a Senior PM at Google Japan with
RSUs can clear ¥25M, while the same role at Mercari sits in the ¥14–18M band.</p>

<h2 id="getting-in">How foreigners actually get PM roles</h2>
<p>Three dominant entry paths:</p>
<ol>
  <li><strong>Internal pivot at a foreigner-friendly company.</strong> Mercari, PayPay,
      Indeed, and SmartNews regularly promote engineers and designers into PM roles.
      Entering as an engineer and pivoting after 1–2 years is the most common path.</li>
  <li><strong>Direct hire from abroad, FAANG.</strong> Google APAC, Amazon Japan, and
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
  <li><strong>Recruiter screen</strong> (30 min), English or Japanese, depending.
      Confirms PM track-record and visa status.</li>
  <li><strong>Hiring-manager interview</strong> (45–60 min), PM career, why-this-
      company, why-PM, recent project deep-dive.</li>
  <li><strong>Product case study</strong> (60 min), typically a take-home (1 week)
      followed by a 60-min walkthrough. Prepare for Japan-context cases (e.g.
      <em>"How would you improve onboarding in Mercari for first-time sellers?"</em>).</li>
  <li><strong>Cross-functional panel</strong> (45–60 min × 2–3), meet engineering,
      design, data partners.</li>
  <li><strong>Leadership / bar-raiser</strong> (45 min), VP of Product or equivalent.</li>
</ol>
<p>Average elapsed time: 3–5 weeks at gaishikei, 5–8 weeks at Japanese employers.
Mercari publishes a 4-week median for PM roles. Expect the case to be the highest-
leverage round, prepare 3 detailed PM stories using a structure like CIRCLES or
your own STAR variant, and be ready to defend metrics choices in Japanese-context
ambiguity.</p>

<h2 id="flavors">PM flavors, product, growth, platform</h2>
<ul>
  <li><strong>Core / Product PM</strong>, feature discovery, customer research, owning
      a slice of the product. Most common at Mercari, SmartNews, PayPay.</li>
  <li><strong>Growth PM</strong>, funnel, retention, conversion, A/B testing. Heavy
      data fluency required. Cyberagent, DeNA, and Mercari all run growth PM tracks.</li>
  <li><strong>Platform / Infrastructure PM</strong>, internal-facing products
      (developer platforms, payment rails, data infrastructure). Indeed, PayPay,
      and FAANG Tokyo all hire heavily here. Comp tends to be the highest of the three
      flavors.</li>
  <li><strong>B2B / Enterprise PM</strong>, Cybozu, Money Forward, Sansan, freee. Heavy
      customer interview cycles in Japanese; ramp curve is longer.</li>
  <li><strong>AI / ML PM</strong>, newest flavor, hottest demand. Sakana AI, PFN,
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
  <li><strong>Consultant → PM</strong>, common in Japan because top-of-class management
      consultants get poached into PM at Mercari and FAANG Tokyo. Strong
      structured-thinking signal, weak shipping signal, close the gap by side-
      projecting.</li>
  <li><strong>Sales / CS → PM</strong> harder but possible at B2B SaaS. You bring
      customer empathy and discovery rigor; you need to ramp on technical fluency and
      data.</li>
</ul>
<div class="callout">
  Build your career roadmap with the
  <a href="/roadmaps/product-management">Product Management roadmap</a>, five stages
  with explicit promotion criteria, salary bands, and Japan-specific notes.
</div>
<!-- ENRICH_V2:product-management -->
<h2 id="apm-programs">APM programmes in Japan</h2>
<p>Formal Associate PM programmes are rare in Japan, most APM roles are filled via
internal transfer from engineering or design rather than external hire. The known
formal programs in 2026:</p>
<ul>
  <li><strong>Mercari APM bootcamp</strong>, informal 6-month internal training.
      Mostly internal transfers; occasionally hires from bootcamps or new grads.</li>
  <li><strong>Indeed Tokyo APM</strong>, part of Indeed's global APM programme;
      bilingual or English-only candidates. ¥7–9M starting comp.</li>
  <li><strong>Google APM (APAC, Tokyo seats)</strong>, global programme; competitive;
      typically 2–3 Tokyo seats per cohort.</li>
  <li><strong>Cybozu kintone PM bootcamp</strong>, Japanese-language focused; for
      Japanese-fluent candidates entering B2B SaaS PM.</li>
</ul>
<p>The realistic path for most foreigners: enter as engineer or designer, ask to
shadow your team's PM, propose owning a small feature area after 6–12 months.</p>

<h2 id="pm-portfolio">PM portfolio essentials for Japan</h2>
<p>Unlike engineering or design, PM portfolios are less standardised. What
hiring managers at Mercari, PayPay, Stripe Tokyo, Indeed Tokyo actually want to see:</p>
<ul>
  <li><strong>3 detailed case studies</strong>, each 800–1,500 words. Structure:
      problem framing → discovery → hypothesis → solution → measurement → outcome.</li>
  <li><strong>Quantified outcomes</strong> in each case. "Increased conversion by X%
      with 95% confidence" beats "improved user experience".</li>
  <li><strong>Show your decision-making, not just outcomes.</strong> Document one
      decision where you ruled out the obvious answer; explain why.</li>
  <li><strong>One end-to-end discovery → ship example.</strong> Demonstrates you've
      run product discovery, not just executed someone else's specs.</li>
  <li><strong>Optional: Japan-context case study.</strong> If you've worked in
      Japan, one case showing you handled a Japan-specific consumer preference well
      is a strong signal.</li>
  <li><strong>Don't overshare confidential data.</strong> Most Japanese employers
      respect NDAs scrupulously; redact numbers if needed but show methodology.</li>
</ul>

<h2 id="salary-deep">Bilingual PM salary, deep dive</h2>
<p>The bilingual PM premium in Tokyo (2026):</p>
<table>
  <thead><tr><th>Level</th><th>English-only (FAANG Tokyo)</th><th>Bilingual (Japanese SaaS)</th></tr></thead>
  <tbody>
    <tr><td>Associate PM</td><td>¥7–9M</td><td>¥6–8M</td></tr>
    <tr><td>PM</td><td>¥10–14M</td><td>¥10–14M</td></tr>
    <tr><td>Senior PM</td><td>¥14–22M</td><td>¥13–18M</td></tr>
    <tr><td>Group PM</td><td>¥18–28M</td><td>¥16–22M</td></tr>
    <tr><td>Director of Product</td><td>¥25–40M</td><td>¥22–32M</td></tr>
  </tbody>
</table>
<p>FAANG Tokyo pays best at every level, but the gap is smaller than for engineering.
Bilingual capacity opens roles at PayPay, Sansan, freee, Money Forward, Cybozu, where mid-level pay reaches ¥10–14M and the company-equity upside can be material
on a public listing or scale.</p>

<h2 id="pm-ja-cultural">What's culturally different about Japan PM</h2>
<ul>
  <li><strong>Nemawashi (根回し)</strong>, Japanese teams build consensus before
      formal decisions. As PM, expect to spend 2–3× more time aligning stakeholders
      individually than you would in a US PM context.</li>
  <li><strong>Slower roadmap cadence.</strong> Quarterly planning is loose; many
      Japanese teams operate on 6-month or annual cadences. Don't try to drive
      US-style "weekly OKR check-ins" without adapting.</li>
  <li><strong>Engineering autonomy.</strong> Japanese engineers historically expect
      more autonomy over implementation choices than US engineers. PM defines
      "what" and rarely "how".</li>
  <li><strong>Customer obsession is different.</strong> Japanese consumers tolerate
      product friction more graciously and complain less; reading silence as
      satisfaction is a common foreigner-PM mistake.</li>
  <li><strong>Risk aversion.</strong> Japanese companies (and PMs) prefer iterative
      improvement to risky big bets. Pitching radical product overhauls requires
      careful coalition-building.</li>
  <li><strong>Visual artefacts matter.</strong> Japanese PMs produce more written
      one-pagers and visual diagrams than US PMs. Beautiful product briefs land
      well; under-formatted documents land poorly.</li>
</ul>

<h2 id="pm-tools">Tools used by Japan PM teams</h2>
<ul>
  <li><strong>Slack</strong>, universal at modern tech employers. LINE is more
      common at traditional Japanese workplaces.</li>
  <li><strong>Jira / Asana / Linear</strong>, Jira at large Japanese tech firms;
      Linear at modern startups; Asana at bilingual SaaS.</li>
  <li><strong>Figma</strong>, universal for design collaboration; replaced
      Sketch and most XD usage.</li>
  <li><strong>Miro / Mural / Whimsical</strong>, workshop facilitation; Miro is the
      Tokyo default.</li>
  <li><strong>Notion / Confluence</strong>, Notion dominant at modern tech; Confluence
      at established Japanese tech.</li>
  <li><strong>Amplitude / Mixpanel / Heap</strong>, product analytics; Amplitude
      most common in Tokyo.</li>
  <li><strong>Hotjar / Microsoft Clarity</strong>, session replay; widely used.</li>
  <li><strong>Optimizely / VWO</strong>, A/B testing; less common than internally-
      built tools at top tech employers (Mercari, PayPay, SmartNews all use internal
      experimentation platforms).</li>
</ul>

""",
    },
    {
        "slug": "marketing-growth",
        "category": 'Role',
        "icon": 'rocket',
        "title": "Marketing & growth in Japan, the foreigner's guide",
        "summary": ('Foreigners can build strong marketing careers in Japan, but the playbook is different from the '
 "US/EU. Performance marketing, brand marketing, content, and growth, what's hiring, what pays, "
 'and what bilingual capacity unlocks.'),
        "updated": 'May 2026',
        "read_time": '10 min',
        "toc": [   ('market', 'The 2026 marketing market'),
    ('flavors', 'Marketing flavors in Japan'),
    ('companies', 'Companies actively hiring'),
    ('comp', 'Compensation by level'),
    ('japanese', 'Japanese language and culture'),
    ('channels', "Channel landscape, what's different in Japan"),
    ('entry', 'How foreigners enter the field'),
            ("channel-2026-shifts", 'Channel shifts, LINE, TikTok, X in 2026'),
            ("inbound-tourism", 'Inbound tourism marketing, the biggest growth area'),
            ("agencies-vs-inhouse", 'Agency vs in-house, career trade-offs'),
            ("japan-specific-tools", 'Japan-specific tools and platforms'),
            ("foreign-marketers-success", 'How foreign marketers actually succeed'),
    ('pivots', 'Common pivots')],
        "body": """
<h2 id="market">The 2026 marketing market</h2>
<p>Japan's marketing industry is large, Dentsu, Hakuhodo, and ADK still dominate
ad spend, but the modern in-house digital marketing function is comparatively
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
      HubSpot, most have Japan marketing teams now and recruit bilingual foreigners
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
<h3>Tier 1, English-friendly, foreigner-receptive</h3>
<ul>
  <li><strong>Mercari</strong>, growth, product marketing, brand. English-OK on
      international team; Japanese for domestic.</li>
  <li><strong>PayPay</strong>, performance marketing, partnerships marketing.
      Bilingual preferred.</li>
  <li><strong>SmartNews</strong>, content, growth, brand. Strong international team.</li>
  <li><strong>Stripe Tokyo</strong>, PMM, content, partner marketing.</li>
  <li><strong>Notion Japan</strong>, content, community, partner marketing.</li>
  <li><strong>HubSpot Japan</strong>, growth, demand gen, content. Heavy bilingual hiring.</li>
  <li><strong>Datadog Japan</strong>, PMM, demand gen.</li>
  <li><strong>Snowflake Japan</strong>, field marketing, PMM, partner marketing.</li>
</ul>
<h3>Tier 2, Japanese-first but foreigner-friendly</h3>
<ul>
  <li>Rakuten, large in-house marketing org spanning 70+ services.</li>
  <li>LINE Yahoo Japan, growth, partnerships.</li>
  <li>Cyberagent, performance and brand for AbemaTV, gaming, ads.</li>
  <li>Recruit (Indeed parent), multi-brand portfolio.</li>
  <li>Sony Group, global brand, gaming, music marketing.</li>
</ul>
<h3>Luxury and FMCG</h3>
<ul>
  <li>LVMH Japan (LV, Dior, Tiffany, Bulgari), Richemont, Kering, bilingual brand managers.</li>
  <li>P&amp;G Japan (Kobe HQ historically), global brand-management career track.</li>
  <li>Unilever Japan, Coca-Cola Japan, Nestlé Japan, bilingual brand and trade roles.</li>
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

<h2 id="channels">Channel landscape, what's different in Japan</h2>
<ul>
  <li><strong>LINE, the dominant messaging and broadcast channel.</strong> 97M monthly
      active users in Japan. Brand accounts, LINE Ads Platform, LINE Official Accounts
      replace much of what Facebook/Instagram do elsewhere.</li>
  <li><strong>Yahoo! Japan, still 60M MAU.</strong> Yahoo Display Ads and Yahoo Search
      Ads remain meaningful spend channels alongside Google.</li>
  <li><strong>X (formerly Twitter)</strong>, disproportionately influential in Japan vs.
      most countries. Strong organic reach for B2C brands; campaigns often run on X
      first, Instagram second.</li>
  <li><strong>Instagram</strong>, dominant for lifestyle, food, fashion, beauty.</li>
  <li><strong>TikTok</strong>, growing fast for under-25 segments, particularly food,
      retail, and entertainment.</li>
  <li><strong>YouTube</strong>, strong for long-form content; Japanese YouTuber
      ecosystem is large.</li>
  <li><strong>Facebook</strong>, small reach in Japan, mostly older B2B segments.</li>
  <li><strong>Out-of-home</strong>, Tokyo Metro and JR train ads are still meaningful;
      Shibuya street and station ads are common for launches.</li>
  <li><strong>PR &amp; media relations</strong>, Japanese press has strong protocols
      (kisha club, embargo customs). Foreign PMMs typically partner with a local
      bilingual PR agency rather than going direct.</li>
</ul>

<h2 id="entry">How foreigners enter the field</h2>
<ol>
  <li><strong>Foreign-cap SaaS Japan launch teams</strong>, Stripe, Notion, Figma,
      Datadog, Snowflake, HubSpot, Asana, Miro all hire Japan PMMs. These are the
      easiest English-first entry points.</li>
  <li><strong>Bilingual brand management at FMCG / luxury</strong>, P&amp;G, Unilever,
      L'Oréal, LVMH all run global brand-manager grad programmes. Mostly recruit at
      MBA level.</li>
  <li><strong>Mercari / PayPay / SmartNews global team</strong>, apply directly through
      English careers pages; many roles open to overseas applicants.</li>
  <li><strong>Inbound tourism marketing</strong>, JNTO (Japan National Tourism
      Organisation), prefectural tourism boards, Hoshino Resorts, Tokyu, periodically
      hire English-native marketers for overseas-targeting roles.</li>
  <li><strong>Agency side first, in-house later</strong>, Dentsu D, Ogilvy, McCann
      Tokyo, R/GA hire foreign marketers and creatives; agency tenure builds bilingual
      capital before pivoting in-house.</li>
</ol>

<h2 id="pivots">Common pivots</h2>
<ul>
  <li><strong>Performance marketer → growth PM</strong> at Mercari, PayPay,
      Cyberagent.</li>
  <li><strong>Brand manager → general manager / country head</strong> at FMCG and
      luxury (P&amp;G grads in particular).</li>
  <li><strong>PMM → product manager</strong> at SaaS, common because PMM already owns
      a market segment and competitive narrative.</li>
  <li><strong>Content / SEO → in-house demand gen</strong> at B2B SaaS once the SEO
      muscle proves out.</li>
  <li><strong>In-house → founder</strong>, D2C founders in Japan often come from a
      brand-marketing or growth background.</li>
</ul>
<div class="callout">
  Build your career roadmap with the
  <a href="/roadmaps/marketing">Marketing roadmap</a>, five stages from coordinator
  to CMO, with salary bands and Japan-specific notes.
</div>
<!-- ENRICH_V2:marketing-growth -->
<h2 id="channel-2026-shifts">Channel shifts, LINE, TikTok, X in 2026</h2>
<p>The Japan marketing channel landscape continues to shift faster than most foreign
marketers expect. The 2026 updates:</p>
<ul>
  <li><strong>LINE</strong> remains dominant in messaging (97M MAU) and is increasingly
      the primary CRM channel for D2C brands. LINE Ads Platform launched broadcast
      targeting refinements in 2024 that materially improved ROAS for B2C campaigns.
      Cost-per-click is rising as more advertisers enter.</li>
  <li><strong>TikTok</strong>, TikTok Japan crossed 30M MAU in 2024 and continues
      to grow fastest among under-30. Food, retail, beauty, gaming brands
      over-index. CPM is still 30–40% cheaper than Instagram for equivalent
      targeting.</li>
  <li><strong>X (formerly Twitter)</strong>, usage has held up better in Japan than
      globally. Strong for B2B SaaS announcements, gaming launches, retail flash
      sales. CPM has dropped substantially since 2022.</li>
  <li><strong>Instagram</strong>, still core for lifestyle, beauty, food, fashion.
      Reels traction continues but Story remains the dominant placement.</li>
  <li><strong>YouTube</strong>, long-form content drives loyalty for B2B SaaS,
      finance, and gaming brands. Major Japanese YouTubers (HikakinTV, Hajime
      Shacho, Sushi Ramen) command high integration fees.</li>
  <li><strong>Yahoo! Japan</strong>, losing organic search share to Google but
      still 35–40% of search queries. Yahoo Display and Search Ads remain meaningful
      for older demographics.</li>
  <li><strong>Facebook</strong>, declining for under-40; useful only for B2B
      professional services and older B2C audiences.</li>
  <li><strong>Pinterest</strong>, under-indexed but growing; lifestyle/wedding/home
      categories increasing.</li>
  <li><strong>Out-of-home</strong>, Tokyo Metro and JR ad spend grew through 2024–25.
      Shibuya Scramble Crossing screens remain iconic launch venues; daily rates have
      doubled vs 2019.</li>
</ul>

<h2 id="inbound-tourism">Inbound tourism marketing, the biggest growth area</h2>
<p>Inbound tourism is Japan's fastest-growing economic theme, over 33M visitors in
2024, projected 40M+ in 2026. Marketing roles for foreigners are concentrated in:</p>
<ul>
  <li><strong>JNTO (Japan National Tourism Organisation)</strong>, runs overseas
      offices in 26 cities; hires bilingual marketers for specific regional
      campaigns. Bureaucratic but stable; ¥5–8M starting.</li>
  <li><strong>Prefectural / municipal tourism boards</strong>, Kyoto, Hokkaido,
      Okinawa, Nagano, Fukuoka all hire English-native marketers. Pay is lower
      (¥4–7M) but lifestyle benefits exist outside Tokyo.</li>
  <li><strong>Hospitality groups</strong>, Hoshino Resorts (Karuizawa HQ),
      Mitsui Fudosan Hotels, Tokyu Hotels, IHG Japan, Marriott Japan, Park Hyatt
      Tokyo, Aman Tokyo, all run bilingual marketing teams.</li>
  <li><strong>Inbound retail</strong>, Don Quijote, Bicqlo (Bic Camera + Uniqlo),
      Daimaru Matsuzakaya, Takashimaya, luxury and duty-free divisions hire foreign
      marketers for overseas-source campaigns.</li>
  <li><strong>OTA (online travel)</strong>, Booking.com Japan, Expedia Japan,
      Agoda Japan, Klook Japan, bilingual demand gen and PMM roles.</li>
  <li><strong>Restaurant booking / lifestyle</strong>, TableCheck, Pocket Concierge,
      OZmall, increasing in cross-border restaurant booking.</li>
  <li><strong>Inbound tech</strong>, Notion Japan, Stripe (cross-border payments),
      Wise (international remittance), Revolut Japan, all hire marketers with
      international+Japan dual capacity.</li>
</ul>

<h2 id="agencies-vs-inhouse">Agency vs in-house, career trade-offs</h2>
<table>
  <thead><tr><th>Dimension</th><th>Agency (Dentsu, Hakuhodo, R/GA, Ogilvy)</th><th>In-house (Mercari, Stripe Japan)</th></tr></thead>
  <tbody>
    <tr><td>Pay (mid-career)</td><td>¥6–10M</td><td>¥8–14M</td></tr>
    <tr><td>Variety of work</td><td>High, multiple clients, brands, sectors</td>
        <td>Lower, one product, deeper</td></tr>
    <tr><td>Pace</td><td>Fast, deadline-driven</td><td>Sustained, OKR-driven</td></tr>
    <tr><td>Career path</td><td>Account director → group head → MD</td>
        <td>Manager → senior → head/VP</td></tr>
    <tr><td>Foreign marketer hiring</td><td>Dentsu Y&amp;R / Ogilvy / R/GA Tokyo /
        Wieden+Kennedy Tokyo / TBWA</td>
        <td>Mercari, Stripe, Notion, HubSpot, Datadog, PayPay, foreign-cap SaaS</td></tr>
    <tr><td>Work-life balance</td><td>Variable; campaign launches involve long weeks</td>
        <td>Generally better</td></tr>
    <tr><td>Career capital</td><td>Strong portfolio + brand exposure</td>
        <td>Operating depth in one company / sector</td></tr>
  </tbody>
</table>

<h2 id="japan-specific-tools">Japan-specific tools and platforms</h2>
<ul>
  <li><strong>Yappli</strong>, no-code mobile app platform widely used by Japanese
      retailers.</li>
  <li><strong>Cookpad ads</strong>, recipe-platform native advertising; strong for
      food and CPG brands.</li>
  <li><strong>Karte (PLAID)</strong>, Japanese customer-experience platform;
      similar role to Optimizely + Heap.</li>
  <li><strong>Treasure Data</strong>, Japanese-founded CDP, now part of SoftBank;
      widely used for cross-channel data unification.</li>
  <li><strong>Synapse / SmartHR</strong>, Japan-specific HR tech marketing channels.</li>
  <li><strong>LINE Ads Platform</strong>, broadcast targeting platform; LINE
      account integrations are unique to Japan.</li>
  <li><strong>Yahoo! Tag Manager / Yahoo! Display Ads</strong>, for the 35–40% of
      Japan search that goes to Yahoo.</li>
  <li><strong>Hostess / Tabelog reservation ad placements</strong>, restaurant
      industry-specific.</li>
  <li><strong>Mercari Shops Ads</strong>, for D2C and resale brands targeting
      Mercari's 20M+ users.</li>
</ul>

<h2 id="foreign-marketers-success">How foreign marketers actually succeed</h2>
<ul>
  <li><strong>Master one channel deeply first.</strong> Bilingual performance
      marketer with strong Google Ads and Meta capability lands jobs easier than
      generalist "marketing manager".</li>
  <li><strong>Develop cultural literacy.</strong> Read 30 Japanese ad campaigns and
      identify the patterns. Most Western-style assertive copy fails; quieter,
      benefit-led copy lands better.</li>
  <li><strong>Build a bilingual portfolio.</strong> Even if you can't write copy in
      Japanese yourself, brief and approve copy in Japanese. Demonstrate you can
      work with native-speaking partners.</li>
  <li><strong>Network with Tokyo agency creatives.</strong> Tokyo Creative Cluster,
      Wieden+Kennedy Tokyo open studios, ad-industry meetups all hire from
      crossover.</li>
  <li><strong>Cross-border specialisation pays.</strong> Marketers who handle Japan
      ↔ overseas brand campaigns command premium. Hoshino Resorts, P&amp;G Japan
      global brand managers are top of band.</li>
</ul>

""",
    },
    {
        "slug": "finance-accounting",
        "category": 'Role',
        "icon": 'chart-line',
        "title": "Finance &amp; accounting in Japan, the foreigner's guide",
        "summary": ("Tokyo's foreign finance scene runs deep: investment banking, asset management, private equity, "
 'hedge funds, structured finance, corporate finance. The roles, the firms, the pay, and the '
 'unglamorous parts no one warns you about.'),
        "updated": 'May 2026',
        "read_time": '11 min',
        "toc": [   ('market', "Tokyo's foreign finance market"),
    ('buckets', 'Five buckets, banking, AM, PE/HF, corp dev, controllership'),
    ('firms', "Who's hiring, by bucket"),
    ('comp', 'Compensation, by bucket and level'),
    ('japanese', 'Japanese, certifications, and licensing'),
    ('entry', 'How foreigners enter'),
    ('hours', 'Hours and lifestyle, the honest version'),
            ("boj-rate-impact", 'BoJ rate normalisation impact on hiring'),
            ("activist-deal-flow", 'Activist and take-private deal flow 2024–26'),
            ("private-banking-boom", 'Private banking and wealth management boom'),
            ("uscpa-track", 'USCPA → controllership path explained'),
            ("hours-myth-real", 'Hours myth vs reality, by role'),
    ('pivots', 'Common pivots')],
        "body": """
<h2 id="market">Tokyo's foreign finance market</h2>
<p>Tokyo hosts the largest foreign finance community in Asia outside Hong Kong and
Singapore. The Robert Walters 2026 sector report flags banking &amp; financial
services as having the strongest hiring momentum of any sector covered, 67% of
hiring managers planning to add headcount, 5.4% average expected pay increases, and
acute shortages in private banking, M&amp;A advisory, and ESG/sustainability finance.</p>
<p>The structural drivers in 2026:</p>
<ul>
  <li><strong>BoJ normalisation.</strong> The end of negative rates in 2024 reshaped
      JGB and corporate-bond trading desks; new hiring across fixed-income.</li>
  <li><strong>Activist and PE inflows.</strong> Record M&amp;A activity in 2024–25
      (Toshiba, 7-Eleven family take-private discussions, multiple large carve-outs)
      drove M&amp;A advisory hiring.</li>
  <li><strong>Wealth management.</strong> NISA reform and rising household assets
      drove private-banking and wealth-management hiring at the major foreign houses.</li>
  <li><strong>ESG / sustainable finance.</strong> Japanese corporates increasing
      disclosure quality; specialist hiring across banks and asset managers.</li>
</ul>

<h2 id="buckets">Five buckets, banking, AM, PE/HF, corp dev, controllership</h2>
<table>
  <thead><tr><th>Bucket</th><th>What it is</th><th>JP required?</th></tr></thead>
  <tbody>
    <tr><td>Investment banking (M&amp;A, ECM, DCM)</td>
        <td>Advisory and capital-markets execution for corporates</td>
        <td>Bilingual increasingly required; English-only at international-focused desks</td></tr>
    <tr><td>Asset / wealth management</td>
        <td>Discretionary investment for institutional and HNW clients</td>
        <td>JP required for distribution; portfolio management roles often English</td></tr>
    <tr><td>Private equity / hedge funds</td>
        <td>Direct investing across buyouts, growth, hedge strategies</td>
        <td>Senior roles need fluent JP; analyst roles often English-OK</td></tr>
    <tr><td>Corporate development / strategy finance</td>
        <td>In-house at Japanese / foreign corporates, M&amp;A, FP&amp;A, strategy</td>
        <td>Depends on company; bilingual valued at Japanese corporates</td></tr>
    <tr><td>Controllership / accounting / audit</td>
        <td>Statutory reporting, tax, internal controls</td>
        <td>USCPA + N2+ JP unlocks the top of the band</td></tr>
  </tbody>
</table>

<h2 id="firms">Who's hiring, by bucket</h2>
<h3>Investment banking</h3>
<ul>
  <li><strong>Bulge brackets in Tokyo</strong>, Goldman Sachs Japan, Morgan Stanley
      MUFG (JV), JPMorgan Securities Japan, BofA Securities Japan, Citi Japan, UBS Japan,
      Credit Suisse Japan (UBS-merged), Deutsche Bank Tokyo, Barclays Japan, BNP
      Paribas Securities (Japan).</li>
  <li><strong>Boutiques</strong>, Lazard Japan, Rothschild Japan, Houlihan Lokey
      Japan, Centerview, Evercore (small Tokyo presence), Moelis.</li>
  <li><strong>Japanese majors</strong>, Nomura, Daiwa Securities, SMBC Nikko, Mizuho
      Securities, MUFG Securities. Hire bilingual foreigners for cross-border deals.</li>
</ul>
<h3>Asset / wealth management</h3>
<ul>
  <li><strong>Foreign houses</strong>, BlackRock Japan, Fidelity Japan, JPMorgan
      Asset Management, Wellington, Goldman Sachs Asset Management, Schroders,
      BNP Paribas AM, Capital Group, T. Rowe Price.</li>
  <li><strong>Private banks</strong>, UBS Japan WM, Goldman Sachs PWM, Morgan
      Stanley WM, JPMorgan Private Bank, Citi Private Bank.</li>
  <li><strong>Japanese majors</strong>, Nomura AM, Daiwa AM, Sumitomo Mitsui DS AM,
      Mitsubishi UFJ AM, Asset Management One.</li>
</ul>
<h3>Private equity &amp; hedge funds</h3>
<ul>
  <li><strong>Global PE Tokyo offices</strong>, KKR Japan, Bain Capital Japan,
      Carlyle Japan, Blackstone Japan, Apollo Japan, EQT Japan, CVC Asia Tokyo, TPG
      Capital Japan, Permira, PAG.</li>
  <li><strong>Japan-focused funds</strong>, J-Star, Advantage Partners, Polaris
      Capital, Integral, Unison Capital.</li>
  <li><strong>Hedge funds with Tokyo presence</strong>, Citadel, Millennium, Point72,
      Balyasny, Bridgewater, Capula, Brevan Howard, Coatue.</li>
</ul>
<h3>Corporate development / FP&amp;A</h3>
<ul>
  <li><strong>Foreign corporates' Japan arms</strong>, Stripe, Amazon, Google, Apple,
      Microsoft, Salesforce all run FP&amp;A and corp dev in Tokyo.</li>
  <li><strong>Japanese conglomerates with cross-border M&amp;A</strong>, SoftBank
      Group, Hitachi, Sony Group, Nidec, Asahi Group, Suntory, actively hire bilingual
      foreigners into strategy and corp dev.</li>
</ul>
<h3>Controllership / accounting / audit</h3>
<ul>
  <li><strong>Big Four Japan</strong>, KPMG AZSA, Deloitte Touche Tohmatsu, EY ShinNihon,
      PwC Aarata.</li>
  <li><strong>Industry controllers</strong>, most large foreign-cap firms (Stripe,
      Salesforce, Amazon Japan, etc.) hire bilingual USCPAs into controllership.</li>
</ul>

<h2 id="comp">Compensation, by bucket and level</h2>
<table>
  <thead><tr><th>Role</th><th>Year 1</th><th>Year 3–5</th><th>VP / 5–10y</th></tr></thead>
  <tbody>
    <tr><td>IB analyst (bulge bracket)</td><td>¥12–15M total</td><td>¥18–25M</td><td>VP ¥25–40M+ inc bonus</td></tr>
    <tr><td>IB analyst (Japanese major)</td><td>¥8–11M</td><td>¥13–18M</td><td>¥20–30M</td></tr>
    <tr><td>Sales &amp; trading</td><td>¥12–15M</td><td>¥18–30M</td><td>¥30–60M+ heavily variable</td></tr>
    <tr><td>Portfolio manager (AM)</td><td>¥10–14M</td><td>¥18–28M</td><td>¥30–60M+</td></tr>
    <tr><td>Wealth / private bank RM</td><td>¥10–13M</td><td>¥15–22M</td><td>¥25–50M+ (book-dependent)</td></tr>
    <tr><td>PE associate</td><td>¥15–18M base + carry</td><td>¥20–30M + carry</td><td>VP ¥35–60M+ + carry</td></tr>
    <tr><td>Hedge fund analyst</td><td>¥15–22M</td><td>¥25–45M</td><td>PM ¥50M+ (P&amp;L-driven)</td></tr>
    <tr><td>Corp dev manager (foreign-cap)</td><td>¥10–13M</td><td>¥14–20M</td><td>Senior ¥22–30M+</td></tr>
    <tr><td>Controller (foreign-cap)</td><td>¥7–10M</td><td>¥11–16M</td><td>¥18–28M</td></tr>
    <tr><td>Big Four senior</td><td>¥5.5–7M</td><td>¥8–12M (manager)</td><td>Sr Mgr ¥12–18M, Partner ¥20–40M+</td></tr>
  </tbody>
</table>
<p>The 2024–25 cycle saw 8–15% base raises at most bulge brackets for VP and above,
plus signing bonuses of ¥3–10M for cross-firm moves at the right desks. Carry-bearing
PE roles materially outpace base+bonus comp on a 5–7-year view.</p>

<h2 id="japanese">Japanese, certifications, and licensing</h2>
<ul>
  <li><strong>JLPT N1 / N2.</strong> N1 is preferred for client-facing roles in
      banking (M&amp;A, sales, wealth); N2 is the practical floor at bulge brackets.
      Pure quantitative trading and global execution desks tolerate N3 or English-only.</li>
  <li><strong>CFA.</strong> Highly recognized in Japanese asset management; required
      for most portfolio-management progressions.</li>
  <li><strong>USCPA / JP CPA.</strong> USCPA opens controllership at foreign-cap firms.
      Japan CPA (kōnin kaikeishi) is rare for foreigners but unlocks practising-
      accountant and Big Four partner paths.</li>
  <li><strong>FSA registration.</strong> Sales/trading roles require registration with
      the Financial Services Agency (Type 1 / Type 2). Employer sponsors the exam.</li>
  <li><strong>Securities Sales Representative (証券外務員)</strong>, Class-I / Class-II
      registrations required for client-facing securities work; employer-sponsored.</li>
</ul>

<h2 id="entry">How foreigners enter</h2>
<ol>
  <li><strong>Graduate analyst programmes.</strong> Bulge brackets (GS, MS, JPM) and
      Big Four run Tokyo graduate intakes. Recruiting starts 18 months ahead via
      campus channels in the US/UK/HK/Singapore.</li>
  <li><strong>Lateral hire from an Asia hub.</strong> Many foreigners transfer from
      Hong Kong, Singapore, or London. Singapore-to-Tokyo lateral moves are common at
      senior associate / VP level.</li>
  <li><strong>Foreign-cap controllership.</strong> Most modern foreign firms (Stripe,
      Snowflake, Datadog, Salesforce) hire bilingual USCPAs directly into Japan
      controller / FP&amp;A roles.</li>
  <li><strong>Senior bilingual hire.</strong> Specialist recruiters (Robert Walters,
      Robert Half, Pro-Recruitment, Hays, Michael Page, Morgan McKinley) place
      bilingual MD-level moves between Japanese and foreign houses.</li>
</ol>

<h2 id="hours">Hours and lifestyle, the honest version</h2>
<ul>
  <li><strong>IB &amp; PE analyst</strong>, 70–95 hours/week is normal in deal mode.
      Tokyo is no easier than NYC or LDN on hours.</li>
  <li><strong>Sales &amp; trading</strong>, market hours (8am–6pm JST core) plus
      pre-open work and post-close summaries. Weekends largely free.</li>
  <li><strong>Asset management portfolio teams</strong>, 50–60 hours, depending on
      strategy. More civilised than IB or HF.</li>
  <li><strong>Hedge funds</strong>, bimodal: pod shops are 60–80 hour weeks with
      heavy P&amp;L pressure; some macro funds are calmer.</li>
  <li><strong>Big Four audit</strong>, busy season (Q1) is 70–80 hours; off-season
      40–55 hours.</li>
  <li><strong>Corporate FP&amp;A &amp; controllership</strong>, 45–55 hours typically,
      worse at month-end and quarter-end close.</li>
</ul>

<h2 id="pivots">Common pivots</h2>
<ul>
  <li><strong>IB → PE</strong>, the classic post-analyst move; happens after year 2.</li>
  <li><strong>IB → corporate dev</strong> at Hitachi / SoftBank / Sony, better hours,
      comparable comp at senior level.</li>
  <li><strong>Big Four → industry controller</strong> at a foreign-cap, pay step-up,
      hours improve.</li>
  <li><strong>Asset management → wealth management</strong>, going closer to clients
      at high-net-worth practice.</li>
  <li><strong>Finance → startup operator</strong>, CFO or VP Finance at a Japanese
      Series B/C startup.</li>
</ul>
<div class="callout">
  Build your career roadmap with the
  <a href="/roadmaps/finance-accounting">Finance &amp; accounting roadmap</a>, six
  stages from analyst to MD, with salary bands and Japan-specific notes.
</div>
<!-- ENRICH_V2:finance-accounting -->
<h2 id="boj-rate-impact">BoJ rate normalisation impact on hiring</h2>
<p>The Bank of Japan ended the negative interest rate policy in March 2024, the
first rate-hike cycle in 17 years. The cumulative impact on Tokyo finance hiring
through 2025–26:</p>
<ul>
  <li><strong>Fixed-income desks at bulge brackets are scaling.</strong> The JGB
      yield curve is suddenly tradeable again; Goldman, Morgan Stanley, JPMorgan,
      Nomura, Daiwa all expanded their JGB and corporate-bond trading teams 2024–25.</li>
  <li><strong>Japanese mega-banks (MUFG, SMBC, Mizuho) have improved net interest
      margins</strong>, leading to capital-deployment hiring across syndicated
      lending, structured finance, and specialty credit.</li>
  <li><strong>Reinvestment of life-insurance balance sheets.</strong> Nippon Life,
      Dai-ichi Life, Sumitomo Life all reallocated significant book value from
      foreign bonds to JGB in 2024–25. Asset-management talent in JGB is in
      demand.</li>
  <li><strong>Foreign asset managers</strong> have ramped Tokyo presence, BlackRock,
      Fidelity, JPMAM, Wellington all expanded portfolio-management teams
      2024–25.</li>
  <li><strong>Yen carry trade unwind dynamics</strong> have shifted FX trading desk
      composition, more hedge funds opening Tokyo macro/credit pods.</li>
</ul>

<h2 id="activist-deal-flow">Activist and take-private deal flow 2024–26</h2>
<p>Japan saw record M&amp;A activity in 2024–25, driven by:</p>
<ul>
  <li><strong>Activist investor pressure.</strong> Foreign activist funds (Elliott,
      ValueAct, Oasis Management, Asset Value Investors, 3D Investment Partners,
      Strategic Capital) increasing pressure on Japanese corporates for restructuring,
      buybacks, and divestitures.</li>
  <li><strong>Take-private trends.</strong> Toshiba (¥2T deal, 2023), Outsourcing
      Inc, multiple mid-cap deals through 2025. PE buyers (KKR, Bain Capital,
      Carlyle, Permira, Blackstone) increased Japan deployment.</li>
  <li><strong>Tokyo Stock Exchange reform.</strong> JPX revised the listing
      requirements in 2023–24, pressuring companies trading below book value to
      improve capital efficiency. Many responded with buybacks, spinoffs, or PE
      sales.</li>
  <li><strong>Corporate carve-outs.</strong> Sōgō shōsha (Mitsubishi, Mitsui,
      Itochu), conglomerates (Hitachi, Sony Group, Renesas) accelerating divestiture
      of non-core businesses.</li>
</ul>
<p>What this means for hiring:</p>
<ul>
  <li>M&amp;A advisory teams at bulge brackets are at all-time deal volumes; VP
      and director hiring competitive.</li>
  <li>PE associates with Japan execution experience command material premium.
      KKR, Bain Capital, Carlyle, Blackstone Tokyo all hired aggressively in 2024–25.</li>
  <li>Cross-border M&amp;A (Japanese acquirer / foreign target) skill-set is
      premium-priced; bilingual VP-level bankers see signing bonuses of ¥5–15M.</li>
</ul>

<h2 id="private-banking-boom">Private banking and wealth management boom</h2>
<p>Japan household financial assets reached ¥2,200 trillion in 2024, the largest
pool of investable household wealth in Asia. Private banking and wealth management
are growing fastest in:</p>
<ul>
  <li><strong>NISA reform (new NISA from 2024)</strong>, annual contribution
      cap raised to ¥3.6M; lifetime cap to ¥18M. Massively expanded mass-affluent
      investment market.</li>
  <li><strong>Foreign private banks expanding HK / Singapore overflow into Tokyo.</strong>
      UBS, Goldman Sachs PWM, Morgan Stanley WM, Citi Private Bank, JPMorgan Private
      Bank all expanded bilingual RM hiring 2024–25.</li>
  <li><strong>Family offices</strong>, number of single-family offices in Japan
      grew ~30% 2022–25; many recruit from foreign private banks.</li>
  <li><strong>Wealth tech / robo-advisors</strong>, Wealthnavi, ONE Tap BUY (now
      PayPay Securities), THEO. Most are domestic-focused but expanding international
      reach.</li>
</ul>

<h2 id="uscpa-track">USCPA → controllership path explained</h2>
<p>The USCPA → Japan controller path is one of the most reliable foreigner career
escalators in finance. The realistic timeline:</p>
<ol>
  <li><strong>Pass USCPA exams</strong> while in your home country (US/Asia). 4
      exams; passing all 4 typically takes 1–2 years.</li>
  <li><strong>Year 1–2 in Japan: Big Four senior/manager.</strong> KPMG AZSA,
      Deloitte Touche Tohmatsu, EY ShinNihon, PwC Aarata all hire USCPAs into audit
      or transactions. ¥5.5–8M starting.</li>
  <li><strong>Year 3–4: Switch to foreign-cap industry controller.</strong> Stripe,
      Salesforce, Snowflake, Datadog, ServiceNow, Notion, Workday Japan all hire
      bilingual USCPAs at the controller / FP&amp;A level. ¥9–13M total comp.</li>
  <li><strong>Year 5–8: Senior controller / finance director.</strong> Bigger
      scope, equity grants kick in. ¥14–22M total.</li>
  <li><strong>Year 8+: VP Finance / Japan CFO.</strong> Manage 5–15 person finance
      org. ¥22–35M+ with significant equity.</li>
</ol>
<p>JLPT N2 unlocks the higher tier (interaction with Japanese vendors, banks, tax
auditors). USCPA + N2 is the gold-standard combination.</p>

<h2 id="hours-myth-real">Hours myth vs reality, by role</h2>
<table>
  <thead><tr><th>Role</th><th>Reputation</th><th>2026 reality</th></tr></thead>
  <tbody>
    <tr><td>IB analyst (M&amp;A)</td><td>80+ hours/week</td>
        <td>70–95 hrs in deal mode; 50–60 between. Worse than US/UK due to weekend
        culture.</td></tr>
    <tr><td>IB analyst (ECM/DCM)</td><td>70 hours/week</td>
        <td>55–75 hrs typically; better lifestyle than M&amp;A.</td></tr>
    <tr><td>Sales &amp; trading</td><td>Fixed</td>
        <td>Market hours 7:30am–6pm + 1–2 hrs pre/post. Weekends usually free.</td></tr>
    <tr><td>Asset management PM</td><td>Civilised</td>
        <td>50–60 hours/week. Pension consulting bursts.</td></tr>
    <tr><td>Hedge fund analyst (pod)</td><td>Long</td>
        <td>60–80 hrs; performance pressure intense.</td></tr>
    <tr><td>PE associate</td><td>Long but lumpy</td>
        <td>70–100 hrs in deal mode; 50–60 between; carry over multi-year.</td></tr>
    <tr><td>Big Four audit</td><td>Heavy busy season</td>
        <td>70–80 hrs Q1; 40–55 hrs off-season.</td></tr>
    <tr><td>Industry controller (foreign-cap)</td><td>Mid</td>
        <td>45–55 hrs typical; worse at month-end / quarter-end close (60–70).</td></tr>
    <tr><td>Industry FP&amp;A</td><td>Variable</td>
        <td>45–55 hrs typical; budgeting cycle (October–December) is the crunch.</td></tr>
    <tr><td>Country CFO (Japan)</td><td>Variable</td>
        <td>50–65 hrs; some travel; board reporting cycle</td></tr>
  </tbody>
</table>

""",
    },
    {
        "slug": "sales-business-development",
        "category": 'Role',
        "icon": 'briefcase',
        "title": "Sales &amp; business development in Japan, the foreigner's guide",
        "summary": ('Tech sales, enterprise SaaS sales, partnerships, and BD in Japan, the highest-leverage path for '
 'bilingual foreigners outside engineering. Who pays the most, what the OTE structures look like, '
 'and how to break in.'),
        "updated": 'May 2026',
        "read_time": '10 min',
        "toc": [   ('market', 'The 2026 sales market'),
    ('buckets', 'Sales buckets, SDR, AE, AM, BD, partnerships'),
    ('companies', "Who's hiring"),
    ('comp', 'Compensation and OTE structures'),
    ('japanese', 'Japanese language reality'),
    ('entry', 'How foreigners get in'),
    ('culture', "Japan B2B sales culture, what's different"),
            ("2024-2026-wave", '2024–26 SaaS Japan expansion wave'),
            ("ote-structures", 'OTE structures explained'),
            ("ramp-period", 'Ramp period and quota timing'),
            ("partner-ecosystem", 'Partner ecosystem, SIs and integrators'),
            ("comp-negotiation", 'Negotiating sales comp at offer'),
    ('pivots', 'Common pivots')],
        "body": """
<h2 id="market">The 2026 sales market</h2>
<p>Foreign-cap SaaS expansion through 2023–25 created the largest B2B sales hiring
wave Tokyo has seen. Stripe, Notion, Datadog, Snowflake, HubSpot, Salesforce,
ServiceNow, MongoDB, Asana, Atlassian, Miro, Confluent, Twilio, Anthropic, all
either established Japan sales teams or materially scaled them in this window.</p>
<p>The Robert Walters 2026 sector report flags <em>Enterprise Account Executive
(bilingual)</em>, <em>Partner / Alliance Manager</em>, and <em>Customer Success
Manager (enterprise)</em> as top-five demand roles in technology &amp; online, with 6–8% expected pay increases for job-changers and aggressive sign-on bonuses
at the high end.</p>

<h2 id="buckets">Sales buckets, SDR, AE, AM, BD, partnerships</h2>
<table>
  <thead><tr><th>Bucket</th><th>What it does</th><th>Bilingual required?</th></tr></thead>
  <tbody>
    <tr><td>SDR / BDR (sales development)</td>
        <td>Outbound prospecting; book qualified meetings for AEs</td>
        <td>Bilingual essential for outbound to Japanese targets</td></tr>
    <tr><td>Account Executive (AE)</td>
        <td>Carry new-business quota; close deals</td>
        <td>Bilingual essential outside SMB English-only segments</td></tr>
    <tr><td>Account Manager (AM) / CSM</td>
        <td>Expand and retain existing customers</td>
        <td>Bilingual essential for Japanese customer base</td></tr>
    <tr><td>Solutions Engineer</td>
        <td>Technical pre-sales partner to AE</td>
        <td>Technical English fine for most foreign-cap; bilingual preferred</td></tr>
    <tr><td>Partner / channel sales</td>
        <td>Manage SI partners (Accenture, NTT Data, IBM Japan, SCSK)</td>
        <td>Bilingual essential</td></tr>
    <tr><td>BD / strategic partnerships</td>
        <td>Multi-party deals, cross-co integrations</td>
        <td>Bilingual essential at senior level</td></tr>
  </tbody>
</table>

<h2 id="companies">Who's hiring</h2>
<h3>Foreign-cap SaaS (English-friendly globally, bilingual locally)</h3>
<ul>
  <li>Salesforce Japan, ServiceNow Japan, Microsoft Japan, Google Cloud Japan, AWS Japan.</li>
  <li>Stripe Tokyo, Snowflake Japan, Datadog Japan, MongoDB Japan, Confluent Japan,
      Cloudflare Japan.</li>
  <li>Notion Japan, Figma Japan, Asana Japan, Atlassian Japan, Miro Japan, Smartsheet Japan.</li>
  <li>HubSpot Japan, Zendesk Japan, Twilio Japan, Intercom Japan.</li>
  <li>Adobe Japan, Workday Japan, SAP Japan, Oracle Japan.</li>
</ul>
<h3>Japanese SaaS</h3>
<ul>
  <li>Mercari (B2B Mercari Shops &amp; payments), PayPay (merchant sales), freee,
      Money Forward, Sansan, Cybozu, BASE, Smartcamp, KARTE (Plaid), Hitobito,
      Studist, Caddi.</li>
</ul>
<h3>Adtech / mar-tech</h3>
<ul>
  <li>The Trade Desk Japan, Criteo Japan, Treasure Data, Braze Japan, Iterable.</li>
</ul>
<h3>Enterprise / industrial</h3>
<ul>
  <li>NVIDIA Japan, Splunk Japan, Palo Alto Networks Japan, CrowdStrike Japan,
      Cisco Japan, Dell EMC Japan, NetApp Japan.</li>
</ul>

<h2 id="comp">Compensation and OTE structures</h2>
<table>
  <thead><tr><th>Role</th><th>Base (¥M)</th><th>OTE (¥M)</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>SDR / BDR</td><td>5–7</td><td>6.5–9</td><td>40–60 quota %, mostly inbound at top tier</td></tr>
    <tr><td>SMB / mid-market AE</td><td>8–11</td><td>13–18</td><td>50/50 base/var common</td></tr>
    <tr><td>Enterprise AE (foreign-cap)</td><td>11–16</td><td>22–35</td><td>50/50; can spike to ¥45M+ with kickers</td></tr>
    <tr><td>Strategic / named-account AE</td><td>15–20</td><td>35–60+</td><td>Top performers ¥80M+ with accelerators</td></tr>
    <tr><td>Solutions engineer (mid)</td><td>10–13</td><td>11.5–15</td><td>15–25% variable</td></tr>
    <tr><td>Senior SE / staff SE</td><td>14–18</td><td>16–22</td><td>15–25% variable</td></tr>
    <tr><td>CSM (mid)</td><td>8–11</td><td>9–13</td><td>10–20% variable</td></tr>
    <tr><td>Senior CSM / enterprise CSM</td><td>11–15</td><td>13–18</td><td>Retention-tied variable</td></tr>
    <tr><td>Partner manager</td><td>10–14</td><td>13–19</td><td>30% variable typical</td></tr>
    <tr><td>Sales manager (1st-line)</td><td>14–19</td><td>22–32</td><td>50/50 OTE</td></tr>
    <tr><td>Director / RVP</td><td>20–28</td><td>35–55+</td><td>50/50 OTE + equity</td></tr>
    <tr><td>Country GM / VP Japan</td><td>25–40</td><td>50–100+</td><td>Heavy equity + bonus</td></tr>
  </tbody>
</table>

<h2 id="japanese">Japanese language reality</h2>
<ul>
  <li><strong>Closing motion</strong> happens in Japanese for ~95% of foreign-cap deals
      in Japan. Customer procurement, legal, and IT teams operate in Japanese.</li>
  <li><strong>Executive-level cross-cultural sales</strong> is the highest-leverage
      profile, bilingual AEs who can run an exec meeting in Japanese and translate
      back to US/EU HQ command top of band.</li>
  <li><strong>English-only segments</strong> exist: APAC HQ accounts, foreign-cap
      Japan offices of multinationals, gaming. These are smaller pools.</li>
  <li><strong>JLPT N1</strong> is the practical floor for enterprise AE outside the
      English-only segments. N2 is workable for SMB/mid-market.</li>
</ul>

<h2 id="entry">How foreigners get in</h2>
<ol>
  <li><strong>SaaS sales academy.</strong> Salesforce, HubSpot, Datadog, and a handful
      of others run formal entry-level BDR / SDR programmes that hire bilingual
      foreigners directly. 6–12 month bench-to-quota path.</li>
  <li><strong>APAC HQ inbound transfer.</strong> Many foreign-cap firms hire AEs in
      Singapore or Sydney first, then transfer high performers to a Japan AE seat.</li>
  <li><strong>Bilingual SE → AE</strong>, solutions engineers who develop selling
      muscle can convert to AE after 2–3 years at the same company.</li>
  <li><strong>Lateral from a Japanese / EU competitor.</strong> Once you have one
      Japan sales seat under your belt, recruiter activity (Robert Walters, Computer
      Futures, Robert Half) becomes the dominant inbound path.</li>
  <li><strong>BD / partnerships first.</strong> Foreigners with consulting or BD
      backgrounds sometimes enter partner-management seats and convert to direct
      sales later.</li>
</ol>

<h2 id="culture">Japan B2B sales culture, what's different</h2>
<ul>
  <li><strong>Long cycles, multi-stakeholder.</strong> Enterprise SaaS cycles in Japan
      run 6–18 months (vs. 3–9 months US). Decision-making is consensus-driven
      (<em>nemawashi</em>); skipping middle layers backfires.</li>
  <li><strong>Procurement is rigorous.</strong> Japanese procurement (チョウタツ /
      購買) frequently runs structured RFPs with mandatory clarification rounds; treat
      it as a separate workstream from the business buyer.</li>
  <li><strong>Pricing transparency.</strong> Public price lists carry weight; volume
      discounts must be defensible. Bespoke pricing is fine but requires written
      justification.</li>
  <li><strong>Hanko and paperwork.</strong> Some procurement processes still require
      sealed paper contracts. eSignature adoption growing but uneven.</li>
  <li><strong>Trust before transaction.</strong> Multiple face-to-face meetings before
      a major contract is normal; lunches and dinners are standard.</li>
  <li><strong>Reference-driven.</strong> Japanese buyers ask for case studies of
      <em>Japanese</em> customers. Building a domestic case-study bank is critical.</li>
</ul>

<h2 id="pivots">Common pivots</h2>
<ul>
  <li><strong>SDR → AE</strong>, universal first promotion; 12–18 months.</li>
  <li><strong>AE → enterprise AE → strategic AE</strong>, comp ladder up to ¥50M+.</li>
  <li><strong>AE → sales manager</strong>, typically requires 2 years over-quota.</li>
  <li><strong>AE → product / PMM</strong>, works at SaaS where deep customer empathy
      transfers.</li>
  <li><strong>Sales manager → country GM</strong>, multi-year path; equity matters
      more than base.</li>
  <li><strong>Senior AE → founder</strong>, common in Japan B2B SaaS; Sansan, freee,
      KARTE founders all came from sales-adjacent backgrounds.</li>
</ul>
<div class="callout">
  Build your career roadmap with the
  <a href="/roadmaps/sales-business-development">Sales &amp; BD roadmap</a>, six
  stages from SDR to country GM, with OTE bands and Japan-specific notes.
</div>
<!-- ENRICH_V2:sales-business-development -->
<h2 id="2024-2026-wave">2024–26 SaaS Japan expansion wave</h2>
<p>Foreign-cap SaaS expansion into Japan through 2024–26 has been the largest wave
since 2018–19. Notable expansions:</p>
<ul>
  <li><strong>Stripe Tokyo</strong>, opened proper office in 2023; ramping sales and
      product-marketing hiring aggressively. Reportedly among the fastest-growing
      foreign-cap entrants in 2024–26.</li>
  <li><strong>Datadog Japan</strong>, JP Tower office in Marunouchi; ramped sales,
      SE, CSM in 2024.</li>
  <li><strong>Snowflake Japan</strong>, expanded enterprise AE and partner-channel
      hiring in 2024–25.</li>
  <li><strong>MongoDB Japan</strong>, expanded both direct AE and channel teams.</li>
  <li><strong>Confluent Japan</strong>, Kafka commercial team; bilingual AE
      hiring.</li>
  <li><strong>Notion Japan</strong>, community-led growth motion; expanded sales
      and partner-marketing.</li>
  <li><strong>HubSpot Japan</strong>, heavy bilingual AE and demand-gen hiring.</li>
  <li><strong>Anthropic Tokyo</strong>, opened Tokyo presence in 2025; sales and
      partnerships hiring.</li>
  <li><strong>Smartsheet, Miro, Asana Japan</strong>, all expanded sales teams.</li>
  <li><strong>Cloudflare Japan</strong>, expanded enterprise sales and SE.</li>
  <li><strong>CrowdStrike Japan, Palo Alto Networks Japan, Splunk Japan</strong>, security expansion continues post-2024 incidents.</li>
</ul>

<h2 id="ote-structures">OTE structures explained</h2>
<p>OTE (On-Target Earnings) structures at foreign-cap SaaS in Tokyo:</p>
<table>
  <thead><tr><th>Component</th><th>Typical %</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>Base salary</td><td>50% of OTE</td>
        <td>Guaranteed; paid monthly. Higher in some markets (60–70%) but 50/50 is
        the SaaS norm.</td></tr>
    <tr><td>Variable (commission)</td><td>50% of OTE</td>
        <td>Earned at 100% quota attainment. Below 100% pro-rated; above 100%
        accelerated.</td></tr>
    <tr><td>Accelerators (above 100%)</td><td>1.5× – 3× multiplier</td>
        <td>Top performers can exceed OTE by 30–100%.</td></tr>
    <tr><td>SPIFs (special incentives)</td><td>Variable</td>
        <td>Time-bound bonus on specific product / segment / accounts.</td></tr>
    <tr><td>President's Club</td><td>Trip + bonus</td>
        <td>Top 10–20% of sellers; 4–7 day trip + cash bonus.</td></tr>
    <tr><td>Signing bonus</td><td>10–30% of base</td>
        <td>Common at senior AE+ levels; vested over 12–24 months.</td></tr>
    <tr><td>Equity / RSU</td><td>Variable</td>
        <td>At public-company FAANG-like SaaS, RSU grants are material. Pre-IPO
        startups offer options instead.</td></tr>
  </tbody>
</table>

<h2 id="ramp-period">Ramp period and quota timing</h2>
<p>Practical notes on the first year as a Tokyo AE:</p>
<ul>
  <li><strong>Most foreign-cap SaaS run a 6-month ramp period.</strong> During ramp,
      quota is reduced (typically 25% in Q1, 50% in Q2, 75% Q3, 100% Q4 of first year).</li>
  <li><strong>Signing bonus</strong> exists partly because Q1 commissions are limited
      during ramp.</li>
  <li><strong>Territory assignment matters more than skill at year 1.</strong> Push
      for clarity on accounts and patch coverage during offer negotiation.</li>
  <li><strong>Quota credit on co-sold deals</strong> can be ambiguous; clarify in
      writing.</li>
  <li><strong>SI partner commissions</strong>, at companies that channel through SIs
      (Salesforce, ServiceNow), some AE quota gets credited against partner-led
      deals; ask about the split.</li>
</ul>

<h2 id="partner-ecosystem">Partner ecosystem, SIs and integrators</h2>
<p>Japan's B2B SaaS market is partner-channel-driven to an extent foreigners often
underestimate. The major Japanese SIs (System Integrators) sit between SaaS vendors
and end customers, especially at enterprise:</p>
<ul>
  <li><strong>Accenture Japan</strong>, largest international SI; partners with most
      major SaaS vendors.</li>
  <li><strong>NTT Data</strong>, Japan's biggest SI; partner across Salesforce,
      ServiceNow, AWS.</li>
  <li><strong>NRI (Nomura Research Institute)</strong>, major Japan SI; financial
      services focus.</li>
  <li><strong>NSI (Nikkei Systems / Otoyama-grouped SI), SCSK, ITOCHU Techno-
      Solutions (CTC), Hitachi Systems</strong>, large Japanese SIs.</li>
  <li><strong>NEC, Fujitsu, NTT Com</strong>, historic Japanese systems vendors,
      now also distribution channels for SaaS.</li>
  <li><strong>Specialist SIs:</strong> Bee Communication (Salesforce), Cloudbees
      Japan (DevOps), Server Works (AWS), Kasai Group (ERP).</li>
</ul>
<p>Partner-channel roles at SaaS vendors, Partner Manager, Alliance Manager, pay
similarly to AE roles (¥10–18M total) and offer slower-burn but more predictable
careers.</p>

<h2 id="comp-negotiation">Negotiating sales comp at offer</h2>
<ul>
  <li><strong>Negotiate base, not OTE.</strong> Base compounds; variable doesn't.
      Push for ¥1–2M more base if possible.</li>
  <li><strong>Ramp quota</strong>, push for longer / more generous ramp than the
      standard offer.</li>
  <li><strong>Signing bonus</strong>, universally negotiable. At senior AE+ levels,
      ask for ¥2–5M signing.</li>
  <li><strong>Territory clarity</strong>, get the account list in writing; it's
      worth more than the comp.</li>
  <li><strong>President's Club eligibility</strong> in year 1, some companies require
      full-year tenure to qualify; check whether ramp-month quotas count.</li>
  <li><strong>Equity grant size</strong>, at public-company SaaS, RSU grant value
      is negotiable up to 30%. Ask for the grant in JPY-fixed amount rather than
      shares to insulate against USD-JPY moves.</li>
  <li><strong>Sales kickoff travel</strong>, confirm that annual SKO (typically in
      US headquarters city) is fully covered including overseas allowance.</li>
</ul>

""",
    },
]


def get_resource(slug: str) -> dict | None:
    return next((r for r in RESOURCES if r["slug"] == slug), None)


def get_guide(slug: str) -> dict | None:
    return next((g for g in GUIDES if g["slug"] == slug), None)


# ---------------------------------------------------------------------------
# Success stories, composite profiles of foreigners hired in Japan.
# The names are illustrative; numbers and trajectories are representative
# of patterns we see in user testimonials and TokyoDev's annual survey.
# ---------------------------------------------------------------------------

STORIES: list[dict] = [
    {
        "slug": "alex-engineer-from-abroad",
        "avatar": "cpu",
        "name": "Alex M.",
        "role": "Senior Backend Engineer @ Mercari",
        "headline": "Got hired from Berlin, started in Tokyo 3 months later, ¥11M base.",
        "summary": "How a German backend engineer with no Japanese landed a senior role at a Tokyo product company without ever flying out for interviews.",
        "tags": ["Software Engineering", "Visa sponsorship", "English-only"],
        "from_location": "Berlin, Germany",
        "current_role": "Senior Backend Engineer",
        "current_company": "Mercari",
        "japanese_level": "None at time of hire (now N4)",
        "background": """
Alex spent 7 years as a backend engineer in Berlin, mostly working on payments
infrastructure at a fintech scale-up. By 2025 he was tired of the European tech ecosystem
and wanted a market with bigger problems but lower competitive intensity than the US. Japan
had been on his shortlist for a while.""",
        "process": """
He targeted four companies he'd already used as a consumer (Mercari, SmartNews, PayPay,
Indeed Tokyo). Applied directly through their careers pages, no recruiters, no agencies.
Total timeline: first application sent in early January, first offer arrived in early March,
moved to Tokyo in May.

Interview process: 1 recruiter call → 1 technical screen (live coding, in English) →
2 on-site interviews (system design + behavioral, done as video calls). All conversations
happened in English. He never flew out for interviews, Mercari does final rounds remotely
for overseas candidates.""",
        "outcome": """
Final offer: ¥11M base salary + ¥2M signing bonus + RSU package. Mercari sponsored
both the working visa (Engineer/Specialist) and the relocation logistics: shipping container,
30 days of corporate housing, 3 weeks of in-person Japanese lessons.""",
        "lessons": [
            "Apply directly to companies. Recruiters skew toward Japanese-speaking candidates.",
            "Have a clear theme to your background. 'Payments at scale' opened more doors than 'general backend'.",
            "Don't worry about Japanese for the initial application, the companies that hire remotely either don't need it, or will pay for lessons after you arrive.",
            "Negotiate hard on the signing bonus. Base salaries are sticky at Japanese companies; one-off cash is easier to move.",
        ],
    },
    {
        "slug": "priya-design-london-to-tokyo",
        "avatar": "pencil",
        "name": "Priya R.",
        "role": "Product Designer @ LINE Yahoo Japan",
        "headline": "Used JLPT N2 plus a strong portfolio to compete head-on with Japanese designers.",
        "summary": "Studied Japanese for 18 months, then applied to bilingual design roles in Tokyo.",
        "tags": ["Design", "JLPT N2", "Bilingual roles"],
        "from_location": "London, UK",
        "current_role": "Product Designer",
        "current_company": "LINE Yahoo Japan",
        "japanese_level": "JLPT N2",
        "background": """
Priya worked at a London consumer-mobile startup for 5 years. Her partner is Japanese, so
relocating to Tokyo was always the long-term plan, but she didn't want to start over as a
junior. She gave herself 18 months to get to N2 while keeping her current job.""",
        "process": """
By the time she applied, she'd built a portfolio site with English + Japanese case studies,
sat the JLPT N2 (passed on second attempt), and joined a couple of Tokyo design Slack groups.
Interview process: 5 companies, all bilingual roles. Two rejected her in the first round.
LINE Yahoo's interview was conducted ~70% in English with the remainder in Japanese, mostly
small talk to confirm she could function in mixed-language meetings.""",
        "outcome": """
¥8.5M base + bonuses (typically 4 months at LINE Yahoo, so ~¥11M total comp). Spouse visa
through her partner, so no visa sponsorship needed from the employer.""",
        "lessons": [
            "Bilingual design roles pay more than 'English-only' equivalents, the supply of N2 designers is small.",
            "Translate at least 2 case studies into Japanese for your portfolio. It signals seriousness more than the JLPT certificate alone.",
            "If you have a Japanese spouse, get the spouse visa first, it gives you unrestricted work rights and you stop being a visa liability for employers.",
        ],
    },
    {
        "slug": "marco-eikaiwa-to-engineering",
        "avatar": "mortar-board",
        "name": "Marco D.",
        "role": "Software Engineer @ Cybozu",
        "headline": "From eikaiwa teacher to ¥7M backend engineer in 3 years.",
        "summary": "Used English teaching as a foothold, then taught himself Go on weekends and switched careers without leaving Japan.",
        "tags": ["Software Engineering", "Career change", "Teaching → tech"],
        "from_location": "Madrid, Spain (originally), Osaka → Tokyo",
        "current_role": "Software Engineer",
        "current_company": "Cybozu",
        "japanese_level": "JLPT N3",
        "background": """
Marco came to Osaka in 2022 on an eikaiwa contract, ¥260K/month, 5 days a week, no benefits.
Decent foothold but a dead end financially. He'd studied computer science briefly in Spain
years earlier but never worked in tech. Started teaching himself Go evenings and weekends in
his first year in Japan.""",
        "process": """
Built one small open-source CLI tool (a JLPT vocabulary spaced-repetition timer) and got it
to ~150 stars on GitHub. After 18 months at the eikaiwa, started applying to junior engineer
roles. Got 22 rejections in 4 months. The 23rd application, a small bilingual SaaS company, brought him in for a paid take-home (¥30K for a weekend's work) and offered him the role.

Worked there for 14 months at ¥4.5M, then jumped to Cybozu via a referral from a Tokyo Dev
Slack contact he'd met at a meetup.""",
        "outcome": """
Now at Cybozu in Tokyo. ¥7.2M base + bonuses. Sponsored their visa transition from Instructor
(eikaiwa) to Engineer / Specialist with zero gap in residence status.""",
        "lessons": [
            "Eikaiwa is fine as a starting point. It's NOT fine as a destination, plan your exit in your first 6 months.",
            "Open-source contributions matter more than degrees for foreign engineers in Japan. They de-risk the hire.",
            "Get to N3 minimum before switching into tech. Even at 'English-friendly' companies, the documentation, Jira tickets, and lunchtime chatter are still in Japanese.",
        ],
    },
    {
        "slug": "yuki-foreign-pr-to-startup-founder",
        "avatar": "rocket",
        "name": "Yuki S.",
        "role": "Founder / CEO @ stealth-mode B2B SaaS",
        "headline": "Used Business Manager visa to start a company in Tokyo.",
        "summary": "Quit her Tokyo enterprise PM role at 32, used HSP points to fast-track PR, then went out on her own.",
        "tags": ["Business Manager visa", "Founder", "HSP"],
        "from_location": "Singapore (originally), Tokyo for 6 years",
        "current_role": "Founder / CEO",
        "current_company": "(stealth)",
        "japanese_level": "JLPT N1",
        "background": """
Yuki moved to Tokyo from Singapore in 2020 to take a product manager role at a large enterprise.
N1 fluency, masters from Waseda, ¥10M salary by year 4, strong HSP point profile (95 by her
last calculation). Got PR through the 1-year HSP fast-track in 2024.""",
        "process": """
Spent 2024 quietly building the prototype for a B2B SaaS tool aimed at Japanese small businesses.
Quit her PM role in late 2024 with 18 months of runway. Filed for a Business Manager visa
transition (capital deposited, office secured in Roppongi, hired her first full-time engineer), approved in 11 weeks.""",
        "outcome": """
Now in seed-fundraising mode, talking to JAFCO, Coral Capital, and a couple of corporate VCs.
Day-to-day operating in Japanese with one bilingual engineer.""",
        "lessons": [
            "PR before founding is a huge unlock, you stop being beholden to any single visa or employer.",
            "Business Manager visa requires real substance: ¥5M deposited, real office, a real plan. The Immigration Bureau will visit.",
            "Japanese VC due diligence is exhaustive, expect months, not weeks.",
        ],
    },
]


def get_story(slug: str) -> dict | None:
    return next((s for s in STORIES if s["slug"] == slug), None)


# ---------------------------------------------------------------------------
# Community groups, curated external links.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Phase 6: Interview questions by role family + STAR prompts
# ---------------------------------------------------------------------------

INTERVIEW_QUESTIONS: dict[str, list[dict]] = {
    "Software Engineering": [
        {"q": "Walk me through the most complex system you've designed.",
         "watch_for": "Look for: who the users were, what tradeoffs were made, what failed and how it was fixed.",
         "jp_tip": "Japanese interviewers love specifics, name the technology stack and quantify the scale."},
        {"q": "Describe a time you had to debug a production issue under pressure.",
         "watch_for": "Look for: methodical process, communication, post-mortem follow-through.",
         "jp_tip": "Lead with what you did to prevent recurrence, Japanese eng culture prizes 改善 (kaizen)."},
        {"q": "How do you approach learning a new technology?",
         "watch_for": "Look for: structure (read docs → build small thing → ship → review).",
         "jp_tip": "Mention if you've taught the technology to others, collaborative learning is valued."},
        {"q": "Tell me about a code review that taught you something.",
         "watch_for": "Look for: openness to feedback, willingness to revise.",
         "jp_tip": "Phrase it humbly, 'I learned that…' rather than 'they were wrong about…'."},
        {"q": "What's a recent technical decision you'd revisit if you could?",
         "watch_for": "Look for: self-awareness, ability to articulate trade-offs in retrospect.",
         "jp_tip": "Don't trash former colleagues. Focus on the decision, not the people."},
        {"q": "How would you onboard a junior engineer to your current team?",
         "watch_for": "Look for: empathy, documentation instinct, time investment willingness.",
         "jp_tip": "Mentorship is hugely valued at Japanese tech companies."},
        {"q": "Where do you want to be in 3 years?",
         "watch_for": "Look for: clear direction, alignment with the role they're hiring for.",
         "jp_tip": "Japanese companies expect longer tenures, don't say 'I'll be looking elsewhere'."},
    ],
    "Data / AI": [
        {"q": "Walk me through an ML project end-to-end, problem framing, data, model, deploy.",
         "watch_for": "Look for: did they validate the problem before modeling?",
         "jp_tip": "Quantify the business impact, Japanese hiring managers underweight pure modeling chops."},
        {"q": "How do you handle a model that performs well offline but poorly in production?",
         "watch_for": "Look for: data drift awareness, feedback loops, evaluation discipline.",
         "jp_tip": "Show structured thinking; the recruiter may translate notes for tech panels."},
        {"q": "Tell me about a time data was missing or low-quality. How did you proceed?",
         "watch_for": "Look for: pragmatism, communication with stakeholders.",
         "jp_tip": "Acknowledge limitations honestly, overclaiming hurts trust."},
        {"q": "What's a recent paper or technique you found compelling?",
         "watch_for": "Look for: real curiosity beyond the role's narrow tech stack.",
         "jp_tip": "Tie it to a hypothetical at their company; it shows you researched them."},
        {"q": "How do you decide between a simple model and a complex one?",
         "watch_for": "Look for: bias toward simplicity, willingness to ship.",
         "jp_tip": "Japanese teams often prefer simple, observable systems."},
    ],
    "Product Management": [
        {"q": "Tell me about a feature you killed. Why?",
         "watch_for": "Look for: data-driven reasoning, customer empathy.",
         "jp_tip": "Killing features requires courage, Japanese PMs are praised for this."},
        {"q": "How do you decide what NOT to build?",
         "watch_for": "Look for: prioritization framework, opportunity cost awareness.",
         "jp_tip": "Reference any Japan-specific user research you've done."},
        {"q": "Describe a cross-functional disagreement you resolved.",
         "watch_for": "Look for: facilitation skills, willingness to compromise.",
         "jp_tip": "Japanese culture deeply values group consensus (合意, gōi). Lean into it."},
        {"q": "How would you measure success for our product in its first year?",
         "watch_for": "Look for: research into the actual product, clear North-Star thinking.",
         "jp_tip": "Bring 2-3 specific suggestions, not a generic 'I'd look at engagement'."},
        {"q": "How do you handle pushback from engineering on scope?",
         "watch_for": "Look for: trust-building, willingness to descope.",
         "jp_tip": "Avoid sounding combative, emphasize 'partnering' over 'pushing back'."},
    ],
    "Design": [
        {"q": "Walk me through a project from research to shipped design.",
         "watch_for": "Look for: structured process, evidence of iteration.",
         "jp_tip": "Bring a Japanese case study if you have one, it signals you understand the market."},
        {"q": "Describe a design you defended that turned out to be wrong.",
         "watch_for": "Look for: humility, learning orientation.",
         "jp_tip": "Spinning this positively is hard, practice the answer aloud."},
        {"q": "How do you handle stakeholders who want their preferences over user data?",
         "watch_for": "Look for: diplomacy, ability to educate, framing.",
         "jp_tip": "In Japan, defer first, then propose alternatives, direct refusal is rare."},
    ],
    "Sales / BD": [
        {"q": "Tell me about your largest deal. How did you close it?",
         "watch_for": "Look for: specifics on stakeholder mapping, objection handling.",
         "jp_tip": "Naming Japanese companies you've worked with builds credibility."},
        {"q": "How would you build pipeline in Japan with limited language?",
         "watch_for": "Look for: realism, partnership thinking, comfort with constraints.",
         "jp_tip": "Acknowledge the limitation up front; propose how to compensate."},
        {"q": "Describe a deal you lost. What did you learn?",
         "watch_for": "Look for: ownership rather than blaming.",
         "jp_tip": "Self-criticism is culturally appreciated, don't be afraid to look 'weak'."},
    ],
    # Behavioral questions every interview throws at you
    "Behavioral (universal)": [
        {"q": "Why do you want to work at our company specifically?",
         "watch_for": "Specificity: a product, a value, a recent announcement, not generic praise.",
         "jp_tip": "Mention something only an insider would know, recent news, a hiring blog post, a CEO talk."},
        {"q": "Why are you leaving your current role?",
         "watch_for": "Forward-looking framing, not bitter retrospection.",
         "jp_tip": "Loyalty matters, don't bash your current employer."},
        {"q": "Tell me about a conflict at work and how you resolved it.",
         "watch_for": "Process: listen → understand → find common ground → propose.",
         "jp_tip": "Indirect resolution is normal in Japan, explicit confrontation is rare."},
        {"q": "What's your biggest weakness?",
         "watch_for": "Real but addressable, with concrete steps you're taking.",
         "jp_tip": "Acknowledging a Japanese-specific weakness (language, culture) with a plan signals self-awareness."},
        {"q": "Why Japan, and why now?",
         "watch_for": "Genuine reasons beyond 'I like anime'. Career, life-stage, partner, depth of interest.",
         "jp_tip": "If your reasons include a Japanese spouse or long-term ties, mention it, signals retention."},
        {"q": "Do you have any questions for us?",
         "watch_for": "ALWAYS prepare 3-5. The depth of your questions signals seriousness.",
         "jp_tip": "Ask about team dynamics, success criteria for the role, mentorship, learning culture."},
    ],
}

# STAR template prompts for the answer-builder
STAR_PROMPTS = {
    "Situation": "Set the context. When? Where? What was the team / scope?",
    "Task":      "What was your specific responsibility or goal?",
    "Action":    "What did YOU (not 'we') actually do? Pick 2-3 specific actions.",
    "Result":    "What happened? Include numbers, percentages, business impact.",
}


# ---------------------------------------------------------------------------
# Phase 6: Career roadmaps per role family
# ---------------------------------------------------------------------------

ROADMAPS: list[dict] = [
    {
        "slug": "software-engineering",
        "icon": "cpu",
        "title": "Software Engineering, career roadmap in Japan",
        "summary": "From bootcamp grad to staff/principal at a Tokyo product company. Five stages with skills, salary, and timeline.",
        "stages": [
            {
                "title": "Junior / Associate Engineer",
                "years": "0-2 yrs",
                "salary": "¥4M – ¥6M",
                "skills": [
                    "One mainstream language (Go, Python, TypeScript, Java) at confident level.",
                    "Git workflow, code review etiquette, basic CI/CD familiarity.",
                    "Reading specs / Jira tickets and shipping in 1-week increments.",
                    "Owning small features end-to-end with senior support.",
                    "Write tests at three levels: unit, integration, end-to-end.",
                    "Read 'how this system works' documents in 30 minutes and ask substantive questions.",
                ],
                "promotion_to_next": "Ship a project you own from spec to production. Mentor an intern or junior. Pass a basic on-call shift.",
                "japan_specifics": [
                    "Most JP entry-level eng salaries are ¥4-5M. Mercari, SmartNews, foreign-cap startups go higher.",
                    "Most teams will have at least some Japanese, get to N3 by end of year 2.",
                    "Most foreigner-friendly Japanese employers offer a 1-month onboarding bootcamp where Japanese vocabulary basics are taught at no cost.",
                    "Foreign-cap Japan offices (FAANG, Stripe, Datadog) start junior comp at ¥5.5–8M, well above Japanese-majors at ¥4–5.5M.",
                ],
            },
            {
                "title": "Mid Engineer",
                "years": "2-5 yrs",
                "salary": "¥6M – ¥10M",
                "skills": [
                    "Strong primary stack + comfort with adjacent areas (e.g. backend + some frontend).",
                    "Design docs and tradeoff analysis for medium-sized features.",
                    "Database design (indexing, denormalization, transactions).",
                    "Production debugging using observability tooling (logs, traces, metrics).",
                    "Code review giver, not just receiver.",
                    "Lead a small migration or refactor across one service.",
                    "Run an incident response: triage, mitigate, write the postmortem.",
                ],
                "promotion_to_next": "Drive a quarter-long initiative across 2-3 engineers. Be the on-call expert for one subsystem. Interview candidates.",
                "japan_specifics": [
                    "This is the sweet spot for switching companies, pay jumps 20-40% per move.",
                    "Mercari / PayPay / LINE Yahoo offer signing bonuses of ¥1-3M at this level.",
                    "Bilingual mid engineers at Japanese-headquartered employers see 25–40% comp uplift on job change in the 2026 market.",
                    "Mid engineers at PayPay, Mercari, SmartNews routinely cross ¥10M total with signing bonuses.",
                ],
            },
            {
                "title": "Senior Engineer",
                "years": "5-9 yrs",
                "salary": "¥10M – ¥16M",
                "skills": [
                    "System design across multiple services, including async / distributed concerns.",
                    "Designing migrations from legacy systems with zero downtime.",
                    "Setting technical direction for a team or sub-team.",
                    "Mentoring 2-3 mid-level engineers actively.",
                    "Cross-team comms: explaining tradeoffs to PM, design, leadership.",
                    "Author and defend a multi-quarter technical roadmap.",
                    "Drive incident reviews and process changes that prevent classes of bugs.",
                    "Interview senior IC candidates as a primary panelist.",
                ],
                "promotion_to_next": "Lead a 6-12 month project that touches 3+ teams. Author a public-facing engineering blog post. Be in the room when the architecture decisions get made.",
                "japan_specifics": [
                    "Many senior engineers plateau here for years, that's fine if comp keeps growing.",
                    "Equity packages start mattering. Pre-IPO startups offer 0.05-0.2%.",
                    "Senior engineers at FAANG Tokyo with RSUs commonly clear ¥18–22M total comp; same level at Mercari/PayPay sits at ¥13–16M cash.",
                    "Equity grants at pre-IPO Japanese unicorns (SmartNews historically, Sakana AI now) can be material at this level.",
                ],
            },
            {
                "title": "Staff / Tech Lead",
                "years": "9-12 yrs",
                "salary": "¥14M – ¥22M",
                "skills": [
                    "Reason about cross-cutting concerns (security, observability, reliability) across the org.",
                    "Drive consensus on technical direction across multiple teams.",
                    "Mentor seniors (not just juniors).",
                    "Translate business problems into multi-quarter technical roadmaps.",
                    "Write artifacts that outlast you: design docs, postmortems, training materials.",
                    "Own one technical area as the named authority across the company.",
                    "Develop other engineers to senior and staff levels.",
                    "Influence product strategy at the GM / VP level.",
                ],
                "promotion_to_next": "Become the named technical authority on one major area for the company. Lead a hiring loop. Sponsor at least one engineer's promotion.",
                "japan_specifics": [
                    "Rare at small companies; more common at Indeed / Mercari / Rakuten / global FAANGs in Tokyo.",
                    "RSU packages start being a meaningful share of comp at FAANG.",
                    "Staff engineers at FAANG Tokyo clear ¥25–30M+; rare role at most Japanese employers, mostly mapping to 'Principal' / 'Fellow' tracks.",
                    "Bilingual staff engineers in heavy demand for cross-org architecture roles at PayPay, LINE Yahoo, Rakuten.",
                ],
            },
            {
                "title": "Principal / Distinguished",
                "years": "12+ yrs",
                "salary": "¥18M – ¥35M+",
                "skills": [
                    "Set technical strategy at the company or division level.",
                    "Direct technical influence over decisions made by VPs and C-suite.",
                    "External technical reputation: talks, papers, open source.",
                    "Train other staff engineers to become principals.",
                    "Set engineering strategy at the company level.",
                    "Author public engineering blog posts that drive recruiting brand.",
                    "Develop 2+ staff engineers to principal level.",
                ],
                "japan_specifics": [
                    "Maybe 50-100 people in Tokyo at this level across all companies.",
                    "Most reach it after one big move to a foreign-cap firm (Google / Amazon / Stripe).",
                    "Principal IC at FAANG Tokyo: ¥30–50M+ total comp, mostly RSU-loaded.",
                    "Most Japan-domestic Principal IC roles are at Mercari, Sakana AI, PFN, bilingual capital essential.",
                ],
            },
        ],
        "common_pivots": [
            "→ Engineering Manager: people-first, ¥15-22M, less coding.",
            "→ Founder: high risk, requires PR or Business Manager visa.",
            "→ Solutions Architect / DevRel: heavy customer interaction, ¥15-25M, sometimes more travel.",
            "→ Independent contractor: ¥15-25M/yr equivalent but no benefits / visa sponsorship.",
            "→ Solutions architect at AWS / GCP / Azure Japan: customer-facing technical role at ¥18–28M with travel.",
            "→ Developer advocate / DevRel: high public-facing role at Stripe / MongoDB / Cloudflare Japan; ¥15–25M with strong personal brand upside.",
            "→ Open-source maintainer-as-employee: rare in Japan but growing (Sakana AI, PFN sponsor maintainers).",
        ],
    },
    {
        "slug": "data-ai",
        "icon": "database",
        "title": "Data / AI, career roadmap in Japan",
        "summary": "From junior data analyst to ML platform lead. Three sub-tracks (analyst / scientist / engineer) and how they merge at senior.",
        "stages": [
            {
                "title": "Junior Data Analyst / Data Engineer",  # ENRICH:data-ai:Junior Data Analyst / Data Engineer:v1
                "years": "0-2 yrs",
                "salary": "¥4.5M – ¥7M",
                "skills": [
                    "SQL fluently. Python / pandas for transformations. Tableau or Looker.",
                    "Building daily dashboards, answering business stakeholder questions.",
                    "Basic statistics: p-values, confidence intervals, A/B test reading.",
                    'Build one production ETL pipeline (dbt + Airflow / Dagster).',
                    'Author SQL that runs over billions of rows efficiently.',
                ],
                "promotion_to_next": "Own a dashboard end-to-end. Catch one data quality issue before stakeholders do. Run one A/B test.",
                "japan_specifics": [
                    "Many Japanese companies underinvest in data, opportunity if you can demonstrate impact.",
                    'Bilingual junior data hires at Mercari, PayPay start at ¥6–7M.',
                    'Japanese-majors (Rakuten, LINE Yahoo) historically pay ¥4.5–5.5M at this level.',
                ],
            },
            {
                "title": "Mid Data Scientist / ML Engineer",  # ENRICH:data-ai:Mid Data Scientist / ML Engineer:v1
                "years": "2-5 yrs",
                "salary": "¥7M – ¥12M",
                "skills": [
                    "Build and ship one production model end-to-end.",
                    "Feature engineering, hyperparameter tuning, simple deep learning.",
                    "Statistical experimentation design, A/B/n, sequential testing.",
                    "Pair with product to define success metrics.",
                    'Productionise one ML model with monitoring and re-training.',
                    'Run a rigorous online experiment with proper power analysis.',
                ],
                "promotion_to_next": "Ship a model that drives a measurable revenue/cost number. Onboard a junior.",
                "japan_specifics": [
                    "LLM teams at Cyberagent, Rakuten, and PFN pay top of band.",
                    'Sakana AI, PFN, and FAANG Tokyo AI teams are the highest-paying mid-band: ¥12–18M with equity at Sakana AI.',
                    'Bilingual MLEs at LINE Yahoo Japan and Rakuten see 20–30% job-change uplifts in the 2026 cycle.',
                ],
            },
            {
                "title": "Senior / Staff ML",  # ENRICH:data-ai:Senior / Staff ML:v1
                "years": "5-9 yrs",
                "salary": "¥12M – ¥20M",
                "skills": [
                    "Architect end-to-end ML systems: training pipelines, online inference, monitoring.",
                    "Influence product strategy with data-driven recommendations.",
                    "Mentor a team of 3-5 analysts/scientists.",
                    'Own an ML platform layer (training infra, feature store, inference serving).',
                    'Author the org-wide ML practices and review templates.',
                    'Mentor 3–5 ML engineers and data scientists.',
                ],
                "japan_specifics": [
                    "Preferred Networks, Sakana AI, and global FAANG Tokyo offices pay ¥18-25M+ at this level.",
                    'Senior ML at Sakana AI: ¥18–28M cash plus generous equity in a fast-growing unicorn.',
                    'Senior ML at FAANG Tokyo (Google Brain Japan, Amazon Science Tokyo): ¥22–32M with RSUs.',
                ],
            },
        ],
        "common_pivots": [
            "→ Research scientist (PhD-heavy track): less business-facing, ¥15-30M.",
            "→ Analytics engineering: between data and software eng, currently hot.",
            '→ ML platform engineering: hybrid of MLE and platform / SRE; high comp at FAANG Tokyo and Sakana AI.',  # ENRICH:data-ai:pivots:v1
            '→ Applied research scientist: PhD-favoured; PFN, Sakana AI, Cyberagent AI Lab pay ¥18–35M.',  # ENRICH:data-ai:pivots:v1
            '→ AI product manager: hot pivot in 2025–26; AI PMs at FAANG Tokyo, Sakana AI, Mercari at ¥15–25M.',  # ENRICH:data-ai:pivots:v1
            '→ Quant researcher at HF: Citadel Tokyo, Millennium Tokyo recruit ML/data backgrounds at ¥20–40M+.',  # ENRICH:data-ai:pivots:v1
        ],
    },
    {
        "slug": "product-management",
        "icon": "clipboard",
        "title": "Product Management, career roadmap in Japan",
        "summary": "PM roles for foreigners in Japan are scarcer than eng, but doors open faster once you're in.",
        "stages": [
            {
                "title": "Associate PM",  # ENRICH:product-management:Associate PM:v1
                "years": "0-2 yrs",
                "salary": "¥5M – ¥8M",
                "skills": [
                    "Write a clear PRD. Run a sprint review. Hold a retrospective.",
                    "Light data analysis, basic SQL is the floor.",
                    "User research basics, interviewing 5 users without leading them.",
                    'Write a single-page strategy doc that survives an exec review.',
                    'Run a customer interview without leading the witness.',
                    'Read a dashboard and propose three follow-up hypotheses.',
                ],
                "japan_specifics": [
                    "Most APM positions go to internal converts (engineer / designer → PM) rather than external hires.",
                    'Most APM roles in Japan are internal conversions (engineer / designer to PM) rather than external hires.',
                    'Mercari APM bootcamp is the closest thing to a formal Japan APM programme.',
                ],
            },
            {
                "title": "Mid PM",  # ENRICH:product-management:Mid PM:v1
                "years": "2-5 yrs",
                "salary": "¥8M – ¥13M",
                "skills": [
                    "Own a feature area end-to-end across 1-2 quarters.",
                    "Run discovery: customer interviews, market research, competitive scan.",
                    "Influence engineering and design without authority.",
                    'Own a feature area through 4+ quarterly cycles.',
                    'Run a competitive teardown that influences positioning.',
                    'Partner with sales on at least 5 customer deals as the named product POC.',
                ],
                "japan_specifics": [
                    "Bilingual PMs are heavily in demand at companies expanding into Japan.",
                    'Bilingual mid PMs at PayPay, Mercari, Indeed clear ¥10–13M; foreign-cap (Google, Stripe, Notion) clear ¥13–18M.',
                    'B2B SaaS PM seats (Sansan, freee, Money Forward) involve more customer-facing time and Japanese-language interviewing.',
                ],
            },
            {
                "title": "Senior / Group PM",  # ENRICH:product-management:Senior / Group PM:v1
                "years": "5-9 yrs",
                "salary": "¥13M – ¥20M",
                "skills": [
                    "Set product strategy for an area with multiple feature teams.",
                    "Mentor 2-3 PMs.",
                    "Manage stakeholders up to VP/Director level.",
                    'Set product strategy at the area level (multiple feature teams).',
                    'Hire and develop 2–3 mid PMs.',
                    'Run multi-quarter discovery on a new product line.',
                ],
            },
        ],
        "common_pivots": [
            "→ Director of Product: ¥18-30M.",
            "→ Chief of Staff: cross-functional executive role.",
            "→ VC associate: Japan ecosystem is hungry for ex-PMs.",
            '→ Director of Product: ¥22–35M; rare role outside FAANG Tokyo and unicorn-stage Japanese SaaS.',  # ENRICH:product-management:pivots:v1
            '→ Chief of Staff to CEO: cross-functional exec role at growth-stage Japanese startups.',  # ENRICH:product-management:pivots:v1
            '→ VC associate: Japan VC ecosystem (Globis Capital, JIC VGI, Mitsubishi UFJ Capital) hungry for ex-PMs.',  # ENRICH:product-management:pivots:v1
            '→ Founder: Japan B2B SaaS founder pool is increasingly ex-PM rather than ex-engineer.',  # ENRICH:product-management:pivots:v1
        ],
    },
    {
        "slug": "design",
        "icon": "pencil",
        "title": "Design, career roadmap in Japan",
        "summary": "Product / UX / UI designers in Japan. Bilingual roles pay more than English-only because supply is small.",
        "stages": [
            {
                "title": "Junior Designer",  # ENRICH:design:Junior Designer:v1
                "years": "0-2 yrs",
                "salary": "¥4M – ¥7M",
                "skills": [
                    "Figma fluency, design system usage.",
                    "Wireframing and prototyping.",
                    "Basic user research: usability tests, click tests.",
                    'Build a portfolio of 3–4 case studies showing your end-to-end process.',
                    'Run a usability test and synthesize insights into 3 actionable changes.',
                ],
            },
            {
                "title": "Mid Product Designer",  # ENRICH:design:Mid Product Designer:v1
                "years": "2-5 yrs",
                "salary": "¥7M – ¥11M",
                "skills": [
                    "Lead design for a feature from research to ship.",
                    "Run user interviews; synthesize insights.",
                    "Contribute to the design system.",
                    'Own design end-to-end for one feature area through ship.',
                    'Run research with Japanese-speaking participants (with translator if needed).',
                    'Contribute meaningfully to a design system (components + tokens + docs).',
                ],
                "japan_specifics": [
                    "JP-language case studies make a strong portfolio differentiator.",
                    'Bilingual junior product designers at foreign-cap Tokyo offices (Stripe, Notion, Figma Japan) start at ¥6–8M.',
                    'Japanese-majors (Rakuten, LINE Yahoo) start at ¥4.5–5.5M but offer faster level progression in some teams.',
                    'Bilingual mid product designers in heavy demand at Mercari, SmartNews, PayPay; ¥9–13M.',
                    'Visual / brand designers at design-led Japanese firms (Goodpatch, Cookpad, Studio Ghibli digital) command meaningful premiums.',
                ],
            },
            {
                "title": "Senior / Staff Designer",  # ENRICH:design:Senior / Staff Designer:v1
                "years": "5-9 yrs",
                "salary": "¥11M – ¥17M",
                "skills": [
                    "Own design direction for a major product area.",
                    "Mentor mid-level designers.",
                    "Cross-functional partnership at director level.",
                    'Own design direction for a major product area across multiple feature teams.',
                    'Mentor 2–4 mid designers actively.',
                    'Partner with senior PM and senior EM at parity.',
                ],
            },
        ],
        "common_pivots": [
            "→ Design Manager: ¥15-22M.",
            "→ Design Engineer: hybrid role at modern startups.",
            "→ Brand / Marketing design: different ladder, similar comp.",
            '→ Design Manager: people-management track; ¥18–25M at top employers.',  # ENRICH:design:pivots:v1
            '→ Design Engineer: hybrid IC role at modern startups; high comp at SmartNews, Sakana AI.',  # ENRICH:design:pivots:v1
            '→ Brand / Marketing design: different ladder, similar comp; particularly strong at luxury / FMCG Japan.',  # ENRICH:design:pivots:v1
            '→ Design Director: rare in Japan; ¥25–35M at FAANG Tokyo and unicorn-stage Japanese SaaS.',  # ENRICH:design:pivots:v1
            '→ Founder: design-founder startups (Goodpatch heritage) are increasingly common in Japan B2B SaaS.',  # ENRICH:design:pivots:v1
        ],
    },

    # NEW_ROADMAPS:v1
    {
        "slug": "marketing",
        "icon": 'rocket',
        "title": 'Marketing, career roadmap in Japan',
        "summary": ('From coordinator to CMO across performance, brand, content, and product marketing. Six stages '
 'with salary bands, promotion criteria, and Japan-specific notes.'),
        "stages": [   {   'title': 'Coordinator / Specialist',
        'years': '0-2 yrs',
        'salary': '¥4.5M – ¥7M',
        'skills': [   'Own one channel end-to-end: paid search, paid social, SEO, content, or '
                      'email.',
                      'Hands-on with the tooling: Google Ads, Yahoo Japan Ads, Meta, LINE Ads '
                      'Platform, GA4, HubSpot, Marketo, or Pardot.',
                      'Read a campaign report: CPM, CPC, CTR, CPA, ROAS, what each tells you and '
                      'what they hide.',
                      'Write a single campaign brief: audience, hypothesis, creative, KPI, success '
                      'threshold.',
                      'Run a basic A/B test and interpret it correctly (avoid p-hacking).'],
        'promotion_to_next': 'Own one channel above target for two consecutive quarters. Run at '
                             'least three campaigns end-to-end. Be the named owner of one KPI.',
        'japan_specifics': [   'Bilingual coordinators at foreign-cap SaaS (Notion, HubSpot, '
                               'Datadog) start at the top of the band, ¥6.5–7M.',
                               'Domestic agencies (Dentsu D, Cyberagent) pay less at entry but '
                               'offer faster channel-rotation training.']},
    {   'title': 'Marketing Manager',
        'years': '2-5 yrs',
        'salary': '¥7M – ¥11M',
        'skills': [   'Run two or more channels with a meaningful budget (¥30M+/yr).',
                      'Set quarterly targets and forecast budget-to-outcome on a defensible model.',
                      'Brief and manage an agency or freelance creator; review creative for tone '
                      'and brand fit.',
                      'Manage cross-functional dependencies (legal review, brand approval, product '
                      'launches).',
                      'Mentor a coordinator and review their work.'],
        'promotion_to_next': 'Own a full P&L slice. Lead one cross-functional launch end-to-end. '
                             'Hire and onboard one specialist.',
        'japan_specifics': [   'Bilingual capacity is the largest comp lever at this level, N2+ '
                               'adds ~¥1.5–2.5M.',
                               'Foreign-cap SaaS expansion (Stripe, Notion, Snowflake) drives most '
                               'of the 2025–26 hiring at this band.']},
    {   'title': 'Senior Manager',
        'years': '5-9 yrs',
        'salary': '¥11M – ¥16M',
        'skills': [   "Own a region or function (e.g., 'Japan demand gen' or 'APAC content').",
                      'Build an annual plan with executive sponsors; defend trade-offs against '
                      'revenue forecasts.',
                      'Hire and manage 2–5 ICs; develop one to promotion.',
                      'Set positioning narrative in the local market; partner with PMM, sales, and '
                      'product on launches.',
                      'Run partner / agency selection RFPs.'],
        'promotion_to_next': 'Run a 12-month plan with a meaningful (¥300M+) budget. Promote one '
                             'report. Be present in product / sales / GM exec reviews.',
        'japan_specifics': [   'First-line senior managers at FAANG Tokyo or top-tier SaaS clear '
                               '¥14–16M total.',
                               'Luxury/FMCG senior brand managers receive structured promotion at '
                               'year 7–8 (P&G, Unilever).']},
    {   'title': 'Head of Marketing / Director',
        'years': '9-13 yrs',
        'salary': '¥16M – ¥25M',
        'skills': [   'Own the marketing function for a brand or region.',
                      'Set the multi-year strategy; defend it to CEO/CFO.',
                      'Hire and develop 1–2 senior managers; oversee 10–20 total org.',
                      'Operate marketing as a profit-influencing function: pipeline, LTV/CAC, '
                      'brand equity.',
                      'Manage external relationships: agency, press, partners, vendors.'],
        'promotion_to_next': 'Drive a measurable revenue inflection. Sponsor one senior promotion. '
                             'Be a credible CEO/board partner.',
        'japan_specifics': [   'Most Head of Japan Marketing roles at foreign-cap firms include '
                               '0.05–0.15% equity and ¥3–5M signing.',
                               'Director-band hiring at LVMH, Richemont, Kering in Japan is '
                               'competitive; bilingual capital essential.']},
    {   'title': 'VP Marketing / CMO',
        'years': '13+ yrs',
        'salary': '¥25M – ¥45M+',
        'skills': [   'Own brand, demand gen, PMM, and comms across the whole company / region.',
                      'Be a credible peer to CEO, head of product, head of sales.',
                      'Set go-to-market strategy at the company level.',
                      'Build the marketing org: hire 2–3 directors, define the operating model.',
                      'External representation: press, investors, partners.'],
        'japan_specifics': [   'CMO roles at Japanese SaaS (freee, Money Forward, Sansan) command '
                               '¥25–35M plus equity.',
                               'VP Japan / APAC at foreign-cap (Stripe, Snowflake, Datadog) '
                               'reaches ¥35–55M with equity.']}],
        "common_pivots": [   '→ Country GM: top brand managers and CMOs transition to general-management roles at ¥30–50M+.',
    '→ Founder: D2C founders commonly come from brand-marketing backgrounds; Tokyo D2C scene is '
    'small but growing.',
    '→ VC partner / operator: ex-CMOs join growth-stage VC firms in operator-partner roles.',
    '→ Agency leadership: pivot to running a Japan ad / brand agency (Dentsu D, R/GA, '
    'Wieden+Kennedy Tokyo).'],
    },
    {
        "slug": "sales-business-development",
        "icon": 'briefcase',
        "title": 'Sales & business development, career roadmap in Japan',
        "summary": ('From SDR to country GM. Six stages with OTE bands, promotion criteria, and Japan-specific notes '
 'for foreign-cap SaaS and Japanese B2B contexts.'),
        "stages": [   {   'title': 'SDR / BDR',
        'years': '0-2 yrs',
        'salary': '¥5M – ¥7M base, ¥6.5–9M OTE',
        'skills': [   'Run an outbound prospecting motion: cold email, cold call, LinkedIn '
                      'outreach.',
                      'Qualify leads with a discovery framework (BANT, MEDDIC, MEDDPICC light).',
                      'Schedule and prepare qualified meetings for AEs.',
                      'Operate in CRM (Salesforce, HubSpot) and outbound tooling (Outreach, '
                      'Salesloft, Apollo).',
                      'Read and prioritize a target account list.'],
        'promotion_to_next': 'Hit quota for two consecutive quarters. Build one repeatable plays '
                             'book. Earn AE-segment manager endorsement.',
        'japan_specifics': [   'Bilingual SDR base sits at ¥6–7M at top SaaS; pure English-only '
                               'SDR (APAC HQ accounts) is smaller pool, similar pay.',
                               'Most foreign-cap firms promote SDRs to AE in 12–18 months; '
                               'aggressive over-performers in 9–12 months.']},
    {   'title': 'Account Executive (SMB / Mid-Market)',
        'years': '2-4 yrs',
        'salary': '¥8M – ¥11M base, ¥13–18M OTE',
        'skills': [   'Run full sales cycles end-to-end: discovery, demo, proposal, negotiation, '
                      'close.',
                      'Hold a monthly / quarterly quota; forecast accurately within 10%.',
                      'Build relationships across the buying committee: champion, economic buyer, '
                      'technical evaluator.',
                      'Co-sell with SE on technical proofs.',
                      'Manage a pipeline of 30–80 active opportunities.'],
        'promotion_to_next': 'Hit quota in 2 of 3 quarters. Close 1+ multi-stakeholder deal. '
                             'Develop one named account into recurring expansion.',
        'japan_specifics': [   'Bilingual mid-market AEs are heavily oversubscribed; quota-hitters '
                               'routinely get poached at +25–40% OTE.',
                               'Most foreign-cap SaaS Japan teams promote AEs to Enterprise AE in '
                               '2–3 years.']},
    {   'title': 'Enterprise / Strategic AE',
        'years': '4-8 yrs',
        'salary': '¥11M – ¥18M base, ¥22–35M+ OTE',
        'skills': [   'Run 6–18 month enterprise sales cycles with multi-stakeholder buying '
                      'committees.',
                      'Master commercial structuring: multi-year, multi-product, partner-led '
                      'co-sells.',
                      'Develop top-down exec sponsorship; defend ROI to CFO and CIO.',
                      'Partner with marketing, customer success, partner managers, RVP on named '
                      'accounts.',
                      'Mentor mid-market AEs and SDRs.'],
        'promotion_to_next': 'Hit enterprise quota with 1+ ¥100M+ deal. Develop 2–3 multi-product '
                             'wins. Earn senior manager endorsement.',
        'japan_specifics': [   'Top enterprise AEs at Salesforce / ServiceNow / Snowflake '
                               'routinely clear ¥40–55M total in good years.',
                               'Japanese conglomerate sales cycles run 12–18 months; SI partner '
                               '(Accenture, NTT Data) co-sell is the norm.']},
    {   'title': 'Sales Manager (First-Line)',
        'years': '8-11 yrs',
        'salary': '¥14M – ¥20M base, ¥22–32M OTE',
        'skills': [   'Hire, ramp, and coach 6–10 AEs.',
                      "Run an accurate forecast (3 reps' worth of pipeline x discount + commit).",
                      'Operate the sales-management cadence: 1:1s, deal reviews, QBR.',
                      'Build the territory plan; partner with marketing on demand allocation.',
                      'Manage performance: PIPs, terminations, top-grading.'],
        'promotion_to_next': 'Hit team quota in 3 of 4 quarters. Promote 1+ AE. Earn '
                             'director-level endorsement.',
        'japan_specifics': [   'First-line managers at foreign-cap SaaS Japan command ¥22–32M '
                               'total comp + RSUs.',
                               "Senior managers often transition to RVP at year 12–14 once they've "
                               'top-graded a team.']},
    {   'title': 'Director / RVP',
        'years': '11-15 yrs',
        'salary': '¥20M – ¥28M base, ¥35–55M OTE',
        'skills': [   'Own a region or segment with 20–60 quota-carrying reps under 2–4 first-line '
                      'managers.',
                      'Set go-to-market strategy; co-own with PMM and country GM.',
                      'Develop the second-line bench: 1–2 first-line managers ready for director '
                      'promotion.',
                      'Build external exec relationships with top customer accounts.',
                      'Operate as a peer to head of marketing, head of CS, country GM.'],
        'promotion_to_next': 'Hit segment quota in 4 of 6 quarters. Develop 2+ managers. Earn '
                             'VP-level endorsement and accountability for full P&L slice.',
        'japan_specifics': [   'Director-band at top SaaS in Tokyo commands meaningful equity '
                               'grants, often ¥40–80M over 4 years.',
                               'Most country GMs come from this band; the path is 2–4 years RVP → '
                               'GM.']},
    {   'title': 'Country GM / VP Japan',
        'years': '15+ yrs',
        'salary': '¥25M – ¥40M base, ¥50–100M+ OTE',
        'skills': [   'Own the full Japan P&L: sales, marketing, customer success, professional '
                      'services, partner ecosystem.',
                      'Be the face of the company to customers, press, government regulators.',
                      'Manage HQ relationship: defend Japan investment cases; influence product '
                      'roadmap.',
                      'Lead 100–500 person Japan org through hyper-growth phases.',
                      'Build executive bench: head of sales, head of marketing, head of CS, head '
                      'of partners.'],
        'japan_specifics': [   'VP Japan packages at Salesforce, ServiceNow, AWS, Microsoft '
                               'commonly include ¥30–60M base + RSU + bonus + signing, well over '
                               '¥100M total comp.',
                               'Japanese-only employers (LINE Yahoo, PayPay, Rakuten) pay less '
                               'cash but offer significant board/equity upside.']}],
        "common_pivots": [   '→ Founder: senior AEs and RVPs commonly start B2B SaaS companies; Sansan, KARTE founders had '
    'sales-adjacent backgrounds.',
    '→ VC partner / operator: top-of-funnel and GTM experience is in demand at growth-stage Tokyo '
    'VC firms.',
    '→ Country GM at adjacent foreign-cap: lateral move from VP Sales to GM at a smaller '
    'competitor.',
    '→ COO / VP Operations: country GMs frequently move into COO roles at later-stage scale-ups.'],
    },
    {
        "slug": "finance-accounting",
        "icon": 'chart-line',
        "title": 'Finance & accounting, career roadmap in Japan',
        "summary": ('From analyst to MD across investment banking, asset management, PE, and corporate finance. Six '
 'stages with comp bands and Japan-specific notes.'),
        "stages": [   {   'title': 'Analyst',
        'years': '0-2 yrs',
        'salary': '¥8M – ¥15M total (¥15M+ at bulge bracket IB)',
        'skills': [   'Build a full three-statement financial model from scratch.',
                      'Run a discounted cash flow and a comparable-company analysis.',
                      'Draft sections of a pitch book or buy-side memo.',
                      'Manage data: deal-room, comp screens, transaction databases.',
                      'Operate with extreme attention to detail under deadline pressure.'],
        'promotion_to_next': 'Complete an analyst-class training. Earn senior banker / portfolio '
                             'manager endorsement on at least one closed transaction or fund-level '
                             'project.',
        'japan_specifics': [   'Bulge bracket Japan analyst comp (GS, MS, JPM) sits at ¥12–15M '
                               'total in year 1, materially above Japanese majors at ¥8–11M.',
                               'FSA Type 1 / Type 2 registration is required for client-facing '
                               'securities work; employer pays for prep.',
                               'Big Four audit starts lower (¥5.5–7M) but offers a fast '
                               'CPA-to-controller pathway with foreign-cap firms.']},
    {   'title': 'Associate',
        'years': '2-5 yrs',
        'salary': '¥15M – ¥25M total',
        'skills': [   'Lead deal execution: drive model build, due diligence, document drafting.',
                      'Manage 1–2 analysts; review and quality-check their work.',
                      'Develop direct client / portfolio company relationships.',
                      'Operate cross-functionally with legal, tax, and compliance.',
                      'Earn CFA / equivalent (CFA Charter, MBA, JP CPA if relevant).'],
        'promotion_to_next': 'Lead one execution end-to-end. Pass CFA Level III or complete MBA. '
                             'Earn senior banker endorsement.',
        'japan_specifics': [   'Top-tier IB associate at GS/MS/JPM clears ¥20–25M total comp in '
                               'good years.',
                               'PE associate roles at KKR Japan, Bain Capital Japan offer ¥15–22M '
                               'cash plus carry on 1–2 funds.']},
    {   'title': 'Vice President',
        'years': '5-9 yrs',
        'salary': '¥25M – ¥45M total',
        'skills': [   'Originate (or co-originate) transactions; build client relationships at CFO '
                      '/ Treasurer level.',
                      'Manage execution across 2–4 associates / analysts.',
                      'Negotiate transaction terms; coordinate across legal, tax, syndicate.',
                      "Develop sector expertise (e.g., 'Japan industrials M&A' or 'JREIT "
                      "structured finance').",
                      'Mentor associate-class talent into directors.'],
        'promotion_to_next': 'Lead one major transaction as the named relationship VP. Generate ¥X '
                             'bn in fees over a year. Earn MD-level endorsement.',
        'japan_specifics': [   'VP at bulge bracket Tokyo clears ¥35–45M total comp at year 7–9.',
                               'PE VP at top funds clears ¥30–45M cash plus meaningful carry '
                               'across 2–3 active funds.',
                               'Bilingual capacity is decisive, Japan-domestic relationships '
                               '(sōgō shōsha CFOs, banking institution treasurers) require fluent '
                               'JP.']},
    {   'title': 'Director / Senior VP / Principal',
        'years': '9-13 yrs',
        'salary': '¥35M – ¥70M total',
        'skills': [   'Own a sector or product franchise (Japan industrials M&A, Japan ECM tech, '
                      'Japan fixed-income credit).',
                      'Generate ¥XXX mn in annual fees / P&L.',
                      'Manage a team of 6–12 VPs and associates.',
                      'Represent the firm publicly: industry conferences, financial press, '
                      'regulators.',
                      'Develop the franchise pipeline: client relationships, deal flow, talent.'],
        'promotion_to_next': 'Generate top-quartile fee/P&L performance for multiple consecutive '
                             'years. Manage and develop a top-decile team. Earn executive '
                             'committee / MD-class endorsement.',
        'japan_specifics': [   'Director / SVP at bulge bracket Tokyo: ¥50–70M total comp with '
                               'bonus heavily P&L-driven.',
                               'PE Principal at KKR / Bain / Carlyle: ¥45–60M cash + significant '
                               'carry; can clear ¥100M+ in fund-realization years.']},
    {   'title': 'Managing Director / Partner',
        'years': '13-20 yrs',
        'salary': '¥60M – ¥150M+ total',
        'skills': [   'Run a major franchise: head of Japan M&A, head of Japan equities, head of '
                      'Japan PE.',
                      'Operate as a peer of country head / regional head.',
                      "Develop and protect the firm's most strategic client relationships at "
                      'CEO/Chairman level.',
                      'Manage a P&L of ¥XX bn in revenue or AUM.',
                      'Build the next generation of VPs and directors.'],
        'japan_specifics': [   'MD at bulge bracket Tokyo: ¥80–150M total comp in normal years, '
                               '¥200M+ in record years.',
                               'PE Partner at top Japan-focused funds: ¥100M+ cash plus full carry '
                               'exposure across multiple funds.',
                               'Japanese major MD (Nomura, Daiwa, MUFG) ranges are lower, ¥40–80M '
                               'typically, but include extensive Japanese-domestic franchise '
                               'upside.']},
    {   'title': 'Head of Country / Regional Head',
        'years': '20+ yrs',
        'salary': '¥100M – ¥300M+',
        'skills': [   'Run the entire Japan franchise across investment banking, markets, asset '
                      'management, or PE.',
                      'Manage the regulator relationship: FSA, MoF, JPX.',
                      'Set the strategy for the firm in Japan; defend it to global executive '
                      'committee.',
                      'Manage 500–5,000+ Japan staff.',
                      'Be a public-facing figure: financial press, government policy advisory, '
                      'industry committees.'],
        'japan_specifics': [   'Country Head at bulge bracket Tokyo: cash + bonus + LTIP can '
                               'exceed ¥300M in good years.',
                               'Most country heads come from MD-class M&A or markets bankers with '
                               'deep Japan franchise tenure.']}],
        "common_pivots": [   '→ IB analyst → PE associate: classic 2-year post-banking pivot to KKR, Bain Capital, Carlyle, '
    'or Blackstone Japan.',
    '→ IB / PE → Corporate Development: senior bankers move in-house to SoftBank, Hitachi, Sony '
    'Group, Nidec, or Renesas at director-band comp with better hours.',
    '→ Big Four audit → Industry Controller: USCPA + N2 unlocks bilingual controller roles at '
    'foreign-cap firms (Stripe, Salesforce, Snowflake) at ¥12–20M total.',
    '→ Asset management → Wealth management: senior PMs move client-side to private banking at GS '
    '/ UBS / JPM with book-driven upside.',
    '→ Senior banker → CFO at portfolio company: PE-funded CFO roles at scale-ups offer ¥25–50M '
    'plus equity.',
    '→ MD → fund founder: rare but lucrative; multiple ex-MS / KKR partners have founded '
    'Japan-focused funds.'],
    },
    {
        "slug": "engineering-management",
        "icon": 'users',
        "title": 'Engineering management, career roadmap in Japan',
        "summary": ('From tech lead to VP Engineering. Five stages with people-leadership skills, salary bands, and '
 'notes on managing across Japanese and international engineering cultures.'),
        "stages": [   {   'title': 'Tech Lead',
        'years': '6-9 yrs eng experience',
        'salary': '¥13M – ¥18M',
        'skills': [   'Lead 3–6 engineers on a project; still write meaningful code (~30% of '
                      'time).',
                      'Run sprint planning, retros, technical reviews.',
                      'Author design docs; drive technical decision-making in disagreements.',
                      'Mentor 1–2 mid engineers actively.',
                      'Partner with PM and design as the engineering voice of the team.'],
        'promotion_to_next': 'Lead one cross-team initiative end-to-end. Mentor one engineer to '
                             'promotion. Be in the room when staffing decisions are made.',
        'japan_specifics': [   'Tech lead roles at foreign-cap Tokyo are well-defined '
                               'IC-leadership roles; many Japanese employers conflate this with '
                               'manager.',
                               'TLs at Mercari, PayPay, FAANG Tokyo clear ¥14–18M total comp.']},
    {   'title': 'Engineering Manager (EM)',
        'years': '9-12 yrs',
        'salary': '¥16M – ¥24M',
        'skills': [   'Manage 5–10 engineers across mixed seniority; own 1:1s, performance '
                      'reviews, growth plans.',
                      'Hire 2–4 engineers per year; partner with recruiting on sourcing strategy.',
                      'Run engineering operations: backlog, delivery forecasting, on-call '
                      'rotations.',
                      'Coach engineers through performance issues; manage hard conversations.',
                      'Stop coding day-to-day; pair with TL on technical direction instead.'],
        'promotion_to_next': 'Build a team that delivers consistently across 2–3 quarters. Promote '
                             '2+ engineers. Hire 5+ engineers above bar.',
        'japan_specifics': [   "EM roles in Japan increasingly use the US-style 'manager of ICs' "
                               'model at Mercari, SmartNews, FAANG Tokyo.',
                               'At Japanese-headquartered companies, EM often combines with bucho '
                               '(部長) responsibilities, broader scope but more bureaucratic.',
                               'Bilingual EMs at PayPay, Cyberagent, Rakuten command top of band '
                               'due to bridge-management capacity.']},
    {   'title': 'Senior EM / Manager of Managers',
        'years': '12-15 yrs',
        'salary': '¥22M – ¥30M',
        'skills': [   'Manage 2–4 first-line EMs covering 20–40 engineers.',
                      'Set hiring plan and budget at the organisational level.',
                      'Develop the manager bench: coach EMs into senior EMs.',
                      'Partner with director-band peers in product, design, data.',
                      'Run quarterly business reviews; partner with finance on headcount '
                      'planning.'],
        'promotion_to_next': 'Develop 1+ EM into a senior EM. Run a 12-month plan that ships on '
                             'time. Earn director-level endorsement.',
        'japan_specifics': [   'Senior EMs at FAANG Tokyo commonly clear ¥25–30M total with '
                               'significant equity.',
                               'Mercari, SmartNews, PayPay senior EM bands are ¥22–28M with '
                               'smaller equity.']},
    {   'title': 'Director of Engineering',
        'years': '15-18 yrs',
        'salary': '¥28M – ¥40M',
        'skills': [   'Own an engineering function (platform, product engineering, infrastructure) '
                      'at 50–100+ engineers.',
                      'Set multi-year technical strategy; partner with VP Eng and CTO.',
                      'Develop the senior EM bench: coach senior EMs to director.',
                      'Run executive-level OKRs; defend roadmap trade-offs to CEO/CTO.',
                      'Represent engineering externally: hiring brand, conferences, technical '
                      'recruiting.'],
        'promotion_to_next': 'Own a multi-year strategic outcome (platform migration, scale-out, '
                             'new product line). Develop 2+ senior EMs. Earn VP-level endorsement.',
        'japan_specifics': [   'Director of Engineering at FAANG Tokyo: ¥30–40M base + significant '
                               'RSUs (¥15–30M/yr at vest).',
                               'Director at Japanese tech (Mercari, PayPay): ¥28–35M total with '
                               'smaller equity.']},
    {   'title': 'VP Engineering / CTO',
        'years': '18+ yrs',
        'salary': '¥35M – ¥80M+',
        'skills': [   'Own the engineering function at the company or major-division level.',
                      'Be a credible peer to CEO, head of product, head of design.',
                      'Set the technical strategy and operating model for the entire engineering '
                      'org.',
                      'Build the leadership team: directors, senior EMs, staff/principal '
                      'engineers.',
                      'External representation: investor pitches, board updates, technical talent '
                      'brand.'],
        'japan_specifics': [   'VP Eng at Japanese SaaS scale-ups (freee, Money Forward, Sansan) '
                               'clears ¥35–50M plus meaningful equity.',
                               'CTO at growth-stage Japanese startups: cash often modest (¥25–35M) '
                               'but equity packages can be 1–5% with materially higher exit '
                               'upside.',
                               'VP Eng at FAANG Tokyo equivalent (Indeed, Stripe Tokyo): ¥50–80M '
                               'total with high RSU loads.']}],
        "common_pivots": [   '→ EM → Staff Engineer: many EMs return to IC at staff/principal level after a few years of '
    'management. Comp is comparable.',
    '→ Director → CTO at a startup: classic late-career move; equity-heavy compensation profile.',
    '→ VP Eng → COO / GM: a few VPs transition into general management at scale-ups.',
    '→ CTO → VC operator-partner: increasingly common at Tokyo growth-stage funds.',
    '→ Founder: many ex-EMs at Mercari, PayPay, Indeed have founded their own startups.'],
    },
]


# ---------------------------------------------------------------------------
# Phase 6: Pillar guides, long-form SEO content
# ---------------------------------------------------------------------------

PILLAR_GUIDES: list[dict] = [
    {
        "slug": "visa-deep-dive",
        "icon": "clipboard",
        "title": "The complete Japan work visa guide for foreigners",
        "summary": "Everything we know about Japan's work visas in one place: who qualifies, what it costs, how long it takes, common pitfalls.",
        "read_time": "12 min",
        "toc": [
            ("overview",      "Overview: which visa fits your situation"),
            ("engineer",      "Engineer / Specialist in Humanities (most common)"),
            ("hsp",           "Highly Skilled Professional (HSP)"),
            ("business",      "Business Manager"),
            ("instructor",    "Instructor"),
            ("workinghol",    "Working Holiday"),
            ("jfind",         "Designated Activities (J-Find)"),
            ("spouse",        "Spouse visa"),
            ("documents",     "Documents you'll need"),
            ("timeline",      "Realistic timeline"),
            ("pitfalls",      "Common pitfalls"),
            ("transitions",   "Transitioning visa types"),
            ("pr",            "Path to permanent residence"),
        ],
        "body": """
<h2 id="overview">Overview: which visa fits your situation</h2>
<p>Japan has 27 types of residence status, but the ones most foreigners care about are six work
visas, a couple of "designated activities" categories, and the spouse / dependent visas.</p>
<p>The quickest way to figure out which one fits you: run our
<a href="/tools/visa-eligibility">visa eligibility checker</a>, then come back here for the
deep dive. The HSP threshold can also be checked with the
<a href="/tools/hsp-points">HSP points calculator</a>.</p>

<h2 id="engineer">Engineer / Specialist in Humanities / International Services</h2>
<p>The default work visa for most foreigners in tech, finance, business, design, marketing,
translation, and language teaching. About 70% of new working-visa approvals fall under this
category.</p>
<h3>Who qualifies</h3>
<ul>
  <li>Bachelor's degree in a field relevant to the job, <strong>OR</strong></li>
  <li>10+ years of practical work experience in the field (less common, harder to prove), <strong>OR</strong></li>
  <li>For language-teaching specifically: bachelor's degree (any field) + proven language skills.</li>
</ul>
<h3>Sponsorship</h3>
<p>An employer has to sponsor your application. You can't apply for this visa speculatively
without a job offer.</p>
<h3>Cost</h3>
<p>The Certificate of Eligibility (COE) costs ¥0 if filed by your employer in Japan. The visa
sticker at the embassy is roughly ¥3,000 single-entry / ¥6,000 multi.</p>
<h3>Duration</h3>
<p>Granted in 1, 3, or 5-year increments. Renewable indefinitely.</p>

<h2 id="hsp">Highly Skilled Professional (HSP), Type 1(b)</h2>
<p>The "fast lane" visa. Points-based; you need 70+ to qualify for the 5-year HSP visa, or 80+
for the 1-year permanent-residency fast track.</p>
<p>Run the <a href="/tools/hsp-points">HSP calculator</a> to score yourself. The most common
ways to hit 70 are:</p>
<ul>
  <li>Master's (20) + 7 yrs experience (15) + age &lt;35 (10) + ¥7M salary (25) = 70</li>
  <li>Bachelor's (10) + 5 yrs (10) + age &lt;30 (15) + ¥6M (20) + JLPT N1 (15) = 70</li>
  <li>PhD (30) + 5 yrs (10) + age &lt;35 (10) + ¥7M (25) = 80</li>
</ul>

<h2 id="business">Business Manager</h2>
<p>For founders and executives running a Japan-registered business.</p>
<h3>Requirements</h3>
<ul>
  <li>Real office (no virtual offices accepted).</li>
  <li>¥5M minimum capital investment.</li>
  <li>Either two full-time non-foreign staff OR ¥5M+ in operational expenses each year.</li>
  <li>A credible business plan.</li>
</ul>
<p>Immigration officers may physically visit your office. Be prepared.</p>

<h2 id="instructor">Instructor</h2>
<p>Specifically for K-12 teachers at Japanese elementary, junior-high, and high schools.
Eikaiwa (English conversation school) and corporate teaching roles use Engineer/Specialist
instead, not Instructor.</p>

<h2 id="workinghol">Working Holiday</h2>
<p>If you're 18-30 (some countries 18-25), citizen of one of 27 partner countries, and meet
the financial requirements (typically ¥250K liquid assets at entry), you can apply for a 6-12
month working holiday visa.</p>
<p>It's not a path to long-term residence, but it's an excellent way to test Japan before
committing.</p>

<h2 id="jfind">Designated Activities (J-Find)</h2>
<p>Introduced in 2023 for graduates of top-ranked global universities. Gives you up to 2 years
in Japan to find work.</p>

<h2 id="spouse">Spouse visa</h2>
<p>If your spouse is a Japanese citizen or PR holder, this is the simplest visa. Unrestricted
work rights, eligible for PR after 3 years, and you stop being a visa liability for employers.</p>

<h2 id="documents">Documents you'll need</h2>
<p>Universal: passport, photos (4×3 cm), application form. Plus visa-specific items:</p>
<ul>
  <li><strong>Engineer/Specialist:</strong> diploma + transcript, employer's company registration, employment contract.</li>
  <li><strong>HSP:</strong> all of the above + point sheet + supporting documents (JLPT certificate, etc.).</li>
  <li><strong>Business Manager:</strong> business plan, office lease, capital deposit proof, hiring records.</li>
  <li><strong>Spouse:</strong> marriage certificate (Japanese family register if applicable), spouse's residence card or koseki.</li>
</ul>
<p>Use our <a href="/tools/visa-timeline">visa timeline tool</a> to get a checklist
specific to your situation.</p>

<h2 id="timeline">Realistic timeline</h2>
<ul>
  <li>Engineer/Specialist via Japanese employer: COE takes 4-12 weeks, visa sticker 3-5 days, total ~2-4 months.</li>
  <li>HSP: similar to E/S but officers may take longer if points are borderline (~8-14 weeks).</li>
  <li>Business Manager: 8-16 weeks plus 2-3 months of pre-setup (registering company, opening office).</li>
</ul>

<h2 id="pitfalls">Common pitfalls</h2>
<ul>
  <li><strong>Mismatched job and degree:</strong> a CS grad applying for a marketing role gets refused under E/S. You'd need 10+ years of marketing experience to compensate.</li>
  <li><strong>Salary below the minimum:</strong> ¥3M floor for E/S in practice. HSP requires ¥3M absolute minimum.</li>
  <li><strong>Working before COE arrives:</strong> illegal. Wait.</li>
  <li><strong>Employer trouble:</strong> if your sponsoring employer goes bankrupt or your visa is for a job that ends, you have 3 months to find a new sponsor.</li>
  <li><strong>Visa-status mismatch:</strong> doing a job your visa doesn't permit (e.g., teaching on a marketing visa) can trigger refusal of future renewals.</li>
</ul>

<h2 id="transitions">Transitioning between visa types</h2>
<p>Common transitions:</p>
<ul>
  <li>Working Holiday → Engineer/Specialist (must find sponsor before WH expires).</li>
  <li>Engineer/Specialist → HSP (apply once you score 70+).</li>
  <li>Engineer/Specialist or HSP → Business Manager (founding a company).</li>
  <li>Any work visa → Spouse (marriage).</li>
</ul>

<h2 id="pr">Path to permanent residence</h2>
<p>Standard path: 10 years of continuous residence in Japan, with 5+ of those on a working visa.
HSP shortcuts this: 80+ points = PR in 1 year; 70+ points = PR in 3 years.</p>
<p>Spouse visa holders: PR in 3 years (or 1 year if married 3+ years and resident 1 year).</p>
""",
    },
    {
        "slug": "negotiation-playbook",
        "icon": "compass",
        "title": "Salary negotiation playbook for Japan",
        "summary": "Japanese salary negotiation has different rules than the West. Here's what works, what backfires, and how to ask for 15% more without losing the offer.",
        "read_time": "8 min",
        "toc": [
            ("philosophy",   "The cultural philosophy"),
            ("when",         "When to negotiate"),
            ("how-much",     "How much to ask for"),
            ("scripts",      "Scripts that work"),
            ("non-cash",     "Non-cash negotiations"),
            ("pitfalls",     "Pitfalls to avoid"),
            ("counter",      "Handling 'final offer'"),
        ],
        "body": """
<h2 id="philosophy">The cultural philosophy</h2>
<p>Japanese hiring culture views salary negotiation as a normal but understated process.
You're allowed, even expected, to negotiate, but the tone is different: collaborative,
deferential, with specific justifications, and almost never confrontational. The goal is to
arrive at a number both sides feel good about.</p>

<h2 id="when">When to negotiate</h2>
<ul>
  <li><strong>After the offer arrives, before signing.</strong> Never during interviews, the
      "salary expectations" question early on is a tripwire, not the start of negotiation.</li>
  <li><strong>If you have a competing offer.</strong> This is the strongest lever.</li>
  <li><strong>If your current comp is meaningfully higher.</strong> A 10-15% raise minimum is
      standard for switching companies in Japan; less than that and you should push back.</li>
</ul>

<h2 id="how-much">How much to ask for</h2>
<p>Reasonable asks in Japan:</p>
<ul>
  <li><strong>Base salary:</strong> 5-15% above the offer is normal. 20%+ is aggressive and
      should be backed by a competing offer or unambiguous market data.</li>
  <li><strong>Signing bonus:</strong> often easier to win than base, especially at smaller companies. ¥500K-¥3M is typical.</li>
  <li><strong>Annual bonus structure:</strong> ask how the bonus is calculated and whether
      it's discretionary or formula-based. Convert vague language into specific numbers.</li>
</ul>

<h2 id="scripts">Scripts that work</h2>
<p>The script that consistently lands:</p>
<blockquote style="background:var(--line-soft); border:1px solid var(--line); padding:10px 14px; margin:14px 0; font-style:italic;">
"Thank you for the offer. I'm genuinely excited about joining {company} as {role}.
Before I formally accept, I'd like to discuss base salary. Based on {a specific anchor, my current comp / a competing offer / market data}, I was hoping for {specific number}.
Would the team have room to revisit?"
</blockquote>
<p>Three things this script gets right:</p>
<ol>
  <li>Leads with gratitude, Japanese recipients perceive any negotiation as somewhat tense
      and lowering the temperature first reduces friction.</li>
  <li>Names a specific anchor, vague "I think I'm worth more" lands poorly.</li>
  <li>Uses "Would the team have room" instead of "Will you give me", gives the recruiter
      face to negotiate internally.</li>
</ol>
<p>Our <a href="/templates">email templates</a> include this script in both English and
Japanese with prefilled placeholders.</p>

<h2 id="non-cash">Non-cash negotiations</h2>
<p>Often easier to win than base:</p>
<ul>
  <li><strong>Signing bonus:</strong> see above.</li>
  <li><strong>Stock / RSU grants:</strong> at FAANG and large pre-IPO companies; ask explicitly about refresh schedule and vesting.</li>
  <li><strong>Annual training budget:</strong> ¥200K-¥500K is increasingly common at gaijin-friendly companies.</li>
  <li><strong>Remote work days:</strong> 2-3 days/week is negotiable; 100% remote is harder but happens.</li>
  <li><strong>Relocation package:</strong> shipping container, 30-90 days of corporate housing,
      Japanese lessons, family relocation assistance.</li>
  <li><strong>Start date:</strong> push it 4-8 weeks if you need to wrap up current commitments.</li>
</ul>

<h2 id="pitfalls">Pitfalls to avoid</h2>
<ul>
  <li><strong>Don't give a hard number during interviews.</strong> "Open to fair-market comp"
      or "I'm researching" is fine until the offer comes.</li>
  <li><strong>Don't bluff about competing offers.</strong> Japanese recruiters check more than
      you'd think; getting caught burns the offer and your reputation.</li>
  <li><strong>Don't go silent for days.</strong> Acknowledge offers within 24 hours, even if
      it's "thank you, I'd like a week to think it over".</li>
  <li><strong>Don't escalate to 'final' too early.</strong> Always leave a way for both sides
      to save face after a counter-offer.</li>
</ul>

<h2 id="counter">Handling 'this is our final offer'</h2>
<p>Most "final offers" in Japan aren't actually final, but they signal you're approaching
the edge. Options:</p>
<ul>
  <li><strong>Accept gracefully</strong> if the gap is small (less than ¥500K) and the role is
      otherwise strong.</li>
  <li><strong>Walk away gracefully</strong> if the gap is large. Use our
      <a href="/templates">decline email template</a>, keep the door open. You may want to
      apply again in 18 months.</li>
  <li><strong>Pivot to non-cash.</strong> "I appreciate the base is fixed, would there be room
      on the signing bonus or vesting acceleration?"</li>
</ul>
""",
    },
    {
        "slug": "first-90-days",
        "icon": "calendar",
        "title": "Your first 90 days in Japan, a practical checklist",
        "summary": "What to do in your first week, first month, and first three months in Japan, banking, phones, hanko, taxes, social. The boring-but-essential stuff.",
        "read_time": "10 min",
        "toc": [
            ("airport",      "Day 1: at the airport"),
            ("week1",        "Week 1: residence card, address registration, phone"),
            ("month1",       "Month 1: bank account, hanko, MyNumber"),
            ("month2",       "Month 2: National Health, pension, tax 101"),
            ("month3",       "Month 3: language, social, hobbies, money habits"),
            ("apartment",    "The apartment question"),
            ("don't",        "Things you don't need to do (despite the internet)"),
        ],
        "body": """
<h2 id="airport">Day 1: at the airport</h2>
<p>At immigration, you'll receive your residence card (在留カード). Keep it on you at all times, it's legally required. Your work visa is now active.</p>
<p>Most international airports have free WiFi and a JR ticket counter. Pick up an IC card
(Suica or Pasmo) before leaving the airport, it'll be your transit pass and convenience-store
payment method for the entire stay.</p>

<h2 id="week1">Week 1: residence card, address registration, phone</h2>
<p>Once you have a permanent address (even temporary corporate housing counts), you have
14 days to register at your local ward office (区役所). Without this, you can't open a bank
account or get a phone plan.</p>
<p>What to bring: passport, residence card, lease or rental agreement.</p>
<p>What you'll leave with: residence registration certificate (住民票), and your address gets
printed on the back of your residence card.</p>
<h3>Phone</h3>
<p>Mainstream carriers (Docomo, Softbank, au) require a Japanese bank account, so most
foreigners start with an MVNO that accepts foreign credit cards: <strong>IIJmio</strong>,
<strong>povo 2.0</strong>, <strong>mineo</strong>, or <strong>Sakura Mobile</strong>.</p>
<p>Plans are ¥1,500-¥3,000/month for 5-20 GB. Set this up first; you'll need a Japanese phone
number for every subsequent step.</p>

<h2 id="month1">Month 1: bank account, hanko, MyNumber</h2>
<h3>Bank account</h3>
<p>The bilingual-friendly banks: <strong>Shinsei Bank</strong>, <strong>Sony Bank</strong>,
<strong>Rakuten Bank</strong>, <strong>SBI Sumishin Net Bank</strong>. JP Post Bank (ゆうちょ)
is the universal fallback. Visit a branch; bring residence card + phone + apartment address +
hanko (optional but often requested).</p>
<h3>Hanko (印鑑)</h3>
<p>The personal seal used in place of a signature on Japanese paperwork. Most newer banks
accept signatures, but you'll eventually need one for apartments, employment paperwork, or
buying a car. Order one online (¥3,000-¥10,000), kanji, katakana, or romaji all work.</p>
<h3>MyNumber card (マイナンバーカード)</h3>
<p>Your tax/social-security ID. You'll receive a notification at your registered address
within a couple of weeks. Then visit the ward office to convert it into the plastic card.
You'll need it for tax filing, health-insurance changes, and government services.</p>

<h2 id="month2">Month 2: National Health, pension, tax 101</h2>
<h3>National Health Insurance (国民健康保険), but actually 社会保険</h3>
<p>If you're employed full-time, your employer enrolls you in 社会保険 (employee health
insurance + pension) and withholds the premiums from your paycheck. You don't need to do
anything yourself for this. Around 14.7% of gross salary goes to social insurance + pension.</p>
<p>If you're freelance / unemployed for the first month, you'll enroll directly at the ward
office in 国民健康保険 (National Health Insurance) instead.</p>
<h3>Annual tax filing</h3>
<p>Employed: your employer handles year-end adjustment (年末調整). You don't file unless you
have other income.</p>
<p>Freelance, or earnings over ¥20M, or itemized deductions: file
<strong>確定申告</strong> (kakutei shinkoku) between February 16 and March 15 of the following
year. Use the <a href="/tools/take-home-pay">take-home pay calculator</a> to model your
liability.</p>

<h2 id="month3">Month 3: language, social, hobbies, money habits</h2>
<ul>
  <li><strong>Language:</strong> commit to a JLPT level and a timeline. JLPT exams run every
      July and December. Most foreigners benefit from N5/N4 in their first 6 months, enough
      to read menus, ask directions, handle ward-office paperwork.</li>
  <li><strong>Social:</strong> join 1-2 communities. See our <a href="/community">community list</a>.</li>
  <li><strong>Money habits:</strong> Japan still has a strong cash culture, but tap-to-pay is
      now ubiquitous (Suica/Pasmo, QR codes like PayPay/LinePay). Most utility bills get
      direct-debited; ATM fees can be ¥220 outside business hours.</li>
</ul>

<h2 id="apartment">The apartment question</h2>
<p>If your employer offers corporate housing for 30-90 days, take it. Apartment hunting
is much easier once you have:</p>
<ol>
  <li>A residence card with your registered address.</li>
  <li>A Japanese bank account.</li>
  <li>A Japanese phone number.</li>
  <li>A pay stub (給与明細) showing income, ideally 1-3 months.</li>
</ol>
<p>Foreigner-friendly agencies: <strong>GaijinPot Housing</strong>, <strong>Ken Real Estate</strong>,
<strong>Apartment Japan</strong>, <strong>Sakura House</strong> (short-term). Most charge 1
month rent as commission; plus 1-2 months key money, 1-2 months deposit, 1 month rent in
advance. Budget ¥300K-¥600K for move-in costs.</p>

<h2 id="don't">Things you don't need to do (despite the internet)</h2>
<ul>
  <li><strong>Carry yen in cash everywhere.</strong> Suica + a credit card covers 95% of urban purchases.</li>
  <li><strong>Get a hanko before arriving.</strong> Order it after your name's on your
      residence card; the kanji/katakana spelling needs to match.</li>
  <li><strong>Bring a year's worth of medication.</strong> Japan allows a 1-month supply of
      prescription drugs into the country without a special permit; for longer you'd need a
      yakkan shoumei (薬監証明) form, but most foreigners just refill via a Japanese clinic.</li>
  <li><strong>Buy a car immediately.</strong> Tokyo / Osaka / Yokohama don't need one. Outside
      major metros, yes, but get settled first.</li>
</ul>
""",
    },
]


# ---------------------------------------------------------------------------
# Phase 6: Glossary of Japanese hiring terms
# ---------------------------------------------------------------------------

GLOSSARY: list[dict] = [
    {"term": "Aiseki (相席)", "category": "Workplace",
     "definition": "Sharing a table/seating with strangers, common at lunch counters and some izakaya. You'll experience this in corporate Japan during company outings."},
    {"term": "Bonenkai (忘年会)", "category": "Workplace",
     "definition": "End-of-year company drinking party held in December, literally 'forget-the-year gathering'. Attendance is socially expected but not technically mandatory."},
    {"term": "Burakku kigyou / Black company (ブラック企業)", "category": "Warning",
     "definition": "Slang for an exploitative employer, long unpaid hours, harassment, no career growth. Check for it in reviews before signing."},
    {"term": "Daikigyou (大企業)", "category": "Company types",
     "definition": "Large established Japanese corporation, Toyota, Mitsubishi, Sony, etc. Stable employment, slow career progression, strong benefits, conservative culture."},
    {"term": "Eigyō (営業)", "category": "Role",
     "definition": "Sales / business development. Different from Western sales, heavy on relationship cultivation, lower on quota-driven aggression."},
    {"term": "Eikaiwa (英会話)", "category": "Industry",
     "definition": "English conversation school. Largest employer of English-speaking foreigners in Japan. Pay is low (¥3-4M/yr), turnover is high."},
    {"term": "Furigana (ふりがな)", "category": "Document",
     "definition": "Phonetic reading written above or beside kanji. Required on your rirekisho for your name + address."},
    {"term": "Gaishikei (外資系)", "category": "Company types",
     "definition": "Foreign-capital companies, Google Japan, Goldman Sachs, Microsoft. Typically higher pay, more English, more aggressive performance management."},
    {"term": "Genka (現価)", "category": "Compensation",
     "definition": "Current salary. Recruiters will ask 現価はいくらですか, 'what's your current pay?'"},
    {"term": "Hanko / Inkan (印鑑)", "category": "Document",
     "definition": "Personal seal used in place of a signature on Japanese documents. Order one once you have your residence card."},
    {"term": "Henji (返事)", "category": "Process",
     "definition": "A reply, specifically the formal response (yes/no) you give the company after they make an offer. Standard to ask for a week to respond."},
    {"term": "Hojin (法人)", "category": "Business",
     "definition": "A legal corporate entity. Required for the Business Manager visa."},
    {"term": "Honne / Tatemae (本音・建前)", "category": "Culture",
     "definition": "True feelings vs. public stance. Critical for reading Japanese interviewers, what they say first is rarely what they truly mean."},
    {"term": "HSP (高度専門職)", "category": "Visa",
     "definition": "Highly Skilled Professional visa. Points-based; 70+ = 5-yr visa with PR in 3 yrs; 80+ = PR in 1 yr. Run the calculator at /tools/hsp-points."},
    {"term": "Jikyū (時給)", "category": "Compensation",
     "definition": "Hourly wage. Used for part-time and contract roles."},
    {"term": "Joushi (上司)", "category": "Workplace",
     "definition": "Direct manager / boss. Hierarchy matters in Japanese offices; never address your joushi by first name."},
    {"term": "JLPT (日本語能力試験)", "category": "Certification",
     "definition": "Japanese-Language Proficiency Test. Levels N5 (basic) to N1 (native-ish). N2+ unlocks most bilingual roles."},
    {"term": "Kaisha-in (会社員)", "category": "Workplace",
     "definition": "Company employee, the default identity in Japanese society. Used on the rirekisho occupation field."},
    {"term": "Kaizen (改善)", "category": "Culture",
     "definition": "Continuous improvement. A core Japanese workplace value, bring evidence of kaizen mindset to engineering interviews."},
    {"term": "Keigo (敬語)", "category": "Language",
     "definition": "Formal honorific Japanese. Used in business contexts. Spoken keigo is a JLPT N2+ skill; written is easier (templates exist)."},
    {"term": "Kokumin Kenko Hoken (国民健康保険)", "category": "Benefits",
     "definition": "National Health Insurance, for self-employed, students, unemployed. Most foreign workers are on 社会保険 (employer-sponsored) instead."},
    {"term": "Koseki (戸籍)", "category": "Document",
     "definition": "Japanese family register. You don't have one (foreigners aren't on koseki), but your Japanese spouse does, relevant for spouse visas."},
    {"term": "Meishi (名刺)", "category": "Workplace",
     "definition": "Business card. Receive with both hands, study briefly, place on the table in front of you. Never write on it or stuff it in a pocket."},
    {"term": "Naitei (内定)", "category": "Process",
     "definition": "Informal offer / 'we want to hire you'. Comes before the formal employment contract. Acceptance (内定承諾) is somewhat binding socially but not legally."},
    {"term": "Nemawashi (根回し)", "category": "Process",
     "definition": "Building consensus informally before formal meetings. A core skill for senior IC and PM roles in Japan."},
    {"term": "Nenshu (年収)", "category": "Compensation",
     "definition": "Annual income. Almost always means base + bonus. Always confirm whether bonus is included when receiving offers."},
    {"term": "Nōkai (能力)", "category": "Skills",
     "definition": "Ability / competency. Used in performance reviews."},
    {"term": "Ojigi (お辞儀)", "category": "Culture",
     "definition": "Bowing. 15° for casual workplace greetings, 30° for formal meetings, 45° for apologies or addressing executives."},
    {"term": "OL (オーエル)", "category": "Role",
     "definition": "'Office Lady', slightly dated term for female office workers. You'll still see it in some job listings."},
    {"term": "Onsha (御社)", "category": "Language",
     "definition": "Polite way to say 'your (esteemed) company' in spoken Japanese, especially during interviews. Written equivalent: 貴社 (kisha)."},
    {"term": "Permanent Residence / PR (永住権)", "category": "Visa",
     "definition": "Unrestricted right to live and work in Japan. Standard path: 10 years. HSP fast-track: 3 yrs (70+ pts) or 1 yr (80+ pts)."},
    {"term": "Rirekisho (履歴書)", "category": "Document",
     "definition": "Standardized Japanese resume, personal info, education, work history, certs, motivation. Build one at /resume."},
    {"term": "Sanitary (三日坊主)", "category": "Slang",
     "definition": "Literally 'three-day monk', someone who gives up quickly. Recruiters look for evidence you'll stay."},
    {"term": "Sashizu (指図)", "category": "Workplace",
     "definition": "Direct instruction. Japanese managers often avoid giving sashizu, preferring suggestion. Read context, not just words."},
    {"term": "Senpai / Kohai (先輩・後輩)", "category": "Workplace",
     "definition": "Senior/junior relationship by tenure. Affects who pays at drinks, who speaks first in meetings, who introduces whom."},
    {"term": "Shachō (社長)", "category": "Workplace",
     "definition": "Company president / CEO. Address as '社長' or '[surname]社長'."},
    {"term": "Shakai Hoken (社会保険)", "category": "Benefits",
     "definition": "Employer-sponsored social insurance: health + pension + employment insurance. ~14.7% of gross deducted from your paycheck."},
    {"term": "Shōkai (紹介)", "category": "Process",
     "definition": "Referral / introduction. A 紹介 from an existing employee often skips initial screening."},
    {"term": "Shokumu keirekisho (職務経歴書)", "category": "Document",
     "definition": "Career-history document, Japan's equivalent of a Western CV. More flexible than rirekisho. Build one at /resume/shokumu."},
    {"term": "Sōkatsu (総括)", "category": "Workplace",
     "definition": "Summary / wrap-up. End-of-project retrospectives are usually called 総括 in Japanese workplaces."},
    {"term": "Sponsorship (スポンサーシップ)", "category": "Visa",
     "definition": "Employer-arranged visa application. Most foreign workers need it. Filter the job board for /jobs?visa_sponsorship_mentioned=1."},
    {"term": "Tax shōmei (納税証明)", "category": "Document",
     "definition": "Tax payment certificate from the ward office. Often required for visa renewals and apartment applications."},
    {"term": "Tedori (手取り)", "category": "Compensation",
     "definition": "Take-home pay, gross minus social insurance, income tax, residence tax. Use /tools/take-home-pay to estimate."},
    {"term": "Vacation (有給休暇 / yūkyū kyūka)", "category": "Benefits",
     "definition": "Paid vacation. 10 days minimum after 6 months of employment; rises with tenure. Use of yūkyū is socially discouraged at conservative Japanese companies."},
    {"term": "Wago / Jōgo (和語・上語)", "category": "Language",
     "definition": "Native Japanese vocabulary (wago) vs. Sino-Japanese (kango). Business Japanese leans kango. Use 'gokijou (御希望)' not 'nozomi (望み)' in formal emails."},
    {"term": "Yakuin (役員)", "category": "Workplace",
     "definition": "Executive officer. Director-level and above. Different employment contract from regular employees (kaisha-in)."},
    {"term": "Yen / ¥ (円)", "category": "Money",
     "definition": "Japanese currency. Job offers are usually denominated in 万円 (man-yen), 1 man = ¥10,000. '600 man' = ¥6,000,000/yr."},
    {"term": "Zairyū Card (在留カード)", "category": "Document",
     "definition": "Residence card. Issued at the airport on arrival. Must be carried at all times. Renew with your visa."},
    {"term": "Zangyou (残業)", "category": "Workplace",
     "definition": "Overtime. Legally capped at 45 hr/month, 360 hr/year in most industries. Service zangyou (unpaid overtime) is a major red flag, see /resources/red-flags."},
]


# ---------------------------------------------------------------------------
# Community groups
# ---------------------------------------------------------------------------

COMMUNITY_GROUPS: list[dict] = [
    {
        "category": "Chat groups",
        "icon": "message",
        "links": [
            {"name": "Tokyo Dev Slack",
             "url": "https://www.tokyodev.com/community",
             "desc": "5,000+ English-speaking software engineers in Tokyo. The single highest-signal community for foreign engineers."},
            {"name": "r/movingtojapan",
             "url": "https://www.reddit.com/r/movingtojapan/",
             "desc": "Visa questions, paperwork, first-90-days topics. Active moderation."},
            {"name": "r/japanlife",
             "url": "https://www.reddit.com/r/japanlife/",
             "desc": "Daily life as a foreigner, apartments, taxes, banks, social etiquette."},
            {"name": "Tokyo Tech Mafia",
             "url": "https://www.tokyotechmafia.com/",
             "desc": "Invite-only community for senior engineers and engineering leaders in Tokyo."},
        ],
    },
    {
        "category": "Meetups & events",
        "icon": "calendar",
        "links": [
            {"name": "Tokyo Dev meetups",
             "url": "https://www.tokyodev.com/events",
             "desc": "Monthly in-person meetups for foreign engineers in Tokyo."},
            {"name": "Japan Rust Tokyo",
             "url": "https://rust.tokyo/",
             "desc": "Annual Rust conference held in Tokyo."},
            {"name": "Tokyo JS",
             "url": "https://tokyojs.com/",
             "desc": "JavaScript / TypeScript meetup, mixed English/Japanese."},
            {"name": "Startup Grind Tokyo",
             "url": "https://www.startupgrind.com/tokyo/",
             "desc": "Founder-focused events, mostly bilingual."},
        ],
    },
    {
        "category": "Podcasts & newsletters",
        "icon": "megaphone",
        "links": [
            {"name": "Disrupting Japan",
             "url": "https://www.disruptingjapan.com/",
             "desc": "Long-running podcast on Japan's startup ecosystem. Hosted by Tim Romero."},
            {"name": "Tokyo Dev's newsletter",
             "url": "https://www.tokyodev.com/newsletter",
             "desc": "Weekly digest of tech roles + the occasional industry report."},
            {"name": "TokyoTechie",
             "url": "https://tokyotechie.com/",
             "desc": "Salary surveys, working-in-Japan deep dives."},
        ],
    },
    {
        "category": "YouTube channels",
        "icon": "eye",
        "links": [
            {"name": "Life Where I'm From",
             "url": "https://www.youtube.com/c/LifeWhereImFrom",
             "desc": "Greg Lam's documentary-style channel on daily life in Japan."},
            {"name": "The Japan Reporter",
             "url": "https://www.youtube.com/c/TheJapanReporter",
             "desc": "Investigative journalism, immigration, foreign-worker policy."},
        ],
    },
    {
        "category": "Useful blogs",
        "icon": "pencil",
        "links": [
            {"name": "TokyoDev",
             "url": "https://www.tokyodev.com/articles",
             "desc": "Engineering-focused career advice, salary surveys, visa guides."},
            {"name": "Tokyo Cheapo",
             "url": "https://tokyocheapo.com/",
             "desc": "Cost-of-living, transit, neighborhoods, written for residents."},
            {"name": "Surviving in Japan",
             "url": "https://www.survivingnjapan.com/",
             "desc": "Practical 'how to do X in Japan', taxes, healthcare, day-to-day."},
        ],
    },
]

# EXTERNAL_DIR_LINK:v1


# ---------------------------------------------------------------------------
# Newer resource pages live in resources_new.py to keep this file manageable.
# Appended here so hubs, sitemap, llms.txt and get_resource() all pick them up.
# ---------------------------------------------------------------------------
from resources_new import EXTRA_RESOURCES as _EXTRA_RESOURCES

for _r in _EXTRA_RESOURCES:
    if not any(x["slug"] == _r["slug"] for x in RESOURCES):
        RESOURCES.append(_r)
