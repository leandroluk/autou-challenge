class EmailConversionError(Exception):
    def __init__(self, filename: str) -> None:
        super().__init__(f"Could not convert '{filename}' as text.")


class EmailAnalyzerError(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(f"Analyzer failed: {detail}")
