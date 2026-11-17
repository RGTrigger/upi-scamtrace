# 10. Risk Policy and Decision Logic

## 10.1 Risk Labels
- `LOW_CONCERN`: no strong suspicious sequence found in supplied evidence
- `CAUTION`: one or more indicators; evidence is incomplete or ambiguous
- `HIGH_CONCERN`: multiple independent, grounded indicators form a concerning sequence
- `INSUFFICIENT_EVIDENCE`: too little or too unreliable evidence to assess

These labels describe the prototype’s assessment, not an authoritative fraud determination.

## 10.2 Aggregation Principles
- Prefer multiple independent indicators over repeated copies of the same signal.
- Consider sequence and escalation, but do not treat temporal proximity alone as proof.
- Account for benign explanations.
- Downgrade when provenance is weak or agents conflict materially.
- Use `INSUFFICIENT_EVIDENCE` when required fields or evidence are absent.
- Avoid using an uncalibrated numeric score as a probability.

## 10.3 Reason Codes
Examples:
- `URGENT_IMPERSONATION_CLAIM`
- `EXTERNAL_LINK_AFTER_PRESSURE`
- `PAYMENT_REQUEST_AFTER_REFUND_CLAIM`
- `REPEATED_PAYMENT_ESCALATION`
- `CREDENTIAL_OR_PIN_REQUEST`
- `CHANNEL_SWITCH_WITH_PRESSURE`
- `RECIPIENT_OR_AMOUNT_REPEATED`
- `CONFLICTING_OR_INCOMPLETE_EVIDENCE`

## 10.4 Explainability
Every assessment must include:
- what was observed
- which event IDs support it
- what was inferred
- what remains uncertain
- safe next steps

## 10.5 Recommendation Safety
Recommendations may include pausing, independently verifying through official contact channels, not sharing credentials, and contacting the bank/provider if money was sent. Never promise recovery or instruct the user to confront an alleged scammer.
