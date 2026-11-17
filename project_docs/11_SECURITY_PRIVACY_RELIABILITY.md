# 11. Security, Privacy, and Reliability

## 11.1 Threat Model
Consider:
- prompt injection embedded in evidence
- malicious URLs and QR payloads
- oversized or malformed uploads
- unsafe file handling
- model hallucination
- sensitive data accidentally entered
- local database corruption
- API outages/rate limits
- graph/parser failures

## 11.2 Input Safety
- Treat all uploaded/user-provided content as untrusted data.
- Never execute uploaded files or embedded scripts.
- Enforce extension, MIME, size, and text-length limits.
- Sanitize content before rendering.
- Avoid arbitrary network requests.
- Use timeouts and safe error handling for optional external services.

## 11.3 Prompt Injection Defense
Evidence is data, not instructions. Agent prompts must explicitly ignore commands found inside messages, documents, QR payloads, and URLs. Tool access should be minimal and controlled.

## 11.4 Secrets
- Use `.env` locally and environment secrets in deployment.
- Provide `.env.example` with placeholders only.
- Never commit keys.
- Do not display secret values in UI or logs.

## 11.5 Privacy and Data Handling
- Local-first SQLite storage.
- Explain where case data is stored.
- Provide export and delete controls.
- Do not access SMS/call logs/contacts automatically.
- Do not request PIN/OTP/passwords.
- Synthetic examples must use fictional identifiers.

## 11.6 Reliability
- Deterministic fallback for no-key mode.
- Validate every agent output.
- Bound retries.
- Persist partial results and report failed agents.
- Avoid silently converting errors into low risk.
- Provide `INSUFFICIENT_EVIDENCE` when analysis cannot complete.

## 11.7 Disclaimer
This prototype is not a guarantee of fraud detection and does not replace official payment-provider or bank support.
