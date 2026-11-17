# 1. Product Requirements

## 1.1 Product Overview
UPI ScamTrace investigates possible multi-stage UPI scams by reconstructing a sequence of related events—messages, call summaries, links, QR/payment payloads, and payment attempts—and identifying how evidence connects over time.

## 1.2 Problem Statement
Scam events are often assessed individually. A message may be ambiguous, a call summary may be incomplete, and a payment request may appear ordinary. The combination and order of events can reveal an escalating social-engineering journey. ScamTrace aims to represent that sequence, explain the supporting evidence, and warn users before further action.

## 1.3 Intended Users
- Student project demonstrators and evaluators
- A user reviewing a suspected scam incident using evidence they manually provide
- Researchers evaluating sequence-level scam analysis on synthetic datasets

## 1.4 Goals
- Reconstruct a chronological incident journey.
- Identify temporal and cross-channel relationships.
- Explain the risk assessment with traceable evidence.
- Update findings as events are added.
- Demonstrate specialized agents coordinated by LangGraph.
- Work offline using deterministic logic and fixtures.
- Provide responsible, non-alarmist guidance.

## 1.5 Non-Goals
- Direct integration with UPI/bank payment rails.
- Transaction blocking, reversal, recovery, or fund tracing.
- Automatic access to SMS, call logs, contacts, or banking applications.
- Definitive accusation of a person or recipient.
- Law-enforcement reporting automation.
- Production-grade fraud prevention claims.

## 1.6 Functional Requirements
| ID | Requirement | Priority |
|---|---|---|
| FR-01 | Create, edit, reopen, export, and delete a case | Must |
| FR-02 | Add timestamped events of supported types | Must |
| FR-03 | Validate and normalize event input | Must |
| FR-04 | Build a time-ordered timeline | Must |
| FR-05 | Execute specialist agents through LangGraph | Must |
| FR-06 | Construct event/evidence relations | Must |
| FR-07 | Produce sequence-level investigation | Must |
| FR-08 | Show risk, evidence, uncertainty, and safe actions | Must |
| FR-09 | Re-run analysis when evidence changes | Must |
| FR-10 | Provide synthetic demo scenarios | Must |
| FR-11 | Run labeled evaluation and display metrics | Must |
| FR-12 | Operate without LLM credentials | Must |
| FR-13 | Persist agent runs and assessments | Must |
| FR-14 | Validate uploads and sanitize display | Must |
| FR-15 | Provide optional LLM mode with structured outputs | Should |
| FR-16 | Provide optional OCR/QR parsing when available | Could |

## 1.7 Non-Functional Requirements
- Reproducible local setup
- Clear module boundaries
- Schema-validated outputs
- Useful errors and graceful fallback
- No secrets in source or logs
- Reasonable performance for student-scale cases
- Accessible labels and readable warnings
- Testable deterministic core

## 1.8 Success Metrics
- All required acceptance scenarios pass.
- Sequence-level findings cite known event IDs.
- Benign and ambiguous examples are not automatically labeled high concern.
- The same synthetic dataset yields reproducible metrics.
- Offline mode completes the main demo flow.
- Documentation matches the implementation.
