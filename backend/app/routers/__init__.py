# app/routers/__init__.py

# Import all your individual router modules here
from . import auth
from . import transactions 

# You can also define an __all__ variable to control what gets imported when someone does `from app.routers import *`
# __all__ = ["auth", "transactions"]  # Optional, but good practice for larger applications

# If you have shared dependencies or common initialization logic for your routers, 
# you can define it here. For instance, creating a common APIRouter instance:

from fastapi import APIRouter

api_router = APIRouter()

# Include all the individual routers in the main API router
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
