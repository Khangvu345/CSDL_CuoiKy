# main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from routers import user, giangvien, sinhvien

# Khởi tạo app
app = FastAPI(
    title="Quản lý điểm tín chỉ",
    description="API backend",
    version="1.0.0"
)

# Cấu hình CORS (cho phép kết nối từ frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hoặc liệt kê origin cụ thể như "http://localhost:5173"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký routers
app.include_router(user.router, prefix="/api/user", tags=["User"])
app.include_router(giangvien.router, prefix="/api/teacher", tags=["GiangVien"])
app.include_router(sinhvien.router, prefix="/api/student", tags=["SinhVien"])

@app.get("/")
def root():
    return {"msg": "Hệ thống quản lý điểm tín chỉ - Backend đang chạy!"}
