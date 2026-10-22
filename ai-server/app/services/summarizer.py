"""gemma4:12b 기반 문서 요약 (긴 문서는 map-reduce)."""
from app.config import get_settings
from app.services import ollama_client
from app.services.document_parser import split_chunks

SYSTEM_PROMPT = (
    "당신은 문서 요약 전문가입니다. 주어진 문서 내용만 근거로 한국어로 요약합니다. "
    "문서에 없는 내용은 추측하지 않습니다."
)

FINAL_PROMPT = """다음 문서를 한국어로 요약하세요.

형식:
## 한 줄 요약
(한 문장)

## 핵심 내용
- (3~7개 불릿)

## 키워드
(쉼표로 구분된 키워드 3~6개)

문서 제목: {filename}
---
{text}
---"""

SECTION_PROMPT = """다음은 긴 문서의 일부({index}/{total})입니다.
이 부분의 핵심 내용을 한국어 불릿 3~5개로 요약하세요. 다른 말은 덧붙이지 마세요.
---
{text}
---"""


async def summarize(filename: str, text: str) -> str:
    settings = get_settings()
    if len(text) <= settings.summary_section_size:
        return await ollama_client.chat(SYSTEM_PROMPT, FINAL_PROMPT.format(filename=filename, text=text))

    # map: 섹션별 부분 요약
    sections = split_chunks(text, settings.summary_section_size, 0)
    partials = []
    for i, section in enumerate(sections, start=1):
        prompt = SECTION_PROMPT.format(index=i, total=len(sections), text=section)
        partials.append(await ollama_client.chat(SYSTEM_PROMPT, prompt))

    # reduce: 부분 요약을 다시 최종 형식으로 요약
    merged = "\n\n".join(f"[부분 {i}]\n{p}" for i, p in enumerate(partials, start=1))
    if len(merged) > settings.summary_section_size * 2:
        merged = merged[: settings.summary_section_size * 2]
    return await ollama_client.chat(SYSTEM_PROMPT, FINAL_PROMPT.format(filename=filename, text=merged))
