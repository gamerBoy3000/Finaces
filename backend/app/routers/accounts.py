from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("", response_model=schemas.Account, status_code=status.HTTP_201_CREATED)
def create_account(data: schemas.AccountCreate, db: Session = Depends(get_db)):
    return crud.create_account(db, data)

@router.get("", response_model=list[schemas.Account])
def list_accounts(db: Session = Depends(get_db)):
    return crud.list_accounts(db)
