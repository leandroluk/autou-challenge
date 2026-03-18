import json
import re
from typing import Any

import httpx

from src.domain._shared.ports.email_analyzer import EmailAnalyzerPortProvider
from src.domain.email.enums import CategoryEnum
from src.infrastructure.email_analyzer.httpx._prompt import EMAIL_ANALYZER_SYSTEM_PROMPT


class HttpxAnthropicEmailAnalyzerPortProvider(EmailAnalyzerPortProvider):
    def __init__(self, api_key: str, model: str) -> None:
        self._api_key = api_key
        self._model = model

    def _headers(self) -> dict[str, str]:
        return {
            "x-api-key": self._api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

    async def analyze_text(self, text: str) -> tuple[CategoryEnum, str]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers=self._headers(),
                    json={
                        "model": self._model,
                        "max_tokens": 600,
                        "system": EMAIL_ANALYZER_SYSTEM_PROMPT,
                        "messages": [{"role": "user", "content": text[:3000]}],
                    },
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP {e.response.status_code} {e.response.text}") from e
        except httpx.RequestError as e:
            raise Exception(f"Request failed: {e}") from e
        return self._parse(response.json()["content"][0]["text"])

    async def analyze_file(self, pages_b64: list[str], mime_type: str) -> tuple[CategoryEnum, str]:
        content: list[dict[str, Any]] = []
        for page in pages_b64:
            content.append(
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": mime_type, "data": page},
                }
            )
        content.append({"type": "text", "text": EMAIL_ANALYZER_SYSTEM_PROMPT})
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers=self._headers(),
                    json={
                        "model": self._model,
                        "max_tokens": 600,
                        "messages": [{"role": "user", "content": content}],
                    },
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP {e.response.status_code} {e.response.text}") from e
        except httpx.RequestError as e:
            raise Exception(f"Request failed: {e}") from e
        return self._parse(response.json()["content"][0]["text"])

    def _parse(self, raw: str) -> tuple[CategoryEnum, str]:
        raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
        raw = re.sub(r"\s*```$", "", raw)
        try:
            data = json.loads(raw)
            return (CategoryEnum(data["category"]), data["suggested_reply"])
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise Exception(f"Unexpected model output: {e}") from e
