# 병합 기록: 문서 형식 지원 (feature/* → develop → main)

| 항목 | 내용 |
|------|------|
| 일시 | 2026-10-25 09:22 |
| 작성자 | grok |
| 병합 방식 | `--no-ff` (사용자 명시적 지시: 남은 브랜치를 확인한 뒤 develop에 먼저 병합하고, 그다음 main에 병합) |
| 대상 | `feature/*` → `develop` → `main` |
| push | 수행하지 않음 |

## 1. 병합 순서와 결과

앞서 `2002a4b`에서 당시 `develop`(`1f44f71`)만 `main`에 들어가 있었다. 아래 feature 커밋은 그 병합에 포함되지 않았고, 이번에 `develop`으로 먼저 통합했다.

| 순서 | 브랜치 | 병합 직전 HEAD | 병합된 커밋 수 | develop 병합 커밋 |
|------|--------|----------------|----------------|-------------------|
| 1 | `feature/project-setup` | `34d0eec` | 5 | `a431181` |
| 2 | `feature/fastapi-init` | `4cb2855` | 4 | `91f8d7c` |
| 3 | `feature/rails-api` | `8da12ea` | 3 | `3bffed3` |
| 4 | `feature/vue-ui` | `b000edc` | 3 | 이 기록을 포함한 병합 커밋 |

이후 `develop`을 `main`에 `--no-ff`로 병합했다.

## 2. 반영 내용

- `feature/project-setup`: README 지원 형식 표, AGENTS.md 프로젝트 요약, 아키텍처 문서의 계층별 책임, 실행 가이드와 MVP 체크리스트
- `feature/fastapi-init`: MD, DOCX, PPTX 텍스트 추출(`office_parser`), 형식별 테스트, ai-server README
- `feature/rails-api`: MD, DOCX, PPTX 업로드 허용과 안내 메시지, 통합 테스트, backend README
- `feature/vue-ui`: 업로드 UI의 MD, DOCX, PPTX 지원과 형식 안내, frontend README

## 3. 충돌

- 없음. 브랜치가 서로 다른 파일만 수정했다.

## 4. 병합 후 상태

- 병합 후 브랜치는 삭제하지 않았다. (삭제는 별도 지시 필요)
- 네 feature 브랜치의 문서 형식 지원 커밋은 `develop`과 `main`에 모두 포함된다.

## 5. 검증 상태 (병합 시점)

- 이번 병합에서 테스트와 브라우저 확인을 다시 실행하지 않았다.
- 미검증: ai-server `pytest`, backend `bin/rails test`, frontend 빌드, 브라우저 업로드 E2E, `docker compose up`
