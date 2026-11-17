# 29. Documentation Coverage from the Attached Reference PDF

## Purpose
The attached 16-page scanned PDF presents a documentation checklist through visual examples. The checklist has been extracted and mapped to ScamTrace documentation requirements below. The PDF itself is not a project feature or required runtime asset; only applicable documentation practices are incorporated.

## Source-Derived Checklist
The PDF pages show these documentation areas: PRD/problem and users (page 1), design/rulebook (page 2), architecture (page 3), database (page 4), API (page 5), agents/rules/guardrails (page 6), README/project overview (page 7), plan/phases (page 8), setup (page 9), features (page 10), authentication (page 11), MCP connection (page 12), integrations (page 13), testing (page 14), debugging (page 15), and a golden-rule/source-of-truth flow (page 16).

## Mapping to ScamTrace
| Reference category | ScamTrace document(s) | Applicability |
|---|---|---|
| PRD: problem, users, core features, journeys, roles, MVP | `01_PRODUCT_REQUIREMENTS.md`, `02_FEATURE_SPECIFICATION.md`, `24_USER_GUIDE_AND_DEMO_SCRIPT.md` | Required |
| Design/rulebook: palette, typography, buttons, UI rules | `08_UI_UX_SPECIFICATION.md`, `27_UI_VISUAL_DESIGN_HANDOFF.md`, `28_UI_REFERENCE_IMAGE_INDEX.md` | Required; includes locked UI references |
| Architecture | `03_ARCHITECTURE.md`, `04_LANGGRAPH_WORKFLOW.md` | Required |
| Database/schema | `09_DATA_MODEL.md` | Required |
| API/module reference | `25_API_AND_MODULE_REFERENCE.md` | Required; update after implementation |
| Agents, rules, guardrails | `07_AGENT_CONTRACTS_AND_PROMPTS.md`, `10_RISK_POLICY_AND_DECISION_LOGIC.md`, `11_SECURITY_PRIVACY_RELIABILITY.md` | Required |
| README/project overview | `00_README_AND_MASTER_INSTRUCTIONS.md` plus generated repository `README.md` | Required |
| Plan/phases | `17_IMPLEMENTATION_INSTRUCTIONS_FOR_CODEX.md`, `26_CODEX_EXECUTION_PROTOCOL_AND_QUALITY_GATES.md` | Required build sequence and gates |
| Setup | `14_DEPLOYMENT_AND_SETUP.md` | Required |
| Features | `02_FEATURE_SPECIFICATION.md`, `08_UI_UX_SPECIFICATION.md` | Required |
| Authentication | `11_SECURITY_PRIVACY_RELIABILITY.md`, `14_DEPLOYMENT_AND_SETUP.md` | Applicability decision required; no fake login. Local student prototype may not require authentication. If exposed to multiple users/public deployment, document and implement real access control before deployment. |
| MCP connection | `03_ARCHITECTURE.md`, `25_API_AND_MODULE_REFERENCE.md` | Not part of approved MVP unless a concrete need is established. Do not add MCP merely to match the reference checklist. Document as out of scope unless implemented. |
| Integrations | `14_DEPLOYMENT_AND_SETUP.md`, `25_API_AND_MODULE_REFERENCE.md`, `11_SECURITY_PRIVACY_RELIABILITY.md` | Optional provider adapter only; external integrations disabled by default and clearly documented |
| Testing | `12_TESTING_AND_ACCEPTANCE.md`, `22_EVALUATION_METHODOLOGY.md`, `20_VERIFICATION_REPORT.md` | Required |
| Debugging/troubleshooting | `30_DEBUGGING_AND_TROUBLESHOOTING.md` | Required |
| Golden rule/source of truth | This file, `00_README_AND_MASTER_INSTRUCTIONS.md`, `26_CODEX_EXECUTION_PROTOCOL_AND_QUALITY_GATES.md`, and `MANIFEST.md` | The numbered docs are authoritative; update cross-references when implementation changes |

## Scope Protection
The PDF is a documentation checklist only, not a request to copy its example app's features or add the PDF as a runtime asset. ScamTrace must not add unrelated posts, users, payment processing, MCP, login, or other features unless independently required by ScamTrace scope.

## Source of Truth Rule
When docs conflict:
1. Approved product scope and safety constraints in `01_PRODUCT_REQUIREMENTS.md`.
2. Functional behavior in `02_FEATURE_SPECIFICATION.md` and `08_UI_UX_SPECIFICATION.md`.
3. Architecture/data contracts in `03`–`16`.
4. UI visual target in `27` and image index `28`.
5. Build/verification process in `17`, `26`, and `20`.
6. `MANIFEST.md` records the current package inventory.

Codex must flag conflicts instead of silently choosing or inventing behavior.
