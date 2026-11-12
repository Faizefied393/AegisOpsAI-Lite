def test_health(client): assert client.get('/health').json()['status']=='ok'
def test_requires_auth(client): assert client.get('/events').status_code==401
def test_seed_and_metrics(client,headers):
    assert client.post('/demo/seed',headers=headers).json()['loaded']==8
    m=client.get('/metrics',headers=headers).json()
    assert m['events']==8 and m['alerts']==3
def test_invalid_input(client,headers):
    r=client.post('/events',headers=headers,json={'events':[{'id':'x','timestamp':'bad','event_type':'auth'}]})
    assert r.status_code==422
def test_missing_alert(client,headers):
    assert client.post('/alerts/no-such-alert/investigate',headers=headers).status_code==404
def test_ingest(client,headers):
    payload={'events':[{'id':'new','timestamp':'2026-11-08T12:00:00Z','event_type':'auth','success':True}]}
    assert client.post('/events',headers=headers,json=payload).json()['stored']==1
    assert len(client.get('/events',headers=headers).json())==1
def test_alerts_reject_missing_key(client):
    response = client.get("/alerts")
    assert response.status_code == 401
    