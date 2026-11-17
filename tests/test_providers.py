import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from scamtrace import agents, providers


def test_missing_groq_key_uses_labeled_local_fallback(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.setattr(providers, "_secret", lambda name: None if name == "GROQ_API_KEY" else os.getenv(name))
    monkeypatch.setenv("SCAMTRACE_LLM_PROVIDER", "groq")
    config = providers.config_summary()
    assert config["provider"] == "offline"
    assert config["fallback_reason"] == "missing_api_key"
    finding = agents.message_analysis([{"id":"E-1","content":"Share your OTP immediately","timestamp":"2026-01-01T00:00:00+00:00","event_type":"message","channel":"SMS"}])
    assert finding["status"] == "fallback"
    assert finding["provider"] == "local"
    assert finding["fallback_reason"] == "missing_api_key"
    assert any(x["code"] == "credential_request" for x in finding["indicators"])


def test_model_names_are_environment_configurable(monkeypatch):
    monkeypatch.setenv("SCAMTRACE_LLM_PROVIDER", "offline")
    monkeypatch.setenv("SCAMTRACE_COMPLEX_MODEL", "openai/gpt-oss-120b")
    monkeypatch.setenv("SCAMTRACE_SIMPLE_MODEL", "openai/gpt-oss-20b")
    config = providers.config_summary()
    assert config["complex_model"] == "openai/gpt-oss-120b"
    assert config["simple_model"] == "openai/gpt-oss-20b"


def test_message_agent_routes_to_small_model_and_validates_event_refs(monkeypatch):
    monkeypatch.setattr(providers, "config_summary", lambda: {"provider":"groq","simple_model_enabled":True,"simple_model":"test-small","complex_model":"test-large","fallback_reason":None})
    calls=[]
    def fake_completion(**kwargs):
        calls.append(kwargs["model"])
        return {"summary":"Possible credential solicitation.","indicators":[{"code":"credential_request","description":"OTP requested.","severity":"low","confidence":.9,"event_ids":["E-1"]}],"evidence_refs":["E-1"],"confidence":.9,"uncertainties":[]}
    monkeypatch.setattr(providers,"structured_completion",fake_completion)
    finding=agents.message_analysis([{"id":"E-1","content":"Share OTP","event_type":"message","channel":"SMS"}])
    assert calls==["test-small"]
    assert finding["status"]=="success" and finding["provider"]=="groq"
    assert finding["indicators"][0]["severity"]=="high"  # severity is policy-owned, not model-chosen


def test_rate_limit_is_recorded_and_agent_falls_back(monkeypatch):
    monkeypatch.setattr(providers,"config_summary",lambda:{"provider":"groq","simple_model_enabled":True,"simple_model":"test-small","fallback_reason":None})
    class RateLimited(Exception):
        status_code=429
    def fail(**kwargs): raise RateLimited("private request details")
    monkeypatch.setattr(providers,"structured_completion",fail)
    finding=agents.message_analysis([{"id":"E-1","content":"Share your OTP","event_type":"message","channel":"SMS"}])
    assert finding["status"]=="fallback"
    assert finding["fallback_reason"]=="rate_limit"
    assert "private request details" not in finding["summary"]


def test_journey_and_final_synthesis_route_to_complex_model(monkeypatch):
    monkeypatch.setattr(providers,"config_summary",lambda:{"provider":"groq","simple_model_enabled":True,"simple_model":"test-small","complex_model":"test-complex","fallback_reason":None})
    models=[]
    def fake_completion(**kwargs):
        models.append(kwargs["model"])
        if kwargs["schema_name"]=="journey_agent_finding":
            return {"summary":"Message followed by payment request.","indicators":[],"evidence_refs":["E-1"],"confidence":.8,"uncertainties":["Sequence is user supplied."]}
        return {"summary":"Cautious case synthesis.","evidence_basis":["E-1"],"uncertainties":[],"safe_next_steps":["Verify with official support."]}
    monkeypatch.setattr(providers,"structured_completion",fake_completion)
    event={"id":"E-1","content":"A payment request arrived","event_type":"payment_request","channel":"SMS"}
    journey=agents.journey_analysis([event],[])
    assessment={"risk_level":"CAUTION","score":38,"reason":"A limited indicator is present.","reason_codes":[],"supporting_event_ids":["E-1"],"uncertainties":[],"recommendations":[]}
    synthesis=agents.final_synthesis([event],[journey],assessment)
    assert models==["test-complex","test-complex"]
    assert journey["provider"]=="groq" and synthesis["status"]=="success"
