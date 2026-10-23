# 커밋 기록: feat(ai-server): MD, DOCX, PPTX 문서 형식 지원 추가

| 항목 | 내용 |
|------|------|
| 일시 | 2026-10-23 21:34 |
| 커밋 ID | `3e15837` |
| 작성자 | claude |
| 브랜치 | `feature/fastapi-init` |
| 커밋 메시지 | `feat(ai-server): MD, DOCX, PPTX 문서 형식 지원 추가` |

## 1. 작업 목적

- TXT/PDF만 받던 업로드를 일반적인 문서 형식(MD, DOCX, PPTX)까지 넓힌다.

## 2. 변경 내용

기존 TXT/PDF에 더해 마크다운(.md, .markdown), Word(.docx), PowerPoint(.pptx)에서
텍스트를 추출한다. DOCX는 본문 순서대로 문단/표/제목을, PPTX는 슬라이드별
텍스트/표/그룹 도형/발표자 노트를 추출한다.
구형 .doc/.ppt는 변환 안내와 함께 415로, 손상/암호 문서와 압축 해제 크기
100MB 초과(zip bomb)는 422로 거절한다.

## 3. 변경 파일

| 파일 | 구분 | 설명 |
|------|------|------|
| `ai-server/app/services/document_parser.py` | 수정 | |
| `ai-server/app/services/office_parser.py` | 추가 | |
| `ai-server/requirements.txt` | 수정 | |

## 4. 검증

- pytest 17 passed. 실제 Ollama gemma4:12b로 DOCX(표 내용), PPTX(발표자 노트), MD 요약 및 질의응답 성공(각 4~5초).

## 5. 비고 / 후속 작업

- python-docx 1.2.0, python-pptx 1.0.2 추가. .hwp/.xlsx 등은 미지원. 허용 확장자는 Rails/Vue에도 있어 해당 브랜치에서 함께 변경 필요.
