# 🚀 SEO Skill (Antigravity / Claude / Codex)

An LLM-first SEO analysis skill for agent IDEs, with 12 specialized sub-skills, 6 specialist agents, and optional utility scripts used as evidence collectors.

## ✅ IDE Compatibility

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
| `seo programmatic` | Programmatic SEO safeguards & quality gates |
| `seo competitors` | Comparison & alternatives page generation |
| `seo hreflang` | International SEO / hreflang validation |
| `seo plan` | Strategic SEO planning with industry-specific templates |

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

Or install directly from GitHub (remote source mode):

```bash
curl -fsSL https://raw.githubusercontent.com/Bhanunamikaze/Agentic-SEO-Skill/main/install.sh | \
  bash -s -- --target codex
```

Use a different repository URL (for forks or repo rename):

```bash
curl -fsSL https://raw.githubusercontent.com/Bhanunamikaze/Agentic-SEO-Skill/main/install.sh | \
  bash -s -- --target codex --source remote --repo-url https://github.com/<you>/Agentic-SEO-Skill.git
```

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

Use these directly in Antigravity, Claude, or Codex:

```text
Run a full SEO audit for https://hackingdream.net and prioritize fixes by impact.
```

```text
Do a single-page SEO analysis of https://hackingdream.net and show critical issues first.
```

```text
Analyze technical SEO for https://hackingdream.net (robots, crawlability, canonicals, redirects, headers).
```

```text
Review content quality and E-E-A-T signals on https://hackingdream.net and suggest concrete rewrites.
```

```text
Check schema markup on https://hackingdream.net, validate errors, and generate corrected JSON-LD.
```

```text
Audit sitemap quality for https://hackingdream.net and flag missing, redirected, or noindex URLs.
```

```text
Run image SEO checks for https://hackingdream.net (alt text, lazy loading, dimensions, format suggestions).
```

```text
Evaluate GEO readiness for https://hackingdream.net (AI crawler access, llms.txt, citation structure).
```

```text
Create a 6-month SEO strategy for https://hackingdream.net with milestones and KPIs.
```

```text
Analyze https://hackingdream.net as an article/homepage content target and propose before/after copy improvements.
```

Example run + output artifacts in an IDE session:

- Prompt: `perform SEO analysis on hackingdream.net`
- Generated outputs: `FULL-AUDIT-REPORT.md` and `ACTION-PLAN.md`

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
```

Generate a single HTML dashboard if needed:

```bash
python3 scripts/generate_report.py "$URL"
```

---

## 🧪 Local Validation

From `seo-skill/`:

```bash
# Script syntax validation
python3 -m py_compile scripts/*.py
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
