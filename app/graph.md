# Support Ticket Graph

LangGraph flow defined in [graph.py](app/graph.py).

```mermaid
flowchart TD
    START([START]) --> make_decision["make_decision<br/><i>handle_ticket(ticket) → decision</i>"]
    make_decision -->|choose_path| decide{"decision.action<br/>== 'respond'?"}
    decide -->|yes| automatic_response["automatic_response<br/><i>path = automatic_response</i>"]
    decide -->|no| human_escalation["human_escalation<br/><i>path = human_escalation</i>"]
    automatic_response --> END([END])
    human_escalation --> END
```

## State

| Field | Type | Set by |
| --- | --- | --- |
| `ticket` | `str` | caller (graph input) |
| `decision` | `AgentDecision` | `make_decision` |
| `path` | `str` | `automatic_response` / `human_escalation` |
