# MVP 검증 체크리스트

## 성공 기준 (기획서 11장)

- [ ] TXT/PDF 업로드 후 요약이 화면에 표시된다 (API까지 확인, 브라우저 화면 미검증)
- [x] 해당 문서에 대해 질문에 답변이 나온다 (API 기준: Rails 경유 질문 201, 근거 포함)
- [x] Vue ↔ Rails ↔ FastAPI 흐름이 명확히 분리되어 있다 (Vue→Rails→FastAPI→Ollama, DB는 Rails만)
- [x] 각 서버 개별 실행으로 동작한다 (2026-10-23, Rails :3000 + FastAPI :8000)
- [ ] `docker compose up`으로 동작한다 (미검증: Docker 데몬 꺼짐)

## 세부 점검

### AI Server
- [x] `GET /health` 에서 `ollama: true`, `model: gemma4:12b`
- [x] `POST /summarize` TXT/PDF 정상, 미지원 확장자 → 415
- [x] 텍스트 없는 PDF(스캔본) → 422 (빈 텍스트 pytest로 확인, 실제 스캔 PDF는 미검증)
- [x] `POST /ask` 존재하지 않는 document_id → 404

### Backend
- [ ] `POST /api/documents` 크기 초과 → 413 (미검증), 미지원 포맷 → 415 (확인)
- [x] AI 서버 다운 시 → 502 + 한국어 에러 메시지 (AiClient 단위 확인)
- [x] `GET /api/documents` 최근 문서 목록 (rails test)
- [x] 질문 히스토리 저장/조회

### Frontend
- [ ] 드래그 앤 드롭 / 파일 선택 업로드 + 진행률 표시
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
| 미실시 | 브라우저 UI E2E, `docker compose up`, 실제 스캔 PDF, 413 응답 | - |
