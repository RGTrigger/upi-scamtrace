# 26. Codex Execution Protocol and Quality Gates

## Purpose
This document defines how Codex must build, verify, and hand off the complete UPI ScamTrace application from this documentation package.

## 26.1 Work in the Correct Repository
- Confirm the active workspace/project root before creating files.
- Preserve unrelated user files; inspect any existing ScamTrace code before changing it.
- Keep source, tests, sample data, documentation, scripts, and UI assets in one coherent repository.
- Extract the PDF checklist categories and apply only relevant documentation requirements to ScamTrace as mapped in `29_DOCUMENTATION_COVERAGE_FROM_REFERENCE_PDF.md`; do not copy unrelated example-app features.

## 26.2 Read All Documentation and UI Assets First
1. Read every Markdown file in the package and `MANIFEST.md`.
2. Read `28_DOCUMENTATION_COVERAGE_FROM_REFERENCE_PDF.md`.
3. Inspect all six approved image assets under `ui_reference_images/` and verify filenames against `28_UI_REFERENCE_IMAGE_INDEX.md`.
4. Read `08_UI_UX_SPECIFICATION.md` and `27_UI_VISUAL_DESIGN_HANDOFF.md` before coding UI.
5. Create a requirement traceability matrix before implementation.

## 26.3 Required Build Artifacts
- Runnable Streamlit application
- Compatible dependency manifest
- `.env.example` and safe configuration
- SQLite initialization/migrations
- Deterministic offline/demo workflow
- Optional provider adapter behind an interface
- Synthetic scenarios and loader
- Automated tests
- Evaluation runner/report
- Windows and Unix setup/run instructions where practical
- Root README and complete docs
- UI reference image folder and index
- Requirement traceability matrix
- Actual verification report
- No placeholder-only screens or fake “complete” features

## 26.4 Requirement Traceability
Create `docs/REQUIREMENT_TRACEABILITY.md` with requirement ID, summary, implementing module/page, test IDs, status, and evidence. Map every Must requirement in `01`, `02`, `08`, and `12`. Documentation alone is not implementation evidence.

## 26.5 Implementation Rules
- Implement deterministic core before optional LLM features.
- Use Pydantic schemas at agent/service boundaries.
- Use one canonical event model across UI, parsing, storage, graph, and evaluation.
- Keep business logic out of Streamlit page scripts.
- Keep risk aggregation deterministic and auditable.
- Ground every conclusion in event/evidence references.
- Use typed LangGraph state and actual graph execution.
- Use stable IDs and UTC-aware timestamps internally.
- Version assessments when case evidence changes.
- Default to offline mode when provider configuration is absent/invalid.
- External lookups are optional, disabled by default, and documented.

## 26.6 UI Implementation — Strict Reference Matching
The six UI reference images are the required visual target, not loose inspiration.
- Use `28_UI_REFERENCE_IMAGE_INDEX.md` to locate and map assets.
- Match the page composition, sidebar, header, colors, cards, spacing, typography, charts, buttons, and selected states as closely as possible.
- Use the locked theme: Deep Emerald `#142923`, Champagne Gold `#C6A76A`, Warm Ivory `#F5F2EA`.
- Do not replace the approved visual system with a generic Streamlit theme.
- Implement the functional controls represented in the images; a static screenshot or background image is not an implementation.
- Keep actual content/data honest even when the reference contains illustrative numbers.
- If Streamlit/browser constraints prevent exact rendering, implement the closest functional match and record the precise limitation. Do not silently redesign or claim exactness without comparison.
- Capture actual app screenshots and compare at 1600×900.

## 26.7 No-Scroll Quality Gate (Mandatory)
At 1600×900, all six primary pages must fit within the viewport without page-level vertical or horizontal scrolling.
- No hiding scrollbars, clipping content, or omitting controls to pass.
- Use compact layout, columns, tabs, and progressive disclosure.
- Inner case/evidence lists may use bounded internal scrolling only when necessary.
- Test the actual running Streamlit app and record viewport and result.
- If a page fails, fix it before handoff; if environment prevents testing, mark NOT RUN and explain.

## 26.8 Interaction and Motion Quality Gate
- Sidebar navigation and case tabs work.
- Case History selection opens the nested case workspace.
- Every visible button/control has a real action.
- Use restrained transitions (about 120–220 ms) where supported.
- Respect reduced-motion preferences.
- Progress indicators reflect actual work.
- Destructive actions require confirmation.
- No fake “agent active,” “verified,” or success states.

## 26.9 LLM and Offline Behavior
- Missing API key must not prevent startup.
- Provider config is validated without exposing secrets.
- Model calls use timeouts and bounded retries.
- Outputs are parsed/validated; failures use controlled fallback.
- Evidence is untrusted input and cannot issue tool/system instructions.
- Required tests use deterministic fixtures and no network.
- Live-provider tests are opt-in.
- LLM cannot independently set final risk level.

## 26.10 Quality Gates (Must Execute)
1. Clean dependency installation where environment permits.
2. Import/compile check.
3. Full `pytest` suite.
4. Streamlit startup smoke test.
5. Synthetic scenario evaluation.
6. Verify report/metrics outputs.
7. Manual case flow: create/load, analyze, inspect timeline/graph/agents, add event, export, reopen, delete.
8. UI screenshot comparison for all six pages at 1600×900.
9. No-scroll check for all six pages.
10. Check secrets, real personal data, and placeholder-only features.
11. Confirm README commands match actual entry points.
12. Update traceability matrix and verification report.

If a gate cannot run, mark `NOT RUN`; never fabricate logs, screenshots, metrics, test counts, or successful checks.

## 26.11 Completion Definitions
- Implemented: code exists and is wired into the app.
- Tested: a test/manual check was executed.
- Verified: evidence of a successful check is recorded.
- Locally runnable: setup and launch succeeded in a clean local environment.
- Deployable: deployment configuration exists and was tested in its target environment.
- Production-ready: out of scope for this student prototype; never claim it.

Minimum result: locally runnable, supervisor-demo-ready Streamlit prototype. Cloud deployment is optional and must not be claimed unless tested.

## 26.12 Final Handoff
Report repository path, setup/run commands, offline/LLM mode, implemented pages/workflows, test counts, evaluation dataset/metrics, UI screenshot/no-scroll results, known limitations, traceability matrix, and supervisor demo sequence.


## 26.12 Mandatory Reference-Image Fidelity Gate
- Each implemented screen must be visually compared to its exact supplied PNG at 1600×900.
- Required evidence: captured app screenshot, side-by-side comparison, and overlay/diff or equivalent visual inspection.
- Every visible section, label, card, chart, button, tab, icon, and selected state must be present in the same hierarchy and placement. No redesign or omission is allowed.
- Keep source PNGs unchanged; do not use them as static backgrounds.
- If a control cannot be fully implemented, preserve its placement and show an honest disabled state.
- No page-level vertical/horizontal scrolling at 1600×900; verify scroll dimensions and confirm no content is clipped/hidden.
- Any unverified image match or failed no-scroll check blocks the “UI verified” claim.

## 26.13 Streamlit Community Cloud Gate
- Prepare a GitHub-ready repo with root `app.py`, `requirements.txt`, `.gitignore`, safe `.streamlit` configuration, and secrets instructions.
- Follow `31_STREAMLIT_COMMUNITY_CLOUD_DEPLOYMENT.md`.
- Clearly distinguish locally runnable, Community-Cloud-ready, and actually deployed/tested.
- Verify hosted startup, core synthetic workflow, secrets handling, persistence behavior, and 1600×900 UI after deployment.
