# 30. Debugging and Troubleshooting

## Purpose
Provide a practical debugging guide for implementation and demo operation. Codex must update this document when real issues are found during build and verification.

## Common Issues
| Symptom | Check | Expected handling |
|---|---|---|
| Streamlit fails to start | Python version, virtual environment, dependency installation, entry point | Provide exact error and setup correction; do not hide import failures |
| Missing API key/provider | `.env` and settings status | App starts in offline mode; no secret shown |
| Model timeout/invalid output | Provider logs, schema validation, retry count | Bounded retry then deterministic fallback; show partial/fallback status |
| LangGraph node failure | Node input/output schema, state transitions, exception logs | Mark affected agent failed and preserve safe partial analysis |
| No cases/analytics | SQLite path, initialization, seed/demo loading | Show empty state or explicitly load synthetic scenarios; never fake counts |
| Case fails to reopen | Repository query, foreign keys, schema version | Surface actionable error; test persistence/reload |
| Graph rendering unavailable | Graph data and visualization dependency | Show relation table fallback |
| Upload rejected | MIME/type, size, file parsing | Explain validation error and accepted formats |
| UI page scrolls | Actual viewport, card dimensions, Streamlit spacing | Rework layout; do not hide scrollbar or clip content |
| UI differs from reference | Asset mapping, viewport, CSS, component dimensions | Compare screenshot and update layout against image |
| Button appears inert | Callback/routing/state update | Wire real action and add UI test/manual check |
| Export contains sensitive data | Sanitization and export schema | Block/remove secrets; add regression test |

## Logging Rules
- Use structured, bounded logs.
- Never log API keys, PINs, OTPs, passwords, full bank credentials, or unnecessary personal data.
- Include case/event IDs only when safe and useful.
- Distinguish expected fallback from unexpected error.
- Avoid logging raw uploaded evidence by default.

## Debugging Workflow
1. Reproduce from a clean environment or synthetic fixture.
2. Capture exact command, error, and relevant sanitized logs.
3. Identify the failing layer (UI, service, parser, agent, workflow, graph, risk, database, export).
4. Add or update a deterministic regression test.
5. Fix the root cause, not just the visible symptom.
6. Run the focused test, full suite, startup smoke, and relevant UI check.
7. Update `20_VERIFICATION_REPORT.md` and this guide with actual results.

## Known Scope Limitations
- No direct UPI/bank access, transaction blocking, reversal, or recovery.
- No automatic access to device SMS/call logs.
- OCR/QR parsing and live external reputation are optional only.
- Local prototype authentication may be omitted; do not expose publicly without suitable access controls.
- Cloud deployment must be verified separately from local run.
