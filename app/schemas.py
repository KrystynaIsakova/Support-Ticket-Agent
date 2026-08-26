from pydantic import BaseModel, Field
from typing import Literal


class TicketRequest(BaseModel):
    ticket: str = Field(min_length=1, examples=["I was charged twice this month."])


class TicketResponse(BaseModel):
    '''
    defines waht the FastAPI endpoint returns
    '''
    action: Literal["respond", "escalate"]
    response: str
    reason: str

class AgentDecision(BaseModel):
    '''
    Validates what the LLM procues
    '''
    action: Literal["respond", "escalate"]
    response: str
    reason: str
