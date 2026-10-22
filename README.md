# DocuForge

**AI 기반 문서 요약 및 질의응답 플랫폼** — TXT/PDF를 업로드하면 로컬 LLM(Ollama `gemma4:12b`)이 요약하고, 문서 내용에 기반해 질문에 답한다.

```
Vue 3 (:5173) ──▶ Rails 8 API (:3000) ──▶ FastAPI (:8000) ──▶ Ollama gemma4:12b (:11434)
                        │
                        ▼
                  PostgreSQL (:5432)
```

## 구성

| 디렉터리 | 역할 |
|----------|------|
| [`frontend/`](frontend/) | Vue 3 + Vite — 업로드, 요약 카드, 채팅 UI |
| [`backend/`](backend/) | Rails API — 오케스트레이션, 메타데이터/QA 저장 |
| [`ai-server/`](ai-server/) | FastAPI — 텍스트 추출, 요약, RAG 답변 |
| [`docs/`](docs/) | 기획·아키텍처·커밋 기록·가이드 |

## 빠른 시작

```bash
ollama pull gemma4:12b
docker compose up -d db

# 1) AI 서버
cd ai-server && py -3.12 -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt && uvicorn app.main:app --port 8000

# 2) Rails
cd backend && bundle install && bin/rails db:prepare && bin/rails s -p 3000

# 3) Vue
cd frontend && npm install && npm run dev
```

자세한 내용: [docs/guidance/local_run_guide.md](docs/guidance/local_run_guide.md)

## API

| Method | Endpoint (Rails) | 설명 |
|--------|------------------|------|
| GET | `/api/documents` | 최근 문서 목록 |
| POST | `/api/documents` | 파일 업로드 + 요약 |
| GET | `/api/documents/:id` | 문서 + 요약 조회 |
| POST | `/api/documents/:id/questions` | 질문 전송 |
| GET | `/api/documents/:id/questions` | 질문 히스토리 |

| Method | Endpoint (FastAPI) | 설명 |
|--------|--------------------|------|
| GET | `/health` | 상태 + Ollama 연결 확인 |
| POST | `/summarize` | 파일 → 요약 + document_id |
| POST | `/ask` | `{ document_id, question }` → 답변 + 근거 |

## 규칙

작업 규칙(커밋 형식, 브랜치 전략 등)은 [AGENTS.md](AGENTS.md)를 따른다.
