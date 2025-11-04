from typing import Optional
from service.tokenService import TokenService
from service.authService import AuthService
from service.emailService import EmailService
from service.fileService import FileService
from service.userService import UserService
from service.cacheService import CacheService
from controller.authController import AuthController
from controller.userController import UserController
from controller.fileController import FileController
from utilities.logger import logger

class Container:
    """A lightweight IoC container managing application-wide singletons."""

    _instance: Optional["Container"] = None

    def __new__(cls) -> "Container":
        """Ensure only one instance of the container exists (singleton)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_initialized") and self._initialized:
            return

        # Initialize placeholders for lazy singletons
        self._cache_service: Optional[CacheService] = None
        self._email_service: Optional[EmailService] = None
        self._file_service: Optional[FileService] = None
        self._token_service: Optional[TokenService] = None
        self._auth_service: Optional[AuthService] = None
        self._user_service: Optional[UserService] = None

        self._auth_controller: Optional[AuthController] = None
        self._user_controller: Optional[UserController] = None
        self._file_controller: Optional[FileController] = None

        self._initialized = True

    # ---------------------
    # Service Getters (lazy singletons)
    # ---------------------

    @property
    def cache_service(self) -> CacheService:
        if self._cache_service is None:
            self._cache_service = CacheService()
        return self._cache_service

    @property
    def email_service(self) -> EmailService:
        if self._email_service is None:
            self._email_service = EmailService()
        return self._email_service

    @property
    def file_service(self) -> FileService:
        if self._file_service is None:
            self._file_service = FileService()
        return self._file_service

    @property
    def token_service(self) -> TokenService:
        if self._token_service is None:
            self._token_service = TokenService(self.cache_service)
        return self._token_service

    @property
    def auth_service(self) -> AuthService:
        if self._auth_service is None:
            self._auth_service = AuthService(
                token_service=self.token_service,
                email_service=self.email_service,
            )
        return self._auth_service

    @property
    def user_service(self) -> UserService:
        if self._user_service is None:
            self._user_service = UserService(self.file_service)
        return self._user_service

    @property
    def auth_controller(self) -> AuthController:
        if self._auth_controller is None:
            self._auth_controller = AuthController(self.auth_service)
        return self._auth_controller

    @property
    def user_controller(self) -> UserController:
        if self._user_controller is None:
            self._user_controller = UserController(self.user_service)
        return self._user_controller

    @property
    def file_controller(self) -> FileController:
        if self._file_controller is None:
            self._file_controller = FileController(self.file_service)
        return self._file_controller


    def summary(self) -> None:
        """Prints out all active singletons for debugging."""
        active = {
            "CacheService": self._cache_service is not None,
            "EmailService": self._email_service is not None,
            "FileService": self._file_service is not None,
            "TokenService": self._token_service is not None,
            "AuthService": self._auth_service is not None,
            "UserService": self._user_service is not None,
            "AuthController": self._auth_controller is not None,
            "UserController": self._user_controller is not None,
            "FileController": self._file_controller is not None,
        }
        print("[Container Summary]")
        for k, v in active.items():
            print(f" - {k}: {'Loaded' if v else 'Lazy'}")


def bootstrap() -> Container:
    """
    Initializes core dependencies, ensuring required services are ready.

    - Eagerly initializes critical infrastructure (cache, DB, email).
    - Runs readiness checks.
    - Logs initialization summary.

    Returns:
        Container: The initialized application container.
    """
    container = Container()

    logger.info("Bootstrapping application container...")

    try:
        # Eagerly load essential services
        _ = container.cache_service
        _ = container.email_service
        _ = container.file_service
        _ = container.token_service

        # Example readiness checks
        try:
            ping = container.cache_service.client.ping()
        except Exception as e:
            logger.warn(f"CacheService failed health check: {e}")

        logger.info("Core services initialized successfully.")

    except Exception as e:
        logger.error(f"Bootstrap failed: {e}", exc_info=True)
        raise SystemExit(1)

    return container

container = bootstrap()
