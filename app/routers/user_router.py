"""Endpoints REST relacionados a User."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.user_service import UserService
from app.schemas import UserCreate, UserUpdate, UserOut

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        return UserService(db).create_user(name=payload.name, email=payload.email)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return UserService(db).get_all_users()


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService(db).get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = UserService(db).update_user(user_id, name=payload.name, email=payload.email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = UserService(db).delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
