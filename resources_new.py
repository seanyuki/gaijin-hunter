"""
Newer resource pages kept out of the very large content.py. content.py imports
this module at the bottom and appends each entry to RESOURCES, so these render
identically to the originals at /resources/<slug>.
"""

APPLYING_FROM_ABROAD = {
    "slug": "applying-from-abroad",
    "icon": "🌏",
    "title": "Applying from abroad, how to land a Japan job before you move",
    "summary": "The realistic playbook for getting hired in Japan while you still live "
               "overseas: which employers actually do it, how the COE process works, "
               "interview logistics across time zones, and what to have ready.",
    "updated": "2026-06",
    "read_time": 9,
    "toc": [
        ("reality", "The reality check"),
        ("who-hires", "Who actually hires from overseas"),
        ("coe", "How the visa process works (COE)"),
        ("documents", "Documents to prepare before applying"),
        ("interviews", "Remote interviews across time zones"),
        ("timeline", "A realistic end-to-end timeline"),
        ("checklist", "Checklist"),
    ],
    "body": """
<p style="background:var(--accent-tint); border:1px solid var(--accent-soft); border-radius:10px;
   padding:14px 16px; font-size:14px; line-height:1.7;">
<strong>Start here:</strong> browse
<a href="/jobs?apply_from_abroad=1">jobs you can apply to from abroad</a>,
<a href="/jobs?visa_support=1">jobs that mention visa support</a>, or
<a href="/jobs?professional_only=1&visa_support=1">professional roles with visa support</a>.
Then come back for the process below — offer to first day is typically 2–4 months.</p>

<h2 id="reality">The reality check</h2>
<p>Hiring someone who is not yet in Japan costs an employer real money and 2–4 months of
waiting, so most postings quietly assume you already live here. That said, thousands of
people are hired from abroad every year — overwhelmingly into roles where the skill is
scarce in Japan: software engineering, data/AI, finance, bilingual product and project
roles, research, and some teaching programs that run structured overseas intakes.</p>
<p>On this board, use the <a href="/jobs?overseas_application_ok=1">Apply from abroad</a>
filter for postings that say so explicitly, and
<a href="/jobs?visa_sponsorship_mentioned=1">Visa support</a> for employers that mention
sponsorship. A posting that says neither isn't necessarily closed to you — but your first
question to the recruiter should settle both points before you invest in the process.</p>

<h2 id="who-hires">Who actually hires from overseas</h2>
<p>Four employer groups do the bulk of overseas hiring. <strong>Global tech companies with
Tokyo offices</strong> (and English-first Japanese tech companies like Mercari or Money
Forward's international teams) run mature relocation pipelines: they sponsor visas as
standard, often pay for flights and the first month of housing, and interview entirely on
video. <strong>Japanese companies with structured global-hiring programs</strong> recruit
new graduates and engineers from overseas universities on fixed annual cycles.
<strong>Eikaiwa chains and ALT dispatch companies</strong> (Interac, Borderlink, JET
Programme) are built around overseas intake — lower pay, but the lowest-friction path in.
<strong>Recruiting agencies</strong> (Robert Walters, Morgan McKinley, en world, JAC) place
bilingual professionals; they rarely relocate someone without Japanese, but are worth
contacting if you have N2-level Japanese or a hard-to-find specialty.</p>

<h2 id="coe">How the visa process works (COE)</h2>
<p>You cannot apply for a Japanese work visa on your own from zero — an employer applies
<em>for</em> you. After you sign an offer, the company files for a
<strong>Certificate of Eligibility (COE)</strong> with the Immigration Services Agency in
Japan. This takes roughly <strong>1–3 months</strong>. Once the COE is issued, you take it
to your local Japanese embassy or consulate and receive the actual visa, usually within
about a week. Then you book the flight.</p>
<p>Practical consequences: your start date will be 2–4 months after the offer, employers
know this and plan around it, and any company that asks <em>you</em> to figure out your own
work visa is a red flag. The employer drives the COE; your job is to supply documents
quickly (degree certificate, passport scan, photos, CV).</p>

<h2 id="documents">Documents to prepare before applying</h2>
<p>Have these ready before you start applying — they're requested at offer stage and slow
everything down if missing: your <strong>degree certificate</strong> (the standard work
visa effectively requires a bachelor's degree or 10 years of documented experience), an
up-to-date <strong>English CV</strong> (use the <a href="/resume/cv">CV builder</a>), a
<strong>Japanese rirekisho</strong> if you'll approach Japanese-language employers
(<a href="/resume">builder here</a>), JLPT certificates if you have them, and a passport
valid for well over a year. If your salary will exceed roughly ¥20M or you have a strong
academic background, check the <a href="/tools/hsp-points">HSP points calculator</a> —
the Highly Skilled Professional visa gives faster permanent-residence eligibility and is
worth requesting when you qualify.</p>

<h2 id="interviews">Remote interviews across time zones</h2>
<p>Expect 3–5 video rounds. Japanese companies usually schedule in Japan business hours, so
from the Americas or Europe you'll interview early morning or late evening — confirm the
time zone explicitly in every invite (JST is referenced by default, often without saying
so). Technical hiring at international companies looks like technical hiring anywhere:
coding screens, system design, behavioral rounds. Traditional Japanese employers add
motivation-heavy questions — "why Japan" matters as much as "why us", and a concrete
answer (not "I love anime") carries real weight. See
<a href="/resources/interview-etiquette">interview etiquette</a> and prep with the
<a href="/interview-prep">question bank</a>.</p>

<h2 id="timeline">A realistic end-to-end timeline</h2>
<p>From first application to your first day in Tokyo, plan on <strong>4–8 months</strong>:
1–3 months of applications and interviews, 2–4 weeks of offer negotiation and document
collection, 1–3 months of COE processing, a week for the visa itself, then flights and
temporary housing. Money: arrive with ¥500K–¥1M of savings even with a relocation package —
deposits, key money and furniture hit before your first paycheck. The
<a href="/tools/relocation-budget">relocation budget tool</a> gives a line-item estimate.</p>

<h2 id="checklist">Checklist</h2>
<table>
<tr><th>Stage</th><th>Action</th></tr>
<tr><td>Before applying</td><td>Degree certificate located; English CV finished; JLPT certs scanned; target list built from the <a href="/jobs?overseas_application_ok=1">Apply-from-abroad filter</a> and <a href="/companies">companies index</a></td></tr>
<tr><td>Applying</td><td>Ask about sponsorship + overseas hiring in the first conversation; track everything in the <a href="/tracker">application tracker</a></td></tr>
<tr><td>Offer</td><td>Confirm who pays for relocation and temporary housing; confirm COE filing date; check HSP eligibility</td></tr>
<tr><td>COE wait</td><td>Give notice (after COE is filed, not before); gather apartment-guarantor info; budget with the <a href="/tools/take-home-pay">take-home pay calculator</a></td></tr>
<tr><td>Visa in hand</td><td>Book flights; arrange first month's housing; read the <a href="/living">Living in Japan guides</a> for arrival-week admin</td></tr>
</table>
""",
}

EXTRA_RESOURCES = [APPLYING_FROM_ABROAD]
