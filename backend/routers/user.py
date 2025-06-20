from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from schemas.user import UserLogin, User
from crud import user_crud
from db import get_db

router = APIRouter(tags=["User"])

@router.post("/login", response_model=User)
def login_user(data: UserLogin, db=Depends(get_db)):
    user = user_crud.authenticate_user(db, data.Username, data.Password)
    if not user:
        raise HTTPException(status_code=401, detail="Sai tên đăng nhập hoặc mật khẩu.")
    return user
