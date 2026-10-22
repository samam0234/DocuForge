"""환경 변수 기반 설정."""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gemma4:12b"
    # 비어 있으면 TF-IDF 키워드 검색, 값이 있으면 Ollama 임베딩 검색
    ollama_embed_model: str = ""
    ollama_num_ctx: int = 8192
    ollama_timeout: float = 300.0

    ai_data_dir: Path = Path("./data")
    max_upload_mb: int = 10

    # 검색용 청크 (문자 수)
    chunk_size: int = 1000
    chunk_overlap: int = 150
    # 요약 map 단계 섹션 크기 (문자 수)
    summary_section_size: int = 6000
    top_k: int = 4


@lru_cache
def get_settings() -> Settings:
    return Settings()
