# 커밋 기록: feat(ai-server): FastAPI 기본 설정 및 Ollama gemma4:12b 클라이언트 추가

| 항목 | 내용 |
|------|------|
| 일시 | 2026-10-23 06:18 |
| 커밋 ID | `bb6b108` |
| 작성자 | claude |
| 브랜치 | `feature/fastapi-init` |
| 커밋 메시지 | `feat(ai-server): FastAPI 기본 설정 및 Ollama gemma4:12b 클라이언트 추가` |

## 1. 작업 목적

- AI 서버의 설정과 Ollama gemma4:12b 호출 계층을 분리해 이후 요약/RAG 로직이 재사용하도록 한다.

## 2. 변경 내용

환경 변수 기반 설정(모델, 컨텍스트 길이, 타임아웃)과 요청/응답 스키마를 정의한다.
Ollama /api/chat, /api/embed 호출 클라이언트와 Dockerfile을 추가한다.

## 3. 변경 파일

| 파일 | 구분 | 설명 |
|------|------|------|
| `ai-server/.dockerignore` | 추가 | |
| `ai-server/Dockerfile` | 추가 | |
| `ai-server/README.md` | 추가 | |
| `ai-server/app/__init__.py` | 추가 | |
| `ai-server/app/config.py` | 추가 | |
| `ai-server/app/models/__init__.py` | 추가 | |
| `ai-server/app/models/schemas.py` | 추가 | |
| `ai-server/app/services/__init__.py` | 추가 | |
| `ai-server/app/services/ollama_client.py` | 추가 | |
| `ai-server/requirements.txt` | 추가 | |

## 4. 검증

- GET /health 에서 model=gemma4:12b, ollama=true 확인.

## 5. 비고 / 후속 작업

- think=false 로 호출하여 추론 토큰 없이 바로 답변을 받는다.
