# DocuForge 인수인계 문서

**AI 기반 문서 요약 및 질의응답 플랫폼**  
버전: 1.0  
작성일: 2026-10-23  
기술 스택: Vue.js 3 + Vite / Ruby on Rails / FastAPI / PostgreSQL

---

## 1. 프로젝트 개요

DocuForge는 사용자가 업로드한 문서(PDF, TXT 등)를 AI가 자동으로 요약하고, 문서 내용에 기반하여 자연어 질의응답을 제공하는 플랫폼입니다.

**핵심 가치**: 긴 문서를 읽지 않고도 핵심을 파악하고, 원하는 정보를 바로 질문으로 얻을 수 있는 경험

### 선정 배경
- RAG 패턴을 단순하고 명확하게 학습할 수 있는 주제
- Vue + Rails + FastAPI 3계층 아키텍처 연습에 적합
- Vibe Coding 방식으로 빠르게 MVP 완성 가능

---

## 2. 목표 및 범위

### 목표
1. 문서 업로드 → 요약 생성 → 질의응답까지 End-to-End 흐름 구현
2. FastAPI(AI) / Rails(Orchestrator) / Vue(UI) 역할 분리 실습
3. Vibe Coding 방식으로 빠르게 동작하는 MVP 완성

### MVP 범위
- 지원 파일: TXT, PDF
- 단일 문서 단위 요약 및 Q&A
- 기본 채팅형 UI + 문서별 세션 유지

### 제외 범위 (향후 확장)
- 다중 문서 동시 검색
- 사용자 인증 / 권한 관리
- 실시간 스트리밍 응답
- 고급 벡터 DB (pgvector, Pinecone 등)

---

## 3. 기술 스택

| 레이어 | 기술 | 역할 | 디렉터리 | 기본 포트 |
|--------|------|------|----------|-----------|
| Frontend | Vue.js 3 + Vite | UI, 파일 업로드, 요약 표시, 채팅 | `frontend/` | 5173 |
| Backend (Orchestrator) | Ruby on Rails (API) | 파일 처리, 메타데이터, AI 프록시 | `backend/` | 3000 |
| AI Server | FastAPI | 텍스트 추출, 요약, 임베딩, RAG, LLM | `ai-server/` | 8000 |
| Database | PostgreSQL | 문서 메타데이터, 요약, 질문 기록 | - | 5432 |

---

## 4. 시스템 아키텍처

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Vue.js    │────▶│  Ruby on Rails   │────▶│    FastAPI      │
│  (Frontend) │◀────│  (Orchestrator)  │◀────│   (AI Server)   │
└─────────────┘     └──────────────────┘     └─────────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │ PostgreSQL  │
                     └─────────────┘
```

### 역할 분담

| 컴포넌트 | 책임 |
|----------|------|
| **Vue.js** | 사용자 인터랙션, 파일 업로드 UI, 요약/답변 렌더링 |
| **Rails** | API 게이트웨이, 파일 저장/메타데이터 관리, FastAPI 호출 오케스트레이션, 에러 처리 |
| **FastAPI** | 문서 파싱, LLM 기반 요약, 청크 분할 + 임베딩, RAG 기반 답변 생성 |
| **PostgreSQL** | `documents`, `summaries`, `qa_histories` 테이블 |

### 오케스트레이션 흐름
1. 사용자가 Vue에서 파일 업로드
2. Rails가 파일을 받아 임시 저장 후 FastAPI `/summarize` 호출
3. FastAPI가 텍스트 추출 → 요약 생성 → 임베딩 생성 후 Rails에 결과 반환
4. Rails가 메타데이터 + 요약 DB 저장 후 Vue에 응답
5. 사용자가 질문 시 Rails가 FastAPI `/ask` 프록시
6. FastAPI가 관련 청크 검색 후 LLM으로 답변 생성

---

## 5. 폴더 구조

```
docuforge/
├── frontend/                     # Vue.js 3 + Vite
│   ├── src/
│   │   ├── components/
│   │   │   ├── DocumentUpload.vue
│   │   │   ├── SummaryCard.vue
│   │   │   └── ChatInterface.vue
│   │   ├── views/
│   │   │   └── HomeView.vue
│   │   └── api/
│   │       └── document.js
│   └── package.json
│
├── backend/                      # Ruby on Rails API
│   ├── app/
│   │   ├── controllers/
│   │   ├── models/
│   │   └── services/
│   │       └── ai_client.rb
│   └── Gemfile
│
├── ai-server/                    # FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── services/
│   │   └── models/
│   └── requirements.txt
│
├── docs/                         # 문서 저장소 (아래 참조)
├── docker-compose.yml
├── README.md
├── AGENTS.md                     # SSOT (단일 진실 공급원)
└── .env.example
```

### Docs 폴더 구조 (필수)

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

---

## 6. 핵심 기능

- 문서 업로드 및 AI 요약 (드래그 앤 드롭, 진행률 표시)
- 문서 기반 질의응답 (채팅 UI, 근거 문장 표시 가능)
- 최근 문서 목록 및 재질문

---

## 7. API 설계 (초안)

### Rails → Frontend

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/documents` | 파일 업로드 + 요약 요청 |
| GET | `/api/documents/:id` | 문서 + 요약 조회 |
| POST | `/api/documents/:id/questions` | 질문 전송 |
| GET | `/api/documents/:id/questions` | 질문 히스토리 |

