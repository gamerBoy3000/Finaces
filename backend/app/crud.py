from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import date
from . import models, schemas

def to_cents(amount: float) -> int: return int(round(amount * 100))
def from_cents(cents: int) -> float: return round(cents / 100.0, 2)

# Accounts
def create_account(db: Session, data: schemas.AccountCreate):
    acc = models.Account(name=data.name, type=data.type)
    db.add(acc); db.commit(); db.refresh(acc); return acc
def list_accounts(db: Session): return list(db.scalars(select(models.Account)).all())

# Categories
def create_category(db: Session, data: schemas.CategoryCreate):
    cat = models.Category(name=data.name, kind=data.kind)
    db.add(cat); db.commit(); db.refresh(cat); return cat
def list_categories(db: Session): return list(db.scalars(select(models.Category)).all())

# Tags helper
def get_or_create_tag(db: Session, name: str):
    tag = db.scalar(select(models.Tag).where(models.Tag.name == name))
    if not tag:
        tag = models.Tag(name=name); db.add(tag); db.commit(); db.refresh(tag)
    return tag

# Transactions
def create_transaction(db: Session, data: schemas.TransactionCreate):
    tx = models.Transaction(
        date=data.date, description=data.description,
        amount_cents=to_cents(data.amount),
        type=models.TxType(data.type), account_id=data.account_id,
        category_id=data.category_id, transfer_group=data.transfer_group
    )
    if data.tags:
        for t in data.tags:
            tag = get_or_create_tag(db, t.strip()); tx.tags.append(tag)
    db.add(tx); db.commit(); db.refresh(tx); return tx

def list_transactions(db: Session, start: date|None=None, end: date|None=None,
                      account_id: int|None=None, category_id: int|None=None,
                      tag: str|None=None, search: str|None=None, type: str|None=None,
                      limit: int=100, offset: int=0):
    stmt = select(models.Transaction).order_by(models.Transaction.date.desc(), models.Transaction.id.desc())
    if start: stmt = stmt.where(models.Transaction.date >= start)
    if end:   stmt = stmt.where(models.Transaction.date <  end)  # EXCLUSIVE end
    if account_id:  stmt = stmt.where(models.Transaction.account_id == account_id)
    if category_id: stmt = stmt.where(models.Transaction.category_id == category_id)
    if search:
        like = f"%{search.lower()}%"; stmt = stmt.where(func.lower(models.Transaction.description).like(like))
    if tag:
        stmt = stmt.join(models.Transaction.tags).where(models.Tag.name == tag)
    if type:
        stmt = stmt.where(models.Transaction.type == models.TxType(type))
    stmt = stmt.limit(limit).offset(offset)
    return list(db.scalars(stmt).unique().all())

# Budgets
def upsert_budget(db: Session, data: schemas.BudgetCreate):
    cents = to_cents(data.amount)
    existing = db.query(models.Budget).filter(models.Budget.month == data.month,
                                              models.Budget.category_id == data.category_id).first()
    if existing:
        existing.amount_cents = cents; db.commit(); db.refresh(existing); return existing
    bud = models.Budget(month=data.month, category_id=data.category_id, amount_cents=cents)
    db.add(bud); db.commit(); db.refresh(bud); return bud

def list_budgets(db: Session, month: str|None=None):
    q = db.query(models.Budget); 
    if month: q = q.filter(models.Budget.month == month)
    return q.all()

# Reports
def monthly_summary(db: Session, month: str):
    y, m = map(int, month.split("-"))
    start = date(y, m, 1)
    end = date(y+1, 1, 1) if m == 12 else date(y, m+1, 1)
    txs = list_transactions(db, start=start, end=end, limit=10_000)
    total_expense = sum(-t.amount_cents for t in txs if t.amount_cents < 0 and t.type != models.TxType.transfer)
    total_income  = sum( t.amount_cents for t in txs if t.amount_cents > 0 and t.type != models.TxType.transfer)
    by_cat = {}
    for t in txs:
        if t.type == models.TxType.transfer: continue
        cat = t.category.name if t.category else "Uncategorized"
        by_cat.setdefault(cat, {"spent":0,"income":0})
        (by_cat[cat]["spent"] if t.amount_cents<0 else by_cat[cat]["income"]) += abs(t.amount_cents)
    items = [schemas.MonthlyCategorySummary(category=k, spent=round(v["spent"]/100,2), income=round(v["income"]/100,2))
             for k,v in sorted(by_cat.items())]
    return schemas.MonthlySummary(month=month, total_expense=round(total_expense/100,2),
                                  total_income=round(total_income/100,2), by_category=items)

def budget_progress(db: Session, month: str):
    budgets = list_budgets(db, month=month)
    y, m = map(int, month.split("-"))
    start = date(y, m, 1)
    end = date(y+1, 1, 1) if m == 12 else date(y, m+1, 1)
    txs = list_transactions(db, start=start, end=end, limit=10_000)
    spent_by_cat: dict[int,int] = {}
    for t in txs:
        if t.type == models.TxType.transfer or t.amount_cents >= 0: continue
        cid = t.category_id or -1
        spent_by_cat[cid] = spent_by_cat.get(cid, 0) + (-t.amount_cents)
    items = [schemas.BudgetProgressItem(category=b.category.name, budget=round(b.amount_cents/100,2),
                                        spent=round(spent_by_cat.get(b.category_id,0)/100,2),
                                        remaining=round((b.amount_cents - spent_by_cat.get(b.category_id,0))/100,2))
             for b in budgets]
    return schemas.BudgetProgress(month=month, items=items)
