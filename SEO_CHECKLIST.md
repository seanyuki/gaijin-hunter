# SEO checklist

## Done (verified in this pass)

- [x] **Canonical URLs** on every page (`<link rel=canonical>`), path-only —
      filter/query params never create duplicate canonicals.
- [x] **BASE_URL env var** drives canonical/sitemap/OG/JSON-LD/llms.txt
      absolute URLs in production (falls back to request origin in dev).
      Set it on deploy: `BASE_URL=https://yourdomain`.
- [x] **Sitemap** (`/sitemap.xml`): static pages + resources, guides, living,
      pillars, companies, /privacy. Priorities + changefreq + lastmod.
- [x] **robots.txt**: allows everything except /api/ and internal; explicitly
      allows AI crawlers; links the sitemap.
- [x] **OG image**: `static/og-default.png` (1200×630) now actually exists
      (was a 404 — meta tags referenced .png while only .svg shipped).
- [x] **noindex** on user-specific/utility pages: /saved /applied /archived
      views, /tracker, /profile, /data, /compare, employer manage, error pages,
      newsletter-unsubscribe.
- [x] **Job detail pages**: unique `<title>` (job title) + unique meta
      description generated from company/location/description snippet.
- [x] **llms.txt** for AI-assistant discovery; FAQPage + Organization +
      WebSite/SearchAction + per-page JSON-LD intact.
- [x] No duplicate content routes found (/roadmaps 301s into /guides;
      /tracker and /jobs/tracker render the same noindexed page).

## On deploy

- [ ] Set `BASE_URL` to the real public origin (no trailing slash).
- [ ] Verify `https://domain/sitemap.xml` URLs use that origin.
- [ ] Submit the sitemap in Google Search Console + Bing Webmaster Tools.
- [ ] Spot-check one job page, one resource and the homepage in
      https://search.google.com/test/rich-results (FAQ + Organization).
- [ ] Check the OG card in https://www.opengraph.xyz or a Slack/Discord paste.

## Known trade-offs

- Job pages churn (30-day stale window): expired jobs 404 — acceptable, but a
  410 or an "expired posting" page with similar-jobs links would be nicer.
- The OG image still uses the older navy branding; regenerate from the warm
  palette when convenient (`static/og-default.svg` → screenshot at 1200×630).
- JobPosting JSON-LD on /job/<id> (Google Jobs eligibility) is not implemented;
  worth doing once the site has a stable public domain.
