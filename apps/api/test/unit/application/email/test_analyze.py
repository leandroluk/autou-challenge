from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import ValidationError
from src.application.email.analyze import EmailAnalyzeHandler, EmailAnalyzeQuery
from src.domain._shared.ports.email_analyzer import (
    EmailAnalyzerPort,
    EmailAnalyzerPortProvider,
    EmailAnalyzerPortProviderEnum,
)
from src.domain._shared.ports.file_converter import FileConverterPort
from src.domain.email.enums import CategoryEnum
from src.domain.email.errors import EmailAnalyzerError, EmailConversionError


@pytest.fixture
def mock_provider() -> AsyncMock:
    provider = AsyncMock(spec=EmailAnalyzerPortProvider)
    provider.analyze_file.return_value = (CategoryEnum.PRODUCTIVE, "mocked file reply")
    provider.analyze_text.return_value = (CategoryEnum.UNPRODUCTIVE, "mocked text reply")
    return provider


@pytest.fixture
def mock_analyzer(mock_provider: AsyncMock) -> MagicMock:
    analyzer = MagicMock(spec=EmailAnalyzerPort)
    analyzer.get_provider.return_value = mock_provider
    return analyzer


@pytest.fixture
def mock_converter() -> AsyncMock:
    converter = AsyncMock(spec=FileConverterPort)
    converter.convert.return_value = (["b64page1"], "image/png")
    return converter


@pytest.fixture
def handler(mock_analyzer: MagicMock, mock_converter: AsyncMock) -> EmailAnalyzeHandler:
    return EmailAnalyzeHandler(email_analyzer=mock_analyzer, file_converter=mock_converter)


def test_query_validation_mutually_exclusive() -> None:
    with pytest.raises(ValidationError):
        EmailAnalyzeQuery(
            provider=EmailAnalyzerPortProviderEnum.OPENAI_GPT_4O_MINI,
            api_key="test",
            file=("test.pdf", b"123"),
            text="test",
        )

    with pytest.raises(ValidationError):
        EmailAnalyzeQuery(provider=EmailAnalyzerPortProviderEnum.OPENAI_GPT_4O_MINI, api_key="test")


@pytest.mark.asyncio
async def test_execute_with_text(
    handler: EmailAnalyzeHandler, mock_analyzer: MagicMock, mock_provider: AsyncMock
) -> None:
    query = EmailAnalyzeQuery(
        provider=EmailAnalyzerPortProviderEnum.OPENAI_GPT_4O_MINI, api_key="test-key", text="hello"
    )
    result = await handler.execute(query)

    mock_analyzer.get_provider.assert_called_once_with(
        EmailAnalyzerPortProviderEnum.OPENAI_GPT_4O_MINI,
        "test-key",
    )
    mock_provider.analyze_text.assert_called_once_with("hello")
    mock_provider.analyze_file.assert_not_called()
    assert result.category == CategoryEnum.UNPRODUCTIVE.value
    assert result.reply == "mocked text reply"


@pytest.mark.asyncio
async def test_execute_with_file_pdf(
    handler: EmailAnalyzeHandler, mock_provider: AsyncMock, mock_converter: AsyncMock
) -> None:
    query = EmailAnalyzeQuery(
        provider=EmailAnalyzerPortProviderEnum.GEMINI_2_5_FLASH,
        api_key="key",
        file=(
            "test.pdf",
            b"pdfcontent",
        ),
    )
    result = await handler.execute(query)

    mock_converter.convert.assert_called_once_with("test.pdf", b"pdfcontent")
    mock_provider.analyze_file.assert_called_once_with(["b64page1"], "image/png")
    mock_provider.analyze_text.assert_not_called()
    assert result.category == CategoryEnum.PRODUCTIVE.value
    assert result.reply == "mocked file reply"


@pytest.mark.asyncio
async def test_execute_with_file_txt_fallback(
    handler: EmailAnalyzeHandler,
    mock_provider: AsyncMock,
    mock_converter: AsyncMock,
) -> None:
    mock_converter.convert.return_value = (["pure text"], "text/plain")
    query = EmailAnalyzeQuery(
        provider=EmailAnalyzerPortProviderEnum.ANTHROPIC_CLAUDE_SONNET_4_5,
        api_key="key",
        file=("test.txt", b"txtcontent"),
    )

    result = await handler.execute(query)

    mock_converter.convert.assert_called_once_with("test.txt", b"txtcontent")
    mock_provider.analyze_text.assert_called_once_with("pure text")
    mock_provider.analyze_file.assert_not_called()
    assert result.category == CategoryEnum.UNPRODUCTIVE.value


@pytest.mark.asyncio
async def test_execute_conversion_error(handler: EmailAnalyzeHandler, mock_converter: AsyncMock) -> None:
    mock_converter.convert.side_effect = Exception("pymupdf failed")
    query = EmailAnalyzeQuery(
        provider=EmailAnalyzerPortProviderEnum.OPENAI_GPT_4O_MINI, api_key="k", file=("err.pdf", b"x")
    )

    with pytest.raises(EmailConversionError) as exc_info:
        await handler.execute(query)

    assert "Could not convert 'err.pdf'" in str(exc_info.value)


@pytest.mark.asyncio
async def test_execute_analyzer_error(handler: EmailAnalyzeHandler, mock_provider: AsyncMock) -> None:
    mock_provider.analyze_text.side_effect = Exception("API down")
    query = EmailAnalyzeQuery(provider=EmailAnalyzerPortProviderEnum.OPENAI_GPT_4O_MINI, api_key="k", text="hi")

    with pytest.raises(EmailAnalyzerError) as exc_info:
        await handler.execute(query)

    assert "API down" in str(exc_info.value)
