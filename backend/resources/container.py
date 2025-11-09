from typing import Callable, Dict, Optional, Any, Literal
from contextlib import contextmanager
from utilities.logger import logger

from service.cacheService import CacheService
from service.emailService import EmailService
from service.fileService import FileService
from service.tokenService import TokenService
from service.authService import AuthService
from service.userService import UserService
from service.paymentService import PaymentService
from controller.authController import AuthController
from controller.userController import UserController
from controller.fileController import FileController
from controller.paymentController import PaymentController

Lifetime = Literal["singleton", "transient", "scoped"]


class Container:
    """Advanced IoC container with configurable lifetimes and factory-based dependency resolution."""

    _instance: Optional["Container"] = None

    def __new__(cls) -> "Container":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
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
        """Registers a dependency with a specified lifetime."""
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
        """Creates a new dependency scope (e.g. per-request)."""
        scope: dict[str, Any] = {}
        try:
            yield scope
        finally:
            for instance in scope.values():
                close_fn = getattr(instance, "close", None)
                if callable(close_fn):
                    close_fn()
            scope.clear()

    def add_core_services(
        self,
        cache_lifetime: Lifetime = "singleton",
        email_lifetime: Lifetime = "singleton",
        file_lifetime: Lifetime = "singleton",
        token_lifetime: Lifetime = "transient",
    ) -> "Container":
        """Registers fundamental services with overridable lifetimes."""
        self.register("CacheService", lambda c: CacheService(), cache_lifetime)
        self.register("EmailService", lambda c: EmailService(), email_lifetime)
        self.register("FileService", lambda c: FileService(), file_lifetime)
        self.register(
            "TokenService",
            lambda c: TokenService(c.resolve("CacheService")),
            token_lifetime,
        )
        return self

    def add_app_services(
        self,
        auth_service_lifetime: Lifetime = "transient",
        user_service_lifetime: Lifetime = "transient",
        payment_service_lifetime: Lifetime = "transient",
    ) -> "Container":
        """Registers application-level services with configurable lifetimes."""
        self.register(
            "AuthService",
            lambda c: AuthService(
                token_service=c.resolve("TokenService"),
                email_service=c.resolve("EmailService"),
            ),
            auth_service_lifetime,
        )
        self.register(
            "UserService",
            lambda c: UserService(c.resolve("FileService")),
            user_service_lifetime,
        )
        self.register(
            "PaymentService",
            lambda c: PaymentService(),
            payment_service_lifetime,
        )
        return self

    def add_controllers(
        self,
        auth_controller_lifetime: Lifetime = "scoped",
        user_controller_lifetime: Lifetime = "scoped",
        file_controller_lifetime: Lifetime = "scoped",
        payment_controller_lifetime: Lifetime = "scoped",
    ) -> "Container":
        """Registers controllers with configurable lifetimes."""
        self.register(
            "AuthController",
            lambda c: AuthController(c.resolve("AuthService")),
            auth_controller_lifetime,
        )
        self.register(
            "UserController",
            lambda c: UserController(c.resolve("UserService")),
            user_controller_lifetime,
        )
        self.register(
            "FileController",
            lambda c: FileController(c.resolve("FileService")),
            file_controller_lifetime,
        )
        self.register(
            "PaymentController",
            lambda c: PaymentController(c.resolve("PaymentService")),
            payment_controller_lifetime,
        )
        return self

    def summary(self) -> None:
        """Logs dependency registration summary."""
        logger.info("[Container Summary]")
        for name, lifetime in self._lifetimes.items():
            state = "Loaded" if name in self._instances else "Lazy"
            logger.info(f" - {name:<18} [{lifetime:<9}] : {state}")

    def build(self) -> "Container":
        """Eagerly initializes singletons and checks service health."""
        try:
            cache = self.resolve("CacheService")
            try:
                cache.client.ping()
                logger.info("CacheService passed health check.")
            except Exception as e:
                logger.warning(f"CacheService health check failed: {e}")

            self.resolve("EmailService")
            self.resolve("FileService")

            logger.info("Core services initialized successfully.")
        except Exception as e:
            logger.error(f"Bootstrap failed: {e}", exc_info=True)
            raise SystemExit(1)
        return self


def bootstrap(
    *,
    cache_lifetime: Lifetime = "singleton",
    email_lifetime: Lifetime = "singleton",
    file_lifetime: Lifetime = "singleton",
    token_lifetime: Lifetime = "transient",
    auth_service_lifetime: Lifetime = "transient",
    user_service_lifetime: Lifetime = "transient",
    payment_service_lifetime: Lifetime = "transient",
    auth_controller_lifetime: Lifetime = "scoped",
    user_controller_lifetime: Lifetime = "scoped",
    file_controller_lifetime: Lifetime = "scoped",
    payment_controller_lifetime: Lifetime = "scoped",
) -> Container:
    """Bootstraps the container with optional lifetime overrides."""
    logger.info("Bootstrapping IoC container with configurable lifetimes...")

    container = (
        Container()
        .add_core_services(
            cache_lifetime=cache_lifetime,
            email_lifetime=email_lifetime,
            file_lifetime=file_lifetime,
            token_lifetime=token_lifetime,
        )
        .add_app_services(
            auth_service_lifetime=auth_service_lifetime,
            user_service_lifetime=user_service_lifetime,
            payment_service_lifetime=payment_service_lifetime,
        )
        .add_controllers(
            auth_controller_lifetime=auth_controller_lifetime,
            user_controller_lifetime=user_controller_lifetime,
            file_controller_lifetime=file_controller_lifetime,
            payment_controller_lifetime=payment_controller_lifetime,
        )
        .build()
    )

    # container.summary()
    logger.info("IoC container Bootstrap completed")
    return container


container = bootstrap()
