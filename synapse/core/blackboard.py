import json
import redis.asyncio as redis
import asyncio
import inspect
from typing import Callable, Any, Dict, Optional
from synapse.core.config import settings

class Blackboard:
    def __init__(self, redis_url: str = settings.REDIS_URL):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.pubsub = self.redis.pubsub()
        self.callbacks: Dict[str, Callable] = {}
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