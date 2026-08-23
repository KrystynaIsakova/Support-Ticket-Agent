from pydantic import BaseModel, Field


class TicketRequest(BaseModel):
    ticket: str = Field(min_length=1, examples=["I was charged twice this month."])


class TicketResponse(BaseModel):
    response: str
