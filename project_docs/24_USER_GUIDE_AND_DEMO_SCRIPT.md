# 24. User Guide and Supervisor Demo Script

## 24.1 Start the App
Follow `14_DEPLOYMENT_AND_SETUP.md` and the root README. Confirm the UI indicates offline/demo or configured LLM mode.

## 24.2 Recommended 4-Minute Demo
1. Open Dashboard and point out local/demo mode and synthetic case labels.
2. Load the multi-channel scam journey scenario.
3. Open the case from Case History, then show its Timeline and the sequence of message, call summary, link, and payment request.
4. Run the investigation and show the specialized agents and LangGraph workflow.
5. Open the temporal evidence graph and inspect a relation’s supporting event IDs.
6. Show the sequence-level risk assessment, uncertainties, and safe next steps.
7. Add a new escalation event and rerun; show assessment update.
8. Load a benign or ambiguous case to demonstrate false-positive/uncertainty handling.
9. Open Analytics and explain the synthetic evaluation metrics, dataset scope, and limitations.

## 24.3 What to Say
“ScamTrace does not try to decide based on one message alone. It reconstructs the sequence of events, links evidence across channels, and explains why the combined pattern may be concerning. This is a student prototype using synthetic and user-provided evidence, not a live UPI integration.”

## 24.4 Troubleshooting
- If LLM key is absent, use offline mode.
- If graph display fails, use the relation table.
- If a case fails, use a seeded scenario and inspect agent errors.
- Do not demo real credentials, PINs, OTPs, or private victim information.
