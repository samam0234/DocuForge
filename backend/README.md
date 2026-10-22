# DocuForge Backend (Rails API)

Vue와 FastAPI 사이의 오케스트레이터. 파일 검증, FastAPI 호출, 메타데이터/요약/질문 기록을 PostgreSQL에 저장한다.

## 실행

```bash
bundle install
bin/rails db:prepare          # PostgreSQL 필요 (docker compose up -d db)
bin/rails server -p 3000
```

환경 변수 (루트 `.env.example` 참고)

| 변수 | 기본값 |
|------|--------|
| `DATABASE_HOST` / `DATABASE_PORT` | `localhost` / `5432` |
| `DATABASE_USERNAME` / `DATABASE_PASSWORD` | `postgres` / `postgres` |
| `AI_SERVER_URL` | `http://localhost:8000` |
| `AI_SERVER_TIMEOUT` | `600` (초) |
| `FRONTEND_ORIGIN` | `http://localhost:5173` |
| `MAX_UPLOAD_MB` | `10` |

## API

| Method | Path | 설명 | 주요 에러 |
|--------|------|------|-----------|
| GET | `/api/documents` | 최근 문서 20개 | |
| POST | `/api/documents` | multipart `file` 업로드 → 요약 | 400, 413, 415, 422, 502, 504 |
| GET | `/api/documents/:id` | 문서 + 요약 | 404 |
| GET | `/api/documents/:id/questions` | 질문 히스토리 | 404 |
| POST | `/api/documents/:id/questions` | `{ question }` → 답변 + 근거 | 400, 404, 502, 504 |

에러 응답 형식: `{ "error": "한국어 메시지" }`

## 구조

```
app/
├── controllers/
│   ├── application_controller.rb   # 공통 에러 처리
│   ├── documents_controller.rb
│   └── questions_controller.rb
├── models/
│   ├── document.rb
│   └── qa_history.rb
└── services/
    └── ai_client.rb                # FastAPI /summarize, /ask 호출
```

## 테스트

```bash
bin/rails test        # AiClient는 가짜 객체로 대체, PostgreSQL 필요
```
