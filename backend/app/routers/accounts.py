# app/routers/accounts.py

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Optional
from app.database import get_db
from sqlalchemy.orm import Session
from app import models, schemas # Assuming you have models.py and schemas.py defined

router = APIRouter()

# Pydantic models for request and response data validation
# These define the structure and data types for your API requests and responses.
class AccountBase(BaseModel):
    name: str = Field(..., description="Name of the financial account")
    account_type: str = Field(..., description="Type of the account (e.g., checking, savings, credit card)")
    balance: float = Field(default=0.0, ge=0, description="Current balance of the account")

class AccountCreate(AccountBase):
    pass # No additional fields needed for creation beyond the base

class AccountUpdate(AccountBase):
    name: Optional[str] = None
    account_type: Optional[str] = None
    balance: Optional[float] = None

class AccountInDB(AccountBase):
    id: int
    owner_id: int # Assuming accounts are linked to users
    class Config:
        orm_mode = True # Enables Pydantic to read data from ORM objects

# API endpoints

# 1. Create a new account
@router.post("/", response_model=AccountInDB, status_code=status.HTTP_201_CREATED)
async def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    db_account = models.Account(**account.model_dump()) # Create a new account object from Pydantic model
    # You'd likely link the account to the authenticated user here (e.g., db_account.owner_id = current_user.id)
    db.add(db_account) # Add the account to the database session
    db.commit() # Commit the changes to the database
    db.refresh(db_account) # Refresh the object to get the latest data, including the generated ID
    return db_account

# 2. Get a list of all accounts for the current user
@router.get("/", response_model=List[AccountInDB])
async def get_accounts(db: Session = Depends(get_db)):
    # Assuming user authentication and fetching user-specific accounts
    # For now, let's fetch all accounts (you'd filter by owner_id in a real app)
    accounts = db.query(models.Account).all()
    return accounts

# 3. Get a single account by its ID
@router.get("/{account_id}", response_model=AccountInDB)
async def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    # You'd also check if the account belongs to the authenticated user
    return account

# 4. Update an existing account
@router.put("/{account_id}", response_model=AccountInDB)
async def update_account(account_id: int, account_update: AccountUpdate, db: Session = Depends(get_db)):
    db_account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    # Update account fields based on the Pydantic model
    update_data = account_update.model_dump(exclude_unset=True) # Exclude unset fields from update data
    for key, value in update_data.items():
        setattr(db_account, key, value)
    
    db.commit()
    db.refresh(db_account)
    return db_account

# 5. Delete an account
@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(account_id: int, db: Session = Depends(get_db)):
    db_account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    db.delete(db_account)
    db.commit()
    return {"message": "Account deleted successfully"}
