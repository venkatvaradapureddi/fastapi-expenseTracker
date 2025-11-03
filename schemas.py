from pydantic import BaseModel
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    username:str
    email:str
    password:str

class UserOut(BaseModel):
    id:int
    username:str
    email:str
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ExpenseBase(BaseModel):
    title:str
    amount:float
    category:str
    date:date

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseOut(ExpenseBase):
    id:int
    class Config:
        orm_mode = True

