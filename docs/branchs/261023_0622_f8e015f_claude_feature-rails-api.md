# 커밋 기록: feat(backend): 문서 업로드/요약 및 질의응답 API 구현

| 항목 | 내용 |
|------|------|
| 일시 | 2026-10-23 06:22 |
| 커밋 ID | `f8e015f` |
| 작성자 | claude |
| 브랜치 | `feature/rails-api` |
| 커밋 메시지 | `feat(backend): 문서 업로드/요약 및 질의응답 API 구현` |

## 1. 작업 목적

- Vue ↔ FastAPI 사이에서 업로드 검증, AI 호출, 결과 저장을 담당하는 API를 구현한다.

## 2. 변경 내용

documents, qa_histories 테이블과 모델을 추가한다.
AiClient 서비스로 FastAPI /summarize, /ask를 호출하고,
/api/documents, /api/documents/:id/questions 엔드포인트와
공통 에러 처리(404, 413, 415, 502, 504)를 구현한다.

## 3. 변경 파일

| 파일 | 구분 | 설명 |
|------|------|------|
| `backend/app/controllers/application_controller.rb` | 추가 | |
| `backend/app/controllers/documents_controller.rb` | 추가 | |
| `backend/app/controllers/questions_controller.rb` | 추가 | |
| `backend/app/models/document.rb` | 추가 | |
| `backend/app/models/qa_history.rb` | 추가 | |
| `backend/app/services/ai_client.rb` | 추가 | |
| `backend/config/routes.rb` | 추가 | |
| `backend/db/migrate/20261023000001_create_documents.rb` | 추가 | |
| `backend/db/migrate/20261023000002_create_qa_histories.rb` | 추가 | |

## 4. 검증

- bin/rails routes로 5개 엔드포인트 확인. bin/rails runner로 AiClient를 실제 FastAPI(gemma4:12b)에 연결해 요약/답변 성공, 404·415 전달, 서버 다운 시 502 매핑을 확인했다.

## 5. 비고 / 후속 작업

- 로컬에 PostgreSQL이 없어(Docker 데몬 미실행) 마이그레이션과 DB 저장은 미검증. docker compose up -d db 후 bin/rails db:prepare 필요.
