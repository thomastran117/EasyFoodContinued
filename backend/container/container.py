from contextlib import asynccontextmanager
from typing import Any, Awaitable, Callable, Dict, Literal, Optional

from utilities.logger import logger

Lifetime = Literal["singleton", "transient", "scoped"]


class Container:
    """
    Async-aware IoC container.
    Supports async factories and async init lifetimes.
    """

    _instance: Optional["Container"] = None

    def __new__(cls) -> "Container":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        try:
            if getattr(self, "_initialized", False):
                return
            self._factories: Dict[str, Callable[["Container"], Any]] = {}
            self._lifetimes: Dict[str, Lifetime] = {}
            self._instances: Dict[str, Any] = {}
            self._initialized = True
        except Exception as e:
            logger.error(
                f"[Container] Initializing container failed: {e}", exc_info=True
            )
            raise SystemExit(1)

    def register(
        self,
        name: str,
        factory: Callable[["Container"], Any | Awaitable[Any]],
        lifetime: Lifetime = "singleton",
    ) -> None:
        try:
            self._factories[name] = factory
            self._lifetimes[name] = lifetime
        except Exception as e:
            logger.error(
                f"[Container] Registering resources failed: {e}", exc_info=True
            )
            raise SystemExit(1)

    async def resolve(self, name: str, scope: Optional[dict] = None) -> Any:
        lifetime = self._lifetimes.get(name, "singleton")

        async def _create_instance():
            result = self._factories[name](self)
            if isinstance(result, Awaitable):
                return await result
            return result

        if lifetime == "singleton":
            if name not in self._instances:
                self._instances[name] = await _create_instance()
            return self._instances[name]

        elif lifetime == "transient":
            return await _create_instance()

        elif lifetime == "scoped":
            if scope is None:
                raise RuntimeError(
                    f"Scope required to resolve scoped dependency '{name}'"
                )
            if name not in scope:
                scope[name] = await _create_instance()
            return scope[name]

        raise KeyError(f"Unknown lifetime '{lifetime}' for dependency '{name}'")

    async def optionalResolve(self, name: str, scope: Optional[dict] = None) -> Any:
        try:
            return await self.resolve(name, scope)
        except Exception as e:
            logger.warn(
                f"[Container] Optional dependency '{name}' failed to resolve: {e}"
            )
            return None

    @asynccontextmanager
    async def create_scope(self):
        scope: dict[str, Any] = {}
        try:
            yield scope
        except Exception as e:
            logger.error(f"[Container] Resolving dependency failed: {e}", exc_info=True)
        finally:
            for instance in scope.values():
                close_fn = getattr(instance, "close", None)
                if callable(close_fn):
                    maybe_await = close_fn()
                    if isinstance(maybe_await, Awaitable):
                        await maybe_await
            scope.clear()

    async def build(self) -> "Container":
        try:
            await self.resolve("CacheService")
            await self.resolve("FileService")
            await self.resolve("BasicTokenService")
            logger.info("Core services initialized successfully.")
        except Exception as e:
            logger.error(f"[Container] Core bootstrap failed: {e}", exc_info=True)
            raise SystemExit(1)
        return self

    def summary(self):
        try:
            logger.info("[Container Summary]")
            for name, lifetime in self._lifetimes.items():
                state = "Loaded" if name in self._instances else "Lazy"
                logger.info(f" - {name:<18} [{lifetime:<9}] : {state}")
        except Exception as e:
            logger.error(f"[Container] Summary display failed: {e}", exc_info=True)
            return
