# 16. AI Output Schemas

## 16.1 Common Agent Result
```json
{
  "agent_name": "message_analysis",
  "status": "success",
  "summary": "Grounded summary",
  "indicators": [
    {
      "code": "URGENT_IMPERSONATION_CLAIM",
      "description": "Possible impersonation/urgency language",
      "severity": "medium",
      "confidence": 0.72,
      "event_ids": ["evt-001"],
      "evidence": ["short excerpt"],
      "origin": "rule"
    }
  ],
  "uncertainties": [],
  "missing_information": []
}
```

## 16.2 Journey Hypothesis
```json
{
  "hypothesis_id": "hyp-001",
  "pattern_name": "refund_to_payment_request",
  "summary": "Candidate journey pattern",
  "steps": [
    {
      "step_number": 1,
      "event_ids": ["evt-001"],
      "observed": "What the event contains",
      "interpretation": "Possible role in journey",
      "confidence": 0.65
    }
  ],
  "supporting_evidence_ids": ["ev-001"],
  "contradicting_evidence_ids": [],
  "alternative_explanations": ["Possible benign explanation"],
  "uncertainties": ["Recipient identity not independently verified"]
}
```

## 16.3 Risk Assessment
```json
{
  "risk_level": "CAUTION",
  "risk_score": null,
  "reason_codes": ["PAYMENT_REQUEST_AFTER_REFUND_CLAIM"],
  "supporting_event_ids": ["evt-001", "evt-002"],
  "summary": "Sequence-level explanation",
  "uncertainties": ["Evidence is user-provided"],
  "recommended_actions": ["Pause and verify through an official channel"]
}
```

## 16.4 Validation Rules
- IDs must exist in the current case.
- Confidence must be within [0,1] if numeric.
- Risk labels must be enumerated.
- No unsupported factual claims.
- Unknown fields rejected or safely ignored according to schema policy.
- Invalid model output triggers bounded retry/fallback.
