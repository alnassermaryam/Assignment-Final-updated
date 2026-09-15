"""Run the exact committed golden set under AI_MODEL_ALIAS.
Examples:
  AI_MODEL_ALIAS=commercial_primary python scripts/run_backend.py eval/commercial.json
  AI_MODEL_ALIAS=open_weight python scripts/run_backend.py eval/open_weight.json
"""
import json, os, sys, time
from pathlib import Path
root=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(root/"src"))
from ai_engineering.service import handle_request
from ai_engineering.costing import cost_record
cases=json.loads((root/"data/golden_set.json").read_text(encoding="utf-8"))["cases"]
out=[]; t=time.perf_counter()
for c in cases:
    r,u=handle_request(c["input"], alias=os.getenv("AI_MODEL_ALIAS","mock")); raw=r.model_dump_json()
    ok=r.intent==c["expected_intent"] and c["must_contain"] in raw and all(x.lower() not in raw.lower() for x in c["must_not_contain"])
    out.append({"id":c["id"],"slice":c["slice"],"pass":ok,**cost_record(u)})
elapsed=time.perf_counter()-t
artifact={"model_alias":os.getenv("AI_MODEL_ALIAS","mock"),"golden_version":"1.0.0","elapsed_seconds":elapsed,"measured_throughput_rps":len(cases)/elapsed if elapsed else None,"rows":out}
Path(sys.argv[1] if len(sys.argv)>1 else "backend_run.json").write_text(json.dumps(artifact,indent=2),encoding="utf-8")
print(json.dumps(artifact,indent=2))
