#!/usr/bin/env python3
"""Evidence-coverage-aware per-module scoring for marketing audit findings."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

MARKETING_BLOCKS = (
    "organic_search", "paid_media", "social_content", "marketplaces",
    "local_reputation", "funnel_analytics", "crm_retention", "compliance",
)
SEO_BLOCKS = (
    "technical", "yandex", "semantics", "content", "architecture",
    "analytics", "local", "authority",
)
PENALTY = {"critical": 35, "high": 18, "medium": 8, "low": 3}
APPLICABILITY = {"applicable", "not_applicable", "planned", "unknown"}
COVERAGE = {"complete", "partial", "unknown"}


def evaluate(document: Any, block_names: tuple[str, ...] = MARKETING_BLOCKS) -> dict[str, Any]:
    if isinstance(document, list):
        findings = document
        declared: dict[str, Any] = {}
    elif isinstance(document, dict):
        findings = document.get("findings", [])
        declared = document.get("blocks", {})
    else:
        raise ValueError("Input must be a JSON object or a findings list")
    if not isinstance(findings, list) or not all(isinstance(item, dict) for item in findings):
        raise ValueError("'findings' must be a list of JSON objects")
    if not isinstance(declared, dict):
        raise ValueError("'blocks' must be a JSON object keyed by block name")

    by_block: dict[str, list[dict[str, Any]]] = {name: [] for name in block_names}
    for item in findings:
        block = str(item.get("block", "")).strip().lower()
        if block in by_block:
            by_block[block].append(item)
    for name, block_doc in declared.items():
        if name not in by_block or not isinstance(block_doc, dict):
            continue
        local_findings = block_doc.get("findings", [])
        if isinstance(local_findings, list):
            by_block[name].extend(item for item in local_findings if isinstance(item, dict))

    result: dict[str, Any] = {}
    for name in block_names:
        block_doc = declared.get(name, {})
        if not isinstance(block_doc, dict):
            block_doc = {}
        applicability = str(block_doc.get("applicability", "unknown")).lower()
        coverage = str(block_doc.get("coverage", "unknown")).lower()
        if applicability not in APPLICABILITY:
            raise ValueError(f"Invalid applicability for {name}: {applicability}")
        if coverage not in COVERAGE:
            raise ValueError(f"Invalid coverage for {name}: {coverage}")
        observed = by_block[name]
        penalties = sum(PENALTY.get(str(f.get("severity", "medium")).lower(), 8) for f in observed)
        score = None
        if applicability == "applicable" and coverage == "complete":
            score = round(max(0, 100 - min(100, penalties)), 1)
        result[name] = {
            "applicability": applicability,
            "coverage": coverage,
            "score": score,
            "observed_findings": len(observed),
        }

    return {
        "schema_version": 1,
        "overall_score": None,
        "note": "No aggregate score. Per-block scores are shown only for applicable blocks with complete declared coverage.",
        "blocks": result,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", help="Findings JSON with explicit block applicability and coverage")
    parser.add_argument("--profile", choices=("marketing", "seo"), default="marketing")
    args = parser.parse_args()
    try:
        document = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
        blocks = SEO_BLOCKS if args.profile == "seo" else MARKETING_BLOCKS
        print(json.dumps(evaluate(document, blocks), ensure_ascii=False, indent=2))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
