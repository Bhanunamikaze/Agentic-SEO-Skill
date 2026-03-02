---
name: seo
description: >
  LLM-first SEO analysis and optimization for websites, blog posts, and
  business pages. Performs full audits, single-page reviews, technical SEO
  checks (crawlability, indexability, Core Web Vitals with INP), structured
  data detection/validation/generation, content quality and E-E-A-T assessment,
  sitemap and hreflang validation, image optimization, programmatic SEO
  safeguards, competitor page strategy, and GEO optimization for AI Overviews,
  ChatGPT, and Perplexity. Uses scripts as optional evidence collectors while
  keeping reasoning, prioritization, and recommendations in the LLM. Trigger on
  "SEO", "audit", "schema", "Core Web Vitals", "E-E-A-T", "technical SEO",
  "page speed", "structured data", "hreflang", "programmatic SEO", "GEO", "AI
  Overviews", "competitor pages", or "SEO plan".
---

# SEO Skill — Antigravity IDE

LLM-first SEO analysis skill with 12 specialized sub-skills and 6 specialist agents for complete website and blog optimization.

## Available Commands

| Command | Sub-Skill | Description |
|---------|-----------|-------------|
| `seo audit <url>` | [seo-audit](resources/skills/seo-audit.md) | Full website audit with scoring |
| `seo page <url>` | [seo-page](resources/skills/seo-page.md) | Deep single-page analysis |
| `seo technical <url>` | [seo-technical](resources/skills/seo-technical.md) | Technical SEO checks |
| `seo content <url>` | [seo-content](resources/skills/seo-content.md) | Content quality & E-E-A-T |
| `seo schema <url>` | [seo-schema](resources/skills/seo-schema.md) | Schema detection/validation/generation |
| `seo sitemap <url>` | [seo-sitemap](resources/skills/seo-sitemap.md) | Sitemap analysis & generation |
| `seo images <url>` | [seo-images](resources/skills/seo-images.md) | Image optimization audit |
| `seo geo <url>` | [seo-geo](resources/skills/seo-geo.md) | AI search optimization (GEO) |
| `seo programmatic <url>` | [seo-programmatic](resources/skills/seo-programmatic.md) | Programmatic SEO safeguards |
| `seo competitors <url>` | [seo-competitor-pages](resources/skills/seo-competitor-pages.md) | Comparison/alternatives pages |
| `seo hreflang <url>` | [seo-hreflang](resources/skills/seo-hreflang.md) | International SEO validation |
| `seo plan <url>` | [seo-plan](resources/skills/seo-plan.md) | Strategic SEO planning |
| `seo article <url>` | [seo-article](resources/skills/seo-article.md) | Article data extraction & LLM optimization |

---

## Orchestration Logic

When the user requests SEO analysis, follow this routing:

### Step 1 — Identify the Task

Parse the user's request to determine which sub-skill(s) to activate:

- **Full audit**: Read `resources/skills/seo-audit.md` — crawl multiple pages, delegate to agents, score and report
- **Single page**: Read `resources/skills/seo-page.md` — deep dive on one URL
- **Specific area**: Read the matching `resources/skills/seo-*.md` file
- **Strategic plan**: Read `resources/skills/seo-plan.md` and the matching `resources/templates/*.md` for the detected industry

### Step 2 — Collect Evidence

**Primary method** — use the built-in `read_url_content` tool:
```
read_url_content(url)  →  returns parsed HTML content directly
```
Use this as the default source of evidence.

**Fallback** — use utility scripts only when you need raw HTML, headers, or structured JSON outputs:
```bash
# Step 1: Fetch page HTML to a file
python3 <SKILL_DIR>/scripts/fetch_page.py <url> --output /tmp/page.html

# Step 2: Parse the saved HTML for SEO data
python3 <SKILL_DIR>/scripts/parse_html.py /tmp/page.html --url <url> --json
```

> **Note**: `parse_html.py` accepts a file path (not a URL). Fetch first, then parse.
> `<SKILL_DIR>` = absolute path to this skill directory (the folder containing this SKILL.md).

### Step 3 — Perform LLM-First Analysis

Use the LLM as the primary SEO analyst:

1. Synthesize evidence from page content, metadata, and optional script outputs.
2. Produce findings with explicit proof:
   - `Finding`
   - `Evidence` (specific element, metric, or snippet)
   - `Impact` (why it matters for ranking/indexing/UX)
   - `Fix` (clear implementation step)
3. Prioritize by impact and implementation effort.
4. Separate confirmed issues, likely issues, and unknowns (missing data).

