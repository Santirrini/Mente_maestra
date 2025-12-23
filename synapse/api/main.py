from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from synapse.core.blackboard import Blackboard
from synapse.core.models import SynapseState, AgentContribution, AgentPhase, BlackboardState
from synapse.core.config import settings
from typing import Annotated
import asyncio
import json

# Dependency to get blackboard
async def get_blackboard():
    bb = Blackboard(redis_url=settings.REDIS_URL)
    try:
        yield bb
    finally:
        await bb.close()

app = FastAPI(title="Synapse Control Plane API")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, bb: Annotated[Blackboard, Depends(get_blackboard)]):
    await websocket.accept()
    
    # Subscribe to redis channels
    pubsub = bb.redis.pubsub()
    await pubsub.subscribe("synapse:contributions", "synapse:state_updates")
    
    try:
        while True:
            # Check for messages from redis
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message:
                data = json.loads(message["data"])
                # Forward to websocket client
                await websocket.send_json({
                    "channel": message["channel"].decode("utf-8"),
                    "data": data
                })
            
            # Non-blocking sleep to allow other tasks
            await asyncio.sleep(0.01)
            
    except WebSocketDisconnect:
        await pubsub.unsubscribe()
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await pubsub.close()

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