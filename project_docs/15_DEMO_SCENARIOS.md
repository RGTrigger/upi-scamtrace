# 15. Demo Scenarios and Synthetic Dataset

## 15.1 Dataset Rules
- All cases are synthetic and fictional.
- Use clearly fake domains and recipient identifiers.
- Include labels and expected findings.
- Include benign and ambiguous cases to test false positives.
- Do not use real victims or private identifiers.

## 15.2 Required Scenarios
### S01 — Fake Refund / Receive-Money Deception
A message claims the user is receiving a refund, followed by a payment request that would debit the user. Expected: intent/action conflict and sequence concern.

### S02 — Electricity Disconnection Impersonation
Urgent message, call summary, external link, and payment request. Expected: cross-channel sequence warning.

### S03 — Fake Bank/KYC Support
A support impersonation claim asks the user to install an app or share credentials. Expected: coercion/credential indicators and safe warning.

### S04 — QR Payment Deception
User believes a QR is for receiving money, but payload represents a payment action. Expected: parsed fields and mismatch warning only if supported by payload/user intent.

### S05 — Repeated Payment Escalation
An initial payment attempt is followed by failed/refund claims and additional requests. Expected: repeated/escalation pattern.

### S06 — Benign Rent Payment
Known-context rent payment without pressure indicators. Expected: low concern or insufficient evidence, not high concern.

### S07 — Benign Merchant Payment
Ordinary merchant payment request. Expected: no unsupported warning.

### S08 — Ambiguous Incomplete Case
Partial message and missing recipient/action details. Expected: insufficient evidence and verification guidance.

### S09 — False-Positive Challenge
Legitimate urgent message or unfamiliar recipient without corroborating scam signals. Expected: caution at most, with uncertainty.

### S10 — Multi-Channel Scam Journey
Message → call summary → link → payment request across timestamps. Expected: timeline and graph connections with supporting event IDs.

## 15.3 Demo Presentation
Show one synthetic scam case, inspect individual events, run agents, view temporal graph, explain the sequence assessment, add a new event, rerun, then contrast with a benign/ambiguous case.
