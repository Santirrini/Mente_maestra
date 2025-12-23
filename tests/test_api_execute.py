import pytest
from httpx import AsyncClient, ASGITransport
from synapse.api.main import app

@pytest.mark.asyncio
async def test_execute_command():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/execute", json={"command": "test command"})
    
    assert response.status_code == 202
    assert response.json()["status"] == "started"
    assert "task_id" in response.json()
