"""
"Living in Japan" content registry, the post-offer relocation & settlement
journey. Deep, specific, sub-sectioned guides.

Same shape as content.RESOURCES (slug / icon / title / summary / updated /
read_time / toc / body). Figures are 2025–26 and deliberately concrete (named
institutions, real yen amounts, timelines). Where rules are mid-change, the
change and its timing are called out rather than hidden. This is orientation,
not legal advice, visa/tax specifics should be confirmed with the Immigration
Services Agency of Japan, the Japan Pension Service, or a licensed professional
(行政書士 / 税理士).
"""

LIVING_GUIDES: list[dict] = [

    # ===================================================================== COE
    {
        "slug": "coe-and-arrival",
        "icon": "plane",
        "title": "Certificate of Eligibility & arrival, from offer to landing",
        "summary": "The COE is the document that makes your visa happen. Who files it, the real 1–3 month timeline, the digital-COE shortcut, what to do at the airport, and the 14-day clock with a ¥200,000 fine attached.",
        "updated": "June 2026",
        "read_time": "16 min",
        "key_takeaways": [
            "Three gates, in order: <strong>COE</strong> (immigration pre-approval, filed by your employer in Japan) → <strong>visa</strong> (stamped at an embassy abroad) → <strong>landing permission</strong> (the airport, where you get your Residence Card).",
            "Your <strong>employer files the COE</strong>, you can't do it from abroad. Plan <strong>2–4 months</strong> from signed offer to first day.",
            "Ask if they'll issue a <strong>digital COE (since 2023)</strong>, it's emailed as a PDF and skips the international-mail leg.",
            "From move-in you have <strong>14 days to register your address</strong> at the ward office, or risk a fine up to ¥200,000. This one visit unlocks insurance, pension, My Number, and banking.",
            "Carry your <strong>Residence Card at all times</strong>, it's a legal requirement and your most-used document.",
        ],
        "faqs": [
            ("What is a Certificate of Eligibility (COE) and who applies for it?",
             "<p>The COE (在留資格認定証明書) is a pre-approval from Japan's Immigration Services Agency confirming you qualify for a status of residence. It's <strong>not your visa</strong>, it's the document that makes the visa a formality. <strong>Your employer (or their immigration lawyer) files it in Japan on your behalf</strong>; you cannot file it yourself from abroad. With the COE you then get the actual visa at a Japanese embassy in your country.</p>"),
            ("How long does it take to move to Japan after accepting a job?",
             "<p>Plan for <strong>2–4 months</strong> end to end. The COE alone takes 1–3 months at immigration, then ~1 week for the embassy visa, plus your own move logistics. It's slower around the April and autumn intake crunches. The 2023 digital COE removes the international-mail step if your employer opts in.</p>"),
            ("What is the 14-day rule when arriving in Japan?",
             "<p>Within <strong>14 days of moving into your address</strong>, you must file a move-in notification (転入届) at your local ward/municipal office. It's enforced, penalties run up to ¥200,000 under the Immigration Control Act. Beyond the fine, this single registration is what unlocks your residence record, health insurance, pension, My Number, and the ability to open a bank account, so it's the first errand to run.</p>"),
            ("What do I need to do at the airport when I arrive in Japan?",
             "<p>At major airports (Haneda, Narita, Kansai, Chubu, Fukuoka) immigration checks your passport, visa, and COE, takes your photo and fingerprints, and issues your <strong>Residence Card on the spot</strong>. Pre-register on <strong>Visit Japan Web</strong> before flying for faster QR-code processing. Then carry your Residence Card at all times and head to the ward office within 14 days.</p>"),
            ("Should I bring my university diploma to Japan?",
             "<p>Yes, and order an <strong>extra official copy before you leave home</strong>. Your work visa rests on a relevant degree (or 10+ years' experience), and you may need the diploma again years later for a visa renewal or permanent-residence application. Re-ordering from abroad is slow and sometimes impossible. Also pack restricted-medication import certificates (yakkan shoumei) if relevant, and 10–15 spare passport photos.</p>"),
        ],
        "toc": [
            ("what-is-coe", "What the COE actually is"),
            ("three-gates", "The three gates: COE, visa, landing"),
            ("who-files", "Who files it, you don't"),
            ("timeline", "The real timeline (2–4 months end to end)"),
            ("digital-coe", "Digital COE, the 2023 shortcut"),
            ("documents", "Documents your employer will ask for"),
            ("documents-you-keep", "Documents to bring for yourself"),
            ("visa-stamp", "Turning the COE into a visa"),
            ("airport", "At the airport, landing permission"),
            ("residence-card", "Your Residence Card, carry it always"),
            ("14-days", "The 14-day clock (¥200,000 fine)"),
            ("first-week", "Arrival-week sequence"),
            ("pitfalls", "Common mistakes that cost weeks"),
            ("checklist", "Printable arrival checklist"),
        ],
        "body": """
<h2 id="what-is-coe">What the COE actually is</h2>
<p>The <strong>Certificate of Eligibility (在留資格認定証明書, <em>zairyū shikaku nintei
shōmeisho</em>)</strong> is not your visa. It is a pre-approval issued by the Immigration
Services Agency of Japan (出入国在留管理庁) confirming you meet the conditions for a status of
residence, for most readers, Engineer / Specialist in Humanities / International Services. With
a COE in hand the actual visa is a near-formality stamped by a Japanese embassy or consulate
abroad. Without one, a work visa is effectively impossible to obtain.</p>

<h2 id="three-gates">The three gates: COE, visa, landing</h2>
<p>Almost every confusion about Japanese immigration dissolves once you see it as three separate
gates, in strict order:</p>
<table>
  <thead><tr><th>Gate</th><th>Who says yes</th><th>Where</th><th>Result</th></tr></thead>
  <tbody>
    <tr><td>1. COE</td><td>Immigration Services Agency</td><td>Inside Japan (your employer files)</td><td>"This person qualifies"</td></tr>
    <tr><td>2. Visa</td><td>Japanese embassy/consulate</td><td>Your home country</td><td>"You may board a plane"</td></tr>
    <tr><td>3. Landing permission</td><td>Immigration officer</td><td>The airport</td><td>"You may enter" + Residence Card</td></tr>
  </tbody>
</table>
<div class="callout">You can't skip or reorder these. The COE is the slow one and the gate your
employer controls, which is why everything below focuses on it.</div>

<h2 id="who-files">Who files it, you don't</h2>
<p>Your <strong>employer</strong>, or the immigration lawyer / administrative scrivener
(行政書士, <em>gyōsei shoshi</em>) they retain, files the COE application at the regional
immigration bureau covering their office. <strong>You cannot file it from abroad yourself.</strong>
This is why HR asks you for documents weeks before your start date: they're assembling the packet.</p>
<h3>Why a responsive employer matters</h3>
<p>A company that files quickly and cleanly is one of the best signals of an employer worth
joining. Chasing a COE through a disorganised HR team is one of the most common, and most
avoidable, sources of delay. If your start date is slipping because the company hasn't filed,
that is a yellow flag about how the rest of the job will run.</p>

<h2 id="timeline">The real timeline (2–4 months end to end)</h2>
<p>Plan for the <strong>COE alone to take 1–3 months</strong> from filing to issuance, then add
the embassy visa step and your own logistics. A realistic end-to-end expectation from signed offer
to first day in Tokyo is <strong>2 to 4 months</strong>.</p>
<table>
  <thead><tr><th>Step</th><th>Typical duration</th><th>Who acts</th></tr></thead>
  <tbody>
    <tr><td>You send documents to employer</td><td>Days 0–14</td><td>You</td></tr>
    <tr><td>Employer files COE at immigration</td><td>Week 2–3</td><td>Employer / scrivener</td></tr>
    <tr><td>Immigration processing</td><td>2–10 weeks</td><td>Immigration Services Agency</td></tr>
    <tr><td>COE delivered (paper couriered, or digital PDF same-day)</td><td>0–7 days</td><td>Employer → you</td></tr>
    <tr><td>Visa application at embassy/consulate</td><td>~5 business days</td><td>You</td></tr>
    <tr><td>Fly to Japan, landing permission</td><td>1 day</td><td>You</td></tr>
  </tbody>
</table>
<div class="warn"><strong>Peak-season drag:</strong> COE processing slows noticeably before the
April corporate intake and the autumn term. Filing outside those crunches can shave weeks. Bureau
workload also varies by region, Tokyo and Osaka bureaus are busier than smaller prefectures.</div>

<h2 id="digital-coe">Digital COE, the 2023 shortcut</h2>
<p>Since March 2023, Japan issues a <strong>Digital Certificate of Eligibility</strong>, the COE
delivered as a PDF by email rather than a physical sheet couriered internationally. If your
employer opts into the digital COE, you skip the 1–2 week international mail leg entirely: they
email you the PDF and you take it (printed, plus the reference) to the embassy. Ask your HR
explicitly whether they're issuing a digital or paper COE; it can be the difference of a week or
more, and a digital COE can't get lost in transit.</p>

<h2 id="documents">Documents your employer will ask for</h2>
<ul>
  <li><strong>Passport</strong> photo page (often a full scan).</li>
  <li><strong>Photo</strong> to spec, 4cm × 3cm, taken within 3 months, plain background.</li>
  <li><strong>Degree certificate / diploma</strong>, the Engineer/Specialist visa rests on a
      relevant degree <em>or</em> 10+ years of relevant experience. Keep an official copy.</li>
  <li><strong>CV / résumé</strong> in the company's format.</li>
  <li><strong>Sometimes:</strong> a diploma/transcript translation, professional certificates, or
      a short written explanation of how your degree relates to the role (immigration wants the
      job to match your background).</li>
</ul>
<div class="callout"><strong>Do this before you leave home:</strong> order an <em>extra official
copy</em> of your university diploma and transcript. Requesting one later from abroad is slow and
occasionally impossible, and you may need it again years later for a visa renewal or your
permanent-residence application.</div>

<h2 id="documents-you-keep">Documents to bring for yourself</h2>
<p>Separate from the COE packet, pack a "bureaucracy kit" you'll draw on for months:</p>
<ul>
  <li>10–15 spare <strong>passport photos</strong> (every application wants one).</li>
  <li><strong>International Driving Permit</strong> (valid 1 year) if you might drive; after that
      you need to convert to a Japanese licence (外免切替).</li>
  <li><strong>Vaccination / medical records</strong>, and a few months of any prescription
      medication with its generic name (some common Western meds are restricted, check before
      flying; ADHD stimulants in particular need a <em>yakkan shoumei</em> import certificate).</li>
  <li>A <strong>credit card from home</strong> that works abroad, plus enough cash/forex for
      4–6 months of move-in costs (Japanese payroll lags; see the relocation budget calculator).</li>
  <li>Digital + paper copies of your <strong>degree, birth certificate, and (if relevant)
      marriage certificate</strong>, ideally with certified translations for dependents.</li>
</ul>

<h2 id="visa-stamp">Turning the COE into a visa</h2>
<p>Once you have the COE (paper or digital), take it plus your passport, the embassy's visa
application form, and a photo to the Japanese embassy/consulate with jurisdiction over your
residence. The visa is usually issued in about <strong>5 business days</strong>. It is
<strong>single-entry and valid for 3 months</strong>, you must enter Japan within 3 months of
issuance. Don't apply until your move date is reasonably locked.</p>

<h2 id="airport">At the airport, landing permission</h2>
<p>At a major airport (Haneda, Narita, Kansai, Chubu, Fukuoka) immigration will:</p>
<ol>
  <li>Check your passport, visa, and COE.</li>
  <li>Take your <strong>photo and fingerprints</strong>.</li>
  <li>Issue your <strong>Residence Card (在留カード)</strong> on the spot at those major airports.
      At smaller ports of entry it is mailed to your registered address later.</li>
</ol>
<p>Use the <strong>Visit Japan Web</strong> service to pre-register immigration and customs before
you fly, it produces QR codes that speed the airport queues considerably.</p>

<h2 id="residence-card">Your Residence Card, carry it always</h2>
<p>The Residence Card is your single most important document in Japan, and by law you must
<strong>carry it at all times</strong>. It states your status of residence, period of stay, work
eligibility, and (after you register) your address on the back. You'll show it constantly: ward
office, phone contract, bank, even some gyms.</p>
<div class="warn"><strong>Coming 2025–26:</strong> the government is integrating the Residence
Card and the My Number Card functions to reduce duplicate paperwork for foreign residents. Until
that's fully live, treat them as two separate must-have cards.</div>

<h2 id="14-days">The 14-day clock (¥200,000 fine)</h2>
<p>From the day you move into your address, you have <strong>14 days to register it</strong> at
the local ward/municipal office by filing a move-in notification (転入届). This is not optional
paperwork: failing to register your residence can draw a fine of up to <strong>¥200,000</strong>
under the Immigration Control Act, plus up to ¥50,000 under the Basic Resident Registration Act.
More practically, the registration is the keystone that unlocks health insurance, pension, My
Number, and your ability to open a bank account, so missing it stalls everything. See the
dedicated <a href="/living/ward-office">ward office guide</a> for the counter-by-counter walkthrough.</p>

<h2 id="first-week">Arrival-week sequence</h2>
<p>Order matters because each step unlocks the next:</p>
<ol>
  <li><strong>Secure an address</strong>, corporate housing, a share house, or a short lease. You
      need one to register.</li>
  <li><strong>Ward office</strong> (within 14 days) → residence record (jūminhyō), health
      insurance + pension enrolment, My Number issued.</li>
  <li><strong>Phone number</strong>, a foreigner-friendly SIM works before you have a bank account.</li>
  <li><strong>Bank account</strong>, now that you have an address + phone + residence card.</li>
  <li>Give your employer your <strong>My Number and bank details</strong> for payroll.</li>
</ol>

<h2 id="pitfalls">Common mistakes that cost weeks</h2>
<ul>
  <li><strong>Applying for the embassy visa too early</strong>, it expires in 3 months; time it
      to your actual departure.</li>
  <li><strong>No address on arrival</strong>, you can't register, bank, or get a normal SIM.
      Book a share house or use corporate housing for week one.</li>
  <li><strong>Leaving the diploma behind</strong>, re-ordering from abroad can derail a renewal.</li>
  <li><strong>Bringing restricted medication</strong> without a <em>yakkan shoumei</em>, it can be
      confiscated at customs.</li>
  <li><strong>Assuming salary lands immediately</strong>, first pay can be 4–6 weeks out; that
      plus move-in costs makes month one the tightest cash window of the whole move.</li>
</ul>

<h2 id="checklist">Printable arrival checklist</h2>
<ul>
  <li>☐ COE received (digital PDF or paper) and visa stamped in passport</li>
  <li>☐ Visit Japan Web pre-registration done</li>
  <li>☐ Residence Card received at airport; carry it always</li>
  <li>☐ Address secured (corporate housing / share house / lease)</li>
  <li>☐ Within 14 days: ward office → jūminhyō, NHI/pension, My Number</li>
  <li>☐ A few jūminhyō copies in hand for bank/phone</li>
  <li>☐ Japanese phone number active</li>
  <li>☐ Bank account opened</li>
  <li>☐ My Number + bank details given to employer</li>
  <li>☐ Suica/PASMO + a cashless app (PayPay) set up</li>
</ul>
<div class="callout">Next: <a href="/living/ward-office">Ward office & My Number</a> ·
<a href="/living/housing">Renting an apartment</a> ·
<a href="/living/banking">Opening a bank account</a> ·
<a href="/tools/relocation-budget">Relocation budget calculator</a></div>
"""
    },

    # ================================================================= HOUSING
    {
        "slug": "housing",
        "icon": "building",
        "title": "Renting an apartment, guarantors, key money, and the real move-in cost",
        "summary": "Why your first apartment costs 4–6 months' rent upfront, every fee decoded, how guarantor companies work for foreigners, the zero-zero and UR shortcuts, reading a Japanese lease, and getting your deposit back.",
        "updated": "June 2026",
        "read_time": "18 min",
        "key_takeaways": [
            "Expect <strong>4–6 months' rent upfront</strong>, a ¥100k/month apartment typically needs ¥400–600k cash before you get the keys, much of it non-refundable (key money, agency, guarantor fees).",
            "<strong>Guarantor companies (保証会社)</strong> solve the no-Japanese-relative problem, you pay ~0.5–1 month upfront, they guarantee your rent. Standard, not a red flag.",
            "Cut upfront cost with <strong>'zero-zero' listings</strong> (no key money/deposit), a <strong>share house</strong> for the first months, or <strong>UR housing</strong> (no key money, no guarantor, no agency fee, if you meet the income bar).",
            "Some landlords still refuse foreigners, filter for <strong>外国人可 ('foreigners OK')</strong> and use a bilingual agency rather than wasting time.",
            "Budget monthly running costs beyond rent: management fee, utilities, internet, a ¥100k 'rent' apartment really costs ¥125–140k all-in.",
        ],
        "faqs": [
            ("Why is renting an apartment in Japan so expensive upfront?",
             "<p>Japanese leases stack several one-time fees: a <strong>security deposit (敷金, 1–2 months), key money (礼金, a non-refundable gift to the landlord, 0–2 months), agency fee (~1 month), guarantor-company fee, first month's rent, fire insurance, and a lock change</strong>. Together that's commonly 4–6 months' rent, ¥400–600k on a ¥100k apartment. Much of it (key money, fees) you never get back.</p>"),
            ("What is key money (reikin) in Japan?",
             "<p><strong>Key money (礼金, reikin)</strong> is a one-time, non-refundable 'gift' to the landlord, traditionally 0–2 months' rent, paid just to move in. Unlike the deposit, you never get it back. To avoid it, look for <strong>'zero-zero' (ゼロゼロ) listings</strong> with zero key money and zero deposit, increasingly common in newer and foreigner-targeted buildings, and they can roughly halve your move-in cost.</p>"),
            ("Do I need a guarantor to rent in Japan as a foreigner?",
             "<p>Almost always, but you don't need a Japanese relative. The standard solution is a <strong>guarantor company (保証会社)</strong> that stands as your guarantor for a fee (~0.5–1 month upfront, then a smaller annual fee). Companies like GTN specialise in foreigners. Landlords may also want an <strong>emergency contact</strong> in Japan (often your employer or a colleague), which is just a contact, not a financial guarantor.</p>"),
            ("Can foreigners be refused apartments in Japan?",
             "<p>Yes, some landlords still decline foreign tenants, and in housing it isn't prohibited the way it might be in your home country. The practical workarounds: filter from the start for <strong>外国人可 ('foreigners OK')</strong> listings, use a <strong>bilingual/foreigner-focused agency</strong> that pre-screens friendly landlords, and lead with your strengths, a stable employer, work visa, and guarantor company reassure landlords more than anything.</p>"),
            ("What's the cheapest way to find first housing in Japan?",
             "<p>Three low-friction options: a <strong>share house</strong> (Oakhouse, Sakura House, furnished, ~¥30–50k deposit, no guarantor, English staff) for your first 1–3 months; <strong>employer corporate housing</strong> if offered; or <strong>UR housing</strong> (no key money, no guarantor, no agency fee, no renewal fee, if you meet the income requirement). Many people land in a share house, set up bank/phone, then sign a normal lease once they have the paperwork.</p>"),
        ],
        "toc": [
            ("upfront", "The upfront cost shock (4–6× rent)"),
            ("breakdown", "Every move-in fee, decoded"),
            ("apartment-types", "Apartment types & the size code"),
            ("guarantor", "Guarantors & guarantor companies"),
            ("discrimination", "The foreigner barrier, and how to route around it"),
            ("foreigner-friendly", "Foreigner-friendly options"),
            ("ur", "UR Housing, the underused win"),
            ("sharehouse", "Share houses & temporary landing"),
            ("finding", "How to actually find a place"),
            ("viewing", "The viewing & application day"),
            ("contract", "Reading the lease, what to check"),
            ("running-costs", "Monthly running costs beyond rent"),
            ("leaving", "Move-out & getting your deposit back"),
        ],
        "body": """
<h2 id="upfront">The upfront cost shock (4–6× rent)</h2>
<p>The single biggest financial surprise for new arrivals is move-in cost. A ¥100,000/month
apartment typically requires <strong>¥400,000–¥600,000 in cash before you get the keys</strong>,
and total initial costs of <strong>4–6 months' rent</strong> are standard in Tokyo, Osaka, and
Kyoto. This is not a deposit you fully recover, a large chunk is non-refundable. Budget for it
before you fly; it's the line item that ambushes people who assumed "first month + deposit."</p>
<div class="warn">Stack three things and month one is brutal: move-in costs, a relocation, and a
first salary that may not land for 4–6 weeks. Arrive with a cash buffer, see the
<a href="/tools/relocation-budget">relocation budget calculator</a>.</div>

<h2 id="breakdown">Every move-in fee, decoded</h2>
<table>
  <thead><tr><th>Fee</th><th>Japanese</th><th>Typical size</th><th>Refundable?</th></tr></thead>
  <tbody>
    <tr><td>Security deposit</td><td>敷金 shikikin</td><td>1–2 months</td><td>Partly, minus cleaning/repairs</td></tr>
    <tr><td>Key money (gift to landlord)</td><td>礼金 reikin</td><td>0–2 months</td><td>No, never returned</td></tr>
    <tr><td>Agency fee</td><td>仲介手数料 chūkai tesūryō</td><td>0.5–1 month + 10% tax</td><td>No</td></tr>
    <tr><td>Guarantor company fee</td><td>保証会社 hoshō-gaisha</td><td>0.5–1 month initial, then annual</td><td>No</td></tr>
    <tr><td>First month rent (+ prorated)</td><td>前家賃 maeyachin</td><td>1 month +</td><td>It's rent</td></tr>
    <tr><td>Fire insurance</td><td>火災保険 kasai hoken</td><td>¥15–20K / 2 yrs</td><td>No</td></tr>
    <tr><td>Key exchange / lock change</td><td>鍵交換 kagi kōkan</td><td>¥10–25K</td><td>No</td></tr>
    <tr><td>Cleaning fee (sometimes prepaid)</td><td>クリーニング</td><td>¥20–40K</td><td>No</td></tr>
  </tbody>
</table>
<div class="callout"><strong>Hunt for "zero-zero" (ゼロゼロ) listings</strong>, zero reikin, zero
shikikin. They're increasingly common in Tokyo and Osaka, especially in newer buildings and
foreigner-targeted stock, and they can turn a ¥550K move-in into ¥200K. The trade-off is sometimes
slightly higher monthly rent or a fixed move-out cleaning charge, so read the contract, but for a
first apartment they're often the smart play.</div>

<h2 id="apartment-types">Apartment types & the size code</h2>
<p>Listings use a shorthand you'll want to read fluently:</p>
<ul>
  <li><strong>1R</strong> (one room), studio, kitchen not separated. Smallest/cheapest.</li>
  <li><strong>1K</strong>, one room + a separated kitchen. The classic single's apartment.</li>
  <li><strong>1DK / 1LDK</strong>, one bedroom + dining-kitchen / living-dining-kitchen. 1LDK is
      the comfortable single or couple unit.</li>
  <li><strong>2LDK / 3LDK</strong>, family sizes.</li>
  <li><strong>アパート (apāto)</strong> = smaller, often wood/light-steel, cheaper, less
      soundproof. <strong>マンション (manshon)</strong> = reinforced-concrete, sturdier, pricier.</li>
</ul>
<p>Floor area is given in <strong>m²</strong> and rooms in <strong>jō (畳, tatami mats ≈ 1.65m²)</strong>.
"Walk 8 min from X station" (徒歩8分) assumes ~80m/minute. Older buildings (築古, <em>chikko</em>)
are cheaper but may lack insulation and modern bathrooms.</p>

<h2 id="guarantor">Guarantors & guarantor companies</h2>
<p>Most landlords require a <strong>guarantor (保証人, <em>hoshōnin</em>)</strong> who covers your
rent if you default. Few foreigners have a qualifying Japanese relative, so the market solution is
a <strong>guarantor company (保証会社)</strong>: you pay a fee, typically <strong>50–100% of one
month's rent upfront</strong>, then ¥10,000 or ~half a month annually, and they stand as your
guarantor. This is now standard and not a red flag. The fee scales with your perceived risk: visa
type, income, and employer all factor in, so a stable full-time contract lowers it.</p>
<p>Separately, many landlords want an <strong>emergency contact (緊急連絡先)</strong> in Japan, a person they can reach, often your employer or a colleague. That's a contact, not a financial
guarantor, and is usually easy to satisfy.</p>

<h2 id="discrimination">The foreigner barrier, and how to route around it</h2>
<p>Be realistic: some landlords still decline foreign tenants outright, citing language,
move-out risk, or "no foreigners" (外国人不可) policies. It's frustrating and, in housing, not
illegal in the way it would be in many home countries. The practical workarounds:</p>
<ul>
  <li>Filter for <strong>外国人可 ("foreigners OK")</strong> listings from the start, don't waste
      time on units that will reject you.</li>
  <li>Use a <strong>bilingual / foreigner-focused agency</strong> (below) that pre-screens for
      foreigner-friendly landlords.</li>
  <li>Lead with your strengths: <strong>stable employer, work visa, guarantor company</strong>.
      A signed employment contract reassures landlords more than anything.</li>
  <li>If you have zero Japanese, bring a Japanese-speaking colleague or use an agency that handles
      the landlord conversation.</li>
</ul>

<h2 id="foreigner-friendly">Foreigner-friendly options</h2>
<ul>
  <li><strong>GTN (Global Trust Networks)</strong>, guarantor + bilingual support built for
      foreigners; very widely accepted.</li>
  <li><strong>Leopalace21</strong>, furnished units, often no key money, flexible terms; popular
      for first landings (monthly cost is higher, but upfront is low).</li>
  <li><strong>Sakura House / Oakhouse / Borderless House</strong>, furnished apartments and share
      houses aimed at foreigners, English contracts, low or no deposit.</li>
  <li><strong>Bilingual agencies</strong>, Plaza Homes, Ken Corporation (higher-end / serviced),
      plus foreigner-flagged listings on Suumo/Homes. GaijinPot Apartments and Real Estate Japan
      aggregate English listings.</li>
</ul>

<h2 id="ur">UR Housing, the underused win</h2>
<p><strong>UR Housing (UR都市機構)</strong> is semi-public rental stock with a killer feature set
for foreigners: <strong>no key money, no guarantor, no agency fee, and no renewal fee</strong>. You
deal with UR directly. The catches: you must meet an <strong>income requirement</strong> (commonly
around the monthly rent × 4, or roughly ~¥400,000/month for mid-tier units, with a lump-sum
deposit alternative if your income is lower), units skew older and more suburban, and popular
buildings have waitlists. For a foreigner with a solid salary who doesn't mind a slightly older or
less central building, UR is one of the best-value options in Japan and badly underused.</p>

<h2 id="sharehouse">Share houses & temporary landing</h2>
<p>A <strong>share house</strong> (Oakhouse, Sakura House, Borderless House) is the lowest-friction
way to land: furnished, deposit often ¥30–50K, utilities bundled, English-speaking staff, no
guarantor or key money, and a built-in social circle. Many people stay 1–3 months, open a bank
account and get a phone, then sign a normal lease once they have the paperwork and a feel for
neighbourhoods. If your employer offers <strong>corporate housing</strong> for the first month,
take it, it removes the chicken-and-egg of needing an address to set up everything else.</p>

<h2 id="finding">How to actually find a place</h2>
<ol>
  <li><strong>Suumo, Homes, AtHome</strong>, the big Japanese portals; image-and-rent browsing is
      easy even without much Japanese. Filter for 外国人可, ペット可 (pets), 楽器可 (instruments).</li>
  <li><strong>GaijinPot Apartments, Real Estate Japan, E-Housing</strong>, English portals
      aggregating foreigner-friendly listings.</li>
  <li>Shortlist online, then visit an agency in the target neighbourhood, they'll show several
      units in an afternoon and handle the landlord/guarantor paperwork.</li>
  <li><strong>Decide fast.</strong> Good, well-priced units in Tokyo move within days; agencies
      expect a quick yes after a viewing.</li>
</ol>

<h2 id="viewing">The viewing & application day</h2>
<p>Bring: <strong>Residence Card, passport, proof of income or your job offer letter, your hanko
if you have one, and the ability to pay the move-in total</strong> by transfer once approved.
After you apply, <strong>screening (審査, <em>shinsa</em>)</strong> takes a few days while the
guarantor company and landlord approve you. Things to physically check at the viewing: mobile signal
inside, water pressure, mould in the bathroom, direction the unit faces (south-facing 南向き is
prized for light), noise from rail/road, and whether gas is city gas or propane (propane bills run
higher).</p>

<h2 id="contract">Reading the lease, what to check</h2>
<ul>
  <li><strong>Renewal fee (更新料, kōshinryō)</strong>, many leases charge ~1 month's rent every
      2 years just to renew. Budget for it.</li>
  <li><strong>Move-out cleaning fee</strong>, sometimes fixed in the contract regardless of how
      clean you leave it.</li>
  <li><strong>Cancellation notice</strong>, usually 1 month's written notice; less and you forfeit
      rent.</li>
  <li><strong>Prohibitions</strong>, pets, instruments, extra occupants, subletting. Running an
      Airbnb (民泊) is almost always banned and can void the lease.</li>
  <li><strong>Auto-renewal vs fixed-term (定期借家)</strong>, a <em>teiki shakka</em> contract
      ends on a set date and may not renew; confirm which you're signing.</li>
</ul>

<h2 id="running-costs">Monthly running costs beyond rent</h2>
<p>Budget on top of rent: <strong>management/common-area fee (管理費 / 共益費)</strong> ¥3,000–15,000;
utilities (electric + gas + water) ¥10,000–20,000 for a single, more in summer/winter; internet
¥4,000–6,000; and NHK (public broadcaster) fees if billed. A ¥100,000 "rent" apartment realistically
costs ¥125,000–140,000/month all-in.</p>

<h2 id="leaving">Move-out & getting your deposit back</h2>
<p>Landlords deduct cleaning and "restoration" (原状回復, <em>genjō kaifuku</em>) costs from your
shikikin. The Ministry of Land, Infrastructure, Transport and Tourism guidelines are clear that
<strong>normal wear-and-tear is the landlord's responsibility, not the tenant's</strong>, so you
can and should push back on excessive charges (e.g. full repainting billed to a one-year tenant).
Protect yourself:</p>
<ul>
  <li><strong>Photograph the unit at move-in and move-out</strong>, date-stamped.</li>
  <li>Give <strong>written notice</strong> on time (usually 1 month).</li>
  <li>Ask for an <strong>itemised deduction statement</strong>; dispute line items that are normal
      aging, not damage.</li>
  <li>Expect the deposit balance <strong>1–2 months after</strong> you leave.</li>
</ul>
<div class="callout">Next: <a href="/tools/relocation-budget">Relocation budget calculator</a> ·
<a href="/living/banking">Banking (for rent autopay)</a> ·
<a href="/resources/cost-of-living">Cost of living by ward</a></div>
"""
    },

    # ================================================================= BANKING
    {
        "slug": "banking",
        "icon": "currency-yen",
        "title": "Opening a bank account as a foreigner, which banks actually say yes",
        "summary": "The six-month rule, why Japan Post and Shinsei are the new-arrival wins (and that Sony Bank closed English signups in 2025), cash cards vs the credit gap, rent autopay, and sending money home cheaply with Wise.",
        "updated": "June 2026",
        "read_time": "14 min",
        "key_takeaways": [
            "<strong>Japan Post Bank and SBI Shinsei</strong> are the go-to banks for new arrivals, they open accounts for residents under six months. Shinsei and SMBC Trust PRESTIA have full English support.",
            "<strong>Important 2025 change:</strong> Sony Bank stopped accepting new English-language applications (June 2025). Older guides are out of date, use Shinsei, PRESTIA, Japan Post, or Rakuten.",
            "You generally need a <strong>registered address, Residence Card, and Japanese phone number first</strong>; My Number is increasingly required and needed for international transfers.",
            "Most foreigner-friendly banks <strong>accept a signature instead of a hanko</strong>. A credit card is hard at first (no Japanese credit history), start with Rakuten or Epos.",
            "Send money home cheaply with <strong>Wise</strong> (mid-market rate), not a megabank wire. Once settled, NISA and iDeCo offer tax-advantaged investing.",
        ],
        "faqs": [
            ("Which bank is best for foreigners in Japan?",
             "<p>For new arrivals, <strong>Japan Post Bank (ゆうちょ)</strong> and <strong>SBI Shinsei Bank</strong> are the easiest, they open for residents under six months. For full English service, <strong>Shinsei and SMBC Trust Bank PRESTIA</strong> are best (PRESTIA even lets you apply online/by phone in English). <strong>Rakuten Bank</strong> offers fully online signup. The common strategy is two accounts: Japan Post/Shinsei immediately for daily life, plus whatever megabank your employer prefers for salary.</p>"),
            ("Can I open a Japanese bank account with less than 6 months in Japan?",
             "<p>Yes, at the right bank. Many banks apply an informal <strong>'six-month rule'</strong> treating newer residents as non-residents, but <strong>Japan Post Bank and SBI Shinsei</strong> will open for new arrivals (Shinsei limits you to deposits/withdrawals until month six). Note that <strong>Sony Bank stopped new English-language applications in June 2025</strong>, so don't rely on older advice recommending it.</p>"),
            ("What documents do I need to open a bank account in Japan?",
             "<p>Bring your <strong>Residence Card</strong> (with your address printed on the back, register at the ward office first), a <strong>Japanese phone number</strong>, your <strong>passport</strong>, and increasingly your <strong>My Number</strong> (required for international transfers and investment accounts). A hanko helps but most foreigner-friendly banks accept a signature. Some branches also ask for proof of employment.</p>"),
            ("Do I need a hanko (personal seal) to bank in Japan?",
             "<p>Usually not anymore. <strong>Most foreigner-friendly banks now accept a signature</strong>, Japan Post and Shinsei will open accounts with one. A basic hanko (your name in katakana) is cheap (¥1,000–3,000) and smooths some other bureaucratic moments, so many people get one anyway, but it's no longer a barrier to opening an account.</p>"),
            ("What's the cheapest way to send money from Japan to my home country?",
             "<p>Use a specialist, not a megabank wire (which costs ¥3,000–7,000+ plus a poor exchange rate). <strong>Wise</strong> gives you the mid-market rate with a low fee and is the default for most expats; <strong>Revolut</strong> and SMBC PRESTIA GLOBAL PAY are alternatives. You fund the transfer from your Japanese account, so an English-friendly account helps. International remittance often unlocks only after six months plus My Number.</p>"),
        ],
        "toc": [
            ("why-hard", "Why it's awkward at first"),
            ("six-month", "The unofficial six-month rule"),
            ("best-banks", "Banks that work for foreigners (2026)"),
            ("sony-update", "Important: Sony Bank closed English signups"),
            ("choosing", "Choosing: a two-account strategy"),
            ("what-to-bring", "What to bring"),
            ("hanko", "Do you need a hanko?"),
            ("online-banks", "Online-only banks (Rakuten, au Jibun)"),
            ("salary-account", "Salary account & rent autopay"),
            ("cards", "Cash cards, credit cards & the credit gap"),
            ("ic-pay", "IC cards & QR payment (the cashless layer)"),
            ("sending-money", "Sending money abroad cheaply"),
            ("investing", "Once settled, NISA & iDeCo"),
        ],
        "body": """
<h2 id="why-hard">Why it's awkward at first</h2>
<p>Opening a Japanese bank account isn't hard, but order of operations matters: you generally need
a <strong>registered address (jūminhyō) and Residence Card first</strong>, ideally a Japanese phone
number, and increasingly your My Number. Some megabank branches are also genuinely unhelpful with
non-Japanese speakers. The trick is choosing a bank built for foreigners rather than fighting a
branch that isn't.</p>

<h2 id="six-month">The unofficial six-month rule</h2>
<p>There's no law requiring a minimum stay to open an account, but in practice many banks apply a
<strong>"six-month rule"</strong>, treating residents in Japan under six months as non-residents
for account purposes (limiting features like international remittance). It's an anti-fraud policy,
not a statute, and the banks below are the standard ways around it for new arrivals.</p>

<h2 id="best-banks">Banks that work for foreigners (2026)</h2>
<table>
  <thead><tr><th>Bank</th><th>Why</th><th>English?</th></tr></thead>
  <tbody>
    <tr><td><strong>Japan Post Bank (ゆうちょ)</strong></td>
        <td>Most willing for new arrivals, no minimum-residency demand; branches/ATMs everywhere;
            works from day one with a residence card.</td><td>Limited, but foreigner-tolerant procedures</td></tr>
    <tr><td><strong>SBI Shinsei Bank</strong></td>
        <td>One of the few that opens for residents under 6 months (deposit/withdrawal only until
            month 6); strong English net banking.</td><td>Full English app & site</td></tr>
    <tr><td><strong>SMBC Trust Bank PRESTIA</strong></td>
        <td>Full English support, can apply online or by phone in English; good for those who want
            English service end-to-end.</td><td>Full English</td></tr>
    <tr><td><strong>Rakuten Bank</strong></td>
        <td>Fully online signup, residence card photo + selfie, no branch visit, no minimum
            residency. Great rates, ties into Rakuten ecosystem.</td><td>App mostly Japanese; signup foreigner-friendly</td></tr>
    <tr><td><strong>SMBC / MUFG / Mizuho (megabanks)</strong></td>
        <td>What many employers expect for salary; ATMs everywhere.</td><td>Patchy by branch</td></tr>
  </tbody>
</table>

<h2 id="sony-update">Important: Sony Bank closed English signups</h2>
<div class="warn"><strong>2025 change:</strong> Sony Bank, long a top recommendation for
English-speaking foreigners, <strong>stopped accepting new English-language account applications
as of June 2025</strong>. Existing customers keep their English portal, but new applicants now need
enough Japanese to navigate the standard interface. If an older guide tells you to "just open Sony
Bank," that advice is out of date. Use Shinsei, PRESTIA, Japan Post, or Rakuten instead.</div>

<h2 id="choosing">Choosing: a two-account strategy</h2>
<p>The pragmatic path most settled foreigners land on:</p>
<ol>
  <li><strong>Open Japan Post Bank or Shinsei immediately</strong> on arrival for rent and daily
      life (they tolerate new arrivals).</li>
  <li><strong>Open whatever megabank your employer prefers</strong> for salary once you're settled.</li>
</ol>
<p>Many people keep both: a megabank for payroll, and Shinsei/PRESTIA/Rakuten for English service,
better FX, and online life.</p>

<h2 id="what-to-bring">What to bring</h2>
<ul>
  <li><strong>Residence Card</strong> with your address printed on the back (register at the ward
      office first).</li>
  <li><strong>My Number</strong>, increasingly required, and needed for international transfers and
      investment accounts.</li>
  <li><strong>Japanese phone number</strong>, almost always required on the form.</li>
  <li><strong>Passport</strong> as secondary ID.</li>
  <li><strong>Hanko</strong> if you have one (see below).</li>
  <li>Some branches ask for <strong>proof of employment</strong> or a student ID.</li>
</ul>

<h2 id="hanko">Do you need a hanko?</h2>
<p>A <strong>hanko (印鑑, personal seal)</strong> is traditional for banking and contracts. In
practice, <strong>most foreigner-friendly banks now accept a signature</strong>, Japan Post and
Shinsei will open with one. Still, a basic hanko (your name in katakana) costs ¥1,000–3,000 and
smooths some bureaucratic moments, so many people get one early. Property purchases and a few
official processes occasionally want a <strong>registered seal (実印, jitsuin)</strong> plus a seal
certificate (印鑑証明).</p>

<h2 id="online-banks">Online-only banks (Rakuten, au Jibun, PayPay Bank)</h2>
<p>Online banks offer better interest, slick apps, and, increasingly, foreigner-friendly remote
signup (Rakuten's residence-card-photo-plus-selfie flow is the smoothest). Trade-offs: support is
mostly in Japanese, and a few employers still prefer a "traditional" bank for salary transfer.
They pair well as your second account once your first is running.</p>

<h2 id="salary-account">Salary account & rent autopay</h2>
<p>Your employer pays salary by bank transfer (振込, <em>furikomi</em>) into the account you
nominate. Set up <strong>automatic rent payment (口座振替, <em>kōza furikae</em>)</strong> so rent
is pulled monthly, the landlord or guarantor company provides the form. Utility bills can be
auto-debited the same way, paid at any konbini with the paper slip, or charged to a credit card
once you have one.</p>

<h2 id="cards">Cash cards, credit cards & the credit gap</h2>
<p>You'll get a <strong>cash card (ATM/debit)</strong> immediately; it arrives by mail in ~1–2
weeks. A <strong>credit card is harder at first</strong>, Japan runs its own credit history and
you start with none. Easier early cards: <strong>Rakuten Card</strong>, <strong>Epos</strong>, and
cards tied to your own bank. Approval improves after a few months of salary history. Until then,
debit cards and prepaid IC cards cover daily life.</p>
<div class="callout">Japan is less cash-only than its reputation, but keep some cash on hand, small restaurants, older clinics, and some landlords still don't take cards.</div>

<h2 id="ic-pay">IC cards & QR payment (the cashless layer)</h2>
<p>Get a <strong>Suica or PASMO</strong> immediately (or add Suica to Apple Wallet / a Google
phone). You'll tap it for trains, buses, konbini, vending machines, and many shops. Add
<strong>PayPay</strong> (QR pay, near-universal in cities) once you have a bank account or card to
link. Between an IC card and PayPay, you can go almost cashless day to day.</p>

<h2 id="sending-money">Sending money abroad cheaply</h2>
<p>Megabank international wires are slow and expensive (¥3,000–7,000+ fees plus a poor FX spread).
Use a specialist: <strong>Wise</strong> (mid-market rate, low fee, the default for most expats),
<strong>Revolut</strong>, or a remittance service like <strong>SMBC PRESTIA GLOBAL PAY</strong>.
You'll typically fund a Wise transfer by pulling from your Japanese account, which is another reason
an English-friendly account helps. Note: international remittance features often unlock only after
you pass the six-month mark and provide My Number.</p>

<h2 id="investing">Once settled, NISA & iDeCo</h2>
<p>When you're established and plan to stay, two tax-advantaged accounts are worth knowing:
<strong>NISA</strong> (tax-free investment account, expanded and made permanent in 2024, generous
annual limits, no tax on gains) and <strong>iDeCo</strong> (private defined-contribution pension
with income-tax deductions on contributions). Both are open to foreign residents with a My Number.
They're a major reason long-term foreigners keep building wealth in Japan rather than only remitting
home.</p>
<div class="callout">Next: <a href="/living/ward-office">Get your address & My Number first</a> ·
<a href="/living/phone-utilities">Get a phone number</a> ·
<a href="/tools/take-home-pay">Take-home pay calculator</a></div>
"""
    },

    # ============================================================== WARD OFFICE
    {
        "slug": "ward-office",
        "icon": "document",
        "title": "The ward office & My Number, your first-week bureaucracy, counter by counter",
        "summary": "One visit sets up your residence record, health insurance, pension, and My Number, and there's a ¥200,000 fine for skipping it. Exactly which counters to hit, what to bring, what you walk out with, and the My Number Card worth applying for.",
        "updated": "June 2026",
        "read_time": "13 min",
        "key_takeaways": [
            "One ward-office visit creates your <strong>residence record (jūminhyō)</strong>, enrols you in <strong>health insurance + pension</strong>, and starts your <strong>My Number</strong>, everything else depends on these outputs.",
            "File your move-in within <strong>14 days</strong> or risk a fine up to ¥200,000. Go early on a weekday; large urban offices have foreign-resident desks.",
            "Bring your <strong>Residence Card</strong> (and passport). Ask for <strong>several jūminhyō copies</strong> while you're there, banks and phone shops each want one.",
            "<strong>My Number</strong> is a 12-digit ID for tax and social security; give it to your employer and bank, never to unsolicited callers. The optional <strong>My Number Card</strong> lets you print documents at konbini.",
            "2025–26: the My Number Card and Residence Card functions are being integrated, and the paper health-insurance card is being phased into the My Number Card.",
        ],
        "faqs": [
            ("What do I need to do at the ward office when I arrive in Japan?",
             "<p>File your <strong>move-in notification (転入届)</strong> to register your address, which prints it on the back of your Residence Card. While there: enrol in National Health Insurance and National Pension if you're <em>not</em> on your employer's Shakai Hoken, collect your My Number, and (for families) apply for the Child Allowance and child medical subsidy. Bring your Residence Card and passport, and grab a few jūminhyō copies.</p>"),
            ("What is My Number and who do I give it to?",
             "<p><strong>My Number (マイナンバー)</strong> is a 12-digit individual ID used for tax, social security, and increasingly banking. After you register your address, you receive a notification by mail. <strong>Give it to your employer</strong> for payroll/tax and to your <strong>bank</strong> when asked, but never post it publicly or give it to unsolicited callers. It's sensitive like a tax ID.</p>"),
            ("Should I get a physical My Number Card?",
             "<p>It's optional but worth it. The <strong>My Number Card (マイナンバーカード)</strong> is a photo IC card that serves as official ID, lets you print your jūminhyō and tax documents from any konbini (saving ward-office trips), speeds online government services, and is being merged with the health-insurance function. Apply at the ward office, online, or by mail; it takes a few weeks to be ready.</p>"),
            ("What is a jūminhyō and why do I need copies?",
             "<p>The <strong>jūminhyō (住民票)</strong> is your authoritative proof of address, Japan's version of 'bring a utility bill,' but official. You'll be asked for it repeatedly in your first months (bank, phone, employer), so request several copies (~¥300 each) at the ward office to avoid return trips. Once your My Number Card is active, you can print copies from konbini machines.</p>"),
        ],
        "toc": [
            ("why", "Why this one visit matters"),
            ("deadline", "The 14-day deadline & the fine"),
            ("when", "When & where to go"),
            ("bring", "What to bring"),
            ("counters", "The counters, in order"),
            ("juminhyo", "Residence record (jūminhyō)"),
            ("mynumber", "My Number, what it is"),
            ("mynumber-card", "The My Number Card, apply for it"),
            ("integration", "2025–26: card integration"),
            ("moving-again", "If you move again later"),
            ("leaving-japan", "When you eventually leave"),
            ("after", "After the visit, checklist"),
        ],
        "body": """
<h2 id="why">Why this one visit matters</h2>
<p>Registering your address at the local <strong>city/ward office (市区町村役所,
<em>shikuchōson yakusho</em>)</strong> is the keystone of settling in. This single visit creates
your residence record, enrols you in health insurance and pension, and starts your My Number, and
almost everything else (bank account, phone, credit card, even some deliveries) depends on the
outputs of this visit.</p>

<h2 id="deadline">The 14-day deadline & the fine</h2>
<p>You must file your <strong>move-in notification (転入届, <em>tennyū todoke</em>) within 14
days</strong> of moving into your address. This is enforced: up to <strong>¥200,000</strong> in
penalties under the Immigration Control and Refugee Recognition Act, and up to ¥50,000 under the
Basic Resident Registration Act. Beyond the fine, skipping it stalls your insurance, pension, My
Number, and banking, so it's the first errand to run, not the last.</p>

<h2 id="when">When & where to go</h2>
<p>Go to the office for the municipality where you live, your ward (区役所) in Tokyo's 23 wards,
or your city/town hall (市役所 / 町役場) elsewhere. Typical hours are weekdays 8:30–17:00, usually
closed weekends, though some larger offices open one Saturday morning or weekday evening a month.
Go early; it gets crowded, especially in March–April. Larger urban offices (Shinjuku, Minato,
Shibuya, Yokohama) have foreign-resident desks with English forms or interpreters.</p>

<h2 id="bring">What to bring</h2>
<ul>
  <li><strong>Residence Card</strong> (and passport).</li>
  <li><strong>Moving-out certificate (転出証明書)</strong>, only if moving <em>between</em>
      Japanese municipalities; not needed on first arrival from abroad.</li>
  <li><strong>Proof of address / lease</strong> if asked (often not required, bring it anyway).</li>
  <li><strong>Hanko</strong> if you have one (a signature is usually fine).</li>
  <li>For family: <strong>marriage / birth certificates</strong> (translated) to register dependents.</li>
  <li>A pen, patience, and ~1–2 hours.</li>
</ul>

<h2 id="counters">The counters, in order</h2>
<ol>
  <li><strong>Resident registration (住民登録)</strong>, file the move-in (転入届). They print your
      address on the back of your Residence Card.</li>
  <li><strong>National Health Insurance (国民健康保険)</strong>, enrol here <em>only if you're not
      on your employer's Shakai Hoken</em> (see the health-insurance guide).</li>
  <li><strong>National Pension (国民年金)</strong>, same logic: enrol if not on employer pension.</li>
  <li><strong>My Number desk</strong>, your number is assigned now; the notification follows by
      mail. You can apply for the physical card here or later.</li>
  <li><strong>(Optional) Seal registration (印鑑登録)</strong>, if you need a registered jitsuin.</li>
  <li><strong>(Families) Child Allowance & child medical subsidy</strong>, apply at the relevant
      desk while you're there.</li>
</ol>
<div class="callout">Ask for <strong>several copies of your jūminhyō</strong> (residence
certificate, ~¥300 each) while you're at the counter. Banks, phone shops, and your employer may
each want one, and a second trip across town is a waste of an afternoon.</div>

<h2 id="juminhyo">Residence record (jūminhyō)</h2>
<p>The <strong>jūminhyō (住民票)</strong> is your authoritative proof of address, the document
Japan uses instead of "bring a utility bill." You'll be asked for it repeatedly in your first
months. Once your My Number Card is active you can print copies from konbini multi-copy machines,
which saves return trips.</p>

<h2 id="mynumber">My Number, what it is</h2>
<p><strong>My Number (マイナンバー)</strong> is a 12-digit individual ID used for tax, social
security, and increasingly banking. After you register, you receive a <strong>notification by
mail</strong> of your number within a couple of weeks. Give your My Number to your employer for
payroll/tax and to your bank when asked, but never post it publicly or give it to unsolicited
callers. It's sensitive like a tax ID.</p>

<h2 id="mynumber-card">The My Number Card, apply for it</h2>
<p>The physical <strong>My Number Card (マイナンバーカード)</strong> is optional but worth getting:
a photo IC card that serves as official ID, lets you pull jūminhyō and tax documents from any
konbini, speeds online government services, and is being merged with the health-insurance function
(the "MyNa" health card). Apply at the ward office, online, or by mail; the card takes a few weeks
to be ready for pickup.</p>

<h2 id="integration">2025–26: card integration & the health-card change</h2>
<div class="warn">Two live changes to know: (1) the government is <strong>integrating the My Number
Card and Residence Card</strong> functions for foreign residents through 2025–26 to cut duplicate
paperwork; and (2) the traditional paper <strong>health-insurance card is being phased out in favour
of the My Number Card's health function</strong> ("MyNa" / Eligibility Confirmation Certificates).
If you arrive in this window you may be issued newer document types than older guides describe, follow what your ward office hands you.</div>

<h2 id="moving-again">If you move again later</h2>
<p>Moving within Japan is a two-step dance: file a <strong>move-out notification (転出届, tenshutsu
todoke)</strong> at your old municipality (or online with a My Number Card), get the moving-out
certificate, then file a <strong>move-in (転入届)</strong> at the new one within 14 days. Update your
address with immigration, your bank, employer, and anywhere your Residence Card address matters.</p>

<h2 id="leaving-japan">When you eventually leave</h2>
<p>On permanent departure you file a <strong>move-out notification</strong> too, and critically,
if you'll claim the pension lump-sum refund, <strong>appoint a tax representative (納税管理人) before
you go</strong> (see the pension guide). Settle residence tax, close or notify your bank, and return
your Residence Card at the airport on the way out.</p>

<h2 id="after">After the visit, checklist</h2>
<ul>
  <li>☐ Residence Card now shows your address (back side)</li>
  <li>☐ Enrolled in health insurance + pension</li>
  <li>☐ My Number notification on the way (apply for the card if you want konbini pickup)</li>
  <li>☐ A few jūminhyō copies in hand for bank/phone</li>
  <li>☐ (Families) Child Allowance + child medical subsidy applications filed</li>
</ul>
<div class="callout">Next: <a href="/living/health-insurance">Health insurance</a> ·
<a href="/living/pension">Pension</a> · <a href="/living/banking">Banking</a> ·
<a href="/living/coe-and-arrival">Arrival & the 14-day clock</a></div>
"""
    },

    # =========================================================== HEALTH INSURANCE
    {
        "slug": "health-insurance",
        "icon": "badge",
        "title": "Health insurance in Japan, Shakai Hoken vs National Health Insurance",
        "summary": "Enrolment is mandatory. The 70/30 split, how premiums come out of your salary, the high-cost ceiling that caps a catastrophic month at ~¥80–90k, finding an English-speaking clinic, and covering family for free.",
        "updated": "June 2026",
        "read_time": "13 min",
        "key_takeaways": [
            "Health insurance is <strong>mandatory for all residents</strong> and genuinely good, you pay <strong>30%</strong> of most medical costs, the system pays 70%, and any clinic accepts it.",
            "Employees get <strong>Shakai Hoken</strong> (employer pays ~half, auto-deducted); the self-employed enrol in <strong>National Health Insurance</strong> at the ward office and pay it all.",
            "The <strong>high-cost ceiling (高額療養費)</strong> caps your out-of-pocket at ~¥80–90k/month for an average earner, no matter how large the bill, apply for a limit certificate in advance.",
            "On Shakai Hoken, a non-working <strong>spouse and children are covered free</strong> (below income threshold).",
            "Budget for <strong>year-two residence tax (~10%)</strong>, it's billed on the prior year's income, so it appears in your second year.",
        ],
        "faqs": [
            ("Is health insurance mandatory in Japan for foreigners?",
             "<p>Yes, enrolment is compulsory for all residents, including foreigners on a work visa. If you're a full-time employee, your employer automatically enrols you in <strong>Shakai Hoken</strong> (social insurance) and deducts the premium from your paycheck. If you're self-employed or between jobs, you enrol in <strong>National Health Insurance (NHI)</strong> at the ward office. There's no opting out.</p>"),
            ("How much does healthcare cost in Japan with insurance?",
             "<p>You pay <strong>30% of covered medical costs</strong>; insurance covers 70%. A GP visit typically costs you ¥1,000–3,000 out of pocket, a specialist a bit more, prescriptions also at 30%. Critically, the <strong>high-cost medical ceiling</strong> caps your monthly out-of-pocket at roughly ¥80,000–90,000 for an average earner, so even a major surgery or hospitalisation that 'costs' millions of yen still caps your share around that level.</p>"),
            ("What's the difference between Shakai Hoken and National Health Insurance?",
             "<p><strong>Shakai Hoken (社会保険)</strong> is for company employees, your employer pays about half the premium, it's auto-deducted, and it bundles pension and covers dependents for free. <strong>National Health Insurance (国民健康保険)</strong> is for the self-employed and people between jobs, you enrol at the ward office and pay the full income-based premium yourself, with pension handled separately. Most readers are on Shakai Hoken.</p>"),
            ("Can I find English-speaking doctors in Japan?",
             "<p>Yes. Use the <strong>JNTO multilingual medical directory</strong> and your prefecture's medical info service (Tokyo runs <strong>Himawari</strong>) to find clinics that handle English. Big cities have dedicated international clinics (pricier but fully English), and many ordinary clinics manage basic English with translation apps filling gaps. Save a shortlist for your ward before you need it. Emergency numbers: 119 (ambulance), #7119 (medical advice), #8000 (after-hours paediatric).</p>"),
            ("Does Japanese health insurance cover my family?",
             "<p>On employer Shakai Hoken, your <strong>non-working spouse and children enrol as dependents at no additional premium</strong> (if their income is below the threshold), a real saving versus NHI, where each person is charged. Childbirth is also well supported: a <strong>lump-sum allowance of about ¥500,000</strong> per child, plus prenatal vouchers and often free/cheap paediatric care via municipal subsidies.</p>"),
        ],
        "toc": [
            ("mandatory", "It's mandatory, and genuinely good"),
            ("two-systems", "The two systems"),
            ("cost", "What it costs"),
            ("residence-tax", "The year-two residence-tax surprise"),
            ("coverage", "What's covered (the 70/30 rule)"),
            ("not-covered", "What's not covered"),
            ("high-cost", "The high-cost medical ceiling"),
            ("using-it", "Using it, at the clinic"),
            ("english-clinics", "Finding English-speaking doctors"),
            ("emergencies", "Emergencies & after-hours"),
            ("dependents", "Covering family"),
            ("mychild", "Pregnancy & childbirth support"),
        ],
        "body": """
<h2 id="mandatory">It's mandatory, and genuinely good</h2>
<p>Enrolment in Japan's health system is <strong>compulsory for all residents</strong>, including
foreigners on a work visa. The upside is real: it's excellent and cheap at the point of use. You pay
30% of most medical costs, the system pays 70%, and a monthly ceiling protects you from catastrophic
bills. There's no in-network/out-of-network game, any clinic or hospital accepts it.</p>

<h2 id="two-systems">The two systems</h2>
<table>
  <thead><tr><th></th><th>Shakai Hoken (社会保険)</th><th>National Health Insurance (国民健康保険)</th></tr></thead>
  <tbody>
    <tr><td>Who</td><td>Company employees (most readers)</td><td>Self-employed, freelancers, between jobs</td></tr>
    <tr><td>Enrol via</td><td>Employer (automatic)</td><td>Ward office (you enrol)</td></tr>
    <tr><td>Premium split</td><td><strong>~50% paid by employer</strong></td><td>You pay all of it</td></tr>
    <tr><td>Bundles pension?</td><td>Yes, with Employees' Pension</td><td>No, National Pension is separate</td></tr>
    <tr><td>Dependents</td><td>Covered free if under income threshold</td><td>Each person pays</td></tr>
  </tbody>
</table>
<div class="callout">Normal full-time employee? Your employer enrols you in <strong>Shakai
Hoken</strong> and the premium (plus pension) is deducted from your paycheck automatically, you do
nothing. Only enrol in NHI at the ward office if you're <em>not</em> on an employer plan.</div>

<h2 id="cost">What it costs</h2>
<p>For employees, health insurance + pension + employment insurance together typically run
<strong>~14–16% of gross salary as your half</strong>, with the employer matching much of it.
Health insurance alone is roughly 5% of "standard monthly remuneration," split with the employer.
NHI premiums for the self-employed are income-based, set by municipality, and feel steeper because
there's no employer contribution.</p>

<h2 id="residence-tax">The year-two residence-tax surprise</h2>
<div class="warn"><strong>Budget for this:</strong> residence tax (住民税) is billed in arrears based
on the <em>previous</em> year's income. Your first year in Japan you barely pay it (you had little
or no prior-year Japanese income); in <strong>year two it appears and is roughly 10% of income</strong>,
landing as a noticeable new deduction. Many first-year arrivals are blindsided when their take-home
drops in their second year despite no pay change.</div>

<h2 id="coverage">What's covered (the 70/30 rule)</h2>
<p>You pay <strong>30%</strong> of covered care; insurance covers 70% (the elderly and young
children pay even less). Covered: doctor visits, hospitalisation, surgery, most prescriptions,
dental, mental-health treatment, and maternity care via subsidies. A GP visit often costs you
¥1,000–3,000 out of pocket; a specialist consultation a bit more.</p>

<h2 id="not-covered">What's not covered</h2>
<ul>
  <li>Purely <strong>cosmetic</strong> procedures.</li>
  <li>Some <strong>advanced/elective</strong> or unapproved treatments.</li>
  <li><strong>Normal pregnancy</strong>, not classed as illness, so it's handled by subsidies and
      a lump-sum payment rather than 70/30 (see below).</li>
  <li><strong>Routine health checks beyond the subsidised ones</strong>, and some vaccinations.</li>
</ul>

<h2 id="high-cost">The high-cost medical ceiling</h2>
<p>The <strong>High-Cost Medical Expense system (高額療養費, <em>kōgaku ryōyōhi</em>)</strong> caps
your out-of-pocket spending per calendar month. For an average earner the monthly ceiling is roughly
<strong>¥80,000–¥90,000</strong> regardless of the bill's true size, so a major surgery or
hospitalisation that "costs" millions of yen still caps your share around that level. Apply in
advance for a <strong>limit-applicable certificate (限度額適用認定証)</strong> and the hospital
bills you only up to the ceiling, instead of you paying in full and claiming back.</p>

<h2 id="using-it">Using it, at the clinic</h2>
<ol>
  <li>Bring your <strong>health insurance card</strong> (or My Number Card if linked).</li>
  <li>Pay 30% at the desk on your way out.</li>
  <li>No referral needed for most clinics; large hospitals add a fee (¥7,000+) if you arrive
      without a referral, to discourage using them as walk-in GPs.</li>
  <li>Pharmacies fill prescriptions separately, also at 30%, keep your <strong>medicine notebook
      (お薬手帳, <em>okusuri techō</em>)</strong> for interaction checks.</li>
</ol>

<h2 id="english-clinics">Finding English-speaking doctors</h2>
<p>Use the <strong>JNTO multilingual medical directory</strong> and your prefecture's medical
information service (Tokyo runs <strong>Himawari</strong>) to find clinics that handle English. In
big cities, dedicated international clinics exist (e.g. around central Tokyo and Yokohama), pricier
but fully English. Many ordinary clinics manage basic English, and translation apps cover the rest.
Keep a shortlist for your ward saved before you need it.</p>

<h2 id="emergencies">Emergencies & after-hours</h2>
<ul>
  <li><strong>119</strong>, ambulance and fire (free ambulance; you pay for treatment via the 30%).</li>
  <li><strong>#7119</strong> (where available), emergency medical advice line if you're unsure
      whether to go to hospital.</li>
  <li><strong>#8000</strong>, after-hours paediatric advice.</li>
  <li>Carry your insurance card; ERs still bill through the normal system.</li>
</ul>

<h2 id="dependents">Covering family</h2>
<p>On Shakai Hoken, a non-working spouse and children can be enrolled as <strong>dependents at no
extra premium</strong> if their income is below the threshold, a significant benefit versus NHI,
where each person is charged. Register dependents through your employer and at the ward office.</p>

<h2 id="mychild">Pregnancy & childbirth support</h2>
<p>Childbirth is well supported even though normal delivery isn't billed through 70/30: there's a
<strong>lump-sum childbirth allowance (出産育児一時金) of about ¥500,000</strong> per child, plus
prefectural <strong>prenatal check-up vouchers</strong>. Register your pregnancy at the ward office
to receive a <strong>Mother and Child Handbook (母子手帳, <em>boshi techō</em>)</strong>, often
available in English/bilingual versions, which tracks checkups and vaccinations. Pediatric care for
young children is frequently <strong>free or near-free</strong> via municipal child medical
subsidies (age cutoff varies by municipality).</p>
<div class="callout">Next: <a href="/living/pension">Pension</a> ·
<a href="/living/family">Bringing family</a> · <a href="/tools/take-home-pay">Take-home pay calculator</a></div>
"""
    },

    # ================================================================= PENSION
    {
        "slug": "pension",
        "icon": "chart-line",
        "title": "The pension system & the lump-sum refund most foreigners miss",
        "summary": "Why you pay in, the totalization agreements that protect your home-country contributions, the lump-sum withdrawal you can claim on leaving (and the 60→96-month cap reform), plus the tax-representative trick to reclaim the 20.42% withholding.",
        "updated": "June 2026",
        "read_time": "13 min",
        "key_takeaways": [
            "Pension is <strong>mandatory</strong> (ages 20–59). Employees pay ~9.15% of salary into Employees' Pension, matched by the employer; it's bundled into your social-insurance deduction.",
            "Leaving Japan? You can claim a <strong>Lump-sum Withdrawal Payment</strong> after 6 months of contributions, but you must <strong>apply within 2 years of departure</strong>.",
            "The calculation cap is <strong>60 months (5 years)</strong> today, rising to <strong>96 months (8 years)</strong> under a 2025 reform expected ~2029, so contributing well beyond 5 years currently returns a shrinking fraction.",
            "A <strong>20.42% tax</strong> is withheld from the lump sum, but you can reclaim most of it, <strong>appoint a tax representative (納税管理人) before you leave Japan</strong>.",
            "If you have a <strong>totalization agreement</strong> (US, UK, Germany, Canada, Australia, etc.), your years count toward your home pension, so contributions are rarely truly lost.",
        ],
        "faqs": [
            ("Can I get my pension money back when I leave Japan?",
             "<p>Yes, if you contributed for at least 6 months, you can claim a <strong>Lump-sum Withdrawal Payment (脱退一時金)</strong>, a partial refund of your contributions. You must apply <strong>after you've left Japan and within 2 years of departure</strong>, miss the window and it's gone. The refund is capped at 60 months of contributions for the calculation (rising to 96 months under a 2025 reform, expected ~2029), so long-stayers get proportionally less back.</p>"),
            ("How do I reclaim the tax withheld on my pension refund?",
             "<p>A <strong>20.42% withholding tax</strong> is deducted from Employees' Pension lump sums, but it's largely refundable because you're no longer subject to Japanese income tax once you've left. The key: <strong>appoint a tax representative (納税管理人) before you depart Japan</strong>, a Japanese national or foreign resident with a valid residence card who stays after you go. After you receive the refund notice, send the original to them and they file a tax return to reclaim the tax. Doing this after you've left is much harder, so people routinely forfeit it by not knowing.</p>"),
            ("Do I pay pension in both Japan and my home country?",
             "<p>Not if your country has a <strong>social-security totalization agreement</strong> with Japan (the US, UK, Germany, Canada, Australia, France, South Korea, the Netherlands, and others do). These prevent double-paying and let you <strong>combine contribution periods</strong> across countries toward eligibility. If you're seconded for a few years, an agreement may even let you stay on your home pension and be exempted from the Japanese one, check with your employer and home pension authority.</p>"),
            ("Should I take the pension refund or keep contributing?",
             "<p>If you're leaving Japan for good and contributed under ~5 years, take the lump sum (and reclaim the tax). If you're <strong>staying long-term or pursuing permanent residence, don't take it</strong>, keep contributing. Consistent pension payment is something immigration weighs for PR, and your contributions build toward an actual Japanese pension (now payable after 10 qualifying years). Long-termers also add tax-advantaged NISA and iDeCo.</p>"),
        ],
        "toc": [
            ("mandatory", "Mandatory, like health insurance"),
            ("two-tiers", "The two tiers"),
            ("cost", "What you pay"),
            ("totalization", "Totalization agreements"),
            ("lump-sum", "The lump-sum withdrawal"),
            ("cap-reform", "The 60→96 month cap reform"),
            ("tax-trick", "Reclaiming the 20.42% withholding tax"),
            ("how-to-claim", "How to claim, step by step"),
            ("pr-plan", "If you're staying long-term"),
            ("nisa-ideco", "Building wealth: NISA & iDeCo"),
        ],
        "body": """
<h2 id="mandatory">Mandatory, like health insurance</h2>
<p>Pension enrolment is <strong>compulsory for residents aged 20–59</strong>. Employees are placed
in the <strong>Employees' Pension (厚生年金, <em>kōsei nenkin</em>)</strong> automatically, deducted
from payroll alongside health insurance. Freelancers/contractors pay the flat-rate <strong>National
Pension (国民年金, <em>kokumin nenkin</em>)</strong> via the ward office.</p>

<h2 id="two-tiers">The two tiers</h2>
<table>
  <thead><tr><th></th><th>Employees' Pension</th><th>National Pension</th></tr></thead>
  <tbody>
    <tr><td>Who</td><td>Company employees</td><td>Self-employed, students, unemployed</td></tr>
    <tr><td>Amount</td><td>~9.15% of salary (your half; employer matches)</td><td>Flat ~¥17,000/month</td></tr>
    <tr><td>Future benefit</td><td>Higher, salary-linked</td><td>Base only</td></tr>
  </tbody>
</table>

<h2 id="cost">What you pay</h2>
<p>For employees the pension slice is about <strong>9.15% of standard monthly remuneration</strong>,
with the employer paying a matching ~9.15%. It's bundled into the same payroll deduction as Shakai
Hoken health insurance, which is why "social insurance" is the largest line on your payslip after
income tax.</p>

<h2 id="totalization">Totalization agreements</h2>
<p>Japan has <strong>social-security totalization agreements</strong> with many countries, the
United States, United Kingdom, Germany, Canada, Australia, France, South Korea, the Netherlands, and
more. They do two things: prevent <strong>double-paying pension</strong> in two countries, and let
you <strong>combine contribution periods</strong> across countries toward eligibility. If you're
seconded from home for a few years, an agreement may let you stay on your home pension and be
exempted from the Japanese one, check with your employer and your home pension authority before you
arrive.</p>
<div class="callout">If your country has an agreement, your years in Japan can count toward your home
pension (and vice versa), so contributions are rarely truly "lost," even if you skip the lump sum.</div>

<h2 id="lump-sum">The lump-sum withdrawal</h2>
<p>If you leave Japan permanently after contributing at least <strong>6 months</strong>, you can
claim a <strong>Lump-sum Withdrawal Payment (脱退一時金, <em>dattai ichijikin</em>)</strong>, a
partial refund of contributions. Core rules:</p>
<ul>
  <li>You must <strong>file within 2 years of leaving Japan</strong>, miss it and it's gone.</li>
  <li>You must <strong>apply after departure</strong>, you can't submit while still resident.</li>
  <li>The refund scales with contribution months but is <strong>capped</strong> for the calculation
      (see the reform below), so long-stayers get proportionally less back per year.</li>
  <li>A withholding tax of <strong>20.42%</strong> is deducted from Employees' Pension refunds at
      source, but much of it is reclaimable (see the tax trick).</li>
</ul>

<h2 id="cap-reform">The 60→96 month cap reform</h2>
<div class="warn"><strong>Important and current:</strong> the calculation cap has historically been
<strong>60 months (5 years)</strong> of contributions. Under a pension reform law published in
Japan's Official Gazette on <strong>20 June 2025</strong>, that cap is being <strong>raised to 96
months (8 years)</strong>, aligned with the new Ikusei Shūrō (育成就労) work program. Implementation
is expected around <strong>2029</strong> (exact date by cabinet order). Until it takes effect, the
<strong>5-year cap still applies</strong>, so today, contributing well beyond 5 years means the
lump sum returns a shrinking fraction, which strengthens the case to either stay (and keep the real
pension) or plan your exit around the cap.</div>

<h2 id="tax-trick">Reclaiming the 20.42% withholding tax</h2>
<p>The 20.42% withheld on your lump sum is <strong>largely refundable</strong>, because once you've
left you're no longer subject to Japanese income tax. The mechanism:</p>
<ol>
  <li><strong>Before you leave Japan</strong>, appoint a <strong>tax representative (納税管理人)</strong>, a Japanese national or a foreign resident with a valid residence card who stays in Japan after
      you go. File the appointment at your local tax office.</li>
  <li>After you receive the lump sum, you get a <strong>Lump-sum Withdrawal Payment Notice
      (脱退一時金支給決定通知書)</strong> showing the tax withheld.</li>
  <li>Send the <strong>original notice</strong> to your tax representative, who files a tax return at
      your old local tax office to reclaim the withholding on your behalf.</li>
</ol>
<div class="warn">Sequence is everything: <strong>appoint the representative before you depart.</strong>
Doing it afterward is much harder, and people routinely forfeit this refund simply by not knowing it
exists.</div>

<h2 id="how-to-claim">How to claim, step by step</h2>
<ol>
  <li>While in Japan: keep your <strong>pension number / pension book</strong>, and appoint a tax
      representative if you'll reclaim the tax.</li>
  <li>File your ward-office <strong>move-out</strong> notification on departure.</li>
  <li>After leaving, mail the <strong>Lump-sum Withdrawal claim</strong> to the Japan Pension Service
      with your bank details (a bank that accepts JPY international transfers), passport copy,
      pension number, and proof you've left.</li>
  <li>Receive the lump sum (minus 20.42% if Employees' Pension), then have your representative
      reclaim the tax.</li>
</ol>

<h2 id="pr-plan">If you're staying long-term</h2>
<p>Planning to pursue permanent residence? <strong>Don't take the lump sum</strong>, keep
contributing. Consistent pension and tax payment is something immigration weighs for PR, and your
contributions build toward an actual Japanese pension (payable after the required contribution years,
now reduced to 10 years to qualify). Many long-termers also layer in private retirement saving below.</p>

<h2 id="nisa-ideco">Building wealth: NISA & iDeCo</h2>
<p>Two tax-advantaged accounts that make staying financially attractive:</p>
<ul>
  <li><strong>NISA</strong>, tax-free investment account, expanded and made permanent in 2024 with
      generous annual limits and no tax on gains. Open to foreign residents with a My Number.</li>
  <li><strong>iDeCo</strong>, private defined-contribution pension; contributions are
      income-tax-deductible, growth is tax-deferred. Locks until 60, so it's genuinely for retirement.</li>
</ul>
<div class="callout">Next: <a href="/living/health-insurance">Health insurance</a> ·
<a href="/resources/visa-types">Path to permanent residence</a> ·
<a href="/tools/take-home-pay">See pension on your payslip</a></div>
"""
    },

    # ============================================================ PHONE/UTILITIES
    {
        "slug": "phone-utilities",
        "icon": "globe",
        "title": "Phone, internet & utilities, getting connected without a credit history",
        "summary": "Why your phone number is the master key, the cheap-SIM route that skips contracts, the foreigner-friendly carriers that set up before you have a bank account, fibre vs pocket WiFi, getting gas turned on, and the cashless layer.",
        "updated": "June 2026",
        "read_time": "12 min",
        "key_takeaways": [
            "A <strong>Japanese phone number is the master key</strong>, banks, apartments, and utilities all want one. Get it in your first few days.",
            "<strong>Sakura Mobile and Mobal</strong> are foreigner-friendly SIMs that set up before you have a Japanese bank account (they take foreign cards), the fix for the chicken-and-egg problem. Switch to a cheaper MVNO later.",
            "<strong>Electricity is deregulated</strong> (pick a cheaper provider, activates same/next day), but <strong>gas needs a technician appointment</strong>, book it before move-in or no hot water night one.",
            "Home fibre takes <strong>2–4 weeks</strong> to install, bridge with pocket WiFi. Many share houses include internet.",
            "Set up <strong>Suica/PASMO + PayPay</strong> to go nearly cashless; pay utilities by bank auto-debit (口座振替).",
        ],
        "faqs": [
            ("How do I get a phone number in Japan as a new arrival?",
             "<p>Use a <strong>foreigner-friendly SIM, Sakura Mobile or Mobal</strong>. They offer English support and signup, accept foreign credit cards (so you don't need a Japanese bank account yet), and can arrange a SIM for airport pickup or delivery to your first address. This solves the chicken-and-egg problem where a bank wants a phone but a normal carrier wants a bank. Once you have a bank account, you can port your number to a cheaper domestic MVNO.</p>"),
            ("Can I set up a phone before I have a Japanese bank account?",
             "<p>Yes, that's exactly what <strong>Sakura Mobile and Mobal</strong> are for. They accept foreign payment cards, so you can get connected in week one before your bank account is open. For the literal first hours after landing, a travel eSIM (Airalo, Ubigi) gives you data immediately for maps and translation, just make sure your phone is carrier-unlocked before you fly.</p>"),
            ("How do I turn on electricity, gas, and water in a Japanese apartment?",
             "<p><strong>Electricity</strong> is deregulated, pick a provider (cheaper options like Looop or ENEOS Denki beat the regional default) and it activates same/next day via web form. <strong>Gas requires a technician visit</strong> to turn it on and check appliances, so you must be home, book it before move-in day. <strong>Water</strong> is run by the municipality; submit the move-in card or call. Pay all of them by bank auto-debit (口座振替) or at any konbini.</p>"),
            ("How long does home internet take to set up in Japan?",
             "<p>Fixed fibre (光, hikari) is fast and cheap (~¥4,000–6,000/month) but <strong>installation takes 2–4 weeks</strong> and may need landlord permission to run the line. Bridge the gap with a <strong>pocket WiFi or home router (WiMAX, Rakuten)</strong> usable from day one. Many apartments and most share houses already include internet, check before arranging your own.</p>"),
        ],
        "toc": [
            ("phone-first", "Get a phone number first"),
            ("carriers", "Carriers vs cheap SIMs"),
            ("foreigner-sims", "Foreigner-friendly SIMs (the week-one fix)"),
            ("esim", "eSIM & arrival connectivity"),
            ("internet", "Home internet, fibre vs pocket WiFi"),
            ("electricity", "Electricity (deregulated, choose cheap)"),
            ("gas", "Gas, the appointment you must book"),
            ("water", "Water & the move-in card"),
            ("paying-bills", "Paying bills (auto-debit, konbini)"),
            ("nhk", "The NHK question"),
            ("ic-cards", "Suica/PASMO & QR pay"),
            ("order", "The smart setup order"),
        ],
        "body": """
<h2 id="phone-first">Get a phone number first</h2>
<p>A <strong>Japanese mobile number is the master key</strong> to everything else, bank accounts,
apartment applications, utility signups, delivery slips, and most app registrations want one.
Prioritise it in your first few days. You'll generally need your <strong>Residence Card</strong> and
often a <strong>Japanese payment method</strong>, which creates a chicken-and-egg with the bank
account. The fix is a foreigner-friendly SIM that accepts a foreign card (below).</p>

<h2 id="carriers">Carriers vs cheap SIMs</h2>
<table>
  <thead><tr><th>Option</th><th>Cost/mo</th><th>Best for</th></tr></thead>
  <tbody>
    <tr><td>Big 3 (docomo, au, SoftBank)</td><td>¥5,000–9,000</td><td>Max coverage, phone financing, family plans</td></tr>
    <tr><td>Sub-brands (ahamo, povo, LINEMO)</td><td>¥2,000–3,000</td><td>Same networks, online-only, simpler</td></tr>
    <tr><td><strong>MVNO / cheap SIM</strong> (IIJmio, mineo, Rakuten Mobile)</td><td>¥1,000–3,000</td><td>Domestic value once you have a bank account</td></tr>
    <tr><td><strong>Foreigner MVNOs</strong> (Sakura Mobile, Mobal)</td><td>¥2,000–4,000</td><td><strong>Week one</strong>, English support, no Japanese bank needed</td></tr>
  </tbody>
</table>

<h2 id="foreigner-sims">Foreigner-friendly SIMs (the week-one fix)</h2>
<p><strong>Sakura Mobile</strong> and <strong>Mobal</strong> specialise in foreigners: English
support and signup, they accept foreign credit cards (so you don't need a Japanese bank yet), and
they can arrange a SIM for <strong>airport pickup or delivery to your first address</strong>.
Slightly pricier than a domestic MVNO, but they dissolve the chicken-and-egg problem. Once you have
a bank account, you can port your number (MNP) to a cheaper domestic MVNO if you want to cut cost.</p>

<h2 id="esim">eSIM & arrival connectivity</h2>
<p>For the literal first hours, a travel <strong>eSIM</strong> (Airalo, Ubigi, or a Sakura/Mobal
eSIM) gives you data from the moment you land, before you've sorted a real plan. Handy for maps,
translation, and calling your share house/landlord on day one. Make sure your phone is
<strong>carrier-unlocked</strong> before you fly.</p>

<h2 id="internet">Home internet, fibre vs pocket WiFi</h2>
<p>Fixed fibre (光, <em>hikari</em>) is fast and cheap (~¥4,000–6,000/month) but
<strong>installation can take 2–4 weeks</strong> and sometimes needs landlord permission to run the
line. Bridge the gap with a <strong>pocket WiFi or home router (WiMAX, Rakuten)</strong> usable from
day one. Many apartments and most share houses include internet, check before arranging your own,
and check whether the building is already wired for a specific provider (it speeds installation).</p>

<h2 id="electricity">Electricity (deregulated, choose cheap)</h2>
<p>The electricity market is deregulated: you can pick a provider rather than defaulting to the
regional monopoly. Beyond TEPCO/Kansai Electric etc., cheaper alternatives like <strong>Looop,
ENEOS Denki, and au Denki</strong> often cut bills. Activation is usually same/next day via a web
form or phone call, there's a breaker you flip in the new apartment to start service.</p>

<h2 id="gas">Gas, the appointment you must book</h2>
<div class="warn"><strong>Gas is the one utility that needs a person.</strong> A technician must
visit to turn it on and verify your appliances/safety, you (or someone) must be home. Book it
<em>before</em> move-in day or you'll have no hot water your first night. Note whether the unit is
<strong>city gas (都市ガス)</strong>, cheaper, or <strong>propane / LP gas (プロパン)</strong>,
which can cost noticeably more month to month (worth asking before you sign a lease).</p>

<h2 id="water">Water & the move-in card</h2>
<p>Water is run by the municipality. Usually you just submit the move-in postcard left in the
apartment or call the local water bureau; service is rarely an issue and often already on. Billing
is typically every two months.</p>

<h2 id="paying-bills">Paying bills (auto-debit, konbini, card)</h2>
<p>Three ways: <strong>auto-debit from your bank (口座振替)</strong>, set-and-forget; <strong>konbini
payment</strong>, take the paper slip to any convenience store; or <strong>credit-card autopay</strong>
once you have a card. Auto-debit is the least effort once your bank account is live.</p>

<h2 id="nhk">The NHK question</h2>
<p>A collector for <strong>NHK</strong> (public broadcaster) may knock asking you to pay the
receiving fee if you have a TV-capable device. The legal situation is nuanced and much-debated among
foreigners; many people handle it by simply not owning a TV/tuner. Know that the knock will come and
decide your approach; you're not obliged to sign anything on the spot.</p>

<h2 id="ic-cards">Suica/PASMO & QR pay</h2>
<p>Get a <strong>Suica or PASMO</strong> immediately (or add Suica to Apple Wallet / a Google
phone). Tap it for trains, buses, konbini, vending machines, and many shops; top up with cash at any
station machine or auto-charge from a linked card. Add <strong>PayPay</strong> (QR pay) once you have
a bank account or card, between the two you can go nearly cashless.</p>

<h2 id="order">The smart setup order</h2>
<ol>
  <li>Land → travel eSIM for instant data; keep Residence Card on you.</li>
  <li>Ward office → address registered (jūminhyō, My Number).</li>
  <li><strong>Phone</strong> via a foreigner-friendly SIM (Sakura/Mobal), works before a bank account.</li>
  <li>Bank account (now you have address + phone).</li>
  <li>Utilities to auto-debit; book the gas appointment; order fibre (bridge with pocket WiFi).</li>
  <li>Add Suica + PayPay; optionally port to a cheaper MVNO later.</li>
</ol>
<div class="callout">Next: <a href="/living/banking">Banking</a> ·
<a href="/living/ward-office">Ward office & My Number</a> ·
<a href="/living/housing">Housing (internet & gas at move-in)</a></div>
"""
    },

    # ================================================================== FAMILY
    {
        "slug": "family",
        "icon": "users",
        "title": "Bringing your family, dependent visas, schools, and spouse work rights",
        "summary": "How the Dependent visa works, the 28-hour spouse work limit and how to lift it, free 3–5 childcare and Tokyo's new free 0–2 daycare, the hoikuen waitlist, local vs international schools (¥1.5–3M/yr), and the allowances foreigners can claim.",
        "updated": "June 2026",
        "read_time": "15 min",
        "key_takeaways": [
            "Your <strong>legally married spouse and minor children</strong> join on a <strong>Dependent visa (家族滞在)</strong> you sponsor, you file a COE for each, proving you can support them.",
            "A dependent spouse can work only <strong>28 hours/week</strong> (with a free permit). For a full career, they switch to their own work visa once they find a qualifying job.",
            "<strong>HSP visa holders get family superpowers</strong>: full spouse work rights, and the ability to bring a parent (to help with a young child) and domestic help.",
            "Childcare is heavily subsidised: <strong>free for ages 3–5 nationwide</strong>, and <strong>free for a first child 0–2 in Tokyo</strong> (from Sept 2025), but popular wards have waitlists, so research before choosing where to live.",
            "International school runs <strong>¥1.5–3M+/year</strong>; local public school is effectively free and younger kids come out bilingual. Childbirth brings a ~¥500k lump sum.",
        ],
        "faqs": [
            ("Can I bring my family with me to Japan on a work visa?",
             "<p>Yes, your <strong>legally married spouse and minor children</strong> can join you on a <strong>Dependent visa (家族滞在)</strong>, which you sponsor as the primary work-visa holder. You file a Certificate of Eligibility for each dependent (same process as your own), showing your relationship with translated marriage/birth certificates and that your income clearly covers the family. Many people move first, set up housing and banking, then bring the family 1–3 months later.</p>"),
            ("Can my spouse work in Japan on a dependent visa?",
             "<p>Only part-time by default. A Dependent-visa holder can apply, free, at immigration, for permission to work up to <strong>28 hours per week</strong>. To work full-time, your spouse needs their own status of residence: they find a qualifying professional job and the employer sponsors a change from Dependent to a work visa. If you hold the <strong>HSP visa</strong>, your spouse gets enhanced full work rights without needing their own independent qualifying visa.</p>"),
            ("Is childcare free in Japan for foreigners?",
             "<p>Substantially, yes, with a residence card and ward registration. Early childhood education is <strong>free for ages 3–5 nationwide</strong> regardless of income (you pay only meals/materials). In <strong>Tokyo, from September 2025, licensed daycare is free for a first child aged 0–2</strong> for all families; elsewhere under-3 fees are income-scaled. The catch is availability, popular urban wards have waitlists (待機児童), and dual-income households score higher for placement.</p>"),
            ("Should my kids go to local or international school in Japan?",
             "<p>It depends on age and how long you'll stay. <strong>Local public school</strong> is effectively free, immerses kids in Japanese, and younger children adapt fast and come out bilingual, best for long-term stayers. <strong>International school</strong> (¥1.5–3M+/year) keeps an English or IB curriculum, suiting teenagers mid-curriculum and shorter stays. International fees are a major budget line, so factor them into salary negotiation, some employers offer school-fee assistance for senior hires.</p>"),
            ("What child allowances can foreigners claim in Japan?",
             "<p>Any foreign resident with a residence card and ward registration can claim them. The main ones: the monthly <strong>Child Allowance (児童手当)</strong> (the 2024 reform removed income caps and extended payments for many families); a <strong>child medical subsidy</strong> for free/cheap paediatric care; free preschool (3–5) and public schooling; <strong>prenatal vouchers</strong>; and a <strong>~¥500,000 childbirth lump sum</strong> per child. Apply at the ward office.</p>"),
        ],
        "toc": [
            ("dependent-visa", "The Dependent visa"),
            ("who-qualifies", "Who qualifies & proving support"),
            ("timing", "Bring them together or after?"),
            ("spouse-work", "Can your spouse work? (the 28-hour rule)"),
            ("spouse-career", "Lifting the limit, a real career"),
            ("hsp-family", "HSP family superpowers"),
            ("healthcare", "Family healthcare"),
            ("childbirth", "Pregnancy & childbirth support"),
            ("childcare", "Daycare (hoikuen) & the waitlist"),
            ("free-childcare", "Free childcare, 3–5 nationwide, 0–2 in Tokyo"),
            ("schools", "Schools, local vs international"),
            ("allowances", "Child allowances & subsidies"),
        ],
        "body": """
<h2 id="dependent-visa">The Dependent visa</h2>
<p>Your spouse and children can join you on a <strong>Dependent visa (家族滞在,
<em>kazoku taizai</em>)</strong>, sponsored by you as the primary work-visa holder. You file a COE
for each dependent (same process as your own, see the COE guide), showing the relationship
(marriage and birth certificates, translated) and that you can financially support them. Dependents'
period of stay is tied to yours.</p>
<div class="callout">"Dependent" is specifically the <em>Family Stay</em> status for a
work-visa-holder's spouse and minor children. It's different from the "Spouse of Japanese National"
visa (for those married to a Japanese citizen), which carries full work rights.</div>

<h2 id="who-qualifies">Who qualifies & proving support</h2>
<p>Only your <strong>legally married spouse and minor children</strong> qualify (not parents,
siblings, or unmarried partners, except under HSP, below). There's no fixed income threshold, but
immigration wants to see your earnings clearly cover the family: expect to provide
<strong>salary slips, a tax certificate, and bank statements</strong>. A common rule of thumb is
that supporting a spouse comfortably wants a salary meaningfully above the single-person minimum;
more dependents, higher expectation.</p>

<h2 id="timing">Bring them together or after?</h2>
<ul>
  <li><strong>Together:</strong> file all COEs at once. Cleaner paperwork, but slower to your start
      date and you arrive juggling housing + bureaucracy for everyone simultaneously.</li>
  <li><strong>You first, family follows (most common with kids):</strong> you land, secure a
      family-sized apartment, set up bank/phone/ward registration, then bring the family 1–3 months
      later into a working household. Far less stressful than building everything from a hotel with
      jet-lagged children.</li>
</ul>

<h2 id="spouse-work">Can your spouse work? (the 28-hour rule)</h2>
<p>A Dependent-visa holder <strong>cannot work by default</strong>, but can apply, free, at
immigration, for <strong>"Permission to Engage in Activity Other Than That Permitted
(資格外活動許可)"</strong>, which allows up to <strong>28 hours per week</strong>. That covers
part-time work but not a full-time career.</p>

<h2 id="spouse-career">Lifting the limit, a real career</h2>
<p>To work full-time, the spouse needs their own status of residence. The usual route: the spouse
finds a qualifying professional job and the employer sponsors a <strong>change of status from
Dependent to a work visa</strong> (e.g. Engineer/Specialist). At that point they're no longer your
dependent, they're a primary visa holder in their own right, with full work rights and their own
path to PR. Many dual-career couples plan this from the start.</p>

<h2 id="hsp-family">HSP family superpowers</h2>
<p>If you qualify for the <strong>Highly Skilled Professional (HSP)</strong> visa, the family
benefits are unusually generous and can justify pursuing HSP on their own:</p>
<ul>
  <li>Your <strong>spouse can work full-time</strong> in skilled work without needing their own
      independent qualifying visa (the "spouse of HSP" allowance).</li>
  <li>You may bring a <strong>parent</strong> under conditions (typically to help raise a child
      under 7, or a pregnant spouse), almost unique among Japanese visas.</li>
  <li>You may bring <strong>domestic help</strong> under conditions.</li>
</ul>
<p>See the <a href="/resources/visa-types">visa categories guide</a> for HSP point scoring.</p>

<h2 id="healthcare">Family healthcare</h2>
<p>On employer Shakai Hoken, a non-working spouse and children enrol as <strong>dependents at no
additional premium</strong> (below the income threshold), a real saving versus NHI's per-person
charge. Register them through your employer and at the ward office.</p>

<h2 id="childbirth">Pregnancy & childbirth support</h2>
<p>A <strong>childbirth lump-sum (出産育児一時金) of ~¥500,000</strong> per child offsets delivery
(normal birth isn't billed through 70/30), plus prefectural prenatal check-up vouchers. Register the
pregnancy at the ward office for a <strong>Mother & Child Handbook (母子手帳)</strong>, often
available bilingually. As of April 2025, maternity/paternity leave provisions were further
strengthened, check your employer's policy, which often tops up the statutory benefit.</p>

<h2 id="childcare">Daycare (hoikuen) & the waitlist</h2>
<p>Licensed daycare (<strong>認可保育園, <em>ninka hoikuen</em></strong>) is high quality and heavily
subsidised, but demand outstrips supply in popular urban wards, the famous <strong>waitlist
(待機児童, <em>taiki jidō</em>)</strong>. Placement is points-based: <strong>dual-income households
score higher</strong>, and you apply through your ward office, ideally before you even arrive if you
can. Alternatives when you can't get a licensed spot: unlicensed (認可外) daycare, employer-sponsored
childcare, and international preschools.</p>
<div class="warn">If both parents must work from arrival, treat daycare availability as a constraint
on <em>which ward you live in</em>, it varies enormously between and even within wards. Research it
before signing a lease.</div>

<h2 id="free-childcare">Free childcare, 3–5 nationwide, 0–2 in Tokyo</h2>
<p>Two big subsidies for foreign families (residence card + ward registration required):</p>
<ul>
  <li><strong>Nationwide:</strong> early childhood education is <strong>free for ages 3–5</strong> at
      licensed centres and kindergartens, regardless of income, you pay only meals/materials
      (~¥3,000–10,000/month).</li>
  <li><strong>Tokyo (from September 2025):</strong> licensed daycare is <strong>free for a first
      child aged 0–2</strong> for all families, a major expansion. Outside Tokyo, under-3 fees are
      income-scaled (¥0 up to ~¥77,500/month).</li>
</ul>

<h2 id="schools">Schools, local vs international</h2>
<table>
  <thead><tr><th></th><th>Local public school</th><th>International school</th></tr></thead>
  <tbody>
    <tr><td>Cost</td><td>Effectively free (small fees, lunch)</td><td><strong>¥1.5–3M+ per year</strong></td></tr>
    <tr><td>Language</td><td>Japanese immersion</td><td>English (or IB/home curriculum)</td></tr>
    <tr><td>Best for</td><td>Younger kids; long-term stayers; integration & bilingualism</td><td>Older kids; shorter stays; continuity & university pathways</td></tr>
    <tr><td>Trade-off</td><td>Sink-or-swim language at first; PTA in Japanese</td><td>Cost; long waitlists at top schools; less local integration</td></tr>
  </tbody>
</table>
<p>Younger children adapt to local schools remarkably fast and come out bilingual; teenagers
mid-curriculum usually do better in an international school for continuity. International fees are a
major budget line, <strong>factor them into your salary negotiation</strong> if relocating a family,
as some employers offer school-fee assistance for senior hires.</p>

<h2 id="allowances">Child allowances & subsidies</h2>
<ul>
  <li><strong>Child Allowance (児童手当)</strong>, monthly payment per child; the 2024 reform
      removed income caps and extended payments through high school for many families. Apply at the
      ward office.</li>
  <li><strong>Child medical subsidy</strong>, free/cheap paediatric care; age cutoff varies by
      municipality (some cover through junior high or high school).</li>
  <li><strong>Free preschool (3–5)</strong> nationwide, plus free public schooling.</li>
  <li><strong>Prenatal vouchers</strong> and the <strong>~¥500K childbirth lump sum</strong>.</li>
</ul>
<div class="callout">Next: <a href="/resources/visa-types">Visa categories (HSP family benefits)</a> ·
<a href="/living/health-insurance">Health insurance (dependents)</a> ·
<a href="/living/ward-office">Ward office (register dependents & allowances)</a></div>
"""
    },
]


def get_living_guide(slug: str):
    return next((g for g in LIVING_GUIDES if g["slug"] == slug), None)
