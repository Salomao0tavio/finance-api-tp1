"""Endpoints REST relacionados a Transaction."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.transaction_service import TransactionService
from app.schemas import TransactionCreate, TransactionOut

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionOut, status_code=201)
def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db)):
    try:
        return TransactionService(db).register_transaction(
            description=payload.description,
            amount=payload.amount,
            type=payload.type,
            account_id=payload.account_id,
            category_id=payload.category_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[TransactionOut])
def list_transactions(db: Session = Depends(get_db)):
    return TransactionService(db).get_all_transactions()


@router.get("/{transaction_id}", response_model=TransactionOut)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = TransactionService(db).get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return transaction


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    deleted = TransactionService(db).delete_transaction(transaction_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transação não encontrada")


@router.get("/report/{account_id}")
def report_by_category(account_id: int, db: Session = Depends(get_db)):
    return TransactionService(db).report_by_category(account_id)
