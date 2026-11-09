# Script Inventory

The README shows only the most-used scripts. This wiki page is the full script inventory for Agentic SEO Skill `v3.0.0`, with purpose notes kept in one place for maintainers and users who need deeper coverage.

The skill ships 89 runtime scripts. The authoritative inventory check is:

```bash
python3 scripts/validate_skill_inventory.py
```

Expected result:

```text
Inventory: 16 skills, 10 agents, 89 scripts (88 Python + 1 shell)
OK: documented inventory matches files on disk.
```

## Start Here

| Need | Start with |
|---|---|
| Full site/page audit | `audit_runner.py`, `generate_report.py` |
| Raw page evidence | `fetch_page.py`, `parse_html.py` |
| Technical SEO | `crawl_audit.py`, `indexability_matrix.py`, `robots_checker.py`, `sitemap_checker.py` |
| Core Web Vitals | `pagespeed.py`, `lcp_subparts.py`, `lighthouse_runner.py` |
| Content quality | `readability.py`, `article_seo.py`, `eeat_signal_checker.py` |
| Schema | `validate_schema.py`, `schema_required_props.py`, `schema_template_generator.py` |
| Images and rendering | `image_inventory.py`, `image_weight_audit.py`, `analyze_visual.py` |
| Links | `internal_links.py`, `broken_links.py`, `anchor_text_audit.py` |
| GitHub repository SEO | `github_seo_report.py`, `github_repo_audit.py`, `github_readme_lint.py` |
| Report QA | `finding_verifier.py` |

## Full List

