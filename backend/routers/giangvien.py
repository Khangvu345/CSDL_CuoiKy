from fastapi import APIRouter, Depends, HTTPException, Query
from crud import giangvien_crud
from db import get_db
from schemas.giangvien import LopTinChiGV, SinhVienTrongLopTC, DiemUpdateRequest

router = APIRouter(prefix="/api/teacher", tags=["GiangVien"])

@router.get("/my-classes", response_model=list[LopTinChiGV])
def get_my_classes(userid: str = Query(...), db=Depends(get_db)):
    return giangvien_crud.get_teacher_classes(db, ma_gv=userid)

@router.get("/class/{ma_loptc}/students", response_model=list[SinhVienTrongLopTC])
def get_students(ma_loptc: str, userid: str = Query(...), db=Depends(get_db)):
    # Optionally: kiểm tra xem lớp này có đúng là của gv không (để chống truy cập trái phép)
    return giangvien_crud.get_students_in_class(db, ma_loptc=ma_loptc)

@router.post("/class/{ma_loptc}/student/{ma_sv}/grades")
def update_grade(ma_loptc: str, ma_sv: str, diem: DiemUpdateRequest, userid: str = Query(...), db=Depends(get_db)):
    # Optionally: kiểm tra quyền
    return giangvien_crud.update_student_grade(db, ma_loptc, ma_sv, diem.dict())

@router.delete("/class/{ma_loptc}/student/{ma_sv}/grades")
def delete_grade(ma_loptc: str, ma_sv: str, userid: str = Query(...), db=Depends(get_db)):
    # Optionally: kiểm tra quyền
    return giangvien_crud.delete_student_grade(db, ma_loptc, ma_sv)
