from typing import TypedDict, Annotated, Sequence, Dict, Any
from langgraph.graph import StateGraph, END
import operator
import json
from synapse.core.agents.vision_agent import VisionAgent
from synapse.core.agents.guardian_agent import GuardianAgent
from synapse.core.blackboard import Blackboard
from synapse.core.models import AgentContribution

class OrchestratorState(TypedDict):
    input: str
    analysis: str
    is_valid: bool
    iterations: int
    final_response: str

class SynapseOrchestrator:
    def __init__(self, blackboard: Blackboard = None):
        self.workflow = StateGraph(OrchestratorState)
        self.blackboard = blackboard or Blackboard()
        self.max_iterations = 3
        
        # Initialize agents
        self.vision_agent = VisionAgent(agent_id="vision_1")
        self.guardian_agent = GuardianAgent(agent_id="guardian_1")
        
        # Define nodes
        self.workflow.add_node("analyzer", self.analyzer_node)
        self.workflow.add_node("guardian", self.guardian_node)
        self.workflow.add_node("responder", self.responder_node)
        
        # Define edges
        self.workflow.set_entry_point("analyzer")
        self.workflow.add_edge("analyzer", "guardian")
        
        # Conditional edge for feedback loop
        self.workflow.add_conditional_edges(
            "guardian",
            self.should_continue,
            {
                "continue": "analyzer",
                "end": "responder"
            }
        )
        
        self.workflow.add_edge("responder", END)
        
        self.app = self.workflow.compile()

    async def emit_state(self, node_id: str):
        """Helper to emit active node state to Redis."""
        await self.blackboard.publish("synapse:state_updates", {
            "status": "processing",
            "active_node": node_id
        })

    async def analyzer_node(self, state: OrchestratorState) -> OrchestratorState:
        """Calls the Vision Agent and publishes to blackboard."""
        await self.emit_state("analyzer")
        print(f"--- ANALYZING (Iteration {state['iterations'] + 1}) ---")
        
        contribution = await self.vision_agent.analyze(state['input'])
        
        # Publish to Blackboard (Logs)
        await self.blackboard.publish("synapse:contributions", {
            "agent_id": "vision_agent",
            "content": f"Analysis complete (Iter {state['iterations'] + 1}): {contribution.content[:50]}..."
        })
        
        return {
            **state,
            "analysis": contribution.content,
            "iterations": state['iterations'] + 1
        }

    async def guardian_node(self, state: OrchestratorState) -> OrchestratorState:
        """Calls the Guardian Agent and validates against security policies."""
        await self.emit_state("guardian")
        print("--- VALIDATING ---")
        
        contribution = AgentContribution(
            agent_id="vision_1",
            timestamp=0.0,
            content=state["analysis"]
        )
        
        validation_result = await self.guardian_agent.validate(contribution)
        
        # Publish validation status to Blackboard (Logs)
        await self.blackboard.publish("synapse:contributions", {
            "agent_id": "guardian_agent",
            "content": f"Validation: {'PASSED' if validation_result.is_compliant else 'FAILED'}. {validation_result.logs}"
        })
        
        return {
            **state,
            "is_valid": validation_result.is_compliant
        }

    async def responder_node(self, state: OrchestratorState) -> OrchestratorState:
        """Final node that produces the user-facing response."""
        await self.emit_state("responder")
        
        response = f"Ejecución finalizada. Resultado: {state['analysis']}"
        if not state['is_valid']:
            response = "Lo siento, la respuesta generada no cumple con las políticas de seguridad después de varios intentos."

        # Store in chat history
        final_msg = {
            "id": "final_resp",
            "role": "assistant",
            "content": response
        }
        await self.blackboard.redis.rpush("synapse:chat_history", json.dumps(final_msg))

        # Notify UI through contributions channel
        await self.blackboard.publish("synapse:contributions", {
            "agent_id": "assistant",
            "content": response
        })

        return {**state, "final_response": response}

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
