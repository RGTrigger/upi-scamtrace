# Implemented Module Reference

The runnable interface is the Streamlit application at `app.py`. Core logic lives in `src/scamtrace`.

| Module | Public operations |
|---|---|
| `scamtrace.database` | `init_db()`, `list_cases()`, `get_case(case_id)`, `create_case(title, summary='', synthetic=False, events=None)`, `add_event(case_id, event, c=None)`, `save_analysis(case_id, assessment, findings, relations, version)`, `delete_case(case_id)`, `get_attachments(case_id)` |
| `scamtrace.workflow` | `build_workflow()` returns a compiled LangGraph state graph; `run_investigation(case_id)` executes it and persists the result, returning the final graph state including findings, assessment, relations, status, and version |
| `scamtrace.agents` | Six specialist functions for message, URL/QR, payment, timeline, journey, and decision analysis; simple classification and journey reasoning use Groq when configured, with provider/model/fallback metadata in each `Finding` |
| `scamtrace.providers` | Loads Groq settings from environment or Streamlit secrets; makes structured-output requests, validates provider mode, and exposes sanitized error categories without exposing API keys |
| `scamtrace.graph` | `build_graph(events)` returns `(networkx.MultiDiGraph, relations)` with chronological and exact URL relations |
| `scamtrace.scenarios` | `scenarios()` returns ten fictional cases with expected labels for deterministic evaluation |

Events are validated at the database boundary by the Pydantic `Event` model. Supported event types are message, call summary, URL, QR payload, payment request, payment attempt, note, and other. Exceptions such as missing case IDs and validation errors propagate to the caller. The app intentionally does not open user-provided URLs or query external services.

Example:

```python
case_id = database.create_case("Review", "", events=[
    {"event_type": "message", "channel": "SMS", "content": "User supplied text"}
])
result = run_investigation(case_id)
print(result["assessment"]["risk_level"])
```
