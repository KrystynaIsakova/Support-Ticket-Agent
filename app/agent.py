import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

SYSTEM_PROMPT = """You are a customer support assistant.

Read the support ticket and write a concise, helpful response.

Do not claim that you performed actions you cannot actually perform.
If the request requires access to account data or a real-world action,
explain what information or human assistance is needed.
"""


def handle_ticket(ticket: str) -> str:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    model = os.getenv("MODEL", "gemini-2.5-flash")

    response = client.models.generate_content(
        model=model,
        contents=f"{SYSTEM_PROMPT}\n\nSupport ticket:\n{ticket}",
    )

    return response.text or ""