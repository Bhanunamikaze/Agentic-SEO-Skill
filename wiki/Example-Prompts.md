# Example Prompts

Use these prompts when you want the SEO skill to run with clear scope, evidence requirements, and expected outputs. Replace placeholders such as `<url>`, `<domain>`, `<repo>`, `<keyword>`, and `<competitor>` before running.

## Prompt Pattern

A strong SEO prompt usually includes:

- Target: domain, page URL, article URL, or GitHub repository.
- Scope: full audit, technical SEO, schema, content, performance, links, GEO/AEO, or GitHub SEO.
- Evidence requirement: ask for specific proof from HTML, scripts, screenshots, APIs, or crawl data.
- Output format: ask for prioritized fixes, confidence labels, and report artifacts.
- Constraints: mention API limits, credentials, crawl depth, or pages to exclude when needed.

Example structure:

```text
Run <audit type> for <target>.
Use direct page evidence and bundled scripts where available.
Label every finding as Confirmed, Likely, or Hypothesis.
Prioritize fixes by impact and effort.
Create FULL-AUDIT-REPORT.md and ACTION-PLAN.md.
```

## Full Website Audit

Use this when you want the broadest site-level review.

```text
Run a full SEO audit for <domain>.

Scope:
- Crawl representative pages from the homepage, sitemap, and internal links.
- Check robots.txt, sitemap quality, indexability, canonicals, redirects, status codes, security headers, Core Web Vitals, schema, content quality, internal links, image SEO, GEO, and AEO.
- Use bundled scripts for evidence where execution is available.

Output:
- Create FULL-AUDIT-REPORT.md with findings grouped by Technical SEO, Content, Schema, Performance, Links, Images, GEO/AEO, and Unknowns.
- Create ACTION-PLAN.md with prioritized fixes sorted by impact and effort.
- For every finding, include Evidence, Impact, Fix, Severity, and Confidence.
- Do not treat API rate limits or blocked fetches as confirmed site issues.
```

## Single Page Audit

Use this for one important URL such as a homepage, product page, landing page, or service page.

```text
Run a single-page SEO audit for <url>.

Check:
- Title, meta description, canonical, robots directives, headings, internal links, schema, social metadata, images, readability, E-E-A-T, Core Web Vitals, and mobile rendering risks.
- Compare the visible page intent against this target query: <keyword>.

Output:
- Start with the top 10 highest-impact fixes.
- Include exact HTML or script evidence for each issue.
- Separate quick fixes from engineering fixes.
- Include a recommended title tag, meta description, H1, and schema improvements if needed.
```

## Blog Post or Article Audit

Use this when optimizing editorial content.

```text
Analyze this article for SEO, E-E-A-T, and answer readiness: <article-url>.

Target keyword: <keyword>
Search intent: <informational/commercial/investigational/local>

Review:
- Title, slug, meta description, H1/H2 structure, intro clarity, topical coverage, freshness, author signals, citations, internal links, image alt text, Article/BlogPosting schema, and answer-block formatting.
- Identify missing sections that would help satisfy search intent.
- Check whether the article can answer featured snippets, People Also Ask style questions, and AI answer citations.

Output:
- Give a rewrite plan for the title, meta description, intro, headings, FAQ-style answer blocks, and internal links.
- Include a content gap table with Missing Topic, Why It Matters, Suggested Section, and Priority.
- Label findings as Confirmed, Likely, or Hypothesis.
```

## Technical SEO Deep Dive

Use this when crawlability and indexability are the priority.

```text
Run a technical SEO audit for <domain>.

Focus on:
- robots.txt, AI crawler policies, XML sitemaps, canonical tags, noindex/nofollow directives, X-Robots-Tag headers, redirect chains, HTTP status codes, duplicate metadata, URL quality, crawl depth, orphan candidates, JavaScript rendering risks, mobile viewport, and security headers.

Use scripts where available:
- robots_checker.py
- sitemap_checker.py
- crawl_audit.py
- indexability_matrix.py
- redirect_checker.py
- x_robots_header_checker.py
- security_headers.py
- javascript_render_audit.py

Output:
- Produce an indexability matrix with URL, status, robots, meta robots, x-robots, canonical, sitemap presence, verdict, and fix.
- Prioritize issues that block crawling, indexing, rendering, or canonical consolidation.
```

## Schema Audit and JSON-LD Generation

Use this when structured data matters.

