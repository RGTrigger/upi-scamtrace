# UPI ScamTrace — Documentation Package

## Purpose
This package is the complete product and implementation blueprint for **UPI ScamTrace — A Multi-Agent Framework for Reconstructing and Detecting Multi-Stage UPI Scam Journeys**.

It is written so Codex can read the full package and implement the project without redesigning the product. The SupportIQ AI package supplied by the project owner was used only as a reference for documentation organization, clarity, separation of concerns, and implementation-instruction style. ScamTrace is a different product with its own scope and architecture.

## Locked Project
- **Project:** UPI ScamTrace
- **Tagline:** Multi-Agent Reconstruction and Detection of Multi-Stage UPI Scam Journeys
- **Primary purpose:** Analyze a sequence of user-provided or synthetic events to identify a possible scam journey, explain the evidence, and provide a safe warning.
- **Target:** Student major-project prototype suitable for a local supervisor demonstration.

## Core Technology Direction
- Python 3.11+
- Streamlit multi-page UI
- LangGraph for real agent orchestration
- Pydantic for validated schemas
- SQLite for local persistence
- NetworkX for temporal evidence graph
- Pandas and Plotly for evaluation/visualization
- pytest for automated tests
- Optional Groq-compatible LLM provider, configurable through environment variables
- Deterministic offline/demo mode as a required capability

Do not add technologies merely to make the stack look impressive. Every component must have a documented purpose and a working implementation.

## Required Product Principle
ScamTrace is an **evidence-oriented scam-journey investigation prototype**, not a generic chatbot or a single-message classifier.

It must:
1. Accept multiple events belonging to one case.
2. Normalize event evidence into a common schema.
3. Build a chronological timeline.
4. Run specialized agents over relevant evidence.
5. Link events using a temporal evidence graph.
6. investigate candidate scam journeys across channels.
7. resolve contradictions and express uncertainty.
8. produce an explainable risk assessment tied to event IDs.
9. update the assessment when new events are added.
10. provide safe next-step guidance.
11. persist cases locally and support export/delete.
12. include synthetic scenarios, evaluation, tests, and complete documentation.

## Critical Implementation Instruction
Build one coherent application. Do not create disconnected agent demos.
Do not put the entire application on one page.
Use explicit separation between UI, services, agents, graph orchestration, parsers, risk logic, and persistence.
Do not silently substitute unrelated fraud detection features for the approved ScamTrace journey-reconstruction scope.

## Must Work
- Local/demo case creation and evidence intake
- Multi-event timeline
- Deterministic analysis without API credentials
- LangGraph workflow with visible agent runs
- Temporal evidence graph and explainable relations
- Sequence-level investigation
- Risk/uncertainty assessment
- SQLite persistence and case reload
- Synthetic scam, benign, and ambiguous scenarios
- Evaluation metrics on labeled synthetic cases
- Export and deletion
- Automated tests and startup smoke test
- UI that can be demonstrated locally

## Optional / Advanced
- Groq-compatible live LLM mode
- OCR for screenshots
- QR image decoding
- Safe URL reputation lookups
These must be optional and must not prevent offline mode from working. Never claim live verification unless a configured source was actually queried.

## Important Demo Principle
Provide fictional synthetic data only. Clearly label it. Do not include real victim information, real credentials, or real payment secrets.

## Final Success Condition
A fresh user can:
1. Install dependencies.
2. Configure `.env` optionally.
3. Run the setup command.
4. Launch Streamlit.
5. Load a synthetic case or create a case.
6. add multiple events.
7. run the multi-agent investigation.
8. inspect timeline, graph, agent findings, and evidence.
9. see a calibrated assessment and safe actions.
10. add another event and observe assessment updates.
11. export and reopen a case.
12. run the tests and inspect the verification report.

## Documentation Reading Order
Read every numbered Markdown file in order, then `MANIFEST.md`. Treat all product/engineering files as authoritative requirements and `20_VERIFICATION_REPORT.md` as the actual verification record populated after implementation. Also inspect `ui_reference_images/` and follow `28_UI_REFERENCE_IMAGE_INDEX.md`.

## Locked UI Requirements
- Theme: Deep Emerald `#142923`, Champagne Gold `#C6A76A`, Warm Ivory `#F5F2EA`.
- Six primary pages: Dashboard, New Investigation, Case History, Analytics, Settings, About Project.
- Case investigation views are nested inside a selected case from Case History; they are not primary sidebar destinations.
- The approved UI PNGs are included in `ui_reference_images/` and are strict implementation targets—not inspiration. Reproduce their visible layouts, labels, colors, and placements faithfully; use screenshot overlay/diff comparisons and iterate.
- No page-level vertical or horizontal scrolling at 1600×900. Do not clip content or hide scrollbars to satisfy this.
- Implement functional controls and restrained transitions; respect reduced-motion.
- Read `08_UI_UX_SPECIFICATION.md`, `27_UI_VISUAL_DESIGN_HANDOFF.md`, and `28_UI_REFERENCE_IMAGE_INDEX.md` before UI work.
- If reference images are missing, report missing filenames; do not claim image-matched verification.

## Streamlit Deployment Target
Build a reproducible Streamlit app suitable for local execution and **Streamlit Community Cloud** hosting. Keep secrets in environment variables locally and Streamlit Secrets in hosted environments. Explicitly document persistence limitations: hosted ephemeral filesystems may not retain SQLite data across restarts/redeploys; use a supported persistent database/storage option for durable hosted cases, or clearly label the hosted demo as non-persistent. Do not claim cloud deployment is verified until deployed and tested.


## Documentation vs. Application
This ZIP is the **specification and Codex build blueprint**, not the runnable application. Codex must create the source code, dependency files, tests, scripts, and local app in the active project workspace. A successful handoff means the app was actually run and verified to the extent recorded in `20_VERIFICATION_REPORT.md`.

## Required Additional Instructions
- Read `26_CODEX_EXECUTION_PROTOCOL_AND_QUALITY_GATES.md` and `27_UI_VISUAL_DESIGN_HANDOFF.md`.
- Create a requirement traceability matrix and keep it current.
- Do not claim Community Cloud deployment or production readiness until the actual hosted app is tested. Follow `31_STREAMLIT_COMMUNITY_CLOUD_DEPLOYMENT.md`.
- The supplied UI images must be used during implementation from the beginning; do not postpone them as optional polish. Match them faithfully while preserving functional behavior and truthful data. No page-level scrolling at 1600×900 is a hard gate.


## Strict UI Match and Hosting Rules
- Treat every PNG in `ui_reference_images/` as the visual source of truth; do not redesign or substitute.
- Match the reference layout, labels, visible sections, selected states, controls, and palette. Capture and compare screenshots at 1600×900 using overlay/diff.
- No page-level vertical/horizontal scrolling at 1600×900; do not hide scrollbars or clip content.
- Deploy target is Streamlit Community Cloud. Read `31_STREAMLIT_COMMUNITY_CLOUD_DEPLOYMENT.md`.
