import pytest
import asyncio
import logging
from synapse.core.blackboard import Blackboard
from synapse.core.agents.refiner_agent import RefinerAgent
from synapse.core.models import AgentContribution

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test_refiner")

@pytest.mark.asyncio
async def test_refiner_agent_flow():
    """
    Verifies that the RefinerAgent correctly processes inputs and publishes refined outputs.
    Note: Requires Ollama running with llama3.2 model.
    """
    
    # 1. Setup
    blackboard = Blackboard()
    await blackboard.start()
    
    # Initialize agent (assuming llama3.2 is pulled)
    refiner = RefinerAgent()
    await refiner.start_listening(blackboard)
    
    refined_output = []

    async def on_refined_output(data: dict):
        logger.info(f"Received refined output: {data}")
        refined_output.append(data)

    await blackboard.subscribe("synapse:agent:refiner:output", on_refined_output)

    # 2. Execution - Messy Input
    raw_content = "uhm so yeah the system is like kinda slow maybe check the database metrics? thanks"
    test_contrib = AgentContribution(
        agent_id="user-input-test",
        timestamp=asyncio.get_event_loop().time(),
        content=raw_content
    )

    logger.info("Publishing raw input...")
    await blackboard.publish("synapse:input:text", test_contrib)
    
    # Allow time for LLM processing (might take a few seconds depending on hardware)
    # We use a longer timeout for LLM tasks
    for _ in range(30): # Up to 30 seconds
        if len(refined_output) > 0:
            break
        await asyncio.sleep(1)

    # 3. Assertions
    assert len(refined_output) == 1, "Should have received exactly one refined message"
    refined_msg = refined_output[0]
    assert refined_msg['metadata']['original_agent'] == "user-input-test"
    assert len(refined_msg['content']) > 0
    logger.info(f"Refined content: {refined_msg['content']}")

    # 4. Cleanup
    await blackboard.close()
