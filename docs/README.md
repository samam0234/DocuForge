# DocuForge 문서 저장소

프로젝트의 기획, 설계, 작업 기록, 운영 문서를 한곳에 모은다. 작성 규칙은 루트 [AGENTS.md](../AGENTS.md)를 따른다.

## 폴더 안내

| 폴더 | 용도 | 주요 문서 |
|------|------|-----------|
| [`plan/`](plan/) | 초기 기획·로직·DB·배포 계획 | 기획서 v1.0 (md/docx), 인수인계 문서 |
| [`Architecture/`](Architecture/) | 시스템·계층·데이터 흐름 | [system_architecture.md](Architecture/system_architecture.md) |
| [`branchs/`](branchs/) | 브랜치·커밋 기록 | [_template.md](branchs/_template.md) |
| [`find_debug/`](find_debug/) | 작업/실행 디버깅 일일 기록 | |
| [`guidance/`](guidance/) | 기능·실행 가이드 | [local_run_guide.md](guidance/local_run_guide.md) |
| [`trainings/`](trainings/) | 학습·연구 정리 | |
| [`repeater/`](repeater/) | 서버 연결·인프라 장애와 해결 | |
| [`vaildates/`](vaildates/) | 검증·체크리스트 | [mvp_checklist.md](vaildates/mvp_checklist.md) |
| [`web_management/`](web_management/) | 배포 전/배포 시 웹 관리 기록 | |

> 폴더명 `vaildates`는 인수인계 문서의 표기를 그대로 따른 것이다. 임의로 고치지 않는다.

## 문서 작성 규칙

- 문서는 한국어, 파일명은 영문 소문자와 `_`를 권장한다.
- 디버깅 기록(`find_debug/`)은 `YYMMDD_주제.md` 형식으로 하루 단위로 남긴다.
- 장애 기록(`repeater/`)은 **증상 → 원인 → 해결** 순서로 쓴다.
- 커밋 기록(`branchs/`)은 아래 규칙을 따른다.

### 커밋 기록 (`branchs/`)

- 파일명: `YYMMDD_HHMM_[커밋ID앞7자리]_[작성자]_[브랜치명].md` (브랜치명의 `/` → `-`)
- 템플릿 [`_template.md`](branchs/_template.md)를 사용한다.
- 작업 커밋 후 같은 브랜치에 `docs(branchs)` 커밋으로 기록 파일을 추가한다.
- 병합 기록은 총 병합 시점에 한 번에 작성한다.

## 처음 읽는다면

1. [plan/DocuForge_기획서_v1.0.md](plan/DocuForge_기획서_v1.0.md) — 무엇을 만드는가
2. [Architecture/system_architecture.md](Architecture/system_architecture.md) — 어떻게 구성되는가
3. [guidance/local_run_guide.md](guidance/local_run_guide.md) — 어떻게 실행하는가
4. [vaildates/mvp_checklist.md](vaildates/mvp_checklist.md) — 어떻게 검증하는가
