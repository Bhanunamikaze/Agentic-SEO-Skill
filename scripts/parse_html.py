#!/usr/bin/env python3
"""
Parse HTML and extract SEO-relevant elements.

Usage:
    python parse_html.py page.html
    python parse_html.py page.html --url https://example.com
    python parse_html.py --fetch https://example.com --json
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Optional
from urllib.parse import urljoin, urlparse

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: beautifulsoup4 required. Install with: pip install beautifulsoup4")
    sys.exit(1)

try:
    from lib.safe_http import safe_get
except ImportError:
    from scripts.lib.safe_http import safe_get


def _fetch_url(url: str, timeout: int = 20) -> dict[str, Any]:
    """Fetch HTML for direct parsing."""
    response = safe_get(
        url,
        timeout=timeout,
        headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
    )
    return {
        "url": response.url,
        "content": response.text,
        "headers": dict(response.headers),
        "status_code": response.status_code,
    }


def _schema_items(schema_data: Any) -> list[dict[str, Any]]:
    """Flatten top-level JSON-LD objects and @graph nodes for validation."""
    if isinstance(schema_data, list):
        items: list[dict[str, Any]] = []
        for item in schema_data:
            items.extend(_schema_items(item))
        return items
    if not isinstance(schema_data, dict):
        return []
    items = [schema_data]
    graph = schema_data.get("@graph")
    if isinstance(graph, list):
        items.extend([node for node in graph if isinstance(node, dict)])
    return items


def _rel_contains(value: Any, token: str) -> bool:
    if not value:
        return False
    if isinstance(value, str):
        values = value.lower().split()
    else:
        values = [str(item).lower() for item in value]
    return token in values


def _is_responsive_fill_image(img) -> bool:
    if img.get("data-nimg") == "fill":
        return True
    style = re.sub(r"\s+", "", (img.get("style") or "").lower())
    return "position:absolute" in style and "width:100%" in style and "height:100%" in style


def parse_html(
    html: str,
    base_url: Optional[str] = None,
    headers: Optional[dict[str, Any]] = None,
) -> dict:
    """
    Parse HTML and extract SEO-relevant elements.

    Args:
        html: HTML content to parse
        base_url: Base URL for resolving relative links

    Returns:
        Dictionary with extracted SEO data
    """
    soup = BeautifulSoup(html, "lxml" if "lxml" in sys.modules else "html.parser")
    headers = headers or {}
    header_lookup = {str(k).lower(): v for k, v in headers.items()}

    result = {
        "title": None,
        "meta_description": None,
        "meta_robots": None,
        "x_robots_tag": header_lookup.get("x-robots-tag"),
        "canonical": None,
        "lang": None,
        "charset": None,
        "viewport": None,
        "favicon": None,
        "h1": [],
        "h2": [],
        "h3": [],
        "h4": [],
        "h5": [],
        "h6": [],
        "images": [],
        "links": {
            "internal": [],
            "external": [],
        },
        "pagination": {
            "prev": None,
            "next": None,
        },
        "resource_hints": {
            "preload": [],
            "preconnect": [],
            "dns-prefetch": [],
            "prefetch": [],
            "prerender": [],
        },
        "schema": [],
        "open_graph": {},
        "twitter_card": {},
        "word_count": 0,
        "hreflang": [],
    }

    html_tag = soup.find("html")
    if html_tag:
        result["lang"] = html_tag.get("lang")

    # Title
    title_tag = soup.find("title")
    if title_tag:
        result["title"] = title_tag.get_text(strip=True)

    # Meta tags
    for meta in soup.find_all("meta"):
        name = meta.get("name", "").lower()
        property_attr = meta.get("property", "").lower()
        content = meta.get("content", "")

        if name == "description":
            result["meta_description"] = content
        elif name == "robots":
            result["meta_robots"] = content
        elif name == "viewport":
            result["viewport"] = content

        if meta.get("charset"):
            result["charset"] = meta.get("charset")
        elif meta.get("http-equiv", "").lower() == "content-type":
            charset_match = re.search(r"charset=([^;\s]+)", content, re.I)
            if charset_match:
                result["charset"] = charset_match.group(1)

        # Open Graph
        if property_attr.startswith("og:"):
            result["open_graph"][property_attr] = content

        # Twitter Card
        if name.startswith("twitter:"):
            result["twitter_card"][name] = content

    # Canonical
    canonical = soup.find("link", rel="canonical")
    if canonical:
        href = canonical.get("href")
        result["canonical"] = urljoin(base_url, href) if base_url and href else href

    for icon in soup.find_all("link"):
        rel = icon.get("rel")
        if icon.get("href") and (
            _rel_contains(rel, "icon")
            or _rel_contains(rel, "shortcut")
            or _rel_contains(rel, "apple-touch-icon")
        ):
            result["favicon"] = urljoin(base_url, icon.get("href")) if base_url else icon.get("href")
            break

    # Hreflang
    for link in soup.find_all("link", rel="alternate"):
        hreflang = link.get("hreflang")
        if hreflang:
            result["hreflang"].append({
                "lang": hreflang,
                "href": urljoin(base_url, link.get("href", "")) if base_url else link.get("href"),
            })

    for rel_name in ("prev", "next"):
        page_link = soup.find("link", rel=rel_name)
        if page_link and page_link.get("href"):
            href = page_link.get("href")
            result["pagination"][rel_name] = urljoin(base_url, href) if base_url else href

    for rel_name in result["resource_hints"]:
        for link in soup.find_all("link", rel=rel_name):
            href = link.get("href")
            if href:
                result["resource_hints"][rel_name].append({
                    "href": urljoin(base_url, href) if base_url else href,
                    "as": link.get("as"),
                    "type": link.get("type"),
                    "crossorigin": link.get("crossorigin"),
                })

    # Headings
    for tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        for heading in soup.find_all(tag):
            text = heading.get_text(strip=True)
            if text:
                result[tag].append(text)

    # Images
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if base_url and src:
            src = urljoin(base_url, src)
        is_responsive_fill = _is_responsive_fill_image(img)

        result["images"].append({
            "src": src,
            "alt": img.get("alt"),
            "width": img.get("width"),
            "height": img.get("height"),
            "is_responsive_fill": is_responsive_fill,
            "loading": img.get("loading"),
        })

    # Links
    if base_url:
        base_domain = urlparse(base_url).netloc

        for a in soup.find_all("a", href=True):
            href = a.get("href", "")
            if not href or href.startswith("#") or href.startswith("javascript:"):
                continue

            full_url = urljoin(base_url, href)
            parsed = urlparse(full_url)

            link_data = {
                "href": full_url,
                "text": a.get_text(strip=True)[:100],
                "rel": a.get("rel", []),
            }

            if parsed.netloc == base_domain:
                result["links"]["internal"].append(link_data)
            else:
                result["links"]["external"].append(link_data)

    # Schema (JSON-LD) — enhanced with type validation
    DEPRECATED_SCHEMA = {
        "HowTo", "SpecialAnnouncement", "CourseInfo", "EstimatedSalary",
        "LearningVideo", "ClaimReview", "VehicleListing", "PracticeProblems",
    }
    RESTRICTED_SCHEMA = {"FAQPage"}  # no rich result since 7 May 2026; markup still valid

    for script in soup.find_all("script", type="application/ld+json"):
        try:
            schema_data = json.loads(script.string)
        except (json.JSONDecodeError, TypeError):
            result["schema"].append({
                "error": "invalid_json",
                "raw_snippet": (script.string or "")[:120],
            })
            continue

        items = _schema_items(schema_data)
        for item in items or [{}]:
            schema_type = item.get("@type", "Unknown")
            if isinstance(schema_type, list):
                schema_types = schema_type
                primary_type = next((t for t in schema_type if isinstance(t, str)), "Unknown")
            else:
                schema_types = [schema_type]
                primary_type = schema_type

            status = "active"
            note = ""

            if primary_type in DEPRECATED_SCHEMA:
                status = "deprecated"
                note = f"{primary_type} was deprecated/removed from rich results. Remove or replace."
            elif primary_type in RESTRICTED_SCHEMA:
                status = "restricted"
                note = f"{primary_type}: FAQPage no longer produces rich results for any site (Google removed them on 7 May 2026). The markup is NOT deprecated and may stay — it still helps answer engines parse the page."

            result["schema"].append({
                "@type": primary_type,
                "@types": schema_types,
                "@id": item.get("@id"),
                "@context": item.get("@context", schema_data.get("@context", "") if isinstance(schema_data, dict) else ""),
                "status": status,
                "note": note,
                "has_context": bool(item.get("@context") or (isinstance(schema_data, dict) and schema_data.get("@context"))),
                "has_type": bool(item.get("@type")),
                "from_graph": item is not schema_data,
                "raw": item,
            })

    # Word count (visible text only)
    for element in soup(["script", "style", "nav", "footer", "header"]):
        element.decompose()

    text = soup.get_text(separator=" ", strip=True)
    words = re.findall(r"\b\w+\b", text)
    result["word_count"] = len(words)

    return result


def main():
    parser = argparse.ArgumentParser(description="Parse HTML for SEO analysis")
    parser.add_argument("file", nargs="?", help="HTML file to parse")
    parser.add_argument("--url", "-u", help="Base URL for resolving links")
    parser.add_argument("--fetch", help="Fetch and parse a URL directly")
    parser.add_argument("--timeout", "-t", type=int, default=20, help="Fetch timeout in seconds")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    headers = {}
    final_url = args.url

    if args.fetch:
        try:
            fetched = _fetch_url(args.fetch, timeout=args.timeout)
        except Exception as exc:
            print(f"Error fetching {args.fetch}: {exc}", file=sys.stderr)
            sys.exit(1)
        if fetched.get("error"):
            print(f"Error fetching {args.fetch}: {fetched['error']}", file=sys.stderr)
            sys.exit(1)
        html = fetched.get("content") or ""
        headers = fetched.get("headers") or {}
        final_url = args.url or fetched.get("url") or args.fetch
    elif args.file:
        real_path = os.path.realpath(args.file)
        if not os.path.isfile(real_path):
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(real_path, "r", encoding="utf-8") as f:
            html = f.read()
    else:
        html = sys.stdin.read()

    result = parse_html(html, final_url, headers=headers)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Title: {result['title']}")
        print(f"Meta Description: {result['meta_description']}")
        print(f"Canonical: {result['canonical']}")
        print(f"H1 Tags: {len(result['h1'])}")
        print(f"H2 Tags: {len(result['h2'])}")
        print(f"Images: {len(result['images'])}")
        print(f"Internal Links: {len(result['links']['internal'])}")
        print(f"External Links: {len(result['links']['external'])}")
        print(f"Schema Blocks: {len(result['schema'])}")
        print(f"Word Count: {result['word_count']}")


if __name__ == "__main__":
    main()
