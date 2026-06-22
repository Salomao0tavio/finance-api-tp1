"""Schemas Pydantic usados para validar requests e formatar responses da API."""
from datetime import datetime
from pydantic import BaseModel, EmailStr

from app.models.transaction import TransactionType


# ---------- User ----------
class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


# ---------- Account ----------
class AccountCreate(BaseModel):
    name: str
    initial_balance: float = 0.0
    user_id: int


class AccountUpdate(BaseModel):
    name: str | None = None


class AccountOut(BaseModel):
    id: int
    name: str
    initial_balance: float
    user_id: int

    class Config:
        from_attributes = True


class BalanceOut(BaseModel):
    account_id: int
    balance: float


# ---------- Category ----------
class CategoryCreate(BaseModel):
    name: str


class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# ---------- Transaction ----------
class TransactionCreate(BaseModel):
    description: str
    amount: float
    type: TransactionType
    account_id: int
    category_id: int


class TransactionOut(BaseModel):
    id: int
    description: str
    amount: float
    type: TransactionType
    created_at: datetime
    account_id: int
    category_id: int

    class Config:
        from_attributes = True
