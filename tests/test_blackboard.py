import pytest
import asyncio
import json
from synapse.core.blackboard import Blackboard

@pytest.mark.asyncio
async def test_blackboard_publish_subscribe():
    """Verify that we can publish and receive messages on the blackboard."""
    blackboard = Blackboard(redis_url="redis://localhost:6379/0")
    
    received_messages = []

    async def callback(message):
        received_messages.append(message)

    await blackboard.subscribe("test_channel", callback)
    
    test_data = {"agent_id": "vision_1", "content": "detected cat"}
    await blackboard.publish("test_channel", test_data)

    # Allow some time for the message to be processed
    await asyncio.sleep(0.1)

    assert len(received_messages) == 1
    assert received_messages[0] == test_data

    await blackboard.close()

@pytest.mark.asyncio
async def test_blackboard_state_storage():
    """Verify that we can store and retrieve state (memory)."""
    blackboard = Blackboard(redis_url="redis://localhost:6379/0")
    
    key = "agent:vision_1:last_seen"
    value = {"object": "cat", "timestamp": 123456789}
    
    await blackboard.set_state(key, value)
    retrieved = await blackboard.get_state(key)
    
    assert retrieved == value
    
    await blackboard.close()
