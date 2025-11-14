from __future__ import annotations
from typing import Optional, List
from datetime import timedelta
from schema.mongo_template import Category
from service.cacheService import CacheService
from utilities.errorRaiser import NotFoundException, BadRequestException


class CategoryService:
    """
    Fully JSON-safe Beanie + Redis service.
    Adds uniqueness check for category name.
    """

    def __init__(self, cache_service: CacheService, ttl_seconds: int = 300):
        self.cache = cache_service
        self.ttl = ttl_seconds

    def _cache_key_all(self) -> str:
        return "category:all"

    def _cache_key_one(self, category_id: str) -> str:
        return f"category:{category_id}"

    @staticmethod
    def _serialize_category(cat: Category) -> dict:
        return cat.model_dump(mode="json")

    @staticmethod
    def _deserialize_category(data: dict) -> Category:
        return Category(**data)

    async def getAllCategory(self) -> List[Category]:
        key = self._cache_key_all()
        cached = self.cache.get(key)

        if cached:
            return [self._deserialize_category(c) for c in cached]

        categories = await Category.find_all().to_list()
        self.cache.set(
            key,
            [self._serialize_category(c) for c in categories],
            expire=timedelta(seconds=self.ttl),
        )
        return categories

    async def getCategory(self, category_id: str) -> Category:
        key = self._cache_key_one(category_id)
        cached = self.cache.get(key)

        if cached:
            return self._deserialize_category(cached)

        category = await Category.get(category_id)
        if not category:
            raise NotFoundException(f"Category '{category_id}' does not exist")

        self.cache.set(key, self._serialize_category(category), expire=self.ttl)
        return category

    async def createCategory(
        self, name: str, description: Optional[str] = None
    ) -> Category:
        existing = await Category.find_one(Category.name == name)
        if existing:
            raise BadRequestException(f"Category name '{name}' already exists")

        category = Category(name=name, description=description)
        await category.insert()

        self.cache.delete(self._cache_key_all())
        return category

    async def updateCategory(self, category_id: str, name=None, description=None):
        category = await Category.get(category_id)
        if not category:
            raise NotFoundException(f"Category '{category_id}' does not exist")

        if name is not None and name != category.name:
            existing = await Category.find_one(Category.name == name)
            if existing:
                raise BadRequestException(f"Category name '{name}' already exists")

            category.name = name

        if description is not None:
            category.description = description

        await category.save()

        self.cache.set(
            self._cache_key_one(category_id),
            self._serialize_category(category),
            expire=self.ttl,
        )
        self.cache.delete(self._cache_key_all())

        return category

    async def deleteCategory(self, category_id: str) -> bool:
        category = await Category.get(category_id)
        if not category:
            raise NotFoundException(f"Category '{category_id}' does not exist")

        await category.delete()

        self.cache.delete(self._cache_key_one(category_id))
        self.cache.delete(self._cache_key_all())

        return True
