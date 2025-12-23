import pytest
from pydantic import ValidationError
from synapse.core.models import AgentContribution, AgentPhase, SynapseState, MultimodalInput

def test_agent_contribution_validation():
    """Verify AgentContribution validation logic."""
    # Valid input
    valid_data = {
        "agent_id": "vision_1",
        "timestamp": 123456789.0,
        "content": "A cat sitting on a mat",
        "metadata": {"confidence": 0.9}
    }
    contribution = AgentContribution(**valid_data)
    assert contribution.agent_id == "vision_1"

    # Invalid input (missing field)
    invalid_data = {
        "agent_id": "vision_1",
        # timestamp missing
        "content": "A cat"
    }
    with pytest.raises(ValidationError):
        AgentContribution(**invalid_data)

def test_multimodal_input_validation():
    """Verify MultimodalInput validation logic."""
    # Valid image input
    valid_image = {
        "type": "IMAGE",
        "source_url": "/tmp/image.jpg",
        "resolution": {"width": 1920, "height": 1080}
    }
    input_obj = MultimodalInput(**valid_image)
    assert input_obj.type == "IMAGE"

    # Invalid type
    invalid_type = {
        "type": "SMELL", # Not supported
        "source_url": "/tmp/smell.json"
    }
    with pytest.raises(ValidationError):
        MultimodalInput(**invalid_type)

def test_synapse_state_default():
    """Verify SynapseState defaults."""
    state = SynapseState(
        current_phase=AgentPhase.IDLE,
        blackboard={"contributions": [], "is_compliant": False, "logs": []}
    )
    assert state.current_phase == AgentPhase.IDLE
    assert len(state.blackboard.contributions) == 0
