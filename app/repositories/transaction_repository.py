"""Repositório responsável pelo acesso a dados de Transaction."""
from sqlalchemy.orm import Session

from app.models.transaction import Transaction, TransactionType


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        description: str,
        amount: float,
        type: TransactionType,
        account_id: int,
        category_id: int,
    ) -> Transaction:
        transaction = Transaction(
            description=description,
            amount=amount,
            type=type,
            account_id=account_id,
            category_id=category_id,
        )
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def get_all(self):
        return self.db.query(Transaction).all()

    def get_by_id(self, transaction_id: int) -> Transaction | None:
        return self.db.query(Transaction).filter(Transaction.id == transaction_id).first()

    def get_by_account(self, account_id: int):
        return self.db.query(Transaction).filter(Transaction.account_id == account_id).all()

    def delete(self, transaction_id: int) -> bool:
        transaction = self.get_by_id(transaction_id)
        if not transaction:
            return False
        self.db.delete(transaction)
        self.db.commit()
        return True
