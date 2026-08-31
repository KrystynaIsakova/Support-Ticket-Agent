from app.schemas import AgentDecision

FORBIDDEN_CLAIMS = [
    "i issued the refund",
    "i refunded",
    "i changed your account",
    "i disabled your account",
]

def validate_decision(decision: AgentDecision) -> list[str]:
    errors = []
    errors.append("Temporary lesson test: force validation failure.")

    response = decision.response.lower()
    for claim in FORBIDDEN_CLAIMS:
        if claim in response:
            errors.append(
                f'The response claims a real action was performed: {claim}'
            )

    if not decision.response.strip():
        errors.append("The response is empty.")
    
    if not decision.reason.strip():
        errors.append("The reason is empty.")

    return errors