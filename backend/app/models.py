from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
import enum
from .database import Base

class TxType(str, enum.Enum):
    expense = "expense"
    income = "income"
    transfer = "transfer"

class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    type: Mapped[str] = mapped_column(String, default="cash")
    transactions = relationship("Transaction", back_populates="account")

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    kind: Mapped[str] = mapped_column(String, default="expense")
    transactions = relationship("Transaction", back_populates="category")

class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)

class TransactionTag(Base):
    __tablename__ = "transaction_tags"
    tx_id: Mapped[int] = mapped_column(ForeignKey("transactions.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date: Mapped[Date] = mapped_column(Date, index=True)
    description: Mapped[str] = mapped_column(String, index=True)
    amount_cents: Mapped[int] = mapped_column(Integer, index=True)
    type: Mapped[TxType] = mapped_column(Enum(TxType), index=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"), index=True)
    category_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("categories.id"), nullable=True, index=True)
    transfer_group: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())
    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
    tags = relationship("Tag", secondary="transaction_tags", lazy="joined")

class Budget(Base):
    __tablename__ = "budgets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    month: Mapped[str] = mapped_column(String, index=True)  # "YYYY-MM"
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))
    amount_cents: Mapped[int] = mapped_column(Integer)
    category = relationship("Category")
    __table_args__ = (UniqueConstraint("month", "category_id", name="uniq_budget_month_category"),)
