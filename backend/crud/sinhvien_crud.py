def get_student_classes(db, ma_sv: str):
    """từ BangDiem"""
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT ltc.MaLopTC, mh.TenMH, kh.TenKy
            FROM BangDiem bd
            JOIN LopTC ltc ON bd.MaLopTC = ltc.MaLopTC
            JOIN MonHoc mh ON ltc.MaMH = mh.MaMH
            JOIN KyHoc kh ON ltc.MaKy = kh.MaKy
            WHERE bd.MaSV = %s
            """, (ma_sv,))
        return cursor.fetchall()

def get_student_class_grades(db, ma_sv: str, ma_loptc: str):
    with db.cursor() as cursor:
        # Lấy điểm thành phần và hệ số
        cursor.execute("""
            SELECT bd.DiemChuyenCan, bd.DiemGiuaKy, bd.DiemCuoiKy, bd.DiemThucHanh,
                   mh.MaMH, mh.TenMH, mh.SoTinChi,
                   mh.HeSoChuyenCan, mh.HeSoGiuaKy, mh.HeSoCuoiKy, mh.HeSoThucHanh
            FROM BangDiem bd
            JOIN LopTC ltc ON bd.MaLopTC = ltc.MaLopTC
            JOIN MonHoc mh ON ltc.MaMH = mh.MaMH
            WHERE bd.MaSV = %s AND bd.MaLopTC = %s
        """, (ma_sv, ma_loptc))
        row = cursor.fetchone()
        if not row:
            return None

        # TÍNH ĐỘNG
        hs_cc, hs_gk, hs_ck, hs_th = (row[k] or 0 for k in ("HeSoChuyenCan", "HeSoGiuaKy", "HeSoCuoiKy", "HeSoThucHanh"))
        tong_he_so = hs_cc + hs_gk + hs_ck + hs_th
        diem_cc, diem_gk, diem_ck, diem_th = (row[k] or 0 for k in ("DiemChuyenCan", "DiemGiuaKy", "DiemCuoiKy", "DiemThucHanh"))

        if tong_he_so > 0:
            diem_tong_ket_10 = round((diem_cc * hs_cc + diem_gk * hs_gk + diem_ck * hs_ck + diem_th * hs_th) / tong_he_so, 1)
        else:
            diem_tong_ket_10 = 0.0

        # Hệ 4 + điểm chữ + trạng thái
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

        return {
            "MaMH": row["MaMH"],
            "TenMH": row["TenMH"],
            "SoTinChi": row["SoTinChi"],
            "DiemChuyenCan": row["DiemChuyenCan"],
            "DiemGiuaKy": row["DiemGiuaKy"],
            "DiemCuoiKy": row["DiemCuoiKy"],
            "DiemThucHanh": row["DiemThucHanh"],
            "DiemTongKetHe10": diem_tong_ket_10,
            "DiemTongKetHe4": diem_4,
            "DiemChu": diem_chu,
            "TrangThaiQuaMon": trang_thai
        }


def get_all_semesters(db):
    with db.cursor() as cursor:
        cursor.execute("SELECT MaKy, TenKy FROM KyHoc ORDER BY NamHoc DESC, TenKy DESC")
        return cursor.fetchall()

def get_student_grades_in_semester(db, ma_sv: str, ma_ky: str):
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT mh.MaMH, mh.TenMH, mh.SoTinChi,
                   bd.DiemChuyenCan, bd.DiemGiuaKy, bd.DiemCuoiKy, bd.DiemThucHanh,
                   mh.HeSoChuyenCan, mh.HeSoGiuaKy, mh.HeSoCuoiKy, mh.HeSoThucHanh
            FROM BangDiem bd
            JOIN LopTC ltc ON bd.MaLopTC = ltc.MaLopTC
            JOIN MonHoc mh ON ltc.MaMH = mh.MaMH
            WHERE bd.MaSV = %s AND ltc.MaKy = %s
        """, (ma_sv, ma_ky))
        rows = cursor.fetchall()

    diem_mon_list = []
    tong_diem_he10 = tong_diem_he4 = tong_tinchi = tong_tinchi_dat = 0

    for row in rows:
        hs_cc, hs_gk, hs_ck, hs_th = (row[k] or 0 for k in ("HeSoChuyenCan", "HeSoGiuaKy", "HeSoCuoiKy", "HeSoThucHanh"))
        tong_he_so = hs_cc + hs_gk + hs_ck + hs_th
        diem_cc, diem_gk, diem_ck, diem_th = (row[k] or 0 for k in ("DiemChuyenCan", "DiemGiuaKy", "DiemCuoiKy", "DiemThucHanh"))
        so_tinchi = row["SoTinChi"] or 0

        if tong_he_so > 0:
            diem_tong_ket_10 = round((diem_cc * hs_cc + diem_gk * hs_gk + diem_ck * hs_ck + diem_th * hs_th) / tong_he_so, 1)
        else:
            diem_tong_ket_10 = 0.0

        # Hệ 4 + điểm chữ + trạng thái
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

        tong_diem_he10 += diem_tong_ket_10 * so_tinchi
        tong_diem_he4 += diem_4 * so_tinchi
        tong_tinchi += so_tinchi
        if trang_thai == 'Đạt':
            tong_tinchi_dat += so_tinchi

        diem_mon_list.append({
            "MaMH": row["MaMH"],
            "TenMH": row["TenMH"],
            "SoTinChi": so_tinchi,
            "DiemChuyenCan": row["DiemChuyenCan"],
            "DiemGiuaKy": row["DiemGiuaKy"],
            "DiemCuoiKy": row["DiemCuoiKy"],
            "DiemThucHanh": row["DiemThucHanh"],
            "DiemTongKetHe10": diem_tong_ket_10,
            "DiemTongKetHe4": diem_4,
            "DiemChu": diem_chu,
            "TrangThaiQuaMon": trang_thai
        })

    # Tính điểm TB kỳ và xếp loại
    if tong_tinchi > 0:
        diem_tb_10 = round(tong_diem_he10 / tong_tinchi, 2)
        diem_tb_4 = round(tong_diem_he4 / tong_tinchi, 2)
    else:
        diem_tb_10 = diem_tb_4 = 0.0

    # Xếp loại học lực kỳ
    if diem_tb_10 >= 9.0:
        diem_tb_chu, xep_loai = 'A+', 'Giỏi'
    elif diem_tb_10 >= 8.5:
        diem_tb_chu, xep_loai = 'A', 'Giỏi'
    elif diem_tb_10 >= 8.0:
        diem_tb_chu, xep_loai = 'B+', 'Khá'
    elif diem_tb_10 >= 7.0:
        diem_tb_chu, xep_loai = 'B', 'Khá'
    elif diem_tb_10 >= 6.5:
        diem_tb_chu, xep_loai = 'C+', 'Trung bình'
    elif diem_tb_10 >= 5.5:
        diem_tb_chu, xep_loai = 'C', 'Trung bình'
    elif diem_tb_10 >= 5.0:
        diem_tb_chu, xep_loai = 'D+', 'Trung bình yếu'
    elif diem_tb_10 >= 4.0:
        diem_tb_chu, xep_loai = 'D', 'Trung bình yếu'
    else:
        diem_tb_chu, xep_loai = 'F', 'Kém'

    return {
        "diem_mon": diem_mon_list,
        "tongket": {
            "DiemTBKyHe10": diem_tb_10,
            "DiemTBKyHe4": diem_tb_4,
            "DiemTBKyChu": diem_tb_chu,
            "SoTCDatKy": tong_tinchi_dat,
            "XepLoaiHocLucKy": xep_loai
        }
    }

