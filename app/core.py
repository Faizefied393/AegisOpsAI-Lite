from __future__ import annotations
import json, os, sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path
from pydantic import BaseModel, Field

class Event(BaseModel):
    id: str = Field(min_length=1,max_length=100)
    timestamp: datetime
    event_type: str
    username: str = ""
    source_ip: str = ""
    asset: str = ""
    success: bool | None = None
    privileged: bool = False
    new_source: bool = False
    destination_ip: str = ""
    details: str = ""

ASSETS = {"FIN-DC01":100,"FIN-DB01":95,"FIN-LAP01":65,"WEB-01":50}
BAD_IPS = {"203.0.113.66"}  # documentation-only TEST-NET-3; not live threat intelligence

def db_path():
    p=Path(os.getenv('AEGIS_DB_PATH','data/aegisops.db'))
    p.parent.mkdir(parents=True,exist_ok=True)
    return p

def connect():
    db=sqlite3.connect(db_path())
    db.row_factory=sqlite3.Row
    db.execute('CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, timestamp TEXT NOT NULL, payload TEXT NOT NULL)')
    db.commit()
    return db

def save_events(events:list[Event]):
    with connect() as db:
        for e in events:
            db.execute('INSERT OR REPLACE INTO events VALUES (?,?,?)',(e.id,e.timestamp.isoformat(),e.model_dump_json()))

def get_events():
    with connect() as db:
        rows=db.execute('SELECT payload FROM events ORDER BY timestamp,id').fetchall()
    return [Event.model_validate_json(r['payload']) for r in rows]

def score(severity:int,asset:str,confidence:int)->float:
    return round(.4*severity+.35*ASSETS.get(asset,40)+.25*confidence,1)

def detect(events:list[Event]):
    alerts=[]
    def add(rule,severity,confidence,items,explanation):
        ids=sorted(set(e.id for e in items))
        asset=items[-1].asset
        alerts.append({'id':f'{rule}-{ids[-1]}','rule':rule,'severity':severity,'confidence':confidence,
                       'asset':asset,'risk_score':score(severity,asset,confidence),'event_ids':ids,
                       'explanation':explanation,'status':'unconfirmed alert'})
    failures={}
    for e in sorted(events,key=lambda x:x.timestamp):
        if e.event_type=='auth' and e.success is False:
            failures.setdefault(e.username,[]).append(e)
    for username, group in failures.items():
        for i in range(len(group)):
            window=[e for e in group if group[i].timestamp <= e.timestamp <= group[i].timestamp+timedelta(minutes=10)]
            if len(window)>=5:
                add('AUTH-BRUTE-FORCE',85,90,window[:5],f'At least five failed logins for {username} within ten minutes')
                break
    for e in events:
        if e.event_type=='auth' and e.success is True and e.privileged and e.new_source:
            add('PRIVILEGED-NEW-SOURCE',90,75,[e],'Privileged authentication from a new source')
        if e.event_type=='network' and e.destination_ip in BAD_IPS:
            add('SUSPICIOUS-DESTINATION',80,85,[e],'Connection to a synthetic test indicator (not a real threat feed)')
    return sorted(alerts,key=lambda a:a['risk_score'],reverse=True)

def sample_events():
    base=datetime(2026,11,8,12,0,tzinfo=timezone.utc)
    ev=[]
    for i in range(5):
        ev.append(Event(id=f'auth-fail-{i+1}',timestamp=base+timedelta(minutes=i),event_type='auth',username='admin',source_ip='198.51.100.25',asset='FIN-DC01',success=False))
    ev.extend([
        Event(id='priv-login-1',timestamp=base+timedelta(minutes=6),event_type='auth',username='admin',source_ip='198.51.100.25',asset='FIN-DC01',success=True,privileged=True,new_source=True),
        Event(id='net-1',timestamp=base+timedelta(minutes=7),event_type='network',asset='FIN-DB01',source_ip='192.0.2.10',destination_ip='203.0.113.66'),
        Event(id='normal-1',timestamp=base+timedelta(minutes=8),event_type='auth',username='employee',asset='FIN-LAP01',success=True,source_ip='192.0.2.11')])
    return ev
