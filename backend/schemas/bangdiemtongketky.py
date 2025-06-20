from pydantic import BaseModel
from typing import Optional

class BangDiemTongKetKyBase(BaseModel):
    DiemTBKyHe10: Optional[float]
    DiemTBKyHe4: Optional[float]
    DiemTBKyChu: Optional[str]
    SoTCDatKy: Optional[int]
    XepLoaiHocLucKy: Optional[str]

class BangDiemTongKetKyCreate(BangDiemTongKetKyBase):
    MaSV: str
    MaKy: str

class BangDiemTongKetKyUpdate(BangDiemTongKetKyBase):
    pass

class BangDiemTongKetKy(BangDiemTongKetKyBase):
    MaSV: str
    MaKy: str

