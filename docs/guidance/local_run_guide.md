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

Docker 사용 시:

```bash
docker compose up -d db
```

## 2. AI Server (FastAPI, :8000)

```bash
cd ai-server
py -3.12 -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

확인: `GET http://localhost:8000/health` → `{"status":"ok","model":"gemma4:12b","ollama":true}`

## 3. Backend (Rails, :3000)

```bash
cd backend
bundle install
bin/rails db:prepare
bin/rails server -p 3000
```

## 4. Frontend (Vue, :5173)

```bash
cd frontend
npm install
npm run dev
```

브라우저에서 `http://localhost:5173` 접속.

## 5. Docker Compose (전체)

Ollama는 호스트에서 실행하고, 컨테이너는 `host.docker.internal:11434`로 접근한다.

```bash
docker compose up --build
```
