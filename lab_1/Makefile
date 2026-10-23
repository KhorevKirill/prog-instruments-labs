# Makefile ЛР1: установка окружения, запуск программы и проверки качества кода.
# Все команды выполняются из каталога lab_1: `make <цель>`, список целей: `make help`.
# Linux/macOS и GitHub Actions — python3, Windows (GNU make) — лаунчер py.

ifeq ($(OS),Windows_NT)
    PYTHON ?= py -3.12
    BIN := .venv/Scripts
else
    PYTHON ?= python3
    BIN := .venv/bin
endif

PY := $(BIN)/python
CONFIG ?= config.json
SRC := .

.DEFAULT_GOAL := help
.PHONY: help install run-gen run-enc run-dec lint lint-fix format \
	format-check typecheck fullcheck smoke test fulltest precommit \
	precommit-run clean

help: ## показать список команд
	@$(PYTHON) -c "import re; [print(f'  make {m[0]:<14} {m[1]}') for m in re.findall(r'^([a-z-]+):.*?## (.*)$$', open('Makefile', encoding='utf-8').read(), re.M)]"

$(PY):
	$(PYTHON) -m venv .venv

install: $(PY) ## создать .venv и установить зависимости и dev-инструменты
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -r requirements-dev.txt

run-gen: ## сгенерировать ключи (CONFIG=config.json)
	$(PY) main.py --gen $(CONFIG)

run-enc: ## зашифровать input_file (CONFIG=config.json)
	$(PY) main.py --enc $(CONFIG)

run-dec: ## расшифровать encrypted_file (CONFIG=config.json)
	$(PY) main.py --dec $(CONFIG)

lint: ## статический анализ: ruff check
	$(PY) -m ruff check $(SRC)

lint-fix: ## ruff check с автоисправлением
	$(PY) -m ruff check --fix $(SRC)

format: ## автоформатирование: ruff format
	$(PY) -m ruff format $(SRC)

format-check: ## проверить форматирование без изменений
	$(PY) -m ruff format --check --diff $(SRC)

typecheck: ## проверка типов: pyright (strict)
	$(PY) -m pyright --pythonpath $(PY)

fullcheck: lint format-check typecheck ## все статические проверки

smoke: ## сквозной прогон gen -> enc -> dec во временном каталоге
	$(PY) roundtrip_check.py

test: smoke ## тесты проекта (модульных тестов нет, только сквозной прогон)

fulltest: fullcheck test ## статические проверки и тесты

precommit: ## установить git-хуки pre-commit и pre-push
	$(PY) -m pre_commit install --config .pre-commit-config.yaml \
		--hook-type pre-commit --hook-type pre-push

precommit-run: ## прогнать все хуки по всем файлам lab_1
	$(PY) -m pre_commit run --config .pre-commit-config.yaml \
		--all-files --hook-stage pre-push

clean: ## удалить кэши инструментов
	$(PY) -c "import pathlib, shutil; [shutil.rmtree(p, ignore_errors=True) for p in ['.ruff_cache', *pathlib.Path('.').rglob('__pycache__')]]"
