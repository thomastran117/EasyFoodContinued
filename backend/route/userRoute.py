from fastapi import APIRouter, Depends, File, Request, UploadFile

from controller.userController import UserController
from dtos.userDtos import UpdateUserDto
from middleware.authMiddleware import get_current_user
from utilities.errorRaiser import raise_error
from utilities.logger import logger

userRouter = APIRouter(tags=["User"])


async def get_user_controller(request: Request) -> UserController:
    """
    Resolve a scoped UserController from the IoC container stored
    in app.state, ensuring per-request lifecycle and dependency resolution.
    """
    try:
        container = request.app.state.container

        async with container.create_scope() as scope:
            controller = await container.resolve("UserController", scope)
            controller.request = request
            return controller
    except Exception as e:
        logger.error(f"[UserRoute] Resolving controller failed: {e}")
        raise_error(e)


@userRouter.get("/{id}")
async def get_user(
    id: int, user_controller: UserController = Depends(get_user_controller)
):
    return await user_controller.getUserByID(id)


@userRouter.put("/update")
async def update_user(
    update: UpdateUserDto,
    user_payload: dict = Depends(get_current_user),
    user_controller: UserController = Depends(get_user_controller),
):
    return await user_controller.updateUser(user_payload, update)


@userRouter.delete("/delete")
async def delete_user(
    user_payload: dict = Depends(get_current_user),
    user_controller: UserController = Depends(get_user_controller),
):
    return await user_controller.deleteUser(user_payload)


@userRouter.post("/avatar")
async def update_avatar(
    file: UploadFile = File(...),
    user_payload: dict = Depends(get_current_user),
    user_controller: UserController = Depends(get_user_controller),
):
    return await user_controller.updateAvatar(user_payload, file)
