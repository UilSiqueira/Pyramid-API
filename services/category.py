from models.category import Category as CategoryModel
from core.db.connection import Session
from pyramid.httpexceptions import HTTPNotFound


class CategoryService:
    def __init__(self, db_session: Session) -> None:
        self._category_model = CategoryModel(db_session)

    def add_category(self, name: str, slug: str):
        self._category_model.add(name, slug)
        
    def list_categories(self):
        categories = self._category_model.list()
        return categories
        
    def delete_category(self, id: str):
        categories = self._category_model.list(id)
        if not categories:
            raise HTTPNotFound('Category not found')
        self._category_model.delete(id)