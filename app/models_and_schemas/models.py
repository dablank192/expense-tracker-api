from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime
from pydantic import EmailStr, BaseModel
from app.utils import helpers
from typing import List, Optional
from enum import Enum


#DATA SCHEMAS
class Category(str, Enum):
    GROCERIES = "Groceries"
    LEISURE = "Leisure"
    ELECTRONICS = "Electronics"
    UTILITIES = "Utilities"
    CLOTHING = "Clothing"
    HEALTH = "Health"
    OTHERS = "Others"

class Expense(SQLModel):
    name: str
    category: Category = Field(default= Category.OTHERS)

class ExpenseCreate(Expense):
    pass

class ExpenseOut(Expense): #Response
    id: int


class User(SQLModel):
    id: int
    username: str = Field(default_factory=helpers.generate_random_username)
    email: EmailStr

class UserLogin(SQLModel):
    email: EmailStr
    password: str

class UserCreate(UserLogin):
    username: str = Field(default_factory=helpers.generate_random_username)

class UserOut(User): #Response
    pass



#SECURITY
class Token(BaseModel): #Login Response
    access_token: str
    token_bearer: str

class TokenData(BaseModel):
    id: Optional[int] = None



#DATABASE TABLES    
class ExpenseBase(Expense, table = True):
    id: int | None = Field(default= None, primary_key= True)
    created_at: datetime = Field(default_factory= datetime.now)
    updated_at: datetime = Field(default_factory= datetime.now)
    user_id: int | None = Field(default=None, foreign_key="userbase.id")

    user: Optional["UserBase"] = Relationship(back_populates="expense")

class UserBase(User, table = True):
    id: int | None = Field(default= None, primary_key= True)
    password: str
    created_at: datetime = Field(default_factory= datetime.now)

    expense: List["ExpenseBase"] = Relationship(back_populates="user")

