import json
import redis.asyncio as redis
import asyncio
import inspect
from typing import Callable, Any, Dict, Optional

class Blackboard:
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.pubsub = self.redis.pubsub()
        self.callbacks: Dict[str, Callable] = {}
        self._listening_task = None

    async def publish(self, channel: str, message: Dict[str, Any]):
        """Publish a message to a channel."""
        await self.redis.publish(channel, json.dumps(message))

    async def subscribe(self, channel: str, callback: Callable[[Dict[str, Any]], Any]):
        """Subscribe to a channel and execute callback on message."""
        self.callbacks[channel] = callback
        await self.pubsub.subscribe(channel)
        
        # Start listening loop if not already started
        if not self._listening_task:
            self._listening_task = asyncio.create_task(self._listen())

    async def _listen(self):
        async for message in self.pubsub.listen():
            if message['type'] == 'message':
                channel = message['channel']
                if channel in self.callbacks:
                    data = json.loads(message['data'])
                    cb = self.callbacks[channel]
                    if inspect.iscoroutinefunction(cb):
                        await cb(data)
                    else:
                        cb(data)

    async def set_state(self, key: str, value: Dict[str, Any]):
        """Store state in the blackboard."""
        await self.redis.set(key, json.dumps(value))

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
            try:
                await self._listening_task
            except asyncio.CancelledError:
                pass
        await self.redis.aclose()