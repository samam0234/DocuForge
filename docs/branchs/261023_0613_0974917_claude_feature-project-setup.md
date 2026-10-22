# 커밋 기록: chore(repo): gitattributes, gitignore, 환경변수 예시 추가

| 항목 | 내용 |
|------|------|
| 일시 | 2026-10-23 06:13 |
| 커밋 ID | `0974917` |
| 작성자 | claude |
| 브랜치 | `feature/project-setup` |
| 커밋 메시지 | `chore(repo): gitattributes, gitignore, 환경변수 예시 추가` |

## 1. 작업 목적

- Windows/리눅스 혼용 환경에서 줄바꿈을 LF로 고정하고, 비밀값 유출을 막는 기본 저장소 설정을 마련한다.

## 2. 변경 내용

저장소 전체 줄바꿈을 LF로 정규화하는 .gitattributes를 루트에 추가하고,
바이너리(docx, pdf, 이미지) 처리 규칙을 정의한다.
.gitignore와 Ollama gemma4:12b 설정을 포함한 .env.example을 추가한다.

## 3. 변경 파일

| 파일 | 구분 | 설명 |
|------|------|------|
| `.env.example` | 추가 | |
| `.gitattributes` | 추가 | |
| `.gitignore` | 추가 | |

## 4. 검증

- git ls-files --eol 로 모든 텍스트 파일이 i/lf 로 저장됨을 확인했다.

## 5. 비고 / 후속 작업

- 이후 모든 feature 브랜치는 이 브랜치에서 분기하여 .gitattributes를 공유한다.
