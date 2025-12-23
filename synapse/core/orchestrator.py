from typing import TypedDict, Annotated, Sequence, Dict, Any
from langgraph.graph import StateGraph, END
import operator

class OrchestratorState(TypedDict):
    input: str
    analysis: str
    is_valid: bool
    iterations: int

class SynapseOrchestrator:
    def __init__(self):
        self.workflow = StateGraph(OrchestratorState)
        
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

    def analyzer_node(self, state: OrchestratorState) -> OrchestratorState:
        """Simulates an analysis node."""
        # Note: In a real scenario, this would call an LLM or a specialized agent.
        return {
            **state,
            "analysis": f"Analyzed: {state['input']}",
            "iterations": state['iterations'] + 1
        }

    def guardian_node(self, state: OrchestratorState) -> OrchestratorState:
        """Simulates a validation/guardian node."""
        # Logic: For the sake of testing the loop, let's say it's valid 
        # only if iterations > 0 (which is always true after the first run).
        # We could make it complex to force a second iteration.
        return {
            **state,
            "is_valid": state['iterations'] > 0
        }

    def should_continue(self, state: OrchestratorState) -> str:
        """Decides whether to continue or end."""
        if state["is_valid"]:
            return "end"
        return "continue"

    async def run(self, initial_state: OrchestratorState) -> OrchestratorState:
        """Executes the graph."""
        return await self.app.ainvoke(initial_state)