```text
Audit Schema.org markup for <url>.

Check:
- Existing JSON-LD syntax, @type choices, required properties, recommended properties, deprecated schema types, restricted rich result types, placeholder values, duplicate schema, and conflicts between page content and structured data.

Output:
- List existing schema types and validation issues.
- Explain whether each issue affects eligibility, trust, or enhancement quality.
- Generate corrected JSON-LD that matches the visible page content.
- Use JSON-LD only. Do not recommend Microdata or RDFa.
```

## Core Web Vitals and Performance

Use this when speed, UX, and CWV are the focus.

```text
Run Core Web Vitals and performance analysis for <url>.

Check:
- LCP, INP, CLS, TTFB, render-blocking resources, image weight, likely LCP image behavior, lazy loading mistakes, third-party scripts, cache headers, compression, font loading, and mobile rendering risks.

Output:
- Break down LCP into TTFB, resource delay, resource duration, and render delay where data allows.
- Separate lab data, field data, and unknowns.
- Give implementation-specific fixes for images, CSS, JavaScript, fonts, caching, and third-party scripts.
- If PageSpeed is rate-limited, continue with local evidence and mark affected findings as Hypothesis.
```

## Content Quality and E-E-A-T

Use this when content trust, helpfulness, and topical depth are weak points.

```text
Review content quality and E-E-A-T signals for <url>.

Target audience: <audience>
Primary query: <keyword>

Evaluate:
- Search intent match, originality, topical completeness, author expertise, citations, trust signals, contact/about signals, freshness, readability, thin content, duplicate content, internal links, and entity coverage.

Output:
- Provide a prioritized content improvement plan.
- Include rewrite examples for the intro, key headings, and weak paragraphs.
- Suggest internal links and supporting pages needed to build topical authority.
- Label every recommendation by impact, effort, and confidence.
```

## GEO and AI Search Readiness

Use this for AI Overviews, ChatGPT, Perplexity, Claude, and other answer engines.

```text
Evaluate GEO and AI search readiness for <domain>.

Check:
- robots.txt access for major AI crawlers, llms.txt availability, clear entity descriptions, concise answer blocks, citation-ready claims, source references, author signals, schema, sameAs links, topical authority, and pages likely to be quoted by AI systems.

Output:
- Identify blockers for AI crawler access and AI answer citation.
- Recommend pages or sections that should be rewritten into concise, citation-ready explanations.
- Suggest an llms.txt draft if missing.
- Separate confirmed crawler policy issues from strategic content recommendations.
```

## AEO and Featured Snippet Optimization

Use this when targeting direct answers, People Also Ask, and snippets.

```text
Run Answer Engine Optimization analysis for <url>.

Target questions:
- <question 1>
- <question 2>
- <question 3>

Check:
- Whether the page includes concise definitions, steps, tables, comparisons, FAQs where appropriate, summary blocks, and clear question-answer formatting.
- Whether headings match real user questions.
- Whether answers are supported by evidence and internal links.

Output:
- Recommend exact answer blocks to add or rewrite.
- Provide snippet-ready text for definitions, steps, lists, and comparison tables.
- Include the expected snippet type for each recommendation.
```

## Link Profile and Internal Linking

Use this when the issue is crawl depth, weak anchors, orphan pages, or link equity.

```text
Analyze link structure for <domain>.

Check:
- Internal link depth, orphan candidates, anchor text quality, broken links, redirects, external link quality, nofollow/sponsored/ugc usage, and important pages with too few internal links.

Output:
- Create a link action plan with Source Page, Target Page, Anchor Text, Reason, and Priority.
- Flag broken or redirected links separately from strategic internal-link opportunities.
- Identify pages that should become hubs or supporting spokes.
```

## Sitemap and Hreflang

Use this for large, international, or sitemap-heavy sites.

```text
Audit sitemap and hreflang implementation for <domain>.

Check:
- sitemap.xml discovery, sitemap index structure, URL limits, status codes, redirected URLs, noindex URLs, canonical mismatch, lastmod quality, hreflang tags, return tags, x-default, BCP-47 validity, and sitemap hreflang alternates.

Output:
- Report sitemap issues by severity.
- Produce hreflang findings with affected URL pairs and exact fix.
- Separate indexation blockers from hygiene warnings.
```

## Image SEO

Use this when visual assets affect rankings, accessibility, or performance.

