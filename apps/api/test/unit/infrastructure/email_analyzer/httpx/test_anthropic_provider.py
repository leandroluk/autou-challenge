from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from src.domain.email.enums import CategoryEnum
from src.infrastructure.email_analyzer.httpx.anthropic_provider import HttpxAnthropicEmailAnalyzerPortProvider


@pytest.fixture
def mock_httpx_client() -> tuple[AsyncMock, MagicMock]:
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_client.post.return_value = mock_response
    return mock_client, mock_response


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.anthropic_provider.httpx.AsyncClient")
async def test_analyze_text_success(
    mock_client_class: MagicMock,
    mock_httpx_client: tuple[AsyncMock, MagicMock],
) -> None:
    mock_client, mock_response = mock_httpx_client
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_response.json.return_value = {
        "content": [
            {
                "text": '{"category": "Productive", "reply": "claude text"}',
            }
        ]
    }

    provider = HttpxAnthropicEmailAnalyzerPortProvider("fake-key", "f-model")
    cat, _ = await provider.analyze_text("custom email")

    assert cat == CategoryEnum.PRODUCTIVE

    mock_client.post.assert_called_once()
    kwargs = mock_client.post.call_args.kwargs
    assert kwargs["headers"]["x-api-key"] == "fake-key"
    assert kwargs["json"]["messages"][0]["content"] == "custom email"


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.anthropic_provider.httpx.AsyncClient")
async def test_analyze_text_http_error(
    mock_client_class: MagicMock,
    mock_httpx_client: tuple[AsyncMock, MagicMock],
) -> None:
    mock_client, mock_response = mock_httpx_client
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "E",
        request=MagicMock(),
        response=mock_response,
    )

    provider = HttpxAnthropicEmailAnalyzerPortProvider("k", "m")
    with pytest.raises(Exception, match="HTTP 400 Bad Request"):
        await provider.analyze_text("fail")


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.anthropic_provider.httpx.AsyncClient")
async def test_analyze_text_request_error(
    mock_client_class: MagicMock,
    mock_httpx_client: tuple[AsyncMock, MagicMock],
) -> None:
    mock_client, _ = mock_httpx_client
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_client.post.side_effect = httpx.RequestError("Network is unreachable")

    provider = HttpxAnthropicEmailAnalyzerPortProvider("k", "m")

    with pytest.raises(Exception, match="Request failed: Network is unreachable"):
        await provider.analyze_text("fail")


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.anthropic_provider.httpx.AsyncClient")
async def test_analyze_file_success(
    mock_client_class: MagicMock,
    mock_httpx_client: tuple[AsyncMock, MagicMock],
) -> None:
    mock_client, mock_response = mock_httpx_client
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_response.json.return_value = {
        "content": [
            {
                "text": '{"category": "Unproductive", "reply": "c"}',
            }
        ]
    }

    provider = HttpxAnthropicEmailAnalyzerPortProvider("k", "m")
    cat, _ = await provider.analyze_file(["b64p1"], "image/jpeg")

    assert cat == CategoryEnum.UNPRODUCTIVE

    mock_client.post.assert_called_once()
    payload = mock_client.post.call_args.kwargs["json"]["messages"][0]["content"]
    assert isinstance(payload, list)
    assert payload[0]["type"] == "image"
    assert payload[0]["source"]["type"] == "base64"
    assert payload[0]["source"]["media_type"] == "image/jpeg"
    assert payload[0]["source"]["data"] == "b64p1"


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.anthropic_provider.httpx.AsyncClient")
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

    provider = HttpxAnthropicEmailAnalyzerPortProvider("k", "m")

    with pytest.raises(Exception, match="HTTP 502 Bad Gateway"):
        await provider.analyze_file(["b64"], "image/png")


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.anthropic_provider.httpx.AsyncClient")
async def test_analyze_file_request_error(
    mock_client_class: MagicMock,
    mock_httpx_client: tuple[AsyncMock, MagicMock],
) -> None:
    mock_client, _ = mock_httpx_client
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_client.post.side_effect = httpx.RequestError("Connection timeout")

    provider = HttpxAnthropicEmailAnalyzerPortProvider("k", "m")

    with pytest.raises(Exception, match="Request failed: Connection timeout"):
        await provider.analyze_file(["b64"], "image/png")


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.anthropic_provider.httpx.AsyncClient")
async def test_analyze_file__parse_error(
    mock_client_class: MagicMock,
    mock_httpx_client: tuple[AsyncMock, MagicMock],
) -> None:
    mock_client, mock_response = mock_httpx_client
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_response.json.return_value = {"content": [{"text": "invalid json"}]}

    provider = HttpxAnthropicEmailAnalyzerPortProvider("k", "m")

    with pytest.raises(Exception, match="Unexpected model output"):
        await provider.analyze_file(["b64"], "image/png")
