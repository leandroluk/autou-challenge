from fastapi import UploadFile


class EmailAnalyzeRequestBody:
    provider: str
    api_key: str
    file: UploadFile | None = None
    text: str | None = None
