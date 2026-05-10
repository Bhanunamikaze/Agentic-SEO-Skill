# SEO Best Practices for New Builds
<!-- Distilled from: missionspropertyservices.com audit (2026-05-09) -->
<!-- Updated: 2026-05-10 -->

A framework-agnostic checklist to implement on every new web project **before launch**.
Items are grouped by category and ordered by impact. Check each box during build QA.

---

## 1. Rendering & Crawlability

> **Root rule:** If Googlebot cannot read your content in the raw HTML response, nothing else in this list matters.

- [ ] **Use SSR or SSG — never ship a pure client-side SPA for public pages**
  - React: use Next.js (`getServerSideProps`, `generateStaticParams`, or `next export`)
  - Vue: use Nuxt.js
  - General: use Astro, Eleventy, or any static site generator
  - Verify: `curl -s https://yourdomain.com | grep "<h1"` must return content
- [ ] **Each route must return a unique, complete HTML document** — title, meta, H1, and body text present in the server response, not injected post-load
- [ ] **Add `<link rel="canonical">` to every page** matching the canonical URL for that route
  ```html
  <link rel="canonical" href="https://example.com/your-page-path/">
  ```
- [ ] **Set `<html lang="[code]">` correctly** (e.g. `lang="en"` for English sites)
- [ ] **Ensure HTTPS is enforced** — no HTTP fallback; all assets load over HTTPS
- [ ] **Verify no redirect chains** — root domain should resolve in ≤ 1 hop at 200
- [ ] **Keep `robots.txt` at domain root** returning HTTP 200; reference `Sitemap:` URL

---

## 2. On-Page Metadata

- [ ] **`<title>` tag: 50–60 characters** — include primary keyword + brand name
  - Format: `Primary Keyword | Brand Name` or `Brand Name | Keyword Descriptor`
  - Never exceed 60 chars (truncated in SERPs)
- [ ] **`<meta name="description">`: 120–155 characters** — compelling, includes keyword, ends with CTA
- [ ] **One `<h1>` per page** — must be present in server-rendered HTML, not injected by JS
- [ ] **Logical heading hierarchy** — H1 → H2 → H3 (no skipping levels)
- [ ] **Unique title + meta description per page** — no two pages share the same values; critical for service area / location pages
- [ ] **`<meta name="viewport" content="width=device-width, initial-scale=1.0">`** — required for mobile-first indexing (100% of Google indexing since July 2024)
- [ ] **`<meta name="author">`** — set to business or author name for E-E-A-T signals

### Open Graph (required)
```html
<meta property="og:title" content="Page Title (≤60 chars)">
<meta property="og:description" content="Page description (≤155 chars)">
<meta property="og:url" content="https://example.com/canonical-url/">
<meta property="og:type" content="website">
<meta property="og:image" content="https://example.com/images/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:site_name" content="Brand Name">
<meta property="og:locale" content="en_US">
```

### Twitter Card (required)
```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Page description">
<meta name="twitter:image" content="https://example.com/images/og-image.jpg">
<meta name="twitter:site" content="@yourtwitterhandle">
```

> **OG image rules:** 1200×630px minimum; host on your own domain with a descriptive filename (e.g. `san-antonio-handyman-og.jpg`, not `ChatGPT_Image_Apr_20.webp`); avoid external CDN or cloud storage URLs.

---

## 3. Structured Data / Schema

- [ ] **All JSON-LD must be in the static `<head>` — never JS-injected only**
  ```html
  <script type="application/ld+json">{ ... }</script>
  ```
- [ ] **Always use JSON-LD** — never Microdata or RDFa
- [ ] **Include `@context`, `@type`, and `@id`** on every schema block
- [ ] **Match schema type to business type:**
  - Local service business → `LocalBusiness` + relevant subtype (e.g. `Contractor`, `HomeAndConstructionBusiness`)
  - E-commerce → `Product`, `Offer`, `BreadcrumbList`
  - Blog/article → `Article`, `BlogPosting` with `author`, `datePublished`, `dateModified`
  - All sites → `WebSite` with `SearchAction` for sitelinks search box
  - All sites → `Organization` with `logo`, `contactPoint`, `sameAs`

