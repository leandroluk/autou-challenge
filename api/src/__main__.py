import importlib

import uvicorn
from fastapi import FastAPI

from src.application._shared.container import resolve
from src.presentation.http.config import HttpConfig
from src.presentation.http.server import HttpServer


def _bootstrap() -> None:
    for module in ["src.infrastructure", "src.application", "src.presentation"]:
        importlib.import_module(module)


_bootstrap()

http_config = resolve(HttpConfig)
app: FastAPI = resolve(HttpServer).app


def run_app() -> None:
    if http_config.enable_reload:
        uvicorn.run("src.__main__:app", host=http_config.host, port=http_config.port, reload=True, reload_dirs=["src"])
    else:
        uvicorn.run(app, host=http_config.host, port=http_config.port)


if __name__ == "__main__":
    run_app()
