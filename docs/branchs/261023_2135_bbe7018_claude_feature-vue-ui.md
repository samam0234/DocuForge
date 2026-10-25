# 커밋 기록: feat(frontend): MD, DOCX, PPTX 업로드 지원 및 형식 안내

| 항목 | 내용 |
|------|------|
| 일시 | 2026-10-23 21:35 |
| 커밋 ID | `bbe7018` |
| 작성자 | claude |
| 브랜치 | `feature/vue-ui` |
| 커밋 메시지 | `feat(frontend): MD, DOCX, PPTX 업로드 지원 및 형식 안내` |

## 1. 작업 목적

- 서버가 지원하는 형식을 화면에서 막지 않고, 사용자가 올릴 수 있는 형식을 업로드 영역에서 알 수 있게 한다.

## 2. 변경 내용

허용 확장자를 .md, .markdown, .docx, .pptx까지 확장하고
파일 선택 창(accept)과 드래그 앤 드롭 검증에 같은 목록을 사용한다.
업로드 영역에 지원 형식을 표시하며, 구형 .doc/.ppt는 변환 안내를 보여준다.

## 3. 변경 파일

| 파일 | 구분 | 설명 |
|------|------|------|
| `frontend/src/components/DocumentUpload.vue` | 수정 | |

## 4. 검증

- npm run build 성공. validate 함수를 Node로 분리 실행해 md/markdown/docx/pptx/pdf/txt 허용, doc/ppt 변환 안내, png·확장자 없음 거절, 10MB 초과 거절을 확인.

## 5. 비고 / 후속 작업

- 브라우저에서 실제 파일 선택/드롭은 미검증. 프론트엔드 단위 테스트 환경이 없다.