### Minimum LocalBusiness schema for service businesses:
```json
{
  "@context": "https://schema.org",
  "@type": ["LocalBusiness", "Contractor"],
  "@id": "https://example.com/#business",
  "name": "Business Name",
  "url": "https://example.com",
  "telephone": "+1-555-000-0000",
  "email": "hello@example.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "City",
    "addressRegion": "TX",
    "postalCode": "78201",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 29.4241,
    "longitude": -98.4936
  },
  "openingHours": "Mo-Fr 08:00-18:00",
  "priceRange": "$$",
  "image": "https://example.com/images/logo.webp",
  "sameAs": [
    "https://www.google.com/maps/place/YOUR_GBP_ID",
    "https://www.facebook.com/yourpage",
    "https://www.instagram.com/yourhandle"
  ],
  "areaServed": ["City 1", "City 2", "City 3"]
}
```

- [ ] **NEVER use FAQPage schema on commercial sites** — restricted to government/healthcare since August 2023
- [ ] **NEVER use HowTo schema** — deprecated for rich results since September 2023
- [ ] **NEVER reference FID** — replaced by INP as of September 9, 2024
- [ ] **Validate with Google Rich Results Test** before launch: https://search.google.com/test/rich-results

---

## 4. Sitemap & `robots.txt`

### sitemap.xml
- [ ] **All `<loc>` values must be absolute URLs** — `https://example.com/page/`, not `/page/`
- [ ] **Include `<lastmod>` on every URL** in `YYYY-MM-DD` format
- [ ] **Include `<changefreq>` and `<priority>`** (optional but helpful)
- [ ] **Submit sitemap in Google Search Console** after launch
- [ ] **Reference sitemap in robots.txt** with the full absolute URL

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2026-05-10</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

### robots.txt
- [ ] **Include `Sitemap:` directive** with absolute URL
- [ ] **Explicitly manage AI crawlers** — do not leave them to inherit `*` rules

```txt
User-agent: *
Allow: /

# Major search engines
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# Social crawlers
User-agent: Twitterbot
Allow: /

User-agent: facebookexternalhit
Allow: /

# AI crawlers — explicit control
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

User-agent: anthropic-ai
Allow: /

User-agent: FacebookBot
Allow: /

User-agent: Amazonbot
Allow: /

Sitemap: https://example.com/sitemap.xml
```

---

## 5. Security Headers

Set all of these at the CDN/hosting layer (Cloudflare Transform Rules, Vercel headers, Nginx config):

| Header | Recommended Value |
|---|---|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` |
| `X-Frame-Options` | `SAMEORIGIN` |
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=()` |
| `Content-Security-Policy` | At minimum: `upgrade-insecure-requests` |

- [ ] All 6 headers present
- [ ] Verify with `security_headers.py` or https://securityheaders.com — target score **≥ 70/100**

---

## 6. Performance & Core Web Vitals

Target thresholds (Google "Good" band):

| Metric | Good | Needs Improvement | Poor |
|---|---|---|---|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5–4.0s | > 4.0s |
| INP (Interaction to Next Paint) | < 200ms | 200–500ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1–0.25 | > 0.25 |

> ⚠️ **INP replaced FID** on September 9, 2024. Never reference FID in audits or documentation.

- [ ] **Preload above-fold images and fonts:**
  ```html
  <link rel="preload" as="image" href="/images/hero.webp">
  <link rel="preload" as="font" href="/fonts/inter.woff2" crossorigin>
  ```
- [ ] **Lazy-load below-fold images:** `<img loading="lazy" ...>`
- [ ] **Split JS bundles** — no single monolithic bundle; use dynamic imports / code splitting
- [ ] **Serve images in modern formats** — WebP or AVIF; never ship uncompressed PNG/JPG for photos
- [ ] **Set explicit `width` and `height` on all `<img>` tags** — prevents layout shift (CLS)
- [ ] **Use a CDN** for static assets
- [ ] **Verify with PageSpeed Insights** before launch: https://pagespeed.web.dev — target mobile score ≥ 70

---

## 7. Images

- [ ] **Every `<img>` must have a descriptive `alt` attribute**
  - Describe what is shown: `alt="San Antonio handyman installing wood fence in Alamo Heights"`
  - Never: `alt=""` (unless purely decorative), `alt="image"`, `alt="photo"`
- [ ] **OG image hosted on your own domain** with a descriptive filename
  - ✅ `https://example.com/images/san-antonio-handyman-og.jpg`
  - ❌ `https://storage.googleapis.com/.../ChatGPT_Image_Apr_20.webp`
- [ ] **OG image dimensions declared** in meta tags: `og:image:width` = 1200, `og:image:height` = 630
- [ ] **Logo and favicon properly linked** — include `apple-touch-icon` and `favicon.ico`
- [ ] **Image filenames are descriptive and lowercase with hyphens** — `hero-kitchen-remodel.webp`, not `IMG_4892.jpg`

