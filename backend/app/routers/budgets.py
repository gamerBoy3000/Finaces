# app/routers/budgets.py

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

from app.database import get_db
from sqlalchemy.orm import Session
from app import models, schemas # Assuming you have models.py and schemas.py defined
# from app.dependencies import get_current_user # Assuming user authentication dependency

router = APIRouter()

# Pydantic models for request and response data validation
class BudgetBase(BaseModel):
    name: str = Field(..., description="Name of the budget (e.g., 'Monthly Spending', 'Travel Fund')")
    category: str = Field(..., description="Category for the budget (e.g., 'Groceries', 'Utilities', 'Entertainment')")
    amount: float = Field(..., gt=0, description="Total amount allocated for this budget category")
    start_date: date = Field(..., description="Start date of the budget period")
    end_date: date = Field(..., description="End date of the budget period")

class BudgetCreate(BudgetBase):
    pass

class BudgetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    amount: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class BudgetInDB(BudgetBase):
    id: int
    user_id: int  # Link to the user who owns this budget
    # You might also want to add fields like 'current_spend' or 'remaining_amount'
    # that are calculated based on transactions and linked to this budget
    class Config:
        orm_mode = True

# API endpoints

# 1. Create a new budget
@router.post("/", response_model=BudgetInDB, status_code=status.HTTP_201_CREATED)
async def create_budget(
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    # current_user: models.User = Depends(get_current_user) # Uncomment for authentication
):
    # db_budget = models.Budget(**budget.dict(), user_id=current_user.id) # For authenticated users
    db_budget = models.Budget(**budget.model_dump()) # Placeholder, replace with authenticated user's ID
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

# 2. Get all budgets for the current user
@router.get("/", response_model=List[BudgetInDB])
async def get_budgets(
    db: Session = Depends(get_db),
    # current_user: models.User = Depends(get_current_user) # Uncomment for authentication
):
    # budgets = db.query(models.Budget).filter(models.Budget.user_id == current_user.id).all() # For authenticated users
    budgets = db.query(models.Budget).all() # Placeholder, replace with authenticated user's budgets
    return budgets

# 3. Get a specific budget by ID
@router.get("/{budget_id}", response_model=BudgetInDB)
async def get_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    # current_user: models.User = Depends(get_current_user) # Uncomment for authentication
):
    budget = db.query(models.Budget).filter(models.Budget.id == budget_id).first() # Add user_id filter for auth
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    # if budget.user_id != current_user.id: # Check if budget belongs to the user
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this budget")
    return budget

# 4. Update an existing budget
@router.put("/{budget_id}", response_model=BudgetInDB)
async def update_budget(
    budget_id: int,
    budget_update: BudgetUpdate,
    db: Session = Depends(get_db),
    # current_user: models.User = Depends(get_current_user) # Uncomment for authentication
):
    db_budget = db.query(models.Budget).filter(models.Budget.id == budget_id).first() # Add user_id filter for auth
    if not db_budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    # if db_budget.user_id != current_user.id: # Check if budget belongs to the user
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this budget")

    update_data = budget_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_budget, key, value)
    
    db.commit()
    db.refresh(db_budget)
    return db_budget

# 5. Delete a budget
@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    # current_user: models.User = Depends(get_current_user) # Uncomment for authentication
):
    db_budget = db.query(models.Budget).filter(models.Budget.id == budget_id).first() # Add user_id filter for auth
    if not db_budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    # if db_budget.user_id != current_user.id: # Check if budget belongs to the user
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this budget")

    db.delete(db_budget)
    db.commit()
    return {"message": "Budget deleted successfully"}

# 6. (Optional) Get budget summary or spending trends
# This endpoint would involve querying transactions and linking them to budgets
# @router.get("/summary", response_model=BudgetSummary) # Assuming BudgetSummary Pydantic model
# async def get_budget_summary(
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user)
# ):
#     # Logic to fetch transactions, categorize them, and compare against budgets
#     # For example:
#     # transactions = db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id).all()
#     # budgets = db.query(models.Budget).filter(models.Budget.user_id == current_user.id).all()
#     # Calculate spending for each budget category
#     # Return a summary object
#     pass
