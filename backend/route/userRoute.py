from fastapi import APIRouter, Depends, File, Request, UploadFile

from controller.userController import UserController
from dtos.userDtos import UpdateUserDto
from middleware.authMiddleware import get_current_user

userRouter = APIRouter(tags=["User"])


async def get_user_controller(request: Request) -> UserController:
    """
    Resolve a scoped UserController from the IoC container stored
    in app.state, ensuring per-request lifecycle and dependency resolution.
    """
    container = request.app.state.container

    async with container.create_scope() as scope:
        controller = await container.resolve("UserController", scope)
        controller.request = request
        return controller


@userRouter.get("/{id}")
async def get_user(
    id: int, user_controller: UserController = Depends(get_user_controller)
):
    return await user_controller.get_user(id)


@userRouter.put("/update")
async def update_user(
    update: UpdateUserDto,
    user_payload: dict = Depends(get_current_user),
    user_controller: UserController = Depends(get_user_controller),
):
    return await user_controller.update_user(user_payload, update)


@userRouter.delete("/delete")
async def delete_user(
    user_payload: dict = Depends(get_current_user),
    user_controller: UserController = Depends(get_user_controller),
):
    return await user_controller.delete_user(user_payload)


@userRouter.post("/avatar")
async def update_avatar(
    file: UploadFile = File(...),
    user_payload: dict = Depends(get_current_user),
    user_controller: UserController = Depends(get_user_controller),
):
    return await user_controller.update_avatar(user_payload, file)
