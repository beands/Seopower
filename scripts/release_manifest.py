#!/usr/bin/env python3
"""Strict file allowlist for a publishable ru-seo-agent release."""
from __future__ import annotations

from pathlib import Path

ROOT_FILES = {
    "SKILL.md", "README.md", "LICENSE", ".gitignore",
    "install.ps1", "install.sh",
}
DIRECTORIES = {"references", "assets", "scripts"}
EXCLUDED_NAMES = {"__pycache__", ".pytest_cache", "client-profile.md"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".pem", ".key"}
EXCLUDED_PATHS = {"references/agent-adapters.md"}


def allowed_files(root: Path) -> list[Path]:
    """Return the exact release files, sorted and relative to *root*."""
    result: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.name in EXCLUDED_NAMES or path.suffix in EXCLUDED_SUFFIXES:
            continue
        relative = path.relative_to(root)
        if relative.as_posix() in EXCLUDED_PATHS or ".example." in path.name:
            continue
        if len(relative.parts) == 1:
            if relative.name in ROOT_FILES:
                result.append(relative)
        elif relative.parts[0] in DIRECTORIES:
            result.append(relative)
    return sorted(result)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    for file in allowed_files(root):
        print(file.as_posix())
