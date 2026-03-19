import pytest
from httpx import AsyncClient

from src.domain._shared.ports.email_analyzer import EmailAnalyzerPortProviderEnum


@pytest.mark.asyncio
async def test_post_email_analyze_success(http_client: AsyncClient):
    data = {
        "provider": EmailAnalyzerPortProviderEnum.ANTHROPIC_CLAUDE_SONNET_4_5.value,
        "api_key": "[ENCRYPTION_KEY]",
        "text": "optional text content",
    }

    response = await http_client.post(
        "/api/v1/email/analyze",
        data=data,
    )

    assert response.status_code == 200

    res_data = response.json()
    assert res_data["category"] == "Productive"
    assert "reply" in res_data
