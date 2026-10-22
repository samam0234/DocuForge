# 커밋 기록: chore(backend): db/schema.rb 추가

| 항목 | 내용 |
|------|------|
| 일시 | 2026-10-23 06:54 |
| 커밋 ID | `f44a434` |
| 작성자 | claude |
| 브랜치 | `feature/rails-api` |
| 커밋 메시지 | `chore(backend): db/schema.rb 추가` |

## 1. 작업 목적

- PostgreSQL 연동 후 생성된 스키마를 버전 관리하여 db:schema:load 등으로 재현 가능하게 한다.

## 2. 변경 내용

PostgreSQL에서 db:prepare를 실행해 생성된 스키마 파일을 저장소에 포함한다.
documents, qa_histories 테이블과 인덱스, 외래 키(cascade)가 반영되어 있다.

## 3. 변경 파일

| 파일 | 구분 | 설명 |
|------|------|------|
| `backend/db/schema.rb` | 추가 | |

## 4. 검증

- docuforge 전용 계정으로 db:prepare 성공, bin/rails test 5 runs 0 failures. Rails(:3000)+AI서버(:8000)로 업로드(201)→질문(201)→히스토리 조회, CORS, 415 응답 확인.

## 5. 비고 / 후속 작업

- postgres 계정 비밀번호가 기본값과 달라 docuforge 전용 계정(DATABASE_USERNAME/PASSWORD 환경 변수)으로 접속한다.
