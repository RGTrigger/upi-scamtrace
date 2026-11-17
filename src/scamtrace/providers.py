"""Groq configuration and guarded structured-output calls.

API credentials are read only from the process environment or Streamlit secrets.
They are never returned by config_summary(), logged, or persisted with cases.
"""
from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # pragma: no cover - optional local convenience
    pass


class ProviderUnavailable(RuntimeError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def _secret(name: str) -> str | None:
    value = os.getenv(name)
    if value:
        return value.strip() or None
    try:
        import streamlit as st
        value = st.secrets.get(name)
        return str(value).strip() or None if value else None
    except Exception:
        return None


def config_summary() -> dict[str, Any]:
    requested = (_secret("SCAMTRACE_LLM_PROVIDER") or "groq").strip().lower()
    key = _secret("GROQ_API_KEY")
    complex_model = (_secret("SCAMTRACE_COMPLEX_MODEL") or "openai/gpt-oss-120b").strip()
    simple_model = (_secret("SCAMTRACE_SIMPLE_MODEL") or "openai/gpt-oss-20b").strip()
    simple_enabled = (_secret("SCAMTRACE_USE_SMALL_MODEL") or "true").strip().lower() in {"1", "true", "yes", "on"}
    # A preference stored by the Settings page takes precedence over the
    # deployment default. Import lazily so standalone provider use still works.
    try:
        from .database import get_setting
        persisted = get_setting("use_small_model")
        if persisted is not None:
            simple_enabled = str(persisted).strip().lower() in {"1", "true", "yes", "on"}
    except Exception:
        pass
    if requested == "offline":
        provider, reason = "offline", "offline_configured"
    elif requested != "groq":
        provider, reason = "offline", "invalid_provider"
    elif not key:
        provider, reason = "offline", "missing_api_key"
    else:
        provider, reason = "groq", None
    return {
        "requested_provider": requested,
        "provider": provider,
        "fallback_reason": reason,
        "key_configured": bool(key),
        "complex_model": complex_model or "openai/gpt-oss-120b",
        "simple_model": simple_model or "openai/gpt-oss-20b",
        "simple_model_enabled": simple_enabled,
    }


@lru_cache(maxsize=2)
def _client(api_key: str):
    from groq import Groq
    return Groq(api_key=api_key, timeout=25.0, max_retries=1)


def error_code(exc: Exception) -> str:
    status = getattr(exc, "status_code", None)
    if status == 429:
        return "rate_limit"
    if status in (401, 403):
        return "authentication_error"
    if status and status >= 500:
        return "provider_unavailable"
    if "timeout" in type(exc).__name__.lower():
        return "timeout"
    return "request_error"


def structured_completion(*, model: str, system: str, payload: dict, schema_name: str, schema: dict) -> dict:
    cfg = config_summary()
    if cfg["provider"] != "groq":
        raise ProviderUnavailable(cfg["fallback_reason"] or "offline_configured")
    key = _secret("GROQ_API_KEY")
    if not key:
        raise ProviderUnavailable("missing_api_key")
    response = _client(key).chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        response_format={"type": "json_schema", "json_schema": {
            "name": schema_name, "strict": True, "schema": schema,
        }},
    )
    content = response.choices[0].message.content
    if not content:
        raise ProviderUnavailable("empty_response")
    try:
        result = json.loads(content)
    except (TypeError, json.JSONDecodeError) as exc:
        raise ProviderUnavailable("invalid_structured_response") from exc
    if not isinstance(result, dict):
        raise ProviderUnavailable("invalid_structured_response")
    return result