```text
Run image SEO analysis for <url>.

Check:
- Missing or weak alt text, missing explicit dimensions, responsive image usage, srcset/sizes, lazy loading, likely LCP image behavior, image format, image weight, decorative images, and Next.js fill images.

Output:
- List each image issue with image URL, location if available, impact, and fix.
- Suggest improved alt text for meaningful images.
- Separate accessibility issues from performance issues.
```

## Local SEO

Use this for service-area businesses, stores, clinics, agencies, or local landing pages.

```text
Run local SEO analysis for <url>.

Business name: <business-name>
Primary location: <city-region-country>
Primary services: <services>

Check:
- NAP consistency, LocalBusiness schema, service area, location pages, reviews/testimonials, contact signals, map/embed usage, local landing page uniqueness, internal links, and trust signals.

Output:
- Provide fixes for local entity clarity, schema, page copy, and conversion trust.
- Flag doorway/location-page risks separately from normal local SEO improvements.
```

## Ecommerce and Product SEO

Use this for product detail pages, category pages, and collection pages.

```text
Audit ecommerce SEO for <url>.

Page type: <product/category/collection>

Check:
- Product or collection schema, price, availability, shipping, returns, reviews, variants, breadcrumbs, canonicalization, faceted navigation, product grid content, pagination, internal links, image quality, and thin category copy.

Output:
- Provide schema fixes and copy improvements.
- Flag faceted navigation crawl risks.
- Suggest category copy sections that improve uniqueness without hurting UX.
```

## Tour Operator / Tourism SEO Strategy

Use this for tour companies, excursion operators, private guide businesses, and destination-focused travel operators.

```text
Create a strategic SEO plan for this tour operator: <url-or-business-name>.

Business model: <day tours/multi-day packages/private tours/mixed>
Primary destinations: <destination list>
Core activities: <activity list>

Plan for:
- Destination hub architecture, tour pages, itinerary pages, availability/departure pages, pickup-location pages, and policy pages.
- Seasonal demand planning with pre-peak publishing windows.
- Conversion-critical page requirements (inclusions, exclusions, pricing, pickup, cancellation, safety, FAQs).
- Schema/entity recommendations for tour pages and operator trust signals.

Output:
- Recommend the top 20 pages to build or upgrade first.
- Provide a 90-day implementation roadmap with priorities by impact and effort.
- Include KPI targets for organic bookings, inquiry rate, and destination-query visibility.
```

## GitHub Repository SEO

Use this for repository discoverability on GitHub and search engines.

```text
Run GitHub SEO analysis for <owner/repo>.

Check:
- Repository name, description, topics, README quality, install clarity, examples, screenshots, releases, docs site, community health files, social preview readiness, GitHub search ranking signals, and competitor positioning.

Output:
- Create GITHUB-SEO-REPORT.md and GITHUB-ACTION-PLAN.md.
- Recommend a GitHub About description and topic list.
- Compare against these competitors if useful: <competitor-repo-1>, <competitor-repo-2>.
- Label each recommendation by impact, effort, and confidence.
```

## Repository Release SEO

Use this when preparing or reviewing a tagged release.

```text
Audit release SEO for <owner/repo> release <tag>.

Check:
- Release title, release notes, asset names, changelog clarity, install instructions, keywords, upgrade notes, and whether release assets contain only required runtime files.

Output:
- Give corrected release title and release notes if needed.
- Confirm whether package contents match the runtime allowlist.
- Identify any docs or install instructions that should be updated before publishing.
```

## Complete Audit With Strict Output Contract

Use this when you want a thorough final report.

```text
Run a complete SEO audit for <target>.

Mandatory scope:
- Technical SEO
- Content and E-E-A-T
- Schema
- Core Web Vitals
- Images
- Links
- Sitemap and indexability
- GEO and AEO
- Security/trust headers

Mandatory output:
- FULL-AUDIT-REPORT.md
- ACTION-PLAN.md
- Scorecard with category scores
- Top 10 fixes table
- Findings table with Evidence, Impact, Fix, Severity, Confidence, and Owner
- Unknowns table for checks blocked by rate limits, credentials, network, or rendering support

Rules:
- Use direct site evidence and bundled scripts where possible.
- Do not invent metrics when a data source fails.
- Do not mark a finding Confirmed unless the evidence directly supports it.
- Prioritize fixes that affect crawlability, indexability, CWV, trust, and conversion.
```
