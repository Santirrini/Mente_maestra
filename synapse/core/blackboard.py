import json
import redis.asyncio as redis
import asyncio
import inspect
import logging
from typing import Callable, Any, Dict, Optional, List
from pydantic import BaseModel
from synapse.core.config import settings

logger = logging.getLogger(__name__)

class Blackboard:
    def __init__(self, redis_url: str = settings.REDIS_URL):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.pubsub = self.redis.pubsub()
        self.callbacks: Dict[str, List[Callable]] = {}
        self._listening_task = None
        self._heartbeat_task = None

    async def start(self):
        """Start the background tasks."""
        if not self._heartbeat_task:
            self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())

    async def ping(self) -> bool:
        """Check if the connection to Redis is alive."""
        try:
            return await self.redis.ping()
        except Exception:
            return False

    async def _heartbeat_loop(self):
        """Periodically check connection and log status."""
        while True:
            is_alive = await self.ping()
            status = "HEALTHY" if is_alive else "UNHEALTHY"
            await self.publish("synapse:system:heartbeat", {
                "status": status,
                "timestamp": asyncio.get_event_loop().time()
            })
            await asyncio.sleep(settings.HEARTBEAT_INTERVAL)

    async def publish(self, channel: str, message: Any):
        """Publish a message to a channel. Supports Pydantic models."""
        if isinstance(message, BaseModel):
            payload = message.model_dump_json()
        elif isinstance(message, dict):
            payload = json.dumps(message)
        else:
            payload = str(message)
            
        await self.redis.publish(channel, payload)

    async def subscribe(self, channel: str, callback: Callable[[Dict[str, Any]], Any]):
        """Subscribe to a channel and execute callback on message."""
        if channel not in self.callbacks:
            self.callbacks[channel] = []
            await self.pubsub.subscribe(channel)
        
        self.callbacks[channel].append(callback)
        
        # Start listening loop if not already started
        if not self._listening_task:
            self._listening_task = asyncio.create_task(self._listen())

    async def _listen(self):
        async for message in self.pubsub.listen():
            if message['type'] == 'message':
                channel = message['channel']
                if channel in self.callbacks:
                    try:
                        data = json.loads(message['data'])
                        for cb in self.callbacks[channel]:
                            try:
                                if inspect.iscoroutinefunction(cb):
                                    await cb(data)
                                else:
                                    cb(data)
                            except Exception as e:
                                logger.error(f"Error in Blackboard callback for channel {channel}: {e}")
                    except json.JSONDecodeError:
                        logger.warning(f"Received non-JSON message on channel {channel}: {message['data']}")
                    except Exception as e:
                        logger.error(f"Unexpected error in Blackboard listener: {e}")

    async def set_state(self, key: str, value: Dict[str, Any], ttl: Optional[int] = settings.DEFAULT_STATE_TTL):
        """Store state in the blackboard with an optional TTL in seconds."""
        await self.redis.set(key, json.dumps(value), ex=ttl)

    async def get_state(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve state from the blackboard."""
        value = await self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def close(self):
        """Close connections."""
        if self.pubsub:
            await self.pubsub.aclose()
        if self._listening_task:
            self._listening_task.cancel()
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
        
        tasks = [t for t in [self._listening_task, self._heartbeat_task] if t]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        
        await self.redis.aclose()