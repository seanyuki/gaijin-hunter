# Deep-research enrichments for the 8 resources pages.
# Each entry is a dict with:
#   - 'toc_additions': list of (slug, label) tuples to append to existing TOC
#   - 'body_addition': HTML string to append to existing body just before the closing triple-quote
# Marker: "<!-- ENRICH_V2:{slug} -->" appears at the top of each addition so splices are idempotent.

RESOURCE_ENRICHMENTS = {

    # ============================================================ visa-types
    "visa-types": {
        "toc_additions": [
            ("apr-2026-update", "April 2026 — Engineer/Specialist language requirement"),
            ("oct-2025-bizmgr", "October 2025 — Business Manager visa reform"),
            ("jesta", "JESTA — Japan's new ESTA-style pre-screening"),
            ("changing-status", "Changing status — practical timelines"),
            ("dependents", "Dependent visas — spouse and child"),
        ],
        "body_addition": """
<!-- ENRICH_V2:visa-types -->
<h2 id="apr-2026-update">April 2026 — Engineer/Specialist language requirement</h2>
<p>Effective April 15, 2026, Japan's most common foreign-worker visa — Engineer /
Specialist in Humanities / International Services — added a Japanese-language
requirement for applicants whose roles involve substantive Japanese-language
interaction. The Immigration Services Agency now categorises sponsoring employers
into four tiers based on size, tax history, and prior compliance. For Category 3 and
Category 4 employers (generally smaller or newer companies), applicants in roles
requiring Japanese interpersonal work must now submit proof of Japanese ability at
roughly CEFR B2 / JLPT N2 level.</p>
<p>Category 1 and 2 employers — most large Japanese corporations, established
foreign-cap firms, and listed companies — are largely exempt from the documentation
upgrade. The practical impact:</p>
<ul>
  <li><strong>Mercari, Indeed, PayPay, Rakuten, FAANG Tokyo:</strong> no change. Visa
      processing under prior norms.</li>
  <li><strong>Series-A/B Japanese startups, smaller foreign-cap entrants:</strong>
      expect to provide JLPT N2 certification or equivalent during application if the
      role description mentions client / stakeholder interaction in Japanese.</li>
  <li><strong>Pure-English roles</strong> at any size of employer remain unaffected —
      software engineering, research, and other roles that don't require Japanese
      interpersonal work are exempt.</li>
</ul>

<h2 id="oct-2025-bizmgr">October 2025 — Business Manager visa reform</h2>
<p>The Business Manager (経営・管理) visa underwent its largest tightening in years
in October 2025:</p>
<ul>
  <li><strong>Minimum capital raised from ¥5M to ¥30M</strong> — a 6× increase. The
      new threshold aligns Japan with established global norms and was driven by
      concerns about shell-company visas.</li>
  <li><strong>One full-time Japanese-rooted employee required</strong> — either a
      Japanese national, permanent resident, spouse-of-Japanese, or long-term resident.
      The previous standard allowed any nationality.</li>
  <li><strong>JLPT N2 requirement</strong> — at least one person (the applicant or
      the required local employee) must hold JLPT N2 or higher.</li>
  <li><strong>Substantive office space</strong> — virtual offices no longer count;
      Immigration now expects a verifiable physical office with signage and
      operational hours.</li>
</ul>
<p>If you were considering Japan's Business Manager visa to set up a one-person
freelance company, that path is effectively closed unless you can raise ¥30M and
hire a qualifying local employee. Most foreigners who chose Business Manager
historically (consultants, e-commerce sellers, small shop owners) should now
investigate either the Highly Skilled Professional visa or a regular employed
Engineer/Specialist sponsorship instead.</p>

<h2 id="jesta">JESTA — Japan's new ESTA-style pre-screening</h2>
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

<h2 id="changing-status">Changing status — practical timelines</h2>
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

<h2 id="dependents">Dependent visas — spouse and child</h2>
<p>If you bring family on a Dependent visa, expect these realities:</p>
<ul>
  <li><strong>Spouse working rules.</strong> Dependents may work up to 28 hours/week
      with prior "permission for activities other than that permitted" (資格外活動許可)
      from Immigration. Full-time work requires the spouse to change to their own
      Status of Residence (Engineer, etc.) — there's no automatic carry-over.</li>
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

    # ============================================================ jlpt-levels
    "jlpt-levels": {
        "toc_additions": [
            ("salary-impact", "Salary impact by JLPT level — real numbers"),
            ("jft-basic", "JFT-Basic vs JLPT — what employers actually accept"),
            ("alternatives", "BJT, J.TEST, and other employer-recognised tests"),
            ("study-timelines", "Realistic study timelines from N5 to N1"),
            ("how-to-prep", "How working professionals actually pass each level"),
        ],
        "body_addition": """
<!-- ENRICH_V2:jlpt-levels -->
<h2 id="salary-impact">Salary impact by JLPT level — real numbers</h2>
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

<h2 id="jft-basic">JFT-Basic vs JLPT — what employers actually accept</h2>
<p>JFT-Basic (Japan Foundation Test for Basic Japanese) is the newer, faster
alternative to JLPT — but it's not a JLPT replacement at the levels relevant to
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
  <li><strong>BJT (Business Japanese Proficiency Test)</strong> — 8 levels, focused on
      business situations. Companies like Tokio Marine, Tokyo Gas, and large
      sōgō shōsha specifically value BJT J2/J1. HSP points: BJT 480+ = 10 pts,
      BJT 400-479 = 15 pts.</li>
  <li><strong>J.TEST</strong> — practical 6-level test popular among SE Asian
      candidates. Widely accepted in Japan for SSW and Engineer/Specialist purposes.</li>
  <li><strong>NAT-TEST</strong> — administered monthly, parallels JLPT levels.
      Less prestigious than JLPT but useful for interim certification.</li>
  <li><strong>Kanji Kentei (漢検)</strong> — Japanese-language kanji test; only
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
materially — speaking, listening, and contextual vocabulary build faster than book
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
  <li><strong>Mock tests in the final 2 months</strong> — Shin Kanzen Master and Sou
      Matome series are the gold-standard prep books for each level.</li>
  <li><strong>Take the test even if you fail.</strong> The fail-and-retake cycle
      gives you exam pacing, which is half the test.</li>
</ul>
""",
    },

    # ============================================================ japanese-resume-formats
    "japanese-resume-formats": {
        "toc_additions": [
            ("digital-submission", "Digital submission — PDF, photo files, naming"),
            ("photo-rules", "Photo rules — 2025 specifics"),
            ("photo-skip", "When you can skip the photo"),
            ("english-vs-japanese", "English CV vs. rirekisho — when to send which"),
            ("ats-considerations", "ATS / applicant tracking systems in Japan"),
            ("common-mistakes", "10 common rirekisho mistakes foreigners make"),
        ],
        "body_addition": """
<!-- ENRICH_V2:japanese-resume-formats -->
<h2 id="digital-submission">Digital submission — PDF, photo files, naming</h2>
<p>In 2025–26, the majority of Japanese employers — even traditional Japanese
corporates — accept rirekisho and shokumu keirekisho as PDF email attachments or
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
      rirekisho PDF itself — don't send it as a separate attachment unless the company
      explicitly requests it.</li>
</ul>

<h2 id="photo-rules">Photo rules — 2025 specifics</h2>
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
      lighting allows — usable for digital submission but not for printed
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

<h2 id="english-vs-japanese">English CV vs. rirekisho — when to send which</h2>
<table>
  <thead><tr><th>Situation</th><th>What to send</th></tr></thead>
  <tbody>
    <tr><td>FAANG Tokyo, Stripe, Notion, foreign-cap SaaS</td>
        <td>English CV only</td></tr>
    <tr><td>Mercari, SmartNews, PayPay (English career page)</td>
        <td>English CV; shokumu keirekisho if requested in JP</td></tr>
    <tr><td>Rakuten, Cyberagent, LINE Yahoo</td>
        <td>Both — rirekisho + shokumu keirekisho + English CV</td></tr>
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
  <li><strong>Greenhouse / Lever / Workday</strong> — used by most foreign-cap firms.
      Standard CV upload; usually skip rirekisho.</li>
  <li><strong>HRMOS</strong> (BizReach) — Japan's largest enterprise ATS.
      Custom-formatted application forms; sometimes accept PDF rirekisho upload.</li>
  <li><strong>SmartHR / SmartHR Recruiting</strong> — used by Series-A/B startups.
      Generally accepts PDF rirekisho.</li>
  <li><strong>Yappli HR / Talentio</strong> — Japan-specific. Sometimes asks for
      structured form-fill in addition to PDF upload.</li>
  <li><strong>Wantedly</strong> — feed-style profile; the platform substitutes for
      rirekisho if you fill out the profile completely. Used heavily by Tokyo
      startups.</li>
  <li><strong>LinkedIn Easy Apply</strong> — direct CV upload; commonly used by
      Indeed Tokyo, foreign-cap Tokyo offices, and a growing number of Japanese
      employers.</li>
</ul>

<h2 id="common-mistakes">10 common rirekisho mistakes foreigners make</h2>
<ol>
  <li>Writing the date as the application <em>submission</em> date instead of the day
      you'll mail/email it.</li>
  <li>Using the wrong era — recent rirekisho can use either Western (2026) or
      Reiwa era (令和8); pick one and use it consistently throughout.</li>
  <li>Leaving "Reasons for resignation" (退職理由) blank for past jobs — most
      companies want at least "自己都合により退職" (resigned for personal reasons) or
      "契約満了" (contract completion).</li>
  <li>Mixing fonts within the document. MS Mincho or Yu Mincho for body, MS Gothic
      for headings, applied consistently.</li>
  <li>Listing the wrong "Date of issue" (発行日) on certificates — should match
      what the issuing institution shows.</li>
  <li>Skipping the "Hobbies and special skills" (趣味・特技) section. Japanese
      hiring managers read this carefully as a personality signal.</li>
  <li>Adding negative justifications in self-PR ("I struggle with X but...").
      Self-PR in Japanese context should be uniformly positive.</li>
  <li>Misformatting phone numbers — should be 090-XXXX-XXXX, not international
      format.</li>
  <li>Writing the family name first AND in lowercase. Should be UPPERCASE family
      name first when written in romaji.</li>
  <li>Forgetting to handwrite (or carefully sign) the document if submitted on
      paper. Even with digital submission, signature-style fields are sometimes
      expected.</li>
</ol>
""",
    },

    # ============================================================ interview-etiquette
    "interview-etiquette": {
        "toc_additions": [
            ("online-interview", "Online and video interview etiquette"),
            ("reverse-interview", "Reverse interview — questions you should ask"),
            ("body-language", "Body language and pacing"),
            ("difficult-questions", "Difficult questions and how to handle them"),
            ("post-interview", "Post-interview — thank-you emails and follow-up"),
            ("multi-round", "Multi-round interviews — what changes at each stage"),
        ],
        "body_addition": """
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
      affected — onscreen presence still expects the cultural gesture.</li>
  <li><strong>Use proper closing:</strong> <em>"本日はお時間をいただきありがとうございました.
      引き続きどうぞよろしくお願いいたします."</em></li>
  <li><strong>Don't disconnect first.</strong> Wait for the interviewer to end the
      call. If you must leave first, ask politely.</li>
  <li><strong>Connection backup plan.</strong> Have a phone number ready in case
      video fails. Mention it in your reply when scheduling.</li>
</ul>

<h2 id="reverse-interview">Reverse interview — questions you should ask</h2>
<p>Japanese interviews almost always end with "最後に、何かご質問はありますか?" (Any
final questions?). Skipping this question or saying "No, I think I have all the
information" is a notable negative signal — it reads as lack of preparation or
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
  <li><strong>Aizuchi (相槌).</strong> Quiet acknowledgements — "はい",
      "そうですね", "なるほど" — while listening are expected. Silence while the
      interviewer is speaking reads as inattentive.</li>
</ul>

<h2 id="difficult-questions">Difficult questions and how to handle them</h2>
<table>
  <thead><tr><th>Question</th><th>What it's really testing</th><th>How to handle it</th></tr></thead>
  <tbody>
    <tr><td>"前職を辞めた理由は?" (Why did you leave your last job?)</td>
        <td>Stability, attitude toward conflict</td>
        <td>Positive framing only — never blame employer or peers. Focus on
        what you want to learn next.</td></tr>
    <tr><td>"5年後どうなりたいですか?" (Where do you want to be in 5 years?)</td>
        <td>Commitment, planning ability</td>
        <td>Show ambition tied to growth at this employer, not "I'll have my own
        company in 5 years".</td></tr>
    <tr><td>"なぜ日本で働きたいのですか?" (Why work in Japan?)</td>
        <td>Genuine interest, longevity</td>
        <td>Concrete reasons — language study, career fit, family, culture
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

<h2 id="post-interview">Post-interview — thank-you emails and follow-up</h2>
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

<h2 id="multi-round">Multi-round interviews — what changes at each stage</h2>
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

    # ============================================================ salary
    "salary": {
        "toc_additions": [
            ("shunto-2026", "2026 Shunto wage growth in context"),
            ("bilingual-premium", "Bilingual premium — real numbers"),
            ("asking-for-raise", "How to ask for a raise in Japan"),
            ("benefits-translate", "How to compare benefits — Japan vs overseas offers"),
            ("offer-negotiation", "Offer negotiation tactics"),
            ("equity-stock", "Equity, RSUs, and stock options in Japan"),
        ],
        "body_addition": """
<!-- ENRICH_V2:salary -->
<h2 id="shunto-2026">2026 Shunto wage growth in context</h2>
<p>Japan's 2026 Shunto (spring labour-management wage negotiations) delivered a 5.26%
average wage increase — the third consecutive year over 5%, and the strongest
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
  <li>Bilingual professionals see the strongest leverage — Robert Walters' 2026
      report flags bilingual roles in tech, finance, and consulting as the top of
      the salary momentum curve.</li>
  <li>Small and mid-size Japanese employers (SMEs) have not kept pace; their wage
      hikes average 3–4%. If you're at an SME, job-changing to a larger employer
      is the comp lever.</li>
</ul>

<h2 id="bilingual-premium">Bilingual premium — real numbers</h2>
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
<p>The premium curve is steepest between N3 and N2 — that's where the management
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
      if they value you. But don't bluff — if you walk in with a competing offer,
      be willing to take it.</li>
  <li><strong>Be patient with the answer.</strong> Most managers can't grant a raise
      unilaterally; the conversation triggers HR and director-level escalation.
      Expect 2–4 weeks to get an answer.</li>
</ol>

<h2 id="benefits-translate">How to compare benefits — Japan vs overseas offers</h2>
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
  <li><strong>Commuter allowance (通勤手当).</strong> Standard in Japan — typically
      ¥10–50K/month covering train pass. Tax-free up to ¥150,000/month.</li>
  <li><strong>Housing allowance (住宅手当)</strong> — older corporates pay
      ¥20–80K/month. Most modern tech firms have phased this out, rolled into base.</li>
  <li><strong>Relocation package</strong> — international moves should include
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
      foreign-cap firms — increasingly so at Mercari, PayPay, SmartNews. Ask for an
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
""",
    },

    # ============================================================ cost-of-living
    "cost-of-living": {
        "toc_additions": [
            ("2026-rent-updates", "2026 rent changes by ward"),
            ("hidden-move-in", "Hidden move-in costs explained"),
            ("utilities-deep", "Utilities — what they actually cost"),
            ("foreigner-friendly-landlords", "Foreigner-friendly real estate agents"),
            ("monthly-budgets", "Realistic monthly budgets for different lifestyles"),
            ("regional-deltas", "Tokyo vs Osaka vs Fukuoka vs Sapporo"),
        ],
        "body_addition": """
<!-- ENRICH_V2:cost-of-living -->
<h2 id="2026-rent-updates">2026 rent changes by ward</h2>
<p>Tokyo rents continued upward through 2025 and into 2026 — driven by inbound
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

<h2 id="utilities-deep">Utilities — what they actually cost</h2>
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
  <li><strong>GaijinPot Housing / Apartments.com Japan</strong> — large foreigner-friendly
      listings, English-language support.</li>
  <li><strong>Sakura House / Oakhouse</strong> — share-houses and short-term
      apartments aimed at foreigners. Easy to set up; higher monthly rent but
      minimal move-in.</li>
  <li><strong>Tokyo Apartment Inc / Real Tokyo Estate</strong> — bilingual brokers
      with experience handling foreigner applications.</li>
  <li><strong>Plaza Homes</strong> — long-established serviced-apartment broker;
      historically luxury-focused but useful for executive relocations.</li>
  <li><strong>Ken Corporation</strong> — high-end foreigner-focused; specialises in
      Roppongi / Hiroo / Azabu market.</li>
  <li><strong>Apaman Shop / Mini Mini / Able</strong> — large Japanese chains; less
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
    <tr><td>Salary gap vs Tokyo</td><td>—</td><td>−5–10%</td><td>−15–25%</td><td>−20–30%</td></tr>
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

    # ============================================================ interview-phrases
    "interview-phrases": {
        "toc_additions": [
            ("keigo-errors", "Common keigo errors foreigners make"),
            ("tough-question-phrases", "Phrases for tough questions"),
            ("salary-discussion", "Phrases for salary discussions"),
            ("declining-clarifying", "Phrases for declining or clarifying"),
            ("video-specific", "Phrases specific to video interviews"),
        ],
        "body_addition": """
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
      ("Then, please excuse me.") — wait for the interviewer to hang up first.</li>
</ul>
""",
    },

    # ============================================================ red-flags
    "red-flags": {
        "toc_additions": [
            ("hidden-flags", "Hidden red flags in modern job posts"),
            ("remote-flags", "Remote-work and post-pandemic red flags"),
            ("forum-due-diligence", "Forum due-diligence — Reddit, Glassdoor, OpenWork"),
            ("contract-flags", "Contract / offer-letter red flags"),
            ("escape-plan", "If you're already in a black company — your exit plan"),
        ],
        "body_addition": """
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
      turnover — only young employees because mid-career ones have left.</li>
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
      considered a red flag — employers who refuse to share salary ranges typically
      pay below market.</li>
  <li><strong>"自己啓発" (self-development) mentioned as a job duty.</strong> Often
      means "we expect you to attend training on weekends or after hours, unpaid".</li>
  <li><strong>Always-hiring on every platform.</strong> Same job listing posted
      continuously for 6+ months on Indeed, Wantedly, LinkedIn, GaijinPot, Daijob —
      means people keep quitting.</li>
</ul>

<h2 id="remote-flags">Remote-work and post-pandemic red flags</h2>
<ul>
  <li><strong>"Flexible / hybrid" but no clarity on how many days.</strong> Press for
      specifics. "Flexible" with no policy often means "manager's discretion" which
      becomes "5 days in office".</li>
  <li><strong>Surveillance software requirement.</strong> If they require Hubstaff,
      Time Doctor, ActivTrak, or screenshot-based monitoring — strong negative
      signal regardless of nominal flexibility.</li>
  <li><strong>"Always-on" expectations.</strong> Slack DM responses required within
      15 minutes? Saturday client calls? Both red flags even at high-pay roles.</li>
  <li><strong>No equipment stipend.</strong> A modern remote role at any reasonable
      employer covers laptop, monitor budget, internet allowance. Asking employees
      to expense back through reimbursement (or not at all) signals stinginess.</li>
  <li><strong>"Return-to-office" planned without notice.</strong> Ask explicitly:
      "What's the policy on RTO, and what's the change-notice period?" Mercari /
      PayPay / Rakuten have all had unannounced RTO changes — being aware is the
      protection.</li>
</ul>

<h2 id="forum-due-diligence">Forum due-diligence — Reddit, Glassdoor, OpenWork</h2>
<p>Before signing, run the company through these checks:</p>
<ul>
  <li><strong>Glassdoor</strong> — global; many Japan companies have ratings here.
      Look at the "Pros / Cons" patterns over multiple years.</li>
  <li><strong>OpenWork (旧Vorkers)</strong> — Japan-specific. Free with one review
      contribution. Long-form Japanese reviews; translate with a tool if necessary.
      Most accurate single source for Japanese-language workplace culture.</li>
  <li><strong>en-Lighthouse</strong> — En Japan's Japanese-language review platform;
      strong for traditional Japanese corporates.</li>
  <li><strong>Reddit r/japanlife</strong> — search the company name. Strong honest
      sentiment, especially for English-teaching and IT firms.</li>
  <li><strong>Reddit r/teachinginjapan</strong> — eikaiwa- and ALT-specific; search
      the company.</li>
  <li><strong>TokyoDev forum / Slack</strong> — search the company. Many tech
      employees post candid impressions.</li>
  <li><strong>LinkedIn — search current employees.</strong> Are most employees
      <2 years tenure? Are senior people leaving in clusters? These are tell-tale
      patterns.</li>
  <li><strong>Hello Work labor inspector records</strong> — if a company has had
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

<h2 id="escape-plan">If you're already in a black company — your exit plan</h2>
<p>The 6-step exit plan:</p>
<ol>
  <li><strong>Quiet preparation (Month 1–2).</strong> Update CV, rirekisho, English
      LinkedIn. Don't tell co-workers. Apply through personal email only.</li>
  <li><strong>Document everything (Month 1–3).</strong> Save copies of payslips, work
      schedules, overtime hours. If you have unpaid OT or harassment claims, these
      records are your evidence.</li>
  <li><strong>Apply broadly (Month 2–3).</strong> Mercari, PayPay, foreign-cap SaaS,
      Indeed Tokyo, FAANG Tokyo all hire continuously. Aim for 30+ applications.</li>
  <li><strong>Interview during PTO.</strong> Take paid leave for interview rounds —
      it's your legal right.</li>
  <li><strong>Get the offer in writing (Month 3–4).</strong> Wait until you have a
      signed offer before resigning. Don't accept verbal-only offers.</li>
  <li><strong>Resign formally (Month 4).</strong> Submit 退職届 (taishokutodoke,
      resignation letter) at least 30 days before exit date — by law that's all
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
""",
    },

}
