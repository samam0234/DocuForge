# 커밋 기록: feat(backend): MD, DOCX, PPTX 업로드 허용 및 안내 메시지 개선

| 항목 | 내용 |
|------|------|
| 일시 | 2026-10-23 21:34 |
| 커밋 ID | `e09e1b8` |
| 작성자 | claude |
| 브랜치 | `feature/rails-api` |
| 커밋 메시지 | `feat(backend): MD, DOCX, PPTX 업로드 허용 및 안내 메시지 개선` |

## 1. 작업 목적

- FastAPI가 지원하는 새 형식을 Rails 입구에서 막지 않도록 허용 목록을 맞추고, 미지원 사유를 사용자에게 안내한다.

## 2. 변경 내용

허용 확장자에 .md, .markdown, .docx, .pptx를 추가하고
415 응답에 지원 형식 목록을 포함한다. 구형 .doc/.ppt는 변환 안내를 반환한다.
통합 테스트에 새 형식 수락과 구형 형식 거절을 추가하고,
테스트용 가짜 AI 클라이언트가 매번 고유한 document_id를 반환하도록 수정한다.

## 3. 변경 파일

| 파일 | 구분 | 설명 |
|------|------|------|
| `backend/app/controllers/documents_controller.rb` | 수정 | |
| `backend/app/models/document.rb` | 수정 | |
| `backend/test/integration/documents_flow_test.rb` | 수정 | |

## 4. 검증

- bin/rails test 7 runs, 26 assertions, 0 failures (신규: 형식 수락, 구형 형식 415, 지원 형식 안내).

## 5. 비고 / 후속 작업

- 허용 확장자가 FastAPI/Vue와 3곳에 중복되어 있다. 변경 시 함께 수정 필요(README에 명시).
