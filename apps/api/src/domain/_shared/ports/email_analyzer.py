from enum import Enum
from typing import Protocol

from src.domain.email.enums import CategoryEnum


class EmailAnalyzerPortProviderEnum(Enum):
    """
    LLM providers for email analysis.
    """

    GEMINI_2_5_FLASH = "gemini:2.5-flash"
    ANTHROPIC_CLAUDE_SONNET_4_5 = "anthropic:claude-sonnet-4.5"
    OPENAI_GPT_4O_MINI = "openai:gpt-4o-mini"


class EmailAnalyzerPortProvider(Protocol):
    """
    Port for analyzing an email.
    """

    async def analyze_text(self, text: str) -> tuple[CategoryEnum, str]: ...
    async def analyze_file(self, pages_b64: list[str], mime_type: str) -> tuple[CategoryEnum, str]: ...


class EmailAnalyzerPort(Protocol):
    """
    Port for email analysis.
    """

    def get_provider(self, provider: EmailAnalyzerPortProviderEnum, api_key: str) -> EmailAnalyzerPortProvider: ...
