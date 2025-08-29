from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas

router = APIRouter(prefix="/budgets", tags=["budgets"])

@router.post("", response_model=schemas.Budget)
def upsert_budget(data: schemas.BudgetCreate, db: Session = Depends(get_db)):
    b = crud.upsert_budget(db, data)
    return schemas.Budget(id=b.id, month=b.month, category_id=b.category_id, amount=round(b.amount_cents/100.0, 2))

@router.get("", response_model=list[schemas.Budget])
def list_budgets(month: str | None = None, db: Session = Depends(get_db)):
    buds = crud.list_budgets(db, month)
    return [schemas.Budget(id=b.id, month=b.month, category_id=b.category_id, amount=round(b.amount_cents/100.0, 2)) for b in buds]
