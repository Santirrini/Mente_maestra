import pytest
from unittest.mock import AsyncMock, patch
from synapse.core.orchestrator import SynapseOrchestrator

@pytest.mark.asyncio
async def test_full_orchestration_flow():
    """Verify the full flow: Vision -> Guardian."""
    
    # Mock dependencies
    with patch("synapse.core.agents.vision_agent.OllamaNode") as MockOllamaNode:
        mock_node = MockOllamaNode.return_value
        mock_node.model = "llava"
        # Simulate Vision Agent Output
        mock_node.generate = AsyncMock(return_value="A secure image description.")
        
        orchestrator = SynapseOrchestrator()
        
        initial_state = {
            "input": "/tmp/safe_image.jpg",
            "analysis": "",
            "is_valid": False,
            "iterations": 0
        }
        
        final_state = await orchestrator.run(initial_state)
        
        assert "secure image" in final_state["analysis"]
        assert final_state["is_valid"] is True

@pytest.mark.asyncio
async def test_full_orchestration_rejection():
    """Verify rejection flow."""
    
    with patch("synapse.core.agents.vision_agent.OllamaNode") as MockOllamaNode:
        mock_node = MockOllamaNode.return_value
        mock_node.model = "llava"
        # Simulate Restricted Output
        mock_node.generate = AsyncMock(return_value="This is CONFIDENTIAL data.")
        
        orchestrator = SynapseOrchestrator()
        
        initial_state = {
            "input": "/tmp/secret.jpg",
            "analysis": "",
            "is_valid": False,
            "iterations": 0
        }
        
        final_state = await orchestrator.run(initial_state)
        
        assert "CONFIDENTIAL" in final_state["analysis"]
        assert final_state["is_valid"] is False
