from fastapi import APIRouter, Depends, Request

from controller.categoryController import CategoryController
from dtos.categoryDtos import CreateCategoryRequest, UpdateCategoryRequest
from middleware.authMiddleware import get_current_user
from utilities.errorRaiser import raise_error
from utilities.logger import logger


async def get_category_controller(request: Request) -> CategoryController:
    """
    Resolve a scoped CategoryController from the IoC container stored
    in app.state, ensuring per-request lifecycle and dependency resolution.
    """
    try:
        container = request.app.state.container
        scope = request.state.scope

        controller = await container.resolve("CategoryController", scope)
        controller.request = request

        return controller

    except Exception as e:
        logger.error(f"[CategoryRoute] Resolving CategoryController failed: {e}")
        raise_error(e)


categoryRouter = APIRouter(tags=["Category"])


@categoryRouter.post("/")
async def createCategory(
    dto: CreateCategoryRequest,
    user_payload: dict = Depends(get_current_user),
    ctrl: CategoryController = Depends(get_category_controller),
):
    return await ctrl.createCategory(dto)


@categoryRouter.put("/{id}")
async def updateCategory(
    id: str,
    dto: UpdateCategoryRequest,
    user_payload: dict = Depends(get_current_user),
    ctrl: CategoryController = Depends(get_category_controller),
):
    return await ctrl.updateCategory(id, dto)


@categoryRouter.delete("/{id}")
async def deleteCategory(
    id: str,
    user_payload: dict = Depends(get_current_user),
    ctrl: CategoryController = Depends(get_category_controller),
):
    return await ctrl.deleteCategory(id)


@categoryRouter.get("/{id}")
async def getCategory(
    id: str, ctrl: CategoryController = Depends(get_category_controller)
):
    return await ctrl.getCategory(id)


@categoryRouter.get("/")
async def getAllCategories(ctrl: CategoryController = Depends(get_category_controller)):
    return await ctrl.getCategories()
