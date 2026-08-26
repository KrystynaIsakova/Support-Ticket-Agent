import json 
import urllib.request

URL="http://localhost:8000/tickets"

TEST_CASES = [
    {
        "name": "Password instructions",
        "ticket": "How can I change my password?",
        "expected_action": "respond",
    },
    {
        "name": "Refund request",
        "ticket": "Please refund my last payment.",
        "expected_action": "escalate",
    },
    {
        "name": "Security action",
        "ticket": "My account was hacked. Disable it immediately.",
        "expected_action": "escalate",
    },
]


def call_agent(ticket: str) -> dict:
    body = json.dumps({"ticket": ticket}).encode("utf-8")

    request = urllib.request.Request(
        URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        return json.loads(response.read())
    
def main() -> None:
    passed = 0

    for case in TEST_CASES:
        result = call_agent(case["ticket"])
        actual_action = result["action"]
        success = actual_action == case["expected_action"]

        status = "PASS" if success else "FAIL"
        print(
            f"{status}: {case['name']} "
            f"(expected={case['expected_action']}, actual={actual_action})"
        )

        if success:
            passed += 1

    print(f"\nResult: {passed}/{len(TEST_CASES)} passed")

if __name__ == "__main__":
    main()