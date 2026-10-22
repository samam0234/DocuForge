# AGENTS.md — DocuForge 공통 규칙 (SSOT)

> 이 파일이 **단일 진실 공급원(Single Source of Truth)** 이다.
> `.Claude/`, `.Codex/`, `.Cursor/` 등 에이전트별 파일은 이 문서를 가리키기만 하며,
> 규칙이 충돌하면 항상 이 파일이 우선한다.

---

## 1. 프로젝트 요약

DocuForge는 업로드한 문서(TXT, PDF)를 AI가 요약하고, 문서 내용 기반 질의응답(RAG)을 제공하는 플랫폼이다.

| 레이어 | 기술 | 디렉터리 | 포트 |
|--------|------|----------|------|
| Frontend | Vue.js 3 + Vite | `frontend/` | 5173 |
| Backend (Orchestrator) | Ruby on Rails 8 (API only) | `backend/` | 3000 |
| AI Server | FastAPI (Python 3.12) | `ai-server/` | 8000 |
| Database | PostgreSQL | - | 5432 |
| LLM | **Ollama `gemma4:12b`** | 로컬 | 11434 |

### 호출 방향 (반드시 유지)

```
Vue ──▶ Rails ──▶ FastAPI ──▶ Ollama(gemma4:12b)
           │
           ▼
       PostgreSQL
```

- Vue는 **Rails만** 호출한다. FastAPI/Ollama를 직접 호출하지 않는다.
- Rails만 PostgreSQL에 접근한다.
- FastAPI만 Ollama를 호출한다.

### AI 모델 규칙

- 생성(요약/답변) 모델: `gemma4:12b` (환경변수 `OLLAMA_MODEL`)
- 다른 LLM 공급자(OpenAI, Claude 등)로 임의 교체하지 않는다.
- 검색은 기본 키워드(TF-IDF) 방식이며, `OLLAMA_EMBED_MODEL`을 지정하면 Ollama 임베딩 검색을 사용한다.

---

## 2. 커밋 메시지 형식 (필수·예외 없음)

- 형식: `type(scope): 요약`
- `type`, `scope`: **영어** (feat, fix, docs, refactor, chore, test, style, build)
- 요약 + 본문: **한국어**
- scope 예시: `ai-server`, `backend`, `frontend`, `repo`, `docs`, `agents`, `infra`, `branchs`

```
feat(ai-server): PDF 텍스트 추출 및 요약 엔드포인트 추가

pypdf로 PDF에서 텍스트를 추출하고,
Ollama gemma4:12b로 요약을 생성한 뒤 document_id를 반환한다.
```

금지 예시: `added pdf extract`, `feat: PDF 추출 기능 추가함`, `fix(backend): fixed upload bug`

---

## 3. 커밋 기록 문서화 (필수)

- 경로: `docs/branchs/`
- 파일명: `YYMMDD_HHMM_[커밋ID앞7자리]_[작성자]_[브랜치명].md`
  - 브랜치명의 `/` 는 `-` 로 바꾼다. (예: `feature/fastapi-init` → `feature-fastapi-init`)
- 템플릿: `docs/branchs/_template.md`
- 기록 파일은 **해당 커밋과 같은 브랜치**에 커밋한다.
  - 커밋 ID는 커밋 후에 확정되므로, 작업 커밋 → 기록 파일 커밋(`docs(branchs): ...`) 순서로 진행한다.

---

## 4. 브랜치 전략 (필수·예외 없음)

| 브랜치 | 용도 |
|--------|------|
| `main` | 병합 전용 (배포 기준) |
| `develop` | 병합 전용 (통합) |
| `feature/project-setup` | 저장소 공통 설정, 규칙, docs, 인프라 |
| `feature/fastapi-init` | `ai-server/` 작업 |
| `feature/rails-api` | `backend/` 작업 |
| `feature/vue-ui` | `frontend/` 작업 |

- 모든 작업은 `feature/*` 브랜치에서만 수행한다. 위 표 외의 브랜치를 임의로 만들지 않는다.
- 각 작업은 **해당 분야의 브랜치**에만 커밋한다. (예: frontend 코드를 rails 브랜치에 커밋 금지)
- `develop`, `main`에 직접 커밋하지 않는다.
- 병합은 반드시 `--no-ff`.
- 브랜치 하나가 끝날 때마다 병합하지 않는다. 요청 작업 전부를 커밋한 뒤 **사용자 명시적 지시**가 있을 때만 한 번에 총 병합한다.
- 병합 기록 문서도 총 병합 시점에 한 번에 작성한다.

---

## 5. 되돌리기 어려운 작업 (필수·예외 없음)

다음은 **사용자의 명시적 지시**가 있을 때만 수행한다.

- `git push`
- 브랜치 병합
- 파일/브랜치 삭제
- 기존 파일 덮어쓰기 (force)

한 번 승인한 것을 다른 상황에 임의로 확장 적용하지 않는다.

---

## 6. 코드 작성 규칙

- 줄바꿈은 `.gitattributes` 규칙(LF)을 따른다. 루트 `.gitattributes`를 삭제·우회하지 않는다.
- 비밀 값은 `.env`에만 두고 커밋하지 않는다. 새 변수는 `.env.example`에 추가한다.
- 주석/문서는 한국어, 식별자는 영어.
- AI 서버 응답 언어는 한국어를 기본으로 한다.

---

## 7. 문서 폴더 (`docs/`)

| 폴더 | 용도 |
|------|------|
| `docs/plan/` | 초기 기획·로직·DB·배포 계획 |
| `docs/Architecture/` | 시스템·계층·데이터 흐름 아키텍처 |
| `docs/branchs/` | 브랜치·커밋 기록 (템플릿 필수) |
| `docs/find_debug/` | 작업/실행 디버깅 일일 기록 |
| `docs/guidance/` | 기능·실행 가이드 |
| `docs/trainings/` | 학습·연구 정리 |
| `docs/repeater/` | 서버 연결·인프라 장애와 해결 |
| `docs/vaildates/` | 검증·체크리스트 |
| `docs/web_management/` | 배포 전/배포 시 웹 관리 기록 |
