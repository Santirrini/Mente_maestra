import asyncio
import time
import logging
from typing import Optional
from synapse.core.models import AgentContribution
from synapse.core.nodes.ollama_node import OllamaNode
from synapse.core.blackboard import Blackboard

logger = logging.getLogger(__name__)

class RefinerAgent:
    def __init__(self, agent_id: str = "refiner-agent", model: str = "llama3.2"):
        self.agent_id = agent_id
        self.node = OllamaNode(model=model)

    async def refine(self, contribution: AgentContribution) -> AgentContribution:
        """
        Uses Llama 3.2 to refine and summarize the content of a contribution.
        """
        prompt = (
            "You are a professional editor. Refine the following user input to make it clear, "
            "concise, and professional. Provide only the refined text.\n\n"
            f"Input: {contribution.content}"
        )
        
        try:
            refined_content = await self.node.generate(prompt=prompt)
            refined_content = refined_content.strip()
        except Exception as e:
            logger.error(f"Error during refinement with model {self.node.model}: {e}")
            refined_content = contribution.content # Fallback to original

        return AgentContribution(
            agent_id=self.agent_id,
            timestamp=time.time(),
            content=refined_content,
            metadata={
                "original_agent": contribution.agent_id,
                "model": self.node.model,
                "type": "REFINED"
            }
        )

    async def start_listening(self, blackboard: Blackboard):
        """
        Starts the agent's subscription to input channels.
        """
        async def on_new_input(data: dict):
            try:
                # Basic validation to ensure it's a contribution
                if "agent_id" in data and data["agent_id"] != self.agent_id:
                    contrib = AgentContribution(**data)
                    logger.info(f"[{self.agent_id}] Refining contribution from {contrib.agent_id}")
                    
                    refined = await self.refine(contrib)
                    # Publish to both specific channel and general contributions for UI
                    await blackboard.publish("synapse:agent:refiner:output", refined)
                    await blackboard.publish("synapse:contributions", refined)
                    logger.info(f"[{self.agent_id}] Published refined output.")
            except Exception as e:
                logger.error(f"Error in RefinerAgent listener: {e}")

        await blackboard.subscribe("synapse:input:text", on_new_input)
        logger.info(f"[{self.agent_id}] Listening on synapse:input:text")
