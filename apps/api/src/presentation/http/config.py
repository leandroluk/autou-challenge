import os
from collections.abc import Callable
from typing import cast

from pydantic import BaseModel, Field

from src.application._shared.container import injectable


def _get[T](key: str, default: T) -> Callable[[], T]:
    """
    Get an environment variable with a default value.
    """

    def wrapper() -> T:
        value = os.getenv(key)
        if value is None:
            return default
        elif isinstance(default, bool):
            value = value.lower() == "true"
        elif isinstance(default, int):
            value = int(value)
        return cast(T, value)

    return wrapper


@injectable
class HttpConfig(BaseModel):
    """
    Configuration for the HTTP server.
    """

    host: str = Field(default_factory=_get("HTTP_HOST", "127.0.0.1"))
    port: int = Field(default_factory=_get("HTTP_PORT", 8000))
    base_path: str = Field(default_factory=_get("HTTP_BASE_PATH", "/api/v1"))
    docs_path: str = Field(default_factory=_get("HTTP_DOCS_PATH", "/docs"))
    redoc_path: str = Field(default_factory=_get("HTTP_REDOC_PATH", "/redoc"))
    enable_reload: bool = Field(default_factory=_get("HTTP_ENABLE_RELOAD", True))
    title: str = Field(default_factory=_get("HTTP_TITLE", "AutoU Email Triage API"))
    version: str = Field(default_factory=_get("HTTP_VERSION", "1.0.0"))
    description: str = Field(default_factory=_get("HTTP_DESCRIPTION", "Email triage API - AutoU challenge."))
