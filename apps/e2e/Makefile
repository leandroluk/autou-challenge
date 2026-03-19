ROOT_DIR := ../..
.DEFAULT_GOAL := run

.PHONY: install test lint format

install:
	uv sync
	uv run python -m Browser.entry init

test:
	uv run robot --outputdir .robot test

lint:
	uv run robocop check test

format:
	uv run robocop format test