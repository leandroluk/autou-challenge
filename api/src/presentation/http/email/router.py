from typing import Annotated, cast

from fastapi import APIRouter, Depends, Request, UploadFile

from src.application._shared.container import resolve
from src.application.email.analyze import EmailAnalyzeHandler, EmailAnalyzeQuery
from src.domain._shared.ports.email_analyzer import EmailAnalyzerPortProviderEnum
from src.domain.email.errors import EmailAnalyzerError
from src.presentation.http._shared.decorators import map_domain_error
from src.presentation.http.email.dtos.analyze import EmailAnalyzeRequestBody, EmailAnalyzeResponse

router = APIRouter(prefix="/email", tags=["Email"])

schema = EmailAnalyzeRequestBody.model_json_schema()


@router.post(
    "/analyze",
    response_model=EmailAnalyzeResponse,
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {"multipart/form-data": {"schema": EmailAnalyzeRequestBody.model_json_schema()}},
        }
    },
)
@map_domain_error(
    (EmailAnalyzerError, 502),
)
async def analyze(
    handler: Annotated[EmailAnalyzeHandler, Depends(lambda: resolve(EmailAnalyzeHandler))],
    request: Request,
):
    form = await request.form()
    file = cast(UploadFile | None, form.get("file"))
    file_data = (file.filename, await file.read()) if file and file.filename else None
    command = EmailAnalyzeQuery(
        provider=EmailAnalyzerPortProviderEnum(cast(str, form["provider"])),
        api_key=cast(str, form.get("api_key")),
        file=file_data,
        text=cast(str | None, form.get("text")),
    )
    return await handler.execute(command)
