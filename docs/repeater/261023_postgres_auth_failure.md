# PostgreSQL 인증 실패로 Rails 마이그레이션/서버 실행 불가

| 항목 | 내용 |
|------|------|
| 일자 | 2026-10-23 |
| 영역 | backend ↔ PostgreSQL |
| 환경 | Windows 11, PostgreSQL 16 (`D:\PostgreSQL\16`, 서비스 `postgresql-x64-16`), Rails 8.1, Ruby 3.4 |

## 증상

```
bin/rails db:prepare
ActiveRecord::ConnectionNotEstablished: connection to server at "::1", port 5432 failed:
server closed the connection unexpectedly
```

`bin/rails server`와 `bin/rails test`도 DB 연결 단계에서 실패.

## 원인

- PostgreSQL 서비스와 5432 포트는 정상이었다.
- `config/database.yml` 기본 접속 정보(`postgres` / `postgres`)와 이 PC의 `postgres` 계정 비밀번호가 달랐다.
- `psql -h localhost -U postgres`로 직접 접속해도 `password authentication failed`.
- Rails의 `server closed the connection unexpectedly` 메시지는 실제 원인(인증 실패)을 가려서 **원인 파악을 어렵게** 했다.
- `pg_hba.conf`는 localhost도 `scram-sha-256`이라 비밀번호 없이는 접속 불가.

## 해결

기존 `postgres` 계정/비밀번호는 건드리지 않고 **프로젝트 전용 계정**을 만들었다.

1. `pg_hba.conf` 백업 (`pg_hba.conf.docuforge.bak`)
2. localhost 두 줄(`127.0.0.1/32`, `::1/128`)만 잠시 `trust`로 변경 후 `pg_ctl reload`
3. 전용 계정 생성

   ```sql
   CREATE ROLE docuforge LOGIN CREATEDB PASSWORD 'docuforge';
   ```
4. `pg_hba.conf`를 백업본으로 즉시 원복 후 reload, `diff`로 동일 확인
5. 확인: `postgres/postgres`는 여전히 거부, `docuforge/docuforge`는 접속 성공
6. Rails 실행 시 환경 변수 지정

   ```powershell
   $env:DATABASE_USERNAME = "docuforge"; $env:DATABASE_PASSWORD = "docuforge"
   bin/rails db:prepare
   ```

결과: 마이그레이션 2건 적용, `bin/rails test` 5 runs 0 failures.

## 재발 방지 / 참고

- 로컬에 이미 PostgreSQL이 있는 경우 `postgres` 계정 비밀번호가 기본값과 다를 수 있다. 연결 오류 시 먼저 `psql -h localhost -U <계정>`으로 **직접 접속**해 인증 문제인지 구분한다.
- 개발용 `docuforge/docuforge` 계정은 로컬 전용이다. 배포 환경에서는 사용하지 않는다.
- `pg_hba.conf` 백업 파일은 확인 후 사용자 판단으로 삭제한다.
