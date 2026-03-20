ROOT_DIR := .
.DEFAULT_GOAL := install

.PHONY: install test lint format compose-up compose-down compose compose-d

install:
	uv sync --all-packages
	pnpm --dir apps/web install

test:
	$(MAKE) -C apps/api test
	$(MAKE) -C apps/e2e test
	pnpm --dir apps/web test

lint:
	$(MAKE) -C apps/api lint
	$(MAKE) -C apps/e2e lint
	pnpm --dir apps/web lint

format:
	$(MAKE) -C apps/api format
	$(MAKE) -C apps/e2e format
	pnpm --dir apps/web format

compose-up:
	docker compose up --build

compose-down:
	docker compose down --remove-orphans

compose: compose-down compose-up

compose-d: compose-down
	docker compose up --build -d