import pymysql

def get_user_by_username(db, username: str):
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT Username, Password, Role, UserID FROM TaiKhoan WHERE Username = %s", (username,)
        )
        user = cursor.fetchone()
    return user

def authenticate_user(db, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if user["Password"] != password:
        return None
    return {
        "Username": user["Username"],
        "Role": user["Role"],
        "UserID": user["UserID"]
    }
