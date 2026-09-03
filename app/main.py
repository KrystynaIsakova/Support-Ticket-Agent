from fastapi import FastAPI

from app.graph import support_graph
from app.schemas import TicketRequest, TicketResponse


app = FastAPI(
    title="Support Ticket Agent — V0",
    version="0.1.0",
    description="Baseline support-ticket agent: one ticket in, one LLM response out.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/tickets", response_model=TicketResponse)
def create_ticket(request: TicketRequest) -> TicketResponse:
    result = support_graph.invoke(
        {'ticket': request.ticket}
    )

    decision = result['decision']
    return TicketResponse(
        action=decision.action,
        response=decision.response,
        reason = decision.reason
    )
