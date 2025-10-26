import json
import redis
from typing import Any, Optional, Union
from datetime import timedelta
from resources.redis_client import redis_client


class CacheService:
    def __init__(self, client: Optional[redis.Redis] = redis_client):
        self.client = client

    def set(
        self,
        key: str,
        value: Any,
        expire: Optional[Union[int, timedelta]] = None,
        as_json: bool = True,
    ) -> bool:
        """Set a cache value with optional TTL (expire)."""
        try:
            if as_json:
                value = json.dumps(value)

            if isinstance(expire, timedelta):
                expire = int(expire.total_seconds())

            self.client.set(key, value, ex=expire)
            return True
        except Exception as e:
            return False

    def get(self, key: str, as_json: bool = True) -> Optional[Any]:
        """Get a cached value, optionally deserialized from JSON."""
        try:
            value = self.client.get(key)
            if value is None:
                return None

            return json.loads(value) if as_json else value
        except json.JSONDecodeError:
            return None
        except Exception as e:
            return None

    def delete(self, key: str) -> bool:
        """Delete a cached key."""
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            return False

    def exists(self, key: str) -> bool:
        """Check if a key exists in cache."""
        try:
            return bool(self.client.exists(key))
        except Exception as e:
            return False

    def ttl(self, key: str) -> int:
        """Return TTL (in seconds) for a key, -1 if no expiry, -2 if missing."""
        try:
            return self.client.ttl(key)
        except Exception as e:
            return -2

    def clear(self, pattern: Optional[str] = None) -> int:
        """Clear cache. If pattern provided, deletes only matching keys."""
        try:
            if pattern:
                keys = self.client.keys(pattern)
                if keys:
                    self.client.delete(*keys)
                    return len(keys)
                return 0
            else:
                self.client.flushdb()
                return 1
        except Exception as e:
            return 0

    def get_or_set(
        self,
        key: str,
        callback,
        expire: Optional[Union[int, timedelta]] = None,
        as_json: bool = True,
    ) -> Any:
        """
        Retrieve a value from cache or compute and set it if missing.
        The callback should return the computed value.
        """
        cached = self.get(key, as_json)
        if cached is not None:
            return cached

        value = callback()
        if value is not None:
            self.set(key, value, expire, as_json)
        return value
