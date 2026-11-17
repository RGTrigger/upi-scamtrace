# 5. Temporal Evidence Graph

## 5.1 Purpose
Represent how evidence items and events may relate across time and channels. The graph is a supporting investigative view, not proof that a fraud occurred.

## 5.2 Node Types
- `EVENT`: message, call summary, URL, QR payload, payment request/attempt, note
- `ENTITY`: URL/domain, recipient identifier, phone-like string, amount, claimed organization, app/package name (only if extracted)
- `INDICATOR`: urgency, impersonation claim, credential request, repeated payment, external link, etc.
- `HYPOTHESIS`: candidate scam-journey pattern

## 5.3 Edge Types
- `PRECEDES`
- `REFERENCES_SAME_URL`
- `REFERENCES_SAME_RECIPIENT`
- `SAME_CLAIM_OR_ORGANIZATION`
- `REPEATED_PAYMENT_REQUEST`
- `CHANNEL_SWITCH`
- `POSSIBLE_ESCALATION`
- `SUPPORTS_HYPOTHESIS`
- `CONTRADICTS_HYPOTHESIS`
- `USER_LINKED`

## 5.4 Edge Requirements
Every edge must include:
- source and target IDs
- relation type
- supporting evidence references
- origin (`rule`, `parser`, `agent`, `user`)
- confidence/strength
- explanation
- creation time

Do not infer a relation solely from temporal proximity. Temporal proximity may be one signal but must be labeled as such.

## 5.5 Construction
- Build chronological `PRECEDES` relations from valid timestamps.
- Link exact normalized URLs/recipient identifiers only when equality is supported.
- Add semantic relations only when an agent provides event references and evidence.
- Validate all IDs against the case.
- Deduplicate relations.
- Preserve contradictions rather than silently removing them.

## 5.6 Visualization
Use an interactive graph when feasible; provide a table fallback. Users should be able to inspect edge explanations and supporting events. Use distinct visual encoding for observed links vs inferred links and uncertainty.

## 5.7 Limitations
The graph may be incomplete because evidence is user-provided, timestamps may be inaccurate, identifiers may be spoofed, and the prototype has no privileged UPI network access. A graph connection is not proof of common ownership or criminal activity.
