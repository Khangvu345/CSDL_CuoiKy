from pydantic import BaseModel
from typing import Optional

class KhoaBase(BaseModel):
    TenKhoa: str

class KhoaCreate(KhoaBase):
    MaKhoa: str

class KhoaUpdate(BaseModel):
    TenKhoa: Optional[str] = None

class Khoa(KhoaBase):
    MaKhoa: str

