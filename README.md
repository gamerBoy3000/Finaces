# Personal Finance Tracker (FastAPI + SQLite)

A minimalist, local-first personal finance tracker backend. Features:
- Accounts, Categories, Transactions, Budgets
- CSV import (date, description, amount, category, account, tags)
- Monthly summary reports and budget progress
- SQLite file database (`finance.db`) in the project root

## Quickstart

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# run the API
uvicorn app.main:app --reload
# API will be at http://127.0.0.1:8000 (docs: /docs)
```

## CSV Import

Expected columns: `date,description,amount,category,account,tags`  
- `date` format: `YYYY-MM-DD`
- `amount`: negative for expenses, positive for income (e.g., `-120.50`, `2500`)
- `tags`: comma-separated (optional)

```bash
# from project root
python scripts/import_csv.py path/to/your.csv
```

## Seed sample data

```bash
python scripts/seed.py
```

## Notes
- Amounts are stored internally as **integer cents** to avoid floating-point inaccuracies.
- Transfers can be recorded as two transactions with a shared `transfer_group` string (e.g., "2025-08-15-rent-transfer").
- This is a starter project: extend with auth, attachments, and analytics as you need.