"""Quick local integration check, no running services required."""
from app.core import sample_events,detect
from app.sigma import sigma_matches
from app.kev import enrich
from app.ml import train
from app.agent import build_graph
print('Events:',len(sample_events()))
print('Detections:',len(detect(sample_events())))
print('Sigma matches:',len(sigma_matches(sample_events())))
print('KEV fixture:',enrich('FIN-DB01'))
print('ML:',train()[1])
print('LangGraph nodes:',list(build_graph().nodes))
