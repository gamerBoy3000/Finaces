from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
def create_category(data: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, data)

@router.get("", response_model=list[schemas.Category])
def list_categories(db: Session = Depends(get_db)):
    return crud.list_categories(db)
