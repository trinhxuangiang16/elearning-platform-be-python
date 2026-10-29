from rest_framework.views import APIView
from core.authentication import JWTAuthentication, OptionalJWTAuthentication
from core.permissions import IsAuthenticatedCustom, IsInstructorOrAdmin
from core.responses import success_response, raw_response, get_iso_now
from core.services import (
    syllabus_service,
    progress_service,
    assignment_service,
    note_service,
    analytics_service,
)
from core.views import get_query_param


API_URL_CATALOG = {
    "xacThucVaHoSo": [
        {"method": "POST", "url": "/api/QuanLyNguoiDung/DangKy", "moTa": "Đăng ký tài khoản học viên"},
        {"method": "POST", "url": "/api/QuanLyNguoiDung/DangNhap", "moTa": "Đăng nhập và nhận JWT Token"},
        {"method": "POST", "url": "/api/QuanLyNguoiDung/ThongTinTaiKhoan", "moTa": "Lấy hồ sơ cá nhân và khóa học đã ghi danh"},
        {"method": "PUT", "url": "/api/QuanLyNguoiDung/CapNhatThongTinNguoiDung", "moTa": "Cập nhật thông tin tài khoản"},
    ],
    "quanLyNguoiDung": [
        {"method": "GET", "url": "/api/QuanLyNguoiDung/LayDanhSachNguoiDung", "moTa": "Lấy danh sách người dùng"},
        {"method": "GET", "url": "/api/QuanLyNguoiDung/TimKiemNguoiDung?tuKhoa=", "moTa": "Tìm kiếm người dùng theo từ khóa"},
        {"method": "POST", "url": "/api/QuanLyNguoiDung/ThemNguoiDung", "moTa": "Thêm người dùng mới (Quản trị viên)"},
        {"method": "DELETE", "url": "/api/QuanLyNguoiDung/XoaNguoiDung?TaiKhoan=", "moTa": "Xóa tài khoản người dùng"},
        {"method": "POST", "url": "/api/QuanLyNguoiDung/LayDanhSachKhoaHocChoXetDuyet", "moTa": "Lấy danh sách khóa học chờ xét duyệt"},
        {"method": "POST", "url": "/api/QuanLyNguoiDung/LayDanhSachHocVienKhoaHoc", "moTa": "Lấy danh sách học viên trong khóa học"},
    ],
    "quanLyKhoaHoc": [
        {"method": "GET", "url": "/api/QuanLyKhoaHoc/LayDanhMucKhoaHoc", "moTa": "Lấy danh sách danh mục khóa học"},
        {"method": "GET", "url": "/api/QuanLyKhoaHoc/LayKhoaHocTheoDanhMuc?maDanhMuc=", "moTa": "Lấy khóa học theo danh mục"},
        {"method": "GET", "url": "/api/QuanLyKhoaHoc/LayDanhSachKhoaHoc", "moTa": "Lấy danh sách khóa học (Tìm kiếm BM25 & Gợi ý khóa học)"},
        {"method": "GET", "url": "/api/QuanLyKhoaHoc/LayThongTinKhoaHoc?maKhoaHoc=", "moTa": "Lấy chi tiết khóa học"},
        {"method": "POST", "url": "/api/QuanLyKhoaHoc/ThemKhoaHoc", "moTa": "Thêm khóa học mới"},
        {"method": "PUT", "url": "/api/QuanLyKhoaHoc/CapNhatKhoaHoc", "moTa": "Cập nhật thông tin khóa học"},
        {"method": "POST", "url": "/api/QuanLyKhoaHoc/UploadHinhAnhKhoaHoc", "moTa": "Tải lên hình ảnh khóa học"},
        {"method": "DELETE", "url": "/api/QuanLyKhoaHoc/XoaKhoaHoc?maKhoaHoc=", "moTa": "Xóa khóa học"},
        {"method": "POST", "url": "/api/QuanLyKhoaHoc/DangKyKhoaHoc", "moTa": "Ghi danh khóa học"},
        {"method": "POST", "url": "/api/QuanLyKhoaHoc/HuyGhiDanh", "moTa": "Hủy ghi danh khóa học"},
    ],
    "giaoTrinhVaBaiHoc": [
        {"method": "GET", "url": "/api/v1/courses/<maKhoaHoc>/syllabus", "moTa": "Xem đề cương chương và bài học"},
        {"method": "POST", "url": "/api/v1/admin/sections", "moTa": "Tạo chương học mới"},
        {"method": "PUT", "url": "/api/v1/admin/sections/<id>", "moTa": "Cập nhật chương học"},
        {"method": "DELETE", "url": "/api/v1/admin/sections/<id>", "moTa": "Xóa chương học"},
        {"method": "POST", "url": "/api/v1/admin/lessons", "moTa": "Tạo bài học mới"},
        {"method": "PUT", "url": "/api/v1/admin/lessons/<id>", "moTa": "Cập nhật bài học"},
        {"method": "DELETE", "url": "/api/v1/admin/lessons/<id>", "moTa": "Xóa bài học"},
    ],
    "tienDoVaGhiChu": [
        {"method": "POST", "url": "/api/v1/lessons/<maBaiHoc>/progress", "moTa": "Cập nhật tiến độ xem video bài học"},
        {"method": "GET", "url": "/api/v1/courses/<maKhoaHoc>/my-progress", "moTa": "Xem tiến độ hoàn thành khóa học"},
        {"method": "GET", "url": "/api/v1/users/resume-learning", "moTa": "Lấy bài học đang học gần nhất"},
        {"method": "GET", "url": "/api/v1/lessons/<maBaiHoc>/notes", "moTa": "Lấy danh sách ghi chú trong bài học"},
        {"method": "POST", "url": "/api/v1/lessons/<maBaiHoc>/notes", "moTa": "Tạo ghi chú mới theo mốc thời gian video"},
        {"method": "DELETE", "url": "/api/v1/notes/<maGhiChu>", "moTa": "Xóa ghi chú bài học"},
    ],
    "baiTapVaChamDiem": [
        {"method": "GET", "url": "/api/v1/lessons/<maBaiHoc>/assignment", "moTa": "Xem đề bài tập của bài học"},
        {"method": "POST", "url": "/api/v1/assignments/<maBaiTap>/submit", "moTa": "Học viên nộp bài tập"},
        {"method": "GET", "url": "/api/v1/users/my-grades", "moTa": "Xem bảng điểm và GPA cá nhân"},
        {"method": "POST", "url": "/api/v1/admin/lessons/<maBaiHoc>/assignment", "moTa": "Giảng viên tạo bài tập mới"},
        {"method": "PUT", "url": "/api/v1/admin/assignments/<maBaiTap>", "moTa": "Giảng viên cập nhật bài tập"},
        {"method": "DELETE", "url": "/api/v1/admin/assignments/<maBaiTap>", "moTa": "Giảng viên xóa bài tập"},
        {"method": "GET", "url": "/api/v1/admin/assignments/<maBaiTap>/submissions", "moTa": "Xem danh sách bài nộp của học viên"},
        {"method": "PUT", "url": "/api/v1/admin/submissions/<maLuotNop>/grade", "moTa": "Giảng viên chấm điểm và nhận xét bài nộp"},
    ],
    "thongKeHeThong": [
        {"method": "GET", "url": "/api/v1/admin/analytics/quick-stats", "moTa": "Thống kê tổng quan toàn hệ thống"},
        {"method": "GET", "url": "/api/v1/admin/analytics/top-students", "moTa": "Danh sách học viên hoàn thành nhiều bài học nhất"},
    ],
}


