#!/usr/bin/env python3
from pathlib import Path
import argparse, shutil

p = argparse.ArgumentParser()
p.add_argument("--out", default="client-profile.md")
p.add_argument("--force", action="store_true")
a = p.parse_args()

root = Path(__file__).resolve().parents[1]
src = root/"assets"/"client-profile.template.md"
dst = Path(a.out).resolve()
if dst.exists() and not a.force:
    raise SystemExit(f"Refusing to overwrite {dst}; use --force")
dst.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(src, dst)
print(dst)
