from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class GiangVienBase(BaseModel):
    MaKhoaCongTac: str
    HoVaTen: str
    NgaySinh: Optional[date]
    GioiTinh: Optional[str]
    SDT: Optional[str]
    Email: Optional[EmailStr]

class GiangVienCreate(GiangVienBase):
    MaGV: str

class GiangVienUpdate(BaseModel):
    MaKhoaCongTac: Optional[str] = None
    HoVaTen: Optional[str] = None
    NgaySinh: Optional[date] = None
    GioiTinh: Optional[str] = None
    SDT: Optional[str] = None
    Email: Optional[EmailStr] = None

class GiangVien(GiangVienBase):
    MaGV: str

