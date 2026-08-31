import os

from dotenv import load_dotenv
from google import genai
from app.schemas import AgentDecision
from app.validator import validate_decision

load_dotenv()

attempts = 2

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
    model = os.getenv("MODEL", "gemini-3.5-flash")

    feedback = ""
    for attempt in range(attempts):
        contents = f"{SYSTEM_PROMPT}\n\nSupport ticket:\n{ticket}"

        if feedback:
            contents += f"""
            Your previous response failed validation.

        Validation feedback:
        {feedback}

        Revise the response and fix these problems.
        """

        result = client.models.generate_content(
            model=model,
            contents=f"{SYSTEM_PROMPT}\n\nSupport ticket:\n{ticket}",
            config={
                "response_mime_type": "application/json",
                "response_schema": AgentDecision
            }
        )

        decision = result.parsed
        errors = validate_decision(decision)

        if not errors:
            return decision

        feedback = "\n".join(errors)

    '''
    raise ValueError(
        f"Agent response failed validation after {attempts} attempts: {feedback}"
    )
    '''
    print("Maximum attempts reached. Escalating to a human agent.")
    return AgentDecision(
        action="escalate",
        response="I'm unable to provide a valid response. Escalating to a human agent.",
        reason=f"Agent response failed validation after {attempts} attempts: {feedback}"
    )