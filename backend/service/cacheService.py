import json
import pickle
from contextlib import contextmanager
from datetime import timedelta
from typing import Any, Callable, Dict, List, Optional, Union

import redis
from beanie import Document
from pydantic import BaseModel

from resources.redis_client import redis_client
from utilities.errorRaiser import AppHttpException, InternalErrorException
from utilities.logger import logger


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

    def key(self, key: str) -> str:
        try:
            return f"{self.namespace}:{key}"
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[CacheService] key failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def encodeModel(self, value: Any) -> Any:
        """Convert Beanie or Pydantic models (or lists of them) into JSON-safe dicts."""
        try:
            if isinstance(value, (Document, BaseModel)):
                return value.model_dump(mode="json")

            if isinstance(value, list):
                return [self.encodeModel(v) for v in value]

            if isinstance(value, dict):
                return {k: self.encodeModel(v) for k, v in value.items()}

            return value
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[CacheService] encodeModel failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def decodeModel(self, data: Any, model: Any) -> Any:
        """Convert cached data back into model instances."""
        try:
            if data is None:
                return None

            if isinstance(data, list):
                return [model(**item) for item in data]

            if isinstance(data, dict):
                return model(**data)

            return data
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[CacheService] decodeModel failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def serialize(self, value: Any, as_json: bool = True) -> bytes:
        """Serialize to JSON or pickle after encoding models."""

        try:
            value = self.encodeModel(value)

            if as_json:
                return json.dumps(value).encode("utf-8")
            return pickle.dumps(value)
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[CacheService] serialize failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def deserialize(self, data: Optional[bytes], as_json: bool = True) -> Any:
        """Deserialize JSON or pickle back to Python objects."""
        try:
            if data is None:
                return None

            return json.loads(data) if as_json else pickle.loads(data)
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[CacheService] deserialize failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def set(
        self,
        key: str,
        value: Any,
        expire: Optional[Union[int, timedelta]] = None,
        as_json: bool = True,
    ) -> bool:
        try:
            key = self.key(key)
            data = self.serialize(value, as_json)

            if isinstance(expire, timedelta):
                expire = int(expire.total_seconds())

            expire = expire or self.default_expire
            self.client.set(key, data, ex=expire)
            return True
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[CacheService] set failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def get(self, key: str, as_json: bool = True) -> Optional[Any]:
        try:
            key = self.key(key)
            raw = self.client.get(key)
            return self.deserialize(raw, as_json)
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[CacheService] get failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def delete(self, key: str) -> bool:
        try:
            return bool(self.client.delete(self.key(key)))
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[CacheService] delete failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def exists(self, key: str) -> bool:
        try:
            return bool(self.client.exists(self.key(key)))
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[CacheService] exists failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def ttl(self, key: str) -> int:
        try:
            return self.client.ttl(self.key(key))
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[CacheService] ttl failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def clear(self, pattern: Optional[str] = None) -> int:
        try:
            pattern = pattern or "*"
            keys = list(self.client.scan_iter(f"{self.namespace}:{pattern}"))
            if keys:
                self.client.delete(*keys)
            return len(keys)
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[CacheService] clear failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def incr(self, key: str, amount: int = 1) -> int:
        try:
            return self.client.incr(self.key(key), amount)
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[CacheService] incr failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def decr(self, key: str, amount: int = 1) -> int:
        try:
            return self.client.decr(self.key(key), amount)
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[CacheService] decr failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    @contextmanager
    def acquireLock(self, key: str, timeout: int = 10, blocking_timeout: int = 5):
        lock = self.client.lock(
            self.key(key), timeout=timeout, blocking_timeout=blocking_timeout
        )
        acquired = lock.acquire(blocking=True)
        try:
            if acquired:
                yield
        finally:
            if acquired:
                lock.release()

    def getOrSet(
        self,
        key: str,
        callback: Callable[[], Any],
        expire: Optional[Union[int, timedelta]] = None,
        as_json: bool = True,
    ) -> Any:
        try:
            value = self.get(key, as_json)
            if value is not None:
                return value

            value = callback()
            if value is not None:
                self.set(key, value, expire, as_json)
            return value
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[CacheService] serialize failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")
