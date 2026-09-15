from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
import json, time
from .schemas import AssistantOutput
from .config import resolve_model

ROOT = Path(__file__).resolve().parents[2]
PROMPT_DIR = ROOT / "prompts"

TOOL_DEFINITIONS = [{
    "type": "function",
    "name": "get_order_status",
    "description": "Read the current status of an order after authorization.",
    "parameters": {
        "type": "object",
        "properties": {"order_id": {"type": "string", "pattern": "^ORD-[0-9]+$"}},
        "required": ["order_id"],
        "additionalProperties": False,
    },
    "strict": True,
}]

class ProviderBoundary(ABC):
    """Typed boundary: business logic never imports provider SDKs directly."""
    @abstractmethod
    def generate_structured(self, text: str, lang: str) -> tuple[AssistantOutput, dict]: ...

class MockProvider(ProviderBoundary):
    def generate_structured(self, text: str, lang: str):
        import re
        t0 = time.perf_counter()
        oidm = re.search(r"ORD-\d+", text)
        oid = oidm.group(0) if oidm else None
        low = text.lower()
        intent = "order_cancel" if ("cancel" in low or "إلغاء" in text) else "order_update" if ("update" in low or "تحديث" in text) else "order_status" if oid else "general"
        answer = (f"تم استلام طلبك {oid}." if lang == "ar" else f"Request received for {oid}.") if oid else ("كيف يمكنني مساعدتك؟" if lang == "ar" else "How can I help?")
        out = AssistantOutput(language=lang, intent=intent, answer=answer, order_id=oid, safe=True)
        return out, {"provider":"mock","model":"mock-v1","input_tokens":max(1,len(text)//4),"output_tokens":max(1,len(answer)//4),"cached_input_tokens":0,"latency_ms":round((time.perf_counter()-t0)*1000,3)}

class OpenAIResponsesProvider(ProviderBoundary):
    def __init__(self, alias: str):
        from openai import OpenAI
        self.target = resolve_model(alias)
        kwargs = {}
        if self.target.provider == "openai_compatible":
            if not self.target.base_url:
                raise RuntimeError("OPEN_WEIGHT_BASE_URL is required for open_weight alias")
            kwargs = {"base_url": self.target.base_url, "api_key": __import__('os').getenv("OPEN_WEIGHT_API_KEY", "local")}
        self.client = OpenAI(**kwargs)

    def generate_structured(self, text: str, lang: str):
        prompt = (PROMPT_DIR / f"system_{lang}.txt").read_text(encoding="utf-8")
        t0 = time.perf_counter()
        # Real SDK call + schema-constrained structured output over the wire.
        r = self.client.responses.parse(
            model=self.target.model,
            input=[{"role":"system","content":prompt},{"role":"user","content":text}],
            text_format=AssistantOutput,
        )
        usage = getattr(r, "usage", None)
        cached = getattr(getattr(usage, "input_tokens_details", None), "cached_tokens", 0) or 0
        return r.output_parsed, {
            "provider": self.target.provider, "model": self.target.model,
            "input_tokens": getattr(usage,"input_tokens",0) or 0,
            "output_tokens": getattr(usage,"output_tokens",0) or 0,
            "cached_input_tokens": cached,
            "latency_ms": round((time.perf_counter()-t0)*1000,2),
        }

class AnthropicProvider(ProviderBoundary):
    def __init__(self, alias: str):
        from anthropic import Anthropic
        self.target = resolve_model(alias)
        self.client = Anthropic()
    def generate_structured(self, text: str, lang: str):
        prompt = (PROMPT_DIR / f"system_{lang}.txt").read_text(encoding="utf-8")
        schema = AssistantOutput.model_json_schema()
        t0 = time.perf_counter()
        r = self.client.messages.create(
            model=self.target.model, max_tokens=700, system=prompt,
            messages=[{"role":"user","content":text}],
            output_config={"format":{"type":"json_schema","schema":schema}},
        )
        raw = "".join(getattr(b,"text","") for b in r.content)
        out = AssistantOutput.model_validate_json(raw)
        return out, {
            "provider":"anthropic","model":self.target.model,
            "input_tokens":getattr(r.usage,"input_tokens",0) or 0,
            "output_tokens":getattr(r.usage,"output_tokens",0) or 0,
            "cached_input_tokens":getattr(r.usage,"cache_read_input_tokens",0) or 0,
            "latency_ms":round((time.perf_counter()-t0)*1000,2),
        }

def build_provider(alias: str | None = None) -> ProviderBoundary:
    alias = alias or __import__('os').getenv("AI_MODEL_ALIAS", "mock")
    if alias == "mock": return MockProvider()
    target = resolve_model(alias)
    if target.provider in {"openai","openai_compatible"}: return OpenAIResponsesProvider(alias)
    if target.provider == "anthropic": return AnthropicProvider(alias)
    raise ValueError(f"Unsupported provider: {target.provider}")
