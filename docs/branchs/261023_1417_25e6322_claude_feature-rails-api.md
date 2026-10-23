# 커밋 기록: feat(backend): dotenv-rails로 .env 자동 로드

| 항목 | 내용 |
|------|------|
| 일시 | 2026-10-23 14:17 |
| 커밋 ID | `25e6322` |
| 작성자 | claude |
| 브랜치 | `feature/rails-api` |
| 커밋 메시지 | `feat(backend): dotenv-rails로 .env 자동 로드` |

## 1. 작업 목적

- 터미널마다 환경 변수를 지정해야 DB에 접속되던 문제를 없앤다. dotenv가 Application 클래스 정의 시점에 로드되므로 파일 경로를 그 전에 지정한다.

## 2. 변경 내용

개발/테스트 환경에서 backend/.env와 루트 .env를 자동으로 읽는다.
셸 환경 변수가 가장 우선하며, 터미널마다 DB 계정을 지정하지 않아도
bin/rails db:prepare, server, test가 동작한다.
.env.example에 로컬 PostgreSQL 전용 계정 안내를 추가한다.

## 3. 변경 파일

| 파일 | 구분 | 설명 |
|------|------|------|
| `.env.example` | 수정 | |
| `backend/Gemfile` | 수정 | |
| `backend/Gemfile.lock` | 수정 | |
| `backend/config/application.rb` | 수정 | |

## 4. 검증

- 환경 변수 없이 bin/rails db:prepare 성공, bin/rails test 5 runs 0 failures, bin/rails server 기동 후 /up 200, /api/documents 200. 실행 위치(backend, 루트)와 무관하게 루트 .env를 읽음 확인.

## 5. 비고 / 후속 작업

- 루트 .env(gitignore 대상)의 DATABASE_USERNAME/PASSWORD를 docuforge로 채웠다. 기존 admin/DocuForge1234는 DB 인증 실패였다. ai-server는 자체 cwd의 .env만 읽으므로 이번 변경 대상이 아니다.
