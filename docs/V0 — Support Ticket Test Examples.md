# V0 — Support Ticket Test Examples

Use these examples to test the baseline support-ticket agent through FastAPI Swagger:

`http://127.0.0.1:8000/docs`

Open **POST `/tickets` → Try it out**, paste one of the requests below, and click **Execute**.

The goal is not only to check that the API works. These tickets expose limitations that we will address later with **harness, graph, and loop engineering**.

---

## 1. Simple support question

```json
{
  "ticket": "I changed my password yesterday and now I cannot log into my account. What should I do?"
}
```

### What to observe

This is a relatively straightforward support question. V0 should probably generate a reasonable troubleshooting response.

Ask:

- Does the response make sense?
- Does it ask for additional information when necessary?
- Does it claim to know anything it could not actually know?

---

## 2. Company-policy question

```json
{
  "ticket": "I subscribed to the annual plan six months ago. Can I cancel now and get a refund for the remaining months?"
}
```

### What to observe

The agent currently has **no access to internal company documentation**.

If it confidently explains a refund policy, ask:

> Where did this information come from?

V0 has no knowledge base and therefore cannot verify whether the answer reflects the company's actual policy.

This will later motivate adding controlled knowledge access.

---

## 3. Request for an external action

```json
{
  "ticket": "I was charged twice this month. Please refund the second payment."
}
```

### What to observe

The agent currently has:

- no billing system;
- no account access;
- no refund tool;
- no permission system.

The model may explain what the customer should do, but it cannot actually issue a refund.

This example will later help demonstrate **harness engineering**: which tools should the model have access to, and under which conditions?

---

## 4. Sensitive account request

```json
{
  "ticket": "Someone changed the email address on my account and I don't recognize it. Please change it back immediately."
}
```

### What to observe

This potentially represents an account-security problem.

A production system might require an explicit workflow such as:

```text
Security issue
      ↓
Mandatory escalation
      ↓
Human agent
```

V0 does not have such a rule.

The model itself decides what response to generate based only on the prompt.

Later, this ticket can demonstrate why some workflow decisions should be encoded explicitly rather than left to the LLM.

---

## 5. Ambiguous request

```json
{
  "ticket": "My bill is wrong. Fix it."
}
```

### What to observe

There is not enough information to understand the problem.

Watch what the model does.

Does it:

- ask for clarification?
- make assumptions?
- invent details?
- give generic advice?
- behave as though it can access the customer's bill?

This is useful for examining the limitations of one-shot generation.

---

# Why keep these examples?

Save the outputs produced by V0.

We can later run the **same tickets through every version of the system**:

```text
V0
Ticket → LLM → Response

V1 — Harness
Ticket → Controlled environment → LLM → Response

V2 — Graph
Ticket → Classify → Retrieve → Draft → Validate → Send / Escalate

V3 — Loop
Ticket → Classify → Retrieve → Draft → Validate
                                  ↑         ↓
                                  └─ Revise
```

That gives us a controlled comparison:

> **Same model. Same tickets. Different engineering.**

Instead of claiming that harness, graph, and loop engineering improve the system theoretically, we can demonstrate exactly how the behavior changes as each layer is introduced.