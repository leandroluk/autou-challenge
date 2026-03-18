import json
import re
from typing import Any

import httpx

from src.domain._shared.ports.email_analyzer import EmailAnalyzerPortProvider
from src.domain.email.enums import CategoryEnum
from src.infrastructure.email_analyzer._prompt import EMAIL_ANALYZER_SYSTEM_PROMPT


class GeminiEmailAnalyzerPortProvider(EmailAnalyzerPortProvider):
    def __init__(self, api_key: str, model: str) -> None:
        self._api_key = api_key
        self._model = model

    def _url(self) -> str:
        return f"https://generativelanguage.googleapis.com/v1beta/models/{self._model}:generateContent"

    async def analyze_text(self, text: str) -> tuple[CategoryEnum, str]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self._url(),
                    params={"key": self._api_key},
                    headers={"Content-Type": "application/json"},
                    json={
                        "system_instruction": {"parts": [{"text": EMAIL_ANALYZER_SYSTEM_PROMPT}]},
                        "contents": [{"parts": [{"text": text[:3000]}]}],
                    },
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP {e.response.status_code} {e.response.text}") from e
        except httpx.RequestError as e:
            raise Exception(f"Request failed: {e}") from e
        raw = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return self._parse(raw)

    async def analyze_file(self, pages_b64: list[str], mime_type: str) -> tuple[CategoryEnum, str]:
        parts: list[dict[str, Any]] = [{"text": EMAIL_ANALYZER_SYSTEM_PROMPT}]
        for page in pages_b64:
            parts.append({"inline_data": {"mime_type": mime_type, "data": page}})
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self._url(),
                    params={"key": self._api_key},
                    headers={"Content-Type": "application/json"},
                    json={"contents": [{"parts": parts}]},
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP {e.response.status_code} {e.response.text}") from e
        except httpx.RequestError as e:
            raise Exception(f"Request failed: {e}") from e
        raw = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return self._parse(raw)

    def _parse(self, raw: str) -> tuple[CategoryEnum, str]:
        raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
        raw = re.sub(r"\s*```$", "", raw)
        try:
            data = json.loads(raw)
            return (CategoryEnum(data["category"]), data["suggested_reply"])
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise Exception(f"Unexpected model output: {e}") from e
