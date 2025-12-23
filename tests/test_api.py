import pytest
from httpx import ASGITransport, AsyncClient
from synapse.api.main import app
import asyncio

@pytest.mark.asyncio
async def test_read_health():
    """Verify health endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_get_state():
    """Verify we can get the current state."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/state")
    assert response.status_code == 200
    data = response.json()
    assert "current_phase" in data
    assert "blackboard" in data

@pytest.mark.asyncio
async def test_post_contribution():
    """Verify contribution posting."""
    contribution = {
        "agent_id": "test_agent",
        "timestamp": 123456789.0,
        "content": "Test content",
        "metadata": {}
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/contributions", json=contribution)
    assert response.status_code == 201
    assert response.json()["agent_id"] == "test_agent"
