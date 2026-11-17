# Requirement Traceability Matrix

| Requirement | Implementation | Test/evidence | Status |
|---|---|---|---|
| FR-01 Case create/reopen/export/delete | `database.py`; Case History workspace | `test_workflow.py`; Case History UI; see verification report for untested browser-delete path | Implemented; export UI present |
| FR-02 Timestamped event types | `models.py`; intake form | `test_workflow.py` | Implemented |
| FR-03 Normalize/validate events | Pydantic `Event`; form limits | compile and workflow checks | Partial: current app intake uses canonical dicts at DB boundary |
| FR-04 Chronological timeline | workflow normalize + case timeline | graph test | Implemented |
| FR-05 LangGraph specialist agents | `workflow.py`, `agents.py`, `providers.py` | workflow integration tests; provider fallback tests | Groq-enabled model calls for message/payment/journey/final synthesis; local link/timeline/decision plus per-agent fallback |
| FR-06 Evidence relations | `graph.py` | graph relation test | Implemented |
| FR-07 Sequence investigation | Journey node and journey workspace | workflow test | Implemented, deterministic candidate narrative |
| FR-08 Risk/evidence/uncertainty/guidance | Risk node + assessment view | workflow test | Implemented |
| FR-09 Re-run after new evidence | DB invalidation + rerun action | workflow tests; case workspace action | Implemented; follow-up form path not fully re-exercised in final manual pass |
| FR-10 Synthetic scenarios | `scenarios.py`; Dashboard View Demo | evaluation runner | Implemented |
| FR-11 Evaluation metrics | `run_evaluation.py`; Analytics data aggregation | evaluation command | Implemented, small synthetic fixture only |
| FR-12 Offline mode | deterministic rules and provider fallbacks | workflow and missing-key tests | Implemented; clearly labeled |
| FR-13 Persist runs/assessments | SQLite tables cases/events/runs | workflow test | Implemented |
| FR-14 Validate uploads/sanitize | Streamlit upload controls (10 MB, type allowlist); local SQLite attachment storage | attachment persistence test | Implemented for supported file uploads; OCR/QR decoding unavailable |
| FR-15 Groq LLM provider | `providers.py`; `.env.example`; Streamlit secrets example | Missing-key fallback test; no valid replacement credential used for live request | Integrated; live Groq request pending rotated key |
| FR-16 Optional OCR/QR parsing | Image retained with disclaimer; text payload accepted | — | Not implemented |
| UI pages/layout | `app.py`, references in `project_docs/ui_reference_images` | `output/playwright/`; `project_docs/20_VERIFICATION_REPORT.md` | All six rendered and measured at 1600×900 without page overflow; visual differences remain |
| Community Cloud configuration | root files + README | no deployment | Prepared only |