def get_student_overall_progress(db, ma_sv: str):
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT mh.SoTinChi,
                   bd.DiemChuyenCan, bd.DiemGiuaKy, bd.DiemCuoiKy, bd.DiemThucHanh,
                   mh.HeSoChuyenCan, mh.HeSoGiuaKy, mh.HeSoCuoiKy, mh.HeSoThucHanh
            FROM BangDiem bd
            JOIN LopTC ltc ON bd.MaLopTC = ltc.MaLopTC
            JOIN MonHoc mh ON ltc.MaMH = mh.MaMH
            WHERE bd.MaSV = %s
        """, (ma_sv,))
        rows = cursor.fetchall()

    tong_diem_he10 = tong_diem_he4 = tong_tinchi = tong_tinchi_dat = 0

    for row in rows:
        hs_cc, hs_gk, hs_ck, hs_th = (row[k] or 0 for k in ("HeSoChuyenCan", "HeSoGiuaKy", "HeSoCuoiKy", "HeSoThucHanh"))
        tong_he_so = hs_cc + hs_gk + hs_ck + hs_th
        diem_cc, diem_gk, diem_ck, diem_th = (row[k] or 0 for k in ("DiemChuyenCan", "DiemGiuaKy", "DiemCuoiKy", "DiemThucHanh"))
        so_tinchi = row["SoTinChi"] or 0

        if tong_he_so > 0:
            diem_tong_ket_10 = round((diem_cc * hs_cc + diem_gk * hs_gk + diem_ck * hs_ck + diem_th * hs_th) / tong_he_so, 1)
        else:
            diem_tong_ket_10 = 0.0

        if diem_tong_ket_10 >= 9.0:
            diem_4 = 4.0
        elif diem_tong_ket_10 >= 8.5:
            diem_4 = 3.7
        elif diem_tong_ket_10 >= 8.0:
            diem_4 = 3.5
        elif diem_tong_ket_10 >= 7.0:
            diem_4 = 3.0
        elif diem_tong_ket_10 >= 6.5:
            diem_4 = 2.5
        elif diem_tong_ket_10 >= 5.5:
            diem_4 = 2.0
        elif diem_tong_ket_10 >= 5.0:
            diem_4 = 1.5
        elif diem_tong_ket_10 >= 4.0:
            diem_4 = 1.0
        else:
            diem_4 = 0.0

        tong_diem_he10 += diem_tong_ket_10 * so_tinchi
        tong_diem_he4 += diem_4 * so_tinchi
        tong_tinchi += so_tinchi
        if diem_tong_ket_10 >= 4.0:
            tong_tinchi_dat += so_tinchi

    if tong_tinchi > 0:
        diem_tb_10 = round(tong_diem_he10 / tong_tinchi, 2)
        diem_tb_4 = round(tong_diem_he4 / tong_tinchi, 2)
    else:
        diem_tb_10 = diem_tb_4 = 0.0

    return {
        "DiemTBHe10": diem_tb_10,
        "DiemTBHe4": diem_tb_4,
        "TongTinChiDat": tong_tinchi_dat,
        "TongTinChi": tong_tinchi
    }

