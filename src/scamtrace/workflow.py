from typing import TypedDict
from datetime import datetime, timezone
from langgraph.graph import StateGraph, START, END
from . import agents, database
from .graph import build_graph

class InvestigationState(TypedDict, total=False):
    case_id:str; case:dict; events:list; findings:list; relations:list; assessment:dict; status:str; version:int; errors:list

def _load(s):
    case=database.get_case(s["case_id"])
    if not case: raise ValueError("Case not found")
    return {"case":case,"events":case["events"],"findings":[],"errors":[],"status":"running"}
def _normalize(s):
    events=[]
    for e in s["events"]:
        e=dict(e); e["timestamp"]=e["timestamp"] or datetime.now(timezone.utc).isoformat(); events.append(e)
    return {"events":events}
def _message(s): return {"findings":s["findings"]+[agents.message_analysis(s["events"])]}
def _link(s): return {"findings":s["findings"]+[agents.link_analysis(s["events"])]}
def _payment(s): return {"findings":s["findings"]+[agents.payment_analysis(s["events"])]}
def _timeline(s): return {"findings":s["findings"]+[agents.timeline_analysis(s["events"])]}
def _journey(s): return {"findings":s["findings"]+[agents.journey_analysis(s["events"],s["findings"])]}
def _decision(s): return {"findings":s["findings"]+[agents.decision_analysis(s["events"],s["findings"])]}
def _graph(s):
    _,rel=build_graph(s["events"]); return {"relations":rel}
def _quality(s):
    ids={e["id"] for e in s["events"]}; issues=[]
    for f in s["findings"]:
        for eid in f["evidence_refs"]:
            if eid not in ids: issues.append(f"Unknown evidence reference in {f['agent_name']}")
    return {"errors":issues}
def _risk(s):
    inds=[i for f in s["findings"] for i in f.get("indicators",[])]; material=[i for i in inds if i.get("severity") in ("medium","high")]; codes={i["code"] for i in material}; ev=len(s["events"])
    if ev==0 or (ev==1 and not material): level="INSUFFICIENT_EVIDENCE"; score=0; reason="Too little relevant evidence was provided to assess a pattern."
    elif ev>=2 and ("credential_request" in codes or "repeated_payment_request" in codes or ("impersonation" in codes and "payment_direction_unclear" in codes) or len(codes)>=3): level="HIGH_CONCERN"; score=min(95,65+len(codes)*7); reason="Multiple material indicators appear across a multi-event record."
    elif len(codes)>=2: level="CAUTION"; score=min(70,35+len(codes)*9); reason="Several risk indicators are present; verify independently."
    elif codes: level="CAUTION"; score=38; reason="A limited indicator is present; context is incomplete."
    else: level="LOW_CONCERN"; score=12; reason="No strong rule-based indicators were found in supplied evidence."
    return {"assessment":{"risk_level":level,"score":score,"reason":reason,"reason_codes":sorted(codes),"supporting_event_ids":list(dict.fromkeys(eid for i in material for eid in i["event_ids"])),"uncertainties":["User-provided evidence is not independently verified.","This prototype cannot confirm a transaction, account owner, or fraud."],"alternatives":["Legitimate service communication may use similar wording; verify through an official channel."],"recommendations":["Pause before sending money or sharing information.","Verify independently through an official app or trusted contact.","Never share a PIN, OTP, password, or banking login.","If a payment may have occurred, contact your bank/payment provider through a trusted official route."],"updated_at":datetime.now(timezone.utc).isoformat()}}
def _insufficient(s):
    return {"assessment":{"risk_level":"INSUFFICIENT_EVIDENCE","score":0,"reason":"No events were supplied for investigation.","reason_codes":[],"supporting_event_ids":[],"uncertainties":["There is no case evidence to assess."],"alternatives":[],"recommendations":["Add relevant evidence or verify independently through a trusted official channel."],"updated_at":datetime.now(timezone.utc).isoformat()}}
def _route_after_quality(s): return "handle_insufficient_evidence" if not s.get("events") else "aggregate_risk"
def _explain(s):
    assessment=dict(s.get("assessment") or {"risk_level":"INSUFFICIENT_EVIDENCE","score":0,"reason":"Analysis did not produce enough valid evidence.","supporting_event_ids":[],"uncertainties":["Insufficient evidence."],"recommendations":["Add relevant evidence or verify independently."],"updated_at":datetime.now(timezone.utc).isoformat()})
    assessment["llm_synthesis"]=agents.final_synthesis(s.get("events",[]),s.get("findings",[]),assessment)
    return {"assessment":assessment}
def _persist(s):
    version=int(s["case"].get("analysis_version") or 0)+1
    database.save_analysis(s["case_id"],s["assessment"],s["findings"],s["relations"],version)
    return {"version":version,"status":"completed"}

def build_workflow():
    g=StateGraph(InvestigationState)
    for name,fn in [("load_case",_load),("normalize_events",_normalize),("message_analysis",_message),("link_qr_analysis",_link),("payment_event_analysis",_payment),("timeline_pattern_analysis",_timeline),("build_temporal_graph",_graph),("investigate_journey",_journey),("decision_analysis",_decision),("check_evidence_quality",_quality),("aggregate_risk",_risk),("handle_insufficient_evidence",_insufficient),("generate_explanation",_explain),("persist_results",_persist)]: g.add_node(name,fn)
    chain=["load_case","normalize_events","message_analysis","link_qr_analysis","payment_event_analysis","timeline_pattern_analysis","build_temporal_graph","investigate_journey","decision_analysis","check_evidence_quality"]
    g.add_edge(START,chain[0])
    for a,b in zip(chain,chain[1:]): g.add_edge(a,b)
    g.add_conditional_edges("check_evidence_quality",_route_after_quality,{"handle_insufficient_evidence":"handle_insufficient_evidence","aggregate_risk":"aggregate_risk"})
    g.add_edge("handle_insufficient_evidence","generate_explanation"); g.add_edge("aggregate_risk","generate_explanation")
    g.add_edge("generate_explanation","persist_results"); g.add_edge("persist_results",END)
    return g.compile()

def run_investigation(case_id): return build_workflow().invoke({"case_id":case_id})
