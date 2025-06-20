from pydantic import BaseModel
from typing import Literal

class UserBase(BaseModel):
    Role: Literal['student', 'teacher', 'manager']
    UserID: str

class UserCreate(UserBase):
    Username: str
    Password: str

class UserLogin(BaseModel):
    Username: str
    Password: str

class User(UserBase):
    Username: str
