from datetime import datetime,timezone,timedelta
from app.core import Event,detect,score,sample_events
from app.ai import fallback

def test_score(): assert score(90,'FIN-DC01',70)==88.5
def test_three_alerts(): assert {a['rule'] for a in detect(sample_events())}=={'AUTH-BRUTE-FORCE','PRIVILEGED-NEW-SOURCE','SUSPICIOUS-DESTINATION'}
def test_no_false_brute_force():
    ev=[Event(id='ok',timestamp=datetime.now(timezone.utc),event_type='auth',username='a',success=True)]
    assert not detect(ev)
def test_brute_force_outside_window():
    t=datetime.now(timezone.utc)
    ev=[Event(id=str(i),timestamp=t+timedelta(minutes=i*11),event_type='auth',username='a',success=False) for i in range(5)]
    assert not detect(ev)
def test_fallback_evidence_ids():
    a=detect(sample_events())[0]; result=fallback(a,[])
    assert set(result['assessment']['findings'][0]['evidence_ids'])==set(a['event_ids'])
