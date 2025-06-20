const API_BASE_URL = 'http://127.0.0.1:8000';
const studentData = JSON.parse(localStorage.getItem('user'));

if (!studentData || studentData.Role !== 'student') {
    localStorage.clear();
    window.location.replace('../index.html');
}

async function fetchWithAuth(url, options = {}) {
    const headers = { 'Content-Type': 'application/json', ...options.headers };
    const response = await fetch(url, { ...options, headers });
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Lỗi không xác định từ server' }));
        throw new Error(errorData.detail);
    }
    return response.json();
}

async function loadStudentInfo() {
    const studentNameEl = document.getElementById('studentName');
    const studentIdEl = document.getElementById('studentId');
    const majorNameEl = document.getElementById('majorName');

    // Tạm thời hiển thị tên từ localStorage trong lúc tải
    studentNameEl.innerText = studentData.HoTen || studentData.Username;

    try {
        // Gọi API mới để lấy thông tin chi tiết
        const details = await fetchWithAuth(`${API_BASE_URL}/api/student/details?userid=${studentData.UserID}`);

        // Cập nhật giao diện với dữ liệu đầy đủ từ API
        studentNameEl.innerText = details.HoTen;
        studentIdEl.innerText = `Mã SV: ${details.MaSV}`;
        majorNameEl.innerText = `Chuyên ngành: ${details.TenChuyenNganh || 'Chưa có'}`;
    } catch (error) {
        console.error("Lỗi tải thông tin chi tiết:", error);
        // Nếu lỗi, vẫn hiển thị thông tin cơ bản
        studentIdEl.innerText = `Mã SV: ${studentData.UserID}`;
        majorNameEl.innerText = 'Chuyên ngành: Không tải được';
    }
}

// js/student.js

async function loadProgress() {
    const progressInfo = document.getElementById('progress-info');
    progressInfo.innerHTML = `<i>Đang tải...</i>`;
    try {
        const progress = await fetchWithAuth(`${API_BASE_URL}/api/student/progress?userid=${studentData.UserID}`);

        // AN TOÀN HƠN: Kiểm tra xem progress.DiemTBHe10 có phải là số không. Nếu không, gán giá trị mặc định.
        const gpa10 = (typeof progress.DiemTBHe10 === 'number')
            ? progress.DiemTBHe10.toFixed(2)
            : 'Chưa có';

        // Tương tự, kiểm tra cho progress.DiemTBHe4
        const gpa4 = (typeof progress.DiemTBHe4 === 'number')
            ? progress.DiemTBHe4.toFixed(2)
            : 'Chưa có';

        // Cập nhật HTML với các giá trị đã được kiểm tra
        progressInfo.innerHTML = `
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 1rem;">
                <p><strong>Tín chỉ tích lũy:</strong> ${progress.TongTinChiDat || 0} / ${progress.TongTinChi || 0}</p>
                <p><strong>Điểm TB tích lũy (Hệ 10):</strong> ${gpa10}</p>
                <p><strong>Điểm TB tích lũy (Hệ 4):</strong> ${gpa4}</p>
            </div>
        `;
    } catch (error) {
        // Nếu có lỗi khác xảy ra, nó vẫn sẽ được hiển thị ở đây
        progressInfo.innerHTML = `<p style="color:red;">Lỗi tải tiến độ: ${error.message}</p>`;
    }
}

async function loadSemestersAndCourses() {
    const semesterSelect = document.getElementById('semesterSelect');
    const courseSelect = document.getElementById('courseSelect');
    try {
        const semesters = await fetchWithAuth(`${API_BASE_URL}/api/student/semesters`);
        if (semesters.length > 0) {
            semesterSelect.innerHTML = '<option value="">-- Chọn kỳ học --</option>' +
                semesters.map(s => `<option value="${s.MaKy}">${s.TenKy}</option>`).join('');
        } else {
            semesterSelect.innerHTML = '<option value="">Không có dữ liệu</option>';
        }

        const courses = await fetchWithAuth(`${API_BASE_URL}/api/student/my-classes?userid=${studentData.UserID}`);
        if (courses.length > 0) {
            courseSelect.innerHTML = '<option value="">-- Chọn lớp tín chỉ --</option>' +
                courses.map(c => `<option value="${c.MaLopTC}">${c.TenMH} (${c.TenKy})</option>`).join('');
        } else {
            courseSelect.innerHTML = '<option value="">Không có dữ liệu</option>';
        }
    } catch (error) {
        alert(`Lỗi tải dữ liệu các kỳ học/lớp: ${error.message}`);
    }
}

