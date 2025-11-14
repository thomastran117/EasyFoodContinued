import json
import pickle
import redis
from typing import Any, Callable, Optional, Union, List, Dict
from datetime import timedelta
from contextlib import contextmanager
from resources.redis_client import redis_client

from beanie import Document
from pydantic import BaseModel


class CacheService:
    """
    Advanced Redis-backed cache service with model-safe JSON serialization.

    Features:
      - Auto-serialization of Beanie/Pydantic models
      - JSON & pickle support
      - Atomic operations
      - Distributed locking
      - Bulk operations
    """

    def __init__(
        self,
        client: Optional[redis.Redis] = redis_client,
        namespace: str = "easyfood",
        default_expire: Optional[int] = None,
    ):
        self.client = client
        self.namespace = namespace
        self.default_expire = default_expire

    def _key(self, key: str) -> str:
        return f"{self.namespace}:{key}"

    def encode_model(self, value: Any) -> Any:
        """Convert Beanie or Pydantic models (or lists of them) into JSON-safe dicts."""

        if isinstance(value, (Document, BaseModel)):
            return value.model_dump(mode="json")

        if isinstance(value, list):
            return [self.encode_model(v) for v in value]

        if isinstance(value, dict):
            return {k: self.encode_model(v) for k, v in value.items()}

        return value

    def decode_model(self, data: Any, model: Any) -> Any:
        """Convert cached data back into model instances."""
        if data is None:
            return None

        if isinstance(data, list):
            return [model(**item) for item in data]

        if isinstance(data, dict):
            return model(**data)

        return data

    def _serialize(self, value: Any, as_json: bool = True) -> bytes:
        """Serialize to JSON or pickle after encoding models."""

        try:
            value = self.encode_model(value)

            if as_json:
                return json.dumps(value).encode("utf-8")

            return pickle.dumps(value)

        except Exception as e:
            raise ValueError(f"Failed to serialize value for Redis: {e}")

    def _deserialize(self, data: Optional[bytes], as_json: bool = True) -> Any:
        """Deserialize JSON or pickle back to Python objects."""
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
        try:
            key = self._key(key)
            raw = self.client.get(key)
            return self._deserialize(raw, as_json)
        except Exception:
            return None

    def delete(self, key: str) -> bool:
        try:
            return bool(self.client.delete(self._key(key)))
        except Exception:
            return False

    def exists(self, key: str) -> bool:
        return bool(self.client.exists(self._key(key)))

    def ttl(self, key: str) -> int:
        return self.client.ttl(self._key(key))

    def clear(self, pattern: Optional[str] = None) -> int:
        try:
            pattern = pattern or "*"
            keys = list(self.client.scan_iter(f"{self.namespace}:{pattern}"))
            if keys:
                self.client.delete(*keys)
            return len(keys)
        except Exception:
            return 0

    def incr(self, key: str, amount: int = 1) -> int:
        return self.client.incr(self._key(key), amount)

    def decr(self, key: str, amount: int = 1) -> int:
        return self.client.decr(self._key(key), amount)

    @contextmanager
    def acquire_lock(self, key: str, timeout: int = 10, blocking_timeout: int = 5):
        lock = self.client.lock(
            self._key(key), timeout=timeout, blocking_timeout=blocking_timeout
        )
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
        value = self.get(key, as_json)
        if value is not None:
            return value

        value = callback()
        if value is not None:
            self.set(key, value, expire, as_json)
        return value
