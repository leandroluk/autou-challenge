from src.domain._shared.ports.email_analyzer import EmailAnalyzerPortProviderEnum
from src.infrastructure.email_analyzer.httpx.adapter import HttpxEmailAnalyzerAdapter
from src.infrastructure.email_analyzer.httpx.anthropic_provider import HttpxAnthropicEmailAnalyzerPortProvider
from src.infrastructure.email_analyzer.httpx.gemini_provider import HttpxGeminiEmailAnalyzerPortProvider
from src.infrastructure.email_analyzer.httpx.openai_provider import HttpxOpenAIEmailAnalyzerPortProvider


def test_get_provider_openai() -> None:
    adapter = HttpxEmailAnalyzerAdapter()
    provider = adapter.get_provider(EmailAnalyzerPortProviderEnum.OPENAI_GPT_4O_MINI, "key")
    assert isinstance(provider, HttpxOpenAIEmailAnalyzerPortProvider)


def test_get_provider_anthropic() -> None:
    adapter = HttpxEmailAnalyzerAdapter()
    provider = adapter.get_provider(EmailAnalyzerPortProviderEnum.ANTHROPIC_CLAUDE_SONNET_4_5, "key")
    assert isinstance(provider, HttpxAnthropicEmailAnalyzerPortProvider)


def test_get_provider_gemini() -> None:
    adapter = HttpxEmailAnalyzerAdapter()
    provider = adapter.get_provider(EmailAnalyzerPortProviderEnum.GEMINI_2_5_FLASH, "key")
    assert isinstance(provider, HttpxGeminiEmailAnalyzerPortProvider)
