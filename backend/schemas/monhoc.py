from pydantic import BaseModel
from typing import Optional

class MonHocBase(BaseModel):
    TenMH: str
    SoTinChi: int
    LoaiMH: Optional[str]
    HeSoChuyenCan: Optional[float]
    HeSoGiuaKy: Optional[float]
    HeSoCuoiKy: Optional[float]
    HeSoThucHanh: Optional[float]
    MaKhoa: str

class MonHocCreate(MonHocBase):
    MaMH: str

class MonHocUpdate(BaseModel):
    TenMH: Optional[str] = None
    SoTinChi: Optional[int] = None
    LoaiMH: Optional[str] = None
    HeSoChuyenCan: Optional[float] = None
    HeSoGiuaKy: Optional[float] = None
    HeSoCuoiKy: Optional[float] = None
    HeSoThucHanh: Optional[float] = None
    MaKhoa: Optional[str] = None

class MonHoc(MonHocBase):
    MaMH: str

