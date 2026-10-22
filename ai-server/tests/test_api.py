"""Ollama 호출을 대체(mock)한 API 테스트."""
import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app
from app.services import ollama_client


@pytest.fixture(autouse=True)
def fake_ollama(monkeypatch, tmp_path):
    monkeypatch.setattr(get_settings(), "ai_data_dir", tmp_path)
    monkeypatch.setattr(get_settings(), "ollama_embed_model", "")

    async def fake_chat(system, user, **kwargs):
        return "가짜 응답: " + user[-30:]

    monkeypatch.setattr(ollama_client, "chat", fake_chat)


client = TestClient(app)


def upload(name: str, data: bytes):
    return client.post("/summarize", files={"file": (name, data)})


def test_summarize_and_ask():
    text = "도커는 컨테이너 기술입니다.\n\n파이썬은 프로그래밍 언어입니다.\n\n" * 3
    res = upload("note.txt", text.encode("utf-8"))
    assert res.status_code == 200
    body = res.json()
    assert body["summary"].startswith("가짜 응답")
    assert body["chunk_count"] >= 1

    res = client.post("/ask", json={"document_id": body["document_id"], "question": "도커가 뭐야?"})
    assert res.status_code == 200
    assert "도커" in res.json()["sources"][0]["text"]


def test_unsupported_format():
    assert upload("image.png", b"xx").status_code == 415


def test_empty_text():
    assert upload("blank.txt", b"   \n  ").status_code == 422


def test_unknown_document():
    res = client.post("/ask", json={"document_id": "0" * 32, "question": "질문"})
    assert res.status_code == 404
