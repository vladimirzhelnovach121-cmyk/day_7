# Проверка CI

> Поля `<...>` заполняются после запуска в вашем GitHub: удалённые run-ы (Actions) выполнить локально нельзя.
> SHA ниже — из локального репозитория; после push на GitHub они совпадут, если вы переносите историю как есть (иначе подставьте свои).

## Событие, ветка и SHA
- Workflow: `Python quality` (`.github/workflows/ci.yml`), события: `push` в `main`, `pull_request`, `workflow_dispatch`.
- Первый запуск: событие `push`, ветка `main`, SHA `7f2a54f` (коммит «Enable Python quality checks»), run: `<URL>`.
- Исходный набор: 6 тестов, OK, Python 3.11 и 3.12.

## Красный запуск
- Ветка `ci/boundary`, событие `pull_request`, SHA `c3b6c32` («Demonstrate boundary failure for CI lab»).
- URL run: `<URL красного run>`; job: `tests (3.11)` и `tests (3.12)`; упавший step: **Run tests**.
- Изменение: в `sla.py` `elapsed_minutes > LIMITS[priority]` заменено на `>=`.
- Упали 3 теста: `test_at_limit`, `test_high_priority`, `test_low_priority`.
- Ожидалось: `is_overdue(120)` → `False` (на границе просрочки нет); фактически `True` (`AssertionError: True is not false`). Аналогично `is_overdue(30, "high")` и `is_overdue(480, "low")`.
- Причина: по REQUIREMENTS.md просрочка наступает строго после лимита, а `>=` считает просроченной и саму границу.

## Исправление
- SHA `96b1815` («Restore strict SLA boundary»): возвращён оператор `>`, новый коммит (историю не переписывали).
- URL зелёного run: `<URL>`; шесть тестов проходят.

## Зелёный запуск на Python 3.11 и 3.12
- Финальный SHA ветки: `1ac6956` («Test invalid SLA inputs»), run: `<URL>`; оба job зелёные, **8 тестов, OK**.
- После merge: push-запуск на `main`, SHA `<SHA merge>`, run: `<URL>`.
- Локально проверено на Python 3.12.3: 8 тестов, OK. Python 3.11 локально не запускался — его проверяет матрица CI.

## Два новых сценария
- `test_negative_elapsed`: `is_overdue(-1)` должен вызывать `ValueError`.
- `test_unknown_priority`: `is_overdue(10, "urgent")` должен вызывать `ValueError`; `urgent` не входит в допустимые `high`, `normal`, `low`.
- Проверка пользы: при удалении проверки отрицательного времени из `sla.py` `test_negative_elapsed` падает.
- Итоговый diff с `main` содержит только 6 добавленных строк в тестах; `>=` в нём нет.

## Что автоматическая проверка пока не покрывает
- Типы входа, кроме числа и строки (`None`, строка вместо числа, `bool`, `NaN`) — вне учебного контракта.
- Версии Python вне матрицы (3.11, 3.12) и другие ОС.
- Приоритет `normal` проверен только через значение по умолчанию; границы 29/30/31 и 479/480/481 покрыты частично.
- Красный check сам по себе не запрещает merge: нужны правила ветки/ruleset с обязательными проверками.
- Тесты проверяют только описанные случаи; «OK» не доказывает отсутствие других ошибок.
