from rest_framework.views import APIView
from core.authentication import JWTAuthentication
from core.permissions import IsAuthenticatedCustom
from core.responses import success_response, raw_response
from core.services import user_service
from core.views import get_query_param


class RegisterView(APIView):
    def post(self, request):
        result = user_service.register_user(request.data)
        return success_response(result, "Đăng ký tài khoản thành công")


class LoginView(APIView):
    def post(self, request):
        result = user_service.login_user(request.data)
        return success_response(result, "Đăng nhập thành công")


class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request):
        result = user_service.get_user_profile(request.user)
        return raw_response(result)


class UpdateProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def put(self, request):
        result = user_service.update_user_profile(request.user, request.data)
        return success_response(result, "Cập nhật thông tin tài khoản thành công")


class UsersListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def get(self, request):
        result = user_service.get_users_list()
        return raw_response(result)


class SearchUsersView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def get(self, request):
        tu_khoa = get_query_param(request, "tuKhoa", "tukhoa", default="")
        result = user_service.search_users(tu_khoa)
        return raw_response(result)


class AddUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request):
        result = user_service.add_user(request.data)
        return success_response(result, "Thêm người dùng thành công")


class DeleteUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def delete(self, request):
        tai_khoan = get_query_param(request, "TaiKhoan", "taiKhoan")
        if not tai_khoan and isinstance(request.data, dict):
            tai_khoan = request.data.get("TaiKhoan") or request.data.get("taiKhoan")
        result = user_service.delete_user(tai_khoan)
        return success_response(result, "Xóa người dùng thành công")


class CoursesPendingView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request):
        tai_khoan = request.data.get("taiKhoan") if isinstance(request.data, dict) else None
        result = user_service.get_courses_pending(tai_khoan)
        return raw_response(result)


class StudentsInCourseView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request):
        ma_khoa_hoc = None
        if isinstance(request.data, dict):
            ma_khoa_hoc = request.data.get("maKhoaHoc") or request.data.get("MaKhoaHoc")
        if not ma_khoa_hoc:
            ma_khoa_hoc = get_query_param(request, "maKhoaHoc", "MaKhoaHoc")
        result = user_service.get_students_in_course(ma_khoa_hoc)
        return raw_response(result)
