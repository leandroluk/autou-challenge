import base64
from typing import Any, Protocol, cast

import fitz

from src.application._shared.container import injectable
from src.domain._shared.ports.file_converter import FileConverterPort


class _FitzPixmapProtocol(Protocol):
    def tobytes(self, output: str) -> bytes: ...


class _FitzPageProtocol(Protocol):
    def get_pixmap(self, *, matrix: Any) -> _FitzPixmapProtocol: ...


@injectable(as_type=FileConverterPort)
class FileConverterAdapter(FileConverterPort):
    """
    Adapter for converting files using Fitz.
    """

    def _pdf_to_pages(self, content: bytes) -> list[str]:
        """
        Convert PDF content to a list of base64-encoded PNG images.
        """
        pages: list[str] = []
        with fitz.open(stream=content, filetype="pdf") as doc:
            for page in doc:
                pix = cast(_FitzPageProtocol, page).get_pixmap(matrix=fitz.Matrix(2, 2))
                pages.append(base64.b64encode(pix.tobytes("png")).decode())
        return pages

    async def convert(self, filename: str, content: bytes) -> tuple[list[str], str]:
        """
        Convert a file to a list of base64-encoded pages and its MIME type.
        """
        ext = filename.split(".")[-1].lower() if "." in filename else ""

        if ext == "txt":
            return [content.decode("utf-8", errors="replace")], "text/plain"
        if ext == "pdf":
            return self._pdf_to_pages(content), "image/png"

        mime_type = f"image/{ext}" if ext in ["png", "jpg", "jpeg"] else "text/plain"
        if mime_type == "text/plain":
            return [content.decode("utf-8", errors="replace")], mime_type
        return [base64.b64encode(content).decode()], mime_type