### Rails → FastAPI

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/summarize` | 파일 또는 텍스트 전달 → 요약 + document_id |
| POST | `/ask` | `{ document_id, question }` → 답변 |

---

## 8. 데이터 모델 (간단)

### documents
- id, filename, original_text (또는 경로), summary, created_at

### qa_histories
- id, document_id, question, answer, created_at

---

## 9. 코딩 수칙 (필수·예외 없음)

### 9.1 커밋 메시지 형식

- **형식**: `type(scope): 요약`
- **type / scope**: 영어 (feat, fix, docs, refactor, chore, test 등)
- **요약 + 본문**: 한국어

**올바른 예시**
```
feat(ai-server): PDF 텍스트 추출 및 요약 엔드포인트 추가

PyMuPDF를 사용해 PDF에서 텍스트를 추출하고,
OpenAI API로 요약 생성 후 document_id를 반환한다.
```

**잘못된 예시 (금지)**
```
❌ added pdf extract
❌ feat: PDF 추출 기능 추가함
❌ fix(backend): fixed upload bug
```

### 9.2 커밋 기록 문서화 (필수)

- 경로: `docs/branchs/`
- 파일명: `YYMMDD_HHMM_[커밋ID앞7자리]_[작성자]_[브랜치명].md`
- 템플릿 파일(`docs/branchs/_template.md`) 사용
- 기록 파일도 **같은 브랜치**에 함께 커밋

### 9.3 브랜치 전략 (필수·예외 없음)

- 모든 작업은 **`feature/*` 브랜치**에서만 수행
- `develop`, `main` 브랜치는 **병합 전용**
- 병합은 반드시 `--no-ff` 옵션 사용
- **브랜치 하나가 끝날 때마다 병합하지 않는다**
- 요청받은 작업을 전부 커밋한 뒤, **사용자 명시적 지시**가 있을 때만 한 번에 총 병합
- 병합 기록 문서도 총 병합 시점에 한 번에 작성

### 9.4 되돌리기 어려운 작업 (필수·예외 없음)

다음 작업은 **사용자의 명시적 지시**가 있을 때만 수행:

- `git push`
- 브랜치 병합
- 파일/브랜치 삭제
- 기존 파일 덮어쓰기 (force)

한 번 승인한 것을 다른 상황에 임의로 확장 적용하지 않는다.

### 9.5 규칙의 단일 출처 (SSOT)

- 루트 `AGENTS.md`에 공유 규칙을 둔다
- `.Claude/CLAUDE.md`, `.Cursor/CURSOR.md`, `.Grok/GROK.md` 등 에이전트별 파일은 **AGENTS.md를 가리키기만** 한다
- 규칙이 여러 곳에 중복되어 어긋나는 것을 방지

---

## 10. 에이전트 인수인계 대상

다음 에이전트용 폴더/파일을 생성하여 공통 규칙을 참조하도록 한다:

- `.Agents/` (모든 에이전트 공통)
- `.Claude/`
- `.Codex/`
- `.Cursor/`
- `.Grok/`
- `.Gemini/`
- `.Antigravity/`
- `.Manus/`

각 에이전트 파일은 아래와 같은 형태로 작성:

```markdown
# [에이전트명] 규칙 (DocuForge)

> **단일 진실 공급원**: 루트 AGENTS.md를 반드시 따르세요.
> 이 파일은 [에이전트명] 전용 추가 지시만 담습니다.
```

---

## 11. 개발 단계 (Vibe Coding 기준)

| 단계 | 내용 | 예상 |
|------|------|------|
| 1 | FastAPI 기본 엔드포인트 (요약 + 더미 답변) | 30분 |
| 2 | Rails 프록시 + 파일 업로드 | 40분 |
| 3 | Vue 업로드 + 요약 표시 UI | 30분 |
| 4 | 실제 LLM 연동 + 간단한 RAG | 1시간 |
| 5 | 채팅 UI + 히스토리 | 40분 |
| 6 | 폴더 정리 + README | 20분 |

**총 예상: 3~4시간 내 MVP**

---

## 12. 성공 기준 (MVP)

- [ ] TXT/PDF 업로드 후 요약이 화면에 표시된다
- [ ] 해당 문서에 대해 질문에 답변이 나온다
- [ ] Vue ↔ Rails ↔ FastAPI 흐름이 명확히 분리되어 있다
- [ ] 로컬에서 `docker-compose up` 또는 각 서버 개별 실행으로 동작한다

---

## 13. 고려사항 및 확장 포인트

- **LLM 선택**: OpenAI / Claude / 로컬(Ollama) 중 편한 것으로 시작
- **임베딩**: 처음엔 단순 키워드 또는 작은 FAISS in-memory로 시작
- **에러 처리**: 파일 크기 제한, 지원하지 않는 포맷 안내
- **보안**: 업로드 파일은 임시 저장 후 일정 시간 후 삭제
- **확장**: 다중 문서, 인용 출처 표시, 스트리밍 응답, 사용자 계정

---

## 14. 다음 액션

1. FastAPI 서버 스캐폴딩 (`feature/fastapi-init`)
2. 기본 `/summarize` 엔드포인트 구현
3. Rails 프록시 연동

---

**DocuForge 인수인계 v1.0**  
작성일: 2026-10-23  
단일 진실 공급원: `AGENTS.md`  
다음 업데이트: 개발 진행에 따라 `docs/` 하위 문서 갱신
