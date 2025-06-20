const API_BASE_URL = 'http://127.0.0.1:8000';

document.getElementById('loginForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = '';

    const loginData = {
        Username: username,
        Password: password
    };

    try {
        const response = await fetch(`${API_BASE_URL}/api/user/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        });

        const data = await response.json();

        if (!response.ok) {
            errorMessage.textContent = data.detail || 'Đăng nhập thất bại.';
            return;
        }

        // Lưu toàn bộ thông tin user vào localStorage
        localStorage.setItem('user', JSON.stringify(data));

        switch (data.Role) {
            case 'student':
                // Giả sử file dashboard nằm trong thư mục student
                window.location.replace('student/dashboard.html');
                break;
            case 'teacher':
                // Giả sử file dashboard nằm trong thư mục teacher
                window.location.replace('teacher/dashboard.html');
                break;
            case 'manager':
                alert('Chức năng Quản lý chưa có giao diện.');
                break;
            default:
                errorMessage.textContent = 'Vai trò không xác định.';
        }
    } catch (error) {
        console.error('Lỗi đăng nhập:', error);
        errorMessage.textContent = 'Lỗi kết nối. Vui lòng đảm bảo server backend đang chạy.';
    }
});