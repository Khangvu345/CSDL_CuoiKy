from pydantic import BaseModel
from typing import Optional

class LopHCBase(BaseModel):
    MaKhoaQuanLy: str

class LopHCCreate(LopHCBase):
    MaLopHC: str

class LopHCUpdate(BaseModel):
    MaKhoaQuanLy: Optional[str] = None

class LopHC(LopHCBase):
    MaLopHC: str
