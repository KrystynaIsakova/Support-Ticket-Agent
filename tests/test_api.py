from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ticket_endpoint(monkeypatch):
    def fake_handle_ticket(ticket: str) -> str:
        assert ticket == "I was charged twice this month."
        return "I can help explain the next steps for a duplicate charge."

    monkeypatch.setattr("app.main.handle_ticket", fake_handle_ticket)

    response = client.post(
        "/tickets",
        json={"ticket": "I was charged twice this month."},
    )

    assert response.status_code == 200
    assert response.json() == {
        "response": "I can help explain the next steps for a duplicate charge."
    }


def test_empty_ticket_is_rejected():
    response = client.post("/tickets", json={"ticket": ""})

    assert response.status_code == 422
