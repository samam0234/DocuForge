# 커밋 기록: feat(frontend): 문서 업로드, 요약 카드, 채팅 UI 구현

| 항목 | 내용 |
|------|------|
| 일시 | 2026-10-23 06:24 |
| 커밋 ID | `a9b39f1` |
| 작성자 | claude |
| 브랜치 | `feature/vue-ui` |
| 커밋 메시지 | `feat(frontend): 문서 업로드, 요약 카드, 채팅 UI 구현` |

## 1. 작업 목적

- 업로드 → 요약 표시 → 질의응답 → 최근 문서 재선택의 사용자 흐름을 구현한다.

## 2. 변경 내용

Rails API 클라이언트(api/document.js)와 드래그 앤 드롭 업로드(진행률/요약 대기),
요약 카드, 근거 문장을 포함한 채팅, 최근 문서 목록 컴포넌트를 구현한다.
라이트/다크 모드를 지원하는 공통 스타일을 추가한다.

## 3. 변경 파일

| 파일 | 구분 | 설명 |
|------|------|------|
| `frontend/src/App.vue` | 추가 | |
| `frontend/src/api/document.js` | 추가 | |
| `frontend/src/components/ChatInterface.vue` | 추가 | |
| `frontend/src/components/DocumentUpload.vue` | 추가 | |
| `frontend/src/components/RecentDocuments.vue` | 추가 | |
| `frontend/src/components/SummaryCard.vue` | 추가 | |
| `frontend/src/main.js` | 추가 | |
| `frontend/src/style.css` | 추가 | |
| `frontend/src/views/HomeView.vue` | 추가 | |

## 4. 검증

- npm run build 성공 (73 modules, JS 123KB/gzip 47KB).

## 5. 비고 / 후속 작업

- Rails가 PostgreSQL 없이 기동되지 않아 브라우저 E2E 흐름은 미검증. 요약은 v-html 없이 블록 단위로 렌더링해 XSS를 피했다.
