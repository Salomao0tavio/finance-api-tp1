"""Endpoints REST relacionados a Account."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.account_service import AccountService
from app.schemas import AccountCreate, AccountUpdate, AccountOut, BalanceOut

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/", response_model=AccountOut, status_code=201)
def create_account(payload: AccountCreate, db: Session = Depends(get_db)):
    try:
        return AccountService(db).create_account(
            name=payload.name, initial_balance=payload.initial_balance, user_id=payload.user_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[AccountOut])
def list_accounts(db: Session = Depends(get_db)):
    return AccountService(db).get_all_accounts()


@router.get("/{account_id}", response_model=AccountOut)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = AccountService(db).get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return account


@router.put("/{account_id}", response_model=AccountOut)
def update_account(account_id: int, payload: AccountUpdate, db: Session = Depends(get_db)):
    account = AccountService(db).update_account(account_id, name=payload.name)
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return account


@router.delete("/{account_id}", status_code=204)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    deleted = AccountService(db).delete_account(account_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conta não encontrada")


@router.get("/{account_id}/balance", response_model=BalanceOut)
def get_balance(account_id: int, db: Session = Depends(get_db)):
    try:
        balance = AccountService(db).calculate_balance(account_id)
        return BalanceOut(account_id=account_id, balance=balance)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
