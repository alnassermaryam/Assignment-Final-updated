from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os, yaml

ROOT = Path(__file__).resolve().parents[2]
CFG = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))

@dataclass(frozen=True)
class ModelTarget:
    alias: str
    provider: str
    model: str
    base_url: str | None = None


def resolve_model(alias: str | None = None) -> ModelTarget:
    alias = alias or os.getenv("AI_MODEL_ALIAS", "commercial_primary")
    raw = CFG["models"]["aliases"][alias]
    base_url = os.getenv(raw.get("base_url_env", "")) if raw.get("base_url_env") else None
    return ModelTarget(alias=alias, provider=raw["provider"], model=raw["model"], base_url=base_url)

MAX_TOOL_STEPS = int(os.getenv("MAX_TOOL_STEPS", CFG["runtime"]["max_tool_steps"]))
RETRY_ATTEMPTS = int(CFG["runtime"]["retry_attempts"])
RETRY_BASE_SECONDS = float(CFG["runtime"]["retry_base_seconds"])
