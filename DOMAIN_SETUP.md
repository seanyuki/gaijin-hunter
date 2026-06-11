# Domain setup — gaijinhunterjp.com (Squarespace DNS → Render)

## Canonical domain decision

**Canonical: `https://gaijinhunterjp.com` (apex, no www).**

Why apex: the brand reads cleaner in links and citations; Render supports
apex domains directly (it fronts everything with its own proxy, so the usual
"apex can't CNAME" limitation is handled by an A record they provide); and a
single short canonical keeps sitemap/OG/JSON-LD simple. `www.gaijinhunterjp.com`
stays registered and **301-redirects to the apex** — both at the Render edge
(when both domains are added to the service) and in the app itself
(`app.py` canonicalizes any non-canonical host in production; `/healthz` is
exempt so platform health checks never see a redirect). Sitemap, canonical
tags, OpenGraph, robots and llms.txt all emit `BASE_URL`, so setting
`BASE_URL=https://gaijinhunterjp.com` makes everything consistent. If you ever
prefer www as canonical instead, set `BASE_URL=https://www.gaijinhunterjp.com`
— everything follows automatically; just flip which domain is primary in Render.

## Order of operations

1. Deploy the Render service first (`render.yaml`) and confirm
   `https://<your-service>.onrender.com/healthz` returns `{"status":"ok"}`.
2. In Render: **Settings → Custom Domains → Add** `gaijinhunterjp.com`,
   then add `www.gaijinhunterjp.com`. Render displays the exact DNS records
   it wants — use those values (they're authoritative; the values below are
   Render's current standard ones).
3. Then do the Squarespace steps below.

## Squarespace DNS steps

1. Log in to Squarespace → account menu → **Domains** dashboard.
2. Select **gaijinhunterjp.com**.
3. Open **DNS** (a.k.a. DNS Settings / Manage DNS).
4. **Remove Squarespace's default website records.** A Squarespace-purchased
   domain is pre-pointed at Squarespace's own site infrastructure. Delete (or
   you'll get conflicts and the Squarespace parking page instead of the app):
   - the four default `A` records on `@` (Squarespace/Google IPs, e.g. 198.185.159.x / 198.49.23.x)
   - any `AAAA` records on `@`
   - the default `CNAME` on `www` pointing to `ext-cust.squarespace.com` or similar
   - leave MX/TXT records alone if you use the domain for email
5. **Add the records Render shows you:**

   **Apex / root (`gaijinhunterjp.com`)** — Squarespace DNS does not support
   ALIAS/ANAME on the apex, so use Render's A record:

   ```
   Type:  A
   Host:  @
   Value: 216.24.57.1        ← use the IP shown in Render's Custom Domains panel
   ```

   **www (`www.gaijinhunterjp.com`)**:

   ```
   Type:  CNAME
   Host:  www
   Value: <your-service>.onrender.com
   ```

6. Save, then click **Verify** on each domain in Render's Custom Domains panel.

## Warnings & gotchas

- **Conflicting records**: an apex can't have the Render A record *and* old
  A/AAAA records — remove every other A/AAAA on `@`, and any other CNAME on `www`.
- **Propagation**: DNS changes can take minutes to ~48h (usually <1h).
  Check with `dig +short gaijinhunterjp.com` / `dig +short www.gaijinhunterjp.com CNAME`.
- **SSL pending**: Render's certificate stays "Pending" until DNS resolves to
  Render. Don't panic for the first hour; re-verify after propagation.
- **Don't test with `curl -I`** (HEAD) — some routes/CDN paths reject HEAD and
  you'll chase phantom 403/405s. Use GET:
  `BASE_URL=https://gaijinhunterjp.com ./scripts/smoke_prod.sh`
- Squarespace may show a "this domain is not connected to a site" banner in
  its own UI once you de-point it — that's expected; the domain is serving
  Render, not Squarespace.

## After DNS resolves

```bash
BASE_URL=https://gaijinhunterjp.com ./scripts/smoke_prod.sh   # all GET checks
curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" https://www.gaijinhunterjp.com/jobs
#   expect: 301 https://gaijinhunterjp.com/jobs
```

Then run the first-refresh runbook in DEPLOYMENT.md and submit
`https://gaijinhunterjp.com/sitemap.xml` to Google Search Console.
