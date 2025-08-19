# app/routers/reports.py

from fastapi import APIRouter, Depends, Query, status, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Union, Optional
from datetime import date, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.database import get_db
from app import models, schemas # Your SQLAlchemy models and Pydantic schemas
# from app.dependencies import get_current_user # Authentication dependency

router = APIRouter()

# Pydantic Models for Report Data Structures
# These define the shape of the data returned by your reporting endpoints

class IncomeExpenseByCategory(BaseModel):
    category: str
    income: float
    expense: float
    net: float

class IncomeExpenseSummary(BaseModel):
    total_income: float
    total_expense: float
    net_income: float
    by_category: List[IncomeExpenseByCategory]

class CashFlowEntry(BaseModel):
    date: date
    inflow: float
    outflow: float
    net_cash_flow: float

class CashFlowReport(BaseModel):
    start_date: date
    end_date: date
    entries: List[CashFlowEntry]

class NetWorthSnapshot(BaseModel):
    date: date
    assets: float
    liabilities: float
    net_worth: float

class NetWorthReport(BaseModel):
    snapshots: List[NetWorthSnapshot]

# API Endpoints for Reports

# 1. Income/Expense Report by Category
@router.get("/income-expense/summary", response_model=IncomeExpenseSummary)
async def get_income_expense_summary(
    start_date: date = Query(..., description="Start date for the report (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date for the report (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    # current_user: models.User = Depends(get_current_user),
):
    """
    Generates a summary report of income and expenses, categorized by transaction categories.
    """
    # Filter transactions within the specified date range and for the current user
    transactions_query = db.query(models.Transaction).\
        filter(models.Transaction.date >= start_date, models.Transaction.date <= end_date).\
        # filter(models.Transaction.user_id == current_user.id) # For authenticated users

    transactions = transactions_query.all()

    # Aggregate by category
    category_data: Dict[str, Dict[str, float]] = {}
    total_income = 0.0
    total_expense = 0.0

    for transaction in transactions:
        category_name = transaction.category.name if transaction.category else "Uncategorized"
        if category_name not in category_data:
            category_data[category_name] = {"income": 0.0, "expense": 0.0}

        if transaction.type == "income":
            category_data[category_name]["income"] += transaction.amount
            total_income += transaction.amount
        elif transaction.type == "expense":
            category_data[category_name]["expense"] += transaction.amount
            total_expense += transaction.amount

    by_category_list = []
    for category, amounts in category_data.items():
        by_category_list.append(
            IncomeExpenseByCategory(
                category=category,
                income=amounts["income"],
                expense=amounts["expense"],
                net=amounts["income"] - amounts["expense"],
            )
        )

    return IncomeExpenseSummary(
        total_income=total_income,
        total_expense=total_expense,
        net_income=total_income - total_expense,
        by_category=by_category_list,
    )

# 2. Cash Flow Report
@router.get("/cash-flow", response_model=CashFlowReport)
async def get_cash_flow_report(
    start_date: date = Query(..., description="Start date for the report (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date for the report (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    # current_user: models.User = Depends(get_current_user),
):
    """
    Generates a cash flow report showing daily inflows, outflows, and net cash flow.
    """
    cash_flow_entries: Dict[date, Dict[str, float]] = {}

    transactions_query = db.query(models.Transaction).\
        filter(models.Transaction.date >= start_date, models.Transaction.date <= end_date).\
        # filter(models.Transaction.user_id == current_user.id) # For authenticated users
    
    transactions = transactions_query.all()

    for transaction in transactions:
        tx_date = transaction.date
        if tx_date not in cash_flow_entries:
            cash_flow_entries[tx_date] = {"inflow": 0.0, "outflow": 0.0}
        
        if transaction.type == "income":
            cash_flow_entries[tx_date]["inflow"] += transaction.amount
        elif transaction.type == "expense":
            cash_flow_entries[tx_date]["outflow"] += transaction.amount
        # Transfers could be handled as both inflow/outflow to different accounts

    sorted_dates = sorted(cash_flow_entries.keys())
    report_entries = []
    for d in sorted_dates:
        inflow = cash_flow_entries[d]["inflow"]
        outflow = cash_flow_entries[d]["outflow"]
        report_entries.append(
            CashFlowEntry(
                date=d,
                inflow=inflow,
                outflow=outflow,
                net_cash_flow=inflow - outflow,
            )
        )
    
    return CashFlowReport(
        start_date=start_date,
        end_date=end_date,
        entries=report_entries
    )

# 3. Net Worth Report (Simplified)
@router.get("/net-worth", response_model=NetWorthReport)
async def get_net_worth_report(
    db: Session = Depends(get_db),
    # current_user: models.User = Depends(get_current_user),
):
    """
    Generates a simplified net worth report based on current account balances.
    A more comprehensive report would track net worth over time.
    """
    assets = 0.0
    liabilities = 0.0

    accounts_query = db.query(models.Account).\
        # filter(models.Account.owner_id == current_user.id) # For authenticated users
        all()

    for account in accounts_query:
        if account.account_type in ["checking", "savings", "investment"]: # Define asset types
            assets += account.balance
        elif account.account_type in ["credit_card", "loan"]: # Define liability types
            liabilities += account.balance # Assuming balance is negative for liabilities

    net_worth_snapshot = NetWorthSnapshot(
        date=date.today(),
        assets=assets,
        liabilities=liabilities,
        net_worth=assets + liabilities # Liabilities are typically negative values, so add them
    )

    return NetWorthReport(snapshots=[net_worth_snapshot])

# You can add more advanced reports here:
# - Spending trends over time (monthly, quarterly)
# - Budget vs. Actual spending reports
# - Investment performance reports

# Helper function (if needed for more complex aggregations)
# def aggregate_transactions_by_period(transactions, period: str = "month"):
#     # Logic to group transactions by month, quarter, etc.
#     pass

