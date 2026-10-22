# DocuForge 기획서 v1.0

**AI 기반 문서 요약 및 질의응답 플랫폼**

| 항목 | 내용 |
|------|------|
| 프로젝트명 | DocuForge |
| 버전 | 1.0 |
| 작성일 | 2026-10-23 |
| 기술 스택 | Vue.js + Ruby on Rails + FastAPI |
| 유형 | 미니 프로젝트 (Vibe Coding 대상) |

---

## 1. 프로젝트 개요

**DocuForge**는 사용자가 업로드한 문서(PDF, TXT 등)를 AI가 자동으로 요약하고, 문서 내용에 기반하여 자연어 질의응답을 제공하는 플랫폼입니다.

핵심 가치는 **“긴 문서를 읽지 않고도 핵심을 파악하고, 원하는 정보를 바로 질문으로 얻을 수 있는 경험”**입니다.

### 선정 배경
- 이전 미니 프로젝트(AI 일기 감정 분석기) 이후 제비뽑기로 선정
- RAG(Retrieval-Augmented Generation) 패턴을 단순하고 명확하게 학습할 수 있는 주제
- Vue + Rails + FastAPI 3계층 아키텍처 연습에 적합

---

## 2. 목표 및 범위

### 목표
1. 문서 업로드 → 요약 생성 → 질의응답까지 End-to-End 흐름 구현
2. FastAPI(AI) / Rails(Orchestrator) / Vue(UI) 역할 분리 실습
3. Vibe Coding 방식으로 빠르게 동작하는 MVP 완성

### 범위 (MVP)
- 지원 파일: TXT, PDF (텍스트 추출 가능)
- 단일 문서 단위 요약 및 Q&A
- 기본 채팅형 UI
- 문서별 세션 유지 (간단한 ID 기반)

### 제외 범위 (향후 확장)
- 다중 문서 동시 검색
- 사용자 인증 / 권한 관리
- 실시간 스트리밍 응답
- 고급 벡터 DB (pgvector, Pinecone 등)

---

## 3. 기술 스택

| 레이어 | 기술 | 역할 |
|--------|------|------|
| Frontend | Vue.js 3 + Vite | UI, 파일 업로드, 요약 표시, 채팅 인터페이스 |
| Backend (Orchestrator) | Ruby on Rails (API only) | 파일 업로드 처리, 메타데이터 저장, AI 서버 프록시, 세션 관리 |
| AI Server | FastAPI | 텍스트 추출, 요약, 임베딩 생성, 유사도 검색, LLM 호출 |
| Database | PostgreSQL | 문서 메타데이터, 요약, 질문 기록 저장 |
| 기타 | Docker (선택) | 로컬 오케스트레이션 |

---

## 4. 시스템 아키텍처 및 오케스트레이션

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
| **Rails** | 인증 없는 간단한 API 게이트웨이, 파일 저장/메타데이터 관리, FastAPI 호출 오케스트레이션, 에러 처리 |
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
│   │   ├── api/
│   │   │   └── document.js
│   │   └── App.vue
│   ├── package.json
│   └── vite.config.js
│
├── backend/                      # Ruby on Rails API
│   ├── app/
│   │   ├── controllers/
│   │   │   ├── documents_controller.rb
│   │   │   └── questions_controller.rb
│   │   ├── models/
│   │   │   └── document.rb
│   │   └── services/
│   │       └── ai_client.rb
│   ├── config/
│   │   └── routes.rb
│   └── Gemfile
│
├── ai-server/                    # FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── summarize.py
│   │   │   └── ask.py
│   │   ├── services/
│   │   │   ├── document_parser.py
│   │   │   ├── summarizer.py
│   │   │   └── rag_engine.py
│   │   └── models/
│   │       └── schemas.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml            # (선택) 로컬 오케스트레이션
├── README.md
└── .env.example
```

---

## 6. 핵심 기능

### 6.1 문서 업로드 및 요약
- 드래그 앤 드롭 / 파일 선택
- 업로드 진행률 표시
- 요약 결과 카드 형태로 표시

### 6.2 질의응답
- 문서별 채팅 인터페이스
- 질문 입력 → 답변 + (가능하면) 근거 문장 표시
- 이전 질문 히스토리 표시

### 6.3 문서 관리 (간단)
- 최근 업로드한 문서 목록
- 문서 선택 후 다시 질문하기

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

## 9. 개발 단계 (Vibe Coding 기준)

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

## 10. 고려사항 및 확장 포인트

- **LLM 선택**: OpenAI / Claude / 로컬(Ollama) 중 편한 것으로 시작
- **임베딩**: 처음엔 단순 키워드 또는 작은 FAISS in-memory로 시작
- **에러 처리**: 파일 크기 제한, 지원하지 않는 포맷 안내
- **보안**: 업로드 파일은 임시 저장 후 일정 시간 후 삭제
- **확장**: 다중 문서, 인용 출처 표시, 스트리밍 응답, 사용자 계정

---

## 11. 성공 기준 (MVP)

- [ ] TXT/PDF 업로드 후 요약이 화면에 표시된다
- [ ] 해당 문서에 대해 질문에 답변이 나온다
- [ ] Vue ↔ Rails ↔ FastAPI 흐름이 명확히 분리되어 있다
- [ ] 로컬에서 `docker-compose up` 또는 각 서버 개별 실행으로 동작한다

---

**DocuForge v1.0**  
작성일: 2026-10-23  
다음 액션: FastAPI 서버 스캐폴딩부터 시작
