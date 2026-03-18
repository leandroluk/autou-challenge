from fastapi import UploadFile
from pydantic import BaseModel, Field

from src.application.email.analyze import EmailAnalyzerResult
from src.domain._shared.ports.email_analyzer import EmailAnalyzerPortProviderEnum


class EmailAnalyzeRequestBody(BaseModel):
    provider: str = Field(
        description="Provider used to analyze email",
        json_schema_extra={"enum": [e.value for e in EmailAnalyzerPortProviderEnum]},
    )
    api_key: str = Field(description="Provider API key")
    file: UploadFile | None = Field(
        None,
        description="Email file (.pdf)",
        json_schema_extra={"format": "binary"},
    )
    text: str | None = Field(
        None,
        description="Email text",
        examples=["Subject: Hello\n\nThis is a long email body content..."],
        json_schema_extra={"format": "textarea"},
    )


class EmailAnalyzeResponse(EmailAnalyzerResult): ...
