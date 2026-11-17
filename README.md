# UPI ScamTrace

**Multi-Agent Scam Journey Reconstruction** — an evidence-oriented prototype that reconstructs user-provided evidence as an ordered journey and explains a cautious, rule-based risk assessment with optional Groq synthesis.

## What it does

- Create and persist cases and timestamped evidence in local SQLite.
- Run six distinct specialist nodes through LangGraph: Message, Link & QR, Payment, Timeline, Journey, and Decision. Message/payment classification can use Groq GPT-OSS 20B; complex journey reasoning and final synthesis use GPT-OSS 120B by default. Link parsing, timeline relations, and the risk score remain local and deterministic.
- Store uploaded image attachments locally in SQLite and download them from the case report view; OCR and QR image decoding are not included.
- Build a NetworkX evidence graph with chronological and exact URL relations, each grounded in event IDs.
- Review an ordered timeline, findings, uncertainty, candidate scam stages, final assessment, and exportable Markdown/JSON reports.
- Use a single Groq API key across the online agent calls, or run without credentials in a clearly labeled local deterministic fallback. Missing keys, invalid structured responses, API errors, timeouts, and rate limits fall back per agent and are recorded with findings.
- RAG is not part of this build: case evidence is analyzed directly, and there is no trusted reference corpus to retrieve from. A curated, source-cited policy/guidance library can be added later without treating retrieved material as case evidence.
- Load explicitly labeled synthetic scenarios and run the tiny deterministic evaluation set in forced offline mode.

This is not affiliated with UPI or any bank. It cannot access payment rails, identify account owners, block/reverse payments, or independently verify user evidence. Never submit PINs, OTPs, passwords, or banking credentials. Local database contents may be sensitive.

## Requirements and local setup

Python 3.11+ is the documented target. A compatible Python runtime and pip are required.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env locally and set GROQ_API_KEY to a freshly generated key.
streamlit run app.py
```

macOS/Linux:

```bash
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env locally and set GROQ_API_KEY to a freshly generated key.
streamlit run app.py
```

The app creates `data/scamtrace.db` on first run. `SCAMTRACE_DB_PATH` can point elsewhere. The `.env` file is ignored by Git. You can also set `GROQ_API_KEY` in the process environment or Streamlit secrets. If the key is missing or `SCAMTRACE_LLM_PROVIDER=offline`, the app uses the local deterministic fallback. It never displays or stores the key in case data.

If an API key is accidentally shared in chat, logs, or a committed file, revoke it with Groq and create a replacement before enabling online calls. Do not paste API keys into source files or support chats.

Model routing is configurable without editing code:

| Variable | Default | Use |
|---|---|---|
| `SCAMTRACE_LLM_PROVIDER` | `groq` | `groq` or `offline`; missing Groq credentials activate fallback |
| `SCAMTRACE_COMPLEX_MODEL` | `openai/gpt-oss-120b` | Journey reasoning and final synthesis |
| `SCAMTRACE_SIMPLE_MODEL` | `openai/gpt-oss-20b` | Message/payment classification |
| `SCAMTRACE_USE_SMALL_MODEL` | `true` | Set `false` to use local rules for simple agents |
| `GROQ_API_KEY` | unset | One Groq credential shared by the separate Groq-backed agent calls |

When Groq mode is active, submitted evidence text is sent to Groq for the enabled agents. Attachments are not sent as images; OCR and QR-image decoding remain unavailable. The rule-based score and safety thresholds are not changed by model generated synthesis.

## Demo and evaluation

Select **View Demo** on Dashboard to load and investigate ten labeled synthetic cases covering scam, benign, ambiguous, and false-positive controls. Open a case from Case History and inspect all six nested investigation views. Use **Run / Update Investigation** after adding new evidence. To run the reproducible synthetic fixture evaluation:

```bash
python run_evaluation.py
```

The fixture set is intentionally tiny and is not evidence of real-world accuracy or calibrated fraud probability.

## Tests

```bash
python -m pytest
python -m compileall src app.py
```

## Streamlit Community Cloud

This repository is prepared for Community Cloud with root `app.py`, `requirements.txt`, `.streamlit/config.toml`, and placeholder-only `.streamlit/secrets.toml.example`.

1. Push the repository to GitHub.
2. In Streamlit Community Cloud, create an app from the repository, branch, and `app.py` entry point.
3. Add `GROQ_API_KEY` and the `SCAMTRACE_*` model settings in the app's Secrets settings; leave the key unset for local fallback mode.
4. Deploy and check build logs, primary pages, a synthetic investigation, export/delete, and browser layout.
5. Treat SQLite data as ephemeral on hosted infrastructure. Do not enter real sensitive evidence in a public hosted demo. Durable hosted persistence and public access controls are not implemented.

Deployment is prepared but has not been performed or verified.

## Project structure

```text
app.py                         Streamlit entry point and page composition
src/scamtrace/models.py        Pydantic contracts
src/scamtrace/database.py      SQLite persistence
src/scamtrace/agents.py        Specialist agents and local fallback behavior
src/scamtrace/providers.py     Groq configuration, structured calls, and safe failure handling
src/scamtrace/workflow.py      LangGraph workflow and synthesis
src/scamtrace/graph.py         Temporal evidence graph
src/scamtrace/scenarios.py     Labeled synthetic fixtures
tests/                         Automated core/workflow tests
project_docs/                  Original extracted specification and six UI references
docs/                           Traceability and implementation notes
```

The original uploaded ZIP is preserved in the project root. Its extracted documentation and image assets are retained under `project_docs/`.
