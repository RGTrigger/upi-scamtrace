import os
import pytest

@pytest.fixture(autouse=True)
def isolated_db(tmp_path,monkeypatch):
    monkeypatch.setenv("SCAMTRACE_LLM_PROVIDER","offline")
    from scamtrace import database
    monkeypatch.setattr(database,"DB_PATH",tmp_path/"test.db")
    database.init_db()
