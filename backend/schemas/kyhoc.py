from pydantic import BaseModel
from typing import Optional
from datetime import date

class KyHocBase(BaseModel):
    TenKy: str
    NamHoc: int
    NgayBatDau: Optional[date]
    NgayKetThuc: Optional[date]

class KyHocCreate(KyHocBase):
    MaKy: str

class KyHocUpdate(BaseModel):
    TenKy: Optional[str] = None
    NamHoc: Optional[int] = None
    NgayBatDau: Optional[date] = None
    NgayKetThuc: Optional[date] = None

class KyHoc(KyHocBase):
    MaKy: str
