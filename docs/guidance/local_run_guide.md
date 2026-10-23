# 로컬 실행 가이드

## 0. 사전 준비

| 도구 | 버전 (확인 기준) |
|------|------------------|
| Ollama | 0.40+ (`ollama pull gemma4:12b`) |
| Python | 3.12 |
| Ruby / Rails | 3.4 / 8.1 |
| Node.js | 24 |
| PostgreSQL | 16 (로컬 설치 또는 Docker) |

```bash
ollama pull gemma4:12b
ollama list   # gemma4:12b 확인
```

## 1. PostgreSQL

두 가지 중 하나를 선택한다.

### A. Docker

```bash
docker compose up -d db      # postgres / postgres 계정
```

### B. 로컬 설치 PostgreSQL (Windows 등)

Rails 기본 접속 정보는 `postgres` / `postgres`이다. 로컬 `postgres` 계정의 비밀번호가 다르면
`bin/rails db:prepare`가 `server closed the connection unexpectedly`로 실패한다.
(원인과 해결: [repeater/261023_postgres_auth_failure.md](../repeater/261023_postgres_auth_failure.md))

선택지 (어느 쪽이든 값은 루트 `.env`에 적는다):

1. 기존 비밀번호를 사용한다.

   ```
   DATABASE_PASSWORD=실제비밀번호
   ```

2. 프로젝트 전용 계정을 만든다. (기존 계정에 영향 없음)

   ```sql
   CREATE ROLE docuforge LOGIN CREATEDB PASSWORD 'docuforge';
   ```

   ```
   DATABASE_USERNAME=docuforge
   DATABASE_PASSWORD=docuforge
   ```

접속 여부는 Rails보다 `psql`로 먼저 확인하면 원인 구분이 쉽다.

```bash
psql -h localhost -U <계정> -d postgres -c "select 1"
```

## 2. AI Server (FastAPI, :8000)

```bash
cd ai-server
py -3.12 -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

확인: `GET http://localhost:8000/health` → `{"status":"ok","model":"gemma4:12b","embed_model":null,"ollama":true}`

## 3. Backend (Rails, :3000)

```bash
cd backend
bundle install
bin/rails db:prepare           # DB 생성 + 마이그레이션 (PostgreSQL 필요)
bin/rails server -p 3000
```

확인: `GET http://localhost:3000/up` → 200

> Rails는 `dotenv-rails`로 `.env`를 자동 로드한다. 읽는 순서(먼저 읽은 값이 우선):
> 셸 환경 변수 → `backend/.env` → 루트 `.env`
> 루트 `.env.example`을 복사해 `.env`를 만들고 `DATABASE_USERNAME`, `DATABASE_PASSWORD` 등을 채운다.
> (`.env`는 `.gitignore` 대상이라 커밋되지 않는다.)

서버는 `Ctrl+C`로 종료한다. 강제 종료하면 `tmp/pids/server.pid`가 남아 다음 실행이 막힐 수 있다. (7장 참고)

테스트: `bin/rails test`

## 4. Frontend (Vue, :5173)

```bash
cd frontend
npm install
npm run dev
```

브라우저에서 `http://localhost:5173` 접속.

## 5. 빠른 동작 확인 (curl)

```bash
curl -F "file=@sample.txt" http://localhost:3000/api/documents          # 업로드 + 요약 (201)
curl http://localhost:3000/api/documents                                # 목록
curl -X POST http://localhost:3000/api/documents/1/questions \
     -H "Content-Type: application/json; charset=utf-8" \
     --data-binary @question.json                                       # {"question":"..."}
```

> Windows 콘솔에서 `-d '{"question":"한글"}'`처럼 직접 넣으면 UTF-8이 아니어서 `400 Invalid encoding`이 날 수 있다.
> 파일(UTF-8)로 보내거나 프론트엔드를 사용한다.

## 6. Docker Compose (전체)

Ollama는 호스트에서 실행하고, 컨테이너는 `host.docker.internal:11434`로 접근한다.

```bash
docker compose up --build
```

## 7. 자주 만나는 문제

| 증상 | 원인 / 확인 |
|------|-------------|
| `db:prepare`가 `server closed the connection unexpectedly` | PostgreSQL 계정 비밀번호 불일치. `.env`의 `DATABASE_USERNAME/PASSWORD`를 `psql`로 먼저 검증 → 1.B 참고 |
| 업로드/질문 시 502 ("AI 서버에 연결할 수 없습니다") | AI 서버(:8000) 미실행. backend만 실행하면 업로드·질문은 항상 이 오류 → `curl localhost:8000/health` 확인 |
| 업로드/질문 시 502 ("AI 모델 호출 실패") | AI 서버는 503을 내고 Rails가 502로 전달. Ollama 미실행 또는 `gemma4:12b` 미설치 → `/health`의 `ollama` 값 확인 |
| `bin/rails server`가 `A server is already running (pid: …)`로 종료 | 죽은 서버의 PID 파일 잔존. `tasklist`/`netstat`으로 프로세스가 없음을 확인 후 `backend/tmp/pids/server.pid` 삭제 → [repeater/261023_rails_stale_server_pid.md](../repeater/261023_rails_stale_server_pid.md) |
| 프론트엔드가 "서버에 연결할 수 없습니다" | ① `curl localhost:3000/up`으로 Rails 확인 ② 주소를 `http://localhost:5173`으로 접속(`127.0.0.1`은 CORS 차단, 필요하면 `FRONTEND_ORIGIN`에 추가) ③ 새로고침 |
| 서버 명령이 실행되지 않고 `3000`만 출력 | 명령어 오타 (`sever` → `server`) |
| 업로드가 오래 걸림 | 긴 문서는 map-reduce 요약으로 1분 이상 소요 가능 (Rails 대기 600초) |
