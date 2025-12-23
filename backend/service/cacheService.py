import json
import pickle
from contextlib import asynccontextmanager
from datetime import timedelta
from typing import Any, Awaitable, Callable, Optional, Union

import redis.asyncio as redis
from beanie import Document
from pydantic import BaseModel

from resources.redis_client import redis_client
from utilities.logger import logger


class CacheService:
    """
    Redis-backed cache service.
    FAIL-OPEN by design: cache failures never break requests.
    """

    def __init__(
        self,
        client: Optional[redis.Redis] = redis_client,
        namespace: str = "easyfood",
        default_expire: Optional[int] = None,
        enabled: bool = True,
    ):
        self.client = client
        self.namespace = namespace
        self.default_expire = default_expire
        self.enabled = enabled and client is not None

    def key(self, key: str) -> str:
        return f"{self.namespace}:{key}"

    def _encode(self, value: Any) -> Any:
        if isinstance(value, (Document, BaseModel)):
            return value.model_dump(mode="json")
        if isinstance(value, list):
            return [self._encode(v) for v in value]
        if isinstance(value, dict):
            return {k: self._encode(v) for k, v in value.items()}
        return value

    def serialize(self, value: Any, as_json: bool = True) -> bytes:
        encoded = self._encode(value)
        return json.dumps(encoded).encode("utf-8") if as_json else pickle.dumps(encoded)

    def deserialize(self, raw: Optional[bytes], as_json: bool = True) -> Any:
        if raw is None:
            return None
        return json.loads(raw) if as_json else pickle.loads(raw)

    async def get(self, key: str, as_json: bool = True) -> Any:
        if not self.enabled:
            return None

        try:
            raw = await self.client.get(self.key(key))
            return self.deserialize(raw, as_json)
        except Exception as e:
            logger.warn(f"[CacheService] get failed — bypassing cache: {e}")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[Union[int, timedelta]] = None,
        as_json: bool = True,
    ) -> bool:
        if not self.enabled:
            return False

        try:
            if isinstance(expire, timedelta):
                expire = int(expire.total_seconds())
            expire = expire or self.default_expire

            await self.client.set(
                self.key(key),
                self.serialize(value, as_json),
                ex=expire,
            )
            return True
        except Exception as e:
            logger.warn(f"[CacheService] set failed — ignoring: {e}")
            return False

    async def delete(self, key: str) -> bool:
        if not self.enabled:
            return False

        try:
            return bool(await self.client.delete(self.key(key)))
        except Exception as e:
            logger.warn(f"[CacheService] delete failed — ignoring: {e}")
            return False

    async def exists(self, key: str) -> bool:
        if not self.enabled:
            return False

        try:
            return bool(await self.client.exists(self.key(key)))
        except Exception as e:
            logger.warn(f"[CacheService] exists failed — assuming false: {e}")
            return False

    async def ttl(self, key: str) -> int:
        if not self.enabled:
            return -2

        try:
            return await self.client.ttl(self.key(key))
        except Exception as e:
            logger.warn(f"[CacheService] ttl failed — returning -2: {e}")
            return -2

    async def incr(self, key: str, amount: int = 1) -> Optional[int]:
        if not self.enabled:
            return None

        try:
            return await self.client.incr(self.key(key), amount)
        except Exception as e:
            logger.warn(f"[CacheService] incr failed — ignoring: {e}")
            return None

    async def decr(self, key: str, amount: int = 1) -> Optional[int]:
        if not self.enabled:
            return None

        try:
            return await self.client.decr(self.key(key), amount)
        except Exception as e:
            logger.warn(f"[CacheService] decr failed — ignoring: {e}")
            return None

    @asynccontextmanager
    async def acquire_lock(
        self,
        key: str,
        timeout: int = 10,
        blocking_timeout: int = 5,
    ):
        if not self.enabled:
            yield
            return

        try:
            lock = self.client.lock(
                self.key(key),
                timeout=timeout,
                blocking_timeout=blocking_timeout,
            )
            acquired = await lock.acquire()
        except Exception as e:
            logger.warn(f"[CacheService] lock acquire failed — bypassing: {e}")
            yield
            return

        try:
            if acquired:
                yield
        finally:
            try:
                if acquired:
                    await lock.release()
            except Exception:
                pass

    async def getOrSet(
        self,
        key: str,
        callback: Callable[[], Awaitable[Any]],
        expire: Optional[Union[int, timedelta]] = None,
        as_json: bool = True,
    ) -> Any:
        value = await self.get(key, as_json)
        if value is not None:
            return value

        try:
            value = await callback()
        except Exception:
            raise

        if value is not None:
            await self.set(key, value, expire, as_json)

        return value
