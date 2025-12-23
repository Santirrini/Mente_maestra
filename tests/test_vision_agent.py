import pytest
from unittest.mock import AsyncMock, patch
from synapse.core.agents.vision_agent import VisionAgent
from synapse.core.models import AgentContribution

@pytest.mark.asyncio
async def test_vision_agent_analyze():
    """Verify that VisionAgent can analyze an image."""
    # Patch where it is looked up
    with patch("synapse.core.agents.vision_agent.OllamaNode") as MockOllamaNode:
        mock_node_instance = MockOllamaNode.return_value
        mock_node_instance.generate = AsyncMock(return_value="A cute cat.")
        mock_node_instance.model = "llava" # Set the model attribute on the mock
        
        agent = VisionAgent(agent_id="vision_1", model="llava")
        
        # We assume the mock bypasses the file check because generate is mocked
        result = await agent.analyze("/tmp/cat.jpg")
        
        assert isinstance(result, AgentContribution)
        assert result.agent_id == "vision_1"
        assert result.content == "A cute cat."
        mock_node_instance.generate.assert_called_once()