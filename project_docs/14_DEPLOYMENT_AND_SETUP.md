# 14. Deployment and Setup

## 14.1 Supported Initial Environment
Local development on Windows, with Linux/macOS instructions where practical. Python 3.11+ recommended.

## 14.2 Setup Requirements
- Python
- Git (optional if project is downloaded as ZIP)
- Internet for dependency installation
- Optional LLM API key for live model mode

## 14.3 Expected Setup
Codex must create exact platform-appropriate instructions and scripts. Suggested commands:

### Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```

### Linux/macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

## 14.4 Environment Variables
Document provider, model, API key, database path, mode, and optional service settings in `.env.example`. All secrets must be placeholders.

## 14.5 Offline Mode
The app must run without `.env` or API key using deterministic agents and synthetic scenarios. Show the current mode in the UI.

## 14.6 Troubleshooting
Document dependency failures, port conflicts, missing API key, model errors, database initialization, upload limitations, and graph rendering fallback.

## 14.7 Deployment
Local execution is required for development and testing. The intended hosted target is **Streamlit Community Cloud**. Follow `31_STREAMLIT_COMMUNITY_CLOUD_DEPLOYMENT.md`; do not substitute another platform or claim deployment without live verification.


## 14.8 Streamlit Hosting Readiness
The app must be structured so it can be deployed to Streamlit hosting after local verification.

### Hosting requirements
- Provide a valid root `app.py` entry point.
- Pin compatible dependencies in `requirements.txt` or `pyproject.toml`.
- Keep secrets out of source control. Local development uses `.env`; hosted deployment uses Streamlit Secrets.
- Provide `.streamlit/config.toml` only when needed and document every setting.
- Do not assume a local filesystem path exists on the hosted platform.
- Keep provider/model configuration optional; hosted app must show a safe offline/demo mode if secrets are absent.
- Document the deployment steps and required secrets in the root README.

### Persistence warning
Streamlit-hosted environments may use ephemeral local storage. SQLite is suitable for local demos but must not be presented as durable hosted storage unless persistence has been verified. For a hosted deployment that must retain user cases, use a persistent database/storage service with documented credentials, migrations, access controls, and backup behavior. If only SQLite is configured, label hosted deployment as demo/non-persistent and warn users before entering case data.

### Deployment verification
Only report “deployed” after:
1. The app is actually deployed to the target Streamlit environment.
2. Startup and core workflow are tested on the deployed URL.
3. Secrets configuration is verified without exposing values.
4. Persistence behavior is tested and documented.
5. UI layout and no-scroll behavior are checked at the target viewport.


## 14.9 Streamlit Community Cloud (Required Hosting Target)
Read `31_STREAMLIT_COMMUNITY_CLOUD_DEPLOYMENT.md`. Prepare the GitHub repository, root `app.py`, `requirements.txt`, safe `.streamlit` configuration, secrets instructions, `.gitignore`, and hosted persistence warning. Community Cloud local files must not be assumed durable. Deploy and test the live URL before reporting deployed status.
