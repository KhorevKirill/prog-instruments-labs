# Отчёт по ЛР1 «Инструменты контроля качества и CI»

Исходный проект: гибридная криптосистема RSA + 3DES из
[KhorevKirill/isb-2026, ветка lab3_var22](https://github.com/KhorevKirill/isb-2026/tree/lab3_var22).
Программа генерирует пару ключей RSA и ключ 3DES, шифрует ключ 3DES открытым
ключом RSA, а затем шифрует и расшифровывает файл алгоритмом 3DES-CBC.

## Что добавлено

| Файл | Назначение |
| --- | --- |
| `pyproject.toml` | конфиги ruff (линтер + форматтер) и pyright |
| `requirements.txt`, `requirements-dev.txt` | зависимости программы и инструментов (версии закреплены) |
| `Makefile` | команды запуска, проверок и установки хуков |
| `.pre-commit-config.yaml` | хуки pre-commit и pre-push |
| `roundtrip_check.py` | сквозной прогон gen → enc → dec (тестов в проекте не было) |
| `../.github/workflows/lab_1_checks.yml` | проверка push и pull request в GitHub Actions |

### Ruff

* длина строки 79 символов (PEP 8), цель — Python 3.12;
* включено 32 группы правил: pycodestyle, pyflakes, isort, pep8-naming,
  pydocstyle, аннотации, bandit, bugbear, pylint, tryceratops, pathlib и др.;
* отключены только правила, которые противоречат проекту: RUF001–003
  (кириллица в строках), ISC001 (конфликт с форматтером), T201 (print —
  интерфейс консольной программы);
* сложность функции (mccabe) не выше 8.

### Pyright

Режим `strict` плюс `reportDeprecated`, `reportUnnecessaryTypeIgnoreComment`
и `reportMissingModuleSource` как ошибки.

## Что исправлено в коде

* код отформатирован `ruff format`, импорты отсортированы;
* добавлены докстринги модулей;
* сообщения об ошибках вынесены в собственные классы исключений (`errors.py`);
* `open()` заменён на `pathlib.Path.open()`;
* `main()` разбит на `build_parser()` и `apply_overrides()`, вместо `match` по
  кортежу флагов — обычное ветвление; при ошибке код возврата 1;
* настройки описаны `TypedDict` (`settings.py`) и проверяются при загрузке;
* при чтении закрытого ключа проверяется, что это именно ключ RSA;
* `TripleDES` импортируется из `cryptography.hazmat.decrepit`: старый путь
  устарел и выдавал `CryptographyDeprecationWarning`.

Итог: `ruff check`, `ruff format --check` и `pyright` — 0 ошибок и предупреждений.

## Команды

```text
make install        создать .venv и поставить зависимости
make run-gen        сгенерировать ключи (CONFIG=config.json)
make run-enc        зашифровать файл
make run-dec        расшифровать файл
make lint           ruff check
make lint-fix       ruff check --fix
make format         ruff format
make format-check   ruff format --check
make typecheck      pyright
make fullcheck      lint + format-check + typecheck
make test           сквозной прогон gen -> enc -> dec
make fulltest       fullcheck + test
make precommit      установить хуки pre-commit и pre-push
make precommit-run  прогнать все хуки по всем файлам
make clean          удалить кэши
```

Все команды выполняются из каталога `lab_1`. На Windows нужен GNU make и
лаунчер `py` (Python 3.12+).
