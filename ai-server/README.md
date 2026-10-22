# DocuForge AI Server

FastAPI + Ollama **`gemma4:12b`** 기반 텍스트 추출 · 요약 · RAG 질의응답 서버. Rails(Orchestrator)만 이 서버를 호출한다.

## 사전 준비

- Python 3.12
- Ollama 실행 중 (`ollama serve`) 및 모델 설치

```bash
ollama pull gemma4:12b
ollama pull bge-m3        # 선택: 임베딩 검색을 쓸 때만
```

## 실행

```bash
cd ai-server
py -3.12 -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

확인: `GET http://localhost:8000/health` → `{"status":"ok","model":"gemma4:12b","embed_model":null,"ollama":true}`
(`ollama`가 `false`이면 Ollama 미실행 또는 모델 미설치)

## 환경 변수

`ai-server/.env` 파일 또는 시스템 환경 변수로 지정한다. 루트 `.env.example` 참고.

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama 주소 |
| `OLLAMA_MODEL` | `gemma4:12b` | 요약/답변 생성 모델 |
| `OLLAMA_EMBED_MODEL` | (빈 값) | 지정 시 임베딩 검색 (예: `bge-m3`), 비우면 TF-IDF |
| `OLLAMA_NUM_CTX` | `8192` | 컨텍스트 길이 |
| `OLLAMA_TIMEOUT` | `300` | Ollama 호출 타임아웃(초) |
| `AI_DATA_DIR` | `./data` | 청크 인덱스 저장 위치 |
| `MAX_UPLOAD_MB` | `10` | 업로드 최대 크기 |

## 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| GET | `/health` | 상태, 모델명, Ollama 연결 여부 |
| POST | `/summarize` | multipart `file`(TXT/PDF) → `{document_id, summary, text, char_count, chunk_count, model}` |
| POST | `/ask` | `{document_id, question}` → `{answer, sources[], model}` |

```bash
curl -F "file=@sample.txt" http://localhost:8000/summarize
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" \
     -d '{"document_id":"<위에서 받은 ID>","question":"핵심이 뭐야?"}'
```

### 에러 코드

| 코드 | 상황 |
|------|------|
| 404 | `/ask`에 존재하지 않는 `document_id` |
| 413 | 파일 크기 초과 |
| 415 | TXT/PDF가 아닌 형식 |
| 422 | 추출할 텍스트가 없음 (스캔 PDF, 빈 파일, 손상된 PDF) |
| 503 | Ollama 호출 실패 (미실행, 모델 없음, 타임아웃) |

## 처리 흐름

```
/summarize: 파일 → 텍스트 추출 → 청크 분할(1000자, 겹침 150) → [임베딩] → 인덱스 저장
                                 └→ 요약 (gemma4:12b)
/ask:       질문 → 인덱스 검색(top 4) → 발췌 + 질문 → gemma4:12b → 답변 + 근거 청크
```

- 요약: 6,000자 이하는 한 번에, 초과하면 섹션별 부분 요약 후 통합 요약(map-reduce).
- 검색: 기본 TF-IDF(한글은 음절 bigram 보완), `OLLAMA_EMBED_MODEL` 지정 시 코사인 유사도.
- 답변은 제공된 발췌만 근거로 하며, 없으면 "문서에서 해당 내용을 찾을 수 없습니다."로 답한다.
- 인덱스는 `data/{document_id}.json`에 저장되어 재시작 후에도 유지된다. (자동 삭제는 아직 없음)

## 구조

```
app/
├── main.py                 # 앱 + /health
├── config.py               # 환경 변수 설정
├── routers/                # summarize.py, ask.py
├── services/
│   ├── ollama_client.py    # /api/chat(think=false), /api/embed 호출
│   ├── document_parser.py  # TXT/PDF 추출, 청크 분할
│   ├── summarizer.py       # map-reduce 요약
│   └── rag_engine.py       # 인덱스 저장, 검색, 답변 생성
└── models/schemas.py
tests/test_api.py           # Ollama mock 기반
```

## 테스트

```bash
pytest -q      # Ollama 호출은 mock 처리되어 모델 없이 실행 가능
```

## Docker

```bash
docker build -t docuforge-ai ai-server
```

컨테이너에서는 `OLLAMA_BASE_URL=http://host.docker.internal:11434`로 호스트의 Ollama에 접속한다.
