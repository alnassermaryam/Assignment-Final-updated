# Rates are intentionally configurable examples, not claims about current vendor pricing.
RATES = {
    "mock": {"input":0.0,"cached":0.0,"output":0.0},
    "openai": {"input":1.0,"cached":0.25,"output":4.0},
    "openai_compatible": {"input":0.0,"cached":0.0,"output":0.0},
    "anthropic": {"input":3.0,"cached":0.30,"output":15.0},
}
def cost_record(usage: dict) -> dict:
    r = RATES.get(usage.get("provider"), RATES["mock"])
    cached = usage.get("cached_input_tokens",0) or 0
    uncached = max((usage.get("input_tokens",0) or 0)-cached,0)
    output = usage.get("output_tokens",0) or 0
    cost = (uncached*r["input"] + cached*r["cached"] + output*r["output"]) / 1_000_000
    return {**usage, "observed_prompt_cache": cached > 0, "estimated_cost_usd": round(cost,8)}