| Script | Purpose |
|---|---|
| `a11y_seo_checker.py` | Check accessibility signals that affect SEO and UX, including headings, labels, alt text, landmarks, contrast, and tap targets. |
| `ai_crawler_policy_matrix.py` | Compare robots.txt and AI crawler directives for GPTBot, ClaudeBot, PerplexityBot, Google-Extended, and other AI crawlers. |
| `analyze_visual.py` | Analyze rendered layout, mobile responsiveness, and above-the-fold visual SEO signals. |
| `anchor_text_audit.py` | Audit internal anchor text quality, diversity, empty anchors, and exact-match overuse. |
| `answer_block_scanner.py` | Detect answer-ready definitions, ordered steps, tables, lists, and featured-snippet formatting opportunities. |
| `article_seo.py` | Extract article content, detect CMS patterns, and produce article optimization evidence. |
| `audit_runner.py` | Orchestrate JSON, HTML, full audit markdown, and action-plan artifacts from one audit command. |
| `broken_links.py` | Check internal and external page links for broken, redirected, and timed-out targets. |
| `cache_compression_checker.py` | Check cache, compression, ETag, Vary, and immutable asset headers. |
| `canonical_checker.py` | Validate canonical targets, self-canonicals, cross-domain canonicals, and canonical consistency across URL sets. |
| `capture_screenshot.py` | Capture desktop and mobile screenshots with Playwright. |
| `citation_readiness.py` | Evaluate factual claims, citations, source quality, and AI-answer citation readiness. |
| `collection_page_checker.py` | Audit ecommerce collection/category pages for copy, pagination, filter crawlability, and product-grid signals. |
| `competitor_gap.py` | Compare competitor topics and headings to identify content gaps. |
| `content_decay_detector.py` | Analyze exported performance rows for declining pages and striking-distance opportunities. |
| `content_intent_matcher.py` | Compare title, headings, meta, and body sections against a target keyword and search intent. |
| `crawl_audit.py` | Crawl a site with sitemap seeds and depth limits to identify status codes, metadata duplication, crawl depth, and orphan candidates. |
| `critical_request_chain.py` | Detect render-blocking CSS/JS, preconnect/preload opportunities, and critical request risks. |
| `duplicate_content.py` | Detect thin or near-duplicate pages with similarity and word-count checks. |
| `eeat_signal_checker.py` | Check author, editorial, contact, citation, and experience signals for E-E-A-T reviews. |
| `entity_checker.py` | Check entity SEO signals across schema, Wikidata, Wikipedia, and Knowledge Graph inputs. |
| `env_loader.py` | Load local `.env` values for scripts that need optional API credentials. |
| `external_link_quality.py` | Audit external link status, redirects, rel attributes, and low-trust patterns. |
| `faceted_nav_audit.py` | Detect crawl traps and parameter explosion patterns in sort, filter, search, and faceted navigation URLs. |
| `fetch_page.py` | Fetch a URL to local HTML with SEO crawler headers and error handling. |
| `finding_verifier.py` | Deduplicate, prioritize, and validate findings before final reporting. |
| `font_audit.py` | Audit font loading, font-display, preload hints, external font hosts, and FOIT/FOUT risk. |
| `freshness_checker.py` | Check visible and structured published/modified dates, stale claims, and freshness mismatches. |
| `generate_report.py` | Run analysis scripts and generate a self-contained HTML SEO dashboard. |
| `github_api.py` | Shared GitHub API and provider fallback helpers for repository SEO scripts. |
| `github_community_health.py` | Check GitHub community profile and trust artifacts. |
| `github_competitor_research.py` | Build GitHub competitor intelligence and README pattern gaps. |
| `github_readme_lint.py` | Score README quality for GitHub search visibility and conversion. |
| `github_repo_audit.py` | Audit repository metadata, trust signals, topics, and discoverability basics. |
| `github_search_benchmark.py` | Benchmark repository visibility for GitHub search queries. |
| `github_seo_report.py` | Combine repository SEO checks into markdown report and action-plan artifacts. |
| `github_traffic_archiver.py` | Archive GitHub traffic snapshots before the 14-day window expires. |
| `github_weekly_scorecard.py` | Build weekly GitHub SEO score snapshots from repository, release, docs, and traffic artifacts. |
| `gsc_checker.py` | Pull Search Console performance, crawl, and sitemap data with credentials. |
| `hreflang_checker.py` | Validate hreflang implementation, return tags, x-default, and sitemap signals. |
| `hreflang_sitemap_validator.py` | Validate hreflang annotations across sitemap indexes and XML sitemap alternates. |
| `image_inventory.py` | Inventory images for alt text, dimensions, lazy/eager loading, srcset, sizes, and potential LCP candidates. |
| `image_weight_audit.py` | Estimate image weight, dimensions, format, responsive image, and LCP image risks. |
| `indexability_matrix.py` | Produce per-URL indexability verdicts from status, robots, meta robots, x-robots, canonical, and sitemap signals. |
| `indexnow_checker.py` | Validate and optionally ping IndexNow configuration. |
| `internal_links.py` | Analyze internal link structure, anchors, depth, and orphan-page candidates. |
| `javascript_render_audit.py` | Compare raw HTML and rendered DOM SEO signals when Playwright rendering is available, or through the Firecrawl API with `--renderer firecrawl`. |
| `lcp_subparts.py` | Break down LCP risk into TTFB, resource delay, resource duration, and render delay signals. |
| `lighthouse_runner.py` | Run local Lighthouse when available and return structured performance, SEO, accessibility, and best-practice scores. |
| `link_profile.py` | Build internal/external link profile evidence and optional GSC link data. |
| `llms_txt_checker.py` | Check `/llms.txt` availability and format for AI search readiness. |
| `llms_txt_generator.py` | Generate a clean `/llms.txt` draft from a site title, description, and priority URLs. |
| `local_seo_checker.py` | Check NAP, LocalBusiness schema, service area, reviews, map/embed, and GBP-style local signals. |
| `log_file_analyzer.py` | Analyze server logs for crawler hits, status patterns, wasted crawl, and crawl-budget signals. |
| `mobile_render_checker.py` | Check mobile viewport, fixed-width, sticky element, horizontal-scroll, tap-target, and clipped-text risks. |
| `orphan_pages_from_sitemap.py` | Compare crawl-discovered URLs against sitemap URLs to identify orphan candidates. |
| `pagespeed.py` | Fetch Core Web Vitals and performance data from PageSpeed Insights. |
| `parse_html.py` | Extract SEO-relevant HTML elements from a fetched or local page. |
| `pre_commit_seo_check.sh` | Shell pre-commit helper for schema, title, alt, and deprecated-metric checks. |
| `product_schema_checker.py` | Validate Product, Offer, price, availability, shipping, returns, variants, and rating schema signals. |
| `readability.py` | Compute readability, sentence, paragraph, and word-count metrics. |
| `redirect_backlink_reclaim.py` | Analyze backlink exports for 404 targets and long redirect chains that need reclaim work. |
| `redirect_checker.py` | Trace redirect chains, loops, mixed protocol hops, and chain length. |
| `reference_freshness.py` | Validate freshness markers in reference markdown files. |
| `repo_docs_site_checker.py` | Check repository homepage/docs URL availability, docs metadata, and install CTA paths. |
| `repo_file_inventory.py` | Inventory README, license, docs, examples, workflows, and governance files for GitHub SEO. |
| `repo_release_seo.py` | Analyze release cadence, release titles, changelog quality, and keyword-aligned release notes. |
| `repo_social_preview_checker.py` | Check GitHub social preview readiness, description, topics, and share-preview metadata. |
| `repo_topic_suggester.py` | Suggest repository topics from README/package signals and competitor/search-intent terms. |
| `review_schema_checker.py` | Check Review/AggregateRating markup for policy risks, misuse, and missing required fields. |
| `rich_results_guard.py` | Warn on deprecated, restricted, or risky rich-result schema types. |
| `robots_checker.py` | Parse robots.txt and AI crawler access policies. |
| `robots_path_tester.py` | Test specific URL paths against robots.txt rules for search and AI crawler user agents. |
| `schema_diff.py` | Compare current schema against recommended schema and output structured differences. |
| `schema_required_props.py` | Validate required and recommended schema properties across common rich-result types. |
| `schema_template_generator.py` | Generate JSON-LD templates for common page and entity types. |
| `security_headers.py` | Check HTTPS and security headers that influence trust and UX. |
| `seo_common.py` | Shared URL, fetch, HTML, sitemap, and CLI helpers used by core SEO automation scripts. |
| `sitemap_checker.py` | Discover, parse, and validate XML sitemaps, sitemap indexes, URL limits, status codes, and lastmod quality. |
| `sitemap_generator.py` | Generate valid sitemap XML from stdin, URL lists, or crawl exports. |
| `social_meta.py` | Validate Open Graph and Twitter Card metadata. |
| `third_party_script_audit.py` | Identify heavy third-party scripts, analytics/ad tags, blocking scripts, and main-thread risk. |
| `topical_cluster_mapper.py` | Map hub/spoke relationships, topic coverage, and internal-link gaps across URL or content lists. |
| `url_quality.py` | Audit URL quality signals such as slug length, uppercase paths, duplicate variants, parameters, and trailing slashes. |
| `validate_schema.py` | Validate JSON-LD syntax, required fields, placeholders, and deprecated schema. |
| `validate_skill_inventory.py` | Validate documented skill, agent, and script counts against files on disk. |
| `video_schema_checker.py` | Validate VideoObject schema, thumbnails, transcripts, upload date, duration, and embed indexability. |
| `visual_regression_snapshot.py` | Capture or compare visual regression snapshots across desktop, tablet, and mobile viewports. |
| `x_robots_header_checker.py` | Inspect X-Robots-Tag headers for noindex, nofollow, noarchive, and snippet directives. |
