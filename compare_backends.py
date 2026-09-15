from __future__ import annotations
import json, sys
from pathlib import Path
def load_rows(p):
    x=json.loads(Path(p).read_text())
    return x.get("rows", x) if isinstance(x,dict) else x
def by_slice(rows):
    out={}
    for s in sorted({r["slice"] for r in rows}):
        rs=[r for r in rows if r["slice"]==s]
        out[s]={"n":len(rs),"pass_rate":sum(bool(r["pass"]) for r in rs)/len(rs),"avg_latency_ms":sum(r.get("latency_ms",0) for r in rs)/len(rs),"total_cost_usd":sum(r.get("estimated_cost_usd",0) for r in rs)}
    return out
if len(sys.argv)!=3: raise SystemExit("usage: compare_backends.py commercial.json open_weight.json")
a,b=load_rows(sys.argv[1]),load_rows(sys.argv[2])
print(json.dumps({"commercial_by_slice":by_slice(a),"open_weight_by_slice":by_slice(b)},indent=2))
