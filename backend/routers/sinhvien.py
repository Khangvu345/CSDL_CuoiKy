from fastapi import APIRouter, Depends, HTTPException, Query
from crud import sinhvien_crud
from db import get_db
from schemas.sinhvien import SinhVienLopTC, DiemMonHocSinhVien, DiemTongKetKy, SinhVienDetails, TienDoHocTap
router = APIRouter(tags=["SinhVien"])

@router.get("/my-classes", response_model=list[SinhVienLopTC])
def get_my_classes(userid: str = Query(...), db=Depends(get_db)):
    return sinhvien_crud.get_student_classes(db, ma_sv=userid)

@router.get("/class/{ma_loptc}/grades", response_model=DiemMonHocSinhVien)
def get_grades(ma_loptc: str, userid: str = Query(...), db=Depends(get_db)):
    result = sinhvien_crud.get_student_class_grades(db, ma_sv=userid, ma_loptc=ma_loptc)
    if not result:
        raise HTTPException(status_code=404, detail="Không tìm thấy điểm")
    return result

@router.get("/semesters")
def get_all_semesters(db=Depends(get_db)):
    return sinhvien_crud.get_all_semesters(db)

@router.get("/semester/{ma_ky}/grades")
def get_grades_in_semester(ma_ky: str, userid: str = Query(...), db=Depends(get_db)):
    result = sinhvien_crud.get_student_grades_in_semester(db, ma_sv=userid, ma_ky=ma_ky)
    return result

@router.get("/details", response_model=SinhVienDetails)
def get_details(userid: str = Query(...), db=Depends(get_db)):
    details = sinhvien_crud.get_student_details(db, ma_sv=userid)
    if not details:
        raise HTTPException(status_code=404, detail="Không tìm thấy sinh viên")
    return details

# Thêm endpoint này vào trong tệp routers/sinhvien.py

@router.get("/progress", response_model=TienDoHocTap)
def get_progress(userid: str = Query(...), db=Depends(get_db)):
    progress_data = sinhvien_crud.get_student_overall_progress(db, ma_sv=userid)
    if not progress_data:
        return {"DiemTBHe10": 0, "DiemTBHe4": 0, "TongTinChiDat": 0, "TongTinChi": 0}
    return progress_data