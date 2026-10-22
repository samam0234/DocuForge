"""요청/응답 스키마."""
from pydantic import BaseModel, Field


class SummarizeResponse(BaseModel):
    document_id: str
    filename: str
    summary: str
    text: str
    char_count: int
    chunk_count: int
    model: str


class AskRequest(BaseModel):
    document_id: str = Field(min_length=1)
    question: str = Field(min_length=1, max_length=2000)


class Source(BaseModel):
    chunk_index: int
    text: str
    score: float


class AskResponse(BaseModel):
    document_id: str
    question: str
    answer: str
    sources: list[Source]
    model: str


class HealthResponse(BaseModel):
    status: str
    model: str
    embed_model: str | None
    ollama: bool
