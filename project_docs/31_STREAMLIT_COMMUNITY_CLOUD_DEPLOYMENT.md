# 31. Streamlit Community Cloud Deployment — Required Target

## Deployment target
The intended hosting target is **Streamlit Community Cloud**. Do not describe this as “Streamlit project” hosting or substitute another platform unless the project owner explicitly changes the target.

## Repository requirements
Codex must prepare a GitHub repository that Community Cloud can deploy:
- root-level `app.py` as the Streamlit entry point (or document a deliberate alternative and configure the deploy command accordingly)
- root-level `requirements.txt` with compatible, pinned or bounded dependencies
- `.streamlit/config.toml` only for required theme/server settings
- `.streamlit/secrets.toml.example` containing placeholders only; never commit actual secrets
- `.gitignore` excluding `.env`, real secrets, local databases, private evidence uploads, caches, and generated sensitive files
- README with Community Cloud deploy instructions and expected limitations
- synthetic demo data only in the public repository

## Deployment steps to document for the owner
1. Push the verified project to a GitHub repository.
2. Open Streamlit Community Cloud and sign in with GitHub.
3. Create a new app, select the repository, branch, and entry-point file (`app.py`).
4. Configure required secrets in the Community Cloud app settings using the documented key names; do not expose secrets in logs or screenshots.
5. Deploy and inspect build logs for dependency/startup failures.
6. Open the deployed URL and test dashboard, case creation, evidence intake, analysis, case reload, export/delete, and all navigation.
7. Test hosted persistence behavior after app restart/redeploy before claiming cases are durable.
8. Verify UI screenshots and no-scroll behavior at 1600×900 on the deployed app.

## Secrets and provider mode
- App must start without optional LLM credentials in deterministic demo/offline mode.
- Use `st.secrets` for hosted secrets and environment variables locally; centralize configuration.
- Missing/invalid secrets must produce a clear safe message and fall back to demo/offline behavior where supported.
- Never print secrets or place them in client-side HTML.

## Persistence and privacy
Community Cloud local filesystem persistence must not be assumed. SQLite/local files may be ephemeral across restarts or redeploys. For durable multi-session hosted case storage, configure a supported external persistent database/storage service with documented secrets, schema/migrations, access control, and backup considerations. If the project only uses local SQLite, clearly label the hosted app as a non-persistent demo and warn users not to enter real sensitive case data.

## Community Cloud acceptance gate
Do not claim deployed until the app is actually deployed and the following are verified on its live URL:
- successful clean build and startup
- all primary pages and case workspace work
- no secrets exposed
- core synthetic demo flow completes
- persistence claim matches observed behavior
- page layout/no-scroll tested at 1600×900
- logs and verification report contain actual results

Deployment readiness means the repository is prepared and locally verified. “Deployed” means the live Community Cloud deployment was completed and tested. These are different statuses.
