# Support Ticket Agent — V0

This repository is the deliberately simple baseline for a content series about **harness engineering, graph engineering, and loop engineering**.

V0 does one thing:

```text
Ticket → LLM → Response
```

There is no knowledge-base retrieval, no workflow graph, no validation loop, no tool system, and no autonomous external action.

That is intentional.

The goal is to start with a plausible first AI application and evolve the same project step by step.

## Architecture

```text
POST /tickets
     │
     ▼
handle_ticket()
     │
     ▼
    LLM
     │
     ▼
TicketResponse
```

## What V0 can do

- Accept a support ticket through an HTTP API.
- Send the ticket to an LLM.
- Return the generated response.
- Expose a simple health endpoint.
- Run tests without making real model calls.

## What V0 cannot reliably do

- Search internal company documentation.
- Know whether its answer is grounded in company policy.
- Enforce a multi-step support workflow.
- Validate its own answer.
- Retry or revise a failed answer.
- Decide safely when a human must approve an action.
- Perform external actions such as refunds or account updates.

Those limitations are the point of the baseline.

## Project structure

```text
support-ticket-agent-v0/
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── main.py
│   └── schemas.py
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

## Setup with uv

Clone the repository and create the environment:

```bash
uv sync
```

Create your local environment file:

```bash
cp .env.example .env
```

Add your API key to `.env`.

Then load the environment variables before running the service.

On macOS/Linux:

```bash
set -a
source .env
set +a
```

## Using OpenRouter

The project uses the OpenAI Python client, so any OpenAI-compatible provider can be configured through `OPENAI_BASE_URL`.

For OpenRouter:

```env
OPENAI_API_KEY=your_openrouter_key
OPENAI_BASE_URL=https://openrouter.ai/api/v1
MODEL=openai/gpt-4.1-mini
```

You can replace the model with another model supported by your provider.

## Run the API

```bash
uv run uvicorn app.main:app --reload
```

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Try a ticket

```bash
curl -X POST http://127.0.0.1:8000/tickets   -H "Content-Type: application/json"   -d '{
    "ticket": "I was charged twice this month. Can you refund the second payment?"
  }'
```

Example response:

```json
{
  "response": "..."
}
```

## Run the tests

```bash
uv run pytest
```

The endpoint test replaces the real model call with a deterministic fake, so the test suite does not require an API key.

## Example tickets

Try the baseline with different kinds of requests.

### Resolvable-looking request

```text
I cannot log into my account after changing my password.
```

### Missing company knowledge

```text
Can I cancel my annual plan after six months and receive a partial refund?
```

### Sensitive action

```text
Please refund the last payment and change the email address on my account.
```

### Ambiguous request

```text
Something is wrong with my bill. Fix it.
```

## Why start here?

This system looks reasonable at first glance: a ticket comes in and the model writes a response.

But most of the important engineering decisions are still hidden inside one prompt and one model call.

The next versions will ask three different questions:

1. **Harness engineering:** What should surround the model and what should it be allowed to access or do?
2. **Graph engineering:** Which workflow steps and branches should be explicitly enforced?
3. **Loop engineering:** What should happen when the first result is not good enough?

The model can stay the same while the system around it changes.
