import sys
import tempfile
import os
from pathlib import Path
os.environ["SCAMTRACE_LLM_PROVIDER"]="offline"
sys.path.insert(0,str(Path(__file__).parent/'src'))
from scamtrace import database
from scamtrace.workflow import run_investigation
from scamtrace.scenarios import scenarios

with tempfile.TemporaryDirectory(prefix="scamtrace-eval-") as tmp:
    database.DB_PATH=Path(tmp)/"evaluation.db"
    database.init_db()
    correct=0
    for item in scenarios():
        cid=database.create_case(item['title'],item['summary'],True,item['events'])
        result=run_investigation(cid); pred=result['assessment']['risk_level']; ok=pred==item['expected_risk']; correct+=ok
        print(f"{item['title']}: expected={item['expected_risk']} predicted={pred} {'PASS' if ok else 'MISMATCH'}")
    print(f"Synthetic scenario accuracy: {correct}/{len(scenarios())} ({correct/len(scenarios()):.0%}); small fixture set, not a validated performance claim.")
