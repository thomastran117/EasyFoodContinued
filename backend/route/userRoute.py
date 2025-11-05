from fastapi import APIRouter, Depends
from controller.userController import UserController
from resources.container import container

userRouter = APIRouter(tags=["User"])


def get_user_controller() -> UserController:
    """Resolves an UserController with lifetimes managed by the container."""
    with container.create_scope() as scope:
        return container.resolve("UserController", scope)


@userRouter.get("/{id}")
async def login(user_controller: UserController = Depends(get_user_controller)):
    return await user_controller.get_user()


@userRouter.put("/{id}")
async def signup(user_controller: UserController = Depends(get_user_controller)):
    return await user_controller.update_user()


@userRouter.delete("/{id}")
async def verify(user_controller: UserController = Depends(get_user_controller)):
    return await user_controller.delete_user()


@userRouter.post("/avatar")
async def refresh(user_controller: UserController = Depends(get_user_controller)):
    return await user_controller.update_avatar()
