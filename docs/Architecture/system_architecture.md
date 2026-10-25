# DocuForge 시스템 아키텍처

## 1. 구성

```
┌─────────────┐  HTTP   ┌──────────────────┐  HTTP   ┌─────────────────┐  HTTP  ┌──────────────────┐
│  Vue 3      │────────▶│  Rails 8 API     │────────▶│  FastAPI        │───────▶│ Ollama           │
│  :5173      │◀────────│  :3000           │◀────────│  :8000          │◀───────│ gemma4:12b       │
└─────────────┘         └──────────────────┘         └─────────────────┘        │ :11434           │
                                 │                            │                 └──────────────────┘
                                 ▼                            ▼
                          ┌─────────────┐            ┌─────────────────┐
                          │ PostgreSQL  │            │ ai-server/data  │
                          │ :5432       │            │ (청크 인덱스)    │
                          └─────────────┘            └─────────────────┘
```

| 컴포넌트 | 책임 | 저장소 |
|----------|------|--------|
| Vue | 업로드 UI, 요약 카드, 채팅, 문서 목록 | 없음 |
| Rails | API 게이트웨이, 파일 검증, 메타데이터/요약/QA 저장, FastAPI 호출, 에러 매핑 | PostgreSQL |
| FastAPI | 텍스트 추출, 청크 분할, 요약(map-reduce), 검색, 답변 생성 | `ai-server/data/*.json` |
| Ollama | `gemma4:12b` 추론 (선택: 임베딩 모델) | 로컬 모델 |

## 2. 데이터 흐름

### 2.1 업로드 + 요약

1. Vue → `POST /api/documents` (multipart `file`)
2. Rails: 확장자/크기 검증 → FastAPI `POST /summarize` (multipart 전달)
3. FastAPI: 형식별 텍스트 추출(TXT/MD/PDF/DOCX/PPTX) → 청크 분할 → 인덱스 저장 → 청크별 요약 → 최종 요약 (gemma4:12b)
4. FastAPI → Rails: `{ document_id, summary, text, chunk_count }`
5. Rails: `documents` 행 저장 (`ai_document_id` 로 FastAPI 인덱스와 연결) → Vue 응답

### 2.2 질의응답

1. Vue → `POST /api/documents/:id/questions` `{ question }`
2. Rails → FastAPI `POST /ask` `{ document_id: ai_document_id, question }`
3. FastAPI: 관련 청크 top-k 검색 → 컨텍스트 + 질문으로 gemma4:12b 호출
4. FastAPI → Rails: `{ answer, sources: [{ chunk_index, text, score }] }`
5. Rails: `qa_histories` 저장 → Vue 응답

### 2.3 지원 파일 형식과 계층별 책임

| 계층 | 위치 | 역할 |
|------|------|------|
| Vue | `DocumentUpload.vue`의 `ALLOWED` | 선택·드롭 시 1차 검증, 안내 문구 |
| Rails | `Document::ALLOWED_EXTENSIONS` | 확장자·크기 검증, 구형 형식 안내 (텍스트 추출은 하지 않음) |
| FastAPI | `document_parser.SUPPORTED_EXTENSIONS`, `_EXTRACTORS` | 실제 텍스트 추출, 손상·암호 문서 거절 |

- 허용 확장자 목록이 세 곳에 있어 **형식을 추가할 때 세 곳을 함께 바꾼다.** (사용자 입력은 서버 쪽 검증이 최종 기준)
- 추출기: TXT/MD는 디코딩, PDF는 pypdf, DOCX는 python-docx, PPTX는 python-pptx.
- DOCX는 본문 순서대로 문단과 표를 추출하고 제목 스타일은 마크다운 `#`로 표시한다. PPTX는 `[슬라이드 N]` 단위로 텍스트·표·그룹 도형·`[발표자 노트]`를 추출한다.
- 안전장치: Office 문서는 압축 해제 크기 100MB 초과 시 거절(zip bomb 방어), 손상·암호 문서는 422.
- 이미지·차트·도형 모양은 추출하지 않는다.

## 3. 데이터 모델

### documents

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | bigint | PK |
| filename | string | 원본 파일명 |
| content_type | string | MIME |
| byte_size | integer | 파일 크기 |
| original_text | text | 추출된 원문 |
| summary | text | AI 요약 |
| ai_document_id | string | FastAPI 인덱스 ID (unique) |
| created_at / updated_at | datetime | |

### qa_histories

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | bigint | PK |
| document_id | bigint | FK → documents |
| question | text | 질문 |
| answer | text | 답변 |
| sources | jsonb | 근거 청크 목록 |
| created_at / updated_at | datetime | |

> 기획서의 `summaries` 테이블은 MVP에서 `documents.summary` 컬럼으로 통합했다. (1:1 관계)

## 4. LLM 설정 (Ollama)

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama 주소 |
| `OLLAMA_MODEL` | `gemma4:12b` | 요약/답변 모델 |
| `OLLAMA_EMBED_MODEL` | (빈 값) | 지정 시 임베딩 검색 (예: `bge-m3`), 빈 값이면 TF-IDF |
| `OLLAMA_NUM_CTX` | `8192` | 컨텍스트 길이 |
| `OLLAMA_TIMEOUT` | `300` | 초 단위 타임아웃 |

긴 문서는 컨텍스트 한계를 넘지 않도록 **청크별 부분 요약 → 통합 요약(map-reduce)** 으로 처리한다.
