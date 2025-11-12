from typing import Literal, Optional, Any, Dict, Callable
from contextlib import contextmanager
from utilities.logger import logger

from .containerCore import register_singletons
from .containerServices import register_services
from .containerControllers import register_controllers

Lifetime = Literal["singleton", "transient", "scoped"]


class Container:
    """Advanced IoC container with configurable lifetimes and factory-based dependency resolution."""

    _instance: Optional["Container"] = None

    def __new__(cls) -> "Container":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._factories: Dict[str, Callable[["Container"], Any]] = {}
        self._lifetimes: Dict[str, Lifetime] = {}
        self._instances: Dict[str, Any] = {}
        self._initialized = True

    def register(
        self,
        name: str,
        factory: Callable[["Container"], Any],
        lifetime: Lifetime = "singleton",
    ) -> None:
        self._factories[name] = factory
        self._lifetimes[name] = lifetime

    def resolve(self, name: str, scope: Optional[dict] = None) -> Any:
        lifetime = self._lifetimes.get(name, "singleton")
        if lifetime == "singleton":
            if name not in self._instances:
                self._instances[name] = self._factories[name](self)
            return self._instances[name]
        elif lifetime == "transient":
            return self._factories[name](self)
        elif lifetime == "scoped":
            if scope is None:
                raise RuntimeError(
                    f"Scope required to resolve scoped dependency '{name}'"
                )
            if name not in scope:
                scope[name] = self._factories[name](self)
            return scope[name]
        raise KeyError(f"Unknown lifetime '{lifetime}' for dependency '{name}'")

    @contextmanager
    def create_scope(self):
        scope: dict[str, Any] = {}
        try:
            yield scope
        finally:
            for instance in scope.values():
                close_fn = getattr(instance, "close", None)
                if callable(close_fn):
                    close_fn()
            scope.clear()

    def summary(self):
        logger.info("[Container Summary]")
        for name, lifetime in self._lifetimes.items():
            state = "Loaded" if name in self._instances else "Lazy"
            logger.info(f" - {name:<18} [{lifetime:<9}] : {state}")

    def build(self) -> "Container":
        try:
            self.resolve("CacheService")
            self.resolve("EmailService")
            self.resolve("FileService")
            self.resolve("BasicTokenService")
            logger.info("Core services initialized successfully.")
        except Exception as e:
            logger.error(f"Bootstrap failed: {e}", exc_info=True)
            raise SystemExit(1)
        return self


def bootstrap() -> Container:
    logger.info("Bootstrapping IoC container...")

    container = Container()
    register_singletons(container)
    register_services(container)
    register_controllers(container)
    container.build()
    container.summary()
    logger.info("IoC container Bootstrap completed")
    return container


container = bootstrap()
