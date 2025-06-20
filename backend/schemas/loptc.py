from pydantic import BaseModel

class LopTCBase(BaseModel):
    MaMH: str
    MaGV: str
    MaKy: str

class LopTCCreate(LopTCBase):
    MaLopTC: str

class LopTCUpdate(BaseModel):
    MaMH: str = None
    MaGV: str = None
    MaKy: str = None

class LopTC(LopTCBase):
    MaLopTC: str
