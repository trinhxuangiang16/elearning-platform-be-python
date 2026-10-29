from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from core.authentication import JWTAuthentication, OptionalJWTAuthentication
from core.permissions import IsAuthenticatedCustom
from core.responses import success_response, raw_response
from core.services import course_service
from core.views import get_query_param


class CategoriesView(APIView):
    def get(self, request):
        result = course_service.get_categories()
        return raw_response(result)


class CoursesByCategoryView(APIView):
    def get(self, request):
        ma_danh_muc = get_query_param(request, "maDanhMuc", "MaDanhMuc")
        result = course_service.get_courses_by_category(ma_danh_muc)
        return raw_response(result)


class CourseListView(APIView):
    authentication_classes = [OptionalJWTAuthentication]

    def get(self, request):
        ten_khoa_hoc = get_query_param(request, "tenKhoaHoc", "TenKhoaHoc")
        ma_nhom = get_query_param(request, "maNhom", "MaNhom")
        result = course_service.get_course_list(
            ten_khoa_hoc=ten_khoa_hoc,
            ma_nhom=ma_nhom,
            current_user=request.user,
        )
        return raw_response(result)


class CourseDetailView(APIView):
    def get(self, request):
        ma_khoa_hoc = get_query_param(request, "maKhoaHoc", "MaKhoaHoc")
        result = course_service.get_course_detail(ma_khoa_hoc)
        return raw_response(result)


class AddCourseView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request):
        result = course_service.add_course(request.data, request.user)
        return success_response(result, "Thêm khóa học thành công")


class UpdateCourseView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def put(self, request):
        result = course_service.update_course(request.data)
        return success_response(result, "Cập nhật khóa học thành công")


class UploadCourseImageView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        uploaded_file = request.FILES.get("file") or request.FILES.get("File")
        ma_khoa_hoc = request.data.get("maKhoaHoc") or get_query_param(request, "maKhoaHoc")
        result = course_service.upload_course_image(uploaded_file, ma_khoa_hoc)
        return success_response(result, "Tải lên hình ảnh khóa học thành công")


class DeleteCourseView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def delete(self, request):
        ma_khoa_hoc = get_query_param(request, "maKhoaHoc", "MaKhoaHoc")
        if not ma_khoa_hoc and isinstance(request.data, dict):
            ma_khoa_hoc = request.data.get("maKhoaHoc") or request.data.get("MaKhoaHoc")
        result = course_service.delete_course(ma_khoa_hoc)
        return success_response(result, "Xóa khóa học thành công")


class RegisterCourseView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request):
        ma_khoa_hoc = request.data.get("maKhoaHoc") or request.data.get("MaKhoaHoc")
        tai_khoan = request.data.get("taiKhoan") or (request.user.tai_khoan if request.user else None)
        result = course_service.register_course(ma_khoa_hoc, tai_khoan)
        return success_response(result, "Đăng ký khóa học thành công")


class UnenrollCourseView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request):
        ma_khoa_hoc = request.data.get("maKhoaHoc") or request.data.get("MaKhoaHoc")
        tai_khoan = request.data.get("taiKhoan") or (request.user.tai_khoan if request.user else None)
        result = course_service.unenroll_course(ma_khoa_hoc, tai_khoan)
        return success_response(result, "Hủy ghi danh khóa học thành công!")
