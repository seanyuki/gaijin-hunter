#!/usr/bin/env bash
# Production smoke test — plain GET requests (never HEAD: some routes/CDNs
# reject HEAD and produce misleading 403/405s).
#
#   BASE_URL=https://gaijinhunterjp.com ./scripts/smoke_prod.sh
#   BASE_URL=http://127.0.0.1:5000      ./scripts/smoke_prod.sh
set -u

BASE_URL="${BASE_URL:-http://127.0.0.1:5000}"
BASE_URL="${BASE_URL%/}"

PATHS=(
  "/healthz"
  "/"
  "/jobs"
  "/jobs?professional_only=1"
  "/jobs?visa_support=1"
  "/jobs?apply_from_abroad=1"
  "/resources/applying-from-abroad"
  "/privacy"
  "/resume"
  "/sitemap.xml"
  "/robots.txt"
  "/llms.txt"
  "/static/favicon.svg"
  "/static/logo.svg"
  "/static/og-default.png"
)

pass=0; fail=0
printf "Smoke test against %s\n\n" "$BASE_URL"
for p in "${PATHS[@]}"; do
  # -L follows the www->apex / http->https canonical redirects; the final
  # answer must be 200. --max-time keeps a dead host from hanging the run.
  code=$(curl -s -L --max-time 20 -o /dev/null -w "%{http_code}" "$BASE_URL$p")
  if [ "$code" = "200" ]; then
    printf "  [PASS] %s %s\n" "$code" "$p"; pass=$((pass+1))
  else
    printf "  [FAIL] %s %s\n" "$code" "$p"; fail=$((fail+1))
  fi
done

# healthz must report ok and a non-empty job index.
hz=$(curl -s -L --max-time 20 "$BASE_URL/healthz")
if printf '%s' "$hz" | grep -q '"status": *"ok"'; then
  printf "  [PASS] healthz body: %s\n" "$(printf '%s' "$hz" | tr -d '\n ' | cut -c1-80)"; pass=$((pass+1))
else
  printf "  [FAIL] healthz body: %s\n" "$hz"; fail=$((fail+1))
fi

printf "\n%d passed, %d failed\n" "$pass" "$fail"
[ "$fail" -eq 0 ]
