"""Repositório responsável pelo acesso a dados de Category."""
from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str) -> Category:
        category = Category(name=name)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def get_all(self):
        return self.db.query(Category).all()

    def get_by_id(self, category_id: int) -> Category | None:
        return self.db.query(Category).filter(Category.id == category_id).first()

    def update(self, category_id: int, name: str) -> Category | None:
        category = self.get_by_id(category_id)
        if not category:
            return None
        category.name = name
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category_id: int) -> bool:
        category = self.get_by_id(category_id)
        if not category:
            return False
        self.db.delete(category)
        self.db.commit()
        return True
