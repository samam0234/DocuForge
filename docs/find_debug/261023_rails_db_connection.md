# 2026-10-23 디버깅 기록: Rails DB 연결

## 요약

| 순서 | 작업 | 결과 |
|--------|------|------|
| 1 | Docker 꺼짐 + PostgreSQL 미설치로 보여 DB 의존 검증 보류 | 이후 로컬 PostgreSQL 16 확인 |
| 2 | `bin/rails db:prepare` 실패 (`server closed the connection unexpectedly`) | 원인 조사 시작 |
| 3 | `psql`로 직접 접속 → 비밀번호 인증 실패 확인 | 원인 = 계정 비밀번호 불일치 |
| 4 | 전용 계정 `docuforge` 생성, `pg_hba.conf` 원복 | 접속 성공 |
| 5 | `db:prepare` → 마이그레이션 2건, `rails test` 5건 통과 | 해결 |
| 6 | Rails + AI 서버 연동 E2E 확인 | 업로드/질문 정상 |

## 막혔던 지점과 판단

1. **같은 에러, 다른 원인**: Rails 메시지는 "연결이 끊김"이었지만 실제는 인증 실패였다. `psql`/`pg` 젬으로 클라이언트를 단계별로 분리해 보니 원인이 드러났다.
2. **인증 설정 변경은 보수적으로**: 기존 `postgres` 비밀번호를 재설정하면 PC의 다른 프로젝트가 깨질 수 있어, 전용 계정 + 임시 trust + 즉시 원복 방식을 택했다.
3. **직후 일시 실패**: `pg_hba.conf` reload 직후 `db:prepare`가 한 번 더 같은 오류로 실패했으나, pg 젬 단독 접속은 정상이었고 `db:create` 재실행부터 정상 동작했다. reload 직후에는 잠시 후 재시도한다.

## 테스트 중 겪은 환경 이슈 (코드 문제 아님)

- Windows 콘솔(cp949)에서 `curl -d '{"question":"한글"}'`로 보내면 UTF-8이 아니어서 Rails가 `400 Invalid encoding for parameter`를 반환한다. 파일로 UTF-8 본문을 보내거나(`--data-binary @q.json`) 브라우저/프론트엔드를 사용한다.
- 같은 이유로 터미널 출력의 한글이 깨져 보일 수 있으나 응답 자체는 정상이다.

관련 장애 기록: [repeater/261023_postgres_auth_failure.md](../repeater/261023_postgres_auth_failure.md)
