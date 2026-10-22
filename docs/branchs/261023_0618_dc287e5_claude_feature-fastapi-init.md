# 커밋 기록: feat(ai-server): 문서 요약 및 RAG 질의응답 엔드포인트 구현

| 항목 | 내용 |
|------|------|
| 일시 | 2026-10-23 06:18 |
| 커밋 ID | `dc287e5` |
| 작성자 | claude |
| 브랜치 | `feature/fastapi-init` |
| 커밋 메시지 | `feat(ai-server): 문서 요약 및 RAG 질의응답 엔드포인트 구현` |

## 1. 작업 목적

- 기획서 4~6장의 /summarize, /ask 흐름을 실제 LLM과 연동해 구현한다.

## 2. 변경 내용

TXT/PDF 텍스트 추출과 청크 분할, map-reduce 방식 요약(/summarize)을 구현한다.
청크 인덱스를 파일로 저장하고 TF-IDF 또는 임베딩 검색 후
gemma4:12b로 근거 기반 답변을 생성하는 /ask와 /health를 추가한다.

## 3. 변경 파일

| 파일 | 구분 | 설명 |
|------|------|------|
| `ai-server/app/main.py` | 추가 | |
| `ai-server/app/routers/__init__.py` | 추가 | |
| `ai-server/app/routers/ask.py` | 추가 | |
| `ai-server/app/routers/summarize.py` | 추가 | |
| `ai-server/app/services/document_parser.py` | 추가 | |
| `ai-server/app/services/rag_engine.py` | 추가 | |
| `ai-server/app/services/summarizer.py` | 추가 | |

## 4. 검증

- 실제 Ollama gemma4:12b로 TXT 요약(약 10초), PDF 추출+요약, 11,000자 문서 map-reduce 요약(14청크, 36초), TF-IDF/bge-m3 임베딩 검색 답변을 모두 확인했다.

## 5. 비고 / 후속 작업

- OLLAMA_EMBED_MODEL 미지정 시 TF-IDF 검색. bge-m3 사용 시 업로드 시점에 임베딩을 저장한다.
