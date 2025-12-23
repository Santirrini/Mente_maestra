import pytest
from unittest.mock import AsyncMock, patch
from synapse.core.nodes.ollama_node import OllamaNode

@pytest.mark.asyncio
async def test_ollama_node_generate():
    """Verify that OllamaNode can send a prompt and receive a response."""
    # Mock the AsyncClient of ollama
    with patch("ollama.AsyncClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.generate = AsyncMock(return_value={
            "response": "This is a simulated response from Ollama."
        })
        
        node = OllamaNode(model="llama3")
        response = await node.generate("Tell me about synapse.")
        
        assert "simulated" in response.lower()
        mock_instance.generate.assert_called_once()
