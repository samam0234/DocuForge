# 병합 기록: dotenv 자동 로드 및 서버 기동 문서 (develop → main)

| 항목 | 내용 |
|------|------|
| 일시 | 2026-10-25 09:20 |
| 작성자 | grok |
| 병합 방식 | `--no-ff` (사용자 명시적 지시: "main 병합 ㄱㄱ") |
| 대상 | `develop` → `main` |
| develop HEAD | `1f44f71` |
| push | 수행하지 않음 |

## 1. 병합 순서와 결과

이번 지시는 이미 `develop`에 통합된 내용을 `main`에 반영하는 병합이다. feature 브랜치를 다시 통합하지 않았다.

| 순서 | 브랜치 | 비고 |
|------|--------|------|
| 1 | `develop` (`1f44f71`) | 이 기록을 포함한 `main` 병합 커밋 |

`develop`에 이미 반영된 선행 병합:

| 브랜치 | 병합 직전 HEAD | 병합된 커밋 수 | develop 병합 커밋 |
|--------|----------------|----------------|-------------------|
| `feature/project-setup` | `2fd0fc1` | 7 | `a3277f1` |
| `feature/rails-api` | `a41efba` | 5 | `1f44f71` |

`feature/fastapi-init`, `feature/vue-ui`는 위 develop 범위에 추가 커밋이 없다.

문서 형식(MD, DOCX, PPTX) 지원 커밋은 아직 각 feature 브랜치에만 있어 이번 병합에 포함하지 않았다.

| 브랜치 | 미반영 HEAD |
|--------|-------------|
| `feature/fastapi-init` | `4cb2855` |
| `feature/project-setup` | `34d0eec` |
| `feature/rails-api` | `8da12ea` |
| `feature/vue-ui` | `b000edc` |

## 2. 반영 내용

- `feature/rails-api`: dotenv-rails로 `.env` 자동 로드(`config/application.rb`, `Gemfile`), 서버 시작 실패 해결표(backend README)
- `feature/project-setup`: Rails 서버 PID 파일 잔존 장애 기록(`docs/repeater`), 디버깅 기록 갱신, 실행 가이드의 서버 기동·연결 문제 해결표

## 3. 충돌

- 없음.

## 4. 병합 후 상태

- 병합 후 브랜치는 삭제하지 않았다. (삭제는 별도 지시 필요)
- `main`에서 dotenv 자동 로드와 서버 기동 문서가 develop과 같은 내용이 된다.

## 5. 검증 상태 (병합 시점)

- 이번 `main` 병합에서 테스트를 다시 실행하지 않았다.
- develop 병합 시점 기록: backend `bin/rails test` 5 runs 0 failures, 환경 변수 없이 `db:prepare`/`server` 기동 및 `/up` 200 확인
- 미검증: 브라우저 UI E2E, `docker compose up`, 413 응답, 실제 스캔 PDF
