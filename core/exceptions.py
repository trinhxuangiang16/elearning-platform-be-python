from rest_framework.views import exception_handler
from core.responses import error_response


class AppException(Exception):
    status_code = 400
    default_message = "Đã xảy ra lỗi"

    def __init__(self, message=None, status_code=None):
        self.message = message or self.default_message
        if status_code is not None:
            self.status_code = status_code
        super().__init__(self.message)


class BadRequestException(AppException):
    status_code = 400
    default_message = "Yêu cầu không hợp lệ"


class UnauthorizedException(AppException):
    status_code = 401
    default_message = "Chưa xác thực"


class ForbiddenException(AppException):
    status_code = 403
    default_message = "Không có quyền truy cập"


class NotFoundException(AppException):
    status_code = 404
    default_message = "Không tìm thấy dữ liệu"


class ConflictException(AppException):
    status_code = 409
    default_message = "Dữ liệu đã tồn tại"


def custom_exception_handler(exc, context):
    if isinstance(exc, AppException):
        return error_response(message=exc.message, status_code=exc.status_code)

    drf_response = exception_handler(exc, context)
    if drf_response is not None:
        detail = drf_response.data
        msg = "Yêu cầu thất bại"
        if isinstance(detail, dict) and "detail" in detail:
            msg = str(detail["detail"])
        elif isinstance(detail, list) and len(detail) > 0:
            msg = str(detail[0])
        elif detail:
            msg = str(detail)
        return error_response(message=msg, status_code=drf_response.status_code)

    return error_response(message=str(exc) or "Lỗi hệ thống máy chủ", status_code=500)
