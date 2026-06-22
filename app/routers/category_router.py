"""Endpoints REST relacionados a Category."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.category_service import CategoryService
from app.schemas import CategoryCreate, CategoryOut

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryOut, status_code=201)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return CategoryService(db).create_category(name=payload.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return CategoryService(db).get_all_categories()


@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = CategoryService(db).get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return category


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, payload: CategoryCreate, db: Session = Depends(get_db)):
    category = CategoryService(db).update_category(category_id, name=payload.name)
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return category


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    deleted = CategoryService(db).delete_category(category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
