"""Regras de negócio relacionadas a User."""
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, name: str, email: str):
        if not name or not name.strip():
            raise ValueError("O nome do usuário não pode ser vazio")
        if "@" not in email:
            raise ValueError("Email inválido")
        if self.repository.get_by_email(email):
            raise ValueError("Já existe um usuário com esse email")
        return self.repository.create(name=name, email=email)

    def get_all_users(self):
        return self.repository.get_all()

    def get_user(self, user_id: int):
        return self.repository.get_by_id(user_id)

    def update_user(self, user_id: int, name: str | None = None, email: str | None = None):
        return self.repository.update(user_id, name=name, email=email)

    def delete_user(self, user_id: int) -> bool:
        return self.repository.delete(user_id)
