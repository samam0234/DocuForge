"""청크 인덱스 저장 및 검색 + gemma4:12b 답변 생성.

- OLLAMA_EMBED_MODEL 미지정: TF-IDF 키워드 검색 (한글은 음절 bigram 포함)
- OLLAMA_EMBED_MODEL 지정: Ollama 임베딩 + 코사인 유사도
인덱스는 AI_DATA_DIR/{document_id}.json 에 저장되어 서버 재시작 후에도 유지된다.
"""
import json
import math
import re
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from app.config import get_settings
from app.services import ollama_client

ANSWER_SYSTEM = (
    "당신은 문서 기반 질의응답 도우미입니다. 반드시 제공된 [문서 발췌] 내용만 근거로 한국어로 답합니다. "
    "발췌에 답이 없으면 '문서에서 해당 내용을 찾을 수 없습니다.'라고 답합니다. 추측하지 않습니다."
)

ANSWER_PROMPT = """[문서 발췌]
{context}

[질문]
{question}

위 발췌만 근거로 간결하게 답하세요. 근거가 된 발췌 번호를 문장 끝에 (발췌 1)처럼 표시하세요."""

_TOKEN_RE = re.compile(r"[0-9A-Za-z가-힣]+")
_HANGUL_RE = re.compile(r"[가-힣]")


class DocumentNotFoundError(KeyError):
    """인덱스가 없는 document_id."""


async def index_document(filename: str, chunks: list[str]) -> str:
    settings = get_settings()
    document_id = uuid.uuid4().hex
    record = {
        "document_id": document_id,
        "filename": filename,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "embed_model": settings.ollama_embed_model or None,
        "chunks": chunks,
        "embeddings": await ollama_client.embed(chunks) if settings.ollama_embed_model else None,
    }
    path = _path(document_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
    return document_id


def load_document(document_id: str) -> dict:
    if not re.fullmatch(r"[0-9a-f]{32}", document_id):
        raise DocumentNotFoundError(document_id)
    path = _path(document_id)
    if not path.exists():
        raise DocumentNotFoundError(document_id)
    return json.loads(path.read_text(encoding="utf-8"))


async def answer(document_id: str, question: str) -> tuple[str, list[dict]]:
    record = load_document(document_id)
    hits = await search(record, question, get_settings().top_k)
    if not hits:
        return "문서에서 해당 내용을 찾을 수 없습니다.", []

    context = "\n\n".join(f"(발췌 {n}) {h['text']}" for n, h in enumerate(hits, start=1))
    text = await ollama_client.chat(ANSWER_SYSTEM, ANSWER_PROMPT.format(context=context, question=question))
    return text, hits


async def search(record: dict, query: str, top_k: int) -> list[dict]:
    chunks: list[str] = record["chunks"]
    embeddings = record.get("embeddings")
    if embeddings and record.get("embed_model") == get_settings().ollama_embed_model:
        query_vec = (await ollama_client.embed([query]))[0]
        scores = [_cosine(query_vec, vec) for vec in embeddings]
    else:
        scores = _tfidf_scores(chunks, query)

    ranked = sorted(range(len(chunks)), key=lambda i: scores[i], reverse=True)[:top_k]
    hits = [{"chunk_index": i, "text": chunks[i], "score": round(scores[i], 4)} for i in ranked if scores[i] > 0]
    # 키워드가 하나도 안 겹쳐도 짧은 문서는 앞부분을 컨텍스트로 사용
    if not hits and chunks:
        hits = [{"chunk_index": i, "text": chunks[i], "score": 0.0} for i in range(min(top_k, len(chunks)))]
    return hits


def _tokens(text: str) -> list[str]:
    tokens = []
    for word in _TOKEN_RE.findall(text.lower()):
        tokens.append(word)
        # 한국어는 조사가 붙으므로 음절 bigram으로 부분 일치를 보완
        if _HANGUL_RE.search(word) and len(word) > 2:
            tokens.extend(word[i : i + 2] for i in range(len(word) - 1))
    return tokens


def _tfidf_scores(chunks: list[str], query: str) -> list[float]:
    docs = [Counter(_tokens(c)) for c in chunks]
    query_terms = set(_tokens(query))
    n = len(docs)
    scores = []
    for doc in docs:
        length = sum(doc.values()) or 1
        score = 0.0
        for term in query_terms:
            if term in doc:
                df = sum(1 for d in docs if term in d)
                score += (doc[term] / length) * (math.log((n + 1) / (df + 0.5)) + 1)
        scores.append(score)
    return scores


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return dot / norm if norm else 0.0


def _path(document_id: str) -> Path:
    return Path(get_settings().ai_data_dir) / f"{document_id}.json"
