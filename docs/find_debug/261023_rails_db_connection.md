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

---

## 추가 이슈: "서버에 연결할 수 없다" 3종 (같은 날 후속)

| 순서 | 증상 | 원인 | 조치 |
|------|------|------|------|
| 7 | 업로드 시 "AI 서버에 연결할 수 없습니다" (Rails 로그 502, `ECONNREFUSED`) | backend만 실행하고 AI 서버(:8000)를 띄우지 않음 | `uvicorn app.main:app --port 8000` 실행 |
| 8 | 프론트엔드가 "서버에 연결할 수 없습니다. Rails 서버(:3000)…" | Rails 정상(`/up` 200)이었고 브라우저 요청도 Rails에 도달. 서버 재시작 시점의 오류 화면이 남았거나 `127.0.0.1:5173` 접속(CORS 차단) 가능성 | 새로고침, `localhost:5173`으로 접속. 재현 불가라 사용자에게 문구·동작을 확인 요청 |
| 9 | `bin/rails server -p 3000`이 즉시 종료 (`A server is already running (pid: …)`) | 죽은 서버의 `tmp/pids/server.pid` 잔존 | PID 파일 삭제 후 정상 기동 |

### 판단 메모

- 같은 문구라도 계층이 다르다. 화면 문구(프론트) / Rails 502 메시지 / Puma 기동 실패는 각각 원인이 달랐다. **로그를 먼저 본다**: `backend/log/development.log`에 요청이 도달했는지로 브라우저→Rails 구간 문제인지 구분됐다.
- 사용자가 직접 실행할 때와 에이전트 세션에서 실행할 때의 환경(환경 변수, 점유 포트, PID 파일)이 다르다. 에이전트가 띄운 서버가 남기는 PID 파일이 사용자의 실행을 막을 수 있으므로, 확인용 서버는 확인 후 종료하고 PID 파일까지 정리한다.
- `main`에는 아직 `dotenv-rails`가 없어(`feature/rails-api`에만 있음) 직접 실행 시 `.env`가 자동 로드되지 않는다. 병합 전에는 `set -a; . ./.env; set +a`로 셸에 로드한다.

관련 장애 기록: [repeater/261023_rails_stale_server_pid.md](../repeater/261023_rails_stale_server_pid.md)
