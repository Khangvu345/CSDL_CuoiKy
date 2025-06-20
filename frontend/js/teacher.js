const API_BASE = "http://127.0.0.1:8000";
const teacherData = JSON.parse(localStorage.getItem("user"));

let allTeacherClasses = [];

if (!teacherData || teacherData.Role !== "teacher") {
    localStorage.clear();
    window.location.replace("../index.html");
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById("teacherName").innerText = teacherData.HoTen || teacherData.Username;
    document.getElementById("logoutBtn").onclick = () => {
        localStorage.clear();
        window.location.replace("../index.html");
    };

    document.getElementById('yearSelect').addEventListener('change', handleFilterChange);
    document.getElementById('semesterSelect').addEventListener('change', handleFilterChange);
    loadAllClassesAndPopulateFilters();
});
async function fetchWithAlert(url, options = {}) {
    try {
        const res = await fetch(url, options);
        if (!res.ok) {
            const errorText = await res.text();
            try {
                const errorJson = JSON.parse(errorText);
                throw new Error(errorJson.detail || errorText);
            } catch (e) {
                throw new Error(errorText || "Lỗi không xác định");
            }
        }
        if (res.status === 204) return null;
        return await res.json();
    } catch (err) {
        alert("Lỗi: " + err.message);
        throw err;
    }
}

async function loadAllClassesAndPopulateFilters() {
    const classListDiv = document.getElementById("classList");
    classListDiv.innerHTML = "<i>Đang tải...</i>";
    try {
        const classes = await fetchWithAlert(`${API_BASE}/api/teacher/my-classes?userid=${teacherData.UserID}`);
        allTeacherClasses = classes; // Lưu lại danh sách tổng

        if (!allTeacherClasses || !allTeacherClasses.length) {
            classListDiv.innerHTML = "<i>Bạn chưa được phân công lớp nào.</i>";
            document.getElementById('filter-container').style.display = 'none'; // Ẩn bộ lọc nếu không có lớp
            return;
        }

        // Điền dữ liệu cho bộ lọc năm học
        const yearSelect = document.getElementById('yearSelect');
        const uniqueYears = [...new Set(allTeacherClasses.map(cls => cls.NamHoc))];
        yearSelect.innerHTML = uniqueYears.map(year => `<option value="${year}">${year} - ${year + 1}</option>`).join('');

        // Tải lại bộ lọc học kỳ và hiển thị lớp cho lựa chọn đầu tiên
        handleFilterChange();

    } catch (err) {
        classListDiv.innerHTML = `<span style='color:red;'>Không tải được lớp: ${err.message}</span>`;
    }
}
function handleFilterChange() {
    const selectedYear = parseInt(document.getElementById('yearSelect').value);
    const semesterSelect = document.getElementById('semesterSelect');
    const currentSemesterValue = semesterSelect.value;

    // Cập nhật danh sách học kỳ dựa trên năm học đã chọn
    const semestersInYear = allTeacherClasses.filter(cls => cls.NamHoc === selectedYear);
    const uniqueSemesters = [...new Map(semestersInYear.map(item => [item['MaKy'], item])).values()];

    semesterSelect.innerHTML = uniqueSemesters.map(s => `<option value="${s.MaKy}">${s.TenKy}</option>`).join('');

    // Cố gắng giữ lại giá trị học kỳ đã chọn nếu có thể
    if (uniqueSemesters.some(s => s.MaKy === currentSemesterValue)) {
        semesterSelect.value = currentSemesterValue;
    }

    // Hiển thị các lớp đã lọc
    displayFilteredClasses();
}

function displayFilteredClasses() {
    const selectedSemester = document.getElementById('semesterSelect').value;
    const classListDiv = document.getElementById("classList");

    const filteredClasses = allTeacherClasses.filter(cls => cls.MaKy === selectedSemester);

    if (!filteredClasses.length) {
        classListDiv.innerHTML = "<i>Không có lớp nào trong học kỳ này.</i>";
        // Ẩn các section chi tiết nếu không có lớp nào được hiển thị
        document.getElementById("studentsSection").style.display = "none";
        document.getElementById("gradesSection").style.display = "none";
        return;
    }

    classListDiv.innerHTML = filteredClasses.map(
        cls => `<button class="class-item" data-loptc="${cls.MaLopTC}" data-label="${cls.TenMH} (${cls.TenKy})">${cls.TenMH}</button>`
    ).join("");

    // Gán lại sự kiện click cho các nút lớp học
    document.querySelectorAll(".class-item").forEach(btn => {
        btn.onclick = () => {
            document.querySelectorAll(".class-item.active").forEach(activeBtn => activeBtn.classList.remove("active"));
            btn.classList.add("active");
            showClassDetail(btn.dataset.loptc, btn.dataset.label);
        }
    });
}

async function showClassDetail(maLopTC, label) {
    document.getElementById("studentsSection").style.display = "block";
    document.getElementById("gradesSection").style.display = "block";
    document.getElementById("selectedClass").innerText = label;
    document.getElementById("selectedClassGrade").innerText = label;

    loadStudentsInfo(maLopTC);
    loadGradesInfo(maLopTC);
}

