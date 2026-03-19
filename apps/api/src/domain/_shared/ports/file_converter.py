from typing import Protocol


class FileConverterPort(Protocol):
    async def convert(self, filename: str, content: bytes) -> tuple[list[str], str]: ...
