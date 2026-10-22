# 커밋 기록: test(ai-server): Ollama mock 기반 API 테스트 추가

| 항목 | 내용 |
|------|------|
| 일시 | 2026-10-23 06:18 |
| 커밋 ID | `31032a6` |
| 작성자 | claude |
| 브랜치 | `feature/fastapi-init` |
| 커밋 메시지 | `test(ai-server): Ollama mock 기반 API 테스트 추가` |

## 1. 작업 목적

- LLM 없이도 API 계약과 에러 처리를 빠르게 검증한다.

## 2. 변경 내용

요약/질문 정상 흐름과 415, 422, 404 에러 응답을 검증한다.

## 3. 변경 파일

| 파일 | 구분 | 설명 |
|------|------|------|
| `ai-server/pytest.ini` | 추가 | |
| `ai-server/tests/test_api.py` | 추가 | |

## 4. 검증

- pytest -q → 4 passed.

## 5. 비고 / 후속 작업

- 없음
