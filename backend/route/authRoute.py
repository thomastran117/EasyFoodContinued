from fastapi import APIRouter, Depends, Request
from controller.authController import AuthController
from dtos.authDtos import (
    LoginRequestDto,
    SignupRequestDto,
    ForgotPasswordDto,
    ChangePasswordDto,
    GoogleAuthRequest,
    MicrosoftAuthRequest,
)


async def get_auth_controller(request: Request) -> AuthController:
    """
    Resolve a scoped AuthController from the IoC container stored
    in app.state, ensuring per-request lifecycle and dependency resolution.
    """
    container = request.app.state.container

    async with container.create_scope() as scope:
        controller = await container.resolve("AuthController", scope)
        controller.request = request
        return controller


authRouter = APIRouter(tags=["Auth"])


@authRouter.post("/login")
async def login(
    dto: LoginRequestDto, ctrl: AuthController = Depends(get_auth_controller)
):
    return await ctrl.login(dto)


@authRouter.post("/signup")
async def signup(
    dto: SignupRequestDto, ctrl: AuthController = Depends(get_auth_controller)
):
    return await ctrl.signup(dto)


@authRouter.get("/verify")
async def verify(token: str, ctrl: AuthController = Depends(get_auth_controller)):
    return await ctrl.verify_email(token)


@authRouter.post("/refresh")
async def refresh(ctrl: AuthController = Depends(get_auth_controller)):
    return await ctrl.renew()


@authRouter.post("/logout")
async def logout(ctrl: AuthController = Depends(get_auth_controller)):
    return await ctrl.logout()


@authRouter.post("/google")
async def google(
    dto: GoogleAuthRequest, ctrl: AuthController = Depends(get_auth_controller)
):
    return await ctrl.google(dto)


@authRouter.post("/microsoft")
async def microsoft(
    dto: MicrosoftAuthRequest, ctrl: AuthController = Depends(get_auth_controller)
):
    return await ctrl.microsoft(dto)


@authRouter.post("/forgot-password")
async def forgot(
    dto: ForgotPasswordDto, ctrl: AuthController = Depends(get_auth_controller)
):
    return await ctrl.forgot_password(dto)


@authRouter.post("/change-password")
async def change_password(
    token: str,
    dto: ChangePasswordDto,
    ctrl: AuthController = Depends(get_auth_controller),
):
    return await ctrl.change_password(token, dto)
