from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class SinhVienBase(BaseModel):
    MaLopHC: str
    MaChuyenNganh: str
    HoTen: str
    NgaySinh: Optional[date]
    GioiTinh: Optional[str]
    SDT: Optional[str]
    Email: Optional[EmailStr]
    NamNhapHoc: Optional[int]

class SinhVienCreate(SinhVienBase):
    MaSV: str

class SinhVienUpdate(BaseModel):
    MaLopHC: Optional[str] = None
    MaChuyenNganh: Optional[str] = None
    HoTen: Optional[str] = None
    NgaySinh: Optional[date] = None
    GioiTinh: Optional[str] = None
    SDT: Optional[str] = None
    Email: Optional[EmailStr] = None
    NamNhapHoc: Optional[int] = None

class SinhVien(SinhVienBase):
    MaSV: str

