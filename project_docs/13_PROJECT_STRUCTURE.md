# 13. Project Structure

## 13.1 Required Structure
```text
upi-scamtrace/
├── app.py
├── ui_reference_images/
│   ├── README.md
│   ├── 01_dashboard.png
│   ├── 02_new_investigation.png
│   ├── 03_case_history.png
│   ├── 04_analytics.png
│   ├── 05_settings.png
│   └── 06_about_project.png
├── src/
│   └── scamtrace/
│       ├── config/
│       ├── models/
│       ├── database/
│       ├── repositories/
│       ├── services/
│       ├── parsers/
│       ├── agents/
│       ├── graph/
│       ├── workflow/
│       ├── risk/
│       ├── evaluation/
│       ├── integrations/
│       ├── ui/
│       │   ├── components/
│       │   ├── pages/
│       │   ├── case_workspace/
│       │   └── theme/
│       └── utils/
├── sample_data/
├── tests/
│   ├── unit/
│   ├── agents/
│   ├── integration/
│   ├── e2e/
│   └── ui/
├── docs/
├── reports/
├── scripts/
├── .env.example
├── requirements.txt or pyproject.toml
├── README.md
└── CHANGELOG.md
```

## 13.2 Structure Rules
- Keep `app.py` limited to app entry and the approved six-page navigation shell.
- Pages call services, not raw SQL or agent prompts. Case workspace tabs are nested under Case History.
- Agents return validated schemas.
- Repositories own database access.
- Workflow owns orchestration.
- Risk policy is deterministic and testable.
- Parsers do not make risk decisions.
- Evaluation code is separate from UI.
- Avoid circular imports and duplicated logic.
