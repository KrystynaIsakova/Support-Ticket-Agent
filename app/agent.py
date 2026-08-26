import os

from dotenv import load_dotenv
from google import genai
from app.schemas import AgentDecision

load_dotenv()

SYSTEM_PROMPT = """You are a customer support assistant.

Read the support ticket and choose one action:

- respond: when you can safely provide information or troubleshooting steps;
- escalate: when the request requires account access, a payment change,
  a refund, a security action, or another action that only a human can perform.

Rules:
- Never claim that you issued a refund, changed account information,
  accessed customer data, or performed another real-world action.
- If important information is missing, ask the customer for it.
- Keep the response concise and helpful.
- Explain briefly why you selected the action
"""


def handle_ticket(ticket: str) -> AgentDecision:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    model = os.getenv("MODEL", "gemini-2.5-flash")

    result = client.models.generate_content(
        model=model,
        contents=f"{SYSTEM_PROMPT}\n\nSupport ticket:\n{ticket}",
        config={
            "response_mime_type": "application/json",
            "response_schema": AgentDecision
        }
    )

    return result.parsed