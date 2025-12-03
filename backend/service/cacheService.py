import json
import pickle
from contextlib import asynccontextmanager
from datetime import timedelta
from typing import Any, Callable, Optional, Union

import redis.asyncio as redis
from beanie import Document
from pydantic import BaseModel

from resources.redis_client import redis_client
from utilities.errorRaiser import AppHttpException, InternalErrorException
from utilities.logger import logger


class CacheService:
    """
    Fully async Redis-backed cache service using redis.asyncio.
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
        except Exception as e:
            logger.error(f"[CacheService] key failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def encodeModel(self, value: Any) -> Any:
        try:
            if isinstance(value, (Document, BaseModel)):
                return value.model_dump(mode="json")

            if isinstance(value, list):
                return [self.encodeModel(v) for v in value]

            if isinstance(value, dict):
                return {k: self.encodeModel(v) for k, v in value.items()}

            return value

        except Exception as e:
            logger.error(f"[CacheService] encodeModel failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def serialize(self, value: Any, as_json: bool = True) -> bytes:
        try:
            encoded = self.encodeModel(value)

            if as_json:
                return json.dumps(encoded).encode("utf-8")
            return pickle.dumps(encoded)

        except Exception as e:
            logger.error(f"[CacheService] serialize failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def deserialize(self, raw: Optional[bytes], as_json: bool = True) -> Any:
        try:
            if raw is None:
                return None

            if as_json:
                return json.loads(raw)
            return pickle.loads(raw)

        except Exception as e:
            logger.error(f"[CacheService] deserialize failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def set(
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

            await self.client.set(key, data, ex=expire)
            return True

        except Exception as e:
            logger.error(f"[CacheService] set failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def get(self, key: str, as_json: bool = True) -> Any:
        try:
            key = self.key(key)
            raw = await self.client.get(key)
            return self.deserialize(raw, as_json)

        except Exception as e:
            logger.error(f"[CacheService] get failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def delete(self, key: str) -> bool:
        try:
            return bool(await self.client.delete(self.key(key)))
        except Exception as e:
            logger.error(f"[CacheService] delete failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def exists(self, key: str) -> bool:
        try:
            return bool(await self.client.exists(self.key(key)))
        except Exception as e:
            logger.error(f"[CacheService] exists failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def ttl(self, key: str) -> int:
        try:
            return await self.client.ttl(self.key(key))
        except Exception as e:
            logger.error(f"[CacheService] ttl failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def clear(self, pattern: Optional[str] = None) -> int:
        try:
            pattern = pattern or "*"
            full_pattern = f"{self.namespace}:{pattern}"
            keys = [k async for k in self.client.scan_iter(full_pattern)]

            if keys:
                await self.client.delete(*keys)

            return len(keys)

        except Exception as e:
            logger.error(f"[CacheService] clear failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def incr(self, key: str, amount: int = 1) -> int:
        try:
            return await self.client.incr(self.key(key), amount)
        except Exception as e:
            logger.error(f"[CacheService] incr failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def decr(self, key: str, amount: int = 1) -> int:
        try:
            return await self.client.decr(self.key(key), amount)
        except Exception as e:
            logger.error(f"[CacheService] decr failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    @asynccontextmanager
    async def acquireLock(self, key: str, timeout: int = 10, blocking_timeout: int = 5):
        lock = self.client.lock(
            self.key(key),
            timeout=timeout,
            blocking_timeout=blocking_timeout,
        )

        acquired = await lock.acquire()
        try:
            if acquired:
                yield
        finally:
            if acquired:
                await lock.release()

    async def getOrSet(
        self,
        key: str,
        callback: Callable[[], Any],
        expire: Optional[Union[int, timedelta]] = None,
        as_json: bool = True,
    ) -> Any:
        try:
            existing = await self.get(key, as_json)
            if existing is not None:
                return existing

            value = callback()
            if value is not None:
                await self.set(key, value, expire, as_json)

            return value

        except Exception as e:
            logger.error(f"[CacheService] getOrSet failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")
