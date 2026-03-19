import json
import re
from typing import Any

import httpx

from src.domain._shared.ports.email_analyzer import EmailAnalyzerPortProvider
from src.domain.email.enums import CategoryEnum
from src.infrastructure.email_analyzer.httpx._prompt import EMAIL_ANALYZER_SYSTEM_PROMPT


class HttpxOpenAIEmailAnalyzerPortProvider(EmailAnalyzerPortProvider):
    def __init__(self, api_key: str, model: str) -> None:
        self._api_key = api_key
        self._model = model

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"}

    async def analyze_text(self, text: str) -> tuple[CategoryEnum, str]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=self._headers(),
                    json={
                        "model": self._model,
                        "messages": [
                            {"role": "system", "content": EMAIL_ANALYZER_SYSTEM_PROMPT},
                            {"role": "user", "content": text[:3000]},
                        ],
                        "max_tokens": 600,
                    },
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP {e.response.status_code} {e.response.text}") from e
        except httpx.RequestError as e:
            raise Exception(f"Request failed: {e}") from e
        return self._parse(response.json()["choices"][0]["message"]["content"])

    async def analyze_file(self, pages_b64: list[str], mime_type: str) -> tuple[CategoryEnum, str]:
        content: list[dict[str, Any]] = [{"type": "text", "text": EMAIL_ANALYZER_SYSTEM_PROMPT}]
        for page in pages_b64:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{page}", "detail": "auto"},
                }
            )
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=self._headers(),
                    json={
                        "model": self._model,
                        "messages": [{"role": "user", "content": content}],
                        "max_tokens": 600,
                    },
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP {e.response.status_code} {e.response.text}") from e
        except httpx.RequestError as e:
            raise Exception(f"Request failed: {e}") from e
        return self._parse(response.json()["choices"][0]["message"]["content"])

    def _parse(self, raw: str) -> tuple[CategoryEnum, str]:
        raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
        raw = re.sub(r"\s*```$", "", raw)
        try:
            data = json.loads(raw)
            return (CategoryEnum(data["category"]), data["reply"])
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise Exception(f"Unexpected model output: {e}") from e
