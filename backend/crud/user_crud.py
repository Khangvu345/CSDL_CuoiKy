import pymysql

def get_user_by_username(db, username: str):
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT Username, Password, Role, UserID FROM TaiKhoan WHERE Username = %s", (username,)
        )
        user = cursor.fetchone()
    return user

def authenticate_user(db, username: str, password: str):
    with db.cursor() as cursor:
        sql = """
            SELECT 
                tk.Username, 
                tk.Password, 
                tk.Role, 
                tk.UserID,
                CASE
                    WHEN tk.Role = 'student' THEN sv.HoTen
                    WHEN tk.Role = 'teacher' THEN gv.HoVaTen
                    ELSE NULL
                END AS HoTen
            FROM TaiKhoan tk
            LEFT JOIN SinhVien sv ON tk.UserID = sv.MaSV AND tk.Role = 'student'
            LEFT JOIN GiangVien gv ON tk.UserID = gv.MaGV AND tk.Role = 'teacher'
            WHERE tk.Username = %s
        """
        cursor.execute(sql, (username,))
        user = cursor.fetchone()

    if not user:
        return None
    if user["Password"] != password:
        return None

    return {
        "Username": user["Username"],
        "Role": user["Role"],
        "UserID": user["UserID"],
        "HoTen": user["HoTen"]
    }
