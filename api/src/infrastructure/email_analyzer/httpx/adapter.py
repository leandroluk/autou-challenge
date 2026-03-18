from src.application._shared.container import injectable
from src.domain._shared.ports.email_analyzer import (
    EmailAnalyzerPort,
    EmailAnalyzerPortProvider,
    EmailAnalyzerPortProviderEnum,
)
from src.infrastructure.email_analyzer.httpx.anthropic_provider import HttpxAnthropicEmailAnalyzerPortProvider
from src.infrastructure.email_analyzer.httpx.gemini_provider import HttpxGeminiEmailAnalyzerPortProvider
from src.infrastructure.email_analyzer.httpx.openai_provider import HttpxOpenAIEmailAnalyzerPortProvider

_PROVIDER_MODELS: dict[EmailAnalyzerPortProviderEnum, tuple[type, str]] = {
    EmailAnalyzerPortProviderEnum.ANTHROPIC_CLAUDE_SONNET_4_5: (
        HttpxAnthropicEmailAnalyzerPortProvider,
        "claude-sonnet-4-5",
    ),
    EmailAnalyzerPortProviderEnum.OPENAI_GPT_4O_MINI: (
        HttpxOpenAIEmailAnalyzerPortProvider,
        "gpt-4o-mini",
    ),
    EmailAnalyzerPortProviderEnum.GEMINI_2_5_FLASH: (
        HttpxGeminiEmailAnalyzerPortProvider,
        "gemini-2.5-flash",
    ),
}


@injectable(as_type=EmailAnalyzerPort)
class HttpxEmailAnalyzerAdapter(EmailAnalyzerPort):
    def get_provider(self, provider: EmailAnalyzerPortProviderEnum, api_key: str) -> EmailAnalyzerPortProvider:
        adapter_cls, model = _PROVIDER_MODELS[provider]
        return adapter_cls(api_key=api_key, model=model)