class HealthCheckView(APIView):
    def get(self, request):
        return raw_response({
            "status": "OK",
            "service": "Hệ thống Quản lý Đào tạo Trực tuyến (E-Learning Web API)",
            "version": "1.0.0",
            "donViTienTe": "VND",
            "time": get_iso_now(),
            "danhSachApiUrl": API_URL_CATALOG,
        })


class SyllabusView(APIView):
    authentication_classes = [OptionalJWTAuthentication]

    def get(self, request, maKhoaHoc):
        result = syllabus_service.get_syllabus(maKhoaHoc, request.user)
        return success_response(result, "Lấy đề cương khóa học thành công")


class AdminSectionCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstructorOrAdmin]

    def post(self, request):
        result = syllabus_service.create_section(request.data)
        return success_response(result, "Tạo chương học thành công")


class AdminSectionDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstructorOrAdmin]

    def put(self, request, id):
        result = syllabus_service.update_section(id, request.data)
        return success_response(result, "Cập nhật chương học thành công")

    def delete(self, request, id):
        result = syllabus_service.delete_section(id)
        return success_response(result, "Xóa chương học thành công")


class AdminLessonCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstructorOrAdmin]

    def post(self, request):
        result = syllabus_service.create_lesson(request.data)
        return success_response(result, "Tạo bài học thành công")


class AdminLessonDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstructorOrAdmin]

    def put(self, request, id):
        result = syllabus_service.update_lesson(id, request.data)
        return success_response(result, "Cập nhật bài học thành công")

    def delete(self, request, id):
        result = syllabus_service.delete_lesson(id)
        return success_response(result, "Xóa bài học thành công")


class LessonProgressView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request, maBaiHoc):
        strict_query = get_query_param(request, "strict_anticheat", default="false")
        strict_header = request.headers.get("X-Strict-Anticheat", "false")
        is_strict = (
            str(strict_query).lower() == "true"
            or str(strict_header).lower() == "true"
        )
        result = progress_service.update_lesson_progress(
            request.user.tai_khoan,
            maBaiHoc,
            request.data,
            strict_anticheat=is_strict,
        )
        return success_response(result, "Cập nhật tiến độ bài học thành công")


class CourseMyProgressView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def get(self, request, maKhoaHoc):
        result = progress_service.get_course_progress(request.user.tai_khoan, maKhoaHoc)
        return success_response(result, "Lấy tiến độ khóa học thành công")


class ResumeLearningView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def get(self, request):
        result = progress_service.get_resume_learning(request.user.tai_khoan)
        return success_response(result, "Lấy bài học gần nhất thành công")


class LessonAssignmentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def get(self, request, maBaiHoc):
        result = assignment_service.get_lesson_assignment(maBaiHoc, request.user)
        return success_response(result, "Lấy thông tin bài tập thành công")


class SubmitAssignmentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request, maBaiTap):
        result = assignment_service.submit_assignment(
            request.user.tai_khoan,
            maBaiTap,
            request.data,
        )
        return success_response(result, "Nộp bài tập thành công")


class MyGradesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def get(self, request):
        result = assignment_service.get_my_grades(request.user.tai_khoan)
        return success_response(result, "Lấy bảng điểm cá nhân thành công")


class AdminAssignmentSubmissionsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstructorOrAdmin]

    def get(self, request, maBaiTap):
        result = assignment_service.get_submissions_by_assignment(maBaiTap)
        return success_response(result, "Lấy danh sách bài nộp thành công")


class AdminGradeSubmissionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstructorOrAdmin]

    def put(self, request, maLuotNop):
        result = assignment_service.grade_submission(maLuotNop, request.data)
        return success_response(result, "Chấm điểm bài nộp thành công")


class AdminLessonAssignmentCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstructorOrAdmin]

    def post(self, request, maBaiHoc):
        result = assignment_service.create_assignment(maBaiHoc, request.data)
        return success_response(result, "Tạo bài tập thành công")


class AdminAssignmentDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstructorOrAdmin]

    def put(self, request, maBaiTap):
        result = assignment_service.update_assignment(maBaiTap, request.data)
        return success_response(result, "Cập nhật bài tập thành công")

    def delete(self, request, maBaiTap):
        result = assignment_service.delete_assignment(maBaiTap)
        return success_response(result, "Xóa bài tập thành công")


class AdminQuickStatsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstructorOrAdmin]

    def get(self, request):
        result = analytics_service.get_quick_stats()
        return success_response(result, "Lấy thống kê hệ thống thành công")


class AdminTopStudentsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstructorOrAdmin]

    def get(self, request):
        result = analytics_service.get_top_students()
        return success_response(result, "Lấy danh sách học viên tiêu biểu thành công")


class LessonNotesView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def get(self, request, maBaiHoc):
        result = note_service.get_notes_by_lesson(request.user.tai_khoan, maBaiHoc)
        return success_response(result, "Lấy danh sách ghi chú thành công")

    def post(self, request, maBaiHoc):
        result = note_service.create_note(request.user.tai_khoan, maBaiHoc, request.data)
        return success_response(result, "Tạo ghi chú thành công")


class NoteDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def delete(self, request, maGhiChu):
        result = note_service.delete_note(request.user.tai_khoan, maGhiChu)
        return success_response(result, "Xóa ghi chú thành công")
