ROOT_DIR := .
.DEFAULT_GOAL := install

.PHONY: install test lint format _run

install:
	uv sync --all-packages
	python -c "\
import subprocess;\
def run(cmd):\
  try: subprocess.run(cmd, shell=True, check=True);\
  except FileNotFoundError: print(f'skipping: {cmd}');\
run('pnpm --dir apps/web install');\
"

_run:
	python -c "import subprocess,os;cmd=os.environ['CMD'];[(subprocess.run(f'make -C {app} '+cmd,shell=True,check=True) if True else None) for app in ['apps/api','apps/e2e']];subprocess.run('pnpm --dir apps/web '+cmd,shell=True)" CMD=$(CMD)

test:
	$(MAKE) _run CMD=test

lint:
	$(MAKE) _run CMD=lint

format:
	$(MAKE) _run CMD=format