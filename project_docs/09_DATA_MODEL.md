# 9. Data Model

## 9.1 Core Entities
### Case
- `case_id` (UUID/string primary key)
- `title`
- `created_at`
- `updated_at`
- `status`
- `user_summary`
- `language`
- `source_mode` (`synthetic`, `user_supplied`, `mixed`)
- `latest_assessment_id`

### Event
- `event_id`
- `case_id`
- `timestamp` (nullable if unknown; preserve timezone)
- `event_type`
- `channel`
- `description`
- `raw_payload` (safely stored; sensitive fields filtered)
- `source_type`
- `source_filename` (optional)
- `normalization_status`
- `extracted_fields` (JSON)
- `created_at`

### Evidence
- `evidence_id`
- `case_id`
- `event_id`
- `agent_name`
- `indicator_code`
- `description`
- `evidence_excerpt_or_field`
- `severity`
- `confidence`
- `origin`
- `created_at`

### AgentRun
- `run_id`
- `case_id`
- `analysis_version`
- `agent_name`
- `status`
- `started_at`
- `completed_at`
- `structured_output` (JSON)
- `error_summary`

### GraphRelation
- `relation_id`
- `case_id`
- `source_node_id`
- `target_node_id`
- `relation_type`
- `supporting_evidence_ids` (JSON)
- `origin`
- `confidence`
- `explanation`

### Assessment
- `assessment_id`
- `case_id`
- `analysis_version`
- `risk_level`
- `risk_score` (optional; document meaning)
- `reason_codes` (JSON)
- `supporting_event_ids` (JSON)
- `uncertainties` (JSON)
- `candidate_journey`
- `recommended_actions` (JSON)
- `created_at`

## 9.2 Data Integrity
- Foreign keys enabled.
- Validate IDs before relation insertion.
- Preserve event history across analysis runs.
- New analysis creates a versioned assessment.
- Delete case removes associated records transactionally.
- Export should not contain credentials or secrets.

## 9.3 Privacy
Never request/store UPI PIN, OTP, passwords, bank login credentials, or full card numbers. Mask sensitive patterns where feasible and warn users not to submit them.
