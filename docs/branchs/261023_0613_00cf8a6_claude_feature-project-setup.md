# 커밋 기록: chore(infra): README와 docker-compose 구성 추가

| 항목 | 내용 |
|------|------|
| 일시 | 2026-10-23 06:13 |
| 커밋 ID | `00cf8a6` |
| 작성자 | claude |
| 브랜치 | `feature/project-setup` |
| 커밋 메시지 | `chore(infra): README와 docker-compose 구성 추가` |

## 1. 작업 목적

- 프로젝트 소개와 docker-compose 기반 로컬 오케스트레이션을 제공한다.

## 2. 변경 내용

PostgreSQL, ai-server, backend, frontend 서비스를 정의하고
Ollama는 호스트(host.docker.internal)에서 실행하도록 구성한다.

## 3. 변경 파일

| 파일 | 구분 | 설명 |
|------|------|------|
| `README.md` | 추가 | |
| `docker-compose.yml` | 추가 | |

## 4. 검증

- docker-compose.yml 문법 검토. Docker 데몬이 꺼져 있어 실제 기동은 미검증.

## 5. 비고 / 후속 작업

- backend/frontend의 Dockerfile.dev는 각 feature 브랜치에서 추가한다.
