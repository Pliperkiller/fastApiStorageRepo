from enum import Enum
from pydantic import BaseModel, EmailStr, field_validator
from sqlmodel import SQLModel, Field, Relationship, Session, select
from db import engine


class TransactionBase(SQLModel):
    ammount : int
    description : str

class TransactionCreate(TransactionBase):
    customer_id : int = Field(foreign_key="customer.id")

class TransactionUpdate(TransactionBase):
    pass

class Transaction(TransactionBase, table = True):
    id : int | None = Field(default= None, primary_key= True)
    customer_id : int = Field(foreign_key="customer.id")
    customer : Customer = Relationship(back_populates="transactions")



