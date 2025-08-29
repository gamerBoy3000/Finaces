from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from ..database import get_db
from .. import crud, schemas

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("", response_model=schemas.Transaction)
def create_transaction(data: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db, data)

@router.get("", response_model=list[schemas.Transaction])
def list_transactions(
    start: date | None = None, end: date | None = None,
    account_id: int | None = None, category_id: int | None = None,
    tag: str | None = None, search: str | None = None, type: str | None = None,
    limit: int = Query(100, le=500), offset: int = 0, db: Session = Depends(get_db)
):
    txs = crud.list_transactions(db, start, end, account_id, category_id, tag, search, type, limit, offset)
    return [schemas.Transaction(
        id=t.id, date=t.date, description=t.description,
        amount=round(t.amount_cents/100.0, 2), type=t.type.value,
        account_id=t.account_id, category_id=t.category_id,
        tags=[tag.name for tag in t.tags] if t.tags else [],
        transfer_group=t.transfer_group
    ) for t in txs]
