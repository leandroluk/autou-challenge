ROOT_DIR := ../..
.DEFAULT_GOAL := dev

.PHONY: install build dev test test-cov lint format docker-build docker-run

install:
	uv sync

build:
	uv build

dev:
	uv run python -m src

test:
	uv run pytest

test-cov:
	uv run pytest --cov=src --cov-report=term-missing

lint:
	uv run ruff check --fix

format:
	uv run ruff format

docker-build:
	docker build -t autou-challenge-api .

docker-run:
	docker run --rm -p 8000:8000 autou-challenge-api