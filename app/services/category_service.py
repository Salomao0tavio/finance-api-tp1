"""Regras de negócio relacionadas a Category."""
from sqlalchemy.orm import Session

from app.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def create_category(self, name: str):
        if not name or not name.strip():
            raise ValueError("O nome da categoria não pode ser vazio")
        return self.repository.create(name=name)

    def get_all_categories(self):
        return self.repository.get_all()

    def get_category(self, category_id: int):
        return self.repository.get_by_id(category_id)

    def update_category(self, category_id: int, name: str):
        return self.repository.update(category_id, name=name)

    def delete_category(self, category_id: int) -> bool:
        return self.repository.delete(category_id)
