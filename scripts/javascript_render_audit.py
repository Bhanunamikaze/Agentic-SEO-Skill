#!/usr/bin/env python3
"""Compare raw HTML against rendered DOM SEO elements when Playwright or Firecrawl is available.

By default the rendered DOM comes from a local Playwright browser. With
`--renderer firecrawl` the audited URL is sent to the Firecrawl scrape API
instead, using `FIRECRAWL_API_KEY` (shell env or `.env`, see `env_loader.py`).
"""

from __future__ import annotations

import argparse
import json
import time

import requests
from env_loader import get_env
from seo_common import fetch_url, load_html, parse_html

try:
    from lib.safe_http import SafeHTTPError, assert_safe_url, safe_post
except ImportError:
    from scripts.lib.safe_http import SafeHTTPError, assert_safe_url, safe_post

FIRECRAWL_SCRAPE_URL = "https://api.firecrawl.dev/v2/scrape"
FIRECRAWL_RETRY_STATUSES = {408, 429, 500, 502, 503, 504}
FIRECRAWL_MAX_ERROR_CHARS = 300


def summarize(html: str, url: str) -> dict:
    parsed = parse_html(html, url)
    return {
        "title": parsed["title"],
        "meta_description": parsed["meta_description"],
        "canonical": parsed["canonical"],
        "h1_count": len(parsed["headings"]["h1"]),
        "internal_link_count": len([l for l in parsed["links"] if url and l["href"].startswith(url.split("/", 3)[0] + "//" + url.split("/")[2])]) if url.startswith("http") else len(parsed["links"]),
        "schema_count": len(parsed["schema"]),
        "word_count": parsed["word_count"],
    }


def render_with_playwright(url: str, timeout_ms: int) -> tuple[str | None, str | None]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None, "playwright not installed"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=timeout_ms)
            html = page.content()
            browser.close()
            return html, None
    except Exception as exc:  # noqa: BLE001 - CLI should report environment/browser errors
        return None, str(exc)


def render_with_firecrawl(url: str, timeout_ms: int, max_attempts: int = 2) -> tuple[str | None, str | None]:
    api_key = get_env("FIRECRAWL_API_KEY")
    if not api_key:
        return None, "FIRECRAWL_API_KEY not set"
    try:
        url = assert_safe_url(url)
    except SafeHTTPError as exc:
        return None, f"not sent to firecrawl: {exc}"
    timeout_ms = min(max(timeout_ms, 1000), 300000)
    payload = {
        "url": url,
        "formats": ["rawHtml"],
        "maxAge": 0,
        "timeout": timeout_ms,
        "origin": "agentic-seo-skill",
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    error = None
    delay = 3.0
    for attempt in range(max_attempts):
        if attempt:
            time.sleep(delay)
        try:
            resp = safe_post(
                FIRECRAWL_SCRAPE_URL,
                headers=headers,
                json=payload,
                timeout=timeout_ms / 1000 + 15,
                allow_redirects=False,
            )
        except requests.exceptions.Timeout:
            error = f"firecrawl request timed out after {timeout_ms / 1000 + 15:.0f}s"
            delay = 3.0
            continue
        except requests.exceptions.RequestException as exc:
            return None, f"firecrawl request failed: {exc}"[:FIRECRAWL_MAX_ERROR_CHARS]
        try:
            body = resp.json()
        except ValueError:
            body = {}
        if not isinstance(body, dict):
            body = {}
        if resp.status_code != 200:
            error = f"firecrawl HTTP {resp.status_code}: {body.get('error') or 'request failed'}"[:FIRECRAWL_MAX_ERROR_CHARS]
            if resp.status_code not in FIRECRAWL_RETRY_STATUSES:
                return None, error
            try:
                delay = min(max(float(resp.headers.get("Retry-After", 3)), 0.0), 30.0)
            except (TypeError, ValueError):
                delay = 3.0
            continue
        html = (body.get("data") or {}).get("rawHtml")
        if not html:
            return None, "firecrawl returned no rawHtml"
        return html, None
    return None, error


def render_page(url: str, timeout_ms: int, renderer: str = "auto") -> tuple[str | None, str | None, str | None]:
    if renderer == "firecrawl":
        html, error = render_with_firecrawl(url, timeout_ms)
        return html, error, "firecrawl" if html else None
    html, error = render_with_playwright(url, timeout_ms)
    if html:
        return html, None, "playwright"
    if renderer == "auto" and get_env("FIRECRAWL_API_KEY"):
        error = f"{error}; pass --renderer firecrawl to render with Firecrawl"
    return None, error, None


def audit(source: str, timeout: int = 15, render_timeout: int = 30000, renderer: str = "auto") -> dict:
    raw_html, final_url, fetched = load_html(source, timeout=timeout)
    raw = summarize(raw_html, final_url or source)
    rendered_html = None
    render_error = None
    used_renderer = None
    if final_url.startswith("http"):
        rendered_html, render_error, used_renderer = render_page(final_url, render_timeout, renderer)
    else:
        render_error = "rendering requires an http(s) URL"
    rendered = summarize(rendered_html, final_url) if rendered_html else None
    diffs = []
    if rendered:
        for key in raw:
            if raw.get(key) != rendered.get(key):
                diffs.append({"field": key, "raw": raw.get(key), "rendered": rendered.get(key)})
    return {"url": final_url or source, "raw": raw, "rendered": rendered, "diffs": diffs, "renderer": used_renderer, "render_error": render_error, "fetch_error": fetched.get("error")}


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare raw HTML and rendered DOM SEO signals")
    parser.add_argument("source", help="URL or local HTML file")
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument(
        "--render-timeout",
        type=int,
        default=30000,
        help="Render timeout in ms (Firecrawl accepts 1000-300000; values outside are clamped)",
    )
    parser.add_argument(
        "--renderer",
        choices=["auto", "playwright", "firecrawl"],
        default="auto",
        help="auto/playwright: local Playwright browser. firecrawl: sends the URL to the Firecrawl API "
        "(needs FIRECRAWL_API_KEY)",
    )
    parser.add_argument("--json", "-j", action="store_true")
    args = parser.parse_args()
    result = audit(args.source, args.timeout, args.render_timeout, args.renderer)
    print(json.dumps(result, indent=2) if args.json else f"Diffs: {len(result['diffs'])}; renderer={result['renderer']}; render_error={result['render_error']}")


if __name__ == "__main__":
    main()
