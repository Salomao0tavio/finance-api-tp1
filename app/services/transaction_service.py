"""Regras de negócio relacionadas a Transaction."""
from collections import defaultdict
from sqlalchemy.orm import Session

from app.repositories.transaction_repository import TransactionRepository
from app.repositories.account_repository import AccountRepository
from app.repositories.category_repository import CategoryRepository
from app.models.transaction import TransactionType


class TransactionService:
    def __init__(self, db: Session):
        self.repository = TransactionRepository(db)
        self.account_repository = AccountRepository(db)
        self.category_repository = CategoryRepository(db)

    def register_transaction(
        self,
        description: str,
        amount: float,
        type: TransactionType,
        account_id: int,
        category_id: int,
    ):
        if amount <= 0:
            raise ValueError("O valor da transação deve ser maior que zero")
        if not self.account_repository.get_by_id(account_id):
            raise ValueError("Conta não encontrada")
        if not self.category_repository.get_by_id(category_id):
            raise ValueError("Categoria não encontrada")

        if type == TransactionType.EXPENSE:
            self._validate_sufficient_balance(account_id, amount)

        return self.repository.create(
            description=description,
            amount=amount,
            type=type,
            account_id=account_id,
            category_id=category_id,
        )

    def _validate_sufficient_balance(self, account_id: int, expense_amount: float):
        """Impede registrar uma despesa que deixaria o saldo da conta negativo."""
        from app.services.account_service import AccountService

        account_service = AccountService(self.account_repository.db)
        current_balance = account_service.calculate_balance(account_id)
        if current_balance - expense_amount < 0:
            raise ValueError("Saldo insuficiente para registrar essa despesa")

    def get_all_transactions(self):
        return self.repository.get_all()

    def get_transaction(self, transaction_id: int):
        return self.repository.get_by_id(transaction_id)

    def get_transactions_by_account(self, account_id: int):
        return self.repository.get_by_account(account_id)

    def delete_transaction(self, transaction_id: int) -> bool:
        return self.repository.delete(transaction_id)

    def report_by_category(self, account_id: int) -> dict:
        """Agrupa o total de despesas e receitas por categoria, para uma conta."""
        transactions = self.repository.get_by_account(account_id)
        report = defaultdict(lambda: {"income": 0.0, "expense": 0.0})

        for transaction in transactions:
            category_name = transaction.category.name
            if transaction.type == TransactionType.INCOME:
                report[category_name]["income"] += transaction.amount
            else:
                report[category_name]["expense"] += transaction.amount

        return dict(report)
