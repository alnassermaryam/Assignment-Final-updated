from pathlib import Path
import json, statistics, time
from .service import handle_request
from .costing import cost_record

ROOT=Path(__file__).resolve().parents[2]
def run():
    gs=json.loads((ROOT/"data/golden_set.json").read_text(encoding="utf-8"))
    rows=[]
    for c in gs["cases"]:
        out,u=handle_request(c["input"])
        text=out.model_dump_json()
        ok=(out.intent==c["expected_intent"] and c["must_contain"] in text and
            all(x.lower() not in text.lower() for x in c["must_not_contain"]))
        rows.append({"id":c["id"],"slice":c["slice"],"pass":ok,**cost_record(u)})
    (ROOT/"eval/results.json").write_text(json.dumps(rows,indent=2),encoding="utf-8")
    slices={}
    for s in sorted({r["slice"] for r in rows}):
        rs=[r for r in rows if r["slice"]==s]
        slices[s]={"pass_rate":sum(r["pass"] for r in rs)/len(rs),"avg_latency_ms":statistics.mean(r["latency_ms"] for r in rs)}
    report={"golden_version":gs["version"],"total":len(rows),"pass_rate":sum(r["pass"] for r in rows)/len(rows),
            "by_slice":slices,"total_cost_usd":sum(r["estimated_cost_usd"] for r in rows)}
    (ROOT/"eval/summary.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
if __name__=="__main__": run()
