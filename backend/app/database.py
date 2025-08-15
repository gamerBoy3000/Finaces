from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declaretive_base

SQLALCHEMY_DATABASE_URL ="sqlite:///./finance.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,connect_args
)