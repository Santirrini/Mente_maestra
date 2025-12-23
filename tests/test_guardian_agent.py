import pytest
from synapse.core.agents.guardian_agent import GuardianAgent
from synapse.core.models import AgentContribution

@pytest.mark.asyncio
async def test_guardian_agent_validate_success():
    """Verify GuardianAgent approves valid content."""
    agent = GuardianAgent(agent_id="guardian_1")
    
    contribution = AgentContribution(
        agent_id="vision_1",
        timestamp=123.0,
        content="A detailed description of a benign object."
    )
    
    result = await agent.validate(contribution)
    assert result.is_compliant is True
    assert len(result.logs) == 0

@pytest.mark.asyncio
async def test_guardian_agent_validate_failure():
    """Verify GuardianAgent rejects invalid content."""
    agent = GuardianAgent(agent_id="guardian_1")
    
    # Simulate a policy violation (e.g., contains PII or restricted keywords)
    # For this test, let's assume 'CONFIDENTIAL' is a restricted keyword.
    contribution = AgentContribution(
        agent_id="vision_1",
        timestamp=123.0,
        content="This contains CONFIDENTIAL information."
    )
    
    result = await agent.validate(contribution)
    assert result.is_compliant is False
    assert "Violation detected" in result.logs[0]
