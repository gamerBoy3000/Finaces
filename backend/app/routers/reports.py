from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/summary", response_model=schemas.MonthlySummary)
def monthly_summary(month: str, db: Session = Depends(get_db)):
    return crud.monthly_summary(db, month)

@router.get("/budget-progress", response_model=schemas.BudgetProgress)
def budget_progress(month: str, db: Session = Depends(get_db)):
    return crud.budget_progress(db, month)
