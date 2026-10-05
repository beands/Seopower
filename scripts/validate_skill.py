#!/usr/bin/env python3
from pathlib import Path
import re, sys
from repair_mojibake import mojibake_count
root=Path(__file__).resolve().parents[1]
try:
    text=(root/"SKILL.md").read_text(encoding="utf-8")
except UnicodeDecodeError as exc:
    print(f"ERROR: SKILL.md is not valid UTF-8: {exc}")
    sys.exit(1)
errors=[]; warnings=[]
if not text.startswith("---\n"): errors.append("Missing YAML frontmatter")
m=re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$",text)
name=m.group(1) if m else None
if not name: errors.append("Missing/invalid name")
elif root.name!=name: warnings.append(f"Directory {root.name} != skill name {name}; package must be installed as {name}")
if name and (len(name)>64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",name)): errors.append("Name violates Agent Skills spec")
m=re.search(r'(?m)^description:\s*"([^"]+)"\s*$',text)
if not m: errors.append("Missing single-line description")
elif len(m.group(1))>1024: errors.append("Description >1024 chars")
lines=text.count("\n")+1
if lines>500: warnings.append(f"SKILL.md {lines} lines; recommended <=500")
refs=set(re.findall(r"`((?:references|assets|scripts|integrations)/[^`\s]+)",text))
for ref in refs:
    if not (root/ref).exists(): errors.append(f"Missing referenced path: {ref}")
if "\ufffd" in text: errors.append("SKILL.md contains Unicode replacement characters")
if mojibake_count(text): errors.append("SKILL.md contains UTF-8-as-Windows-1251 mojibake")
for path in ("references/external-audit-review.md", "assets/external-audit-review.template.md"):
    if not (root / path).exists(): errors.append(f"Missing external-audit-review asset: {path}")
for path in (
    "references/marketing-channels.md",
    "references/funnel-analytics.md",
    "references/reputation-compliance.md",
    "assets/marketing-audit.template.md",
    "assets/marketing-action-plan.template.md",
    "scripts/marketing_score.py",
    "scripts/import_channel_export.py",
):
    if not (root / path).exists(): errors.append(f"Missing marketing audit asset: {path}")
for required in ("ACTIVE", "PLANNED", "NOT_USED", "NOT_APPLICABLE", "UNKNOWN"):
    if required not in text: errors.append(f"Missing channel status from SKILL.md: {required}")
for path in root.rglob("*"):
    if not path.is_file() or path.suffix not in {".md", ".py", ".csv", ".json"}:
        continue
    try:
        contents = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"Not valid UTF-8: {path.relative_to(root)}")
        continue
    if "\ufffd" in contents: errors.append(f"Replacement character: {path.relative_to(root)}")
    if mojibake_count(contents): errors.append(f"Mojibake: {path.relative_to(root)}")
secret_patterns=(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?(?!\$\{|<)[A-Za-z0-9_\-]{12,}",)
for path in root.rglob("*"):
    if not path.is_file() or path.suffix not in {".md", ".py", ".json", ".ps1", ".sh"}:
        continue
    contents=path.read_text(encoding="utf-8", errors="replace")
    if any(re.search(pattern, contents) for pattern in secret_patterns): errors.append(f"Possible embedded secret: {path.relative_to(root)}")
for w in warnings: print("WARN:",w)
for e in errors: print("ERROR:",e)
print(f"files={sum(1 for p in root.rglob('*') if p.is_file())}; skill_lines={lines}; refs={len(refs)}")
if errors: sys.exit(1)
print("OK")
