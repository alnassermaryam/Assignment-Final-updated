import re

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"reveal\s+(your\s+)?system\s+prompt",
    r"تجاهل\s+التعليمات",
    r"اكشف\s+(?:لي\s+)?(?:تعليمات|system prompt)"
]
SAUDI_ID = re.compile(r"\b[12]\d{9}\b")
SAUDI_MOBILE = re.compile(r"\b05\d{8}\b")

def mask_saudi_pii(text: str) -> str:
    text = SAUDI_ID.sub("[SAUDI_ID_MASKED]", text)
    return SAUDI_MOBILE.sub("[SAUDI_MOBILE_MASKED]", text)

def injection_detected(text: str) -> bool:
    low = text.lower()
    return any(re.search(p, low, re.I) for p in INJECTION_PATTERNS)

def outbound_wall(text: str) -> str:
    # Canary/system-prompt-leak and outbound PII checks.
    forbidden = ["you are a bilingual saudi", "أنت مساعد خدمة عملاء سعودي"]
    if any(x in text.lower() for x in forbidden):
        return "[BLOCKED: prompt leak]"
    return mask_saudi_pii(text)
