import json, sys
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else "eval/summary.json")
s=json.loads(p.read_text())
protected={"injection","pii","schema"}
failed=[k for k,v in s.get("by_slice",{}).items() if k in protected and v.get("pass_rate",0)<1.0]
if s.get("pass_rate",0)<1.0 or failed:
    print("REGRESSION GATE: FAIL", {"failed_protected_slices":failed,"pass_rate":s.get("pass_rate")})
    raise SystemExit(1)
print("REGRESSION GATE: PASS")
