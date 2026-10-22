"""Ollama HTTP API 클라이언트 (gemma4:12b)."""
import httpx

from app.config import get_settings


class OllamaError(RuntimeError):
    """Ollama 호출 실패."""


async def chat(system: str, user: str, *, temperature: float = 0.2) -> str:
    settings = get_settings()
    payload = {
        "model": settings.ollama_model,
        "stream": False,
        "think": False,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "options": {"temperature": temperature, "num_ctx": settings.ollama_num_ctx},
    }
    data = await _post("/api/chat", payload, settings.ollama_timeout)
    content = data.get("message", {}).get("content", "").strip()
    if not content:
        raise OllamaError("모델이 빈 응답을 반환했습니다.")
    return content


async def embed(texts: list[str]) -> list[list[float]]:
    settings = get_settings()
    payload = {"model": settings.ollama_embed_model, "input": texts}
    data = await _post("/api/embed", payload, settings.ollama_timeout)
    return data["embeddings"]


async def ping() -> bool:
    settings = get_settings()
    try:
        async with httpx.AsyncClient(base_url=settings.ollama_base_url, timeout=5) as client:
            res = await client.get("/api/tags")
            res.raise_for_status()
            names = {m["name"] for m in res.json().get("models", [])}
            return settings.ollama_model in names
    except httpx.HTTPError:
        return False


async def _post(path: str, payload: dict, timeout: float) -> dict:
    settings = get_settings()
    try:
        async with httpx.AsyncClient(base_url=settings.ollama_base_url, timeout=timeout) as client:
            res = await client.post(path, json=payload)
    except httpx.HTTPError as exc:
        raise OllamaError(f"Ollama 서버에 연결할 수 없습니다: {exc!r}") from exc
    if res.status_code != 200:
        raise OllamaError(f"Ollama 오류 ({res.status_code}): {res.text[:300]}")
    return res.json()
