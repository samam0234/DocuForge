# 커밋 기록: chore(backend): Rails 8 API 앱 생성 및 PostgreSQL, CORS 설정

| 항목 | 내용 |
|------|------|
| 일시 | 2026-10-23 06:22 |
| 커밋 ID | `15dcd8f` |
| 작성자 | claude |
| 브랜치 | `feature/rails-api` |
| 커밋 메시지 | `chore(backend): Rails 8 API 앱 생성 및 PostgreSQL, CORS 설정` |

## 1. 작업 목적

- 기획서의 Rails Orchestrator 계층을 최소 구성의 API 전용 앱으로 준비한다.

## 2. 변경 내용

rails new --api로 최소 구성(불필요한 프레임워크 제외)의 백엔드를 생성한다.
DB 접속 정보를 환경 변수로 받도록 database.yml을 수정하고,
rack-cors로 프론트엔드 출처만 허용한다. Windows에서 생성된 bin/ shebang을
리눅스 컨테이너에서도 동작하도록 ruby로 수정하고 개발용 Dockerfile을 추가한다.

## 3. 변경 파일

| 파일 | 구분 | 설명 |
|------|------|------|
| `backend/.dockerignore` | 추가 | |
| `backend/.ruby-version` | 추가 | |
| `backend/Dockerfile.dev` | 추가 | |
| `backend/Gemfile` | 추가 | |
| `backend/Gemfile.lock` | 추가 | |
| `backend/README.md` | 추가 | |
| `backend/Rakefile` | 추가 | |
| `backend/app/controllers/concerns/.keep` | 추가 | |
| `backend/app/jobs/application_job.rb` | 추가 | |
| `backend/app/models/application_record.rb` | 추가 | |
| `backend/app/models/concerns/.keep` | 추가 | |
| `backend/bin/ci` | 추가 | |
| `backend/bin/dev` | 추가 | |
| `backend/bin/rails` | 추가 | |
| `backend/bin/rake` | 추가 | |
| `backend/bin/setup` | 추가 | |
| `backend/config.ru` | 추가 | |
| `backend/config/application.rb` | 추가 | |
| `backend/config/boot.rb` | 추가 | |
| `backend/config/ci.rb` | 추가 | |
| `backend/config/credentials.yml.enc` | 추가 | |
| `backend/config/database.yml` | 추가 | |
| `backend/config/environment.rb` | 추가 | |
| `backend/config/environments/development.rb` | 추가 | |
| `backend/config/environments/production.rb` | 추가 | |
| `backend/config/environments/test.rb` | 추가 | |
| `backend/config/initializers/cors.rb` | 추가 | |
| `backend/config/initializers/filter_parameter_logging.rb` | 추가 | |
| `backend/config/initializers/inflections.rb` | 추가 | |
| `backend/config/locales/en.yml` | 추가 | |
| `backend/config/puma.rb` | 추가 | |
| `backend/db/seeds.rb` | 추가 | |
| `backend/lib/tasks/.keep` | 추가 | |
| `backend/log/.keep` | 추가 | |
| `backend/public/robots.txt` | 추가 | |
| `backend/script/.keep` | 추가 | |
| `backend/test/controllers/.keep` | 추가 | |
| `backend/test/models/.keep` | 추가 | |
| `backend/test/test_helper.rb` | 추가 | |
| `backend/tmp/.keep` | 추가 | |
| ... 외 1개 | | |

## 4. 검증

- bin/rails zeitwerk:check → All is good. bundle check 통과.

## 5. 비고 / 후속 작업

- credentials.yml.enc는 커밋되었고 master.key는 .gitignore로 제외된다. 개발 환경에서는 master.key가 필요 없다.
