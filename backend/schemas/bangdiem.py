from pydantic import BaseModel
from typing import Optional

class BangDiemBase(BaseModel):
    DiemChuyenCan: Optional[float]
    DiemGiuaKy: Optional[float]
    DiemCuoiKy: Optional[float]
    DiemThucHanh: Optional[float]
    DiemTongKetHe10: Optional[float]
    DiemTongKetHe4: Optional[float]
    DiemChu: Optional[str]
    TrangThaiQuaMon: Optional[str]

class BangDiemCreate(BangDiemBase):
    MaSV: str
    MaLopTC: str

class BangDiemUpdate(BangDiemBase):
    pass  # Tất cả đều optional

class BangDiem(BangDiemBase):
    MaSV: str
    MaLopTC: str

