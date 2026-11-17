# 6. Data Sources and Parsing

## 6.1 Allowed Inputs
- User-entered text
- User-entered call summaries
- User-provided URLs
- QR payload text or uploaded QR image if decoding is implemented
- Simulated payment request fields
- Synthetic scenario files
- User-uploaded text/CSV/image files only where supported

## 6.2 Source Provenance
Every event must record source type and provenance. Distinguish:
- user-entered
- uploaded file
- synthetic demo
- deterministic parser extraction
- model-generated inference

Do not describe user input as independently verified.

## 6.3 URL Parsing
Default to offline parsing:
- normalize scheme/host safely
- extract domain and path indicators
- detect obvious obfuscation patterns
- do not automatically open or fetch arbitrary URLs
- no unsafe redirects or downloads
- any optional reputation service must be separately configured and documented

## 6.4 QR Parsing
If QR image decoding is implemented:
- validate file type/size
- decode payload only; never execute content
- parse payment URI fields as untrusted strings
- explain what was extracted and what was not verified
- provide text-payload input as a fallback

## 6.5 Payment URI Parsing
Parse supported UPI-like URI fields only as provided in the artifact. The parser may extract payee identifier, name, amount, note, and action semantics if present. Do not assume that a parsed URI proves the recipient is legitimate or that the payment was completed.

## 6.6 OCR
OCR is optional. If included:
- show extracted text for user review
- indicate OCR uncertainty
- never silently treat OCR output as ground truth
- provide manual correction
- test low-quality and malformed images

## 6.7 Input Limits
Document and enforce maximum upload size, event count per case, text length, accepted extensions, and image dimensions. Reject unsupported files with clear messages.