async function viewSemesterSummary() {
    const semesterId = document.getElementById('semesterSelect').value;
    const summaryDiv = document.getElementById('semesterSummary');
    if (!semesterId) {
        summaryDiv.innerHTML = '';
        return;
    }
    summaryDiv.innerHTML = `<i>Đang tải điểm kỳ ${semesterId}...</i>`;
    try {
        const data = await fetchWithAuth(`${API_BASE_URL}/api/student/semester/${semesterId}/grades?userid=${studentData.UserID}`);
        const summary = data.tongket;
        if (summary) {
            summaryDiv.innerHTML = `
                <h4>Kết quả học tập kỳ ${semesterId}</h4>
                <p><strong>Điểm TB (10):</strong> ${summary.DiemTBKyHe10}</p>
                <p><strong>Điểm TB (4):</strong> ${summary.DiemTBKyHe4}</p>
                <p><strong>Tín chỉ đạt:</strong> ${summary.SoTCDatKy}</p>
                <p><strong>Xếp loại:</strong> ${summary.XepLoaiHocLucKy}</p>
            `;
        } else {
             summaryDiv.innerHTML = `<p style="color:red;">Không có dữ liệu tổng kết cho kỳ này.</p>`;
        }
    } catch (error) {
        summaryDiv.innerHTML = `<p style="color:red;">Lỗi tải tổng kết kỳ: ${error.message}</p>`;
    }
}

async function viewClassDetails() {
    const classId = document.getElementById('courseSelect').value;
    const detailsDiv = document.getElementById('classDetails');
    if (!classId) {
        detailsDiv.innerHTML = '';
        return;
    }
    detailsDiv.innerHTML = `<i>Đang tải điểm lớp ${classId}...</i>`;
    try {
        const grade = await fetchWithAuth(`${API_BASE_URL}/api/student/class/${classId}/grades?userid=${studentData.UserID}`);
        detailsDiv.innerHTML = `
            <h4>Chi tiết điểm: ${grade.TenMH}</h4>
            <table>
                <tbody>
                    <tr><th>Điểm chuyên cần:</th><td>${grade.DiemChuyenCan ?? 'N/A'}</td></tr>
                    <tr><th>Điểm giữa kỳ:</th><td>${grade.DiemGiuaKy ?? 'N/A'}</td></tr>
                    <tr><th>Điểm cuối kỳ:</th><td>${grade.DiemCuoiKy ?? 'N/A'}</td></tr>
                    <tr><th>Điểm thực hành:</th><td>${grade.DiemThucHanh ?? 'N/A'}</td></tr>
                    <tr style="font-weight: bold;"><th>Tổng kết (10):</th><td>${grade.DiemTongKetHe10 ?? 'N/A'}</td></tr>
                    <tr><th>Điểm chữ:</th><td>${grade.DiemChu ?? 'N/A'}</td></tr>
                    <tr><th>Trạng thái:</th><td>${grade.TrangThaiQuaMon ?? 'N/A'}</td></tr>
                </tbody>
            </table>`;
    } catch (error) {
        detailsDiv.innerHTML = `<p style="color:red;">Lỗi tải chi tiết lớp: ${error.message}</p>`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('logoutBtn').addEventListener('click', () => {
        localStorage.clear();
        window.location.replace('../index.html');
    });
    document.getElementById('viewSemesterBtn').addEventListener('click', viewSemesterSummary);
    document.getElementById('viewClassBtn').addEventListener('click', viewClassDetails);
    loadStudentInfo();
    loadProgress();
    loadSemestersAndCourses();
});