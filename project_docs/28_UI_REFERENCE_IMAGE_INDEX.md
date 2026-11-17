# 28. UI Reference Image Index — Six Approved Screens

## Binding rule
The six PNGs in `ui_reference_images/` are the **only approved primary UI references** and are the visual source of truth. They are implementation specifications, not inspiration. Codex must reproduce the screens faithfully and must not redesign, simplify, rearrange, or substitute visible elements.

## Approved six-page mapping
| Asset | Page | Main sidebar active state |
|---|---|---|
| `01_dashboard.png` | Dashboard / Home | Dashboard |
| `02_new_investigation.png` | New Investigation / Evidence Intake | New Investigation |
| `03_case_history.png` | Case History | Case History |
| `04_analytics.png` | Analytics — Evidence & Agent Analysis tab active | Analytics |
| `05_settings.png` | Settings | Settings |
| `06_about_project.png` | About Project | About Project |

There are exactly six approved screenshots. Do not add separate Case Investigation or Evidence & Agent Analysis screenshots as additional primary pages. The Case Investigation workspace is opened by selecting a case from Case History. Analytics is a primary sidebar page; its internal tabs include Scam Timeline, Evidence & Agent Analysis, Evidence Graph, Scam Tracker / Journey Tracker, Final Assessment, and Report & Actions as shown/required in the analytics workspace specification. Keep the Analytics sidebar item active when viewing those analytics tabs.

## Exact-match implementation protocol
1. Open each approved PNG at its native dimensions (approximately 1670×941) and inspect all visible content before coding.
2. Create a page-specific layout inventory: sidebar, header, title/subtitle, banners, cards, columns, labels, controls, charts, tables, icons, selected states, alignment, spacing, typography, borders, and shadows.
3. Reproduce the image as closely as possible using functional Streamlit components and custom CSS/components where necessary.
4. Do not use a screenshot as a static background or flatten interactive controls into an image.
5. Keep each approved PNG unchanged in the repository.
6. Capture implementation screenshots at the reference's native dimensions for visual comparison. Also run the no-page-scroll acceptance check at 1600×900.
7. Compare side-by-side and with overlay/diff; iterate until faithful. Record unresolved differences and causes.
8. Treat visible labels and sections as required. If backend behavior is unavailable, preserve placement and show an honest disabled state rather than removing/rearranging the control.
9. Use synthetic demo fixtures for sample records shown in references, clearly labeled as demo data. Do not present sample metrics as real analytics.
10. Never claim exact visual fidelity without recorded screenshot comparison.

## Multi-agent system visibility
The UI should communicate multi-agent operation in these approved locations:
- **Dashboard:** the “Multi-Agent System Status” panel shows the agent roles/status cards, using real workflow state rather than fabricated activity.
- **New Investigation:** the progress sequence indicates evidence intake → AI investigation → scam journey/report; show genuine progress from the workflow.
- **Analytics:** the Evidence & Agent Analysis view shows agent-level performance/findings and evidence-to-agent mapping, derived from evaluation/demo data and clearly labeled.
- **About Project:** the System Architecture diagram and AI Agents (Roles) section explain the orchestration and specialized agents.
- **Settings:** AI & Model Configuration and agent configuration controls reflect actual available settings; do not show nonfunctional toggles as working.

The multi-agent behavior must exist in the backend, not only in the UI: LangGraph should orchestrate specialized agents with defined inputs/outputs, shared case state, evidence references, and a synthesis/decision step. UI status must be tied to actual execution events. Do not fake parallel agents or claim independent agents if the implementation is only one prompt with role labels.

## Asset status
Exactly six approved PNGs belong in `ui_reference_images/`. Remove supplemental workspace images from this folder unless the user separately approves them. Verify file presence and checksums before implementation.
