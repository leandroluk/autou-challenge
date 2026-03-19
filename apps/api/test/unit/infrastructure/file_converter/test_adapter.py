from unittest.mock import MagicMock, patch

import pytest
from src.infrastructure.file_converter.fitz.adapter import FileConverterAdapter


@pytest.mark.asyncio
async def test_convert_txt_file() -> None:
    adapter = FileConverterAdapter()
    pages, mime = await adapter.convert("doc.txt", b"my content")
    assert mime == "text/plain"
    assert pages == ["my content"]


@pytest.mark.asyncio
async def test_convert_fallback_file() -> None:
    adapter = FileConverterAdapter()
    pages, mime = await adapter.convert("doc.csv", b"1,2,3")
    assert mime == "text/plain"
    assert pages == ["1,2,3"]


@pytest.mark.asyncio
@patch("src.infrastructure.file_converter.fitz.adapter.fitz.open")
async def test_convert_pdf_file(mock_fitz_open: MagicMock) -> None:
    mock_doc = MagicMock()
    mock_page = MagicMock()
    mock_pixmap = MagicMock()

    # setup mock tobytes
    mock_pixmap.tobytes.return_value = b"pngdata"
    mock_page.get_pixmap.return_value = mock_pixmap

    # make doc acts like a list/iterator of pages
    mock_doc.__enter__.return_value = [mock_page]
    mock_fitz_open.return_value = mock_doc

    adapter = FileConverterAdapter()
    pages, mime = await adapter.convert("doc.pdf", b"fake_pdf_content")

    assert mime == "image/png"
    assert pages == ["cG5nZGF0YQ=="]  # base64 of 'pngdata'
    mock_fitz_open.assert_called_once_with(stream=b"fake_pdf_content", filetype="pdf")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ext, expected_mime",
    [
        ("png", "image/png"),
        ("jpg", "image/jpg"),
        ("jpeg", "image/jpeg"),
    ],
)
async def test_convert_image_files(ext: str, expected_mime: str) -> None:
    adapter = FileConverterAdapter()
    content = b"fake_image_binary"
    expected_b64 = "ZmFrZV9pbWFnZV9iaW5hcnk="

    pages, mime = await adapter.convert(f"file.{ext}", content)

    assert mime == expected_mime
    assert pages == [expected_b64]
