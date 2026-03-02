# SEO Skill (Antigravity / Claude / Codex)

An LLM-first SEO analysis skill for agent IDEs, with 12 specialized sub-skills, 6 specialist agents, and optional utility scripts used as evidence collectors.

## IDE Compatibility

- Antigravity IDE (`.agent/skills/seo`)
- Claude Code (`~/.claude/skills/seo`)
- Codex (`~/.codex/skills/seo`)


## ✨ Features

| Sub-Skill | Description |
|-----------|-------------|
| `seo audit` | Full website audit with evidence-backed scoring |
| `seo article` | Article data extraction & LLM-driven content optimization |
| `seo page` | Deep single-page analysis |
| `seo technical` | Crawlability, indexability, security, Core Web Vitals, AI crawlers |
| `seo content` | Content quality & E-E-A-T assessment (Sept 2025 QRG) |
| `seo schema` | Schema.org detection, validation & JSON-LD generation |
| `seo sitemap` | XML sitemap analysis & generation |
| `seo images` | Image optimization audit (alt text, formats, lazy loading, CLS) |
| `seo geo` | Generative Engine Optimization — AI Overviews, ChatGPT, Perplexity |
| `seo aeo` | Answer Engine Optimization — Featured Snippets, PAA, Knowledge Panel |
| `seo links` | Link profile analysis — internal links, backlinks, anchor text, orphan pages |
| `seo programmatic` | Programmatic SEO safeguards & quality gates |
| `seo competitors` | Comparison & alternatives page generation |
| `seo hreflang` | International SEO / hreflang validation |
| `seo plan` | Strategic SEO planning with topical clusters & industry templates |

## 🧠 LLM-First Workflow

This skill is designed for reasoning-first SEO analysis:

1. Collect page evidence (`read_url_content` first, scripts optional).
2. Analyze with LLM using explicit proof for each finding.
3. Apply confidence labels (`Confirmed`, `Likely`, `Hypothesis`).
4. Prioritize by impact and effort.
5. Produce a structured action plan.

### Required Rubric

All audits should apply:
- `resources/references/llm-audit-rubric.md`

The rubric standardizes:
- evidence format (`Finding`, `Evidence`, `Impact`, `Fix`)
- severity (`Critical`, `Warning`, `Pass`, `Info`)
- confidence labeling
- output contract for audit reports

## 🤖 Specialist Agents

- **Technical SEO** — crawlability, indexability, security, mobile, JS rendering
- **Content Quality** — E-E-A-T scoring, AI content detection
- **Performance** — Core Web Vitals (LCP, INP, CLS) analysis
- **Schema Markup** — JSON-LD detection, validation, generation
- **Sitemap** — XML sitemap validation, quality gates
- **Visual Analysis** — screenshots, above-the-fold, responsiveness (Playwright)

## 📚 Reference Data (Updated Feb 2026)

- Core Web Vitals thresholds (INP replaced FID)
- E-E-A-T framework (Sept 2025 QRG + Dec 2025 core update)
- Schema.org types — active, restricted, deprecated
- Content quality gates & word count minimums
- Google SEO quick reference
- LLM audit rubric for consistent outputs

## 🏭 Industry Templates

Pre-built strategy templates for: **SaaS**, **E-commerce**, **Local Business**, **Publisher/Media**, **Agency**, and **Generic** businesses.

---

## 🔧 Installation (All IDEs)

### Quick Install Script (Antigravity / Claude / Codex)

```bash
# 1) Clone
git clone https://github.com/Bhanunamikaze/Agentic-SEO-Skill.git
cd Agentic-SEO-Skill

# 2) Install for your target
# Antigravity (project-local):
bash install.sh --target antigravity --project-dir /path/to/your/project

# Claude:
bash install.sh --target claude

# Codex:
bash install.sh --target codex

# Global user install (Claude + Codex):
bash install.sh --target global

# All targets (Antigravity + Claude + Codex):
bash install.sh --target all --project-dir /path/to/your/project

# Install from another local checkout:
bash install.sh --target codex --repo-path /path/to/Agentic-SEO-Skill
```

### Install directly from GitHub (remote source mode):