Always read and apply `resources/references/llm-audit-rubric.md` to keep scoring, severity, confidence, and output structure consistent across audit types.

### Step 4 — Run Targeted Verification Scripts (Optional)

Use scripts to validate uncertain findings or enrich evidence. Do not replace LLM reasoning with script-only scoring.

```bash
# Check robots.txt and AI crawler management
python3 <SKILL_DIR>/scripts/robots_checker.py <url>

# Check llms.txt for AI search readiness
python3 <SKILL_DIR>/scripts/llms_txt_checker.py <url>

# Get Core Web Vitals from PageSpeed Insights (free API, no key needed)
python3 <SKILL_DIR>/scripts/pagespeed.py <url> --strategy mobile

# Check security headers (HSTS, CSP, X-Frame-Options, etc.)
python3 <SKILL_DIR>/scripts/security_headers.py <url>

# Detect broken links on a page (404s, timeouts, connection errors)
python3 <SKILL_DIR>/scripts/broken_links.py <url> --workers 5

# Trace redirect chains, detect loops and mixed HTTP/HTTPS
python3 <SKILL_DIR>/scripts/redirect_checker.py <url>

# Analyze readability from fetched HTML (Flesch-Kincaid, grade level, sentence stats)
python3 <SKILL_DIR>/scripts/readability.py /tmp/page.html --json

# Validate Open Graph and Twitter Card meta tags
python3 <SKILL_DIR>/scripts/social_meta.py <url>

# Analyze internal link structure, find orphan pages
python3 <SKILL_DIR>/scripts/internal_links.py <url> --depth 1 --max-pages 20

# Extract article content and perform keyword research for LLM-driven optimization
python3 <SKILL_DIR>/scripts/article_seo.py <url> --keyword "<optional_target_keyword>" --json
```

**Visual analysis** (requires Playwright — use `conda activate pentest` if available):
```bash
# Capture screenshots (desktop, laptop, tablet, mobile)
python3 <SKILL_DIR>/scripts/capture_screenshot.py <url> --all

# Analyze visual layout, above-the-fold, mobile responsiveness
python3 <SKILL_DIR>/scripts/analyze_visual.py <url> --json
```

**HTML Report Generator** — generates a self-contained interactive HTML dashboard:
```bash
# Generate full SEO report (runs scripts automatically, saves HTML to PWD)
python3 <SKILL_DIR>/scripts/generate_report.py <url>
python3 <SKILL_DIR>/scripts/generate_report.py <url> --output custom-report.html
```

### Step 5 — Delegate to Specialist Agents

For comprehensive audits, read the relevant agent file from `resources/agents/` to adopt the specialist role:

| Agent | File | Focus Area |
|-------|------|------------|
| Technical SEO | [seo-technical.md](resources/agents/seo-technical.md) | Crawlability, indexability, security, URLs, mobile, CWV, JS rendering |
| Content Quality | [seo-content.md](resources/agents/seo-content.md) | E-E-A-T assessment, content metrics, AI content detection |
| Performance | [seo-performance.md](resources/agents/seo-performance.md) | Core Web Vitals (LCP, INP, CLS), optimization recommendations |
| Schema Markup | [seo-schema.md](resources/agents/seo-schema.md) | Detection, validation, generation of JSON-LD structured data |
| Sitemap | [seo-sitemap.md](resources/agents/seo-sitemap.md) | XML sitemap validation, generation, quality gates |
| Visual Analysis | [seo-visual.md](resources/agents/seo-visual.md) | Screenshots, above-the-fold, responsiveness, layout |

### Step 6 — Apply Quality Gates

Reference the quality standards in `resources/references/`:

- **Content minimums**: Read [quality-gates.md](resources/references/quality-gates.md) for word counts, unique content %, title/meta requirements
- **Schema validation**: Read [schema-types.md](resources/references/schema-types.md) for active/deprecated/restricted types
- **Core Web Vitals**: Read [cwv-thresholds.md](resources/references/cwv-thresholds.md) for current metric thresholds
- **E-E-A-T framework**: Read [eeat-framework.md](resources/references/eeat-framework.md) for scoring criteria
- **Google reference**: Read [google-seo-reference.md](resources/references/google-seo-reference.md) for quick reference
- **LLM report rubric**: Read [llm-audit-rubric.md](resources/references/llm-audit-rubric.md) for mandatory evidence format, confidence labels, and output contract

### Step 7 — Score and Report

Use numeric scores as guidance, not as a replacement for evidence quality and judgment.

#### Default Scoring Weights (Full Audit)
| Category | Weight |
|----------|--------|
| Technical SEO | 25% |
| Content Quality | 25% |
| Schema Markup | 15% |
| Performance (CWV) | 15% |
| Image Optimization | 10% |
| AI Search Readiness (GEO) | 10% |

