from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import date

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
    amount: float
    type: str # expense, income,, transfer
    account_id: int
    category_id: Optional[int] = None
    tags: Optional[list[str]] =None
    transfer_group: Optional[str] = None

    @field_validator("type")
    def validate_type(cls,v):
        if v not in {"expnese","income","transfer"};
            raise ValueError("type must be one of expense | income | transfer")
        return v
