from fastapi import FastAPI, Depends
from synapse.core.blackboard import Blackboard
from synapse.core.models import SynapseState, AgentContribution, AgentPhase, BlackboardState
from synapse.core.config import settings
from typing import Annotated

# Dependency to get blackboard
async def get_blackboard():
    bb = Blackboard(redis_url=settings.REDIS_URL)
    try:
        yield bb
    finally:
        await bb.close()

app = FastAPI(title="Synapse Control Plane API")

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/v1/state", response_model=SynapseState)
async def get_state(bb: Annotated[Blackboard, Depends(get_blackboard)]):
    """Retrieve the current state of the synapse control plane."""
    state_data = await bb.get_state("synapse:state")
    if not state_data:
        # Initial default state
        return SynapseState(
            current_phase=AgentPhase.IDLE,
            blackboard=BlackboardState()
        )
    return SynapseState(**state_data)

@app.post("/api/v1/contributions", response_model=AgentContribution, status_code=201)
async def post_contribution(
    contribution: AgentContribution, 
    bb: Annotated[Blackboard, Depends(get_blackboard)]
):
    """Post a new contribution to the blackboard."""
    # 1. Publish to the blackboard channel
    await bb.publish("synapse:contributions", contribution.model_dump())
    
    # 2. Update the state (simplified for MVP)
    # Note: In production, this state update should probably be handled 
    # by a dedicated state manager agent listening to the contributions channel.
    current_state = await get_state(bb)
    current_state.blackboard.contributions.append(contribution)
    await bb.set_state("synapse:state", current_state.model_dump())
    
    return contribution