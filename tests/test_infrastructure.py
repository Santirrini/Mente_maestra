import subprocess
import pytest
import redis
import time

def test_podman_is_installed():
    """Verify that podman is installed and accessible."""
    result = subprocess.run(["podman", "--version"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "podman" in result.stdout.lower()

def test_redis_container_is_running():
    """Verify that a redis container is running."""
    # This checks if a container named 'synapse-redis' is running
    result = subprocess.run(
        ["podman", "ps", "--format", "{{.Names}}"], 
        capture_output=True, 
        text=True
    )
    assert "synapse-redis" in result.stdout

def test_redis_connection():
    """Verify we can connect to the Redis instance."""
    r = redis.Redis(host='localhost', port=6379, db=0)
    try:
        assert r.ping() is True
    except redis.ConnectionError:
        pytest.fail("Could not connect to Redis")
