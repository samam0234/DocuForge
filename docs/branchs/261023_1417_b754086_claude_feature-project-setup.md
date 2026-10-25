# 커밋 기록: docs(guidance): 실행 가이드의 .env 로드 설명을 dotenv-rails 기준으로 수정

| 항목 | 내용 |
|------|------|
| 일시 | 2026-10-23 14:17 |
| 커밋 ID | `b754086` |
| 작성자 | claude |
| 브랜치 | `feature/project-setup` |
| 커밋 메시지 | `docs(guidance): 실행 가이드의 .env 로드 설명을 dotenv-rails 기준으로 수정` |

## 1. 작업 목적

- dotenv-rails 도입으로 달라진 환경 변수 로드 방식을 실행 가이드에 반영한다.

## 2. 변경 내용

Rails가 .env를 자동 로드하는 동작과 읽는 순서를 반영하고,
DB 계정 설정 방법을 .env 기준으로 정리한다.

## 3. 변경 파일

| 파일 | 구분 | 설명 |
|------|------|------|
| `docs/guidance/local_run_guide.md` | 수정 | |

## 4. 검증

- feature/rails-api의 실제 동작 확인 결과(환경 변수 없이 db:prepare/server/test 성공)와 대조.

## 5. 비고 / 후속 작업

- 없음
