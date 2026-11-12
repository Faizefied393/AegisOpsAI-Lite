from app.core import sample_events
from app.sigma import load_rule,sigma_matches
from app.kev import enrich
from app.ml import train
from app.agent import build_graph

def test_sigma_rule():
    assert load_rule()['title'].startswith('AegisOps')
    assert len(sigma_matches(sample_events()))==5

def test_kev_fixture():
    assert enrich('FIN-DB01')[0]['in_kev'] is True
    assert enrich('WEB-01')==[]

def test_ml_baseline():
    _,m=train()
    assert 0<=m['f1']<=1
    assert m['test_samples']==75

def test_agent_structure():
    graph=build_graph()
    assert 'review_gate' in graph.nodes
