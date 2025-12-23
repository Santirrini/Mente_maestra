from typing import TypedDict, Annotated, Sequence, Dict, Any
from langgraph.graph import StateGraph, END
import operator
from synapse.core.agents.vision_agent import VisionAgent
from synapse.core.agents.guardian_agent import GuardianAgent
from synapse.core.models import AgentContribution

class OrchestratorState(TypedDict):
    input: str
    analysis: str
    is_valid: bool
    iterations: int

class SynapseOrchestrator:
    def __init__(self):
        self.workflow = StateGraph(OrchestratorState)
        
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
        """Calls the Vision Agent."""
        print(f"--- ANALYZING (Iteration {state['iterations'] + 1}) ---")
        
        contribution = await self.vision_agent.analyze(state['input'])
        
        return {
            **state,
            "analysis": contribution.content,
            "iterations": state['iterations'] + 1
        }

    async def guardian_node(self, state: OrchestratorState) -> OrchestratorState:
        """Calls the Guardian Agent."""
        print("--- VALIDATING ---")
        
        # Create a temp contribution object from the analysis to validate
        # In a real system, we'd fetch this from the Blackboard
        contribution = AgentContribution(
            agent_id="vision_1", # Mock source
            timestamp=0.0,
            content=state["analysis"]
        )
        
        validation_result = await self.guardian_agent.validate(contribution)
        
        return {
            **state,
            "is_valid": validation_result.is_compliant
        }

    def should_continue(self, state: OrchestratorState) -> str:
        """Decides whether to continue or end."""
        if state["is_valid"]:
            return "end"
        # If not valid, we might want to loop or stop with error.
        # For this logic, if it's invalid, we stop (reject).
        # We only loop if we want to *correct* the output.
        # Here, let's just end. If invalid, the state reflects it.
        return "end"

    async def run(self, initial_state: OrchestratorState) -> OrchestratorState:
        """Executes the graph."""
        return await self.app.ainvoke(initial_state)