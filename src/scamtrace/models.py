from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import Literal


class Risk(str, Enum):
    LOW_CONCERN = "LOW_CONCERN"
    CAUTION = "CAUTION"
    HIGH_CONCERN = "HIGH_CONCERN"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class Event(BaseModel):
    id: str
    timestamp: datetime
    event_type: Literal["message","call_summary","url","qr_payload","payment_request","payment_attempt","note","other"]
    channel: str = "Other"
    content: str = Field(max_length=5000)
    source: str = "user-entered"
    fields: dict = Field(default_factory=dict)

    @field_validator("timestamp")
    @classmethod
    def timestamp_is_utc_aware(cls, value):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)


class Finding(BaseModel):
    agent_name: str
    status: Literal["success","local","fallback"] = "local"
    summary: str
    indicators: list[dict] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    confidence: float = 0.5
    uncertainties: list[str] = Field(default_factory=list)
    provider: Literal["groq","local"] = "local"
    model: str | None = None
    fallback_reason: str | None = None


def utcnow():
    return datetime.now(timezone.utc)
