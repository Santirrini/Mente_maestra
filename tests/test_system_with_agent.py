import pytest
import asyncio
import logging
from synapse.core.blackboard import Blackboard
from synapse.core.agents.guardian_agent import GuardianAgent
from synapse.core.agents.tester_agent import TesterAgent
from synapse.core.models import AgentContribution

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test_system")

@pytest.mark.asyncio
async def test_agent_interaction_flow():
    """
    Verifies that the TesterAgent can interact with the system 
    and that the GuardianAgent correctly validates messages.
    """
    
    # 1. Setup
    blackboard = Blackboard()
    await blackboard.start()
    
    guardian = GuardianAgent("guardian-primary")
    tester = TesterAgent("tester-alpha")
    
    # Validation results capture
    validation_events = []

    async def on_validation_result(data: dict):
        logger.info(f"Received validation result: {data}")
        validation_events.append(data)

    # Subscribe to validation results channel (assuming Guardian publishes here upon check)
    # Note: In the current guardian_agent.py, we saw it returns a value but doesn't explicitly publish 
    # to a channel in the code we viewed. We might need to wire a listener or wrapper to test this integration.
    # checking guardian_agent.py again... 
    # Wait, the reviewed guardian_agent.py just had a `validate` method needed manual invocation or 
    # integration into an orchestrator. 
    
    # Let's create a mockup orchestrator behavior here to bridge them, 
    # OR we modify this test to simulate the Orchestrator's job:
    # Listening to 'synapse:input:text' -> sending to Guardian -> publishing result.
    
    async def orchestrator_logic(data: dict):
        # Deserializing naive check
        try:
            # Reconstruct model from dict data
            if "agent_id" in data:
                 # It's a contribution
                 contrib = AgentContribution(**data)
                 # Validate
                 result = await guardian.validate(contrib)
                 
                 # Publish outcome (This is what a real Orchestrator would do)
                 await blackboard.publish("synapse:agent:guardian:result", result.model_dump())
        except Exception as e:
            logger.error(f"Orchestrator error: {e}")

    await blackboard.subscribe("synapse:input:text", orchestrator_logic)
    await blackboard.subscribe("synapse:agent:guardian:result", on_validation_result)

    # 2. Execution - Safe Scenario
    logger.info("--- Running Safe Scenario ---")
    await tester.scenario_safe_contribution(blackboard)
    
    # Allow async propagation
    await asyncio.sleep(1)
    
    # Assertions for Safe
    safe_results = [e for e in validation_events if e['is_compliant'] == True]
    assert len(safe_results) >= 1, "Expected at least one compliant result"

    # Clear for next
    validation_events.clear()

    # 3. Execution - Restricted Scenario
    logger.info("--- Running Restricted Scenario ---")
    await tester.scenario_restricted_contribution(blackboard)
    
    await asyncio.sleep(1)

    # Assertions for Restricted
    restricted_results = [e for e in validation_events if e['is_compliant'] == False]
    assert len(restricted_results) >= 1, "Expected at least one non-compliant result"
    assert "CONFIDENTIAL" in restricted_results[0]['logs'][0], "Expected specific log message regarding 'CONFIDENTIAL'"

    # 4. Cleanup
    await blackboard.close()
