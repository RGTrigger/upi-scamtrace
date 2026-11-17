import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from scamtrace import database
from scamtrace.workflow import run_investigation
from scamtrace.scenarios import scenarios
from scamtrace.graph import build_graph

def test_langgraph_runs_specialists_and_persists_assessment():
    demo=scenarios()[1]
    cid=database.create_case(demo['title'],demo['summary'],True,demo['events'])
    result=run_investigation(cid)
    assert result['status']=="completed"
    assert len(result['findings'])==6
    assert result['assessment']['risk_level']=="HIGH_CONCERN"
    assert result['assessment']['llm_synthesis']['status']=="fallback"
    assert result['assessment']['llm_synthesis']['provider']=="local"
    case=database.get_case(cid)
    assert case['assessment']['supporting_event_ids']
    assert all(i in {e['id'] for e in case['events']} for f in case['findings'] for i in f['evidence_refs'])

def test_benign_case_is_not_high_concern():
    demo=next(x for x in scenarios() if x['title']=="Benign Rent Payment")
    cid=database.create_case(demo['title'],demo['summary'],True,demo['events'])
    result=run_investigation(cid)
    assert result['assessment']['risk_level']=="LOW_CONCERN"

def test_graph_relations_are_grounded_and_ordered():
    events=[{"id":"E1","timestamp":"2026-01-01T00:00:00+00:00","event_type":"message","content":"visit https://example.invalid/a","channel":"SMS"},{"id":"E2","timestamp":"2026-01-02T00:00:00+00:00","event_type":"url","content":"https://example.invalid/a","channel":"Web"}]
    _,relations=build_graph(events)
    assert {r['relation'] for r in relations}=={"PRECEDES","REFERENCES_SAME_URL"}
    assert all(set(r['evidence_refs']) <= {"E1","E2"} for r in relations)

def test_all_synthetic_scenarios_match_expected_rule_labels():
    for demo in scenarios():
        cid=database.create_case(demo['title'],demo['summary'],True,demo['events'])
        result=run_investigation(cid)
        assert result['assessment']['risk_level']==demo['expected_risk'],demo['title']

def test_new_evidence_updates_version_and_assessment():
    cid=database.create_case("Update test","",False,[{"event_type":"note","content":"A person called, context unknown."}])
    first=run_investigation(cid)
    assert first['assessment']['risk_level']=="INSUFFICIENT_EVIDENCE"
    database.add_event(cid,{"event_type":"message","content":"Share your OTP immediately.","channel":"SMS"})
    second=run_investigation(cid)
    assert second['version']==first['version']+1
    assert second['assessment']['risk_level']=="HIGH_CONCERN"
    reopened=database.get_case(cid)
    assert len(reopened['events'])==2 and reopened['analysis_version']==2

def test_uploaded_attachment_is_retained_and_accessible():
    cid=database.create_case("Attachment test")
    eid=database.add_event(cid,{"event_type":"other","content":"Image evidence; OCR unavailable.","attachment":{"filename":"sample.png","mime_type":"image/png","data":b"fake-image-bytes"}})
    attachment=database.get_attachments(cid)[0]
    assert attachment['event_id']==eid and attachment['filename']=="sample.png"
    assert attachment['data']==b"fake-image-bytes"

def test_event_fields_and_default_view_setting_round_trip():
    cid=database.create_case("Structured evidence")
    fields={"url":"https://example.invalid/login","context":"SMS link"}
    database.add_event(cid,{"event_type":"url","content":fields["url"],"fields":fields})
    reopened=database.get_case(cid)
    assert reopened["events"][0]["fields"]==fields
    database.set_setting("default_view","Analytics")
    assert database.get_setting("default_view")=="Analytics"
    assert database.get_setting("missing","Dashboard")=="Dashboard"
