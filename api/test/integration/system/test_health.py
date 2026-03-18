import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_health_success(http_client: AsyncClient):
    response = await http_client.get("/api/v1/system/health")

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "uptime" in data
