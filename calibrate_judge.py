import json, sys
from pathlib import Path

def kappa(a,b):
    n=len(a); agree=sum(x==y for x,y in zip(a,b))/n
    pa=sum(a)/n; pb=sum(b)/n
    pe=pa*pb+(1-pa)*(1-pb)
    return agree, (agree-pe)/(1-pe) if pe != 1 else 1.0

p=Path(sys.argv[1] if len(sys.argv)>1 else "data/judge_labels.example.json")
d=json.loads(p.read_text())
items=d["items"]
if any(x.get("human_label") is None for x in items):
    raise SystemExit("Human labels are missing. Collect real reviewer labels first; calibration is intentionally not fabricated.")
a=[int(x["human_label"]) for x in items]; b=[int(x["judge_label"]) for x in items]
ag,k=kappa(a,b)
print(json.dumps({"n":len(a),"agreement":ag,"cohens_kappa":k},indent=2))
