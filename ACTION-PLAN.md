# SEO Action Plan — missionspropertyservices.com
**Generated:** 2026-05-09 | Based on FULL-AUDIT-REPORT.md

---

## Phase 1 — Critical Blockers (Fix within 2 weeks)

### Action 1: Implement SSR or Bot Prerender
- **Type:** Strategic | **Impact:** Highest | **Effort:** High
- **Problem:** React SPA renders an empty HTML shell; Googlebot cannot index any content
- **Option A (Recommended):** Migrate to Next.js — wrap pages in `getServerSideProps` or use `next export` for static generation
- **Option B (Stop-gap):** Add Cloudflare Worker that detects bot User-Agents and serves pre-rendered HTML via `@cloudflare/puppeteer` or a prerender.io integration
- **Acceptance:** `parse_html.py` returns H1, H2 headings and word_count > 300

### Action 2: Add Canonical Tags to Every Page
- **Type:** Quick win (once SSR is live) | **Impact:** High | **Effort:** Low
- Add to each page's `<head>`:
  ```html
  <link rel="canonical" href="https://missionspropertyservices.com/[path]">
  ```
- For homepage: `href="https://missionspropertyservices.com/"`
- For city pages: `href="https://missionspropertyservices.com/service-areas/san-antonio"` etc.

### Action 3: Move JSON-LD Schema to Static HTML `<head>`
- **Type:** Quick win | **Impact:** High | **Effort:** Low
- Even before full SSR, paste the Contractor schema directly into the HTML template:
  ```html
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Contractor",
    "@id": "https://missionspropertyservices.com/#contractor",
    "name": "Missions Property Services",
    "url": "https://missionspropertyservices.com",
    "telephone": "+1-210-XXX-XXXX",
    "email": "info@missionspropertyservices.com",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "San Antonio",
      "addressRegion": "TX",
      "addressCountry": "US"
    },
    "areaServed": [
      "San Antonio", "Alamo Heights", "Stone Oak", "Schertz",
      "Cibolo", "Helotes", "Boerne", "Live Oak",
      "Universal City", "Converse", "Leon Valley", "Selma"
    ],
    "openingHours": "Mo-Fr 08:00-18:00",
    "priceRange": "$$",
    "sameAs": [
      "https://www.instagram.com/missionspropertyservices",
      "https://www.google.com/maps/place/YOUR_GBP_ID"
    ]
  }
  </script>
  ```

### Action 4: Fix Sitemap
- **Type:** Quick win | **Impact:** Medium | **Effort:** Low
- Change all relative `<loc>` to absolute URLs:
  ```xml
  <loc>https://missionspropertyservices.com/</loc>
  <loc>https://missionspropertyservices.com/projects</loc>
  <loc>https://missionspropertyservices.com/service-areas/san-antonio</loc>
  ```
- Add `<lastmod>2026-05-01</lastmod>` to each entry
- Submit updated sitemap in Google Search Console

### Action 5: Add og:url Meta Tag
- **Type:** Quick win | **Impact:** Medium | **Effort:** Low
- Add to each page's `<head>`:
  ```html
  <meta property="og:url" content="https://missionspropertyservices.com/">
  ```

---

## Phase 2 — Quick Wins (Fix within 30 days)

### Action 6: Add Security Headers via Cloudflare
- Go to Cloudflare Dashboard → Your Domain → Rules → Transform Rules → Modify Response Header
- Add the following headers:
  ```
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  ```

### Action 7: Populate llms.txt
- Edit `https://missionspropertyservices.com/llms.txt` to:
  ```
  # Missions Property Services
  > Greater San Antonio's one-stop property services contractor.
  > Handyman, remodels, fencing & landscaping. Licensed, insured, 5-star rated.

  ## Key Pages
  - [Home](https://missionspropertyservices.com/): Overview of all services
  - [Services](https://missionspropertyservices.com/#services): Handyman, remodeling, fencing, landscaping
  - [Projects](https://missionspropertyservices.com/projects): Portfolio of completed work
  - [San Antonio](https://missionspropertyservices.com/service-areas/san-antonio): Service area
  - [Contact](https://missionspropertyservices.com/#contact): Book a free estimate
  ```

