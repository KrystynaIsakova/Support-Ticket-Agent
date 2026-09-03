from typing import TypedDict, Literal

from app.schemas import AgentDecision
from app.agent import handle_ticket
from langgraph.graph import END, START, StateGraph

class SupportState(TypedDict, total=False):
    ticket: str
    decision: AgentDecision
    path: str

def make_decision(state: SupportState):
    decision = handle_ticket(state['ticket'])
    return {'decision': decision}

def choose_path(state: SupportState) -> Literal["automatic_response", "human_escalation"]:
    decision = state['decision']

    if decision.action == 'respond':
        return "automatic_response"
    return "human_escalation"

def automatic_response(state: SupportState) -> dict:
    print("Graph path: automatic response")
    return {'path': "automatic_response"}

def human_escalation(state: SupportState) -> dict:
    print("Graph path: human escalation")
    return {'path': "human_escalation"}

graph_builder = StateGraph(SupportState)
graph_builder.add_node('make_decision', make_decision)
graph_builder.add_node('automatic_response', automatic_response)
graph_builder.add_node('human_escalation', human_escalation)

graph_builder.add_edge(START, 'make_decision')
graph_builder.add_conditional_edges(
    "make_decision",
    choose_path,
    {
        "automatic_response": 'automatic_response',
        "human_escalation": 'human_escalation'
    }
)

graph_builder.add_edge('automatic_response', END)
graph_builder.add_edge('human_escalation', END)
support_graph = graph_builder.compile()