from fastapi.testclient import TestClient
import api

client = TestClient(api.app)

def test_ask_returns_answer_and_sources(monkeypatch):
    monkeypatch.setattr(api.ollama, "chat", lambda **kw: {"message": {"content": "fake answer"}})
    r = client.post("/ask", json={"question": "what is React"})
    assert r.status_code == 200
    assert r.json()["answer"] == "fake answer"
    assert "react.txt" in r.json()["sources"]

def test_ask_rejects_missing_question():
    r = client.post("/ask", json={})
    assert r.status_code == 422
