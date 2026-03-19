from typing import Protocol


class FileConverterPort(Protocol):
    """
    Port for converting files.
    """

    async def convert(self, filename: str, content: bytes) -> tuple[list[str], str]: ...
