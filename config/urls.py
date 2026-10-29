from django.conf import settings
from django.urls import re_path
from django.views.static import serve
from core.views import user_legacy_views, course_legacy_views, v1_views

urlpatterns = [
    re_path(r"^$", v1_views.HealthCheckView.as_view()),
    re_path(r"^api/?$", v1_views.HealthCheckView.as_view()),

    re_path(r"^api/QuanLyNguoiDung/DangKy/?$", user_legacy_views.RegisterView.as_view()),
    re_path(r"^api/QuanLyNguoiDung/DangNhap/?$", user_legacy_views.LoginView.as_view()),
    re_path(r"^api/QuanLyNguoiDung/ThongTinTaiKhoan/?$", user_legacy_views.UserProfileView.as_view()),
    re_path(r"^api/QuanLyNguoiDung/CapNhatThongTinNguoiDung/?$", user_legacy_views.UpdateProfileView.as_view()),
    re_path(r"^api/QuanLyNguoiDung/LayDanhSachNguoiDung/?$", user_legacy_views.UsersListView.as_view()),
    re_path(r"^api/QuanLyNguoiDung/TimKiemNguoiDung/?$", user_legacy_views.SearchUsersView.as_view()),
    re_path(r"^api/QuanLyNguoiDung/ThemNguoiDung/?$", user_legacy_views.AddUserView.as_view()),
    re_path(r"^api/QuanLyNguoiDung/XoaNguoiDung/?$", user_legacy_views.DeleteUserView.as_view()),
    re_path(r"^api/QuanLyNguoiDung/LayDanhSachKhoaHocChoXetDuyet/?$", user_legacy_views.CoursesPendingView.as_view()),
    re_path(r"^api/QuanLyNguoiDung/LayDanhSachHocVienKhoaHoc/?$", user_legacy_views.StudentsInCourseView.as_view()),

    re_path(r"^api/QuanLyKhoaHoc/LayDanhMucKhoaHoc/?$", course_legacy_views.CategoriesView.as_view()),
    re_path(r"^api/QuanLyKhoaHoc/LayKhoaHocTheoDanhMuc/?$", course_legacy_views.CoursesByCategoryView.as_view()),
    re_path(r"^api/QuanLyKhoaHoc/LayDanhSachKhoaHoc/?$", course_legacy_views.CourseListView.as_view()),
    re_path(r"^api/QuanLyKhoaHoc/LayThongTinKhoaHoc/?$", course_legacy_views.CourseDetailView.as_view()),
    re_path(r"^api/QuanLyKhoaHoc/ThemKhoaHoc/?$", course_legacy_views.AddCourseView.as_view()),
    re_path(r"^api/QuanLyKhoaHoc/CapNhatKhoaHoc/?$", course_legacy_views.UpdateCourseView.as_view()),
    re_path(r"^api/QuanLyKhoaHoc/UploadHinhAnhKhoaHoc/?$", course_legacy_views.UploadCourseImageView.as_view()),
    re_path(r"^api/QuanLyKhoaHoc/XoaKhoaHoc/?$", course_legacy_views.DeleteCourseView.as_view()),
    re_path(r"^api/QuanLyKhoaHoc/DangKyKhoaHoc/?$", course_legacy_views.RegisterCourseView.as_view()),
    re_path(r"^api/QuanLyKhoaHoc/HuyGhiDanh/?$", course_legacy_views.UnenrollCourseView.as_view()),

    re_path(r"^api/v1/courses/(?P<maKhoaHoc>[^/]+)/syllabus/?$", v1_views.SyllabusView.as_view()),
    re_path(r"^api/v1/admin/sections/?$", v1_views.AdminSectionCreateView.as_view()),
    re_path(r"^api/v1/admin/sections/(?P<id>\d+)/?$", v1_views.AdminSectionDetailView.as_view()),
    re_path(r"^api/v1/admin/lessons/?$", v1_views.AdminLessonCreateView.as_view()),
    re_path(r"^api/v1/admin/lessons/(?P<id>\d+)/?$", v1_views.AdminLessonDetailView.as_view()),

    re_path(r"^api/v1/lessons/(?P<maBaiHoc>\d+)/progress/?$", v1_views.LessonProgressView.as_view()),
    re_path(r"^api/v1/courses/(?P<maKhoaHoc>[^/]+)/my-progress/?$", v1_views.CourseMyProgressView.as_view()),
    re_path(r"^api/v1/users/resume-learning/?$", v1_views.ResumeLearningView.as_view()),

    re_path(r"^api/v1/lessons/(?P<maBaiHoc>\d+)/assignment/?$", v1_views.LessonAssignmentView.as_view()),
    re_path(r"^api/v1/assignments/(?P<maBaiTap>\d+)/submit/?$", v1_views.SubmitAssignmentView.as_view()),
    re_path(r"^api/v1/users/my-grades/?$", v1_views.MyGradesView.as_view()),
    re_path(r"^api/v1/admin/assignments/(?P<maBaiTap>\d+)/submissions/?$", v1_views.AdminAssignmentSubmissionsView.as_view()),
    re_path(r"^api/v1/admin/submissions/(?P<maLuotNop>\d+)/grade/?$", v1_views.AdminGradeSubmissionView.as_view()),
    re_path(r"^api/v1/admin/lessons/(?P<maBaiHoc>\d+)/assignment/?$", v1_views.AdminLessonAssignmentCreateView.as_view()),
    re_path(r"^api/v1/admin/assignments/(?P<maBaiTap>\d+)/?$", v1_views.AdminAssignmentDetailView.as_view()),

    re_path(r"^api/v1/admin/analytics/quick-stats/?$", v1_views.AdminQuickStatsView.as_view()),
    re_path(r"^api/v1/admin/analytics/top-students/?$", v1_views.AdminTopStudentsView.as_view()),

    re_path(r"^api/v1/lessons/(?P<maBaiHoc>\d+)/notes/?$", v1_views.LessonNotesView.as_view()),
    re_path(r"^api/v1/notes/(?P<maGhiChu>\d+)/?$", v1_views.NoteDeleteView.as_view()),

    re_path(r"^uploads/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]

