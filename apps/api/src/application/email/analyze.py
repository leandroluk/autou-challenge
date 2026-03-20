from pydantic import BaseModel, Field, model_validator

from src.application._shared.container import injectable
from src.domain._shared.ports.email_analyzer import (
    EmailAnalyzerPort,
    EmailAnalyzerPortProvider,
    EmailAnalyzerPortProviderEnum,
)
from src.domain._shared.ports.file_converter import FileConverterPort
from src.domain.email.enums import CategoryEnum
from src.domain.email.errors import EmailAnalyzerError, EmailConversionError


class EmailAnalyzeQuery(BaseModel):
    """
    Query for analyzing an email.
    """

    provider: EmailAnalyzerPortProviderEnum = Field(
        description="LLM provider",
        examples=[EmailAnalyzerPortProviderEnum.OPENAI_GPT_4O_MINI],
    )
    api_key: str = Field(
        description="LLM API key",
        examples=["sk-..."],
        min_length=10,
    )
    file: tuple[str, bytes] | None = Field(
        description="File name and content in bytes",
        examples=[("email.pdf", b"...")],
        default=None,
    )
    text: str | None = Field(
        description="Text content",
        examples=["..."],
        default=None,
    )

    @model_validator(mode="after")
    def _validate_mutually_exclusive(self) -> "EmailAnalyzeQuery":
        if self.file and self.text:
            raise ValueError("'file' and 'text' are mutually exclusive")
        if not self.file and not self.text:
            raise ValueError("Either 'file' or 'text' must be provided")
        return self


class EmailAnalyzerResult(BaseModel):
    """
    Result of analyzing an email.
    """

    category: str = Field(
        description="Category of the email",
        examples=[key.value for key in CategoryEnum],
        json_schema_extra={"enum": [e.value for e in CategoryEnum]},
    )
    reply: str = Field(
        description="Suggested reply to the email",
        examples=["Thank you for your email. I will get back to you as soon as possible."],
    )


@injectable
class EmailAnalyzeHandler:
    """
    Handler for analyzing an email.
    """

    _email_analyzer: EmailAnalyzerPort
    _file_converter: FileConverterPort

    def __init__(self, email_analyzer: EmailAnalyzerPort, file_converter: FileConverterPort):
        self._email_analyzer = email_analyzer
        self._file_converter = file_converter

    async def _convert_file(
        self,
        file: tuple[str, bytes],
        analyzer_provider: EmailAnalyzerPortProvider,
    ) -> tuple[CategoryEnum, str]:
        filename, content = file
        try:
            pages_data, mime_type = await self._file_converter.convert(filename, content)
            if mime_type == "text/plain":
                return await analyzer_provider.analyze_text("\n".join(pages_data))
            return await analyzer_provider.analyze_file(pages_data, mime_type)
        except Exception as e:
            raise EmailConversionError(filename) from e

    async def execute(self, command: EmailAnalyzeQuery) -> EmailAnalyzerResult:
        analyzer_provider = self._email_analyzer.get_provider(command.provider, command.api_key)
        try:
            if command.file:
                category, reply = await self._convert_file(command.file, analyzer_provider)
            else:
                category, reply = await analyzer_provider.analyze_text(command.text or "")
        except EmailConversionError:
            raise
        except Exception as e:
            raise EmailAnalyzerError(str(e))
        return EmailAnalyzerResult(category=category.value, reply=reply)
