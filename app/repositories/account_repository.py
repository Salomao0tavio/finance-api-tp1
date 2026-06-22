"""Repositório responsável pelo acesso a dados de Account."""
from sqlalchemy.orm import Session

from app.models.account import Account


class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, initial_balance: float, user_id: int) -> Account:
        account = Account(name=name, initial_balance=initial_balance, user_id=user_id)
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def get_all(self):
        return self.db.query(Account).all()

    def get_by_id(self, account_id: int) -> Account | None:
        return self.db.query(Account).filter(Account.id == account_id).first()

    def get_by_user(self, user_id: int):
        return self.db.query(Account).filter(Account.user_id == user_id).all()

    def update(self, account_id: int, name: str | None = None) -> Account | None:
        account = self.get_by_id(account_id)
        if not account:
            return None
        if name is not None:
            account.name = name
        self.db.commit()
        self.db.refresh(account)
        return account

    def delete(self, account_id: int) -> bool:
        account = self.get_by_id(account_id)
        if not account:
            return False
        self.db.delete(account)
        self.db.commit()
        return True
