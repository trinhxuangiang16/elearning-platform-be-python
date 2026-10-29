from rest_framework.permissions import BasePermission
from core.exceptions import UnauthorizedException, ForbiddenException


class IsAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not getattr(request.user, "is_authenticated", False):
            raise UnauthorizedException("Vui lòng đăng nhập để tiếp tục")
        return True


class IsInstructorOrAdmin(BasePermission):
    allowed_roles = ["GV", "GVU"]

    def has_permission(self, request, view):
        if not request.user or not getattr(request.user, "is_authenticated", False):
            raise UnauthorizedException("Vui lòng đăng nhập")
        user_role = getattr(request.user, "ma_loai_nguoi_dung", None)
        if user_role not in self.allowed_roles:
            raise ForbiddenException("Bạn không có quyền thực hiện thao tác này")
        return True
