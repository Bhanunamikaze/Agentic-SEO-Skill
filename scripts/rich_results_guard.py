#!/usr/bin/env python3
"""Guardrail checks for rich-result eligibility and retired schema types."""

from __future__ import annotations

import argparse
import json
from typing import Any

from schema_required_props import extract_schema_documents, find_schema_nodes, schema_type_names
from seo_common import issue, print_json_or_text


DEPRECATED_TYPES = {
    "SpecialAnnouncement": "retired as a Google rich result on July 31, 2025",
    "CourseInfo": "retired in June 2025",
    "EstimatedSalary": "retired in June 2025",
    "LearningVideo": "retired in June 2025",
    "ClaimReview": "fact-check rich results discontinued in 2025",
    "VehicleListing": "vehicle listing structured data discontinued in 2025",
    "PracticeProblem": "rich result discontinued in late 2025",
    "Dataset": "rich result discontinued in late 2025",
}

RESTRICTED_TYPES = {
    "FAQPage": "no longer shown as a rich result for any site (7 May 2026); markup still valid",
    "HowTo": "no longer broadly shown as a Google rich result",
}

RICH_RESULT_REQUIRED = {
    "BreadcrumbList": {"itemListElement"},
    "Product": {"name", "offers"},
    "Review": {"itemReviewed", "reviewRating", "author"},
    "VideoObject": {"name", "description", "thumbnailUrl", "uploadDate"},
}


def guard_rich_results(documents: list[Any]) -> dict[str, Any]:
    rows = []
    issues = []
    for row in find_schema_nodes(documents):
        node = row["node"]
        type_names = schema_type_names(node.get("@type"))
        row_issues = []
        for type_name in type_names:
            if type_name in DEPRECATED_TYPES:
                row_issues.append(issue("error", f"{type_name} is deprecated/restricted: {DEPRECATED_TYPES[type_name]}", evidence=row["path"]))
            if type_name in RESTRICTED_TYPES:
                row_issues.append(issue("warning", f"{type_name} has eligibility limits: {RESTRICTED_TYPES[type_name]}", evidence=row["path"]))
            for prop in sorted(RICH_RESULT_REQUIRED.get(type_name, set())):
                if not node.get(prop):
                    row_issues.append(issue("error", f"{type_name} missing rich-result property '{prop}'", evidence=row["path"]))
        rows.append({"path": row["path"], "types": type_names, "issues": row_issues})
        issues.extend(row_issues)
    return {
        "nodes": len(rows),
        "rows": rows,
        "issues": issues,
        "summary": {
            "errors": sum(1 for item in issues if item["severity"] == "error"),
            "warnings": sum(1 for item in issues if item["severity"] == "warning"),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Warn about rich-result eligibility risks in JSON-LD")
    parser.add_argument("source", help="URL, HTML file, or JSON-LD file")
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON")
    args = parser.parse_args()
    documents, meta = extract_schema_documents(args.source, timeout=args.timeout)
    result = guard_rich_results(documents)
    result.update({"source": args.source, "final_url": meta["final_url"]})
    lines = [
        f"Rich results guard for {args.source}",
        f"Nodes: {result['nodes']}  Errors: {result['summary']['errors']}  Warnings: {result['summary']['warnings']}",
    ] + [f"[{item['severity']}] {item['message']} {item.get('evidence') or ''}" for item in result["issues"][:30]]
    print_json_or_text(result, args.json, lines)


if __name__ == "__main__":
    main()
