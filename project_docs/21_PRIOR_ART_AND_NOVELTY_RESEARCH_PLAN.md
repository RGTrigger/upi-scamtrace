# 21. Prior Art and Novelty Research Plan

## 21.1 Purpose
ScamTrace is a project direction, not a verified claim of global novelty. The team must investigate close prior work before making novelty claims in the proposal or presentation.

## 21.2 Search Areas
Search for:
- multi-stage scam journey reconstruction
- temporal evidence graphs for payment/social-engineering fraud
- multi-agent scam investigation systems
- UPI scam sequence analysis
- cross-channel scam detection using messages, calls, URLs, QR codes, and payment requests
- scam progression/escalation detection
- graph-based evidence fusion and agent disagreement resolution

## 21.3 Sources to Review
- Research papers and preprints
- Patents
- GitHub and public project repositories
- Product documentation and app features
- Government/bank/payment-provider advisories
- Public datasets and benchmark papers

## 21.4 Novelty Questions
1. Does an existing system reconstruct multi-event UPI scam journeys?
2. Does it build a temporal evidence graph with traceable event-to-event relations?
3. Does it use multiple specialized agents and resolve disagreement?
4. Does it update its assessment incrementally when new events arrive?
5. Does it evaluate sequence-level detection against single-event baselines?
6. Does it provide evidence-grounded explanations and uncertainty?

## 21.5 Defensible Contribution Candidates
Only claim a contribution if implemented and evaluated:
- A specific temporal graph schema and relation-validation method
- Incremental case updates and selective re-analysis
- Evidence provenance/conflict-resolution design
- A synthetic benchmark with sequence-level labels and benign/ambiguous controls
- Comparison of sequence-level vs single-event detection
- Human comprehension evaluation of warnings

## 21.6 Reporting
Maintain a table with source, year, system, overlapping features, differences, and implications. Use precise wording such as “our prototype investigates/evaluates X” rather than “no one has ever built this.”
