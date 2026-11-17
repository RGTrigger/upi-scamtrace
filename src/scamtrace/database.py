import json, os, sqlite3
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime, timezone
from .models import Event

DB_PATH = Path(os.getenv("SCAMTRACE_DB_PATH", "data/scamtrace.db"))

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    return con

@contextmanager
def db():
    con=connect()
    try:
        with con:
            yield con
    finally:
        con.close()

def init_db():
    with db() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS cases(id TEXT PRIMARY KEY,title TEXT NOT NULL,summary TEXT DEFAULT '',created_at TEXT,updated_at TEXT,status TEXT DEFAULT 'New',synthetic INTEGER DEFAULT 0,assessment TEXT,analysis_version INTEGER DEFAULT 0,findings TEXT,relations TEXT);
        CREATE TABLE IF NOT EXISTS events(id TEXT PRIMARY KEY,case_id TEXT NOT NULL REFERENCES cases(id) ON DELETE CASCADE,timestamp TEXT,event_type TEXT,channel TEXT,content TEXT,source TEXT,fields TEXT);
        CREATE TABLE IF NOT EXISTS attachments(id INTEGER PRIMARY KEY AUTOINCREMENT,event_id TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE,filename TEXT,mime_type TEXT,size_bytes INTEGER,data BLOB NOT NULL);
        CREATE TABLE IF NOT EXISTS runs(id INTEGER PRIMARY KEY AUTOINCREMENT,case_id TEXT,created_at TEXT,result TEXT);
        CREATE TABLE IF NOT EXISTS app_settings(key TEXT PRIMARY KEY,value TEXT NOT NULL);
        """)

def list_cases():
    with db() as c:
        rows=[dict(r) for r in c.execute("SELECT * FROM cases ORDER BY updated_at DESC")]
        for case in rows:
            for key in ("assessment","findings","relations"):
                case[key]=json.loads(case[key]) if case[key] else None
        return rows

def get_case(case_id):
    with db() as c:
        row=c.execute("SELECT * FROM cases WHERE id=?",(case_id,)).fetchone()
        if not row: return None
        case=dict(row); case["events"]=[dict(r) for r in c.execute("SELECT * FROM events WHERE case_id=? ORDER BY timestamp",(case_id,))]
        for key in ("assessment","findings","relations"):
            case[key]=json.loads(case[key]) if case[key] else None
        for e in case["events"]:
            e["fields"]=json.loads(e["fields"] or "{}")
            e["attachments"]=[dict(a) for a in c.execute("SELECT id,filename,mime_type,size_bytes FROM attachments WHERE event_id=?",(e["id"],))]
        return case

def create_case(title, summary="", synthetic=False, events=None):
    import uuid
    cid="ST-"+uuid.uuid4().hex[:6].upper(); now=datetime.now(timezone.utc).isoformat()
    with db() as c:
        c.execute("INSERT INTO cases(id,title,summary,created_at,updated_at,synthetic) VALUES(?,?,?,?,?,?)",(cid,title,summary,now,now,int(synthetic)))
        for e in events or []: add_event(cid,e,c)
    return cid

def add_event(case_id,event,c=None):
    import uuid
    own=c is None
    if own: c=connect()
    eid=event.get("id") or "E-"+uuid.uuid4().hex[:7].upper()
    ts=event.get("timestamp") or datetime.now(timezone.utc).isoformat()
    normalized=Event(id=eid,timestamp=ts,event_type=event["event_type"],channel=event.get("channel","Other"),content=event["content"][:5000],source=event.get("source","user-entered"),fields=event.get("fields",{}))
    attachment=event.get("attachment")
    with c:
        c.execute("INSERT INTO events VALUES(?,?,?,?,?,?,?,?)",(normalized.id,case_id,normalized.timestamp.isoformat(),normalized.event_type,normalized.channel,normalized.content,normalized.source,json.dumps(normalized.fields)))
        if attachment:
            blob=attachment["data"]
            c.execute("INSERT INTO attachments(event_id,filename,mime_type,size_bytes,data) VALUES(?,?,?,?,?)",(eid,attachment["filename"],attachment["mime_type"],len(blob),blob))
        c.execute("UPDATE cases SET updated_at=?,assessment=NULL,status='Evidence added' WHERE id=?",(datetime.now(timezone.utc).isoformat(),case_id))
    if own: c.close()
    return eid

def save_analysis(case_id,assessment,findings,relations,version):
    import json
    now=datetime.now(timezone.utc).isoformat(); packed=json.dumps(assessment)
    with db() as c:
        c.execute("UPDATE cases SET assessment=?,findings=?,relations=?,analysis_version=?,updated_at=?,status='Investigated' WHERE id=?",(packed,json.dumps(findings),json.dumps(relations),version,now,case_id))
        c.execute("INSERT INTO runs(case_id,created_at,result) VALUES(?,?,?)",(case_id,now,packed))

def delete_case(case_id):
    with db() as c: c.execute("DELETE FROM cases WHERE id=?",(case_id,))

def get_attachments(case_id):
    with db() as c:
        return [dict(r) for r in c.execute("SELECT a.id,a.filename,a.mime_type,a.size_bytes,a.data,e.id AS event_id FROM attachments a JOIN events e ON e.id=a.event_id WHERE e.case_id=? ORDER BY a.id",(case_id,))]


def get_setting(key, default=None):
    with db() as c:
        row=c.execute("SELECT value FROM app_settings WHERE key=?",(key,)).fetchone()
        return row["value"] if row else default

def set_setting(key, value):
    with db() as c:
        c.execute("INSERT INTO app_settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",(key,str(value)))

def delete_setting(key):
    with db() as c:
        c.execute("DELETE FROM app_settings WHERE key=?",(key,))
