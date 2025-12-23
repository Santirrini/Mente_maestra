import pytest
from synapse.core.orchestrator import SynapseOrchestrator
from synapse.core.models import AgentPhase

@pytest.mark.asyncio
async def test_orchestrator_flow():
    """Verify that the orchestrator can execute a basic flow."""
    orchestrator = SynapseOrchestrator()
    
    # Initial input
    initial_state = {
        "input": "Analyze this clinical data.",
        "analysis": "",
        "is_valid": False,
        "iterations": 0
    }
    
    # Run the graph
    final_state = await orchestrator.run(initial_state)
    
    assert final_state["iterations"] > 0
    assert "analyzed" in final_state["analysis"].lower()
    assert final_state["is_valid"] is True
