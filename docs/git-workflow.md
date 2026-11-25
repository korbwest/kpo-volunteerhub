# Работа с исходным кодом

## Ветвление

Используется GitHub Flow. `main` содержит принятую версию проекта. Изменения выполняются в короткоживущих ветках, созданных от актуальной `main`:

- `feat/...` — функциональность;
- `fix/...` — исправления;
- `test/...` — тесты;
- `docs/...` — документация;
- `ci/...` — автоматизация проверок и сборки.

Первоначальный прототип подготовлен в `feat/initial-prototype`. Постоянной ветки `develop` нет.

```powershell
git switch main
git pull --ff-only origin main
git switch -c feat/project-search
```

## Коммиты

Формат сообщения: `type(scope): описание`. Область `scope` необязательна. Заголовок не длиннее 100 символов. Один коммит соответствует одной связанной задаче.

```text
feat(db): add user and project models
feat(auth): add authentication endpoints
test(projects): cover project access and filtering
fix(auth): correct login validation
docs: describe local setup
```

Используются типы `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`. Для несовместимого изменения после типа или области указывается `!`, а причина описывается в сообщении.

Сообщения проверяются хуком commit-msg и заданием commits в Quality.
После клонирования выполните `git config core.hooksPath .githooks`.

## Pull request и слияние

После локальных проверок рабочая ветка отправляется на GitHub и открывается pull request в `main`. В описании указываются изменения, способ проверки и известные ограничения.

Способ слияния — **Squash and merge**. Один PR создаёт один итоговый коммит в main.
Перед слиянием проверяются сообщения коммитов, итоговый заголовок и результаты обязательных проверок.

Для main используются обязательный PR и проверки commits, backend, frontend, metrics и build.
Параметры защиты и порядок релиза приведены в [workflow.md](workflow.md).
