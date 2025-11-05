from fastapi import APIRouter, Depends
from controller.authController import AuthController
from resources.container import container

authRouter = APIRouter(tags=["Auth"])


def get_auth_controller() -> AuthController:
    """Resolves an AuthController with lifetimes managed by the container."""
    with container.create_scope() as scope:
        return container.resolve("AuthController", scope)


@authRouter.post("/login")
async def login(auth_controller: AuthController = Depends(get_auth_controller)):
    return await auth_controller.login()


@authRouter.post("/signup")
async def signup(auth_controller: AuthController = Depends(get_auth_controller)):
    return await auth_controller.signup()


@authRouter.get("/verify")
async def verify(auth_controller: AuthController = Depends(get_auth_controller)):
    return await auth_controller.verify_email()


@authRouter.post("/refresh")
async def refresh(auth_controller: AuthController = Depends(get_auth_controller)):
    return await auth_controller.renew()


@authRouter.post("/logout")
async def logout(auth_controller: AuthController = Depends(get_auth_controller)):
    return await auth_controller.logout()


@authRouter.post("/google")
async def google(auth_controller: AuthController = Depends(get_auth_controller)):
    return await auth_controller.google()


@authRouter.post("/microsoft")
async def microsoft(auth_controller: AuthController = Depends(get_auth_controller)):
    return await auth_controller.microsoft()


@authRouter.post("/forgot-password")
async def forgot(auth_controller: AuthController = Depends(get_auth_controller)):
    return await auth_controller.forgot_password()


@authRouter.post("/change-password")
async def change(auth_controller: AuthController = Depends(get_auth_controller)):
    return await auth_controller.change_password()
