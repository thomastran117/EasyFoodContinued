from fastapi import Request
from fastapi.responses import JSONResponse
from dtos.categoryDtos import CreateCategoryRequest, UpdateCategoryRequest
from utilities.logger import logger
from utilities.errorRaiser import raise_error, BadRequestException
from service.categoryService import CategoryService
from bson import ObjectId


class CategoryController:
    def __init__(self, category_service: CategoryService):
        self.category_service = category_service
        self.request: Request | None = None

    async def createCategory(self, dto: CreateCategoryRequest):
        try:
            cat = await self.category_service.createCategory(dto.name, dto.description)
            return JSONResponse(
                content={
                    "status": "success",
                    "data": cat.model_dump(mode="json"),
                },
                status_code=201,
            )
        except Exception as e:
            raise_error(e)

    async def updateCategory(self, id: str, dto: UpdateCategoryRequest):
        try:
            if not ObjectId.is_valid(id):
                raise BadRequestException(f"'{id}' is not a valid Category ID")
            category = await self.category_service.updateCategory(
                id, dto.name, dto.description
            )

            return JSONResponse(
                {"status": "success", "data": category.model_dump(mode="json")}
            )
        except Exception as e:
            raise_error(e)

    async def deleteCategory(self, id: str):
        try:
            if not ObjectId.is_valid(id):
                raise BadRequestException(f"'{id}' is not a valid Category ID")
            deleted = await self.category_service.deleteCategory(id)

            return JSONResponse({"status": "success"}, 200)
        except Exception as e:
            raise_error(e)

    async def getCategory(self, id: str):
        try:
            if not ObjectId.is_valid(id):
                raise BadRequestException(f"'{id}' is not a valid Category ID")
            category = await self.category_service.getCategory(id)

            return JSONResponse(
                {"status": "success", "data": category.model_dump(mode="json")}
            )
        except Exception as e:
            raise_error(e)

    async def getCategories(self):
        try:
            cats = await self.category_service.getAllCategory()
            return JSONResponse(
                {
                    "status": "success",
                    "count": len(cats),
                    "data": [c.model_dump(mode="json") for c in cats],
                }
            )
        except Exception as e:
            raise_error(e)
