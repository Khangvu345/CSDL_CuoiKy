from pydantic import BaseModel
from typing import Optional

class ChuyenNganhBase(BaseModel):
    TenChuyenNganh: str
    MaKhoa: str

class ChuyenNganhCreate(ChuyenNganhBase):
    MaChuyenNganh: str

class ChuyenNganhUpdate(BaseModel):
    TenChuyenNganh: Optional[str] = None
    MaKhoa: Optional[str] = None

class ChuyenNganh(ChuyenNganhBase):
    MaChuyenNganh: str
