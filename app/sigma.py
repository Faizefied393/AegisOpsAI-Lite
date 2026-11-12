"""Tiny transparent Sigma rule interpreter for the one demo rule only.
Not a general Sigma backend or pySigma replacement.
"""
from pathlib import Path
import yaml
from app.core import Event
RULE_PATH = Path(__file__).resolve().parents[1] / 'detections/sigma/failed_logins.yml'

def load_rule():
    rule=yaml.safe_load(RULE_PATH.read_text())
    assert rule['logsource']['category']=='authentication'
    return rule

def sigma_matches(events:list[Event]):
    rule=load_rule()
    selection=rule['detection']['selection']
    return [e.id for e in events if e.event_type==selection['event_type'] and e.success is selection['success']]
