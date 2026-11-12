import os, secrets
from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel, Field
from app.core import Event, save_events, get_events, detect, sample_events
from app.ai import investigate

app=FastAPI(title='AegisOps AI X',version='1.0.0',description='Synthetic enterprise security investigation reference application')

def require_key(
    x_api_key: str | None = Header(default=None)
):
    expected = os.getenv("AEGIS_API_KEY")

    if (
        not expected
        or not x_api_key
        or not secrets.compare_digest(x_api_key, expected)
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )

class Batch(BaseModel):
    events:list[Event]=Field(min_length=1,max_length=1000)

@app.get('/health')
def health(): return {'status':'ok','version':'1.0.0'}

@app.post('/demo/seed',dependencies=[Depends(require_key)])
def seed():
    events=sample_events();save_events(events)
    return {'loaded':len(events),'note':'Synthetic demonstration data only'}

@app.post('/events',dependencies=[Depends(require_key)])
def ingest(batch:Batch):
    save_events(batch.events)
    return {'stored':len(batch.events)}

@app.get('/events',dependencies=[Depends(require_key)])
def events(): return [e.model_dump(mode='json') for e in get_events()]

@app.get('/alerts',dependencies=[Depends(require_key)])
def alerts(): return detect(get_events())

@app.get('/metrics',dependencies=[Depends(require_key)])
def metrics():
    ev=get_events(); al=detect(ev)
    return {'events':len(ev),'alerts':len(al),'high_risk_alerts':sum(a['risk_score']>=80 for a in al),
            'highest_risk':max((a['risk_score'] for a in al),default=0),
            'note':'Alerts are unconfirmed; risk is a heuristic score'}

@app.post('/alerts/{alert_id}/investigate',dependencies=[Depends(require_key)])
def investigate_alert(alert_id:str):
    all_events=get_events()
    alert=next((a for a in detect(all_events) if a['id']==alert_id),None)
    if not alert: raise HTTPException(status_code=404,detail='Alert not found')
    evidence=[e.model_dump(mode='json') for e in all_events if e.id in alert['event_ids']]
    return {'alert_id':alert_id,**investigate(alert,evidence)}

@app.get('/extensions/sigma',dependencies=[Depends(require_key)])
def sigma_demo():
    from app.sigma import load_rule,sigma_matches
    ev=get_events()
    return {'rule':load_rule()['title'],'matching_event_ids':sigma_matches(ev),'note':'Subset interpreter; time-window correlation remains in app.core'}

@app.get('/extensions/kev/{asset}',dependencies=[Depends(require_key)])
def kev_demo(asset:str):
    from app.kev import enrich
    return {'asset':asset,'enrichment':enrich(asset),'source':'bundled offline fixture; not current KEV'}

@app.get('/extensions/ml',dependencies=[Depends(require_key)])
def ml_demo():
    from app.ml import train
    return train()[1]

@app.post('/extensions/agent/{alert_id}',dependencies=[Depends(require_key)])
def agent_demo(alert_id:str):
    from app.agent import build_graph
    all_events=get_events()
    alert=next((a for a in detect(all_events) if a['id']==alert_id),None)
    if not alert: raise HTTPException(status_code=404,detail='Alert not found')
    evidence=[e.model_dump(mode='json') for e in all_events if e.id in alert['event_ids']]
    return build_graph().invoke({'alert':alert,'evidence':evidence})

if os.getenv('AEGIS_ENABLE_TRACING')=='1':
    from app.telemetry import setup
    setup(app)