```bash
curl -fsSL https://raw.githubusercontent.com/Bhanunamikaze/Agentic-SEO-Skill/main/install.sh | \
  bash -s -- --target codex
```

### Manual Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Bhanunamikaze/Agentic-SEO-Skill.git
```

### Step 2: Install Python Dependencies

```bash
pip install requests beautifulsoup4
```

**Optional** — for visual analysis (screenshots & layout checks):
```bash
pip install playwright && playwright install chromium
```

### Step 3: Choose Target Directory (Manual Install)

If you prefer not to use `install.sh`, copy or symlink manually:

#### Antigravity IDE (project-local)

```bash
mkdir -p .agent/skills
cp -r /path/to/Agentic-SEO-Skill .agent/skills/seo
# or: ln -s /path/to/Agentic-SEO-Skill .agent/skills/seo
```

#### Claude Code (user-global)

```bash
mkdir -p ~/.claude/skills
cp -r /path/to/Agentic-SEO-Skill ~/.claude/skills/seo
# or: ln -s /path/to/Agentic-SEO-Skill ~/.claude/skills/seo
```

#### Codex (user-global)

```bash
mkdir -p ~/.codex/skills
cp -r /path/to/Agentic-SEO-Skill ~/.codex/skills/seo
# or: ln -s /path/to/Agentic-SEO-Skill ~/.codex/skills/seo
```

### Step 4: Verify Triggering

The skill will auto-trigger when you mention SEO-related keywords in your IDE. Try:

- *"Run an SEO audit on example.com"*
- *"Check the schema markup on my homepage"*
- *"Analyze Core Web Vitals for my site"*
- *"Create an SEO plan for my SaaS product"*

---

## 💬 Example Prompts (hackingdream.net)

### How Prompts Route to Agents & Scripts

Different prompts invoke different specialist agents and scripts. Here's how the skill decides:

| You type... | Scope | Agent(s) activated | Scripts used |
|-------------|-------|-------------------|--------------|
| "Run SEO audit" | 🌐 Full domain | **All 6 agents** (technical, content, schema, performance, sitemap, visual) | `parse_html.py`, `pagespeed.py`, `robots_checker.py`, `security_headers.py`, `broken_links.py`, `readability.py` |
| "Analyze this article" / blog post URL | 📄 Single page | **Content** + **Schema** + **Technical** | `article_seo.py`, `parse_html.py`, `readability.py` |
| "Check technical SEO" | 🔧 Technical only | **Technical** | `robots_checker.py`, `security_headers.py`, `redirect_checker.py`, `parse_html.py` |
| "Review content quality" / "E-E-A-T" | 📝 Content only | **Content** | `article_seo.py`, `readability.py`, `entity_checker.py` |
| "Check schema markup" | 🏷️ Schema only | **Schema** | `parse_html.py`, `validate_schema.py` |
| "Audit sitemap" | 🗺️ Sitemap only | **Sitemap** | `broken_links.py` |
| "Check page speed" / "Core Web Vitals" | ⚡ Performance only | **Performance** | `pagespeed.py` |
| "Take screenshots" / "mobile check" | 📱 Visual only | **Visual** | `capture_screenshot.py`, `analyze_visual.py` |
| "Check GEO readiness" / "AI search" | 🤖 GEO/AI only | **Technical** + **Content** | `llms_txt_checker.py`, `robots_checker.py`, `parse_html.py` |
| "Analyze links" / "backlink profile" | 🔗 Links only | **Technical** | `link_profile.py`, `internal_links.py`, `broken_links.py` |
| "Check hreflang" | 🌍 i18n only | **Technical** | `hreflang_checker.py` |
| "Create SEO plan" / "SEO strategy" | 📋 Strategy | None (LLM reasoning) | `competitor_gap.py` (optional) |
| "AEO analysis" / "Featured Snippets" | 🎯 AEO only | **Content** | `article_seo.py`, `parse_html.py` |
| "Entity SEO" / "Knowledge Graph" | 🏛️ Entity only | **Content** + **Schema** | `entity_checker.py`, `parse_html.py` |
| "Check IndexNow" | 📡 IndexNow only | **Technical** | `indexnow_checker.py` |
| "Find content gaps" / "competitor analysis" | 📊 Gap analysis | None (LLM reasoning) | `competitor_gap.py` |
| "Check for duplicates" / "thin content" | 📋 Dupe check | **Content** | `duplicate_content.py` |
| "GSC data" / "Search Console" | 📈 GSC only | None | `gsc_checker.py` |

### Domain vs URL vs Blog Post — What's Different?

| Input type | What happens | Example |
|-----------|-------------|---------|
| **Domain** (`hackingdream.net`) | Crawls multiple pages, checks robots.txt, sitemap, site-wide patterns | Full audit, link profile, sitemap check |
| **URL** (`hackingdream.net/page`) | Single page deep-dive: HTML, meta, schema, content, CWV | Page audit, schema check, technical check |
| **Blog post URL** | Article-specific: readability, keyword density, heading structure, JSON-LD `Article`/`BlogPosting` schema, publish date | Article analysis, AEO check |

---

### 🌐 Full Domain Audit

```text
Run a full SEO audit for https://hackingdream.net and prioritize fixes by impact.
```

### 📄 Single Page / Blog Post Analysis

```text
Analyze this article: https://www.hackingdream.net/2026/02/cobalt-strike-beacon-commands-red-team-field-guide.html
```

```text
Do a single-page SEO analysis of https://hackingdream.net and show critical issues first.
```

### 🔧 Technical SEO

```text
Analyze technical SEO for https://hackingdream.net (robots, crawlability, canonicals, redirects, headers).
```

### 📝 Content Quality & E-E-A-T

```text
Review content quality and E-E-A-T signals on https://hackingdream.net and suggest concrete rewrites.
```

### 🏷️ Schema Markup

```text
Check schema markup on https://hackingdream.net, validate errors, and generate corrected JSON-LD.
```

### ⚡ Performance & Core Web Vitals

```text
Run Core Web Vitals analysis on https://hackingdream.net and break down LCP subparts.
```

### 🤖 GEO / AI Search Readiness

```text
Evaluate GEO readiness for https://hackingdream.net (AI crawler access, llms.txt, citation structure).
```

### 🎯 Answer Engine Optimization (AEO)

```text
Analyze AEO signals for https://hackingdream.net — Featured Snippet targeting, PAA optimization, Knowledge Panel readiness.
```

### 🔗 Link Profile Analysis

```text
Analyze internal link structure and backlink profile for https://hackingdream.net.
```

### 🏛️ Entity SEO / Knowledge Graph

```text
Check entity SEO for https://hackingdream.net — Wikidata presence, sameAs links, Knowledge Graph signals.
```

### 📊 Competitor Topic Gap

```text
Find content gaps between https://hackingdream.net and competitors https://hackerone.com https://portswigger.net.
```

### 🌍 Hreflang / International SEO

```text
Validate hreflang implementation on https://hackingdream.net — BCP-47 tags, bidirectional links, x-default.
```

### 📡 IndexNow

```text
Check IndexNow implementation for https://hackingdream.net with key abc123def456.
```

### 📋 Topical Cluster Planning

```text
Create a topical authority cluster plan for https://hackingdream.net covering cybersecurity topics.
```

### 📈 Google Search Console (requires credentials)

```text
Pull GSC performance data for https://hackingdream.net and identify striking-distance keywords.
```

### 🗺️ Sitemap Audit

```text
Audit sitemap quality for https://hackingdream.net and flag missing, redirected, or noindex URLs.
```

### 🖼️ Image SEO

```text
Run image SEO checks for https://hackingdream.net (alt text, lazy loading, dimensions, format suggestions).
```

### 📋 Strategic SEO Plan

```text
Create a 6-month SEO strategy for https://hackingdream.net with milestones and KPIs.
```

### 📱 Visual / Mobile Analysis

```text
Take desktop and mobile screenshots of https://hackingdream.net and analyze above-the-fold content.
```

---

### Run Everything at Once

To run **all** analysis types on a single URL:

```text
Run a complete SEO audit on https://hackingdream.net — include technical, content, schema, performance,
links, GEO, AEO, entity SEO, and sitemap analysis. Provide a prioritized action plan.
```

Example generated outputs:
- `FULL-AUDIT-REPORT.md` — comprehensive findings
- `ACTION-PLAN.md` — prioritized fixes

![Example prompt and generated outputs](docs/images/example-prompt-output.png)

---

## 📊 Report Generation

You can generate reports in two ways:

1. **LLM-first report in your IDE (Antigravity / Claude / Codex)** (recommended for strategy + prioritization):

```text
Run a full SEO audit for https://hackingdream.net and produce a prioritized action plan with evidence for each finding.
```

2. **Interactive HTML dashboard** (recommended for shareable technical snapshots):

```bash
python3 scripts/generate_report.py "https://hackingdream.net" --output seo-report-hackingdream.html
```

The HTML report includes:
- overall score and category breakdown
- environment detection (platform/runtime inference)
- environment-specific fix plan
- section-level issues and recommendations
- readability "what to replace" suggestions

Example generated dashboard:

![SEO report dashboard example](docs/images/report-dashboard.png)

---

## ⚙️ Optional Script Workflow

Use scripts when you need additional verification or structured JSON outputs.

```bash
# Example target
URL="https://example.com"