async function loadStudentsInfo(maLopTC) {
     const studentsInfoDiv = document.getElementById("studentsInfo");
     studentsInfoDiv.innerHTML = "<i>Đang tải danh sách sinh viên...</i>";
     try {
        const students = await fetchWithAlert(`${API_BASE}/api/teacher/class/${maLopTC}/students-info?userid=${teacherData.UserID}`);
        studentsInfoDiv.innerHTML = `
        <table>
            <thead>
                <tr><th>Mã SV</th><th>Họ Tên</th><th>Lớp HC</th><th>Chuyên ngành</th><th>Ngày sinh</th><th>Giới tính</th><th>Email</th></tr>
            </thead>
            <tbody>
            ${students.map(s => `
                <tr>
                    <td>${s.MaSV}</td><td>${s.HoTen}</td><td>${s.MaLopHC || ''}</td>
                    <td>${s.MaChuyenNganh || ''}</td><td>${s.NgaySinh || ""}</td>
                    <td>${s.GioiTinh || ""}</td><td>${s.Email || ""}</td>
                </tr>
            `).join("")}
            </tbody>
        </table>`;
    } catch (err) {
        studentsInfoDiv.innerHTML = `<span style='color:red;'>Không tải được sinh viên: ${err.message}</span>`;
    }
}

async function loadGradesInfo(maLopTC) {
    const gradesInfoDiv = document.getElementById("gradesInfo");
    gradesInfoDiv.innerHTML = "<i>Đang tải bảng điểm...</i>";
    try {
        const grades = await fetchWithAlert(`${API_BASE}/api/teacher/class/${maLopTC}/grades?userid=${teacherData.UserID}`);
        gradesInfoDiv.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>Mã SV</th><th>Họ tên</th><th>CC</th><th>GK</th><th>CK</th><th>TH</th>
                    <th>Tổng (10)</th><th>Điểm chữ</th><th>Trạng thái</th><th>Thao tác</th>
                </tr>
            </thead>
            <tbody>
            ${grades.map(g => `
                <tr id="row-${g.MaSV}">
                    <td>${g.MaSV}</td><td>${g.HoTen}</td>
                    <td><input size="3" type="number" step="0.1" min="0" max="10" value="${g.DiemChuyenCan ?? ""}" id="cc_${g.MaSV}" /></td>
                    <td><input size="3" type="number" step="0.1" min="0" max="10" value="${g.DiemGiuaKy ?? ""}" id="gk_${g.MaSV}" /></td>
                    <td><input size="3" type="number" step="0.1" min="0" max="10" value="${g.DiemCuoiKy ?? ""}" id="ck_${g.MaSV}" /></td>
                    <td><input size="3" type="number" step="0.1" min="0" max="10" value="${g.DiemThucHanh ?? ""}" id="th_${g.MaSV}" /></td>
                    <td><b>${g.DiemTongKetHe10 ?? ""}</b></td>
                    <td>${g.DiemChu ?? ""}</td>
                    <td>${g.TrangThaiQuaMon ?? ""}</td>
                    <td>
                        <button onclick="saveGrade('${maLopTC}','${g.MaSV}')">Lưu</button>
                        <button class="delete-btn" onclick="deleteGrade('${maLopTC}','${g.MaSV}')">Xoá</button>
                    </td>
                </tr>
            `).join("")}
            </tbody>
        </table>`;
    } catch (err) {
        gradesInfoDiv.innerHTML = `<span style='color:red;'>Không tải được bảng điểm: ${err.message}</span>`;
    }
}

window.saveGrade = async function(maLopTC, maSV) {
    const data = {
        DiemChuyenCan: parseFloat(document.getElementById(`cc_${maSV}`).value) || null,
        DiemGiuaKy: parseFloat(document.getElementById(`gk_${maSV}`).value) || null,
        DiemCuoiKy: parseFloat(document.getElementById(`ck_${maSV}`).value) || null,
        DiemThucHanh: parseFloat(document.getElementById(`th_${maSV}`).value) || null,
    };
    try {
        await fetchWithAlert(`${API_BASE}/api/teacher/class/${maLopTC}/student/${maSV}/grades?userid=${teacherData.UserID}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        alert("Lưu điểm thành công!");
        loadGradesInfo(maLopTC);
    } catch (err) {
    }
};

window.deleteGrade = async function(maLopTC, maSV) {
    if (!window.confirm(`Bạn có chắc chắn muốn xoá toàn bộ điểm của sinh viên ${maSV} không?`)) return;
    try {
        await fetchWithAlert(`${API_BASE}/api/teacher/class/${maLopTC}/student/${maSV}/grades?userid=${teacherData.UserID}`, {
            method: "DELETE"
        });
        alert("Đã xoá điểm!");
        loadGradesInfo(maLopTC);
    } catch (err) {
    }
}