### Action 8: Fix og:title Length
- Current: "Missions Property Services | San Antonio Handyman & Remodeling" (62 chars)
- Change to: "Missions Property Services | SA Handyman & Remodeling" (54 chars)

### Action 9: Add Supplementary Social Meta Tags
  ```html
  <meta property="og:site_name" content="Missions Property Services">
  <meta property="og:locale" content="en_US">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  ```

### Action 10: Explicit AI Crawler Rules in robots.txt
- Append to `robots.txt`:
  ```
  User-agent: GPTBot
  Allow: /

  User-agent: ChatGPT-User
  Allow: /

  User-agent: ClaudeBot
  Allow: /

  User-agent: PerplexityBot
  Allow: /

  User-agent: Google-Extended
  Allow: /

  User-agent: Applebot-Extended
  Allow: /

  User-agent: Bytespider
  Allow: /

  User-agent: CCBot
  Allow: /
  ```

### Action 11: Extend Contractor Schema
- Add to the JSON-LD from Action 3:
  ```json
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 29.4241,
    "longitude": -98.4936
  },
  "hasMap": "https://maps.google.com/?q=Missions+Property+Services+San+Antonio",
  "image": "https://missionspropertyservices.com/assets/missions-logo-C2qq7klh.webp",
  "description": "Greater San Antonio's one-stop property services contractor. Handyman, remodels, fencing & landscaping in Bexar County."
  ```

---

## Phase 3 — Strategic Improvements (60–90 days)

### Action 12: Unique Content on All City Service Area Pages
- Minimum 300–500 unique words per page
- Include: neighbourhoods served, local landmarks, zip codes, specific services offered in that city, a local FAQ, and 1 project example
- Do NOT copy-paste from the San Antonio page template without significant localisation

### Action 13: Per-City LocalBusiness Schema
- On each `/service-areas/[city]` page add:
  ```json
  {
    "@context": "https://schema.org",
    "@type": ["LocalBusiness", "Contractor"],
    "name": "Missions Property Services",
    "areaServed": {
      "@type": "City",
      "name": "Alamo Heights",
      "sameAs": "https://en.wikipedia.org/wiki/Alamo_Heights,_Texas"
    }
  }
  ```

### Action 14: Create About / Team Page
- Page URL: `/about`
- Content: Owner name + photo, years in business, TX contractor license number, service philosophy, certifications
- This directly improves Google's E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) assessment

### Action 15: Add GBP and Social Links to Footer
- Footer should include links to: Google Business Profile, Facebook, Instagram
- Add these URLs to `sameAs` in schema

### Action 16: Performance Optimisation
- Split JS bundle with dynamic imports in React
- Add `<link rel="preload" as="image" href="/assets/missions-logo-C2qq7klh.webp">` to `<head>`
- Implement lazy loading for below-fold images (`loading="lazy"`)
- Target: LCP < 2.5s, INP < 200ms, CLS < 0.1

### Action 17: Image Alt Text Audit (Post-SSR)
- After SSR is live, run: `document.querySelectorAll('img:not([alt])')` in browser devtools
- Add descriptive, keyword-rich alt text to every image
- Example: `alt="San Antonio handyman installing fence in Alamo Heights"` instead of `alt="image"`

---

## Verification Checklist

- [ ] `parse_html.py` returns H1, headings, and word_count > 300
- [ ] `parse_html.py` returns canonical URL for each page
- [ ] `parse_html.py` returns schema[] with Contractor data
- [ ] `sitemap.xml` shows absolute URLs with lastmod dates
- [ ] `social_meta.py` score > 80/100
- [ ] `llms_txt_checker.py` score > 70/100
- [ ] `security_headers.py` score > 70/100
- [ ] Google Rich Results Test passes for Contractor schema
- [ ] PageSpeed Insights mobile score > 70
