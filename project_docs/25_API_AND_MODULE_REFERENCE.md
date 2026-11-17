# 25. API and Module Reference

> Codex must update this file to match actual implemented module names and public interfaces.

## 25.1 Expected Module Responsibilities
- `models`: Pydantic schemas and enums
- `database`: SQLite initialization and connection management
- `repositories`: case/event/evidence/assessment persistence
- `parsers`: event normalization, URL parsing, QR/payment URI parsing, optional OCR
- `agents`: specialist agent implementations and contracts
- `workflow`: LangGraph state, nodes, edges, and compile/run entrypoint
- `graph`: temporal evidence graph construction and validation
- `risk`: deterministic aggregation policy and recommendation rules
- `services`: case management, analysis orchestration, export
- `evaluation`: dataset runner, baselines, metrics, report generation
- `integrations`: optional LLM provider and external reputation adapters
- `utils`: logging, sanitization, time handling, IDs

## 25.2 Expected Public Service Operations
- `create_case(...)`
- `get_case(case_id)`
- `add_event(case_id, event_input)`
- `run_investigation(case_id, mode=...)`
- `get_timeline(case_id)`
- `get_evidence_graph(case_id)`
- `get_assessment(case_id)`
- `export_case(case_id, format=...)`
- `delete_case(case_id)`
- `run_evaluation(dataset_path, config=...)`

Codex should document exact signatures, return types, exceptions, and examples after implementation.
