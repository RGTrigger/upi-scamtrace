from itertools import combinations
import networkx as nx

def build_graph(events):
    g=nx.MultiDiGraph(); rel=[]
    ordered=sorted(events,key=lambda e:e.get("timestamp", ""))
    for e in ordered: g.add_node(e["id"],kind="EVENT",event_type=e["event_type"])
    for a,b in zip(ordered,ordered[1:]):
        item={"source":a["id"],"target":b["id"],"relation":"PRECEDES","origin":"rule","confidence":1.0,"evidence_refs":[a["id"],b["id"]],"explanation":"Chronological order from supplied timestamps."}; rel.append(item); g.add_edge(a["id"],b["id"],**item)
    urlmap={}
    for e in events:
        for url in __import__('re').findall(r"(?:https?://|www\.)[^\s,]+",e["content"],__import__('re').I): urlmap.setdefault(url.lower().rstrip('.,)'),[]).append(e["id"])
    for _,ids in urlmap.items():
        for a,b in combinations(ids,2):
            item={"source":a,"target":b,"relation":"REFERENCES_SAME_URL","origin":"parser","confidence":.95,"evidence_refs":[a,b],"explanation":"Exact normalized URL string appears in both supplied events."}; rel.append(item); g.add_edge(a,b,**item)
    return g,rel
