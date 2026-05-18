from decimal import Decimal
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Numeric, ForeignKey, TIMESTAMP, text

# 表对应的ORM模式
class Base(DeclarativeBase):
    pass

# 用户表
class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    user_password: Mapped[str] = mapped_column(String(40), nullable=False)
    user_role: Mapped[str] = mapped_column(String(20), nullable=False)
    real_name: Mapped[Optional[str]] = mapped_column(String(30))
    age: Mapped[Optional[int]] = mapped_column(Integer)
    gender: Mapped[Optional[str]] = mapped_column(String(10))

# 书籍库存表
class Book(Base):
    __tablename__ = "book"

    book_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    isbn: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(70), nullable=False)
    publisher: Mapped[Optional[str]] = mapped_column(String(50))
    author: Mapped[Optional[str]] = mapped_column(String(50))
    price: Mapped[Optional[Decimal]] = mapped_column(Numeric(7, 2), nullable=True, server_default=text("0.00"))
    stock_quantity: Mapped[int] = mapped_column(Integer, server_default=text("0"))

# 图书进货表
class Purchase(Base):
    __tablename__ = "purchase"

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("book.book_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    buy_price: Mapped[Decimal] = mapped_column(Numeric(7, 2), nullable=False)
    purchase_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    book_status: Mapped[str] = mapped_column(String(15), nullable=False, server_default=text("'unpaid'"))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    is_stocked: Mapped[str] = mapped_column(String(10), nullable=False, server_default=text("'False'"))

# 书籍销售表
class Sale(Base):
    __tablename__ = "sale"

    sale_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("book.book_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    sale_price: Mapped[Decimal] = mapped_column(Numeric(7, 2), nullable=False)
    sale_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    sold_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)


# 财务账单表
class Bill(Base):
    __tablename__ = "bill"

    bill_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    bill_type: Mapped[str] = mapped_column(String(15), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(7, 2), nullable=False)
    related_id: Mapped[int] = mapped_column(Integer, nullable=False)
    billed_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
