# DocuForge Frontend (Vue 3 + Vite)

업로드(TXT, MD, PDF, DOCX, PPTX), 요약 카드, 문서별 채팅 UI. **Rails API(:3000)만 호출**한다.

## 실행

```bash
npm install
npm run dev        # http://localhost:5173
npm run build
```

API 주소는 `VITE_API_BASE_URL` (기본 `http://localhost:3000`)로 바꿀 수 있다.

## 구조

```
src/
├── api/document.js              # Rails API 호출 (axios)
├── components/
│   ├── DocumentUpload.vue       # 드래그 앤 드롭, 진행률, 요약 대기 표시
│   ├── SummaryCard.vue          # 요약(제목/불릿) 렌더링
│   ├── ChatInterface.vue        # 질문/답변, 근거 문장, 히스토리
│   └── RecentDocuments.vue      # 최근 문서 목록 / 재선택
├── views/HomeView.vue
├── App.vue
└── style.css                    # 라이트/다크 모드 토큰
```

## 지원 파일 형식

`.txt`, `.md`(`.markdown`), `.pdf`, `.docx`, `.pptx` — `DocumentUpload.vue`의 `ALLOWED`

- 파일 선택 창(`accept`)과 드래그 앤 드롭 모두 같은 목록으로 검증한다.
- 구형 `.doc`, `.ppt`는 `.docx`/`.pptx`로 저장하라는 안내를 표시한다.
- 형식을 추가할 때는 Rails(`Document::ALLOWED_EXTENSIONS`), FastAPI(`document_parser.py`)도 함께 바꾼다.
