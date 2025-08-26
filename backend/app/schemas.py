# Example using Pydantic for API request/response validation
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Amount of the transaction, must be positive")
    description: str = Field(..., min_length=1, max_length=200)
    category: str = Field(..., min_length=1, max_length=50)
    account_id: int

class TransactionResponse(TransactionCreate):
    id: int
    date: datetime
