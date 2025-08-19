
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4

router = APIRouter()

# Dummy in-memory "database"
transactions = []

class Transaction(BaseModel):
    id: str
    amount: float
    description: str

@router.post("/transactions/", response_model=Transaction)
def create_transaction(transaction: Transaction):
    transaction.id = str(uuid4())
    transactions.append(transaction)
    return transaction

@router.get("/transactions/", response_model=List[Transaction])
def get_transactions():
    return transactions


