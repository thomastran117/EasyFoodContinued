from service.categoryService import CategoryService


class CategoryController:
    def __init__(self, category_service: CategoryService):
        self.category_service = category_service
