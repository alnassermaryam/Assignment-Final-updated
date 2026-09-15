from __future__ import annotations
import hashlib, json

def response_cache_key(*, prompt_version: str, model_id: str, normalized_input: str,
                       authorization_scope: str, tool_state_version: str = "v1") -> str:
    """Key includes every answer-changing dimension; never cache across auth scopes."""
    payload = {"prompt_version":prompt_version,"model_id":model_id,
               "input":normalized_input,"authorization_scope":authorization_scope,
               "tool_state_version":tool_state_version}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
