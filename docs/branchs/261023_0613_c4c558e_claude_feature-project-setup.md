# 커밋 기록: docs(agents): AGENTS.md 단일 규칙 문서 및 에이전트별 참조 파일 추가

| 항목 | 내용 |
|------|------|
| 일시 | 2026-10-23 06:13 |
| 커밋 ID | `c4c558e` |
| 작성자 | claude |
| 브랜치 | `feature/project-setup` |
| 커밋 메시지 | `docs(agents): AGENTS.md 단일 규칙 문서 및 에이전트별 참조 파일 추가` |

## 1. 작업 목적

- 규칙을 AGENTS.md 한 곳에서 관리하고 에이전트별 파일은 참조만 하도록 하여 규칙 중복/불일치를 막는다.

## 2. 변경 내용

커밋 형식, 브랜치 전략, 되돌리기 어려운 작업 규칙을 루트 AGENTS.md에 정의한다.
각 에이전트 폴더 파일은 AGENTS.md만 가리키도록 작성한다.

## 3. 변경 파일

| 파일 | 구분 | 설명 |
|------|------|------|
| `.Agents/AGENTS.md` | 추가 | |
| `.Antigravity/ANTIGRAVITY.md` | 추가 | |
| `.Claude/CLAUDE.md` | 추가 | |
| `.Codex/CODEX.md` | 추가 | |
| `.Cursor/CURSOR.md` | 추가 | |
| `.Gemini/GEMINI.md` | 추가 | |
| `.Grok/GROK.md` | 추가 | |
| `.Manus/MANUS.md` | 추가 | |
| `AGENTS.md` | 추가 | |

## 4. 검증

- 8개 에이전트 폴더(.Agents, .Claude, .Codex, .Cursor, .Grok, .Gemini, .Antigravity, .Manus) 생성 확인.

## 5. 비고 / 후속 작업

- 없음
