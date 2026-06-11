"""
Non-destructive deep-dive extensions for content.RESOURCES articles.

Rather than edit the large content.py in place (risk to a 400KB+ file), each
resource slug gets an EXTRA block here: additional TOC entries and additional
HTML appended to the end of the existing article body at render time. The Flask
route merges these via merge_resource().

Figures are 2025–26 and grounded in current sources (TokyoDev 2025 Developer
Survey; Immigration Services Agency; Japan Pension Service; MHLW). Orientation,
not legal/financial advice.

Schema per slug:
    "extra_toc":  [(anchor_id, label), ...]   appended to item["toc"]
    "extra_body": "<h2 id=...>...</h2> ..."    appended to item["body"]
"""

RESOURCE_EXTRAS: dict[str, dict] = {

    # ===================================================================== VISAS
    "visa-types": {
        "key_takeaways": [
            "Most foreign professionals enter on the <strong>Engineer / Specialist in Humanities / International Services</strong> visa, it needs a relevant bachelor's degree <em>or</em> 10+ years' experience, and your employer sponsors it.",
            "The <strong>HSP points system</strong> is the fast lane: 70 points → permanent residence after 3 years, 80 points → after just 1 year. Run the HSP calculator before assuming the 10-year route.",
            "Permanent residence now has a published <strong>¥3.5M minimum income (Jan 2026)</strong> and new revocation grounds for willful non-payment of taxes/insurance, pay everything on time, every time.",
            "The <strong>Business Manager visa was tightened in Oct 2025</strong>: ¥30M capital, one full-time employee, and ~JLPT N2 Japanese.",
            "Your visa is sponsored by your employer but <strong>belongs to you</strong>, you can change jobs (notify immigration within 14 days) without losing your status, as long as the new role fits the category.",
        ],
        "faqs": [
            ("Can my employer sponsor my work visa from abroad?",
             "<p>Yes, and this is the normal path. Your employer files the Certificate of Eligibility (COE) with Japanese immigration while you're still abroad; once approved, you convert it to a visa at a Japanese embassy and fly in. The whole process runs about 2–4 months from signed offer. Unlike the US or UK, Japanese employers pay no formal sponsorship fee, though many cover relocation and visa-renewal costs.</p>"),
            ("What's the easiest work visa to get in Japan?",
             "<p>For degree-holders, the <strong>Engineer / Specialist in Humanities / International Services</strong> visa is the workhorse, it covers most office, tech, and professional roles and only requires a relevant bachelor's degree (or 10+ years of relevant experience) plus a job offer. Teaching roles use the Instructor visa, which is similarly accessible. The hardest is the Business Manager visa, tightened in October 2025.</p>"),
            ("How long does the work visa process take?",
             "<p>Plan for <strong>2–4 months end to end</strong>. The Certificate of Eligibility alone takes 1–3 months at immigration, then add ~1 week for the embassy visa and your own move logistics. Filing outside the spring (April) and autumn intake crunches can shave weeks. The 2023 digital COE removes the international-mail leg if your employer opts in.</p>"),
            ("Do I need to speak Japanese to get a work visa?",
             "<p>No, the work visa itself has no language requirement (the Business Manager visa is the exception, now needing ~N2 since Oct 2025). Whether you need Japanese is about the <em>job</em>, not the visa: software, data, and many global-company roles are genuinely English-first. See the <a href='/resources/jlpt-levels'>JLPT guide</a> for what level each field really expects.</p>"),
            ("Can I switch employers without losing my visa?",
             "<p>Yes. Your status of residence is yours, not your employer's. If the new job fits the same visa category, you simply <strong>notify immigration within 14 days</strong> of leaving and of joining. Consider applying for a 'Certificate of Authorized Employment' to pre-confirm the new role qualifies. If the new job is a different category, you change your status of residence rather than just notifying.</p>"),
            ("How do I get permanent residence in Japan?",
             "<p>The standard route is <strong>10 years' continuous residence</strong> (5+ on a work/spouse visa), clean tax and pension records, good conduct, and from January 2026 a <strong>¥3.5M minimum income</strong>. The fast lane is the HSP points system: 70 points cuts it to 3 years, 80 points to just 1 year. The single most common rejection reason is late tax or pension payments, automate everything from day one.</p>"),
        ],
        "extra_toc": [
            ("pr-2026", "Permanent residence, 2026 rules & the new ¥3.5M floor"),
            ("pr-revocation", "PR revocation, the 2026 enforcement change"),
            ("hsp-fast-track", "HSP fast-track to PR (1 or 3 years)"),
            ("bizmgr-2025", "Business Manager, the Oct 2025 tightening"),
            ("status-vs-activity", "Status-based vs activity-based visas"),
            ("renewal", "Renewals, the practical playbook"),
            ("job-change", "Changing jobs without losing your visa"),
            ("naturalization", "Naturalization vs permanent residence"),
            ("visa-faq", "Visa FAQ, the questions people actually ask"),
        ],
        "extra_body": """
<hr>
<h2 id="pr-2026">Permanent residence, 2026 rules & the new ¥3.5M floor</h2>
<p>Permanent residence (永住, <em>eijū</em>) is the goal for most long-term foreigners: no visa
renewals, no occupation restriction, and the strongest footing short of citizenship. The standard
route requires:</p>
<ul>
  <li><strong>10+ years continuous residence</strong> in Japan, with <strong>5+ years on a
      work or spouse visa</strong> (the rest can be student/dependent time).</li>
  <li><strong>Good conduct</strong>, no meaningful criminal record, clean driving history matters
      at the margins.</li>
  <li><strong>Tax, pension, and health-insurance payments fully up to date</strong>, and paid
      <em>on time</em>, not just eventually. Late payments are the most common rejection reason.</li>
  <li><strong>Stable, sufficient income</strong>, and as of <strong>January 2026</strong>, a new
      published <strong>minimum gross income of ¥3.5 million/year</strong> for new applicants under
      the Comprehensive Measures framework.</li>
  <li>A <strong>guarantor (保証人)</strong>, usually your employer or a permanent-resident/citizen
      friend (a moral guarantor, not financially liable in practice).</li>
</ul>
<div class="callout">The most underrated PR requirement is <strong>paying everything on time for
years</strong>. One forgotten residence-tax bill or a gap in pension contributions can reset your
clock in the eyes of immigration. Set everything to auto-debit the day you arrive.</div>

<h2 id="pr-revocation">PR revocation, the 2026 enforcement change</h2>
<p>A revised Immigration Control Act (effective 2025–26) gives authorities new grounds to
<strong>revoke</strong> permanent residence for: <strong>willful non-payment of taxes or social
insurance</strong>, failure to renew the Residence Card before expiry, failure to notify the ward
office of an address change, and certain criminal convictions.</p>
<div class="warn"><strong>Keep perspective:</strong> in 2025 only <strong>7 PR revocations</strong>
occurred nationwide. This is a new tool aimed at willful evaders, not a crackdown on ordinary
residents. The practical takeaway is simply: keep paying on time and keep your address/card current,
which you should do anyway.</div>

<h2 id="hsp-fast-track">HSP fast-track to PR (1 or 3 years)</h2>
<p>The Highly Skilled Professional (HSP) points system is the fastest legal path to PR:</p>
<ul>
  <li><strong>70+ points</strong> → apply for PR after <strong>3 years</strong>.</li>
  <li><strong>80+ points</strong> → apply for PR after just <strong>1 year</strong>.</li>
</ul>
<p>Points come from academic background, professional career length, annual salary, age (younger
scores higher), Japanese ability (N1/N2 add points), and bonuses (degrees from Japanese universities,
work in growth fields). When you file, you substantiate that you met the threshold both at filing
<em>and</em> retroactively for the qualifying period (1 or 3 years) with points sheets, income
certificates, and qualification proofs. If you're a well-paid professional in your 30s with a
master's degree, 80 points is more reachable than most people assume, run the
<a href="/tools/hsp-points">HSP points calculator</a> before assuming the 10-year route.</p>

<h2 id="bizmgr-2025">Business Manager, the Oct 2025 tightening</h2>
<p>If you're thinking of starting a company in Japan, know that the <strong>Business Manager visa
was significantly tightened in October 2025</strong>. Requirements now include a
<strong>minimum capital of ¥30 million</strong> (up sharply from the old ¥5 million), at least
<strong>one full-time employee</strong>, and <strong>Japanese proficiency around B2 / JLPT N2</strong>
for the applicant. The bar for the entrepreneur route is now materially higher, factor this into
any "move to Japan and start a business" plan.</p>

<h2 id="status-vs-activity">Status-based vs activity-based visas</h2>
<p>A mental model that clears up a lot of confusion:</p>
<table>
  <thead><tr><th>Type</th><th>Examples</th><th>Work rights</th></tr></thead>
  <tbody>
    <tr><td><strong>Activity-based</strong></td><td>Engineer/Specialist, Instructor, Business Manager, HSP</td><td>Restricted to the visa's activity/occupation</td></tr>
    <tr><td><strong>Status-based</strong></td><td>Permanent Resident, Spouse of Japanese National, Long-Term Resident</td><td><strong>Unrestricted</strong>, any work, any job</td></tr>
  </tbody>
</table>
<p>This is why PR and a Japanese-spouse visa are so valuable: they sever the link between your job
and your right to stay. On an activity-based visa, your visa is tied to doing roughly the kind of
work it was granted for.</p>

<h2 id="renewal">Renewals, the practical playbook</h2>
<ul>
  <li>Apply to renew <strong>up to 3 months before</strong> expiry; don't leave it to the last week.</li>
  <li>First renewals are often <strong>1 year</strong>; once you have tenure and clean records you
      typically get <strong>3 or 5 years</strong>, which also strengthens a future PR case.</li>
  <li>Bring: employment certificate (在職証明書), tax payment certificate (納税証明書), and the
      residence-tax certificate (課税証明書). The cleaner your tax record, the longer the period
      they grant.</li>
  <li>The "<strong>Designated Activities</strong>" extensions and the special re-entry permit (みなし
      再入国) let you leave Japan up to 1 year without a separate re-entry permit, but get a real
      re-entry permit if you'll be gone longer.</li>
</ul>

<h2 id="job-change">Changing jobs without losing your visa</h2>
<p>You can change employers on an activity-based visa as long as the new role fits the same visa
category. Key obligations:</p>
<ul>
  <li><strong>Notify immigration within 14 days</strong> of leaving and of joining an employer
      (届出, via the online system or in person).</li>
  <li>Strongly consider applying for a <strong>"Certificate of Authorized Employment"
      (就労資格証明書)</strong> when switching, it pre-confirms your new job qualifies, so your next
      renewal isn't a surprise.</li>
  <li>If the new job is a <em>different</em> category (e.g. moving from Instructor to
      Engineer/Specialist), you must <strong>change your status of residence</strong>, not just
      notify.</li>
</ul>

<h2 id="naturalization">Naturalization vs permanent residence</h2>
<table>
  <thead><tr><th></th><th>Permanent Residence</th><th>Naturalization (citizenship)</th></tr></thead>
  <tbody>
    <tr><td>Keep home passport?</td><td>Yes</td><td>No, Japan doesn't allow dual nationality for adults</td></tr>
    <tr><td>Residence requirement</td><td>~10 yrs (1–3 via HSP)</td><td>~5 yrs, generally</td></tr>
    <tr><td>Vote / Japanese passport?</td><td>No</td><td>Yes</td></tr>
    <tr><td>Can be revoked?</td><td>Yes (new 2026 grounds)</td><td>Effectively no</td></tr>
  </tbody>
</table>
<p>Most foreigners want PR, not naturalization, because giving up your original citizenship is a
big step. Naturalization makes sense mainly for those fully rooted in Japan who don't need their
original passport.</p>

<h2 id="visa-faq">Visa FAQ, the questions people actually ask</h2>
<p><strong>Can I job-hunt in Japan while on a tourist visa?</strong> You can attend interviews, but
you cannot start work, and you'll still need a COE filed by the hiring employer before you can switch
to a work status, usually that means leaving and re-entering on the new visa, or changing status
from within Japan if eligible.</p>
<p><strong>Does my visa cover my side income / freelancing?</strong> Not automatically. An
activity-based work visa covers your sponsored job; significant side income or freelancing may need
permission (資格外活動) or a different status. Small passive income (e.g. investments) is generally
fine.</p>
<p><strong>What happens if I'm laid off?</strong> You typically have a grace period to find a new
qualifying job (immigration may grant a "Designated Activities" job-seeking status). Notify
immigration, and don't let your status lapse, register at Hello Work for unemployment benefits if
you paid employment insurance.</p>
<p><strong>Do years on a student or dependent visa count toward PR?</strong> They count toward the
10-year total, but you still need 5+ of those years on a work or spouse visa.</p>
<div class="callout">Tools: <a href="/tools/visa-eligibility">Visa eligibility checker</a> ·
<a href="/tools/hsp-points">HSP points calculator</a> ·
<a href="/tools/visa-timeline">Visa timeline & checklist</a></div>
"""
    },

    # ====================================================================== JLPT
    "jlpt-levels": {
        "key_takeaways": [
            "<strong>N2 is the practical threshold</strong> for working in a Japanese office; N1 is expected for client-facing or document-heavy roles. Below N2, lean toward international / foreign-capital employers.",
            "Software, data, and many global-company roles are genuinely <strong>English-first</strong>, one TokyoDev survey found ~80% of foreign engineers primarily use English at work. JLPT is a 'nice to have' there.",
            "The JLPT tests reading and listening, <strong>not speaking</strong>, confident N2 speakers regularly beat silent N1 certificate-holders in interviews. Practise conversation in parallel.",
            "Rough study time from zero: <strong>N5 ~400 hrs, N3 ~1,000 hrs, N2 ~1,800 hrs, N1 ~3,000+ hrs</strong>. Most working professionals reach N3–N2 over 2–3 years in-country.",
            "The test runs <strong>twice a year (first Sunday of July and December)</strong>; the certificate never expires.",
        ],
        "faqs": [
            ("What JLPT level do I need to work in Japan?",
             "<p>It depends entirely on the job, not a blanket rule. <strong>English-first tech, data, and global-company roles</strong> often need little or no Japanese. <strong>Most Japanese-company office roles want N2–N1.</strong> Customer-facing and sales roles effectively need N1 plus strong speaking. Teaching English needs none. The practical floor for 'can function in a Japanese workplace' is N2.</p>"),
            ("Can I work in Japan without speaking Japanese?",
             "<p>Yes, many people do. The clearest paths are <strong>software engineering, data/AI, English teaching, and global-company roles</strong> where English is the working language. A TokyoDev survey of 435+ engineers found only about a third are fluent in Japanese while ~80% primarily use English at work. Outside these fields, limited Japanese narrows your options sharply, so target English-first employers deliberately.</p>"),
            ("Is N1 better than N2 for getting hired?",
             "<p>On paper yes, but in practice the gap is smaller than people think, and N1 can even backfire. The JLPT measures reading and listening, not speaking, so hiring managers regularly report that <strong>confident N2 speakers outperform N1 certificate-holders who freeze in conversation</strong>. If a job needs working Japanese, invest in speaking and business communication, not just test grammar.</p>"),
            ("How long does it take to reach JLPT N2?",
             "<p>From zero, roughly <strong>1,500–2,200 study hours</strong>, a multi-year project at a sustainable pace of an hour a day, much faster under full-time immersion. Most working professionals reach N3–N2 over 2–3 years while employed in Japan, which is exactly why landing an English-first first job and studying alongside it is the common winning strategy.</p>"),
            ("When and how often is the JLPT held?",
             "<p>Twice a year, the <strong>first Sunday of July and December</strong>, in Japan and many overseas cities (some overseas locations offer December only). Registration opens months ahead and fills early in popular cities. Results arrive about two months later, and the certificate <strong>never expires</strong>.</p>"),
        ],
        "extra_toc": [
            ("level-by-job", "What level you really need, by job type"),
            ("n1-trap", "The N1 trap, why certificates fail interviews"),
            ("business-japanese", "Business Japanese ≠ JLPT"),
            ("study-plan", "A realistic study plan & hours per level"),
            ("study-tools", "The tool stack that actually works"),
            ("keigo", "Keigo, the politeness layer that matters at work"),
            ("test-logistics", "Test logistics, dates, cost, where"),
        ],
        "extra_body": """
<hr>
<h2 id="level-by-job">What level you really need, by job type</h2>
<table>
  <thead><tr><th>Role / setting</th><th>Realistic JLPT floor</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td>Software eng. at int'l/English-first firm</td><td>None–N4</td><td>N2 a "nice to have"; English is the working language</td></tr>
    <tr><td>Software eng. at Japanese company</td><td>N2 (N3 if coding-only)</td><td>N2 becomes expected the moment collaboration starts</td></tr>
    <tr><td>Most office / business roles</td><td>N2–N1</td><td>Meetings, email, documents in Japanese</td></tr>
    <tr><td>Sales / customer-facing</td><td>N1 + strong speaking</td><td>The test level is the floor, not the bar</td></tr>
    <tr><td>Teaching English (ALT/eikaiwa)</td><td>None</td><td>Japanese helps daily life, not the job</td></tr>
    <tr><td>Finance / consulting (bilingual)</td><td>N1 often required</td><td>Client work in Japanese</td></tr>
  </tbody>
</table>
<div class="callout">The honest rule of thumb most recruiters use: <strong>N2 is the practical
threshold for "can work in a Japanese office,"</strong> N1 for client-facing or document-heavy
roles, and language is a "nice to have" mainly in English-first tech. Below N2, lean toward
international/foreign-capital employers.</div>

<h2 id="n1-trap">The N1 trap, why certificates fail interviews</h2>
<p>A counterintuitive truth experienced hiring managers repeat: <strong>N1 holders frequently fail
interviews</strong>, while confident N2 speakers get hired. The JLPT tests reading and listening, not <em>speaking</em> or <em>conversation</em>. You can hold N1 and still freeze in a live
interview, mismanage workplace politeness, or be unable to run a meeting. Japanese employers
increasingly weight <strong>real-world communication over the certificate</strong>.</p>
<p>The implication for your study: don't grind only for the test. If a job needs working Japanese,
practise <strong>speaking and business communication</strong> in parallel, because that's what gets
you hired and promoted, the certificate just gets you past the resume filter.</p>

<h2 id="business-japanese">Business Japanese ≠ JLPT</h2>
<p>"Business-level Japanese" on a job ad means something the JLPT doesn't directly measure:
running a meeting, writing a polite email, handling a phone call, reading internal documents, and
navigating <em>keigo</em> (honorific speech). Some employers reference the <strong>BJT (Business
Japanese Proficiency Test)</strong> or the <strong>JLPT N2/N1 + interview</strong> as a proxy. If
your target roles say "business Japanese," budget study time for practical workplace language, not
just JLPT grammar drills.</p>

<h2 id="study-plan">A realistic study plan & hours per level</h2>
<table>
  <thead><tr><th>Level</th><th>Rough study hours (from zero)</th><th>What it unlocks</th></tr></thead>
  <tbody>
    <tr><td>N5</td><td>~350–460 hrs</td><td>Survival Japanese; daily life basics</td></tr>
    <tr><td>N4</td><td>~550–800 hrs</td><td>Simple conversations; "basic" on job ads</td></tr>
    <tr><td>N3</td><td>~900–1,300 hrs</td><td>The bridge; some coding-only jobs accept it</td></tr>
    <tr><td>N2</td><td>~1,500–2,200 hrs</td><td>The working-in-a-Japanese-office threshold</td></tr>
    <tr><td>N1</td><td>~2,300–4,500 hrs</td><td>Client-facing, documents, professional ceiling</td></tr>
  </tbody>
</table>
<p>At a sustainable ~1 hour/day, N2 from scratch is a multi-year project; full-time immersion
compresses it dramatically. Most working professionals reach N3–N2 over 2–3 years in-country while
employed, which is exactly why landing an English-first first job and studying alongside it is the
common winning strategy.</p>

<h2 id="study-tools">The tool stack that actually works</h2>
<ul>
  <li><strong>Vocabulary/kanji (SRS):</strong> Anki (free, with shared decks like Core 2k/6k) or
      WaniKani (kanji + vocab, gamified, paid).</li>
  <li><strong>Grammar:</strong> Bunpro (SRS for grammar points), the Genki textbooks (N5–N4),
      Tobira (N3+), and the Shin Kanzen Master / Sou Matome series for N2–N1 prep.</li>
  <li><strong>Listening:</strong> the "Nihongo con Teppei" podcast, YouTube comprehensible-input
      channels, and just consuming anime/dramas with Japanese subtitles.</li>
  <li><strong>Speaking:</strong> italki or Preply tutors, language exchange (HelloTalk, Tandem,
      Meetup), and a weekly conversation partner, non-negotiable if you want to pass interviews.</li>
  <li><strong>Reading practice:</strong> NHK Easy News, Satori Reader, graded readers.</li>
</ul>

<h2 id="keigo">Keigo, the politeness layer that matters at work</h2>
<p>Keigo (敬語, honorific language) is the part of Japanese that the JLPT under-weights but the
workplace over-weights. It has three registers, <strong>polite (丁寧語)</strong>, <strong>humble
(謙譲語)</strong>, and <strong>respectful (尊敬語)</strong>, and using the wrong one with a client or
senior reads as rude or clueless. You don't need to master it before arriving, but be aware that
"my Japanese is fine" and "my <em>business</em> Japanese is fine" are different claims, and the gap
is mostly keigo and email conventions.</p>

<h2 id="test-logistics">Test logistics, dates, cost, where</h2>
<ul>
  <li><strong>When:</strong> the JLPT is held <strong>twice a year, first Sunday of July and
      December</strong> in Japan and many overseas cities (some locations offer only December).</li>
  <li><strong>Registration:</strong> opens months ahead and fills early in popular cities, register
      as soon as it opens.</li>
  <li><strong>Cost:</strong> roughly ¥6,500–7,500 in Japan (varies overseas).</li>
  <li><strong>Results:</strong> arrive ~2 months later; the certificate <strong>never expires</strong>,
      though some employers prefer a recent pass.</li>
  <li><strong>Strategy:</strong> if a job needs "N2," take it the cycle <em>before</em> you job-hunt
      so you can list it; don't wait for the offer to depend on a test you haven't sat.</li>
</ul>
<div class="callout">Related: <a href="/resources/interview-phrases">Useful Japanese for interviews</a> ·
<a href="/guides/software-engineering">Software engineering guide (language reality)</a></div>
"""
    },

    # ==================================================================== SALARY
    "salary": {
        "key_takeaways": [
            "<strong>Employer type is the biggest lever on your pay</strong>, often bigger than seniority. The TokyoDev 2025 survey put the median engineer at ¥9.5M, but ¥13.5M at companies with no Japanese entity vs ¥8.5M at Japanese-HQ firms.",
            "The MHLW national average for software engineers (¥5.69M) is far below what foreign-friendly employers pay, don't anchor on Japan-wide averages.",
            "Japanese offers bundle <strong>base + bonus (shōyo, often 2–6 months) + allowances</strong>. Always clarify whether the bonus is guaranteed and watch for 'fixed/deemed overtime' inflating the headline.",
            "Negotiation is more accepted at foreign-capital firms; <strong>base, sign-on bonus, and equity</strong> move most. Bring market data.",
            "Net take-home is typically <strong>~75–80% of gross</strong>, and residence tax (~10%) only kicks in your second year, budget for the year-two drop.",
        ],
        "faqs": [
            ("How much do foreigners earn in Japan?",
             "<p>It varies hugely by field and, critically, employer type. For software engineers (the best-documented field), the TokyoDev 2025 survey found a <strong>median of ¥9.5M</strong>, rising to <strong>¥13.5M at companies without a Japanese entity</strong> and falling to ¥8.5M at Japanese-HQ firms. Other professional fields (finance, PM, marketing) broadly track the same employer-type pattern. Use the <a href='/insights/salary'>live salary insights</a> for per-role numbers from current listings.</p>"),
            ("Do Japanese salaries include bonuses?",
             "<p>Often, and it matters. Many Japanese offers quote an annual figure split across 12, 14, or 16 'months' because of <strong>bonuses (賞与, shōyo)</strong>, commonly 2–6 months of salary paid summer and winter. '¥6M over 12 months' and '¥6M base + 4 months bonus' are very different offers, so always ask whether the bonus is guaranteed or discretionary, and whether 'fixed overtime' (みなし残業) is baked into the base.</p>"),
            ("Can you negotiate salary in Japan?",
             "<p>Yes, more readily at foreign-capital and global firms than at traditional Japanese ones, but it's possible at both. What moves most: <strong>base salary</strong> (bring market data), <strong>sign-on bonus</strong> (often easier than base, useful to offset forfeited equity), and <strong>equity grant size</strong>. Start date, remote days, and relocation/school-fee support are also fair asks. See the <a href='/pillars/negotiation-playbook'>negotiation playbook</a>.</p>"),
            ("What is take-home pay after tax in Japan?",
             "<p>Roughly <strong>75–80% of gross</strong> for a mid-range salary. Deductions are income tax, ~14–16% social insurance (health + pension + employment), and, from your second year only, ~10% residence tax. That year-two residence-tax step-up surprises many first-year arrivals. Model your exact figure with the <a href='/tools/take-home-pay'>take-home pay calculator</a>.</p>"),
            ("Why do foreign companies pay so much more in Japan?",
             "<p>Global and foreign-capital firms benchmark to international (often US-influenced) pay bands and compete for a thin bilingual/global talent pool, while many domestic Japanese firms run flatter, seniority-linked scales. The same factor drives faster raises: foreign-capital firms run performance-based merit cycles, traditional firms run smaller annual seniority bumps. It's the single biggest reason to weight your search toward foreign-capital and global-remote employers.</p>"),
        ],
        "extra_toc": [
            ("real-numbers-2025", "Real 2025 numbers, the foreign-vs-Japanese gap"),
            ("by-experience", "Salary by experience level"),
            ("equity", "Equity, RSUs & the FX trap"),
            ("total-comp", "Reading total comp, bonus, allowances, the lot"),
            ("negotiation", "Negotiation, what's actually movable"),
            ("payslip", "Decoding your payslip"),
            ("raises", "Raises & the Japanese pay curve"),
        ],
        "extra_body": """
<hr>
<h2 id="real-numbers-2025">Real 2025 numbers, the foreign-vs-Japanese gap</h2>
<p>The most important salary fact for foreign professionals isn't the national average, it's the
<strong>gap by employer type</strong>. From the <strong>TokyoDev 2025 Developer Survey</strong> (a
foreigner-heavy sample of software engineers):</p>
<table>
  <thead><tr><th>Cohort</th><th>Median total comp</th></tr></thead>
  <tbody>
    <tr><td>All respondents (2025)</td><td><strong>¥9.5M</strong> (up ¥1M from 2024)</td></tr>
    <tr><td>At Japanese-HQ companies</td><td>¥8.5M</td></tr>
    <tr><td>At companies <em>without</em> a Japanese entity (global/remote)</td><td><strong>¥13.5M</strong></td></tr>
    <tr><td>MHLW national average (all SW engineers, incl. Japanese-only firms)</td><td>¥5.69M</td></tr>
  </tbody>
</table>
<div class="callout">Read that again: the median foreign-friendly engineer earns <strong>~¥9.5M</strong>,
but the same person at a global company with no Japanese entity earns <strong>~¥13.5M</strong>, a
~¥5M swing for similar work. The lesson that runs through this whole site: <strong>employer type is
the biggest lever on your pay</strong>, often bigger than seniority. Sort the job board toward
foreign-capital and global employers.</div>

<h2 id="by-experience">Salary by experience level</h2>
<table>
  <thead><tr><th>Experience</th><th>Median (TokyoDev 2025)</th></tr></thead>
  <tbody>
    <tr><td>&lt; 1 year</td><td>¥2.8M</td></tr>
    <tr><td>Mid-career</td><td>~¥8–10M</td></tr>
    <tr><td>20+ years</td><td>¥14.2M</td></tr>
  </tbody>
</table>
<p>These are software figures, but the <em>shape</em> generalises: foreign-capital and global firms
pay a clear premium, and the senior end stretches much higher than Japanese-firm bands. Use the
live <a href="/insights/salary">salary insights</a> page for per-role percentiles from current
listings.</p>

<h2 id="equity">Equity, RSUs & the FX trap</h2>
<p>Global tech firms increasingly grant <strong>RSUs</strong> on top of base. Two things to watch:</p>
<ul>
  <li><strong>FX exposure:</strong> if your grant is USD-denominated and the yen moves, your real
      compensation swings. Where negotiable, ask for the grant value <strong>fixed in JPY</strong>,
      or understand you're partly betting on USD/JPY.</li>
  <li><strong>Tax:</strong> RSUs are taxed as income on vest in Japan, and capital-gains rules apply
      on sale. Equity comp can complicate your Japanese tax return, many foreign professionals get
      a tax accountant (税理士) the first year they have vesting RSUs.</li>
</ul>

<h2 id="total-comp">Reading total comp, bonus, allowances, the lot</h2>
<p>A Japanese offer is often quoted as <strong>annual base, sometimes split across 12, 14, or 16
"months"</strong> because of bonuses. Decode it:</p>
<ul>
  <li><strong>Bonus (賞与, <em>shōyo</em>):</strong> commonly 2–6 months of salary per year, paid
      summer and winter, but check whether it's guaranteed or performance-discretionary. "¥6M over
      12 months" and "¥6M base + 4 months bonus" are very different offers.</li>
  <li><strong>Allowances (手当):</strong> commuting (通勤手当, usually fully covered), housing
      (住宅手当), family/dependent (家族手当), overtime. Some are tax-advantaged.</li>
  <li><strong>"Fixed overtime" (みなし残業):</strong> watch for offers where a chunk of "salary" is
      actually pre-counted overtime, it can make a number look bigger than the base really is.</li>
</ul>

<h2 id="negotiation">Negotiation, what's actually movable</h2>
<p>Salary negotiation is more accepted at foreign-capital firms than traditional Japanese ones, but
possible at both. What tends to move:</p>
<ul>
  <li><strong>Base</strong>, most movable at global firms with leveling bands; bring market data
      (this site's salary insights, levels.fyi, the TokyoDev survey).</li>
  <li><strong>Sign-on bonus</strong>, often easier to get than base, especially to offset RSUs you
      forfeit by leaving a prior job.</li>
  <li><strong>Equity grant size</strong>, negotiable at public-company SaaS, sometimes ±30%.</li>
  <li><strong>Start date, remote days, relocation support, school-fee assistance</strong>, all
      legitimate asks, especially for family relocations.</li>
</ul>
<p>See the dedicated <a href="/pillars/negotiation-playbook">salary negotiation playbook</a> for
scripts and the Japan-specific etiquette of asking.</p>

<h2 id="payslip">Decoding your payslip</h2>
<p>Your monthly payslip (給与明細) splits into earnings (支給) and deductions (控除):</p>
<ul>
  <li><strong>健康保険</strong> health insurance · <strong>厚生年金</strong> pension ·
      <strong>雇用保険</strong> employment insurance, together your "social insurance," ~14–16%.</li>
  <li><strong>所得税</strong> income tax (withheld monthly, reconciled in year-end 年末調整).</li>
  <li><strong>住民税</strong> residence tax, ~10%, but only from your <em>second</em> year (see the
      health-insurance guide's year-two warning).</li>
</ul>
<p>Net take-home is typically <strong>~75–80% of gross</strong> for a mid-range salary. Model your
exact number with the <a href="/tools/take-home-pay">take-home pay calculator</a>.</p>

<h2 id="raises">Raises & the Japanese pay curve</h2>
<p>Traditional Japanese firms run an annual raise cycle (often April, 昇給) with relatively flat,
seniority-linked increases, predictable but slow. Foreign-capital firms run performance-based merit
cycles closer to Western norms, with bigger jumps for strong performers and via promotion. If
fast pay growth matters to you, weight foreign-capital and global employers, the same factor that
drives the level difference also drives the slope of the raise curve.</p>
<div class="callout">Tools: <a href="/insights/salary">Live salary insights by role</a> ·
<a href="/tools/take-home-pay">Take-home pay calculator</a> ·
<a href="/pillars/negotiation-playbook">Negotiation playbook</a></div>
"""
    },

    # ============================================================== COST OF LIVING
    "cost-of-living": {
        "key_takeaways": [
            "A realistic mid-range monthly budget: <strong>~¥236k single, ~¥369k couple, ~¥549k family of 4</strong> in Tokyo (excluding one-off move-in costs). You can live well below this outside central wards.",
            "<strong>Osaka rent runs 20–30% cheaper</strong> than central Tokyo for comparable apartments; food and transport are similar nationwide.",
            "The biggest hidden cost is <strong>year-two residence tax (~10%)</strong>, billed on the prior year's income, your take-home drops in year two with no pay change.",
            "Furnishing an unfurnished apartment from zero (no fridge, washer, curtains, light fixtures) adds <strong>¥100–200k</strong> on arrival.",
            "Residents save real money with <strong>furusato nōzei</strong> (hometown tax), point ecosystems (Rakuten/PayPay), cheap SIM + electricity providers, and evening supermarket discounts.",
        ],
        "faqs": [
            ("How much money do I need to move to Japan?",
             "<p>Plan for a <strong>landing cost of roughly ¥500,000–¥1,500,000</strong> for a major city. That's apartment move-in (¥300–600k, deposit, key money, agency, guarantor), furnishing an empty apartment (¥100–300k), flights and shipping, plus a survival buffer until your first paycheck arrives (often 4–6 weeks out). Model your exact number with the <a href='/tools/relocation-budget'>relocation budget calculator</a>.</p>"),
            ("How much does it cost to live in Japan per month?",
             "<p>For a single person, a comfortable mid-range Tokyo budget is about <strong>¥150,000–¥250,000/month</strong> (¥236k is typical including rent, utilities, food, transport, and leisure). A couple runs ~¥369k and a family of four ~¥549k. Outside central wards, in Osaka, or in regional cities, the rent component drops substantially.</p>"),
            ("Is Tokyo more expensive than Osaka?",
             "<p>Yes, mainly on rent, <strong>Osaka is roughly 20–30% cheaper</strong> than central Tokyo for a comparable apartment, with the same big-city amenities and famously cheaper food. Salaries in Osaka run somewhat lower, so weigh net purchasing power, not just rent. Within Tokyo, eastern/outer wards and the Saitama/Chiba commuter belt are far cheaper than central Minato/Shibuya.</p>"),
            ("What unexpected costs surprise newcomers in Japan?",
             "<p>The big ones: <strong>year-two residence tax (~10%)</strong> that appears with no pay change; <strong>lease renewal fees</strong> (~1 month's rent every 2 years); <strong>seasonal utility spikes</strong> from poorly insulated apartments; <strong>furnishing from zero</strong> because 'unfurnished' means no appliances at all; and occasional <strong>cash-only</strong> moments at small clinics, restaurants, and some landlords.</p>"),
            ("How can I save money living in Japan?",
             "<p>Use <strong>furusato nōzei</strong> ('hometown tax') to redirect part of your residence tax to regional towns and get local goods back; concentrate spending in one <strong>point ecosystem</strong> (Rakuten, PayPay) for rebates; switch to a <strong>cheap MVNO SIM and a cheaper electricity provider</strong> (saving ¥5,000+/month combined); shop the evening supermarket discount stickers; and furnish from 100-yen shops (Daiso, Seria) on arrival. Once you have a buffer, NISA lets you invest tax-free.</p>"),
        ],
        "extra_toc": [
            ("sample-budgets", "Sample monthly budgets (single, couple, family)"),
            ("tokyo-vs-rest", "Tokyo vs Osaka vs Fukuoka, the real spread"),
            ("hidden-costs", "Hidden costs newcomers miss"),
            ("saving-money", "How residents actually save money"),
            ("first-year-cashflow", "The first-year cashflow trap"),
        ],
        "extra_body": """
<hr>
<h2 id="sample-budgets">Sample monthly budgets (single, couple, family)</h2>
<p>Illustrative Tokyo monthly budgets after tax (¥), excluding one-off move-in costs:</p>
<table>
  <thead><tr><th>Item</th><th>Single (modest)</th><th>Couple</th><th>Family of 4</th></tr></thead>
  <tbody>
    <tr><td>Rent (incl. fees)</td><td>110,000</td><td>170,000</td><td>250,000</td></tr>
    <tr><td>Utilities + internet</td><td>18,000</td><td>25,000</td><td>35,000</td></tr>
    <tr><td>Food (groceries + eating out)</td><td>55,000</td><td>90,000</td><td>140,000</td></tr>
    <tr><td>Transport (commuter pass)</td><td>10,000</td><td>18,000</td><td>22,000</td></tr>
    <tr><td>Phone</td><td>3,000</td><td>6,000</td><td>12,000</td></tr>
    <tr><td>Misc / leisure / health</td><td>40,000</td><td>60,000</td><td>90,000</td></tr>
    <tr><td><strong>Rough total</strong></td><td><strong>~236,000</strong></td><td><strong>~369,000</strong></td><td><strong>~549,000</strong></td></tr>
  </tbody>
</table>
<div class="callout">These are mid-range, not survival or luxury. A single person can live well below
this in a smaller apartment outside central wards; a family with international-school fees is far
above it. Use them as a sanity check against an offer, then refine in the
<a href="/tools/take-home-pay">take-home pay</a> and <a href="/tools/col-comparator">cost-of-living
comparator</a> tools.</div>

<h2 id="tokyo-vs-rest">Tokyo vs Osaka vs Fukuoka, the real spread</h2>
<p>Rent is where regional cost diverges most; food and transport are broadly similar nationwide.</p>
<ul>
  <li><strong>Tokyo (23 wards):</strong> the benchmark. Central wards (Minato, Shibuya, Chuo) carry
      a steep premium; eastern/outer wards (Adachi, Katsushika, Nerima) and the Saitama/Chiba
      commuter belt are much cheaper for the same space.</li>
  <li><strong>Osaka:</strong> roughly <strong>20–30% cheaper rent</strong> than central Tokyo for
      comparable apartments, with big-city amenities, the value-density winner.</li>
  <li><strong>Fukuoka:</strong> cheaper still, a growing startup scene, and a famously livable city;
      salaries run lower too, so weigh net purchasing power, not just rent.</li>
  <li><strong>Nagoya, Sapporo, regional cities:</strong> lower rent, but fewer English-friendly jobs, the trade-off is opportunity density.</li>
</ul>

<h2 id="hidden-costs">Hidden costs newcomers miss</h2>
<ul>
  <li><strong>Year-two residence tax (~10%)</strong>, the single biggest surprise; budget for the
      take-home drop.</li>
  <li><strong>Lease renewal fee</strong>, ~1 month's rent every 2 years.</li>
  <li><strong>Seasonal utility spikes</strong>, poor insulation makes summer AC and winter heating
      expensive; a ¥10,000 utility bill can become ¥20,000+.</li>
  <li><strong>"Furnish from zero"</strong>, unfurnished means no fridge, washer, light fixtures, or
      curtains. Budget ¥100–200k on arrival.</li>
  <li><strong>Cash-only moments</strong>, some clinics, small restaurants, and landlords.</li>
  <li><strong>NHK fee</strong> if you own a TV/tuner.</li>
</ul>

<h2 id="saving-money">How residents actually save money</h2>
<ul>
  <li><strong>furusato nōzei (ふるさと納税)</strong>, "hometown tax": redirect part of your residence
      tax to regional towns and receive local goods (meat, rice, fruit) in return. A legal, popular
      way to get value back from tax you'd pay anyway.</li>
  <li><strong>Point ecosystems</strong>, Rakuten, PayPay, and dPoint stack meaningful rebates if
      you concentrate spending.</li>
  <li><strong>Cheap SIM + cheap electricity provider</strong>, switching both can save ¥5,000+/month.</li>
  <li><strong>Supermarket timing</strong>, evening discount stickers (半額) on fresh food and bento.</li>
  <li><strong>100-yen shops (Daiso, Seria)</strong> for furnishing and kitchenware on arrival.</li>
  <li><strong>NISA</strong> for tax-free investing once you have a buffer.</li>
</ul>

<h2 id="first-year-cashflow">The first-year cashflow trap</h2>
<p>The toughest financial window is your first 2 months: move-in costs (4–6× rent), a relocation,
and a first salary that may not arrive for 4–6 weeks all land together. Then year two brings the
residence-tax step-up. Plan for both: arrive with a cash buffer (model it in the
<a href="/tools/relocation-budget">relocation budget calculator</a>), and don't let year-one's
low tax fool you into lifestyle creep that year-two tax will punish.</p>
<div class="callout">Tools: <a href="/tools/col-comparator">Cost-of-living comparator</a> ·
<a href="/tools/take-home-pay">Take-home pay</a> ·
<a href="/tools/relocation-budget">Relocation budget</a></div>
"""
    },

    # ================================================================= RED FLAGS
    "red-flags": {
        "key_takeaways": [
            "A 'black company' (ブラック企業) exploits workers via illegal overtime, unpaid wages, and harassment. Score an offer against the checklist, <strong>three or more flags is a serious warning</strong>.",
            "Your single best research move: search the company on <strong>OpenWork and JobHouse</strong> (Japan's Glassdoor equivalents) plus the company name + ブラック.",
            "Watch contracts for <strong>'fixed/deemed overtime' (みなし残業)</strong> hiding a low base, vague job scope, and any hint they'll 'hold' your visa, your visa is yours, they only sponsor it.",
            "You can always quit (usually 1 month's notice); <strong>taishoku daikō</strong> resignation-agency services will quit on your behalf if the employer is hostile.",
            "Free official help exists: the <strong>Labour Standards Inspection Office</strong> for unpaid wages/illegal overtime, general unions you can join individually, and Hōterasu legal aid.",
        ],
        "faqs": [
            ("What is a 'black company' in Japan?",
             "<p>A <strong>black company (ブラック企業, burakku kigyō)</strong> is an employer that exploits staff through illegal or excessive overtime, unpaid wages, power harassment, and high churn. Warning signs include job ads heavy on 'passion' but vague on pay/hours, a role that's perpetually re-advertised, reluctance to put overtime policy in writing, and pressure to decide immediately. Three or more such signs is a serious warning.</p>"),
            ("How do I check a Japanese company's reputation before applying?",
             "<p>Search it on <strong>OpenWork (旧 Vorkers) and JobHouse / Lighthouse</strong>, Japan's equivalents of Glassdoor, with blunt current-and-ex-employee reviews on overtime and culture. Also Google the company name plus ブラック, check Glassdoor for foreign-capital firms, and look at LinkedIn for whether people <em>stay</em> (tenure) or mass-exit to competitors.</p>"),
            ("What should I watch for in a Japanese employment contract?",
             "<p>Key traps: <strong>'fixed/deemed overtime' (みなし残業)</strong> that hides a low real base; no written overtime policy; long, low-paid probation (試用期間); penalty/clawback clauses for leaving; vague job scope that lets them reassign you to anything (including work your visa doesn't cover); and any implication they control your visa. Get hours, overtime, and holidays in writing before signing.</p>"),
            ("Can I quit a job in Japan if it's a bad fit?",
             "<p>Yes. Standard notice is often <strong>1 month</strong> (check your contract and work rules / 就業規則), and Japanese civil law lets you resign with notice even if the employer resists. If the employer is hostile or you can't face the conversation, <strong>taishoku daikō (退職代行)</strong> resignation-agency services will quit on your behalf, they're widely used. Line up your next role and notify immigration of the job change within 14 days.</p>"),
            ("Where can I get help with a workplace problem in Japan?",
             "<p>Free and official options: the <strong>Labour Standards Inspection Office (労働基準監督署)</strong> for unpaid wages, illegal overtime, and unsafe conditions; <strong>general unions (ユニオン)</strong> like the Tokyo General Union that any individual can join for help with disputes; <strong>Hōterasu (法テラス)</strong> for subsidised legal advice; and <strong>Hello Work</strong> for unemployment benefits and placement. Document everything, hours, messages, payslips.</p>"),
        ],
        "extra_toc": [
            ("black-company-checklist", "Black-company checklist, score the offer"),
            ("contract-redflags", "Contract red flags to catch before signing"),
            ("interview-tells", "Interview tells that something's off"),
            ("recruiter-games", "Recruiter & agency games"),
            ("if-trapped", "If you're already in a bad job"),
            ("where-to-get-help", "Where to get help, free & official"),
        ],
        "extra_body": """
<hr>
<h2 id="black-company-checklist">Black-company checklist, score the offer</h2>
<p>A "black company" (ブラック企業, <em>burakku kigyō</em>) exploits workers via illegal overtime,
unpaid wages, harassment, and churn. Score an employer against these before signing, three or more
is a serious warning:</p>
<ul>
  <li>☐ Job ad emphasises "passion," "family," or "young energetic team" but is vague on pay and
      hours.</li>
  <li>☐ Salary band is suspiciously high for the role, sometimes because it bakes in heavy
      "fixed overtime."</li>
  <li>☐ The same role is <strong>perpetually advertised</strong> (high churn).</li>
  <li>☐ Reluctance to put hours, overtime policy, or holidays <strong>in writing</strong>.</li>
  <li>☐ Glassdoor / OpenWork / JobHouse reviews mention unpaid overtime, harassment, or mass exits.</li>
  <li>☐ Interviewers dodge questions about <strong>average monthly overtime</strong> or
      paid-leave usage.</li>
  <li>☐ Pressure to decide <strong>immediately</strong>, or to start before paperwork is clear.</li>
  <li>☐ "Everyone here works late" framed as a virtue.</li>
</ul>
<div class="callout">Your best single research move: search the company on <strong>OpenWork
(旧 Vorkers)</strong> and <strong>JobHouse</strong>, Japan's equivalents of Glassdoor, plus the
company name + ブラック on Google. Current-and-ex-employee reviews are blunt and revealing.</div>

<h2 id="contract-redflags">Contract red flags to catch before signing</h2>
<ul>
  <li><strong>"Fixed/deemed overtime" (みなし残業)</strong> hiding a low base, confirm the real base
      and what happens beyond the included hours.</li>
  <li><strong>No written overtime policy</strong> or a "we don't really track it" answer.</li>
  <li><strong>Probation traps</strong>, wildly lower pay or vague "evaluation" terms during a long
      probation (試用期間).</li>
  <li><strong>Penalty/clawback clauses</strong> for leaving (training repayment, etc.), some are
      unenforceable, but their presence signals the culture.</li>
  <li><strong>Visa leverage</strong>, any hint that they'll "hold" your visa over you. Your visa is
      yours; they sponsor it, they don't own it.</li>
  <li><strong>Vague job scope</strong> that lets them reassign you to anything, including work your
      visa doesn't cover.</li>
</ul>

<h2 id="interview-tells">Interview tells that something's off</h2>
<ul>
  <li>They can't name a single thing employees <em>like</em> beyond "the people."</li>
  <li>The person who'd be your manager seems exhausted or evasive.</li>
  <li>No clear answer on <strong>why the role is open</strong> (backfill? growth? someone quit?).</li>
  <li>Discomfort when you ask about <strong>average overtime and paid-leave usage rates</strong>.</li>
  <li>The process is chaotic and disrespectful of your time, that's a preview of the job.</li>
</ul>

<h2 id="recruiter-games">Recruiter & agency games</h2>
<p>Most recruiters are fine; a few play games because they're paid on placement, not your happiness:</p>
<ul>
  <li><strong>Pressure to accept fast</strong> "before the role closes", legitimate roles rarely
      vanish overnight.</li>
  <li><strong>Withholding the company name</strong> until you commit to interview, fine early, but
      you should know before final stages so you can research it.</li>
  <li><strong>Lowballing your expectations</strong> "for the Japanese market", bring your own data
      (this site, TokyoDev survey, levels.fyi).</li>
  <li><strong>Submitting you to roles you didn't approve</strong>, insist on consent before each
      submission, or you can get "burned" with a company you'd have applied to directly.</li>
</ul>

<h2 id="if-trapped">If you're already in a bad job</h2>
<ul>
  <li><strong>You can quit.</strong> Standard notice is often 1 month (check your contract / work
      rules 就業規則); civil law allows resignation with notice even if they resist.</li>
  <li><strong>Taishoku daikō (退職代行)</strong>, paid "resignation agency" services will quit on
      your behalf if the employer is hostile or you can't face the conversation. They're widely used.</li>
  <li><strong>Unpaid wages/overtime</strong> are recoverable, document everything (hours, messages,
      payslips).</li>
  <li><strong>Don't let a bad job jeopardise your visa</strong>, line up the next role, and notify
      immigration of the change within 14 days.</li>
</ul>

<h2 id="where-to-get-help">Where to get help, free & official</h2>
<ul>
  <li><strong>Labour Standards Inspection Office (労働基準監督署, <em>rōdō kijun kantokusho</em>)</strong>, the government body for unpaid wages, illegal overtime, and unsafe conditions. Free.</li>
  <li><strong>Tokyo / prefectural labour consultation hotlines</strong>, some offer multilingual
      advice.</li>
  <li><strong>General unions (合同労組 / ユニオン)</strong>, anyone can join individually (e.g.
      Tokyo General Union, General Union in Kansai); they help foreigners with disputes and
      collective bargaining.</li>
  <li><strong>Legal aid (法テラス, Hōterasu)</strong>, subsidised legal consultation.</li>
  <li><strong>Hello Work (ハローワーク)</strong>, public employment service; unemployment benefits if
      you paid employment insurance, plus job placement.</li>
</ul>
<div class="callout">Related: <a href="/resources/interview-etiquette">Interview etiquette</a> ·
<a href="/resources/external-resources">External resources directory</a> ·
<a href="/community">Community (people who've been there)</a></div>
"""
    },

    # ========================================================= INTERVIEW ETIQUETTE
    "interview-etiquette": {
        "key_takeaways": [
            "Interview style splits by employer: <strong>foreign-capital = Western and direct</strong> (sell yourself); <strong>traditional Japanese = formal, multi-round, consensus-driven</strong> (humility and long-term fit matter more).",
            "Most foreigner-friendly employers run <strong>final rounds remotely</strong> for overseas candidates, you rarely fly out before an offer.",
            "Always have a genuine <strong>'why Japan / why this company'</strong> answer, it's weighted far more heavily here than in a typical Western loop.",
            "A Japanese offer often comes as an informal <strong>naitei (内定)</strong> first; ask for it in writing with full comp before resigning, and it's fine to take a few days to decide.",
            "Asking about <strong>average monthly overtime and paid-leave usage</strong> is a polite, effective way to screen for black-company risk.",
        ],
        "faqs": [
            ("What should I wear to a job interview in Japan?",
             "<p>For <strong>traditional Japanese firms</strong>, a conservative dark suit, white shirt, and minimal accessories is the safe default. For <strong>foreign-capital and tech</strong>, business-casual is usually fine, but err one notch more formal for a first interview unless told otherwise. On video, dress as you would in person from the waist up, don't treat remote as casual.</p>"),
            ("Are job interviews in Japan done in English?",
             "<p>At foreign-capital firms, global-tech Tokyo offices, and English-first Japanese product companies, yes, often entirely in English and frequently <strong>remote for overseas candidates</strong>. At Japanese-domestic companies, interviews are in Japanese and may switch languages to test your level. Bilingual roles often run a mix. Clarify the working language early; it tells you the real Japanese requirement of the job.</p>"),
            ("What questions should I ask the interviewer in Japan?",
             "<p>Strong, screening questions: 'What does success look like at 3/6/12 months?', 'What's the <strong>average monthly overtime</strong> on this team and how is paid leave actually used?' (a polite black-company probe), 'Why is this role open?', and 'What's the team's working language day to day?'. For relocations, ask exactly what visa and relocation support covers and the timeline.</p>"),
            ("Should I send a thank-you note after a Japanese interview?",
             "<p>A brief thank-you email within 24 hours is appreciated at most companies and standard at foreign-capital ones, keep it short, reference something specific, and reiterate interest. At very traditional firms it's less expected but rarely hurts. If you'd be writing in Japanese and aren't confident with keigo, a polite English note to an English-speaking interviewer is safer than clumsy honorifics.</p>"),
            ("What is a 'naitei' and how do offers work in Japan?",
             "<p>A <strong>naitei (内定)</strong> is an informal job offer that precedes the formal contract. Ask for the offer <strong>in writing</strong> with full compensation, hours, and start date before you resign anything, and it's acceptable to request a few days to consider, pressure to accept on the spot is a yellow flag. For overseas hires, the naitei kicks off the 2–4 month COE/visa process, so your real start date is months out.</p>"),
        ],
        "extra_toc": [
            ("formats", "Interview formats, what to expect by company type"),
            ("video-rounds", "Remote/video rounds from abroad"),
            ("what-to-wear", "What to wear (and the recruit-suit question)"),
            ("questions-to-ask", "Smart questions to ask them"),
            ("thank-you", "The follow-up / thank-you note"),
            ("offer-stage", "The offer stage, naitei & timelines"),
        ],
        "extra_body": """
<hr>
<h2 id="formats">Interview formats, what to expect by company type</h2>
<ul>
  <li><strong>Foreign-capital / global tech:</strong> Western-style, recruiter screen, technical
      and behavioural rounds, often in English, sometimes remote end-to-end. Direct questions,
      direct answers; selling yourself is expected.</li>
  <li><strong>Japanese companies:</strong> more formal and consensus-driven, often
      <strong>multiple rounds</strong> ending with senior management. Humility, fit, and long-term
      commitment are weighted heavily; overt self-promotion can backfire. Expect questions about
      <em>why Japan</em> and <em>why this company specifically</em>.</li>
  <li><strong>Bilingual / mixed:</strong> the interview may switch languages to test your level;
      be ready to demonstrate, not just claim, your Japanese.</li>
</ul>

<h2 id="video-rounds">Remote/video rounds from abroad</h2>
<p>Most foreigner-friendly employers run final rounds <strong>remotely for overseas candidates</strong>, you rarely need to fly out before an offer. To run them well: test your setup, use a neutral
background and good light, dial in early, and treat punctuality as seriously as in person (join 2–3
minutes before). Time zones are on you to get right, propose slots in <strong>JST</strong> to show
you understand you're applying <em>into</em> Japan.</p>

<h2 id="what-to-wear">What to wear (and the recruit-suit question)</h2>
<ul>
  <li><strong>Traditional Japanese firms:</strong> conservative dark suit, white shirt, minimal
      accessories, the safe default. The "recruit suit" (リクルートスーツ) culture is real for
      new-grads; mid-career professionals can wear a normal business suit.</li>
  <li><strong>Foreign-capital / tech:</strong> business-casual is usually fine, but err one notch
      more formal for a first interview unless told otherwise.</li>
  <li><strong>Video:</strong> dress as you would in person from the waist up; don't treat remote as
      an excuse to be casual.</li>
</ul>

<h2 id="questions-to-ask">Smart questions to ask them</h2>
<p>Asking good questions signals seriousness and screens for black-company risk:</p>
<ul>
  <li>"What does success in this role look like at 3, 6, and 12 months?"</li>
  <li>"What's the <strong>average monthly overtime</strong> on this team, and how is paid leave
      actually used?" (a polite way to probe culture)</li>
  <li>"How are decisions made here, and how is feedback given?"</li>
  <li>"Why is this role open?"</li>
  <li>"What's the team's working language day to day?" (clarifies the real Japanese requirement)</li>
  <li>For relocation: "What does the visa and relocation support cover, and what's the timeline?"</li>
</ul>

<h2 id="thank-you">The follow-up / thank-you note</h2>
<p>A brief thank-you email within 24 hours is appreciated at most companies and standard at
foreign-capital ones. Keep it short, specific (reference something discussed), and reiterate your
interest. At very traditional firms it's less expected but rarely hurts. In Japanese, mind the keigo;
when unsure, a polite English note to an English-speaking interviewer is safer than clumsy keigo.</p>

<h2 id="offer-stage">The offer stage, naitei & timelines</h2>
<p>A Japanese job offer is often an <strong>informal offer (内定, <em>naitei</em>)</strong> first,
then a formal contract. Know that:</p>
<ul>
  <li>You can, and should, ask for the offer <strong>in writing</strong> with full comp, hours,
      and start date before resigning anything.</li>
  <li>It's acceptable to ask for <strong>a few days to consider</strong>; pressure to accept on the
      spot is a yellow flag.</li>
  <li>For overseas hires, the offer kicks off the <strong>COE process</strong> (2–4 months), so the
      real start date is months out; plan your resignation and move around that.</li>
  <li>Negotiate <em>before</em> you accept the naitei, see the
      <a href="/pillars/negotiation-playbook">negotiation playbook</a>.</li>
</ul>
<div class="callout">Related: <a href="/resources/interview-phrases">Useful Japanese for interviews</a> ·
<a href="/interview-prep">Interview prep hub</a> · <a href="/resources/red-flags">Red flags</a></div>
"""
    },

    # ========================================================== JAPANESE RESUME
    "japanese-resume-formats": {
        "key_takeaways": [
            "Japanese companies want <strong>two documents</strong>: the standardised <strong>rirekisho (履歴書)</strong> for facts and the free-form <strong>shokumu keirekisho (職務経歴書)</strong> for your achievements/story.",
            "Foreign-capital, global-tech, and English-first employers usually just want a <strong>strong English CV + LinkedIn</strong>, you can skip the Japanese-resume apparatus entirely.",
            "Common screen-outs: wrong/inconsistent date format, an empty <strong>motivation field (志望動機)</strong>, no photo, and unproofed keigo. Have a native speaker check the Japanese.",
            "The resume <strong>photo</strong> is expected: 4cm×3cm, business attire, plain background, taken within 3 months (¥800 at a station booth).",
            "The <strong>hanko on resumes is now largely optional</strong> after government de-hanko reforms, though a few traditional employers still expect one.",
        ],
        "faqs": [
            ("What's the difference between a rirekisho and a shokumu keirekisho?",
             "<p>The <strong>rirekisho (履歴書)</strong> is a standardised personal-history form, fixed template covering education, work history, and a motivation field. The <strong>shokumu keirekisho (職務経歴書)</strong> is a free-form career document where you present your roles, scope, and quantified achievements, like a Western achievement resume. Japanese employers typically want both. Build both free on the <a href='/resume'>resume tools</a>.</p>"),
            ("Do I need a Japanese resume to work in Japan?",
             "<p>Only for Japanese-style employers. If you're targeting <strong>foreign-capital firms, global-tech Tokyo offices, or English-first Japanese companies</strong>, a strong English CV and LinkedIn are usually all you need. The Japanese rirekisho + shokumu keirekisho is a Japanese-company expectation, which is one more reason the English-first job market is the path of least resistance for newcomers.</p>"),
            ("Do I need a photo on my Japanese resume?",
             "<p>Yes, for the rirekisho, it's expected. Spec: <strong>4cm × 3cm, taken within 3 months, plain light background, business attire, neutral expression.</strong> Get it at a station photo booth (証明写真機) for ~¥800, or a studio for a noticeably better result on senior applications. For online applications, booths give you a data file you can upload.</p>"),
            ("Is a hanko (seal) required on a Japanese resume?",
             "<p>Increasingly not. The government's de-hanko reforms have made the seal <strong>largely optional on resumes and many official forms</strong>, and most digital applications don't use one. That said, a traditional employer may still expect it, so it's worth keeping a basic hanko (your name in katakana, ¥1,000–3,000) available.</p>"),
            ("What are the most common Japanese resume mistakes?",
             "<p>The screen-out classics: inconsistent date formats (Japanese era 令和 vs Western year), missing furigana for your name, a generic or empty <strong>motivation field (志望動機)</strong>, which is read closely, no photo or a casual one, and unproofed business Japanese/keigo. On the shokumu keirekisho, lead with quantified achievements and mirror the job description's keywords, and keep it to 2–3 pages.</p>"),
        ],
        "extra_toc": [
            ("which-doc", "Which document for which employer"),
            ("rirekisho-mistakes", "Rirekisho mistakes that get you screened out"),
            ("shokumu-tips", "Shokumu keirekisho, making it actually sell"),
            ("photo-rules", "The resume photo, rules & where to get it"),
            ("digital-vs-paper", "Digital vs paper & the hanko question"),
            ("english-cv-when", "When an English CV is enough"),
        ],
        "extra_body": """
<hr>
<h2 id="which-doc">Which document for which employer</h2>
<table>
  <thead><tr><th>Employer type</th><th>What they expect</th></tr></thead>
  <tbody>
    <tr><td>Foreign-capital / global tech</td><td>English CV (1–2 pages, achievement-focused). Often an ATS.</td></tr>
    <tr><td>Japanese company</td><td><strong>Both</strong> rirekisho (履歴書) + shokumu keirekisho (職務経歴書), usually in Japanese</td></tr>
    <tr><td>Bilingual / mixed</td><td>Japanese rirekisho + shokumu, sometimes an English CV too</td></tr>
    <tr><td>Recruiter submission</td><td>Whatever the agency formats you into, usually Japanese for Japanese clients</td></tr>
  </tbody>
</table>
<div class="callout">The rirekisho is a <strong>standardised personal-history form</strong> (think
official template), while the shokumu keirekisho is your <strong>free-form career/achievement
document</strong>. Japanese employers typically want both, the rirekisho for facts, the shokumu for
your story. Build both free on this site's <a href="/resume">resume tools</a>.</div>

<h2 id="rirekisho-mistakes">Rirekisho mistakes that get you screened out</h2>
<ul>
  <li><strong>Wrong date format</strong>, Japanese resumes often use the Japanese era (令和, Reiwa)
      alongside or instead of the Western year; be consistent.</li>
  <li><strong>Inconsistent name order / furigana</strong>, provide furigana (reading) for your name
      and addresses.</li>
  <li><strong>Empty motivation field</strong>, the 志望動機 (reason for applying) is read closely;
      a generic line reads as low interest.</li>
  <li><strong>No photo or a casual photo</strong>, see below.</li>
  <li><strong>Typos / correction fluid on a handwritten form</strong>, traditionally you rewrite
      the whole thing rather than correct it; digital avoids this.</li>
</ul>

<h2 id="shokumu-tips">Shokumu keirekisho, making it actually sell</h2>
<p>This is where you differentiate. Treat it like a Western achievement resume but in Japanese
business register:</p>
<ul>
  <li>Lead each role with <strong>scope</strong> (team size, budget, product), then
      <strong>quantified achievements</strong> (numbers, %, ¥).</li>
  <li>Mirror the <strong>keywords in the job description</strong>, many large firms screen for them.</li>
  <li>Add a short <strong>summary (職務要約)</strong> at the top, 3–4 lines framing your career.</li>
  <li>Keep it <strong>2–3 pages</strong>; relevance over completeness.</li>
  <li>Have a <strong>native speaker proof the Japanese</strong>, especially keigo and business
      phrasing, small errors undercut a senior candidate.</li>
</ul>

<h2 id="photo-rules">The resume photo, rules & where to get it</h2>
<ul>
  <li><strong>Spec:</strong> typically 4cm × 3cm, taken within 3 months, plain light background,
      business attire, neutral expression.</li>
  <li><strong>Where:</strong> photo booths (証明写真機) at stations for ~¥800, or a photo studio for
      a noticeably better result (worth it for senior roles).</li>
  <li><strong>Digital:</strong> for online applications, many booths give you a data version; resume
      builders let you upload it directly.</li>
</ul>

<h2 id="digital-vs-paper">Digital vs paper & the hanko question</h2>
<p>Increasingly, applications are <strong>digital</strong> (PDF upload or ATS), which sidesteps
handwriting and lets you reuse a polished template. Some traditional firms still want a printed,
even handwritten rirekisho. The <strong>hanko on a resume is now largely optional/abolished</strong>
for many forms (the government has pushed de-hanko reforms), but a traditional employer may still
expect one, keep a basic hanko available.</p>

<h2 id="english-cv-when">When an English CV is enough</h2>
<p>If you're targeting <strong>foreign-capital, global tech, or English-first</strong> employers, a
strong English CV (and LinkedIn) is usually all you need, the Japanese resume apparatus is a
Japanese-company expectation. This is another reason the English-first job market is the path of
least resistance for newcomers: it skips an entire document-format learning curve. Build your CV on
the <a href="/resume/cv">English CV builder</a> and sharpen bullets with the
<a href="/resume/bullets">bullet improver</a>.</p>
<div class="callout">Tools: <a href="/resume">Rirekisho builder</a> ·
<a href="/resume/shokumu">Shokumu builder</a> · <a href="/resume/cv">English CV</a> ·
<a href="/templates">Bilingual email templates</a></div>
"""
    },

    # =========================================================== INTERVIEW PHRASES
    "interview-phrases": {
        "key_takeaways": [
            "Even in an English interview, a few Japanese touchpoints signal respect: open with <strong>「本日はよろしくお願いいたします」</strong> and close with <strong>「本日はお時間をいただき、ありがとうございました」</strong>.",
            "The <strong>self-introduction (自己紹介)</strong> opens most Japanese interviews, keep it 60–90 seconds: name (申します), experience, one signature achievement, why you're here.",
            "The <strong>motivation answer (志望動機)</strong> is weighted heavily, connect your trajectory to <em>their</em> specific business, not generic enthusiasm.",
            "Knowing polite phrases to <strong>buy time or ask for clarification</strong> beats pretending to understand and answering the wrong question.",
            "Soften money talk with framing like 「御社の規定に従いますが…」 rather than blunt demands.",
        ],
        "faqs": [
            ("How do I introduce myself in a Japanese job interview?",
             "<p>Use the humble form: <strong>「〇〇と申します」</strong> (My name is ◯◯), then give your current role, years of experience, and one signature achievement, and close with <strong>「よろしくお願いいたします」</strong>. Keep the whole <em>jiko-shōkai</em> to 60–90 seconds and practise it out loud until it's automatic, nerves hit hardest in the first minute.</p>"),
            ("What Japanese phrases are useful even in an English interview?",
             "<p>A few touchpoints go a long way: open with <strong>「本日はよろしくお願いいたします」</strong> ('thank you for your time today') and close with <strong>「本日はお時間をいただき、ありがとうございました」</strong>. They signal respect and effort without requiring you to conduct the interview in Japanese.</p>"),
            ("How do I politely buy time or ask for clarification in Japanese?",
             "<p>Three reliable phrases: <strong>「少し考えさせていただけますか」</strong> (may I take a moment to think?), <strong>「もう一度おっしゃっていただけますか」</strong> (could you say that once more?), and <strong>「〇〇という理解でよろしいでしょうか」</strong> (is my understanding that ◯◯ correct?). Using these well is more impressive than pretending to understand, it shows composure and real communication skill.</p>"),
            ("How do I talk about salary politely in a Japanese interview?",
             "<p>Soften it with framing rather than a blunt demand: <strong>「御社の規定に従いますが、現職では〇〇万円をいただいております」</strong> anchors your current pay without demanding, and <strong>「〇〇万円程度を希望しておりますが、ご相談させていただければ幸いです」</strong> states a target while inviting discussion. At foreign-capital firms you can be more direct in English, see the <a href='/pillars/negotiation-playbook'>negotiation playbook</a>.</p>"),
        ],
        "extra_toc": [
            ("opening-closing", "Opening & closing the interview"),
            ("self-intro", "The self-introduction (jiko-shōkai)"),
            ("motivation", "Explaining your motivation (shibō dōki)"),
            ("buying-time", "Buying time & asking for clarification"),
            ("salary-talk", "Talking money politely"),
            ("video-phrases", "Phrases for video/remote rounds"),
        ],
        "extra_body": """
<hr>
<h2 id="opening-closing">Opening & closing the interview</h2>
<p>Even in an English interview, a few Japanese touchpoints signal respect and effort:</p>
<ul>
  <li>On entering / starting: <strong>「本日はよろしくお願いいたします。」</strong>
      (<em>Honjitsu wa yoroshiku onegai itashimasu</em>), "Thank you for your time today."</li>
  <li>On leaving: <strong>「本日はお時間をいただき、ありがとうございました。」</strong>
      (<em>…otaisetsu na ojikan o itadaki, arigatō gozaimashita</em>), "Thank you for your time."</li>
</ul>

<h2 id="self-intro">The self-introduction (jiko-shōkai)</h2>
<p>The <strong>自己紹介</strong> usually opens a Japanese interview. A clean template:</p>
<ul>
  <li>「〇〇と申します。」, "My name is ◯◯." (humble form)</li>
  <li>Current role + years of experience + one signature achievement.</li>
  <li>One line on <strong>why you're here</strong> for this role.</li>
  <li>Close: 「よろしくお願いいたします。」</li>
</ul>
<p>Keep it ~60–90 seconds; rambling reads as unprepared. Practise it out loud until it's automatic, nerves hit hardest in the first minute.</p>

<h2 id="motivation">Explaining your motivation (shibō dōki)</h2>
<p>The <strong>志望動機</strong> ("why this company") is weighted heavily in Japan. Strong answers
connect <em>your</em> trajectory to <em>their</em> specific business, not "I love Japan" but "your
work on X aligns with my experience in Y, and I want to contribute by Z." Generic enthusiasm reads
as low effort; specificity reads as serious.</p>

<h2 id="buying-time">Buying time & asking for clarification</h2>
<ul>
  <li>「少し考えさせていただけますか。」, "May I take a moment to think?"</li>
  <li>「もう一度おっしゃっていただけますか。」, "Could you say that once more?"</li>
  <li>「〇〇という理解でよろしいでしょうか。」, "Is my understanding that ◯◯ correct?"</li>
</ul>
<p>Using these <em>well</em> is more impressive than pretending to understand and answering the
wrong question, it shows composure and real communication skill, which (per the JLPT discussion)
employers value over a certificate.</p>

<h2 id="salary-talk">Talking money politely</h2>
<p>Direct salary demands can feel blunt in Japanese business culture; soften with framing:</p>
<ul>
  <li>「御社の規定に従いますが、現職では〇〇万円をいただいております。」, "I'll follow your
      guidelines; in my current role I receive ¥◯◯." (anchors without demanding)</li>
  <li>For a target: 「〇〇万円程度を希望しておりますが、ご相談させていただければ幸いです。」, "I'm hoping for around ¥◯◯, but I'd welcome a discussion."</li>
</ul>
<p>At foreign-capital firms you can be more direct in English; see the
<a href="/pillars/negotiation-playbook">negotiation playbook</a>.</p>

<h2 id="video-phrases">Phrases for video/remote rounds</h2>
<ul>
  <li>If audio cuts: 「音声が途切れてしまいました。もう一度お願いできますか。」, "The audio cut
      out, could you repeat that?"</li>
  <li>To confirm you can be heard: 「お声は問題なく聞こえております。」, "I can hear you clearly."</li>
  <li>Closing remotely: 「本日はオンラインで貴重なお時間をありがとうございました。」</li>
</ul>
<div class="callout">Related: <a href="/resources/interview-etiquette">Interview etiquette</a> ·
<a href="/interview-prep">Interview prep hub</a> · <a href="/resources/jlpt-levels">JLPT levels</a></div>
"""
    },

    # ========================================================= EXTERNAL RESOURCES
    "external-resources": {
        "key_takeaways": [
            "<strong>r/japanlife</strong> is the big forum for living-in-Japan logistics; <strong>TokyoDev</strong> (Discord + job board) is the high-signal hub for foreign software engineers.",
            "<strong>OpenWork</strong> is the single best company-reputation check (Japan's Glassdoor); also JobHouse and Lighthouse.",
            "Trustworthy salary data: the <strong>TokyoDev Developer Survey</strong>, levels.fyi for global tech, and Robert Walters/Hays/Michael Page surveys for bilingual professional roles.",
            "Language stack: Anki + WaniKani (kanji), Bunpro + Genki/Tobira (grammar), italki/HelloTalk (speaking), NHK Easy News + Satori Reader (reading).",
            "When a forum post and an official source disagree, <strong>trust the official source</strong> (Immigration Services Agency, Japan Pension Service, National Tax Agency), and treat anything more than a year or two old as possibly stale.",
        ],
        "faqs": [
            ("Where do foreigners in Japan ask questions and get help online?",
             "<p>The best communities: <strong>r/japanlife</strong> (visas, housing, banking, taxes, daily-life problem-solving), <strong>r/movingtojapan</strong> (relocation stage), <strong>r/teachinginjapan</strong> (ALT/eikaiwa), <strong>r/LearnJapanese</strong> (study), and the <strong>TokyoDev Discord/forums</strong> for engineers. State your visa status, location, and what you've already checked to get good answers.</p>"),
            ("How do I research a Japanese company before applying?",
             "<p><strong>OpenWork (旧 Vorkers)</strong> is the leading employee-review site, detailed, honest on overtime and culture. Also check JobHouse and Lighthouse (Japanese), Glassdoor (better for foreign-capital firms), and LinkedIn for employee tenure and where people go next. Google the company name plus ブラック as a quick black-company check.</p>"),
            ("What's the best way to learn Japanese for work?",
             "<p>A proven stack: <strong>Anki or WaniKani</strong> for vocab/kanji (SRS), <strong>Bunpro</strong> plus the Genki/Tobira textbooks for grammar, <strong>italki/Preply and HelloTalk</strong> for speaking, and <strong>NHK Easy News + Satori Reader</strong> for reading. Crucially, practise <em>speaking</em> in parallel with test prep, that's what wins interviews, which the JLPT alone never measures.</p>"),
            ("Where can I find reliable salary data for Japan?",
             "<p>For engineers, the <strong>TokyoDev Developer Survey</strong> is the gold standard (granular by company type and experience). <strong>levels.fyi</strong> covers global-tech leveling and increasingly Tokyo offices. The <strong>Robert Walters, Hays, and Michael Page salary surveys</strong> cover bilingual finance, legal, marketing, and sales roles. This site's <a href='/insights/salary'>live salary insights</a> compute percentiles from current listings.</p>"),
        ],
        "extra_toc": [
            ("reddit-forums", "Reddit & forums, where foreigners actually talk"),
            ("review-sites", "Company review sites (the OpenWork layer)"),
            ("salary-data", "Salary data sources worth trusting"),
            ("language-stack", "Language-learning stack"),
            ("gov-official", "Official / government sources"),
            ("news-staying-current", "Staying current on rule changes"),
        ],
        "extra_body": """
<hr>
<h2 id="reddit-forums">Reddit & forums, where foreigners actually talk</h2>
<ul>
  <li><strong>r/japanlife</strong>, the big one for living-in-Japan logistics: visas, housing,
      banking, taxes, daily-life problem-solving. Search before posting; most questions are answered.</li>
  <li><strong>r/japanresidents, r/movingtojapan</strong>, relocation-stage questions.</li>
  <li><strong>r/teachinginjapan</strong>, ALT/eikaiwa reality, company reputations.</li>
  <li><strong>r/LearnJapanese</strong>, study methods, the famous "Daily Thread."</li>
  <li><strong>TokyoDev Discord & forums</strong>, software-engineer-specific, high signal.</li>
  <li><strong>Gaijinpot & Japan-Guide forums</strong>, older but searchable archives.</li>
</ul>
<div class="callout">Forum etiquette that gets you good answers: state your <strong>visa status,
location, and what you've already checked</strong>. "How do I open a bank account?" gets eye-rolls;
"Shinsei rejected me at 4 months in, who else opens for new arrivals?" gets real help.</div>

<h2 id="review-sites">Company review sites (the OpenWork layer)</h2>
<ul>
  <li><strong>OpenWork (旧 Vorkers)</strong>, Japan's leading employee-review site; detailed,
      Japanese-language, brutally honest on overtime and culture. The single best black-company check.</li>
  <li><strong>JobHouse, Lighthouse (旧カイシャの評判)</strong>, more Japanese review aggregators.</li>
  <li><strong>Glassdoor</strong>, thinner for Japanese firms, useful for foreign-capital ones.</li>
  <li><strong>LinkedIn</strong>, check whether people <em>stay</em> (tenure) and where they go next;
      mass exits to competitors are a tell.</li>
</ul>

<h2 id="salary-data">Salary data sources worth trusting</h2>
<ul>
  <li><strong>TokyoDev Developer Survey</strong> (annual), the gold standard for foreign software
      engineers in Japan; granular by company type and experience.</li>
  <li><strong>levels.fyi</strong>, global-tech leveling and comp, increasingly populated for Tokyo
      offices of FAANG-type firms.</li>
  <li><strong>Robert Walters / Hays / Michael Page salary surveys</strong>, bilingual professional
      roles across finance, legal, marketing, sales.</li>
  <li><strong>This site's <a href="/insights/salary">live salary insights</a></strong>, percentiles
      computed from current listings.</li>
</ul>

<h2 id="language-stack">Language-learning stack</h2>
<ul>
  <li><strong>SRS:</strong> Anki, WaniKani (kanji).</li>
  <li><strong>Grammar:</strong> Bunpro, Genki / Tobira textbooks, Shin Kanzen Master (N2–N1).</li>
  <li><strong>Speaking:</strong> italki, Preply, HelloTalk/Tandem, local Meetups.</li>
  <li><strong>Listening/reading:</strong> NHK Easy News, Satori Reader, Nihongo con Teppei,
      comprehensible-input YouTube.</li>
</ul>

<h2 id="gov-official">Official / government sources</h2>
<ul>
  <li><strong>Immigration Services Agency of Japan (出入国在留管理庁)</strong>, the authority on
      visas, COE, residence procedures.</li>
  <li><strong>Japan Pension Service (日本年金機構)</strong>, pension, the lump-sum withdrawal.</li>
  <li><strong>National Tax Agency (国税庁)</strong>, income/residence tax, the tax representative.</li>
  <li><strong>Your municipality's website</strong>, ward-specific childcare, allowances, garbage
      rules (yes, garbage sorting is real and local).</li>
  <li><strong>JNTO multilingual medical directory</strong>, English-speaking clinics.</li>
</ul>

<h2 id="news-staying-current">Staying current on rule changes</h2>
<p>Immigration and tax rules move (this very page reflects 2025–26 changes: digital COE, the PR
income floor, the pension cap reform, the Business Manager tightening). Stay current via the
Immigration Services Agency announcements, r/japanlife's recurring threads, and English explainer
sites like <strong>TokyoDev, Japan Dev, and Tokyo Cheapo</strong>. When a forum post and an official
source disagree, trust the official source, and treat anything more than a year or two old as
possibly stale.</p>
<div class="callout">Related: <a href="/community">Community hub</a> ·
<a href="/resources/red-flags">Red flags (using review sites)</a> ·
<a href="/insights/salary">Live salary insights</a></div>
"""
    },
}


def merge_resource(item: dict) -> dict:
    """Return a shallow copy of a resource dict with its deep-dive extension
    (extra TOC + extra body) appended, if one exists for that slug."""
    if not item:
        return item
    extra = RESOURCE_EXTRAS.get(item.get("slug"))
    if not extra:
        return item
    merged = dict(item)
    merged["toc"] = list(item.get("toc", [])) + list(extra.get("extra_toc", []))
    merged["body"] = item.get("body", "") + extra.get("extra_body", "")
    # Premium components (Key Takeaways box + FAQ accordion/schema), if supplied.
    if extra.get("key_takeaways"):
        merged["key_takeaways"] = extra["key_takeaways"]
    if extra.get("faqs"):
        merged["faqs"] = extra["faqs"]
        merged["toc"] = list(merged["toc"]) + [("faq", "FAQ")]
    return merged
