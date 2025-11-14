from __future__ import annotations
from typing import Optional, List
from datetime import timedelta

from schema.mongo_template import Category
from service.cacheService import CacheService
from utilities.errorRaiser import NotFoundException, BadRequestException


class CategoryService:
    def __init__(self, cache_service: CacheService, ttl_seconds: int = 300):
        self.cache = cache_service
        self.ttl = ttl_seconds

    def _key_all(self) -> str:
        return "category:all"

    def _key_one(self, cid: str) -> str:
        return f"category:{cid}"

    async def getAllCategory(self) -> List[Category]:
        key = self._key_all()
        cached = self.cache.get(key)

        if cached:
            return self.cache.decode_model(cached, Category)

        categories = await Category.find_all().to_list()

        self.cache.set(
            key,
            categories,
            expire=timedelta(seconds=self.ttl),
        )
        return categories

    async def getCategory(self, category_id: str) -> Category:
        key = self._key_one(category_id)
        cached = self.cache.get(key)
        if cached:
            return self.cache.decode_model(cached, Category)

        category = await Category.get(category_id)
        if not category:
            raise NotFoundException(f"Category '{category_id}' does not exist")

        self.cache.set(key, category, expire=self.ttl)
        return category

    async def createCategory(
        self, name: str, description: Optional[str] = None
    ) -> Category:
        existing = await Category.find_one(Category.name == name)
        if existing:
            raise BadRequestException(f"Category '{name}' already exists")

        category = Category(name=name, description=description)
        await category.insert()

        self.cache.delete(self._key_all())
        return category

    async def updateCategory(self, category_id: str, name=None, description=None):
        category = await Category.get(category_id)
        if not category:
            raise NotFoundException(f"Category '{category_id}' does not exist")

        if name and name != category.name:
            exists = await Category.find_one(Category.name == name)
            if exists:
                raise BadRequestException(f"Category name '{name}' already exists")
            category.name = name

        if description is not None:
            category.description = description

        await category.save()

        self.cache.set(self._key_one(category_id), category, expire=self.ttl)
        self.cache.delete(self._key_all())

        return category

    async def deleteCategory(self, category_id: str) -> bool:
        category = await Category.get(category_id)
        if not category:
            raise NotFoundException(f"Category '{category_id}' does not exist")

        await category.delete()

        self.cache.delete(self._key_one(category_id))
        self.cache.delete(self._key_all())

        return True
