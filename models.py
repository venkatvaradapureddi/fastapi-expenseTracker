from db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DECIMAL, DateTime, func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(256))
    created_at = Column(DateTime, default=func.now())
    expenses = relationship("Expense",back_populates="owner")

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    title = Column(String(100))
    amount = Column(DECIMAL(10,2))
    category = Column(String(50))
    date = Column(Date)
    created_at = Column(DateTime, default=func.now())

    owner = relationship("User",back_populates="expenses")

