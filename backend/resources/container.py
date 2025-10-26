from service.tokenService import TokenService
from service.authService import AuthService
from service.emailService import EmailService
from service.fileService import FileService
from service.userService import UserService
from controller.authController import AuthController
from controller.userController import UserController


class Container:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        self.token_service = TokenService()
        self.email_service = EmailService()
        self.file_service = FileService()
        self.auth_service = AuthService(
            token_service=self.token_service, email_service=self.email_service
        )
        self.user_service = UserService(self.file_service)
        self.auth_controller = AuthController(self.auth_service)
        self.user_controller = UserController(self.user_service)

    def get_token_service(self) -> TokenService:
        return self.token_service

    def get_auth_service(self) -> AuthService:
        return self.auth_service

    def get_auth_controller(self) -> AuthController:
        return self.auth_controller

    def get_user_controller(self) -> UserController:
        return self.user_controller

    def get_email_service(self) -> EmailService:
        return self.email_service

    def get_file_service(self) -> FileService:
        return self.file_service


class_container = Container()
