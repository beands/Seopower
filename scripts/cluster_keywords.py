#!/usr/bin/env python3
"""Lexical RU pre-clusterer. Important clusters MUST be validated by Yandex SERP + intent."""
from __future__ import annotations
import argparse, csv, re
from pathlib import Path

STOP={"и","в","во","на","по","для","из","к","ко","с","со","у","о","об","от","до","за","под","над","при","что","как","это","или","а","но"}
COMMERCIAL={"купить","цена","стоимость","заказать","заказ","недорого","оптом","поставщик","производитель"}
try:
    import pymorphy3
    MORPH=pymorphy3.MorphAnalyzer()
except Exception:
    MORPH=None

def toks(s):
    xs=re.findall(r"[a-zа-яё0-9]+",s.lower())
    out=[]
    for x in xs:
        if x in STOP or len(x)<2: continue
        if MORPH and re.search(r"[а-яё]",x):
            try: x=MORPH.parse(x)[0].normal_form
            except Exception: pass
        out.append(x)
    return set(out)

def intent(s):
    ls=s.lower()
    t=toks(s)
    if t & COMMERCIAL: return "commercial"
    if re.search(r"\b(как|почему|что такое|инструкция|своими руками)\b",ls): return "informational"
    if re.search(r"\b(москва|спб|санкт|петербург|рядом)\b",ls): return "local"
    return "mixed"

def jac(a,b):
    return len(a&b)/len(a|b) if a and b else 0.0

ap=argparse.ArgumentParser()
ap.add_argument("input")
ap.add_argument("--out",default="keyword-clusters.csv")
ap.add_argument("--threshold",type=float,default=.48)
args=ap.parse_args()

p=Path(args.input)
sample=p.read_text(encoding="utf-8-sig",errors="replace")[:4096]
delim=csv.Sniffer().sniff(sample,delimiters=",;\t").delimiter
with p.open(encoding="utf-8-sig",newline="") as f:
    r=csv.DictReader(f,delimiter=delim)
    fields=r.fieldnames or []
    def detect(parts):
        for fld in fields:
            if any(x in fld.lower() for x in parts): return fld
    phrase=detect(["phrase","query","keyword","запрос","фраз"])
    volume=detect(["impressions","shows","volume","частот","показ"])
    if not phrase: raise SystemExit(f"No phrase/query column in {fields}")
    rows=list(r)

items=[]
for row in rows:
    q=(row.get(phrase) or "").strip()
    if not q: continue
    try: v=float((row.get(volume) or "0").replace(" ","").replace(",", ".")) if volume else 0
    except Exception: v=0
    items.append({"q":q,"v":v,"t":toks(q),"i":intent(q)})
items.sort(key=lambda x:(-x["v"],x["q"]))

clusters=[]
for x in items:
    bi,bs=None,0
    for i,c in enumerate(clusters):
        if c["i"]!=x["i"]: continue
        s=jac(c["centroid"],x["t"])
        if s>bs: bi,bs=i,s
    if bi is not None and bs>=args.threshold:
        clusters[bi]["items"].append(x)
        clusters[bi]["centroid"] |= x["t"]
    else:
        clusters.append({"i":x["i"],"centroid":set(x["t"]),"items":[x]})

out=Path(args.out)
with out.open("w",encoding="utf-8-sig",newline="") as f:
    w=csv.writer(f)
    w.writerow(["cluster_id","cluster_name","intent","primary_keyword","secondary_keywords","impressions_sum","review_status"])
    for n,c in enumerate(clusters,1):
        z=sorted(c["items"],key=lambda x:(-x["v"],len(x["q"])))
        w.writerow([f"C{n:04d}",z[0]["q"],c["i"],z[0]["q"]," | ".join(a["q"] for a in z[1:30]),int(sum(a["v"] for a in z)),"NEEDS_SERP_REVIEW"])
print(f"Wrote {len(clusters)} pre-clusters to {out}")
print("Validate important clusters by Yandex SERP and intent.")
