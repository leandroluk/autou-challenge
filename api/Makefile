.DEFAULT_GOAL := run

.PHONY: run setup test test-cov lint format

run:
	uv run python -m src

setup:
	uv sync

test:
	uv run pytest

test-cov:
	uv run pytest --cov=src --cov-report=term-missing

lint:
	uv run ruff check --fix

format:
	uv run ruff format