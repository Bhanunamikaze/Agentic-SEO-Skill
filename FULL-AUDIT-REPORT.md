# SEO Full Audit Report — missionspropertyservices.com

**Audit Date:** 2026-05-09 | **Scope:** Full-Site Audit | **Industry:** Local Service Business  
**Score Confidence:** Medium (CWV data unavailable — PageSpeed API rate-limited)

---

## A) Audit Summary

### Overall Score: 53 / 100 — Needs Improvement

| Category | Weight | Score | Weighted |
|---|---|---|---|
| Technical SEO | 25% | 48 | 12.0 |
| Content Quality / E-E-A-T | 20% | 60 | 12.0 |
| On-Page SEO | 15% | 55 | 8.3 |
| Schema / Structured Data | 15% | 50 | 7.5 |
| Performance (CWV) | 10% | N/A* | 5.0* |
| Image Optimization | 10% | 40 | 4.0 |
| AI Search Readiness (GEO) | 5% | 20 | 1.0 |
| **TOTAL** | 100% | — | **~53** |

> *CWV score estimated from structural signals only.

### Top 3 Critical Issues
1. **React SPA with no SSR** — Googlebot sees an empty `<div id="root"></div>`; all content requires JS execution
2. **Zero canonical tags** — 12 pages serve nearly identical HTML, creating duplicate content risk
3. **Schema only in client-rendered DOM** — Contractor JSON-LD may not be parsed at crawl time

### Top 3 Opportunities
1. Add SSR/pre-rendering — unlocks all existing good content for crawlers immediately
2. Add LocalBusiness/Contractor JSON-LD in static `<head>` — can be done before full SSR migration
3. Expand 11 city service area pages with unique localised content + per-city schema

---

## B) Findings Table

| Area | Severity | Confidence | Finding | Evidence | Fix |
|---|---|---|---|---|---|
| Technical | Critical | Confirmed | React SPA delivers empty HTML to crawlers | parse_html: h1=[], word_count=7, body=`<div id="root">` | Next.js SSR or Cloudflare Edge prerender |
| Technical | Critical | Confirmed | No canonical tag on any page | parse_html canonical: null on all pages | Add `<link rel="canonical">` per-route |
| Technical | Warning | Confirmed | 5 security headers missing (HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy) | security_headers score 40/100 | Add via Cloudflare Transform Rules |
| Technical | Warning | Confirmed | Sitemap uses relative URLs; no lastmod dates | sitemap.xml: `<loc>/</loc>` | Fix to absolute URLs; add `<lastmod>` |
| On-Page | Critical | Confirmed | H1 only in JS-rendered DOM; static HTML has none | parse_html h1: [] | Render H1 server-side |
| On-Page | Critical | Confirmed | og:url missing | social_meta.py: "Missing required: og:url" | Add `<meta property="og:url">` |
| On-Page | Warning | Confirmed | og:title 62 chars (limit 60) | social_meta.py | Trim to ≤ 60 chars |
| On-Page | Warning | Confirmed | All service area pages share same title/meta as homepage | Fetch of /service-areas/san-antonio returns identical HTML shell | Inject unique title/description per route in server response |
| Schema | Critical | Likely | Contractor JSON-LD only in client DOM, not static HTML | parse_html schema: []; browser sees it after JS load | Move JSON-LD to static `<head>` |
| Schema | Warning | Confirmed | Schema missing @id, url, sameAs, openingHours, priceRange, geo | Browser-captured schema lacks GBP, hours, coordinates | Extend with full LocalBusiness properties |
| Schema | Warning | Likely | 11 city pages have no per-page schema | All serve identical JS shell | Add per-city LocalBusiness schema with areaServed |
| Content | Warning | Confirmed | No About/Team page for E-E-A-T | Nav lacks About page | Add owner bio, license number, photo, years in business |
| Content | Warning | Confirmed | Only Instagram in footer; no GBP link | Browser footer observation | Add GBP + Facebook links; include in sameAs |
| Content | Pass | Confirmed | Homepage H1/H2/H3 hierarchy is logical and keyword-rich | Browser: H1="ONE TEAM FOR ALL YOUR PROPERTY NEEDS" | — |
| Content | Pass | Confirmed | San Antonio page has localised content with zip codes, landmarks | Browser: zip codes 78201–78251, Monte Vista, King William | Replicate across all city pages |
| Performance | Warning | Hypothesis | CWV risk from large unoptimised SPA JS bundle | Single ES module bundle; no preload hints in HTML | Run PageSpeed with API key; add code splitting |
| Images | Critical | Likely | No alt attributes in static HTML | parse_html images: [] | Add alt text server-side with SSR |
| Images | Warning | Confirmed | OG image on external GCS with AI-generated filename | og:image URL contains "ChatGPT_Image_Apr_20" | Host on own domain; descriptive filename |
| Images | Info | Confirmed | og:image:width/height missing | social_meta.py | Add 1200x630 |
| GEO/AI | Critical | Confirmed | llms.txt exists but is nearly empty (score 5/100) | llms_txt_checker: no title, description, or links | Populate with site summary and key page links |
| GEO/AI | Warning | Confirmed | 11 AI crawlers not explicitly managed in robots.txt | robots_checker: GPTBot, ClaudeBot, PerplexityBot, etc. inherit * | Add explicit Allow: / per AI crawler |
| Crawl | Pass | Confirmed | No redirect chain; 200 in 186ms | redirect_checker: 0 hops | — |
| Crawl | Pass | Confirmed | robots.txt 200; sitemap referenced | robots_checker | — |
| Crawl | Pass | Confirmed | HTTPS in use | security_headers | — |
| Crawl | Pass | Confirmed | lang="en" on html element | Raw HTML | — |
| Mobile | Pass | Confirmed | Viewport meta correct; no horizontal scroll; touch targets OK | analyze_visual.py | — |
| Social | Pass | Confirmed | Twitter Card summary_large_image configured | social_meta.py | — |

