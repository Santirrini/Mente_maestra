import pytest
from unittest.mock import AsyncMock, patch
from synapse.core.orchestrator import SynapseOrchestrator
from synapse.core.models import AgentPhase

@pytest.mark.asyncio
async def test_orchestrator_flow():
    """Verify that the orchestrator can execute a basic flow."""
    # Mock dependencies to avoid real API calls and file checks
    with patch("synapse.core.agents.vision_agent.OllamaNode") as MockOllamaNode:
        mock_node = MockOllamaNode.return_value
        mock_node.generate = AsyncMock(return_value="Analyzed content")
        mock_node.model = "llava"

        orchestrator = SynapseOrchestrator()
        
        # Initial input - use a dummy path, the mock handles it
        initial_state = {
            "input": "/tmp/dummy.jpg",
            "analysis": "",
            "is_valid": False,
            "iterations": 0
        }
        
        # Run the graph
        final_state = await orchestrator.run(initial_state)
        
        assert final_state["iterations"] > 0
        assert "Analyzed content" in final_state["analysis"]
        # Guardian should approve if no restricted keywords are found
        assert final_state["is_valid"] is True