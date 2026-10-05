#!/usr/bin/env python3
"""Repair proven UTF-8-as-Latin-1 mojibake in text source files.

Run once during maintenance, then rely on validate_skill.py to prevent regressions.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

TEXT_EXTENSIONS = {".md", ".py", ".csv", ".json"}
# The sequences below identify UTF-8 bytes decoded as Windows-1251.
CYRILLIC_RUN = re.compile(r"[\u0400-\u04ff]+")


def mojibake_count(text: str) -> int:
    """Count only runs that can be losslessly decoded from Windows-1251 to UTF-8."""
    count = 0
    for run in CYRILLIC_RUN.findall(text):
        try:
            decoded = run.encode("cp1251").decode("utf-8")
        except UnicodeError:
            continue
        if decoded != run:
            count += 1
    return count


def repair(text: str) -> str:
    """Return repaired text only when the mojibake marker count decreases."""
    def fix_run(match: re.Match[str]) -> str:
        run = match.group(0)
        try:
            return run.encode("cp1251").decode("utf-8")
        except UnicodeError:
            return run
    candidate = CYRILLIC_RUN.sub(fix_run, text)
    return candidate if mojibake_count(candidate) < mojibake_count(text) else text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Report files needing repair without modifying them")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    changed: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_EXTENSIONS:
            continue
        text = path.read_text(encoding="utf-8")
        fixed = repair(text)
        if fixed == text:
            continue
        changed.append(path.relative_to(root))
        if not args.check:
            path.write_text(fixed, encoding="utf-8", newline="\n")
    for path in changed:
        print(path)
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
