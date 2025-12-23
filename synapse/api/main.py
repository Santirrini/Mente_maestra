from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, BackgroundTasks
from synapse.core.blackboard import Blackboard
from synapse.core.models import SynapseState, AgentContribution, AgentPhase, BlackboardState
from synapse.core.config import settings
from synapse.core.orchestrator import SynapseOrchestrator, OrchestratorState
from typing import Annotated, List
from pydantic import BaseModel
import asyncio
import json
import uuid

# Models for API
class CommandRequest(BaseModel):
    command: str

# Dependency to get blackboard
async def get_blackboard():
    bb = Blackboard(redis_url=settings.REDIS_URL)
    try:
        yield bb
    finally:
        await bb.close()

app = FastAPI(title="Synapse Control Plane API")

async def run_orchestration(command: str, bb: Blackboard):
    """Background task to run the orchestrator."""
    orchestrator = SynapseOrchestrator(blackboard=bb)
    initial_state = {
        "input": command,
        "analysis": "",
        "is_valid": False,
        "iterations": 0,
        "final_response": ""
    }
    await orchestrator.run(initial_state)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, bb: Annotated[Blackboard, Depends(get_blackboard)]):
    await websocket.accept()
    
    # Subscribe to redis channels
    pubsub = bb.redis.pubsub()
    await pubsub.subscribe("synapse:contributions", "synapse:state_updates")
    
    try:
        while True:
            try:
                # Check for messages from redis
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message:
                    data = json.loads(message["data"])
                    # Forward to websocket client
                    await websocket.send_json({
                        "channel": message["channel"].decode("utf-8"),
                        "data": data
                    })
            except (asyncio.TimeoutError, RuntimeError):
                # Basic heartbeat check or handle intermittent redis issues
                pass
            
            # Non-blocking sleep to allow other tasks
            await asyncio.sleep(0.01)
            
    except WebSocketDisconnect:
        print("WebSocket client disconnected")
        try:
            await pubsub.unsubscribe()
        except:
            pass
    except Exception as e:
        print(f"WebSocket encounter error: {e}")
    finally:
        try:
            await pubsub.close()
        except:
            pass

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/v1/chat/history")
async def get_chat_history(bb: Annotated[Blackboard, Depends(get_blackboard)]):
    """Retrieve chat history from Redis."""
    history = await bb.redis.lrange("synapse:chat_history", 0, -1)
    return [json.loads(msg) for msg in history]

@app.post("/api/v1/execute", status_code=202)
async def execute_command(
    request: CommandRequest,
    background_tasks: BackgroundTasks,
    bb: Annotated[Blackboard, Depends(get_blackboard)]
):
    """Trigger the orchestration flow from a user command."""
    task_id = str(uuid.uuid4())
    
    # Store initial message in blackboard for persistence
    initial_msg = {
        "id": task_id,
        "role": "user",
        "content": request.command
    }
    await bb.redis.rpush("synapse:chat_history", json.dumps(initial_msg))
    
    # Publish start event
    await bb.publish("synapse:state_updates", {
        "task_id": task_id,
        "status": "started",
        "active_node": "start"
    })
    
    # Run orchestration in background
    # Note: We need a new blackboard instance for the background task
    # because the one from Depends will be closed after the request returns.
    background_bb = Blackboard(redis_url=settings.REDIS_URL)
    background_tasks.add_task(run_orchestration, request.command, background_bb)
    
    return {"status": "started", "task_id": task_id}