---

## 8. AI & GEO Search Readiness

- [ ] **Create and populate `llms.txt`** at domain root (e.g. `https://example.com/llms.txt`):
  ```
  # Business / Site Name
  > One-sentence description of what the site/business does.

  ## Key Pages
  - [Home](https://example.com/): Brief description
  - [Services](https://example.com/services/): What services are offered
  - [About](https://example.com/about/): Who we are
  - [Contact](https://example.com/contact/): How to reach us
  ```
- [ ] **Optionally create `llms-full.txt`** with expanded page summaries for complex sites
- [ ] **All AI crawlers explicitly managed** in `robots.txt` (see Section 4)
- [ ] **Structured data provides machine-readable facts** — name, address, hours, phone, services, service areas — so AI answer engines can cite your site accurately

---

## 9. E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)

> As of December 2025, E-E-A-T applies to **all competitive queries**, not just YMYL.

- [ ] **About / Team page** — include:
  - Owner or team member name + photo
  - Professional credentials, certifications, license numbers
  - Years of experience / founding date
  - Company mission or values
- [ ] **Author bios on blog/article pages** — link to author profile
- [ ] **Reviews / testimonials page or section** — link to Google reviews, include star ratings in schema (`aggregateRating`)
- [ ] **Contact page with physical address, phone, and email**
- [ ] **Privacy Policy and Terms of Service pages** — linked from footer on every page
- [ ] **Social proof links in footer** — Google Business Profile, Facebook, Instagram, LinkedIn as appropriate
- [ ] **License/certification information visible** for regulated industries (contractors, medical, legal, financial)

---

## 10. Local SEO (Service & Location-Based Businesses)

- [ ] **Google Business Profile claimed, verified, and complete** — link in footer and schema `sameAs`
- [ ] **Consistent NAP (Name, Address, Phone)** across website, GBP, and all directories
- [ ] **Service area pages have unique, substantial content** — minimum 300 words per city/neighbourhood page
  - Include: local landmarks, zip codes, neighbourhoods served, specific services in that area, local testimonial or project example
  - Never duplicate content between city pages
- [ ] **Per-city/location schema** on each service area page with `areaServed` scoped to that city
- [ ] **Location page limit** — warning at 30+ pages, hard stop at 50+ pages without genuinely unique content per page
- [ ] **Embed Google Map** on contact or location pages

---

## 11. Pre-Launch Verification Checklist

Run these before every site launch:

```bash
SKILL_DIR=/path/to/seo-skill/scripts

# Core checks
python3 $SKILL_DIR/fetch_page.py https://yourdomain.com --output /tmp/page.html
python3 $SKILL_DIR/parse_html.py /tmp/page.html --url https://yourdomain.com --json
  # ✅ Verify: h1 not empty, word_count > 300, canonical present, schema not empty

python3 $SKILL_DIR/robots_checker.py https://yourdomain.com
  # ✅ Verify: Status 200, sitemap referenced, AI crawlers managed

python3 $SKILL_DIR/redirect_checker.py https://yourdomain.com
  # ✅ Verify: 0 or 1 hop, final status 200

python3 $SKILL_DIR/security_headers.py https://yourdomain.com
  # ✅ Verify: score ≥ 70/100, all 6 headers present

python3 $SKILL_DIR/social_meta.py https://yourdomain.com
  # ✅ Verify: score ≥ 80/100, og:url present, og:title ≤ 60 chars

python3 $SKILL_DIR/llms_txt_checker.py https://yourdomain.com
  # ✅ Verify: score ≥ 70/100

python3 $SKILL_DIR/pagespeed.py https://yourdomain.com --strategy mobile
  # ✅ Verify: score ≥ 70
```

---

## Quick Reference Score Targets

| Check | Minimum Target |
|---|---|
| PageSpeed Insights (mobile) | ≥ 70 |
| Security headers score | ≥ 70 / 100 |
| Social meta score | ≥ 80 / 100 |
| `llms.txt` quality score | ≥ 70 / 100 |
| LCP | < 2.5s |
| INP | < 200ms |
| CLS | < 0.1 |
| `og:title` length | ≤ 60 chars |
| `<meta description>` length | 120–155 chars |
| Words per service/location page | ≥ 300 |

---

*Generated from SEO audit of missionspropertyservices.com — 2026-05-09*
