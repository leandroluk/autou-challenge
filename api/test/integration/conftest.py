import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.application._shared.container import clear, register
from src.domain._shared.ports.email_analyzer import EmailAnalyzerPort
from src.infrastructure.email_analyzer.fake.adapter import FakeEmailAnalyzerAdapter
from src.presentation.http.config import HttpConfig
from src.presentation.http.server import HttpServer

app: FastAPI


@pytest.fixture(autouse=True)
def setup_container():
    global app
    register(EmailAnalyzerPort, FakeEmailAnalyzerAdapter)
    app = HttpServer(config=HttpConfig()).app
    yield
    clear()


@pytest.fixture
async def http_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as async_client:
        yield async_client
