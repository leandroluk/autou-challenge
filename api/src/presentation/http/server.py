from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.application._shared.container import injectable
from src.presentation.http.config import HttpConfig
from src.presentation.http.email.router import router as email_router
from src.presentation.http.system.router import router as system_router


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
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self._apply_routes()

    def _apply_routes(self) -> None:
        prefix = self.config.base_path.rstrip("/")
        for router in [email_router, system_router]:
            self.app.include_router(router, prefix=prefix)
