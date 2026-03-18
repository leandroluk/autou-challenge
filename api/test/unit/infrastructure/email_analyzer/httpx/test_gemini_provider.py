from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.domain.email.enums import CategoryEnum
from src.infrastructure.email_analyzer.httpx.gemini_provider import HttpxGeminiEmailAnalyzerPortProvider


@pytest.fixture
def mock_httpx_client() -> tuple[AsyncMock, MagicMock]:
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_client.post.return_value = mock_response
    return mock_client, mock_response


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.gemini_provider.httpx.AsyncClient")
async def test_analyze_text_success(
    mock_client_class: MagicMock,
    mock_httpx_client: tuple[AsyncMock, MagicMock],
) -> None:
    mock_client, mock_response = mock_httpx_client
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_response.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": '{"category": "Productive", "suggested_reply": "gemini text"}',
                        }
                    ]
                }
            }
        ]
    }

    provider = HttpxGeminiEmailAnalyzerPortProvider("fake-key", "f-model")
    cat, _ = await provider.analyze_text("custom text gemini")

    assert cat == CategoryEnum.PRODUCTIVE

    mock_client.post.assert_called_once()
    kwargs = mock_client.post.call_args.kwargs
    assert kwargs["params"]["key"] == "fake-key"
    assert kwargs["json"]["contents"][0]["parts"][0]["text"] == "custom text gemini"


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.gemini_provider.httpx.AsyncClient")
async def test_analyze_text_http_error(
    mock_client_class: MagicMock,
    mock_httpx_client: tuple[AsyncMock, MagicMock],
) -> None:
    mock_client, mock_response = mock_httpx_client
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_response.status_code = 500
    mock_response.text = "Internal Server Error Google"
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "G",
        request=MagicMock(),
        response=mock_response,
    )

    provider = HttpxGeminiEmailAnalyzerPortProvider("k", "m")
    with pytest.raises(Exception, match="HTTP 500 Internal Server Error Google"):
        await provider.analyze_text("fail")


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.gemini_provider.httpx.AsyncClient")
async def test_analyze_text_request_error(
    mock_client_class: MagicMock,
    mock_httpx_client: tuple[AsyncMock, MagicMock],
) -> None:
    mock_client, _ = mock_httpx_client
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_client.post.side_effect = httpx.RequestError("Network is unreachable")

    provider = HttpxGeminiEmailAnalyzerPortProvider("k", "m")

    with pytest.raises(Exception, match="Request failed: Network is unreachable"):
        await provider.analyze_text("fail")


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.gemini_provider.httpx.AsyncClient")
async def test_analyze_file_success(
    mock_client_class: MagicMock,
    mock_httpx_client: tuple[AsyncMock, MagicMock],
) -> None:
    mock_client, mock_response = mock_httpx_client
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_response.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {
                            "text": '{"category": "Unproductive", "suggested_reply": "g"}',
                        }
                    ]
                }
            }
        ]
    }

    provider = HttpxGeminiEmailAnalyzerPortProvider("k", "m")
    cat, _ = await provider.analyze_file(["b64p1"], "image/png")

    assert cat == CategoryEnum.UNPRODUCTIVE

    mock_client.post.assert_called_once()
    parts = mock_client.post.call_args.kwargs["json"]["contents"][0]["parts"]
    assert len(parts) == 2
    assert parts[1]["inline_data"]["mime_type"] == "image/png"
    assert parts[1]["inline_data"]["data"] == "b64p1"


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.gemini_provider.httpx.AsyncClient")
async def test_analyze_file_http_error(
    mock_client_class: MagicMock,
    mock_httpx_client: tuple[AsyncMock, MagicMock],
) -> None:
    mock_client, mock_response = mock_httpx_client
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_response.status_code = 502
    mock_response.text = "Bad Gateway"
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Error", request=MagicMock(), response=mock_response
    )

    provider = HttpxGeminiEmailAnalyzerPortProvider("k", "m")

    with pytest.raises(Exception, match="HTTP 502 Bad Gateway"):
        await provider.analyze_file(["b64"], "image/png")


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.gemini_provider.httpx.AsyncClient")
async def test_analyze_file_request_error(
    mock_client_class: MagicMock,
    mock_httpx_client: tuple[AsyncMock, MagicMock],
) -> None:
    mock_client, _ = mock_httpx_client
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_client.post.side_effect = httpx.RequestError("Connection timeout")

    provider = HttpxGeminiEmailAnalyzerPortProvider("k", "m")

    with pytest.raises(Exception, match="Request failed: Connection timeout"):
        await provider.analyze_file(["b64"], "image/png")


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.gemini_provider.httpx.AsyncClient")
async def test_analyze_file__parse_error(
    mock_client_class: MagicMock,
    mock_httpx_client: tuple[AsyncMock, MagicMock],
) -> None:
    mock_client, mock_response = mock_httpx_client
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_response.json.return_value = {"candidates": [{"content": {"parts": [{"text": "invalid json"}]}}]}

    provider = HttpxGeminiEmailAnalyzerPortProvider("k", "m")

    with pytest.raises(Exception, match="Unexpected model output"):
        await provider.analyze_file(["b64"], "image/png")
