# 커밋 기록: docs(backend): README에 로컬 PostgreSQL 연결 문제 해결 방법 추가

| 항목 | 내용 |
|------|------|
| 일시 | 2026-10-23 06:57 |
| 커밋 ID | `bd54e7c` |
| 작성자 | claude |
| 브랜치 | `feature/rails-api` |
| 커밋 메시지 | `docs(backend): README에 로컬 PostgreSQL 연결 문제 해결 방법 추가` |

## 1. 작업 목적

- 로컬 PostgreSQL 사용 시 겪은 연결 실패의 원인과 해결을 backend README에서 바로 찾을 수 있게 한다.

## 2. 변경 내용

환경 변수 지정 방법과 비밀번호 불일치 시 증상, 확인 절차를 안내하고
502 에러 코드 설명을 실제 변환 동작에 맞게 정정한다.

## 3. 변경 파일

| 파일 | 구분 | 설명 |
|------|------|------|
| `backend/README.md` | 수정 | |

## 4. 검증

- README 내용을 실제 수행 절차 및 ai_client.rb(PASS_THROUGH)와 대조. 링크 대상 파일은 feature/project-setup에 존재.

## 5. 비고 / 후속 작업

- 링크한 docs/repeater 문서는 feature/project-setup 브랜치에 있어 병합 전까지 이 브랜치에서는 링크가 끊겨 있다.
