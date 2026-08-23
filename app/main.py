from fastapi import FastAPI

from app.agent import handle_ticket
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
    response = handle_ticket(request.ticket)
    return TicketResponse(response=response)
