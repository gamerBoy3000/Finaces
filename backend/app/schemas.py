# backend/app/schemas.py
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List, Literal
from datetime import date

TxnType = Literal["expense", "income", "transfer"]

# ---- Accounts ----
class AccountBase(BaseModel):
    name: str
    type: str = "cash"

class AccountCreate(AccountBase):
    pass

class AccountOut(AccountBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# ---- Categories ----
class CategoryBase(BaseModel):
    name: str
    kind: Literal["expense", "income"] = "expense"

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# ---- Transactions ----
class TransactionBase(BaseModel):
    date: date = Field(default_factory=date.today)
    description: Optional[str] = None
    amount: float
    type: TxnType
    account_id: int
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None
    transfer_group: Optional[str] = None

    @field_validator("amount")
    def amount_not_zero(cls, v: float):
        if v == 0:
            raise ValueError("amount cannot be zero")
        return v

class TransactionCreate(TransactionBase):
    pass

class TransactionOut(TransactionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
