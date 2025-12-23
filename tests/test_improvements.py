import pytest
import asyncio
from synapse.core.blackboard import Blackboard
from synapse.core.models import MultimodalInput

@pytest.mark.asyncio
async def test_blackboard_ping():
    """Verify that the ping method works."""
    blackboard = Blackboard(redis_url="redis://localhost:6379/0")
    is_alive = await blackboard.ping()
    assert is_alive is True
    await blackboard.close()

@pytest.mark.asyncio
async def test_blackboard_state_ttl():
    """Verify that state storage respects TTL."""
    blackboard = Blackboard(redis_url="redis://localhost:6379/0")
    key = "temp_state"
    value = {"data": "gone soon"}
    
    # Set with 1 second TTL
    await blackboard.set_state(key, value, ttl=1)
    
    # Should exist immediately
    exists = await blackboard.get_state(key)
    assert exists == value
    
    # Wait for expiration
    await asyncio.sleep(1.2)
    
    # Should be gone
    expired = await blackboard.get_state(key)
    assert expired is None
    
    await blackboard.close()

def test_multimodal_input_scalability():
    """Verify that new types are supported in MultimodalInput."""
    text_input = MultimodalInput(type='TEXT', source_url="memory://txt1")
    sensory_input = MultimodalInput(type='SENSORY', source_url="sensor://temp1")
    
    assert text_input.type == 'TEXT'
    assert sensory_input.type == 'SENSORY'
