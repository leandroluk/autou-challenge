from typing import cast

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.types import ExceptionHandler

from src.application._shared.container import injectable
from src.presentation.http.config import HttpConfig
from src.presentation.http.email.router import router as email_router
from src.presentation.http.system.router import router as system_router


async def request_validation_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    errors = [f"{' -> '.join(str(loc) for loc in e['loc'])}: {e['msg']}" for e in exc.errors()]
    return JSONResponse(status_code=400, content={"detail": "; ".join(errors)})


async def pydantic_validation_handler(_: Request, exc: ValidationError) -> JSONResponse:
    errors = [f"{' -> '.join(str(loc) for loc in e['loc'])}: {e['msg']}" for e in exc.errors()]
    return JSONResponse(status_code=400, content={"detail": "; ".join(errors)})


@injectable
class HttpServer:
    config: HttpConfig
    app: FastAPI

    def __init__(self, config: HttpConfig):
        self.config = config
        self.app = FastAPI(
            title=config.title,
            version=config.version,
            description=config.description,
            docs_url=config.docs_path,
            redoc_url=config.redoc_path,
        )
        self.app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
        self.app.add_exception_handler(RequestValidationError, cast(ExceptionHandler, request_validation_handler))
        self.app.add_exception_handler(ValidationError, cast(ExceptionHandler, pydantic_validation_handler))

        prefix = self.config.base_path.rstrip("/")
        for router in [email_router, system_router]:
            self.app.include_router(router, prefix=prefix)
