"""
Non-destructive deep-dive extensions for content.GUIDES (city + role guides).

Same pattern as resources_extra: each guide slug gets extra TOC entries and
extra HTML appended at render time, so the large content.py is never edited.
Merged by the Flask /guides/<slug> route via merge_guide().

City guides get: neighborhoods-by-profile, commute reality, day-to-day cost,
where the international community is, schools/families, and getting-settled.
Role guides get: where the jobs are (named employers), the comp ladder, the
Japanese-language reality for that role, the interview loop, and how to break in
from abroad.

Figures 2025–26; grounded where researched (Tokyo ward rents/foreign-resident
ratios; TokyoDev 2025 survey for SWE comp). Orientation, not advice.
"""

GUIDE_EXTRAS: dict[str, dict] = {

    # ===================================================================== TOKYO
    "tokyo": {
        "key_takeaways": [
            "<strong>Minato (Roppongi, Hiroo, Azabu)</strong> has the strongest English support; <strong>Meguro/Shibuya</strong> are stylish and central; <strong>Setagaya</strong> is family-friendly but the least international ward; <strong>Koto</strong> is modern and best value.",
            "Choose a <strong>train line, not a distance</strong>, aim for 30–45 min door-to-door, avoid more than one transfer, and check for express stops.",
            "Outer wards (Adachi, Katsushika) and the <strong>Saitama/Chiba belt</strong> are far cheaper for the same space.",
            "The <strong>commuter pass is employer-reimbursed</strong>, so optimise for time over fare.",
            "Learn your ward's <strong>garbage-sorting schedule</strong>, it's strict and local, and register at your <em>ward</em> office, not a generic city hall.",
        ],
        "faqs": [
            ("Where do most foreigners live in Tokyo?",
             "<p>The classic expat areas are in <strong>Minato ward</strong>, Roppongi, Hiroo, and Azabu, which have the best English infrastructure, international supermarkets, and embassies. <strong>Meguro (Nakameguro, Jiyugaoka)</strong> and <strong>Shibuya (Ebisu, Daikanyama)</strong> are popular for stylish, central living; <strong>Setagaya</strong> suits families wanting space; and <strong>Koto (Toyosu)</strong> offers modern apartments at better value. Your daily quality of life depends more on your train line and commute than the ward name.</p>"),
            ("What's the cheapest area to live in Tokyo?",
             "<p>The eastern and outer wards, <strong>Adachi, Katsushika, Nerima</strong>, and the <strong>Saitama and Chiba commuter belt</strong> offer much cheaper rent for the same space than central wards like Minato or Shibuya. The trade-off is a longer commute. Since commuter passes are usually employer-reimbursed, the real cost of living further out is time, not money, so weigh a cheaper rent against a longer daily ride.</p>"),
            ("How long is a typical Tokyo commute?",
             "<p>Most residents aim for <strong>30–45 minutes door-to-door</strong>. The key is choosing a good train line: the JR Yamanote loop for maximum central access, the Chuo/Sobu lines east-west, or private lines (Tokyu, Odakyu, Keio) for comfortable suburbs. Practical rules: avoid needing more than one transfer, and live near a station with <strong>express stops (急行/快速)</strong>, which dramatically cut travel time.</p>"),
            ("Is Tokyo good for families with children?",
             "<p>Yes, with the right ward. <strong>Setagaya, Meguro (Jiyugaoka), and Koto (Toyosu)</strong> trade centrality for space and greenery. International schools cluster toward Minato/Shibuya/Setagaya and the west (budget ¥1.5–3M/year). Licensed-daycare availability varies sharply by ward, and Tokyo made 0–2 daycare free for a first child from September 2025, so research your target ward's waitlist before signing a lease.</p>"),
        ],
        "extra_toc": [
            ("where-to-live", "Where to live, wards by profile"),
            ("ward-table", "Ward cheat-sheet (rent, vibe, foreign ratio)"),
            ("commute", "The commute reality, lines, not distance"),
            ("english-infra", "Where English actually works"),
            ("families-tokyo", "Tokyo for families"),
            ("neighborhood-picks", "Quick picks by who you are"),
            ("getting-settled", "Getting settled, the first month"),
        ],
        "extra_body": """
<hr>
<h2 id="where-to-live">Where to live, wards by profile</h2>
<p>Tokyo's 23 wards differ enormously in price, vibe, and how foreigner-friendly they are. The
right ward depends on whether you optimise for nightlife, family space, budget, or English support.</p>
<ul>
  <li><strong>Minato (Roppongi, Hiroo, Azabu):</strong> the expat heartland, the strongest English
      infrastructure in Tokyo (ward office, building management, medical), international supermarkets,
      embassies. Expensive, polished, convenient.</li>
  <li><strong>Shibuya / Meguro (Nakameguro, Daikanyama, Ebisu):</strong> stylish, walkable, creative.
      Meguro is ~3.9% foreign residents, calmer than Minato but still cosmopolitan; Nakameguro and
      Jiyugaoka are perennial favourites.</li>
  <li><strong>Setagaya (Sangenjaya, Futako-Tamagawa, Yoga):</strong> family-friendly, green, spacious,
      a slower pace, but the <em>least</em> international ward (~2.9% foreign), and no Yamanote
      station (you ride private lines into Shibuya/Shinjuku).</li>
  <li><strong>Koto (Toyosu, Kiba):</strong> modern waterfront high-rises, more space for the money
      (1BR ~¥70–200k), a growing international community, quick into central Tokyo.</li>
  <li><strong>Shinjuku / Toshima (Ikebukuro):</strong> dense, convenient, transit super-hubs; mixed
      pricing; good value just off the core.</li>
  <li><strong>Eastern & outer wards (Adachi, Katsushika, Nerima) + Saitama/Chiba belt:</strong> the
      budget play, much cheaper rent for the same space, longer commute.</li>
</ul>

<h2 id="ward-table">Ward cheat-sheet (rent, vibe, foreign ratio)</h2>
<table>
  <thead><tr><th>Ward</th><th>1BR rent (approx)</th><th>Vibe</th><th>Foreign-friendly?</th></tr></thead>
  <tbody>
    <tr><td>Minato</td><td>¥160–350k</td><td>Polished expat core</td><td>★★★★★ strongest English</td></tr>
    <tr><td>Meguro</td><td>¥100–280k</td><td>Stylish, calm</td><td>★★★★ trendy-area English</td></tr>
    <tr><td>Shibuya</td><td>¥130–300k</td><td>Young, central</td><td>★★★★</td></tr>
    <tr><td>Setagaya</td><td>¥100–250k</td><td>Family, green</td><td>★★★ comfortable but local</td></tr>
    <tr><td>Koto</td><td>¥70–200k</td><td>Modern waterfront</td><td>★★★ growing</td></tr>
    <tr><td>Outer/Saitama-Chiba</td><td>¥60–120k</td><td>Suburban value</td><td>★★ budget</td></tr>
  </tbody>
</table>
<div class="callout">A common foreigner mistake is fixating on a ward's name. What actually
determines your daily quality of life is your <strong>nearest train line and your door-to-door
commute</strong>, see below. A "cheaper" ward on a slow line can cost you more in time than a
pricier one with a fast express.</div>

<h2 id="commute">The commute reality, lines, not distance</h2>
<p>In Tokyo you choose a <em>line</em>, not a distance. Most residents target
<strong>30–45 minutes door-to-door</strong>. Orient by the network:</p>
<ul>
  <li><strong>JR Yamanote</strong>, the central loop linking Shinjuku, Shibuya, Tokyo, Ueno,
      Ikebukuro. Living near it = maximum optionality.</li>
  <li><strong>JR Chuo / Sobu</strong>, the east-west spine (Nakano, Kichijoji to the west).</li>
  <li><strong>Private lines</strong>, Tokyu Den-en-toshi & Toyoko (into Shibuya), Odakyu & Keio
      (into Shinjuku), Tobu/Seibu (north). These serve the comfortable suburbs.</li>
  <li><strong>Metro</strong>, Hibiya, Ginza, Oedo, etc. weave through the centre.</li>
</ul>
<p>Practical rules: avoid needing to <strong>change lines more than once</strong>; check whether your
station has <strong>express stops (急行/快速)</strong>, which dramatically cut time; and remember the
<strong>commuter pass (定期券)</strong> is usually employer-reimbursed, so optimise for time, not
fare. Rush hour (roughly 7:30–9:00) on core lines is genuinely packed, living one express stop out
can mean a seat.</p>

<h2 id="english-infra">Where English actually works</h2>
<p>Tokyo is functional citywide, but English density is uneven. <strong>Minato</strong> has the best
official English support; <strong>Hiroo, Roppongi, Daikanyama, Azabu</strong> are very
foreigner-friendly with bilingual services and international groceries (National Azabu, Nissin World
Delicatessen). Outside these pockets you'll lean on translation apps and basic Japanese for the ward
office, clinics, and landlords, which is fine, but set expectations accordingly.</p>

<h2 id="families-tokyo">Tokyo for families</h2>
<ul>
  <li><strong>Space & parks:</strong> Setagaya, Meguro (Jiyugaoka), and Koto (Toyosu) trade
      centrality for room and greenery.</li>
  <li><strong>International schools</strong> cluster toward Minato/Shibuya/Setagaya and the west;
      factor school location into ward choice (and budget ¥1.5–3M/yr, see the
      <a href="/living/family">family guide</a>).</li>
  <li><strong>Daycare:</strong> licensed-daycare availability varies sharply by ward, and Tokyo made
      0–2 daycare free for a first child from Sept 2025. Research your target ward's waitlist before
      signing a lease.</li>
</ul>

<h2 id="neighborhood-picks">Quick picks by who you are</h2>
<ul>
  <li><strong>Single, nightlife/central:</strong> Shibuya, Shinjuku, or just off them in Nakano.</li>
  <li><strong>Couple, stylish & calm:</strong> Nakameguro, Ebisu, Daikanyama.</li>
  <li><strong>Max English support:</strong> Hiroo / Azabu (Minato).</li>
  <li><strong>Family, space & schools:</strong> Setagaya or Meguro (Jiyugaoka).</li>
  <li><strong>Value, modern, more sqm:</strong> Koto (Toyosu) or the Saitama/Chiba belt.</li>
</ul>

<h2 id="getting-settled">Getting settled, the first month</h2>
<p>Tokyo-specific tips layered on the universal <a href="/living/coe-and-arrival">arrival sequence</a>:
register at your <em>ward</em> office (not a generic "city hall"); pick up a Suica/PASMO at any
station immediately; learn your ward's <strong>garbage-sorting schedule</strong> (burnable vs
non-burnable vs recyclable, on fixed days, it's strict and local); and find your nearest
international supermarket and English-friendly clinic in week one. Join your line's neighborhood
foreigner groups (most areas have an active Facebook/Discord) for the practical local knowledge that
no guide can fully cover.</p>
<div class="callout">Related: <a href="/living/housing">Renting an apartment</a> ·
<a href="/resources/cost-of-living">Cost of living by ward</a> ·
<a href="/living/family">Tokyo for families</a></div>
"""
    },

    # ===================================================================== OSAKA
    "osaka": {
        "key_takeaways": [
            "Osaka is the <strong>value-density winner</strong>, rent runs 20–30% cheaper than central Tokyo with full big-city amenities and famously cheap, great food.",
            "Live in <strong>Umeda/Kita</strong> (business hub), <strong>Namba/Minami</strong> (nightlife), <strong>Tennoji/Abeno</strong> (value), or <strong>Kobe</strong> (scenic, international, ~30 min away).",
            "The trade-off: <strong>fewer English-friendly professional roles</strong> than Tokyo. Many foreign professionals here work for a multinational, teach, or work remotely.",
            "Kansai culture is <strong>warmer and more direct</strong>, with its own dialect (Kansai-ben), many find it easier to build a local social circle than in Tokyo.",
            "A common path: start in Tokyo for job density, move to Osaka once established or remote.",
        ],
        "faqs": [
            ("Is Osaka cheaper than Tokyo?",
             "<p>Yes, mainly on rent, <strong>Osaka runs roughly 20–30% cheaper</strong> than central Tokyo for a comparable apartment, with the same big-city amenities and notably cheaper food. Salaries in Osaka are somewhat lower, so weigh net purchasing power rather than rent alone. For a foreigner whose job exists in Kansai or who works remotely, Osaka often means a materially higher quality of life per yen.</p>"),
            ("Are there English-speaking jobs in Osaka?",
             "<p>Fewer than Tokyo, and in narrower fields, be clear-eyed about this. Osaka's strengths are manufacturing and trading houses (the Kansai industrial belt), some foreign-capital offices, plentiful English teaching, and a growing startup scene. Many foreign professionals in Kansai work for a multinational with an Osaka office, teach, or work remotely for a Tokyo/overseas employer while enjoying lower costs. Check job density for your field before committing.</p>"),
            ("What is Kansai culture like for foreigners?",
             "<p>Kansai has a distinct identity, <strong>more direct, humorous, and informal</strong> than Tokyo, with its own dialect (Kansai-ben). You don't need to speak Kansai-ben (standard Japanese is universal), but you'll hear it everywhere, and locals tend to warm up fast to foreigners who embrace the friendlier social style. Many people find it easier to build a local social circle in Kansai than in Tokyo.</p>"),
        ],
        "extra_toc": [
            ("why-osaka", "Why Osaka, the value case"),
            ("where-to-live-osaka", "Where to live in Osaka & Kansai"),
            ("osaka-jobs", "The Osaka job market for foreigners"),
            ("kansai-culture", "Kansai culture & language"),
            ("tokyo-vs-osaka", "Tokyo vs Osaka, an honest comparison"),
        ],
        "extra_body": """
<hr>
<h2 id="why-osaka">Why Osaka, the value case</h2>
<p>Osaka is Japan's value-density winner: <strong>roughly 20–30% cheaper rent</strong> than central
Tokyo for comparable apartments, full big-city amenities, famously good and affordable food, and a
warmer, more direct social culture. For a foreigner whose target job exists in Kansai (or who works
remotely), Osaka can mean a materially higher quality of life per yen than Tokyo.</p>

<h2 id="where-to-live-osaka">Where to live in Osaka & Kansai</h2>
<ul>
  <li><strong>Umeda / Kita (north):</strong> the business and transport hub, convenient, central,
      pricier.</li>
  <li><strong>Namba / Minami (south):</strong> nightlife, food, energy; great if you want the city's
      pulse at your door.</li>
  <li><strong>Tennoji / Abeno:</strong> good value, well-connected, increasingly popular.</li>
  <li><strong>Fukushima, Nakatsu:</strong> close to Umeda but cheaper and more residential.</li>
  <li><strong>Kobe (Hyogo):</strong> ~30 min from Osaka, scenic, international, relaxed; a favourite
      for families and a long-standing foreign community.</li>
  <li><strong>Kyoto:</strong> ~30 min by express, traditional, tourist-heavy, tighter rental market;
      doable as a base if your work is in Osaka.</li>
</ul>

<h2 id="osaka-jobs">The Osaka job market for foreigners</h2>
<p>Be clear-eyed: Osaka has <strong>fewer English-friendly professional roles than Tokyo</strong>.
The strengths are manufacturing and trading houses (the Kansai industrial belt), some foreign-capital
offices, English teaching (plentiful), and a growing startup scene. Many foreign professionals in
Kansai either work for a multinational with an Osaka office, teach, or work remotely for a
Tokyo/overseas employer while enjoying Osaka's lower costs. If your field is narrow and English-only,
check job density here before committing, filter the <a href="/jobs?location=Osaka">board for
Osaka</a>.</p>

<h2 id="kansai-culture">Kansai culture & language</h2>
<p>Kansai has a distinct identity: <strong>more direct, humorous, and informal</strong> than Tokyo,
with its own dialect (<strong>Kansai-ben</strong>). You don't need to speak Kansai-ben, standard
Japanese is universally understood, but you'll hear it everywhere, and locals warm up fast to
foreigners who embrace the region's friendlier social style. Many find Kansai an easier place to
build a local social circle than Tokyo.</p>

<h2 id="tokyo-vs-osaka">Tokyo vs Osaka, an honest comparison</h2>
<table>
  <thead><tr><th></th><th>Tokyo</th><th>Osaka</th></tr></thead>
  <tbody>
    <tr><td>English-friendly jobs</td><td>Most in Japan</td><td>Fewer; narrower fields</td></tr>
    <tr><td>Rent</td><td>Highest</td><td>20–30% cheaper</td></tr>
    <tr><td>Salaries</td><td>Highest</td><td>Somewhat lower</td></tr>
    <tr><td>Social ease for foreigners</td><td>Big but can feel anonymous</td><td>Warmer, more direct</td></tr>
    <tr><td>Food value</td><td>Great, pricey</td><td>Great, cheaper</td></tr>
    <tr><td>Best for</td><td>Career optionality, max opportunity</td><td>Quality of life per yen, remote workers</td></tr>
  </tbody>
</table>
<div class="callout">A common path: start in Tokyo for the job density, then move to Osaka/Kansai
once you're established or remote. Related: <a href="/resources/cost-of-living">Cost of living</a> ·
<a href="/jobs?location=Osaka">Osaka jobs</a> · <a href="/guides/tokyo">Tokyo guide</a></div>
"""
    },

    # ======================================================= SOFTWARE ENGINEERING
    "software-engineering": {
        "key_takeaways": [
            "Software is the <strong>most foreigner-accessible field</strong> in Japan, ~80% of foreign engineers primarily use English at work, and visa sponsorship is normal.",
            "<strong>Employer type drives pay</strong>: TokyoDev 2025 median ¥9.5M overall, but ¥13.5M at companies with no Japanese entity vs ¥8.5M at Japanese-HQ firms.",
            "Target English-first employers: Mercari, SmartNews, PayPay, LINE Yahoo, Rakuten, plus global-tech Tokyo offices (Google, Amazon, Indeed, Stripe, Woven).",
            "You usually <strong>don't need to be in Japan to get hired</strong>, the whole loop runs remotely and the company sponsors visa + relocation.",
            "A strong <strong>English CV + GitHub</strong> is enough; skip the Japanese-resume apparatus for these employers. JLPT is a nice-to-have, not a gate.",
        ],
        "faqs": [
            ("Can I work as a software engineer in Japan without speaking Japanese?",
             "<p>Yes, software is the field where 'no Japanese required' is most often genuinely true. At English-first firms (Mercari international, the global-tech Tokyo offices, remote roles), JLPT is a nice-to-have rather than a gate. A TokyoDev survey found only about a third of foreign engineers are fluent in Japanese while ~80% primarily use English at work. Some Japanese smooths daily life and unlocks the local team, but it's not required to get hired.</p>"),
            ("How much do software engineers earn in Japan?",
             "<p>The TokyoDev 2025 Developer Survey put the <strong>median at ¥9.5M</strong>, but the spread by employer type is the real story: <strong>¥13.5M at companies without a Japanese entity</strong> (global/remote) vs ¥8.5M at Japanese-HQ firms, against a ¥5.69M national average that includes Japanese-only employers. Less than 1 year of experience is around ¥2.8M; 20+ years around ¥14.2M. Where you work matters more than how long you've worked.</p>"),
            ("Which companies in Japan hire foreign software engineers?",
             "<p><strong>English-first Japanese product firms:</strong> Mercari, SmartNews, PayPay, LINE Yahoo, Rakuten, Woven by Toyota, Money Forward. <strong>Global tech with Tokyo offices:</strong> Google, Amazon/AWS, Microsoft, Indeed, Stripe, Datadog. <strong>Plus</strong> a large English-OK startup ecosystem (via the TokyoDev and Japan Dev boards) and fully-remote global roles you do from Japan, which are the highest-paying cohort.</p>"),
            ("Can I get a software job in Japan from abroad?",
             "<p>Yes, and it's common, you usually don't need to already be in Japan. Many companies (Mercari and the global-tech offices especially) run the entire interview loop remotely and sponsor the visa and relocation. The playbook: target English-first employers directly, make your English CV and LinkedIn strong, prepare a genuine 'why Japan' answer, and expect a 2–4 month visa/COE timeline after the offer.</p>"),
        ],
        "extra_toc": [
            ("where-jobs", "Where the SWE jobs are, named employers"),
            ("comp-ladder", "The comp ladder (2025 numbers)"),
            ("language-reality-swe", "The Japanese-language reality for engineers"),
            ("interview-loop", "The interview loop & how it differs"),
            ("from-abroad", "Breaking in from abroad"),
            ("stack-demand", "Which stacks & skills are in demand"),
            ("career-growth", "Career growth & the IC/manager split"),
        ],
        "extra_body": """
<hr>
<h2 id="where-jobs">Where the SWE jobs are, named employers</h2>
<p>Software is the single most foreigner-accessible professional field in Japan because so many
employers work in English. The landscape:</p>
<ul>
  <li><strong>Japanese product companies that hire in English:</strong> Mercari, SmartNews, PayPay,
      LINE Yahoo, Rakuten (English-official), Woven by Toyota, Money Forward, SODA/SNKRDUNK.</li>
  <li><strong>Foreign-capital / global tech with Tokyo offices:</strong> Google, Amazon/AWS,
      Microsoft, Indeed (big Tokyo eng. presence), Stripe, Datadog, HubSpot, Woven, Autify, Sider.</li>
  <li><strong>Bilingual / startup ecosystem:</strong> the TokyoDev job board, Japan Dev, and Wantedly
      surface English-OK startups.</li>
  <li><strong>Fully remote (no Japanese entity):</strong> increasingly common and the
      <em>highest-paying</em> cohort (see below), global companies hiring you to live in Japan but
      work for an overseas team.</li>
</ul>

<h2 id="comp-ladder">The comp ladder (2025 numbers)</h2>
<p>From the <strong>TokyoDev 2025 Developer Survey</strong>:</p>
<table>
  <thead><tr><th>Cohort</th><th>Median total comp</th></tr></thead>
  <tbody>
    <tr><td>&lt; 1 yr experience</td><td>¥2.8M</td></tr>
    <tr><td>All respondents</td><td><strong>¥9.5M</strong> (+¥1M YoY)</td></tr>
    <tr><td>Japanese-HQ companies</td><td>¥8.5M</td></tr>
    <tr><td>Companies without a Japanese entity</td><td><strong>¥13.5M</strong></td></tr>
    <tr><td>20+ yrs experience</td><td>¥14.2M</td></tr>
  </tbody>
</table>
<div class="callout">The ¥5M gap between Japanese-HQ (¥8.5M) and no-Japanese-entity (¥13.5M) medians
is the most important number in this guide. Where you work matters more than how long you've worked.
Optimise your search toward foreign-capital and global-remote employers.</div>

<h2 id="language-reality-swe">The Japanese-language reality for engineers</h2>
<p>Engineering is where "no Japanese required" is most often genuinely true. At English-first firms
(Mercari international, the global-tech Tokyo offices, remote roles), <strong>JLPT is a nice-to-have,
not a gate</strong>. At Japanese-domestic companies, expect <strong>N2</strong> for collaboration-heavy
roles (N3 sometimes survives for pure coding). Two practical notes: (1) even at English-first firms,
some Japanese smooths daily life and unlocks the local team; (2) don't grind only for the JLPT
certificate, speaking ability is what wins interviews and promotions (see the
<a href="/resources/jlpt-levels">JLPT guide's "N1 trap"</a>).</p>

<h2 id="interview-loop">The interview loop & how it differs</h2>
<p>At foreign-capital and English-first firms the loop is familiar: recruiter screen → technical
screen (live coding / take-home) → system design → behavioural → sometimes a hiring-manager/values
round, often <strong>fully remote for overseas candidates</strong>. Differences to expect in Japan:</p>
<ul>
  <li>More weight on <strong>"why Japan / why this company"</strong> than a typical Western loop, have a genuine answer.</li>
  <li>Some Japanese product companies add a <strong>culture-fit / long-term-commitment</strong> lens;
      they're wary of foreigners who'll leave in a year.</li>
  <li>System-design and fundamentals matter; leetcode-style screens are common at the bigger names.</li>
</ul>

<h2 id="from-abroad">Breaking in from abroad</h2>
<p>You usually <strong>don't need to be in Japan to get hired</strong>, many companies (Mercari and
the global-tech offices especially) run the whole loop remotely and sponsor the visa + relocation.
The playbook:</p>
<ol>
  <li>Target English-first employers directly (careers pages, TokyoDev, this board).</li>
  <li>Make your <strong>English CV + LinkedIn</strong> strong, that's all most need (skip the
      Japanese-resume apparatus).</li>
  <li>Have a real <strong>"why Japan"</strong> narrative ready.</li>
  <li>Expect a <strong>2–4 month COE/visa timeline</strong> after the offer, plan your move around it
      (see <a href="/living/coe-and-arrival">COE & arrival</a>).</li>
</ol>

<h2 id="stack-demand">Which stacks & skills are in demand</h2>
<p>Broadly Western-aligned: backend (Go, Kotlin/Java, Python, Ruby still strong at older product
firms), frontend (React/TypeScript), mobile (Swift/Kotlin), and platform/SRE/cloud (AWS, GCP,
Kubernetes). Data/ML and security are growth areas. English-first firms care about your engineering,
not Japanese-specific tech. Domestic enterprises and SIers (system integrators) skew toward Java and
on-prem and are less foreigner-friendly, a sector worth knowing exists but not your first target.</p>

<h2 id="career-growth">Career growth & the IC/manager split</h2>
<p>Foreign-capital and modern product firms offer a real <strong>IC (individual contributor)
track</strong> alongside management, you can reach Staff/Principal levels and high comp without
managing people, as in the West. Traditional Japanese firms historically funnel seniority into
management and seniority-based pay, which is slower and flatter. If technical depth and fast comp
growth are your goal, weight modern product companies and global-tech, the same employer-type lever
that drives the salary gap drives the growth ceiling.</p>
<div class="callout">Tools: <a href="/insights/salary">Live SWE salary insights</a> ·
<a href="/roadmaps/software-engineering">SWE career roadmap</a> ·
<a href="/jobs?role_family=Software+Engineering">SWE jobs on the board</a></div>
"""
    },

    # ============================================================= TEACHING ENGLISH
    "teaching-english": {
        "key_takeaways": [
            "Teaching is the <strong>easiest field to enter Japan in</strong>, a bachelor's degree in any subject usually suffices for the visa. That's why pay is flat: supply is high.",
            "Tiers: <strong>ALT</strong> (¥230–300k/mo, JET is the premium version), <strong>eikaiwa</strong> (¥250–280k/mo), <strong>international school</strong> (¥4–7M/yr, needs a teaching licence), <strong>university</strong> (MA/PhD).",
            "Entry pay <strong>barely rises with experience</strong>, treat the entry tiers as a door into Japan, not a destination.",
            "<strong>JET</strong> pays more and supports better than private dispatch (Interac, Borderlink); watch dispatch contracts for unpaid school-holiday periods.",
            "A common move: use teaching to study Japanese and build a network, then <strong>pivot</strong> into recruiting, sales/CS, marketing, or tech.",
        ],
        "faqs": [
            ("How much do English teachers make in Japan?",
             "<p>Entry-level teaching pays roughly <strong>¥230,000–300,000/month</strong> for ALT and eikaiwa roles, and it's largely flat regardless of experience. The JET Programme pays more (~¥3.36M/year first year, rising). To earn meaningfully more you move up to <strong>international schools (¥4–7M/year</strong>, requires a teaching licence) or university roles (MA/PhD). It's a comfortable single's salary in a mid-cost city, tight in central Tokyo, and not a savings engine.</p>"),
            ("Do I need a degree or certificate to teach English in Japan?",
             "<p>You generally need a <strong>bachelor's degree in any subject</strong>, that's what qualifies you for the Instructor/Specialist visa. A TEFL/TESOL certificate helps your application and is sometimes required by eikaiwa chains, but isn't universally mandatory. Native or near-native English and being from an English-speaking country matter most for entry-level ALT and eikaiwa roles. International schools require an actual teaching licence.</p>"),
            ("What's the difference between JET and private dispatch (Interac, etc.)?",
             "<p><strong>JET</strong> is the government-run, premium ALT route, higher pay, better support, airfare, and prestige, but competitive with an annual application cycle and placement anywhere (often rural). <strong>Private dispatch companies</strong> (Interac, Borderlink) hire year-round and are easier to get, but pay less and sometimes have unpaid 'shutdown' periods between school terms. Read the contract for whether school holidays are paid.</p>"),
            ("Can I use English teaching to move into a better job in Japan?",
             "<p>Yes, it's a well-trodden path. Enter on a teaching job, use the time in-country to study Japanese and build a network, then pivot into a higher-paying field. Common jumps: teaching → <strong>bilingual recruiting</strong>, → <strong>customer success or sales</strong> at a foreign-capital firm, → <strong>marketing/localization</strong>, or → <strong>tech</strong> via a coding bootcamp and the English-first engineering market. The visa change is a status-of-residence change once you have the new job.</p>"),
        ],
        "extra_toc": [
            ("the-tiers", "The tiers, ALT, eikaiwa, international school, university"),
            ("pay-reality", "Pay reality & why it's flat"),
            ("jet-vs-private", "JET vs private dispatch, the real difference"),
            ("beyond-teaching", "Using teaching as a launchpad"),
            ("teaching-redflags", "Red flags specific to teaching"),
        ],
        "extra_body": """
<hr>
<h2 id="the-tiers">The tiers, ALT, eikaiwa, international school, university</h2>
<table>
  <thead><tr><th>Tier</th><th>What it is</th><th>Typical pay</th><th>Best for</th></tr></thead>
  <tbody>
    <tr><td><strong>ALT</strong> (Assistant Language Teacher)</td><td>Public schools, via JET or a dispatch company</td><td>¥230–300k/mo</td><td>Entry; stable schedule; JET is the premium version</td></tr>
    <tr><td><strong>Eikaiwa</strong></td><td>Private conversation schools (AEON, ECC, etc.)</td><td>¥250–280k/mo</td><td>Easy entry; evening/weekend hours</td></tr>
    <tr><td><strong>International school</strong></td><td>Licensed teachers, real curriculum</td><td>¥4–7M/yr+</td><td>Qualified teachers; career track</td></tr>
    <tr><td><strong>University</strong></td><td>Lecturer/instructor roles</td><td>¥3–6M/yr</td><td>MA/PhD holders; light hours, hard to get</td></tr>
  </tbody>
</table>
<div class="callout">Teaching is the <strong>easiest field to enter Japan in</strong> (a bachelor's
degree in any subject usually suffices for the Instructor/Specialist visa), which is exactly why pay
is flat, supply is high. Treat the entry-level tiers as a <em>door into Japan</em>, not a destination,
unless you pursue the qualified-teacher (international school) or academic track.</p></div>

<h2 id="pay-reality">Pay reality & why it's flat</h2>
<p>Entry teaching pay (¥230–300k/month) has barely moved in years and isn't keyed to experience, a 5-year eikaiwa teacher often earns roughly what a new one does. With the weaker yen, this stretches
less for those servicing foreign-currency debt (student loans). The honest math: it's a comfortable
single's salary in a mid-cost city, tight in central Tokyo, and not a savings engine. The people who
do well financially in teaching either move up to international schools/university, go private
(direct contracts and private lessons), or pivot out (below).</p>

<h2 id="jet-vs-private">JET vs private dispatch, the real difference</h2>
<ul>
  <li><strong>JET Programme:</strong> government-run, the premium ALT route, higher pay (~¥3.36M/yr
      first year, rising), better support, airfare, and prestige. Competitive, annual application
      cycle, placement anywhere in Japan (often rural).</li>
  <li><strong>Private dispatch (Interac, Borderlink, etc.):</strong> year-round hiring, easier to
      get, but lower pay, sometimes "shutdown" unpaid periods between terms, and you're a contractor
      placed in schools. Read the contract for paid-vs-unpaid school holidays.</li>
</ul>

<h2 id="beyond-teaching">Using teaching as a launchpad</h2>
<p>A well-trodden path: enter on a teaching job, use the time in-country to <strong>study Japanese
and build a network</strong>, then pivot into a higher-paying field. Common jumps:</p>
<ul>
  <li>Teaching → <strong>bilingual recruiting</strong> (agencies love English natives who now speak
      some Japanese).</li>
  <li>Teaching → <strong>customer success / sales</strong> at a foreign-capital firm.</li>
  <li>Teaching → <strong>marketing / localization / content</strong>.</li>
  <li>Teaching → <strong>tech</strong>, via a coding bootcamp + the English-first SWE market.</li>
</ul>
<p>The visa transition is a change of status of residence once you have the new job, see the
<a href="/resources/visa-types">visa guide's "changing jobs" section</a>.</p>

<h2 id="teaching-redflags">Red flags specific to teaching</h2>
<ul>
  <li><strong>Unpaid school holidays</strong> dressed up as "flexible schedule."</li>
  <li><strong>"Training pay"</strong> well below the real rate for a long initial period.</li>
  <li><strong>Visa games</strong>, any dispatch company implying they control your visa; they
      sponsor it, they don't own it.</li>
  <li><strong>Solo "eikaiwa" outfits</strong> with no contract clarity, check OpenWork and r/teachinginjapan.</li>
  <li><strong>Self-sponsorship pressure</strong>, be cautious of arrangements that push visa risk
      onto you.</li>
</ul>
<div class="callout">Related: <a href="/resources/red-flags">Black-company red flags</a> ·
<a href="/roadmaps/marketing">Pivot roadmaps</a> · <a href="/resources/jlpt-levels">JLPT to level up</a></div>
"""
    },

    # ============================================================ PRODUCT MANAGEMENT
    "product-management": {
        "key_takeaways": [
            "PM is more foreigner-accessible than most non-engineering roles, but <strong>often needs more Japanese than software</strong>, it's stakeholder- and user-heavy.",
            "The sweet spot: a company <strong>building for Japan but operating in English internally</strong> (Mercari, SmartNews, Rakuten, global-tech Tokyo offices).",
            "Comp: <strong>¥7–10M</strong> mid-level at Japanese product firms, <strong>¥12–20M+</strong> at global tech and senior levels. Bilingual PMs command a clear premium.",
            "<strong>Internal transfer</strong> into a Tokyo office is the cleanest route; engineers, analysts, and consultants also pivot into PM.",
            "Expect a familiar PM loop plus Japan-specific questions about localizing for the market and your 'why Japan' commitment.",
        ],
        "faqs": [
            ("Can foreigners work as product managers in Japan?",
             "<p>Yes, though it's less foreigner-accessible than software because PM is communication- and user-heavy. The friendly employers are global-tech Tokyo offices (Google, Amazon, Indeed, Microsoft), English-first Japanese product firms (Mercari, SmartNews, Rakuten, LINE Yahoo, Money Forward), and foreign-capital SaaS expanding into Japan, where a bilingual PM who can localize the product is highly valued.</p>"),
            ("Do product managers in Japan need to speak Japanese?",
             "<p>Often more than engineers do, PM is stakeholder management, user research, and writing, frequently with Japanese users and teams. English-only PM roles exist at global product orgs and English-first companies, but a large slice of the market wants <strong>business-level Japanese (N2–N1)</strong>. The sweet spot for a foreign PM is a company building <em>for</em> Japan but operating <em>in</em> English internally. If your Japanese is limited, target those explicitly.</p>"),
            ("How much do product managers earn in Japan?",
             "<p>Roughly <strong>¥7–10M for mid-level PM</strong> at Japanese product firms, and <strong>¥12–20M+</strong> at global-tech Tokyo offices and senior/group-PM levels, with equity at the top end. Bilingual PMs command a premium because the pool, strong product sense plus Japanese plus English, is thin. Check the live salary insights for current listings.</p>"),
        ],
        "extra_toc": [
            ("pm-market", "The PM market, who hires foreigners"),
            ("pm-language", "Language: the PM exception"),
            ("pm-comp", "PM compensation bands"),
            ("pm-interview", "The PM interview loop in Japan"),
            ("pm-breaking-in", "Breaking in & internal transfers"),
        ],
        "extra_body": """
<hr>
<h2 id="pm-market">The PM market, who hires foreigners</h2>
<p>Product management is more foreigner-accessible than most non-engineering roles, but less than
software, because PM is communication-heavy and often touches Japanese users. The foreigner-friendly
employers: <strong>global tech Tokyo offices</strong> (Google, Amazon, Indeed, Microsoft),
<strong>English-first Japanese product firms</strong> (Mercari, SmartNews, Rakuten, LINE Yahoo,
Money Forward), and <strong>foreign-capital SaaS</strong> expanding into Japan (where a bilingual PM
who can localize the product and work with Tokyo customers is gold).</p>

<h2 id="pm-language">Language: the PM exception</h2>
<p>Here's the nuance that surprises engineers: <strong>PM often needs more Japanese than SWE</strong>,
because the job is stakeholder management, user research, and writing, frequently with Japanese
users and teams. English-only PM roles exist (global product orgs, English-first companies), but a
large slice of the market wants <strong>business-level Japanese (N2–N1)</strong>. The sweet spot for
a foreign PM is a company building <em>for</em> Japan but operating <em>in</em> English internally, your outside perspective plus their English working language. If your Japanese is limited, target
those explicitly.</p>

<h2 id="pm-comp">PM compensation bands</h2>
<p>PM comp tracks the same employer-type gap as engineering. Rough bands: <strong>¥7–10M</strong> for
mid-level PM at Japanese product firms, <strong>¥12–20M+</strong> at global-tech Tokyo offices and
senior/group PM levels, with equity at the top end. Bilingual PMs command a premium because the
talent pool, strong product sense <em>and</em> Japanese <em>and</em> English, is thin. Check
<a href="/insights/salary">live salary insights</a> for current listings.</p>

<h2 id="pm-interview">The PM interview loop in Japan</h2>
<p>Familiar to anyone who's done PM loops elsewhere: product-sense / product-design, execution /
analytics, behavioural/leadership, and often a take-home or case. Japan-specific add-ons: expect
questions about <strong>localizing for the Japanese market</strong>, working across a
Japanese/English team, and your <strong>"why Japan"</strong> commitment. At global firms it's run in
English, often remotely.</p>

<h2 id="pm-breaking-in">Breaking in & internal transfers</h2>
<ul>
  <li><strong>Internal transfer</strong> is the cleanest route, if your current company has a Tokyo
      office, transferring in as a PM sidesteps the cold market and the visa is employer-handled.</li>
  <li><strong>From adjacent roles</strong>, engineers, analysts, and consultants pivot into PM;
      Japan's English-first product firms are open to this.</li>
  <li><strong>From abroad</strong>, harder than SWE (more language-sensitive), but global-tech Tokyo
      offices do hire and relocate foreign PMs. Lead with shipped products and measurable impact.</li>
</ul>
<div class="callout">Tools: <a href="/roadmaps/product-management">PM career roadmap</a> ·
<a href="/insights/salary">Salary insights</a> ·
<a href="/jobs?role_family=Product+Management">PM jobs on the board</a></div>
"""
    },

    # ============================================================== MARKETING & GROWTH
    "marketing-growth": {
        "key_takeaways": [
            "Marketing is <strong>language-sensitive</strong>, Japanese-market content marketing needs native-level Japanese, but large parts of modern marketing don't.",
            "Foreigner-friendly slices: <strong>global brands' Japan marketing, B2B/SaaS, international/English content, and growth/performance marketing</strong> (data-driven, less language-bound).",
            "Steer toward <strong>data- and systems-heavy</strong> functions if your Japanese isn't native: paid acquisition, marketing ops, analytics, SEO, product marketing.",
            "Comp: <strong>¥5–8M</strong> mid-level, <strong>¥10–18M+</strong> senior/director at foreign-capital firms. The <strong>bilingual premium is steep</strong>.",
            "Break in with a specialism Japan is short on, a portfolio of measurable results (CAC, ROAS, pipeline), and foreign-capital/global-brand targets.",
        ],
        "faqs": [
            ("Can foreigners work in marketing in Japan without fluent Japanese?",
             "<p>In specific functions, yes. Japanese-market <em>content</em> marketing genuinely needs native-level Japanese, but many modern marketing functions are less language-bound: <strong>paid/performance marketing, marketing operations, analytics, SEO, and product marketing for global products</strong>. The foreigner-friendly employers are global brands' Japan offices, foreign-capital SaaS, and companies marketing out of Japan to global audiences. Steer toward the data- and systems-heavy roles if your Japanese is limited.</p>"),
            ("What marketing roles hire foreigners in Japan?",
             "<p>The most accessible: <strong>growth/performance marketing</strong> (paid channels, CRO, analytics), <strong>marketing operations</strong> (HubSpot/Marketo/Salesforce), <strong>product marketing</strong> for global products, <strong>B2B/demand gen</strong> at foreign-capital SaaS, <strong>international/English content and community</strong> (expat, tourism, global brand), and <strong>partnerships/influencer</strong> for brands entering Japan.</p>"),
            ("How much do marketers earn in Japan?",
             "<p>Roughly <strong>¥5–8M for mid-level</strong> and <strong>¥10–18M+ for senior/manager/director</strong> roles at foreign-capital firms. The bilingual premium is steep, a marketer who can run both Japanese campaigns and English HQ reporting is rare and well-paid. Pure English-only marketing roles exist but are fewer and cap lower than the bilingual track.</p>"),
        ],
        "extra_toc": [
            ("mkt-where", "Where foreign marketers fit"),
            ("mkt-language", "The language divide in marketing"),
            ("mkt-roles", "Roles that hire foreigners most"),
            ("mkt-comp", "Compensation & the bilingual premium"),
            ("mkt-breaking-in", "How foreigners actually break in"),
        ],
        "extra_body": """
<hr>
<h2 id="mkt-where">Where foreign marketers fit</h2>
<p>Marketing is language-sensitive, most consumer marketing in Japan happens in Japanese, for
Japanese audiences. So the foreigner-friendly slices are specific: <strong>global brands' Japan
marketing</strong> (where HQ wants English reporting), <strong>B2B / SaaS marketing</strong> at
foreign-capital firms, <strong>international/English-content marketing</strong> (targeting expats,
tourists, or global audiences from Japan), and <strong>growth/performance marketing</strong> (more
data- and tool-driven, less language-bound).</p>

<h2 id="mkt-language">The language divide in marketing</h2>
<p>Blunt truth: <strong>Japanese-market content marketing requires native-level Japanese</strong>, nuance, tone, and cultural fluency you can't fake. But large parts of modern marketing are less
language-bound: paid acquisition, marketing ops/automation, analytics, SEO/technical, and product
marketing for global products. If your Japanese isn't native, steer toward these
<strong>data- and systems-heavy</strong> functions, or toward roles marketing <em>out of</em> Japan
to global audiences.</p>

<h2 id="mkt-roles">Roles that hire foreigners most</h2>
<ul>
  <li><strong>Growth / performance marketing</strong>, paid channels, CRO, analytics.</li>
  <li><strong>Marketing operations</strong>, HubSpot/Marketo/Salesforce, attribution, lifecycle.</li>
  <li><strong>Product marketing (PMM)</strong> for global products.</li>
  <li><strong>B2B / demand gen</strong> at foreign-capital SaaS.</li>
  <li><strong>International / English content & community</strong> (expat, tourism, global brand).</li>
  <li><strong>Partnerships / influencer</strong> for global brands entering Japan.</li>
</ul>

<h2 id="mkt-comp">Compensation & the bilingual premium</h2>
<p>Bands run roughly <strong>¥5–8M</strong> for mid-level, <strong>¥10–18M+</strong> for senior /
manager / director at foreign-capital firms. The <strong>bilingual premium is steep</strong>: a
marketer who can run both Japanese campaigns and English HQ reporting is rare and well-paid. Pure
English-only marketing roles exist but are fewer and cap lower than the bilingual track.</p>

<h2 id="mkt-breaking-in">How foreigners actually break in</h2>
<ul>
  <li><strong>Bring a specialism Japan is short on</strong>, modern growth/ops/analytics skills are
      in demand and travel across languages.</li>
  <li><strong>Target global brands' Japan offices and foreign-capital SaaS</strong>, where English is
      a working language.</li>
  <li><strong>Use a portfolio of measurable results</strong> (CAC, ROAS, pipeline), numbers beat
      language polish for performance roles.</li>
  <li><strong>Pivot in from teaching/CS</strong> by learning a tool stack and starting in marketing
      ops or growth.</li>
</ul>
<div class="callout">Tools: <a href="/roadmaps/marketing">Marketing roadmap</a> ·
<a href="/insights/salary">Salary insights</a> ·
<a href="/jobs?role_family=Marketing">Marketing jobs</a></div>
"""
    },

    # ============================================================ FINANCE & ACCOUNTING
    "finance-accounting": {
        "key_takeaways": [
            "Segments differ sharply: <strong>foreign investment banks/asset managers</strong> (English-heavy front office, highest pay) and <strong>foreign-capital corporate finance/FP&A</strong> (English HQ reporting) are most foreigner-friendly.",
            "Corporate finance and accounting usually want <strong>business Japanese (N2–N1)</strong>; front-office IB can be English-first.",
            "Qualifications travel well: <strong>CPA, ACCA, CFA, and Big-4 experience</strong> are strong signals. Bilingual + qualified is one of the most employable foreign profiles in Japan.",
            "Comp: <strong>¥6–12M</strong> mid-level corporate finance, <strong>¥15M+</strong> for controller/director; front-office IB much higher.",
            "Finance is the field where <strong>specialist recruiters add real value</strong>, Robert Walters, Michael Page, Hays, Morgan McKinley dominate bilingual placement.",
        ],
        "faqs": [
            ("Can foreigners work in finance and accounting in Japan?",
             "<p>Yes, especially in the foreigner-friendly segments: <strong>foreign investment banks and asset managers</strong> (English-heavy front office), <strong>foreign-capital corporate finance / FP&A / controllership</strong> (multinationals needing English reporting to HQ), and fintech/global-SaaS finance teams. Japanese megabanks and domestic finance are largely Japanese-language and less accessible. A bilingual accountant with a recognised qualification is one of the most reliably employable foreign profiles.</p>"),
            ("Do I need Japanese for finance jobs in Japan?",
             "<p>It depends on the role. Front-office roles at foreign banks can be English-first, but <strong>corporate finance and accounting usually want business Japanese (N2–N1)</strong> because you interface with Japanese auditors, tax authorities, and local teams. The strongest position is bilingual plus a recognised qualification, that pool is thin and well-paid.</p>"),
            ("What qualifications help for finance jobs in Japan?",
             "<p>Internationally recognised credentials travel well: <strong>CPA (US or Japanese 公認会計士), ACCA, CFA, and Big-4 audit/advisory experience</strong> are strong signals. Combined with business Japanese, they open the corporate-finance market sharply. Finance is also the field where building a relationship with one or two <strong>specialist recruiters</strong> (Robert Walters, Michael Page, Hays, Morgan McKinley, en world) is often more effective than cold applications.</p>"),
        ],
        "extra_toc": [
            ("fin-segments", "The segments, where foreigners work"),
            ("fin-language", "Language & qualifications"),
            ("fin-comp", "Compensation bands"),
            ("fin-employers", "Employers & the recruiter route"),
            ("fin-breaking-in", "Breaking in"),
        ],
        "extra_body": """
<hr>
<h2 id="fin-segments">The segments, where foreigners work</h2>
<p>Finance in Japan splits into segments with very different foreigner-friendliness:</p>
<ul>
  <li><strong>Foreign investment banks & asset managers</strong> (Tokyo offices of global firms), English-heavy front office; the most foreigner-friendly and highest-paying.</li>
  <li><strong>Foreign-capital corporate finance / FP&A / controllership</strong>, multinationals'
      Japan entities needing English reporting to HQ. A steady, accessible niche.</li>
  <li><strong>Fintech & global SaaS finance teams</strong>, growing, bilingual.</li>
  <li><strong>Japanese megabanks / domestic finance</strong>, largely Japanese-language, less
      foreigner-accessible.</li>
</ul>

<h2 id="fin-language">Language & qualifications</h2>
<p>Front-office roles at foreign banks can be English-first; <strong>corporate finance and accounting
usually want business Japanese (N2–N1)</strong> because you interface with Japanese auditors, tax,
and local teams. Qualifications travel well: <strong>CPA (US or Japanese 公認会計士), ACCA, CFA, and
Big-4 experience</strong> are strong signals. A bilingual accountant with a recognised qualification
is one of the most reliably employable foreign profiles in Japan.</p>

<h2 id="fin-comp">Compensation bands</h2>
<p>Wide range by segment. Corporate finance / FP&A / accounting at foreign-capital firms:
roughly <strong>¥6–12M</strong> mid-level, <strong>¥15M+</strong> for controller/finance-director.
Front-office IB / asset management runs substantially higher with bonus. Bilingual finance
professionals command a clear premium, the bilingual-plus-qualified pool is thin.</p>

<h2 id="fin-employers">Employers & the recruiter route</h2>
<p>Finance is the field where <strong>specialist recruiters genuinely add value</strong>, Robert
Walters, Michael Page, Hays, Morgan McKinley, and en world dominate bilingual finance placement and
run the relationships with foreign-capital employers. Building a relationship with one or two good
finance recruiters is often more effective than cold applications here. (Their annual salary surveys
are also a useful benchmark.)</p>

<h2 id="fin-breaking-in">Breaking in</h2>
<ul>
  <li><strong>Lead with a qualification</strong> (CPA/CFA/ACCA) and Big-4 or multinational experience.</li>
  <li><strong>Target foreign-capital Japan entities</strong> that need English HQ reporting.</li>
  <li><strong>Work the specialist recruiters</strong> rather than only applying cold.</li>
  <li><strong>Build business Japanese</strong>, it widens the corporate-finance market sharply.</li>
</ul>
<div class="callout">Tools: <a href="/roadmaps/finance-accounting">Finance roadmap</a> ·
<a href="/insights/salary">Salary insights</a> ·
<a href="/jobs?role_family=Finance+%26+Accounting">Finance jobs</a></div>
"""
    },

    # ==================================================== SALES & BUSINESS DEVELOPMENT
    "sales-business-development": {
        "key_takeaways": [
            "Sales is the <strong>language-heaviest field</strong>, selling to Japanese customers needs native/near-native Japanese and deep cultural fluency.",
            "The foreigner path is specific: sell <strong>in English, to global/foreign customers</strong>, or in a role where your foreignness is an asset.",
            "Friendly zones: foreign-capital SaaS selling to MNC accounts, inside sales/SDR at global tech, partner/alliance management, <strong>customer success</strong> (a softer landing, ¥6–10M), and Japan-market-entry BD.",
            "Comp is <strong>OTE (base + variable)</strong>, often 50/50 or 60/40; mid-level AE OTE ¥10–18M. Check whether variable is guaranteed during ramp.",
            "Bilingual ability multiplies options dramatically, if you can build it, the whole Japanese sales market opens.",
        ],
        "faqs": [
            ("Can foreigners work in sales in Japan without fluent Japanese?",
             "<p>Only in specific roles. Selling to Japanese customers requires native or near-native Japanese plus cultural fluency (relationship-building, keigo, the consensus-driven sales cycle), so this is the least forgiving field for limited Japanese. The foreigner path: sell <strong>in English to global or foreign customers</strong>, foreign-capital SaaS selling to multinational accounts, inside sales at global tech, partner management, or customer success, where the buyer often operates in English too.</p>"),
            ("What sales roles are realistic for foreigners in Japan?",
             "<p>The accessible ones: <strong>foreign-capital SaaS selling to multinational accounts</strong>, <strong>inside sales/SDR at global tech</strong> targeting English-speaking accounts, <strong>partner/alliance/channel management</strong>, <strong>customer success</strong> (a softer landing than net-new sales, English-first SaaS hires foreign CSMs at ¥6–10M), and <strong>business development for Japan market entry</strong>, where your bridge between cultures is the whole value.</p>"),
            ("How does sales compensation work in Japan?",
             "<p>Sales comp is <strong>OTE (on-target earnings) = base + variable</strong>. Foreign-capital SaaS typically runs a 50/50 or 60/40 base/variable split; a mid-level AE's total OTE is often <strong>¥10–18M</strong>, more for enterprise reps who hit quota, with accelerators above target. Watch the offer details: is the variable <strong>guaranteed during ramp</strong>? What's the quota and territory? Is commission capped?</p>"),
        ],
        "extra_toc": [
            ("sales-reality", "The reality, sales is the language-heaviest field"),
            ("sales-where", "Where foreigners sell successfully"),
            ("sales-comp", "Compensation & OTE structure"),
            ("sales-interview", "The interview & ramp"),
            ("sales-breaking-in", "Breaking in"),
        ],
        "extra_body": """
<hr>
<h2 id="sales-reality">The reality, sales is the language-heaviest field</h2>
<p>Be honest with yourself: <strong>selling to Japanese customers requires native or near-native
Japanese and deep cultural fluency</strong>, relationship-building (nemawashi), keigo, and the long,
consensus-driven Japanese sales cycle. This is the least forgiving field for limited Japanese. So the
foreigner path in sales is specific: you sell <em>in English</em>, to <em>global or foreign</em>
customers, or in a role where your foreignness is an asset.</p>

<h2 id="sales-where">Where foreigners sell successfully</h2>
<ul>
  <li><strong>Foreign-capital SaaS selling to multinational accounts in Japan</strong>, the buyer
      is often itself an English-operating company.</li>
  <li><strong>Inside sales / SDR at global tech</strong> targeting English-speaking or global accounts.</li>
  <li><strong>Partner / alliance / channel management</strong> with global partners.</li>
  <li><strong>Customer success</strong>, a softer landing than net-new sales; English-first SaaS
      hires foreign CSMs to manage global and bilingual accounts (¥6–10M is common).</li>
  <li><strong>Business development for Japan market entry</strong>, helping a foreign company enter
      Japan, where your bridge between cultures is the whole value.</li>
</ul>

<h2 id="sales-comp">Compensation & OTE structure</h2>
<p>Sales comp is <strong>OTE (on-target earnings) = base + variable</strong>. Foreign-capital SaaS in
Japan typically runs a <strong>50/50 or 60/40 base/variable</strong> split; total OTE for a mid-level
AE often <strong>¥10–18M</strong>, more for enterprise reps who hit quota, with accelerators above
target. Watch the details in an offer: is the variable <strong>guaranteed during ramp</strong>? what's
the <strong>quota and territory</strong>? is commission capped? See the
<a href="/pillars/negotiation-playbook">negotiation playbook</a> for sales-specific asks.</p>

<h2 id="sales-interview">The interview & ramp</h2>
<p>Expect a familiar SaaS-sales loop: recruiter screen, hiring-manager, a <strong>mock pitch / role
play</strong>, and often a panel. They'll probe your <strong>methodology</strong> (MEDDIC, Challenger,
etc.), your numbers (quota attainment history), and, in Japan, your understanding of the local
buying culture even if you sell in English. Ramp expectations and the comp structure during ramp are
fair game to negotiate.</p>

<h2 id="sales-breaking-in">Breaking in</h2>
<ul>
  <li><strong>Target English-operating buyers</strong>, foreign-capital SaaS selling to MNC accounts
      is your zone.</li>
  <li><strong>Start in CS or inside sales</strong> if net-new field sales in Japanese is closed to you.</li>
  <li><strong>Lead with quota attainment numbers</strong>, sales hiring is metrics-driven.</li>
  <li><strong>Bilingual ability multiplies your options</strong> dramatically; if you can build it,
      the whole Japanese sales market opens.</li>
</ul>
<div class="callout">Tools: <a href="/roadmaps/sales-business-development">Sales & BD roadmap</a> ·
<a href="/pillars/negotiation-playbook">Negotiation playbook</a> ·
<a href="/jobs?role_family=Sales+%26+Business+Development">Sales jobs</a></div>
"""
    },
}


def merge_guide(item: dict) -> dict:
    """Return a shallow copy of a guide dict with its deep-dive extension (extra
    TOC + extra body) appended, if one exists for that slug."""
    if not item:
        return item
    extra = GUIDE_EXTRAS.get(item.get("slug"))
    if not extra:
        return item
    merged = dict(item)
    merged["toc"] = list(item.get("toc", [])) + list(extra.get("extra_toc", []))
    merged["body"] = item.get("body", "") + extra.get("extra_body", "")
    if extra.get("key_takeaways"):
        merged["key_takeaways"] = extra["key_takeaways"]
    if extra.get("faqs"):
        merged["faqs"] = extra["faqs"]
    return merged
