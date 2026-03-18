from src.application._shared.container import injectable
from src.domain._shared.ports.email_analyzer import (
    EmailAnalyzerPort,
    EmailAnalyzerPortProvider,
    EmailAnalyzerPortProviderEnum,
)
from src.infrastructure.email_analyzer.anthropic_provider import AnthropicEmailAnalyzerPortProvider
from src.infrastructure.email_analyzer.gemini_provider import GeminiEmailAnalyzerPortProvider
from src.infrastructure.email_analyzer.openai_provider import OpenAIEmailAnalyzerPortProvider

_PROVIDER_MODELS: dict[EmailAnalyzerPortProviderEnum, tuple[type, str]] = {
    EmailAnalyzerPortProviderEnum.ANTHROPIC_CLAUDE_SONNET_4_5: (
        AnthropicEmailAnalyzerPortProvider,
        "claude-sonnet-4-5",
    ),
    EmailAnalyzerPortProviderEnum.OPENAI_GPT_4O_MINI: (
        OpenAIEmailAnalyzerPortProvider,
        "gpt-4o-mini",
    ),
    EmailAnalyzerPortProviderEnum.GEMINI_2_5_FLASH: (
        GeminiEmailAnalyzerPortProvider,
        "gemini-2.5-flash",
    ),
}


@injectable(as_type=EmailAnalyzerPort)
class EmailAnalyzerAdapter(EmailAnalyzerPort):
    def get_provider(self, provider: EmailAnalyzerPortProviderEnum, api_key: str) -> EmailAnalyzerPortProvider:
        adapter_cls, model = _PROVIDER_MODELS[provider]
        return adapter_cls(api_key=api_key, model=model)
