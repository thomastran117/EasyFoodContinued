import json
import pickle
import redis
from typing import Any, Callable, Optional, Union, List, Dict
from datetime import timedelta
from contextlib import contextmanager
from resources.redis_client import redis_client


class CacheService:
    """
    Advanced Redis-backed cache service supporting rich operations:
      - Basic get/set/delete/exists/ttl
      - Hash, list, and set structures
      - Atomic increments/decrements
      - Bulk operations (mget/mset)
      - JSON or pickle serialization
      - Distributed locking
    """

    def __init__(
        self,
        client: Optional[redis.Redis] = redis_client,
        namespace: str = "app",
        default_expire: Optional[int] = None,
    ):
        self.client = client
        self.namespace = namespace
        self.default_expire = default_expire

    def _key(self, key: str) -> str:
        """Apply namespace prefix to a key."""
        return f"{self.namespace}:{key}"

    def _serialize(self, value: Any, as_json: bool = True) -> bytes:
        """Serialize to JSON or pickle for safe storage."""
        try:
            if as_json:
                return json.dumps(value).encode("utf-8")
            return pickle.dumps(value)
        except Exception as e:
            raise ValueError(f"Failed to serialize value for Redis: {e}")

    def _deserialize(self, data: Optional[bytes], as_json: bool = True) -> Any:
        """Deserialize JSON or pickle data."""
        if data is None:
            return None
        try:
            return json.loads(data) if as_json else pickle.loads(data)
        except Exception:
            return None

    def set(
        self,
        key: str,
        value: Any,
        expire: Optional[Union[int, timedelta]] = None,
        as_json: bool = True,
    ) -> bool:
        """Set a cache value with optional TTL."""
        try:
            key = self._key(key)
            data = self._serialize(value, as_json)
            if isinstance(expire, timedelta):
                expire = int(expire.total_seconds())
            expire = expire or self.default_expire
            self.client.set(key, data, ex=expire)
            return True
        except Exception:
            return False

    def get(self, key: str, as_json: bool = True) -> Optional[Any]:
        """Retrieve a cached value."""
        try:
            key = self._key(key)
            data = self.client.get(key)
            return self._deserialize(data, as_json)
        except Exception:
            return None

    def delete(self, key: str) -> bool:
        """Delete a cached key."""
        try:
            return bool(self.client.delete(self._key(key)))
        except Exception:
            return False

    def exists(self, key: str) -> bool:
        """Check if a key exists."""
        try:
            return bool(self.client.exists(self._key(key)))
        except Exception:
            return False

    def ttl(self, key: str) -> int:
        """Return TTL (seconds), -1 if no expiry, -2 if missing."""
        try:
            return self.client.ttl(self._key(key))
        except Exception:
            return -2

    def clear(self, pattern: Optional[str] = None) -> int:
        """Clear all or matching keys."""
        try:
            if pattern:
                keys = list(self.client.scan_iter(f"{self.namespace}:{pattern}"))
                if keys:
                    self.client.delete(*keys)
                    return len(keys)
                return 0
            else:
                keys = list(self.client.scan_iter(f"{self.namespace}:*"))
                if keys:
                    self.client.delete(*keys)
                return len(keys)
        except Exception:
            return 0

    def mget(self, keys: List[str], as_json: bool = True) -> List[Any]:
        """Retrieve multiple keys."""
        full_keys = [self._key(k) for k in keys]
        values = self.client.mget(full_keys)
        return [self._deserialize(v, as_json) for v in values]

    def mset(self, data: Dict[str, Any], expire: Optional[int] = None, as_json: bool = True):
        """Set multiple key-value pairs."""
        try:
            mapping = {self._key(k): self._serialize(v, as_json) for k, v in data.items()}
            self.client.mset(mapping)
            if expire:
                for k in mapping.keys():
                    self.client.expire(k, expire)
        except Exception:
            return False
        return True

    def incr(self, key: str, amount: int = 1) -> int:
        """Increment an integer value atomically."""
        return self.client.incr(self._key(key), amount)

    def decr(self, key: str, amount: int = 1) -> int:
        """Decrement an integer value atomically."""
        return self.client.decr(self._key(key), amount)


    def hset(self, name: str, key: str, value: Any, as_json: bool = True) -> bool:
        try:
            return bool(self.client.hset(self._key(name), key, self._serialize(value, as_json)))
        except Exception:
            return False

    def hget(self, name: str, key: str, as_json: bool = True) -> Optional[Any]:
        try:
            data = self.client.hget(self._key(name), key)
            return self._deserialize(data, as_json)
        except Exception:
            return None

    def hgetall(self, name: str, as_json: bool = True) -> Dict[str, Any]:
        try:
            data = self.client.hgetall(self._key(name))
            return {k.decode(): self._deserialize(v, as_json) for k, v in data.items()}
        except Exception:
            return {}


    @contextmanager
    def acquire_lock(self, key: str, timeout: int = 10, blocking_timeout: int = 5):
        """
        Context-managed distributed lock.
        Example:
            with cache.acquire_lock("task:123"):
                ... critical section ...
        """
        lock = self.client.lock(self._key(key), timeout=timeout, blocking_timeout=blocking_timeout)
        acquired = lock.acquire(blocking=True)
        try:
            if acquired:
                yield
        finally:
            if acquired:
                lock.release()

    def get_or_set(
        self,
        key: str,
        callback: Callable[[], Any],
        expire: Optional[Union[int, timedelta]] = None,
        as_json: bool = True,
    ) -> Any:
        """Retrieve from cache or compute and set if missing."""
        value = self.get(key, as_json)
        if value is not None:
            return value

        value = callback()
        if value is not None:
            self.set(key, value, expire, as_json)
        return value
