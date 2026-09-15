from __future__ import annotations
import re, time, random
from pydantic import ValidationError
from .providers import build_provider
from .safety import mask_saudi_pii, injection_detected, outbound_wall
from .tools import get_order_status, AuthorizationContext
from .config import MAX_TOOL_STEPS, RETRY_ATTEMPTS, RETRY_BASE_SECONDS


def language_of(text: str) -> str:
    return "ar" if re.search(r"[\u0600-\u06FF]", text) else "en"


def handle_request(text: str, auth: AuthorizationContext | None = None, alias: str | None = None):
    auth = auth or AuthorizationContext()
    stages = []

    # Stage 1: Saudi PII is masked BEFORE any model call or application log.
    clean = mask_saudi_pii(text); stages.append("pii_mask")
    injection = injection_detected(clean); stages.append("injection_check")

    provider = build_provider(alias)
    out = usage = None
    # Boundary-level retry/backoff + validation repair. Safe because generation is idempotent.
    for attempt in range(RETRY_ATTEMPTS):
        try:
            out, usage = provider.generate_structured(clean, language_of(clean))
            stages.append("model_structured_output")
            break
        except (ValidationError, ValueError) as e:
            clean += "\nValidation error: " + str(e) + "\nRepair the response to match the schema."
        except Exception:
            if attempt == RETRY_ATTEMPTS - 1: raise
            time.sleep(RETRY_BASE_SECONDS * (2 ** attempt) + random.random() * 0.1)
    if out is None: raise RuntimeError("retry/repair exhausted")

    # Real tool execution path is bounded and authorization-gated.
    # In a provider-native agent loop, TOOL_DEFINITIONS are sent to the model; this app
    # additionally keeps the business-side execution gate deterministic and testable.
    if out.intent == "order_status" and out.order_id:
        for _ in range(min(MAX_TOOL_STEPS, 1)):
            result = get_order_status(out.order_id, auth)
            out.answer = (f"حالة الطلب {out.order_id}: {result['status']}." if out.language == "ar"
                          else f"Order {out.order_id} status: {result['status']}.")
        stages.append("authorized_tool_execution")

    if injection:
        out.answer += (" تم تجاهل محاولة حقن التعليمات." if out.language == "ar" else " Prompt-injection attempt ignored.")
    out.answer = outbound_wall(out.answer); stages.append("outbound_wall")
    usage = dict(usage or {}); usage["stages"] = stages; usage["injection_detected"] = injection
    return out, usage
