"""POST /ask — document_id 기반 RAG 질의응답."""
from fastapi import APIRouter, HTTPException

from app.config import get_settings
from app.models.schemas import AskRequest, AskResponse, Source
from app.services import rag_engine
from app.services.ollama_client import OllamaError

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest) -> AskResponse:
    try:
        answer, hits = await rag_engine.answer(req.document_id, req.question.strip())
    except rag_engine.DocumentNotFoundError as exc:
        raise HTTPException(404, "해당 문서의 인덱스를 찾을 수 없습니다. 문서를 다시 업로드해 주세요.") from exc
    except OllamaError as exc:
        raise HTTPException(503, f"AI 모델 호출 실패: {exc}") from exc

    return AskResponse(
        document_id=req.document_id,
        question=req.question,
        answer=answer,
        sources=[Source(**h) for h in hits],
        model=get_settings().ollama_model,
    )
