from typing import Literal
from pydantic import BaseModel, Field, field_validator

class AssistantOutput(BaseModel):
    language: Literal["ar","en"]
    intent: Literal["order_status","order_update","order_cancel","general"]
    answer: str = Field(min_length=1, max_length=800)
    order_id: str | None = None
    safe: bool = True

    @field_validator("order_id")
    @classmethod
    def valid_order(cls, v):
        if v is not None and not v.startswith("ORD-"):
            raise ValueError("order_id must start with ORD-")
        return v

class ToolCall(BaseModel):
    name: Literal["get_order_status"]
    order_id: str
