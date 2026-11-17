# 23. Limitations and Failure Modes

## 23.1 Evidence Limitations
- Inputs are user-provided or synthetic and may be incomplete, inaccurate, or manipulated.
- Call summaries are not verified recordings.
- Screenshots/OCR may contain extraction errors.
- URLs and QR payloads do not prove who controls a destination.
- Recipient identifiers may be spoofed or reassigned.

## 23.2 Model Limitations
- LLMs may hallucinate or misinterpret language.
- Hindi/Hinglish support may vary by model and test coverage.
- Agents may disagree or miss subtle context.
- Synthetic evaluation does not establish field performance.
- Risk labels are not calibrated probabilities unless a separate calibration study is performed.

## 23.3 Operational Limitations
- No direct access to UPI/bank transaction systems.
- No transaction blocking, reversal, or recovery.
- No automatic SMS/call-log access.
- External reputation checks are optional and may be unavailable.
- Local storage means data remains on the machine unless exported/deleted.

## 23.4 Failure Handling
- Parser failure: retain safely stored source and mark extraction unavailable.
- Agent failure: show partial analysis and identify failed component.
- LLM unavailable: use offline mode.
- Graph render failure: show relation table.
- Insufficient evidence: do not force a risk label.
- Conflicting signals: show conflict and lower certainty.

## 23.5 User Guidance
The tool should encourage independent verification through official channels and must not encourage confrontation or risky investigative behavior.
