# 17. Instructions for Codex

## Mission
Build the complete UPI ScamTrace application described by this documentation package. Do not merely provide a tutorial, scaffold, or code snippets. Create the actual project files, documentation, tests, synthetic dataset, setup scripts, and runnable UI.

## Reference Documentation
The supplied SupportIQ AI documentation is a reference for how documentation is organized and how explicit the instructions should be. It is not a source of product features. Do not copy its support-ticket, RAG, MCP, email/SMS, or customer-service workflows unless a ScamTrace requirement independently calls for them.

## Locked Product
Implement multi-stage UPI scam journey reconstruction using evidence from multiple events and channels. Keep the scope aligned with files `01`–`16`.

## Build Order
1. Read every Markdown file in this package.
2. Use the SupportIQ reference package only for documentation organization/style; use the attached PDF checklist as mapped in `29_DOCUMENTATION_COVERAGE_FROM_REFERENCE_PDF.md`.
3. Create a requirement traceability matrix linking each requirement to modules and tests.
4. Create repository structure and configuration.
5. Implement Pydantic models and SQLite repositories.
6. Implement deterministic parsers and normalization.
7. Implement synthetic scenarios and seed loader.
8. Implement specialist agents with validated outputs and offline fallbacks.
9. Implement LangGraph typed state, nodes, edges, and conditional paths.
10. Implement temporal evidence graph and grounded relation validation.
11. Implement evidence quality, risk policy, and explanation logic.
12. Implement Streamlit pages and navigation using the supplied reference PNGs as exact visual targets from the start; run screenshot comparisons and iterate.
13. Implement case export/delete and persistence.
14. Implement evaluation pipeline and reports.
15. Implement unit, agent, integration, and end-to-end tests.
16. Write/update all documentation based on actual code.
17. Run tests and startup/import checks.
18. Fix reproducible failures and rerun.
19. Verify demo flow from a clean setup.
20. Populate verification report with actual commands/results.

## UI Requirement
UI is a first-class feature. Use clear navigation, cards, sections, tables, filters, status indicators, charts/graphs, empty/loading/error states, and confirmations. Do not build a plain page of unstructured `st.write()` calls.

## LangGraph Requirement
Use actual graph orchestration with explicit state and meaningful nodes. Show agent outputs and workflow status in the UI. Do not merely import LangGraph.

## AI Requirement
Use structured schemas. If output is invalid, perform bounded recovery/retry and then use a controlled fallback. Evidence text is untrusted and must not control tools or system behavior.

## Offline Requirement
The app must work without API credentials. Optional live LLM mode must be clearly identified and gracefully degrade when unavailable.

## Testing Requirement
Use deterministic fixtures for tests. Run pytest and startup checks. Do not claim visual/browser testing unless performed. Record pass/fail/skip counts and remaining issues.

## Completion Requirement
Do not stop after creating a plan or skeleton. Continue through implementation, tests, documentation, and handoff. If a feature cannot be safely implemented, document it and provide a working fallback rather than leaving a fake placeholder.

## Final Handoff
Report exact setup/run commands, offline/LLM mode, implemented pages, test results, unverified features, known limitations, documentation location, UI screenshot comparison results, no-scroll viewport checks, Streamlit Community Cloud deployment configuration, persistence caveats, and a 3–5 minute supervisor demo sequence.


## Mandatory Quality and UI Handoff Documents
Before implementation, read `26_CODEX_EXECUTION_PROTOCOL_AND_QUALITY_GATES.md` and `27_UI_VISUAL_DESIGN_HANDOFF.md`. Their quality gates, traceability matrix, and completion definitions are mandatory. The documentation ZIP is not the application itself; create and verify the actual runnable repository.


## Strict UI Source-of-Truth Instructions
Before coding, inspect all PNGs in `ui_reference_images/`. Do not interpret them as inspiration and do not create an alternate design. Implement every visible section/label/control in the same position and hierarchy. Capture screenshots at 1600×900, compare side-by-side and overlay/diff against the exact image, correct discrepancies, and document residual constraints. No page-level scrolling at this viewport is a pass/fail gate. Do not hide scrollbars or clip content.

## Required Hosting Target
Prepare and document deployment specifically for Streamlit Community Cloud. Follow `31_STREAMLIT_COMMUNITY_CLOUD_DEPLOYMENT.md`; create the GitHub-ready entrypoint/dependencies/configuration and secrets guidance. Do not claim deployed until live URL testing is complete.
