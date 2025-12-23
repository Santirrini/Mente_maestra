from typing import TypedDict, Annotated, Sequence, Dict, Any
from langgraph.graph import StateGraph, END
import operator
from synapse.core.agents.vision_agent import VisionAgent
from synapse.core.agents.guardian_agent import GuardianAgent
from synapse.core.blackboard import Blackboard
from synapse.core.models import AgentContribution

class OrchestratorState(TypedDict):
    input: str
    analysis: str
    is_valid: bool
    iterations: int

class SynapseOrchestrator:
    def __init__(self):
        self.workflow = StateGraph(OrchestratorState)
        self.blackboard = Blackboard()
        self.max_iterations = 3
        
        # Initialize agents
        self.vision_agent = VisionAgent(agent_id="vision_1")
        self.guardian_agent = GuardianAgent(agent_id="guardian_1")
        
        # Define nodes
        self.workflow.add_node("analyzer", self.analyzer_node)
        self.workflow.add_node("guardian", self.guardian_node)
        
        # Define edges
        self.workflow.set_entry_point("analyzer")
        self.workflow.add_edge("analyzer", "guardian")
        
        # Conditional edge for feedback loop
        self.workflow.add_conditional_edges(
            "guardian",
            self.should_continue,
            {
                "continue": "analyzer",
                "end": END
            }
        )
        
        self.app = self.workflow.compile()

    async def analyzer_node(self, state: OrchestratorState) -> OrchestratorState:
        """Calls the Vision Agent and publishes to blackboard."""
        print(f"--- ANALYZING (Iteration {state['iterations'] + 1}) ---")
        
        contribution = await self.vision_agent.analyze(state['input'])
        
        # Publish to Blackboard
        await self.blackboard.publish("synapse:agents:vision", contribution)
        
        return {
            **state,
            "analysis": contribution.content,
            "iterations": state['iterations'] + 1
        }

    async def guardian_node(self, state: OrchestratorState) -> OrchestratorState:
        """Calls the Guardian Agent and validates against security policies."""
        print("--- VALIDATING ---")
        
        # Create a temp contribution object from the analysis
        contribution = AgentContribution(
            agent_id="vision_1",
            timestamp=0.0,
            content=state["analysis"]
        )
        
        validation_result = await self.guardian_agent.validate(contribution)
        
        # Publish validation status to Blackboard
        await self.blackboard.publish("synapse:agents:guardian", {
            "is_valid": validation_result.is_compliant,
            "logs": validation_result.logs,
            "iteration": state["iterations"]
        })
        
        return {
            **state,
            "is_valid": validation_result.is_compliant
        }

    def should_continue(self, state: OrchestratorState) -> str:
        """Decides whether to continue or end based on validity and iteration count."""
        if state["is_valid"]:
            return "end"
        
        if state["iterations"] >= self.max_iterations:
            print(f"--- REJECTED: Max iterations ({self.max_iterations}) reached ---")
            return "end"
            
        print("--- RETRYING: Validation failed ---")
        return "continue"

    async def run(self, initial_state: OrchestratorState) -> OrchestratorState:
        """Executes the graph."""
        return await self.app.ainvoke(initial_state)