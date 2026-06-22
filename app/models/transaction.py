"""Modelo de dados da Transação (receita ou despesa)."""
import enum
from datetime import datetime

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Enum, String
from sqlalchemy.orm import relationship

from app.database import Base


class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
