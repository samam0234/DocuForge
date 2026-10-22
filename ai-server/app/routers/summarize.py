"""POST /summarize — 파일 업로드 → 텍스트 추출 → 인덱싱 → 요약."""
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import get_settings
from app.models.schemas import SummarizeResponse
from app.services import rag_engine, summarizer
from app.services.document_parser import (
    EmptyDocumentError,
    UnsupportedFormatError,
    extract_text,
    split_chunks,
)
from app.services.ollama_client import OllamaError

router = APIRouter()


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize(file: UploadFile = File(...)) -> SummarizeResponse:
    settings = get_settings()
    filename = file.filename or "document.txt"
    data = await file.read()
    if len(data) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, f"파일이 너무 큽니다. (최대 {settings.max_upload_mb}MB)")

    try:
        text = extract_text(filename, data)
    except UnsupportedFormatError as exc:
        raise HTTPException(415, str(exc)) from exc
    except EmptyDocumentError as exc:
        raise HTTPException(422, str(exc)) from exc

    chunks = split_chunks(text, settings.chunk_size, settings.chunk_overlap)
    try:
        summary = await summarizer.summarize(filename, text)
        document_id = await rag_engine.index_document(filename, chunks)
    except OllamaError as exc:
        raise HTTPException(503, f"AI 모델 호출 실패: {exc}") from exc

    return SummarizeResponse(
        document_id=document_id,
        filename=filename,
        summary=summary,
        text=text,
        char_count=len(text),
        chunk_count=len(chunks),
        model=settings.ollama_model,
    )
