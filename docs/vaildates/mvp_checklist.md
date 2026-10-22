# MVP 검증 체크리스트

## 성공 기준 (기획서 11장)

- [ ] TXT/PDF 업로드 후 요약이 화면에 표시된다
- [ ] 해당 문서에 대해 질문에 답변이 나온다
- [ ] Vue ↔ Rails ↔ FastAPI 흐름이 명확히 분리되어 있다
- [ ] 로컬에서 `docker compose up` 또는 각 서버 개별 실행으로 동작한다

## 세부 점검

### AI Server
- [ ] `GET /health` 에서 `ollama: true`, `model: gemma4:12b`
- [ ] `POST /summarize` TXT/PDF 정상, 미지원 확장자 → 415
- [ ] 텍스트 없는 PDF(스캔본) → 422
- [ ] `POST /ask` 존재하지 않는 document_id → 404

### Backend
- [ ] `POST /api/documents` 크기 초과 → 413, 미지원 포맷 → 415
- [ ] AI 서버 다운 시 → 502 + 한국어 에러 메시지
- [ ] `GET /api/documents` 최근 문서 목록
- [ ] 질문 히스토리 저장/조회

### Frontend
- [ ] 드래그 앤 드롭 / 파일 선택 업로드 + 진행률 표시
- [ ] 요약 카드 표시
- [ ] 채팅 질문/답변 + 근거 문장 표시
- [ ] 최근 문서 선택 후 재질문
