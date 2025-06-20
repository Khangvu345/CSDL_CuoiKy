def get_teacher_classes(db, ma_gv: str):
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT 
                ltc.MaLopTC, 
                mh.TenMH, 
                kh.TenKy,
                kh.NamHoc,  
                kh.MaKy     
            FROM LopTC ltc
            JOIN MonHoc mh ON ltc.MaMH = mh.MaMH
            JOIN KyHoc kh ON ltc.MaKy = kh.MaKy
            WHERE ltc.MaGV = %s
            ORDER BY kh.NamHoc DESC, kh.MaKy DESC 
        """, (ma_gv,))
        return cursor.fetchall()

def get_students_personal_in_class(db, ma_loptc: str):
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT sv.MaSV, sv.HoTen, sv.MaLopHC, sv.MaChuyenNganh, sv.NgaySinh, sv.GioiTinh, sv.Email
            FROM BangDiem bd
            JOIN SinhVien sv ON bd.MaSV = sv.MaSV
            WHERE bd.MaLopTC = %s
        """, (ma_loptc,))
        return cursor.fetchall()

def get_students_grades_in_class(db, ma_loptc: str):
    # Lấy hệ số
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT mh.HeSoChuyenCan, mh.HeSoGiuaKy, mh.HeSoCuoiKy, mh.HeSoThucHanh
            FROM LopTC ltc JOIN MonHoc mh ON ltc.MaMH = mh.MaMH
            WHERE ltc.MaLopTC = %s
        """, (ma_loptc,))
        coeffs = cursor.fetchone()
        hs_cc = coeffs["HeSoChuyenCan"] or 0
        hs_gk = coeffs["HeSoGiuaKy"] or 0
        hs_ck = coeffs["HeSoCuoiKy"] or 0
        hs_th = coeffs["HeSoThucHanh"] or 0
        tong_he_so = hs_cc + hs_gk + hs_ck + hs_th

        # Lấy toàn bộ sinh viên & điểm thành phần
        cursor.execute("""
            SELECT sv.MaSV, sv.HoTen,
                   bd.DiemChuyenCan, bd.DiemGiuaKy, bd.DiemCuoiKy, bd.DiemThucHanh
            FROM BangDiem bd
            JOIN SinhVien sv ON bd.MaSV = sv.MaSV
            WHERE bd.MaLopTC = %s
        """, (ma_loptc,))
        sv_list = cursor.fetchall()

    results = []
    for sv in sv_list:
        diem_cc = sv["DiemChuyenCan"] or 0
        diem_gk = sv["DiemGiuaKy"] or 0
        diem_ck = sv["DiemCuoiKy"] or 0
        diem_th = sv["DiemThucHanh"] or 0

        if tong_he_so > 0:
            diem_tong_ket_10 = round((diem_cc * hs_cc + diem_gk * hs_gk + diem_ck * hs_ck + diem_th * hs_th) / tong_he_so, 1)
        else:
            diem_tong_ket_10 = 0.0

        # chuyển hệ 4, chữ, trạng thái
        if diem_tong_ket_10 >= 9.0:
            diem_chu, diem_4 = 'A+', 4.0
        elif diem_tong_ket_10 >= 8.5:
            diem_chu, diem_4 = 'A', 3.7
        elif diem_tong_ket_10 >= 8.0:
            diem_chu, diem_4 = 'B+', 3.5
        elif diem_tong_ket_10 >= 7.0:
            diem_chu, diem_4 = 'B', 3.0
        elif diem_tong_ket_10 >= 6.5:
            diem_chu, diem_4 = 'C+', 2.5
        elif diem_tong_ket_10 >= 5.5:
            diem_chu, diem_4 = 'C', 2.0
        elif diem_tong_ket_10 >= 5.0:
            diem_chu, diem_4 = 'D+', 1.5
        elif diem_tong_ket_10 >= 4.0:
            diem_chu, diem_4 = 'D', 1.0
        else:
            diem_chu, diem_4 = 'F', 0.0

        trang_thai = 'Đạt' if diem_tong_ket_10 >= 4.0 else 'Trượt'

        results.append({
            "MaSV": sv["MaSV"],
            "HoTen": sv["HoTen"],
            "DiemChuyenCan": sv["DiemChuyenCan"],
            "DiemGiuaKy": sv["DiemGiuaKy"],
            "DiemCuoiKy": sv["DiemCuoiKy"],
            "DiemThucHanh": sv["DiemThucHanh"],
            "DiemTongKetHe10": diem_tong_ket_10,
            "DiemTongKetHe4": diem_4,
            "DiemChu": diem_chu,
            "TrangThaiQuaMon": trang_thai
        })
    return results

def update_student_grade(db, ma_loptc: str, ma_sv: str, diem_data: dict):
    """
    Cập nhật điểm thành phần. Nếu muốn có DiemTongKetHe10, DiemChu, DiemTongKetHe4, TrangThaiQuaMon
    thì phải tính toán ở đây rồi UPDATE luôn 4 trường đó.
    """
    # Nếu muốn tính động điểm tổng kết:
    with db.cursor() as cursor:
        # Lấy hệ số từ MonHoc/LopTC nếu cần tính động
        cursor.execute("""
            SELECT mh.HeSoChuyenCan, mh.HeSoGiuaKy, mh.HeSoCuoiKy, mh.HeSoThucHanh
            FROM LopTC ltc JOIN MonHoc mh ON ltc.MaMH = mh.MaMH
            WHERE ltc.MaLopTC = %s
        """, (ma_loptc,))
        coeffs = cursor.fetchone()
        if not coeffs:
            raise Exception("Không tìm thấy hệ số môn học!")

        tong_he_so = sum([
            coeffs.get("HeSoChuyenCan") or 0,
            coeffs.get("HeSoGiuaKy") or 0,
            coeffs.get("HeSoCuoiKy") or 0,
            coeffs.get("HeSoThucHanh") or 0,
        ])
        diem_tong_ket = 0
        if tong_he_so > 0:
            diem_tong_ket = (
                (diem_data.get("DiemChuyenCan", 0) or 0) * (coeffs.get("HeSoChuyenCan") or 0) +
                (diem_data.get("DiemGiuaKy", 0) or 0) * (coeffs.get("HeSoGiuaKy") or 0) +
                (diem_data.get("DiemCuoiKy", 0) or 0) * (coeffs.get("HeSoCuoiKy") or 0) +
                (diem_data.get("DiemThucHanh", 0) or 0) * (coeffs.get("HeSoThucHanh") or 0)
            ) / tong_he_so
            diem_tong_ket = round(diem_tong_ket, 1)
        # Chuyển sang hệ 4 & điểm chữ
        if diem_tong_ket >= 9.0:
            diem_chu, diem_4 = 'A+', 4.0
        elif diem_tong_ket >= 8.5:
            diem_chu, diem_4 = 'A', 3.7
        elif diem_tong_ket >= 8.0:
            diem_chu, diem_4 = 'B+', 3.5
        elif diem_tong_ket >= 7.0:
            diem_chu, diem_4 = 'B', 3.0
        elif diem_tong_ket >= 6.5:
            diem_chu, diem_4 = 'C+', 2.5
        elif diem_tong_ket >= 5.5:
            diem_chu, diem_4 = 'C', 2.0
        elif diem_tong_ket >= 5.0:
            diem_chu, diem_4 = 'D+', 1.5
        elif diem_tong_ket >= 4.0:
            diem_chu, diem_4 = 'D', 1.0
        else:
            diem_chu, diem_4 = 'F', 0.0
        trang_thai = 'Đạt' if diem_tong_ket >= 4.0 else 'Trượt'

        # UPDATE tất cả
        cursor.execute("""
            UPDATE BangDiem
            SET DiemChuyenCan=%s, DiemGiuaKy=%s, DiemCuoiKy=%s, DiemThucHanh=%s,
                DiemTongKetHe10=%s, DiemTongKetHe4=%s, DiemChu=%s, TrangThaiQuaMon=%s
            WHERE MaSV=%s AND MaLopTC=%s
        """, (
            diem_data.get("DiemChuyenCan"),
            diem_data.get("DiemGiuaKy"),
            diem_data.get("DiemCuoiKy"),
            diem_data.get("DiemThucHanh"),
            diem_tong_ket, diem_4, diem_chu, trang_thai,
            ma_sv, ma_loptc
        ))
        db.commit()
    return {"status": "success"}

def delete_student_grade(db, ma_loptc: str, ma_sv: str):
    with db.cursor() as cursor:
        cursor.execute(
            "DELETE FROM BangDiem WHERE MaSV=%s AND MaLopTC=%s",
            (ma_sv, ma_loptc)
        )
        db.commit()
    return {"status": "deleted"}
