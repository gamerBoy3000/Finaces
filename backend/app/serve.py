# backend/app/serve.py
from fastapi import FastAPI
from app.routers.transaction import router as transaction_router  # direct submodule import

app = FastAPI(title="Personal Finance API (minimal)")
app.include_router(transaction_router)

@app.get("/health")
def health():
    return {"status": "ok"}
