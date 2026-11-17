# 12. Testing and Acceptance

## 12.1 Testing Layers
- Unit tests: schemas, parsers, normalization, graph relations, risk policy, sanitization
- Agent contract tests: schema validity, event references, uncertainty, no invented fields
- LangGraph integration tests: normal path, fallback, errors, disagreement, new-event rerun
- Database tests: persistence, reload, versioning, deletion, export
- UI smoke tests: import/startup and core page/service functions
- End-to-end tests: complete demo workflows

## 12.2 Required Test Cases
1. Fake refund claim followed by debit request → sequence warning with event references.
2. Electricity impersonation message + link + payment request → multi-event concern.
3. KYC/support impersonation with app-install pressure → warning; no executable artifact.
4. QR/payment URI with receive-money deception → parsed fields and uncertainty.
5. Repeated payment escalation → escalation indicator.
6. Benign rent payment → no unsupported high concern.
7. Benign merchant payment → no unsupported high concern.
8. Ambiguous incomplete case → insufficient evidence/caution.
9. Legitimate urgent message without other indicators → avoid false high-risk classification.
10. Multi-channel sequence → timeline and graph relationships.
11. Agent output references unknown event ID → reject/flag.
12. Malformed LLM output → bounded fallback/error.
13. LLM unavailable → offline workflow completes.
14. New event added → assessment version updates.
15. Export case → no secrets.
16. Delete case → related records removed.
17. Unsafe/oversized upload → rejected.
18. Prompt injection in evidence → treated as content, not instruction.

## 12.3 Acceptance Criteria
- Core workflow runs offline.
- Required pages render.
- Agents execute through LangGraph.
- Findings are evidence-grounded.
- Graph relations have explanations.
- Benign/ambiguous scenarios are handled responsibly.
- Cases persist and reopen.
- Evaluation is reproducible.
- Tests are executed and actual outcomes recorded.

## 12.4 Verification Honesty
Codex must report exact commands, pass/fail/skip counts, and manual checks. Do not claim browser testing or live provider validation unless performed. Keep the verification report current.


## 12.5 UI-Specific Acceptance Tests
1. Verify all six primary pages render and the active sidebar state is correct.
2. Verify Case Investigation is opened from Case History and its tabs are secondary navigation, not sidebar items.
3. Verify every visible button, tab, filter, row action, dialog, and navigation control performs its advertised action.
4. Compare each running-app screenshot with the corresponding approved reference image at 1600×900.
5. Verify the locked theme tokens are used consistently: `#142923`, `#C6A76A`, `#F5F2EA`.
6. Verify no page-level vertical or horizontal scrolling at 1600×900; no clipping or hidden content is allowed.
7. Verify narrow viewport reflow and document the minimum supported viewport.
8. Verify transitions are restrained and reduced-motion is respected.
9. Verify empty, loading, partial, error, offline, and insufficient-evidence states.
10. Verify analytics are computed from stored/evaluation data and empty states do not show fabricated metrics.
11. Verify all synthetic content is visibly labeled.
12. Record screenshots, viewport, pass/fail, and limitations in `20_VERIFICATION_REPORT.md`.
