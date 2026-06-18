# Command Reference

Use these commands inside an agent that has the skill installed.

| Command | Purpose |
| --- | --- |
| `seo audit <url>` | Full website or page audit with scoring and reports. |
| `seo page <url>` | Deep single-page analysis. |
| `seo technical <url>` | Crawlability, indexability, security, URLs, mobile, Core Web Vitals, and rendering. |
| `seo content <url>` | Content quality, E-E-A-T, originality, and intent fit. |
| `seo schema <url>` | Schema.org JSON-LD detection, validation, and generation. |
| `seo sitemap <url>` | XML sitemap validation and sitemap generation guidance. |
| `seo images <url>` | Image SEO, dimensions, alt text, loading, and weight checks. |
| `seo geo <url>` | Generative Engine Optimization for AI search surfaces. |
| `seo aeo <url>` | Answer Engine Optimization for snippets, PAA, and answer blocks. |
| `seo programmatic <url>` | Programmatic SEO safeguards and quality gates. |
| `seo competitors <url>` | Comparison and competitor page analysis. |
| `seo hreflang <url>` | International SEO and hreflang validation. |
| `seo links <url>` | Internal links, external links, backlink quality, and anchor text. |
| `seo article <url>` | Article extraction and editorial SEO recommendations. |
| `seo github <owner/repo>` | GitHub repo SEO, README quality, metadata, topics, community health, and traffic archival. |
| `seo plan <topic-or-url>` | Strategic SEO plan using industry templates. |

## Generic Requests

When the user says something like:

```text
perform seo analysis on https://example.com
```

Treat it as a single-URL full audit and produce:

- `FULL-AUDIT-REPORT.md`
- `ACTION-PLAN.md`

If the HTML generator runs, also return the saved `SEO-REPORT.html` path.

## `seo plan` Industry Routing Examples

Use `seo plan <topic-or-url>` and route by detected business model:

- `seo plan https://example-tours.com` → Tour Operator / Tourism template (`resources/templates/tour-operator.md`)
- `seo plan https://example-plumber.com` → Local Service template (`resources/templates/local-service.md`)
- `seo plan https://example-saas.com` → SaaS template (`resources/templates/saas.md`)
