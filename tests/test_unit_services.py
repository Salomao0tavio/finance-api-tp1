"""
Testes de unidade: testam a lógica de negócio dos services isoladamente,
usando o banco SQLite em memória (sem subir a API).
"""
import pytest

from app.services.user_service import UserService
from app.services.account_service import AccountService
from app.services.category_service import CategoryService
from app.services.transaction_service import TransactionService
from app.models.transaction import TransactionType


def test_create_user_success(db_session):
    user = UserService(db_session).create_user(name="Kaio", email="kaio@example.com")
    assert user.id is not None
    assert user.name == "Kaio"


def test_create_user_with_invalid_email_raises_error(db_session):
    with pytest.raises(ValueError):
        UserService(db_session).create_user(name="Kaio", email="email-invalido")


def test_create_user_with_duplicate_email_raises_error(db_session):
    service = UserService(db_session)
    service.create_user(name="Kaio", email="kaio@example.com")
    with pytest.raises(ValueError):
        service.create_user(name="Outro", email="kaio@example.com")


def test_calculate_balance_with_no_transactions_returns_initial_balance(db_session):
    user = UserService(db_session).create_user(name="Kaio", email="kaio@example.com")
    account = AccountService(db_session).create_account(
        name="Carteira", initial_balance=100.0, user_id=user.id
    )
    balance = AccountService(db_session).calculate_balance(account.id)
    assert balance == 100.0


def test_calculate_balance_with_income_and_expense(db_session):
    user = UserService(db_session).create_user(name="Kaio", email="kaio@example.com")
    account = AccountService(db_session).create_account(
        name="Carteira", initial_balance=100.0, user_id=user.id
    )
    category = CategoryService(db_session).create_category(name="Salário")

    TransactionService(db_session).register_transaction(
        description="Salário de junho",
        amount=1000.0,
        type=TransactionType.INCOME,
        account_id=account.id,
        category_id=category.id,
    )
    TransactionService(db_session).register_transaction(
        description="Mercado",
        amount=300.0,
        type=TransactionType.EXPENSE,
        account_id=account.id,
        category_id=category.id,
    )

    balance = AccountService(db_session).calculate_balance(account.id)
    assert balance == 800.0  # 100 + 1000 - 300


def test_register_expense_with_insufficient_balance_raises_error(db_session):
    user = UserService(db_session).create_user(name="Kaio", email="kaio@example.com")
    account = AccountService(db_session).create_account(
        name="Carteira", initial_balance=50.0, user_id=user.id
    )
    category = CategoryService(db_session).create_category(name="Lazer")

    with pytest.raises(ValueError):
        TransactionService(db_session).register_transaction(
            description="Viagem",
            amount=500.0,
            type=TransactionType.EXPENSE,
            account_id=account.id,
            category_id=category.id,
        )


def test_register_transaction_with_negative_amount_raises_error(db_session):
    user = UserService(db_session).create_user(name="Kaio", email="kaio@example.com")
    account = AccountService(db_session).create_account(
        name="Carteira", initial_balance=100.0, user_id=user.id
    )
    category = CategoryService(db_session).create_category(name="Outros")

    with pytest.raises(ValueError):
        TransactionService(db_session).register_transaction(
            description="Transação inválida",
            amount=-10.0,
            type=TransactionType.EXPENSE,
            account_id=account.id,
            category_id=category.id,
        )