---

## C) Prioritized Action Plan (Summary)

See ACTION-PLAN.md for full execution steps.

**Phase 1 — Blockers (0–2 weeks):**
1. Implement SSR or Cloudflare Edge bot prerender
2. Add canonical tags to every page
3. Move JSON-LD schema to static `<head>`
4. Fix sitemap: absolute URLs + lastmod dates
5. Add og:url tag

**Phase 2 — Quick Wins (30 days):**
6. Add 5 missing security headers via Cloudflare
7. Populate llms.txt (title, description, links)
8. Trim og:title to ≤ 60 chars
9. Add og:site_name, og:image dimensions
10. Explicit AI-crawler Allow rules in robots.txt
11. Extend Contractor schema: sameAs, openingHours, geo, priceRange

**Phase 3 — Strategic (60–90 days):**
12. Unique 300–500 word content on all 11 city pages
13. Per-city LocalBusiness schema on each city page
14. Create About/Team page for E-E-A-T
15. Add GBP link to footer and schema sameAs
16. PageSpeed: code splitting, image lazy-loading, preload hints
17. Ensure all images have descriptive alt text post-SSR

---

## D) Unknowns & Follow-ups

| Unknown | How to Resolve |
|---|---|
| Core Web Vitals | Re-run pagespeed.py with PAGESPEED_API_KEY or use https://pagespeed.web.dev |
| Unique content on 10 remaining city pages | Visit each /service-areas/[city] in browser |
| Image count + alt coverage | Browser devtools: document.querySelectorAll('img[alt]').length |
| GSC index coverage | Connect to Google Search Console |
| Contractor schema validation | https://search.google.com/test/rich-results |
| GBP claimed/verified | Search Google Maps |
| Backlink profile | Ahrefs / Semrush / Moz |

---

## Environment Limitations

- Google PageSpeed API was rate-limited — CWV metrics are hypothesis only
- Broken links check failed (no links in static DOM) — check manually
- Readability analysis skipped (7 words in static HTML) — re-run after SSR
