from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

class AccountBase(BaseModel):
    name: str
    type: str = "cash"

class AccountCreate(AccountBase):
    id: int
    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    kind: str = "expense" #expense or income

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True
    
class TransactionBase(BaseModel):
    data: date
    description:str
    amount: Decimal
    type: str # expense, income,, transfer
    account_id: int

class TransactionResponse(TransactionCreate):
    id: int
    date: datetime
