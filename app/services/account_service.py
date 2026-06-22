"""Regras de negócio relacionadas a Account."""
from sqlalchemy.orm import Session

from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.user_repository import UserRepository
from app.models.transaction import TransactionType


class AccountService:
    def __init__(self, db: Session):
        self.repository = AccountRepository(db)
        self.transaction_repository = TransactionRepository(db)
        self.user_repository = UserRepository(db)

    def create_account(self, name: str, initial_balance: float, user_id: int):
        if not name or not name.strip():
            raise ValueError("O nome da conta não pode ser vazio")
        if not self.user_repository.get_by_id(user_id):
            raise ValueError("Usuário não encontrado")
        return self.repository.create(name=name, initial_balance=initial_balance, user_id=user_id)

    def get_all_accounts(self):
        return self.repository.get_all()

    def get_account(self, account_id: int):
        return self.repository.get_by_id(account_id)

    def get_accounts_by_user(self, user_id: int):
        return self.repository.get_by_user(user_id)

    def update_account(self, account_id: int, name: str | None = None):
        return self.repository.update(account_id, name=name)

    def delete_account(self, account_id: int) -> bool:
        return self.repository.delete(account_id)

    def calculate_balance(self, account_id: int) -> float:
        """
        Calcula o saldo atual da conta:
        saldo inicial + soma das receitas - soma das despesas.
        """
        account = self.repository.get_by_id(account_id)
        if not account:
            raise ValueError("Conta não encontrada")

        transactions = self.transaction_repository.get_by_account(account_id)
        balance = account.initial_balance
        for transaction in transactions:
            if transaction.type == TransactionType.INCOME:
                balance += transaction.amount
            else:
                balance -= transaction.amount
        return balance
