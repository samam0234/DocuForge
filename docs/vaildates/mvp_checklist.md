# MVP 검증 체크리스트

## 성공 기준 (기획서 11장)

- [ ] TXT/MD/PDF/DOCX/PPTX 업로드 후 요약이 화면에 표시된다 (API까지 확인, 브라우저 화면 미검증)
- [x] 해당 문서에 대해 질문에 답변이 나온다 (API 기준: Rails 경유 질문 201, 근거 포함)
- [x] Vue ↔ Rails ↔ FastAPI 흐름이 명확히 분리되어 있다 (Vue→Rails→FastAPI→Ollama, DB는 Rails만)
- [x] 각 서버 개별 실행으로 동작한다 (2026-10-23, Rails :3000 + FastAPI :8000)
- [ ] `docker compose up`으로 동작한다 (미검증: Docker 데몬 꺼짐)

## 세부 점검

### AI Server
- [x] `GET /health` 에서 `ollama: true`, `model: gemma4:12b`
- [x] `POST /summarize` TXT/PDF 정상, 미지원 확장자 → 415
- [x] `POST /summarize` MD/DOCX/PPTX 정상 (pytest + 실제 gemma4:12b 요약·질문 확인)
- [x] DOCX 표·제목, PPTX 발표자 노트·그룹 도형 텍스트 추출 (pytest)
- [x] 구형 `.doc`/`.ppt` → 415 + 변환 안내, 손상/암호 Office 문서 → 422, 압축 해제 크기 초과 → 422 (pytest)
- [x] 텍스트 없는 PDF(스캔본) → 422 (빈 텍스트 pytest로 확인, 실제 스캔 PDF는 미검증)
- [x] `POST /ask` 존재하지 않는 document_id → 404

### Backend
- [ ] `POST /api/documents` 크기 초과 → 413 (미검증), 미지원 포맷 → 415 (확인)
- [x] `POST /api/documents` md/markdown/docx/pptx/pdf 수락, 구형 `.doc`/`.ppt` → 415 + 변환 안내 (rails test)
- [x] AI 서버 다운 시 → 502 + 한국어 에러 메시지 (AiClient 단위 확인)
- [x] `GET /api/documents` 최근 문서 목록 (rails test)
- [x] 질문 히스토리 저장/조회

### Frontend
- [ ] 드래그 앤 드롭 / 파일 선택 업로드 + 진행률 표시 (선택 창은 5개 형식만 노출)
- [x] 업로드 전 형식 검증: 허용 5종 통과, 구형·미지원·10MB 초과 거절 (validate 함수 로직 확인, 화면은 미검증)
- [ ] 요약 카드 표시
- [ ] 채팅 질문/답변 + 근거 문장 표시
- [ ] 최근 문서 선택 후 재질문

## 검증 로그

| 일자 | 항목 | 결과 |
|------|------|------|
| 2026-10-23 | ai-server `pytest` | 4 passed |
| 2026-10-23 | backend `bin/rails test` | 5 runs, 0 failures |
| 2026-10-23 | frontend `npm run build` | 성공 |
| 2026-10-23 | Rails↔FastAPI↔gemma4:12b E2E (업로드→질문→히스토리) | 성공 |
| 2026-10-23 | ai-server `pytest` (MD/DOCX/PPTX 지원 추가 후) | 17 passed |
| 2026-10-23 | backend `bin/rails test` (허용 형식 확장 후) | 7 runs, 26 assertions, 0 failures |
| 2026-10-23 | 실제 gemma4:12b로 DOCX/PPTX/MD 요약·질문 | 성공 (각 4~5초) |
| 미실시 | 브라우저 UI E2E, `docker compose up`, 실제 스캔 PDF, 413 응답 | - |
