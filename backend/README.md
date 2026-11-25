# VolunteerHub API

Проверка доступности приложения и базы данных: `GET /api/health`.

Для локального запуска задайте `DATABASE_URL`, `SECRET_KEY` (случайное значение не короче 32 символов)
и `APP_ORIGIN=http://127.0.0.1:5173`. Примените миграции `alembic upgrade head`.
Запуск из каталога backend: `uvicorn app.main:create_app --factory --reload --port 8080`.
