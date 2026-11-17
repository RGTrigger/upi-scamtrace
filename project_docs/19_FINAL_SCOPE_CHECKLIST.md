# 19. Final Scope Checklist

## Product
- [ ] Multi-stage UPI scam journey reconstruction is the central workflow.
- [ ] Case creation, event intake, timeline, graph, investigation, assessment, demo, evaluation, and settings pages exist.
- [ ] Benign and ambiguous cases are supported.
- [ ] New events update the analysis.
- [ ] Case persistence, export, and delete work.

## Multi-Agent Architecture
- [ ] Specialist agents have distinct responsibilities.
- [ ] LangGraph actually orchestrates them.
- [ ] Agent outputs use validated schemas.
- [ ] Findings reference valid event/evidence IDs.
- [ ] Conflict and insufficient-evidence paths work.
- [ ] Offline mode runs without an API key.

## Safety and Privacy
- [ ] No payment execution or transaction access.
- [ ] No PIN/OTP/password collection.
- [ ] Uploaded content treated as untrusted.
- [ ] Upload limits and sanitization implemented.
- [ ] No secrets in repository.
- [ ] Disclaimer visible.
- [ ] Synthetic data clearly labeled.

## Testing and Evaluation
- [ ] Required synthetic scenarios included.
- [ ] Unit tests implemented and run.
- [ ] Agent contract tests implemented and run.
- [ ] LangGraph integration tests implemented and run.
- [ ] Persistence/export/delete tests pass.
- [ ] Evaluation metrics are reproducible.
- [ ] Verification report reflects actual results.

## Documentation
- [ ] All numbered Markdown files exist.
- [ ] Root README matches implementation.
- [ ] Setup commands tested.
- [ ] Architecture/workflow diagrams match code.
- [ ] Limitations and prior-art caveats are explicit.
- [ ] No feature is documented as complete unless implemented.

## Supervisor Demo
- [ ] App launches from a clean environment.
- [ ] Synthetic case loads.
- [ ] Timeline and graph render.
- [ ] Agent outputs visible.
- [ ] Assessment cites evidence.
- [ ] New event updates assessment.
- [ ] Benign/ambiguous contrast shown.

## UI and Deployment
- [ ] Six primary UI pages match approved reference assets.
- [ ] Case investigation workspace is nested under Case History.
- [ ] Locked Emerald/Champagne/Ivory palette is consistent.
- [ ] No page-level scrolling at the documented target viewport.
- [ ] Functional controls and restrained transitions are implemented.
- [ ] Streamlit deployment steps and persistence caveats are documented.
