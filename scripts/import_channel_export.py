#!/usr/bin/env python3
"""Normalize known columns in a local CSV/JSON channel export and preserve raw rows."""
from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

ALIASES = {
    "impressions": {"impressions", "показы", "показы рекламы"},
    "clicks": {"clicks", "клики", "переходы"},
    "spend": {"spend", "cost", "расход", "расходы", "затраты"},
    "visits": {"visits", "sessions", "визиты", "сеансы"},
    "leads": {"leads", "лиды", "заявки"},
    "orders": {"orders", "заказы"},
    "conversions": {"conversions", "конверсии"},
    "revenue": {"revenue", "выручка"},
    "returns": {"returns", "возвраты"},
}


def clean_header(value: Any) -> str:
    return re.sub(r"[\s_-]+", " ", str(value or "").strip().lower())


def number(value: Any) -> int | float | None:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    source = str(value).replace("\u00a0", " ").strip()
    if not source:
        return None
    source = source.replace(" ", "")
    source = re.sub(r"[^0-9,.-]", "", source)
    if source in {"", "-", ".", ","}:
        return None
    # Russian exports commonly use comma as the decimal separator. Preserve source text in raw.
    if "," in source and "." not in source:
        source = source.replace(",", ".")
    elif "," in source and "." in source:
        source = source.replace(",", "")
    try:
        value_num = float(source)
    except ValueError:
        return None
    return int(value_num) if value_num.is_integer() else value_num


def load_csv(path: Path) -> list[dict[str, Any]]:
    sample = path.read_text(encoding="utf-8-sig")[:8192]
    if not sample.strip():
        raise ValueError("CSV is empty")
    try:
        delimiter = csv.Sniffer().sniff(sample, delimiters=",;\t").delimiter
    except csv.Error:
        delimiter = ","
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row")
        return [dict(row) for row in reader if any(value not in (None, "") for value in row.values())]


def load_json(path: Path) -> list[dict[str, Any]]:
    document = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(document, dict):
        document = document.get("records", document.get("data", [document]))
    if not isinstance(document, list) or not all(isinstance(row, dict) for row in document):
        raise ValueError("JSON must be an object, a list of objects, or contain a records/data list")
    return document


def normalize_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    aliases = {alias: metric for metric, names in ALIASES.items() for alias in names}
    normalized = []
    for row in rows:
        metrics = {}
        for header, value in row.items():
            metric = aliases.get(clean_header(header))
            if metric:
                parsed = number(value)
                if parsed is not None:
                    metrics[metric] = parsed
        normalized.append({"metrics": metrics, "raw": row})
    return normalized


def valid_capture_time(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use ISO 8601 date/time, including timezone") from exc
    if parsed.tzinfo is None:
        raise argparse.ArgumentTypeError("Capture time must include a timezone offset")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Local .csv or .json export")
    parser.add_argument("--platform", required=True, help="Source platform label, e.g. yandex-direct or wildberries")
    parser.add_argument("--captured-at", required=True, type=valid_capture_time, help="ISO 8601 time with timezone")
    parser.add_argument("--period", default="UNKNOWN", help="Data period as supplied by the source")
    parser.add_argument("--out", default="channel-export.normalized.json")
    args = parser.parse_args()
    source = Path(args.input)
    output = Path(args.out)
    try:
        if source.resolve() == output.resolve():
            raise ValueError("Output path must differ from the source file")
        suffix = source.suffix.lower()
        if suffix == ".csv":
            rows = load_csv(source)
        elif suffix == ".json":
            rows = load_json(source)
        else:
            raise ValueError("Only local CSV and JSON files are supported")
        if not rows:
            raise ValueError("Export contains no data rows")
        records = normalize_rows(rows)
        recognized = sorted({key for record in records for key in record["metrics"]})
        output.parent.mkdir(parents=True, exist_ok=True)
        document = {
            "schema_version": 1,
            "source": {
                "platform": args.platform,
                "file_name": source.name,
                "format": suffix[1:],
                "captured_at": args.captured_at,
                "period": args.period,
            },
            "recognized_metrics": recognized,
            "row_count": len(records),
            "records": records,
            "limitations": [
                "Raw source columns and values are preserved; recognized metrics are best-effort aliases, not platform-independent definitions.",
                "Input must be aggregated and de-identified; this helper does not detect personal data.",
            ],
        }
        output.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, UnicodeDecodeError, csv.Error, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    print(f"Wrote {len(records)} records to {output}")
    print("No network access or platform writes were performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
