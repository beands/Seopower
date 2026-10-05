#!/usr/bin/env python3
"""Compatibility entry point for evidence-aware SEO module scoring."""
from __future__ import annotations

import sys

from marketing_score import main


if __name__ == "__main__":
    sys.argv[1:1] = ["--profile", "seo"]
    raise SystemExit(main())
