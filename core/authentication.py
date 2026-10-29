import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from core.models import User
from core.exceptions import UnauthorizedException, ForbiddenException


def extract_token_from_request(request):
    auth_header = request.headers.get("Authorization") or request.META.get("HTTP_AUTHORIZATION")
    if auth_header and auth_header.startswith("Bearer "):
        parts = auth_header.split(" ", 1)
        if len(parts) == 2 and parts[1].strip():
            return parts[1].strip()

    access_token = request.headers.get("accesstoken") or request.META.get("HTTP_ACCESSTOKEN")
    if access_token and access_token.strip():
        return access_token.strip()

    return None


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = extract_token_from_request(request)
        if not token:
            raise UnauthorizedException("Vui lòng đăng nhập để tiếp tục")

        secret = getattr(settings, "JWT_SECRET", "elearning_secret_key_2026_super_secure")
        try:
            decoded = jwt.decode(token, secret, algorithms=["HS256"])
        except jwt.PyJWTError:
            raise UnauthorizedException("Phiên đăng nhập đã hết hạn hoặc không hợp lệ")

        tai_khoan = decoded.get("taiKhoan") or decoded.get("tai_khoan")
        if not tai_khoan:
            raise UnauthorizedException("Phiên đăng nhập đã hết hạn hoặc không hợp lệ")

        user = User.objects.filter(tai_khoan=tai_khoan).first()
        if not user:
            raise UnauthorizedException("Tài khoản không tồn tại trong hệ thống")

        if user.status is not True:
            raise ForbiddenException("Tài khoản của bạn chưa được kích hoạt hoặc đã bị khóa")

        return (user, token)


class OptionalJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = extract_token_from_request(request)
        if not token:
            return None

        secret = getattr(settings, "JWT_SECRET", "elearning_secret_key_2026_super_secure")
        try:
            decoded = jwt.decode(token, secret, algorithms=["HS256"])
        except jwt.PyJWTError:
            return None

        tai_khoan = decoded.get("taiKhoan") or decoded.get("tai_khoan")
        if not tai_khoan:
            return None

        user = User.objects.filter(tai_khoan=tai_khoan).first()
        if user and user.status is True:
            return (user, token)

        return None
