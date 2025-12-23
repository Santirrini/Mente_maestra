import pytest
import asyncio
import time
from synapse.core.blackboard import Blackboard
from synapse.core.models import AgentContribution, MultimodalInput

@pytest.mark.asyncio
async def test_blackboard_multi_callback():
    """Verify that multiple callbacks can subscribe to the same channel."""
    bb = Blackboard()
    results = []

    async def cb1(data): results.append(("cb1", data))
    async def cb2(data): results.append(("cb2", data))

    await bb.subscribe("multi_channel", cb1)
    await bb.subscribe("multi_channel", cb2)

    msg = {"test": "data"}
    await bb.publish("multi_channel", msg)
    
    await asyncio.sleep(0.2)
    assert len(results) == 2
    assert any(r[0] == "cb1" for r in results)
    assert any(r[0] == "cb2" for r in results)
    await bb.close()

@pytest.mark.asyncio
async def test_blackboard_pydantic_publish():
    """Verify that we can publish Pydantic models directly."""
    bb = Blackboard()
    received = []

    async def cb(data): received.append(data)
    await bb.subscribe("pydantic_channel", cb)

    contribution = AgentContribution(
        agent_id="test_agent",
        timestamp=time.time(),
        content="Testing Pydantic"
    )

    await bb.publish("pydantic_channel", contribution)
    await asyncio.sleep(0.2)

    assert len(received) == 1
    assert received[0]["agent_id"] == "test_agent"
    assert received[0]["content"] == "Testing Pydantic"
    await bb.close()

@pytest.mark.asyncio
async def test_blackboard_callback_resilience():
    """Verify that a failing callback doesn't stop others."""
    bb = Blackboard()
    results = []

    async def failing_cb(data): 
        raise ValueError("Boom!")
    
    async def healthy_cb(data): 
        results.append(data)

    await bb.subscribe("resilience_channel", failing_cb)
    await bb.subscribe("resilience_channel", healthy_cb)

    await bb.publish("resilience_channel", {"status": "ok"})
    await asyncio.sleep(0.2)

    assert len(results) == 1
    assert results[0]["status"] == "ok"
    await bb.close()

@pytest.mark.asyncio
async def test_model_validation():
    """Verify that MultimodalInput validates source_url."""
    # Valid URL
    input_valid = MultimodalInput(type="IMAGE", source_url="https://example.com/img.jpg")
    assert input_valid.source_url == "https://example.com/img.jpg"

    # Invalid URL
    with pytest.raises(ValueError, match="source_url must start with"):
        MultimodalInput(type="IMAGE", source_url="invalid_url")
