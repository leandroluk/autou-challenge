import os

from src.presentation.http.config import HttpConfig


def test_http_config() -> None:
    config = HttpConfig()
    assert config.host == "127.0.0.1"
    assert config.port == 8000
    assert config.base_path == "/api/v1"
    assert config.docs_path == "/docs"
    assert config.redoc_path == "/redoc"
    assert config.enable_reload is True
    assert config.title == "AutoU Email Triage API"
    assert config.version == "1.0.0"
    assert config.description == "Email triage API - AutoU challenge."


def test_http_config_with_env_vars() -> None:
    os.environ["HTTP_HOST"] = "[IP_ADDRESS]"
    os.environ["HTTP_PORT"] = "8080"
    os.environ["HTTP_BASE_PATH"] = "/api/v2"
    os.environ["HTTP_DOCS_PATH"] = "/docs"
    os.environ["HTTP_REDOC_PATH"] = "/redoc"
    os.environ["HTTP_ENABLE_RELOAD"] = "False"
    os.environ["HTTP_TITLE"] = "AutoU Email Triage API"
    os.environ["HTTP_VERSION"] = "1.0.0"
    os.environ["HTTP_DESCRIPTION"] = "Email triage API - AutoU challenge."

    config = HttpConfig()
    assert config.host == "[IP_ADDRESS]"
    assert config.port == 8080
    assert config.base_path == "/api/v2"
    assert config.docs_path == "/docs"
    assert config.redoc_path == "/redoc"
    assert config.enable_reload is False
    assert config.title == "AutoU Email Triage API"
    assert config.version == "1.0.0"
    assert config.description == "Email triage API - AutoU challenge."
