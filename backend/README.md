# DocuForge Backend (Rails API)

Vue와 FastAPI 사이의 오케스트레이터. 파일 검증, FastAPI 호출, 메타데이터/요약/질문 기록의 PostgreSQL 저장을 담당한다. 프론트엔드가 호출하는 유일한 서버다.

## 사전 준비

- Ruby 3.4, Bundler, Rails 8.1
- PostgreSQL 16 (`docker compose up -d db` 또는 로컬 설치)
- AI 서버(`ai-server/`)가 `:8000`에서 실행 중이어야 업로드/질문이 동작한다.

## 실행

```bash
cd backend
bundle install
bin/rails db:prepare          # DB 생성 + 마이그레이션
bin/rails server -p 3000
```

확인: `GET http://localhost:3000/up` → 200

> `dotenv-rails`가 개발/테스트 환경에서 `.env`를 자동으로 읽는다. 읽는 순서(먼저 읽은 값이 우선):
> 셸 환경 변수 → `backend/.env`(앱 전용) → 루트 `.env`(전체 서비스 공유)
> 루트 `.env.example`을 복사해 `.env`를 만들고 DB 계정을 채운다.
> ```
> DATABASE_USERNAME=docuforge
> DATABASE_PASSWORD=docuforge
> ```

### 로컬 PostgreSQL 연결 문제

기본 접속 정보는 `postgres` / `postgres`이다. 로컬에 설치한 PostgreSQL의 `postgres` 비밀번호가 다르면
`db:prepare`가 **`server closed the connection unexpectedly`** 로 실패한다. (실제 원인은 인증 실패)

1. `psql -h localhost -U postgres -d postgres`로 직접 접속해 인증 문제인지 확인한다.
2. 실제 비밀번호를 `.env`의 `DATABASE_PASSWORD`로 지정하거나, 전용 계정을 만들어 사용한다.
   `CREATE ROLE docuforge LOGIN CREATEDB PASSWORD 'docuforge';`

자세한 내용: [docs/repeater/261023_postgres_auth_failure.md](../docs/repeater/261023_postgres_auth_failure.md)

### 서버가 시작되지 않을 때

| 증상 | 원인 / 해결 |
|------|-------------|
| `A server is already running (pid: …)` 후 종료 | 강제 종료된 서버의 PID 파일이 남음. `tasklist`/`netstat -ano`로 프로세스가 없음을 확인하고 `tmp/pids/server.pid` 삭제 후 재실행 |
| 서버는 뜨는데 업로드/질문이 502 | AI 서버(`:8000`) 미실행. `curl localhost:8000/health` 확인 |
| 프론트엔드에서 "서버에 연결할 수 없습니다" | `http://localhost:5173`으로 접속했는지 확인 (`127.0.0.1`은 CORS 차단, `FRONTEND_ORIGIN`에 추가 가능) |
| `bin/rails sever` | 오타. `bin/rails server`(또는 `s`) |

서버는 `Ctrl+C`로 종료한다. 자세한 내용: [docs/repeater/261023_rails_stale_server_pid.md](../docs/repeater/261023_rails_stale_server_pid.md)

## 환경 변수

루트 `.env.example` 참고.

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `DATABASE_HOST` / `DATABASE_PORT` | `localhost` / `5432` | PostgreSQL 주소 |
| `DATABASE_USERNAME` / `DATABASE_PASSWORD` | `postgres` / `postgres` | 접속 계정 |
| `AI_SERVER_URL` | `http://localhost:8000` | FastAPI 주소 |
| `AI_SERVER_TIMEOUT` | `600` | AI 서버 응답 대기(초). 긴 문서 요약을 고려해 길게 둠 |
| `FRONTEND_ORIGIN` | `http://localhost:5173` | CORS 허용 출처 (쉼표로 여러 개) |
| `MAX_UPLOAD_MB` | `10` | 업로드 최대 크기 |

## API

| Method | Path | 설명 | 에러 |
|--------|------|------|------|
| GET | `/api/documents` | 최근 문서 20개 (`summary_preview` 포함) | |
| POST | `/api/documents` | multipart `file` 업로드 → AI 요약 → 저장 (201) | 400, 413, 415, 422, 502, 504 |
| GET | `/api/documents/:id` | 문서 + 요약 | 404 |
| GET | `/api/documents/:id/questions` | 질문 히스토리 (오래된 순) | 404 |
| POST | `/api/documents/:id/questions` | `{ question }` → 답변 + 근거 (201) | 400, 404, 502, 504 |

에러 응답 형식: `{ "error": "한국어 메시지" }`

| 코드 | 의미 |
|------|------|
| 400 | 파일 또는 질문 누락 |
| 404 | 문서 없음 / AI 인덱스 없음 |
| 413 / 415 / 422 | 크기 초과 / 미지원 형식(구형 `.doc`/`.ppt`는 변환 안내) / 텍스트 추출 불가·손상·암호 문서 (AI 서버 응답 전달) |
| 502 | AI 서버 연결 실패, 또는 AI 서버/Ollama 오류(503 포함)를 Rails가 502로 변환 |
| 504 | AI 서버 응답 시간 초과 |

## 지원 파일 형식

`.txt`, `.md`(`.markdown`), `.pdf`, `.docx`, `.pptx` — `Document::ALLOWED_EXTENSIONS`

- Rails는 확장자와 크기(`MAX_UPLOAD_MB`)만 검증하고, 텍스트 추출은 FastAPI가 담당한다.
- 구형 `.doc`, `.ppt`는 415와 함께 "`.docx`/`.pptx`로 저장한 뒤 업로드" 안내를 반환한다.
- 형식을 추가할 때는 FastAPI(`document_parser.py`), 이 모델의 `ALLOWED_EXTENSIONS`/`SUPPORTED_LABEL`, Vue(`DocumentUpload.vue`)를 함께 바꾼다.

## 데이터 모델

| 테이블 | 주요 컬럼 |
|--------|-----------|
| `documents` | filename, content_type, byte_size, original_text, summary, `ai_document_id`(unique) |
| `qa_histories` | document_id(FK, cascade), question, answer, sources(jsonb) |

`ai_document_id`는 FastAPI 청크 인덱스의 ID이며, 질문 시 이 값으로 `/ask`를 호출한다.

## 처리 흐름

```
POST /api/documents
  → 확장자(Document::ALLOWED_EXTENSIONS)·크기 검증 → AiClient#summarize (FastAPI /summarize)
  → Document 저장 → 201

POST /api/documents/:id/questions
  → AiClient#ask (FastAPI /ask) → QaHistory 저장 → 201
```

## 구조

```
app/
├── controllers/
│   ├── application_controller.rb   # 공통 에러 처리(rescue_from)
│   ├── documents_controller.rb
│   └── questions_controller.rb
├── models/
│   ├── document.rb
│   └── qa_history.rb
└── services/
    └── ai_client.rb                # FastAPI 호출, 에러 → HTTP 상태 매핑
config/
├── routes.rb
├── database.yml                    # 환경 변수 기반
└── initializers/cors.rb            # 프론트엔드 출처만 허용
db/migrate/                         # documents, qa_histories
```

## 테스트

```bash
bin/rails test        # AiClient는 가짜 객체로 대체, PostgreSQL 필요 (.env의 DB 계정 사용)
```

## Docker

`Dockerfile.dev`는 docker-compose 전용 개발 이미지다. 컨테이너 시작 시 `db:prepare`를 실행한다.
