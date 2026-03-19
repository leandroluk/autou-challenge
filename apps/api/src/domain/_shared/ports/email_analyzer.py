from enum import Enum
from typing import Protocol

from src.domain.email.enums import CategoryEnum


class EmailAnalyzerPortProviderEnum(Enum):
    GEMINI_2_5_FLASH = "gemini:2.5-flash"
    ANTHROPIC_CLAUDE_SONNET_4_5 = "anthropic:claude-sonnet-4.5"
    OPENAI_GPT_4O_MINI = "openai:gpt-4o-mini"


class EmailAnalyzerPortProvider(Protocol):
    async def analyze_text(self, text: str) -> tuple[CategoryEnum, str]: ...
    async def analyze_file(self, pages_b64: list[str], mime_type: str) -> tuple[CategoryEnum, str]: ...


class EmailAnalyzerPort(Protocol):
    def get_provider(self, provider: EmailAnalyzerPortProviderEnum, api_key: str) -> EmailAnalyzerPortProvider: ...
