from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date

class AccountBase(BaseModel):
    name: str
    type: str = "cash"

class AccountCreate(AccountBase): pass

class Account(AccountBase):
    id: int
    class Config: from_attributes = True

class CategoryBase(BaseModel):
    name: str
    kind: str = "expense"  # expense or income

class CategoryCreate(CategoryBase): pass

class Category(CategoryBase):
    id: int
    class Config: from_attributes = True

class TransactionBase(BaseModel):
    date: date
    description: str
    amount: float  # expose as float; stored as cents
    type: str  # expense, income, transfer
    account_id: int
    category_id: Optional[int] = None
    tags: Optional[list[str]] = None
    transfer_group: Optional[str] = None

    @field_validator("type")
    def validate_type(cls, v):
        if v not in {"expense", "income", "transfer"}:
            raise ValueError("type must be one of expense|income|transfer")
        return v

class TransactionCreate(TransactionBase): pass

class Transaction(TransactionBase):
    id: int
    class Config: from_attributes = True

class BudgetBase(BaseModel):
    month: str  # YYYY-MM
    category_id: int
    amount: float

class BudgetCreate(BudgetBase): pass

class Budget(BudgetBase):
    id: int
    class Config: from_attributes = True

class MonthlyCategorySummary(BaseModel):
    category: str
    spent: float
    income: float

class MonthlySummary(BaseModel):
    month: str
    total_expense: float
    total_income: float
    by_category: list[MonthlyCategorySummary]

class BudgetProgressItem(BaseModel):
    category: str
    budget: float
    spent: float
    remaining: float

class BudgetProgress(BaseModel):
    month: str
    items: list[BudgetProgressItem]
