from src.domain._shared.ports.email_analyzer import (
    EmailAnalyzerPort,
    EmailAnalyzerPortProvider,
    EmailAnalyzerPortProviderEnum,
)
from src.domain.email.enums import CategoryEnum


class FakeEmailAnalyzerPortProvider(EmailAnalyzerPortProvider):
    async def analyze_text(self, text: str) -> tuple[CategoryEnum, str]:
        return CategoryEnum.PRODUCTIVE, "Fake reply"

    async def analyze_file(self, pages_b64: list[str], mime_type: str) -> tuple[CategoryEnum, str]:
        return CategoryEnum.UNPRODUCTIVE, "Fake reply"


class FakeEmailAnalyzerAdapter(EmailAnalyzerPort):
    def get_provider(self, provider: EmailAnalyzerPortProviderEnum, api_key: str) -> EmailAnalyzerPortProvider:
        return FakeEmailAnalyzerPortProvider()
