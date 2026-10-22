# 커밋 기록: test(backend): 문서 업로드 및 질문 흐름 통합 테스트 추가

| 항목 | 내용 |
|------|------|
| 일시 | 2026-10-23 06:22 |
| 커밋 ID | `f9be02e` |
| 작성자 | claude |
| 브랜치 | `feature/rails-api` |
| 커밋 메시지 | `test(backend): 문서 업로드 및 질문 흐름 통합 테스트 추가` |

## 1. 작업 목적

- FastAPI 없이도 Rails 오케스트레이션 흐름을 회귀 검증할 수 있게 한다.

## 2. 변경 내용

가짜 AiClient로 업로드-요약-질문-히스토리 흐름과
415, 400, 404, AI 서버 에러 전달을 검증한다.

## 3. 변경 파일

| 파일 | 구분 | 설명 |
|------|------|------|
| `backend/test/fixtures/files/.keep` | 추가 | |
| `backend/test/fixtures/files/sample.png` | 추가 | |
| `backend/test/fixtures/files/sample.txt` | 추가 | |
| `backend/test/integration/.keep` | 추가 | |
| `backend/test/integration/documents_flow_test.rb` | 추가 | |

## 4. 검증

- ruby -c 문법 확인만 완료. PostgreSQL 부재로 bin/rails test 미실행.

## 5. 비고 / 후속 작업

- DB 준비 후 bin/rails test 실행 필요.