# Fetch + parse HTML
python3 scripts/fetch_page.py "$URL" --output /tmp/page.html
python3 scripts/parse_html.py /tmp/page.html --url "$URL" --json

# Core checks
python3 scripts/robots_checker.py "$URL" --json
python3 scripts/llms_txt_checker.py "$URL" --json
python3 scripts/pagespeed.py "$URL" --strategy mobile --json
python3 scripts/security_headers.py "$URL" --json
python3 scripts/redirect_checker.py "$URL" --json
python3 scripts/social_meta.py "$URL" --json

# Content + structure checks
python3 scripts/readability.py /tmp/page.html --json
python3 scripts/internal_links.py "$URL" --depth 1 --max-pages 20 --json
python3 scripts/broken_links.py "$URL" --workers 5 --json
python3 scripts/article_seo.py "$URL" --json

# New analysis scripts
python3 scripts/hreflang_checker.py "$URL" --json
python3 scripts/entity_checker.py "$URL" --json
python3 scripts/duplicate_content.py "$URL" --json
python3 scripts/link_profile.py "$URL" --json
python3 scripts/competitor_gap.py "$URL" --competitor https://competitor.com --json
# python3 scripts/gsc_checker.py "$URL" --credentials creds.json --json  # requires GSC credentials
# python3 scripts/indexnow_checker.py "$URL" --key YOUR_KEY --json          # requires IndexNow key
```

Generate a single HTML dashboard if needed:

```bash
python3 scripts/generate_report.py "$URL"
```
---

## 🛡️ Critical Rules Enforced

| Rule | Detail |
|------|--------|
| **INP not FID** | FID removed Sept 2024. INP is the sole interactivity metric. |
| **FAQ schema restricted** | FAQPage only for government/healthcare authority sites (Aug 2023) |
| **HowTo deprecated** | Rich results removed Sept 2023 |
| **JSON-LD only** | Never recommend Microdata or RDFa |
| **E-E-A-T everywhere** | Applies to ALL competitive queries since Dec 2025 |
| **Mobile-first complete** | 100% mobile-first indexing since July 2024 |
| **Location page limits** | ⚠️ Warning at 30+ pages, 🛑 Hard stop at 50+ |

---

## 📋 Requirements

| Requirement | Version |
|-------------|---------|
| Python | 3.8+ |
| `requests` | Any |
| `beautifulsoup4` | Any |
| Playwright | Optional (for visual analysis) |

---

## 🙏 Credits

This project is heavily built from **[claude-seo](https://github.com/AgriciDaniel/claude-seo)** by **[AgriciDaniel](https://github.com/AgriciDaniel)**. All core SEO logic, reference data, agent definitions, utility scripts, and sub-skill instructions originate from that project.

This repository restructures and adapts the content to function as a compatible skill package for **Antigravity IDE**, **Claude Code**, and **Codex**, while preserving the same core skill layout (`SKILL.md` + `scripts/` + `resources/`).

---

## 📄 License

Licensed under the MIT License. See [LICENSE](LICENSE).

Portions are derived from [claude-seo](https://github.com/AgriciDaniel/claude-seo), which is also MIT-licensed.
