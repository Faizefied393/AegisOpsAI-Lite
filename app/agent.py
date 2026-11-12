"""Read-only LangGraph orchestration; review is required before any response action."""
from typing import TypedDict
from langgraph.graph import StateGraph,START,END
from app.ai import investigate
from app.kev import enrich
class InvestigationState(TypedDict,total=False):
    alert:dict
    evidence:list[dict]
    enrichment:list[dict]
    report:dict
    review_status:str

def enrichment_node(state:InvestigationState):
    return {'enrichment':enrich(state['alert']['asset'])}

def analysis_node(state:InvestigationState):
    return {'report':investigate(state['alert'],state['evidence'])}

def review_node(state:InvestigationState):
    return {'review_status':'PENDING_HUMAN_REVIEW'}

def build_graph():
    graph=StateGraph(InvestigationState)
    graph.add_node('enrich',enrichment_node)
    graph.add_node('investigate',analysis_node)
    graph.add_node('review_gate',review_node)
    graph.add_edge(START,'enrich')
    graph.add_edge('enrich','investigate')
    graph.add_edge('investigate','review_gate')
    graph.add_edge('review_gate',END)
    return graph.compile()
