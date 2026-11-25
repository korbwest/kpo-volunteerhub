# VolunteerHub

Веб-приложение для взаимодействия волонтёров и организаций.

## Технологии

- Backend: Python, FastAPI, SQLAlchemy, PostgreSQL.
- Frontend: React, TypeScript, Vite.
- Проверки и сборка: GitHub Actions.

## Работа с репозиторием

Изменения выполняются в тематических ветках и принимаются в `main` через pull request.
Сообщения коммитов оформляются по Conventional Commits. Способ слияния — Squash and merge.

## Локальный запуск

Требуются Python 3.11+, Node.js 22 и npm.

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -c backend/requirements-dev.lock.txt -e "./backend[dev]"
git config core.hooksPath .githooks
cd backend
../.venv/Scripts/python.exe -m uvicorn app.main:app --reload --port 8080
```

Во втором терминале:

```powershell
cd frontend
npm ci
npm run dev
```

Текущая основа приложения содержит проверку доступности `GET /health` и стартовую страницу.
Предметные функции добавляются отдельными изменениями.

## Проверки

В каталоге backend: `ruff check .`, `ruff format --check .`, `pytest --cov=app`.
В каталоге frontend: `npm run lint`, `npm run format:check`, `npm run test:coverage`, `npm run build`.
Инструменты Python запускаются из установленного виртуального окружения.

GitHub Actions запускает проверки при push и pull request, затем создаёт артефакт `prototype-build`.
Метрики доступны в артефакте `quality-metrics`. На контрольных точках используется ручной запуск
Quality с параметром `lab5`, `lab6`, `lab7` или `final`; вычисления выполняются автоматически.

Подробности: [правила работы](docs/workflow.md), [методика метрик](docs/metrics.md).
