from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.domain.email.enums import CategoryEnum
from src.infrastructure.email_analyzer.httpx.openai_provider import HttpxOpenAIEmailAnalyzerPortProvider


@pytest.fixture
def mock_httpx_client() -> tuple[AsyncMock, MagicMock]:
    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_client.post.return_value = mock_response
    return mock_client, mock_response


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.openai_provider.httpx.AsyncClient")
async def test_analyze_text_success(
    mock_client_class: MagicMock,
    mock_httpx_client: tuple[AsyncMock, MagicMock],
) -> None:
    mock_client, mock_response = mock_httpx_client
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": '{"category": "Productive", "reply": "reply text"}',
                }
            }
        ]
    }

    provider = HttpxOpenAIEmailAnalyzerPortProvider("fake-key", "fake-model")
    cat, reply = await provider.analyze_text("my custom email text")

    assert cat == CategoryEnum.PRODUCTIVE
    assert reply == "reply text"

    # Asserting payload
    mock_client.post.assert_called_once()
    kwargs = mock_client.post.call_args.kwargs
    assert kwargs["headers"]["Authorization"] == "Bearer fake-key"
    assert "fake-model" in kwargs["json"]["model"]
    assert kwargs["json"]["messages"][1]["content"] == "my custom email text"


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.openai_provider.httpx.AsyncClient")
async def test_analyze_text_http_error(
    mock_client_class: MagicMock,
    mock_httpx_client: tuple[AsyncMock, MagicMock],
) -> None:
    mock_client, mock_response = mock_httpx_client
    mock_client_class.return_value.__aenter__.return_value = mock_client

    # Simulate HTTP Error
    mock_response.status_code = 429
    mock_response.text = "Too Many Requests"
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Err", request=MagicMock(), response=mock_response
    )

    provider = HttpxOpenAIEmailAnalyzerPortProvider("k", "m")
    with pytest.raises(Exception, match="HTTP 429 Too Many Requests"):
        await provider.analyze_text("fail")


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.openai_provider.httpx.AsyncClient")
async def test_analyze_text_request_error(
    mock_client_class: MagicMock,
    mock_httpx_client: tuple[AsyncMock, MagicMock],
) -> None:
    mock_client, _ = mock_httpx_client
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_client.post.side_effect = httpx.RequestError("Network is unreachable")

    provider = HttpxOpenAIEmailAnalyzerPortProvider("k", "m")

    with pytest.raises(Exception, match="Request failed: Network is unreachable"):
        await provider.analyze_text("fail")


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.openai_provider.httpx.AsyncClient")
async def test_analyze_file_success(
    mock_client_class: MagicMock,
    mock_httpx_client: tuple[AsyncMock, MagicMock],
) -> None:
    mock_client, mock_response = mock_httpx_client
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": '{"category": "Unproductive", "reply": "file text"}',
                }
            }
        ]
    }

    provider = HttpxOpenAIEmailAnalyzerPortProvider("fake-key", "fake-model")
    cat, reply = await provider.analyze_file(["base64png"], "image/png")

    assert cat == CategoryEnum.UNPRODUCTIVE
    assert reply == "file text"

    # Asserting payload format
    mock_client.post.assert_called_once()
    payload = mock_client.post.call_args.kwargs["json"]["messages"][0]["content"]
    assert isinstance(payload, list)
    assert payload[1]["type"] == "image_url"
    assert payload[1]["image_url"]["url"] == "data:image/png;base64,base64png"
    assert payload[1]["image_url"]["detail"] == "auto"


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.openai_provider.httpx.AsyncClient")
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

    provider = HttpxOpenAIEmailAnalyzerPortProvider("k", "m")

    with pytest.raises(Exception, match="HTTP 502 Bad Gateway"):
        await provider.analyze_file(["b64"], "image/png")


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.openai_provider.httpx.AsyncClient")
async def test_analyze_file_request_error(
    mock_client_class: MagicMock,
    mock_httpx_client: tuple[AsyncMock, MagicMock],
) -> None:
    mock_client, _ = mock_httpx_client
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_client.post.side_effect = httpx.RequestError("Connection timeout")

    provider = HttpxOpenAIEmailAnalyzerPortProvider("k", "m")

    with pytest.raises(Exception, match="Request failed: Connection timeout"):
        await provider.analyze_file(["b64"], "image/png")


@pytest.mark.asyncio
@patch("src.infrastructure.email_analyzer.httpx.openai_provider.httpx.AsyncClient")
async def test_analyze_file__parse_error(
    mock_client_class: MagicMock,
    mock_httpx_client: tuple[AsyncMock, MagicMock],
) -> None:
    mock_client, mock_response = mock_httpx_client
    mock_client_class.return_value.__aenter__.return_value = mock_client

    mock_response.json.return_value = {"choices": [{"message": {"content": "invalid json"}}]}

    provider = HttpxOpenAIEmailAnalyzerPortProvider("k", "m")

    with pytest.raises(Exception, match="Unexpected model output"):
        await provider.analyze_file(["b64"], "image/png")
