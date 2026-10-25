# Rails 서버가 "already running"으로 시작되지 않음 (죽은 서버의 PID 파일 잔존)

| 항목 | 내용 |
|------|------|
| 일자 | 2026-10-23 |
| 영역 | backend (Rails/Puma) |
| 환경 | Windows 11, Git Bash, Rails 8.1, Puma 8 |

## 증상

```
bin/rails server -p 3000
=> Booting Puma
A server is already running (pid: 48384, file: .../backend/tmp/pids/server.pid).
Exiting
```

- 3000 포트에는 아무 프로세스도 없고(`netstat`), Ruby 프로세스도 없는데 서버가 시작되지 않는다.
- 브라우저/프론트엔드에는 "서버에 연결할 수 없습니다"가 표시된다.
- DB 마이그레이션은 이미 성공한 상태였다. (DB 문제가 아님)

## 원인

- 이전에 실행한 Rails 서버가 `Ctrl+C` 같은 정상 종료 없이 사라졌다. (백그라운드 실행 세션 종료, 프로세스 강제 종료 등)
- Puma는 시작할 때 `tmp/pids/server.pid`를 만들고 정상 종료 때 지우는데, 강제 종료되면 **파일만 남는다**.
- 다음 실행 때 Rails가 이 파일의 PID를 보고 "이미 실행 중"이라고 판단해 종료한다. 해당 PID의 프로세스가 실제로 살아 있는지는 확인하지 않는다.

## 해결

1. 정말 죽은 프로세스인지 확인한다.

   ```bash
   tasklist | grep -i ruby          # 없으면 죽은 것
   netstat -ano | grep ":3000 .*LISTENING"
   ```
2. PID 파일 삭제 후 재실행한다. (`tmp/`는 gitignore 대상인 런타임 파일)

   ```bash
   rm backend/tmp/pids/server.pid
   bin/rails server -p 3000
   ```

결과: `GET /up` 200, `GET /api/documents` 200.

## 같이 확인된 사항

- `bin/rails sever`처럼 **명령어 오타**는 서버를 띄우지 않고 `3000`만 출력하고 끝난다. 반드시 `server`(또는 `s`).
- 3000 포트에 **살아 있는 서버가 있는 경우**에는 PID 파일을 지우지 말고 그 프로세스를 먼저 종료한다. (`taskkill //PID <pid> //F`)
- 프론트엔드는 `http://localhost:5173`으로 접속해야 한다. `127.0.0.1:5173`은 CORS(`FRONTEND_ORIGIN`)에서 막혀 같은 "서버에 연결할 수 없습니다"가 나온다.
- 업로드/질문의 502(`AI 서버에 연결할 수 없습니다`)는 Rails가 아니라 **AI 서버(:8000) 미실행** 때문이다.

## 재발 방지

- 서버는 `Ctrl+C`로 종료한다. 강제 종료했다면 다음 실행 전에 PID 파일을 확인한다.
- "Rails에 연결 안 됨" 증상은 아래 순서로 구분한다.
  1. `curl localhost:3000/up` → 응답 없음: Rails 미실행 또는 PID 파일 문제
  2. 200이면 브라우저 접속 주소(localhost vs 127.0.0.1)와 CORS 확인
  3. 업로드/질문만 502면 `curl localhost:8000/health`로 AI 서버 확인

관련: [261023_postgres_auth_failure.md](261023_postgres_auth_failure.md)
