from pydantic import BaseModel, Field
from typing import Literal

class UserBase(BaseModel):
    Role: Literal['student', 'teacher', 'manager']
    UserID: str

class UserLogin(BaseModel):
    Username: str = Field(..., min_length=1)
    Password: str = Field(..., min_length=1)

class UserCreate(UserBase):
    Username: str
    Password: str

class User(UserBase):
    Username: str