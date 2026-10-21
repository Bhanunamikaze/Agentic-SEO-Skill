# Agentic SEO Skill Wiki

Agentic SEO Skill is an LLM-first SEO audit toolkit for agent IDEs and AI coding assistants. It combines structured prompts, specialist workflows, and deterministic scripts so audits are evidence-backed instead of guesswork.

| At a glance | Current state |
|---|---|
| Latest release package | `v3.0.0` |
| Sub-skills | 16 |
| Specialist agents | 10 |
| Runtime scripts | 89 |
| Runtime package contents | `SKILL.md`, `scripts/`, `resources/` |
| Main deliverables | `FULL-AUDIT-REPORT.md`, `ACTION-PLAN.md`, `SEO-REPORT.html` |

## Start Here

| Goal | Go to | What you get |
|---|---|---|
| Install the skill | [[Installation]] | Target-specific install commands for Codex, Claude, Cursor, Windsurf, Copilot, Cline, Continue, and Antigravity. |
| Learn the commands | [[Command Reference]] | The `seo audit`, `seo page`, `seo technical`, `seo schema`, `seo github`, and related command map. |
| Copy a complete prompt | [[Example Prompts]] | Detailed prompts for full audits, articles, technical SEO, schema, GEO/AEO, local SEO, tour-operator strategy, ecommerce, and GitHub SEO. |
| Understand the audit flow | [[Audit Workflow]] | How evidence is collected, scored, verified, and turned into findings. |
| Generate reports | [[Reports and Outputs]] | Markdown reports, action plans, HTML dashboards, GitHub SEO reports, and report QA guidance. |
| Find a script | [[Script Inventory]] | Start-here script groups plus the full 89-script inventory. |
| Package or release | [[Release and Packaging]] | Runtime allowlist, release tags, and package contents. |
| Fix common failures | [[Troubleshooting]] | PageSpeed limits, Playwright issues, GitHub auth, inventory checks, and stale references. |

## Fast Path

### 1. Install for Codex

```bash
curl -fsSLO https://raw.githubusercontent.com/Bhanunamikaze/Agentic-SEO-Skill/main/install.sh
bash install.sh --online --ref v3.0.0 --target codex --force
```

### 2. Run a full audit prompt

```text
$seo audit https://example.com
```

Or use a detailed prompt:

```text
Run a full SEO audit for https://example.com.
Use direct page evidence and bundled scripts where available.
Create FULL-AUDIT-REPORT.md and ACTION-PLAN.md.
For every finding, include Evidence, Impact, Fix, Severity, Confidence, and Owner.
Prioritize fixes by impact and implementation effort.
```

### 3. Generate a dashboard

```bash
python3 ~/.codex/skills/seo/scripts/generate_report.py "https://example.com" --output SEO-REPORT.html
```

Example dashboard snapshot:

![SEO report dashboard example](https://raw.githubusercontent.com/Bhanunamikaze/Agentic-SEO-Skill/main/docs/images/report-dashboard.png)

## Choose the Right Workflow

| If you need... | Use this workflow | Primary outputs |
|---|---|---|
| A complete website audit | `seo audit <url>` | `FULL-AUDIT-REPORT.md`, `ACTION-PLAN.md`, optional `SEO-REPORT.html` |
| A tour operator growth plan | `seo plan <topic-or-url>` | Industry-routed strategy using the Tour Operator / Tourism template |
| A homepage or landing-page review | `seo page <url>` | Page-level findings and prioritized fixes |
| Technical crawl/indexability checks | `seo technical <url>` | Robots, sitemap, canonical, redirect, indexability, and status findings |
| Article optimization | `seo article <url>` | Content gaps, E-E-A-T issues, schema fixes, snippet opportunities |
| Schema validation and generation | `seo schema <url>` | JSON-LD findings and corrected schema |
| Core Web Vitals review | `seo technical <url>` or performance prompt | CWV evidence, LCP breakdown, implementation fixes |
| AI search readiness | `seo geo <url>` or `seo aeo <url>` | AI crawler policy, llms.txt, answer blocks, citation readiness |
| GitHub repository SEO | `seo github <owner/repo>` | `GITHUB-SEO-REPORT.md`, `GITHUB-ACTION-PLAN.md` |

## What Makes the Reports Useful

Every strong audit should separate proof from opinion:

- `Evidence`: exact page, HTML, script output, metric, or blocked data source.
- `Impact`: why the issue matters for crawling, indexing, ranking, UX, trust, or conversion.
- `Fix`: a concrete implementation step.
- `Severity`: `Critical`, `Warning`, `Pass`, or `Info`.
- `Confidence`: `Confirmed`, `Likely`, or `Hypothesis`.

This keeps reports useful for both strategy and implementation. Failed APIs, rate limits, missing credentials, and unsupported browser rendering should be listed as unknowns, not treated as confirmed site defects.

## What Is Inside

| Area | Examples |
|---|---|
| Technical SEO | robots.txt, AI crawler policies, sitemaps, canonicals, redirects, indexability, JS rendering, mobile checks |
| Content and E-E-A-T | readability, author/trust signals, topical coverage, duplicate/thin content, freshness, citations |
| Performance | PageSpeed, Core Web Vitals, LCP subparts, cache/compression, fonts, third-party scripts |
| Schema | JSON-LD validation, required properties, rich result risk checks, schema templates |
| Images and visual checks | image inventory, dimensions, LCP image behavior, screenshots, rendered visual audits |
| Links | internal links, broken links, anchors, external link quality, backlink reclaim |
| GEO and AEO | AI crawler access, llms.txt, citation readiness, answer blocks, snippet structure |
| GitHub SEO | README quality, repo metadata, topics, releases, search benchmark, competitor research |

## Source of Truth

The installed skill runtime is intentionally small:

- `SKILL.md`
- `scripts/`
- `resources/`

The repository also contains tests, CI, governance files, docs, and wiki source, but those are not required inside release skill bundles.

Use these pages for human documentation. Use `SKILL.md` and the files under `resources/` for runtime behavior.

## Maintenance Signals

The repo validates:

- Python script compilation
- Skill/agent/script inventory drift
- Reference freshness markers
- Focused regression tests for audit behavior

Reference files carry `<!-- Updated: YYYY-MM-DD -->` markers. Stale references are flagged for review so SEO rules and assumptions do not silently age out.
