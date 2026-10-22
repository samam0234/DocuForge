# DocuForge AI Server

FastAPI + Ollama **`gemma4:12b`** 기반 텍스트 추출 · 요약 · RAG 질의응답 서버.

## 실행

```bash
ollama pull gemma4:12b
py -3.12 -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

환경 변수는 루트 `.env.example`의 AI Server 항목을 `ai-server/.env`로 복사해 조정한다.

## 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| GET | `/health` | 상태, 모델명, Ollama 연결 여부 |
| POST | `/summarize` | multipart `file`(TXT/PDF) → `{document_id, summary, text, chunk_count}` |
| POST | `/ask` | `{document_id, question}` → `{answer, sources[]}` |

에러: 413(크기 초과), 415(미지원 형식), 422(텍스트 없음), 404(인덱스 없음), 503(Ollama 실패)

## 구조

```
app/
├── main.py                 # 앱 + /health
├── config.py               # 환경 변수 설정
├── routers/                # summarize.py, ask.py
├── services/
│   ├── ollama_client.py    # /api/chat, /api/embed 호출
│   ├── document_parser.py  # TXT/PDF 추출, 청크 분할
│   ├── summarizer.py       # map-reduce 요약
│   └── rag_engine.py       # 인덱스 저장, TF-IDF/임베딩 검색, 답변 생성
└── models/schemas.py
```

- 긴 문서(6,000자 초과)는 섹션별 부분 요약 후 통합 요약한다.
- 검색: 기본 TF-IDF(한글 음절 bigram), `OLLAMA_EMBED_MODEL=bge-m3` 지정 시 임베딩 검색.
- 인덱스는 `data/{document_id}.json`에 저장되어 재시작 후에도 유지된다.

## 테스트

```bash
pytest -q      # Ollama 호출은 mock 처리
```