> If using `scripts/generate_report.py`, the automated dashboard uses script-level category weights defined in that script. Keep the narrative audit LLM-first and evidence-first.

#### Score Interpretation
| Score | Rating |
|-------|--------|
| 90-100 | Excellent |
| 70-89 | Good |
| 50-69 | Needs Improvement |
| 30-49 | Poor |
| 0-29 | Critical |

---

## Industry Detection

When running `seo plan`, detect the business type and load the matching template:

| Industry | Template File |
|----------|---------------|
| SaaS / Software | [saas.md](resources/templates/saas.md) |
| Local Service Business | [local-service.md](resources/templates/local-service.md) |
| E-commerce / Retail | [ecommerce.md](resources/templates/ecommerce.md) |
| Publisher / Media | [publisher.md](resources/templates/publisher.md) |
| Agency / Consultancy | [agency.md](resources/templates/agency.md) |
| Other / Generic | [generic.md](resources/templates/generic.md) |

**Detection signals:**
- SaaS: pricing page, feature pages, /docs, /api, trial/demo CTAs
- Local: address, phone, Google Business Profile, service area pages
- E-commerce: product pages, cart, checkout, /collections, /categories
- Publisher: article dates, author pages, /news, high content volume
- Agency: case studies, /work, /portfolio, team pages, service offerings

---

## Schema Templates

Pre-built JSON-LD templates are available in [templates.json](resources/schema/templates.json) for:
- **Common**: BlogPosting, Article, Organization, LocalBusiness, BreadcrumbList, WebSite (with SearchAction)
- **Video**: VideoObject, BroadcastEvent, Clip, SeekToAction
- **E-commerce**: ProductGroup (variants), OfferShippingDetails, Certification
- **Other**: SoftwareSourceCode, ProfilePage (E-E-A-T author pages)

---

## Validation Scripts

Two validation scripts are available for CI/CD integration:

### Pre-commit SEO Check
```bash
bash <SKILL_DIR>/scripts/pre_commit_seo_check.sh
```
Checks staged HTML files for: placeholder text in schema, title tag length, missing alt text, deprecated schema types, FID references (should be INP), meta description length.

### Schema Validator
```bash
python3 <SKILL_DIR>/scripts/validate_schema.py <file_path>
```
Validates JSON-LD blocks in HTML files: JSON syntax, @context/@type presence, placeholder text, deprecated/restricted types.

---

## Output Format

All sub-skill reports should use consistent severity levels:
- 🔴 **Critical** — Directly impacts rankings or indexing (fix immediately)
- ⚠️ **Warning** — Optimization opportunity (fix within 1 month)
- ✅ **Pass** — Meets or exceeds standards
- ℹ️ **Info** — Not applicable or informational only

Structure reports as:
1. Summary table with element, value, and severity
2. Detailed findings grouped by category
3. Actionable recommendations ordered by impact

---

## Critical Rules

1. **INP not FID** — FID was removed September 9, 2024. The sole interactivity metric is INP (Interaction to Next Paint). Never reference FID.
2. **FAQ schema is restricted** — FAQPage schema is limited to government and healthcare authority sites only (August 2023). Do NOT recommend for commercial sites.
3. **HowTo schema is deprecated** — Rich results fully removed September 2023. Never recommend.
4. **JSON-LD only** — Always use `<script type="application/ld+json">`. Never recommend Microdata or RDFa.
5. **E-E-A-T everywhere** — As of December 2025, E-E-A-T applies to ALL competitive queries, not just YMYL.
6. **Mobile-first is complete** — 100% mobile-first indexing since July 5, 2024.
7. **Location page limits** — Warning at 30+ pages, hard stop at 50+ pages. Enforce unique content requirements.
8. **AI crawler management** — Check robots.txt for GPTBot, ClaudeBot, PerplexityBot, Applebot-Extended, Google-Extended, Bytespider, CCBot.
9. **Use `read_url_content` first** — Prefer the built-in tool for primary evidence. Use scripts only to validate or enrich evidence.

---

## Dependencies

### Optional Script Dependencies
- Python 3.8+
- `requests` (for network analysis scripts)
- `beautifulsoup4` (for HTML parsing scripts)
- Playwright (for `capture_screenshot.py` and `analyze_visual.py`)
  ```bash
  pip install playwright && playwright install chromium
  ```
  Or if using conda: `conda activate pentest` (if Playwright is pre-installed)

### Install Script Dependencies
```bash
pip install requests beautifulsoup4
```
