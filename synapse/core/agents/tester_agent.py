import asyncio
import uuid
import time
from typing import Optional
from synapse.core.models import AgentContribution
from synapse.core.blackboard import Blackboard
import logging

logger = logging.getLogger(__name__)

class TesterAgent:
    def __init__(self, agent_id: Optional[str] = None):
        self.agent_id = agent_id or f"tester-{uuid.uuid4().hex[:8]}"
    
    def _create_contribution(self, content: str) -> AgentContribution:
        return AgentContribution(
            agent_id=self.agent_id,
            timestamp=time.time(),
            content=content,
            metadata={"type": "test_scenario"}
        )

    async def scenario_safe_contribution(self, blackboard: Blackboard):
        """Publishes a safe, valid message."""
        content = "System status check: All services operational."
        contribution = self._create_contribution(content)
        await blackboard.publish("synapse:contributions", contribution)
        logger.info(f"[{self.agent_id}] Published SAFE contribution.")

    async def scenario_restricted_contribution(self, blackboard: Blackboard):
        """Publishes a message containing restricted keywords."""
        content = "This includes CONFIDENTIAL data that should be flagged."
        contribution = self._create_contribution(content)
        await blackboard.publish("synapse:contributions", contribution)
        logger.info(f"[{self.agent_id}] Published RESTRICTED contribution.")

    async def run_suite(self, blackboard: Blackboard):
        """Runs a sequence of test scenarios."""
        logger.info(f"Starting test suite for {self.agent_id}")
        
        # Scenario 1: Safe
        await self.scenario_safe_contribution(blackboard)
        await asyncio.sleep(0.5) # Wait for processing
        
        # Scenario 2: Restricted
        await self.scenario_restricted_contribution(blackboard)
        await asyncio.sleep(0.5) 
        
        logger.info("Test suite completed.")
