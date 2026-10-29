import re
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from django.conf import settings
from django.db.models import Q
from core.models import (
    User,
    Course,
    Enrollment,
    Lesson,
    LessonProgress,
    AssignmentSubmission,
)
from core.exceptions import (
    BadRequestException,
    UnauthorizedException,
    NotFoundException,
    ConflictException,
)
from core.algorithms.search_engine import normalize_vietnamese_text


VALID_PLANS = {
    "ind_monthly": [199000.0, 399000.0],
    "ind_yearly": [1990000.0, 3990000.0],
    "team_monthly": [129000.0, 249000.0],
    "team_yearly": [1290000.0, 2490000.0],
}


def get_role_display_name(role_code):
    if role_code == "GVU":
        return "Giáo vụ"
    if role_code == "GV":
        return "Giảng viên"
    return "Học viên"


def validate_registration_payload(body):
    tai_khoan = str(body.get("taiKhoan") or "").strip()
    mat_khau = str(body.get("matKhau") or "")
    ho_ten = str(body.get("hoTen") or "").strip()
    email = str(body.get("email") or "").strip()
    so_dt = str(body.get("soDT") or body.get("soDt") or "").strip()

    if len(tai_khoan) < 3:
        raise BadRequestException("Tài khoản phải có ít nhất 3 ký tự")
    if len(mat_khau) < 6:
        raise BadRequestException("Mật khẩu phải có ít nhất 6 ký tự")
    if len(ho_ten) < 2:
        raise BadRequestException("Họ tên phải có ít nhất 2 ký tự")
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        raise BadRequestException("Địa chỉ email không hợp lệ")
    if len(so_dt) < 8:
        raise BadRequestException("Số điện thoại không hợp lệ")


def register_user(body):
    validate_registration_payload(body)

    tai_khoan = str(body.get("taiKhoan")).strip()
    mat_khau = str(body.get("matKhau"))
    ho_ten = str(body.get("hoTen")).strip()
    email = str(body.get("email")).strip()
    so_dt = str(body.get("soDT") or body.get("soDt") or "").strip()
    ma_nhom = str(body.get("maNhom") or "GP01").strip()
    trang_thai = body.get("trangThai")
    plan_code = body.get("planCode") or "ind_monthly"
    price = body.get("price") if body.get("price") is not None else 199000.0

    if plan_code not in VALID_PLANS:
        raise BadRequestException("Vui lòng chọn gói học phí hợp lệ trước khi đăng ký!")

    try:
        numeric_price = float(price)
    except (TypeError, ValueError):
        raise BadRequestException("Mức học phí (VNĐ) không khớp với gói đã chọn!")

    acceptable_prices = VALID_PLANS[plan_code]
    if numeric_price not in acceptable_prices:
        raise BadRequestException("Mức học phí (VNĐ) không khớp với gói đã chọn!")

    existing = User.objects.filter(Q(tai_khoan=tai_khoan) | Q(email=email)).first()
    if existing:
        raise ConflictException("Tài khoản hoặc Email đã tồn tại trong hệ thống!")

    hashed_pw = bcrypt.hashpw(mat_khau.encode("utf-8"), bcrypt.gensalt(10)).decode("utf-8")
    now = datetime.now()

    user = User.objects.create(
        tai_khoan=tai_khoan,
        mat_khau=hashed_pw,
        ho_ten=ho_ten,
        email=email,
        so_dt=so_dt,
        ma_nhom=ma_nhom,
        ma_loai_nguoi_dung="HV",
        status=bool(trang_thai) if trang_thai is not None else True,
        unlocked_courses="",
        created_at=now,
        updated_at=now,
    )

    return {
        "taiKhoan": user.tai_khoan,
        "hoTen": user.ho_ten,
        "email": user.email,
        "soDT": user.so_dt,
        "maLoaiNguoiDung": user.ma_loai_nguoi_dung,
        "maNhom": user.ma_nhom,
        "trangThai": bool(user.status),
        "goiDangKy": plan_code,
        "hocPhi": int(numeric_price),
        "donViTienTe": "VND",
    }


def login_user(body):
    tai_khoan = str(body.get("taiKhoan") or "").strip()
    mat_khau = str(body.get("matKhau") or "")

    if not tai_khoan:
        raise BadRequestException("Vui lòng nhập tài khoản")
    if not mat_khau:
        raise BadRequestException("Vui lòng nhập mật khẩu")

    user = User.objects.filter(tai_khoan=tai_khoan).first()
    if not user:
        raise UnauthorizedException("Tài khoản hoặc mật khẩu không chính xác!")

    try:
        is_match = bcrypt.checkpw(mat_khau.encode("utf-8"), user.mat_khau.encode("utf-8"))
    except ValueError:
        is_match = False

    if not is_match:
        raise UnauthorizedException("Tài khoản hoặc mật khẩu không chính xác!")

    secret = getattr(settings, "JWT_SECRET", "elearning_secret_key_2026_super_secure")
    exp_time = datetime.now(timezone.utc) + timedelta(days=7)
    token_payload = {
        "taiKhoan": user.tai_khoan,
        "email": user.email,
        "maLoaiNguoiDung": user.ma_loai_nguoi_dung,
        "exp": exp_time,
    }
    access_token = jwt.encode(token_payload, secret, algorithm="HS256")

    return {
        "taiKhoan": user.tai_khoan,
        "hoTen": user.ho_ten,
        "email": user.email,
        "soDT": user.so_dt,
        "maLoaiNguoiDung": user.ma_loai_nguoi_dung,
        "maNhom": user.ma_nhom,
        "trangThai": bool(user.status),
        "accessToken": access_token,
    }


def get_user_profile(current_user):
    user_profile = User.objects.filter(tai_khoan=current_user.tai_khoan).first()
    if not user_profile:
        raise NotFoundException("Tài khoản không tồn tại")

    course_codes = []
    seen_codes = set()

    unlocked_raw = user_profile.unlocked_courses or ""
    for code in unlocked_raw.split(","):
        cleaned = code.strip()
        if cleaned and cleaned not in seen_codes:
            seen_codes.add(cleaned)
            course_codes.append(cleaned)

    db_enrollments = Enrollment.objects.filter(
        user_id=user_profile.tai_khoan, trang_thai=True
    ).values_list("course_id", flat=True)
    for code in db_enrollments:
        if code and code not in seen_codes:
            seen_codes.add(code)
            course_codes.append(code)

    courses_qs = Course.objects.filter(ma_khoa_hoc__in=course_codes)
    course_map = {c.ma_khoa_hoc: c for c in courses_qs}
    ordered_courses = [course_map[code] for code in course_codes if code in course_map]

    all_lessons = Lesson.objects.filter(section__course_id__in=course_codes).select_related("section")
    lessons_by_course = defaultdict(list)
    lesson_to_course = {}
    all_lesson_ids = []

    for les in all_lessons:
        cid = les.section.course_id
        lessons_by_course[cid].append(les.ma_bai_hoc)
        lesson_to_course[les.ma_bai_hoc] = cid
        all_lesson_ids.append(les.ma_bai_hoc)

    completed_by_course = defaultdict(int)
    if all_lesson_ids:
        completed_qs = LessonProgress.objects.filter(
            user_id=user_profile.tai_khoan,
            lesson_id__in=all_lesson_ids,
            da_hoan_thanh=True,
        ).values_list("lesson_id", flat=True)
        for lid in completed_qs:
            cid = lesson_to_course.get(lid)
            if cid:
                completed_by_course[cid] += 1

    scores_by_course = defaultdict(list)
    if all_lesson_ids:
        graded_subs = AssignmentSubmission.objects.filter(
            user_id=user_profile.tai_khoan,
            assignment__lesson_id__in=all_lesson_ids,
            trang_thai="DA_CHAM",
            diem_so__isnull=False,
        ).select_related("assignment")
        for sub in graded_subs:
            lid = sub.assignment.lesson_id
            cid = lesson_to_course.get(lid)
            if cid:
                scores_by_course[cid].append(float(sub.diem_so))

    chi_tiet_khoa_hoc = []
    for c in ordered_courses:
        cid = c.ma_khoa_hoc
        total_lessons = len(lessons_by_course.get(cid, []))
        completed_lessons = completed_by_course.get(cid, 0)
        if total_lessons > 0:
            progress_percent = round((completed_lessons / total_lessons) * 100.0, 1)
        else:
            progress_percent = 0

        course_scores = scores_by_course.get(cid, [])
        if course_scores:
            gpa = round(sum(course_scores) / len(course_scores), 1)
        else:
            gpa = None

        chi_tiet_khoa_hoc.append({
            "maKhoaHoc": c.ma_khoa_hoc,
            "tenKhoaHoc": c.ten_khoa_hoc,
            "biAnh": c.bi_anh or "",
            "moTa": c.mo_ta or "",
            "hinhAnh": c.hinh_anh or "",
            "danhGia": c.danh_gia,
            "progressPercent": progress_percent,
            "completedLessons": completed_lessons,
            "totalLessons": total_lessons,
            "gpa": gpa,
        })

    return {
        "taiKhoan": user_profile.tai_khoan,
        "matKhau": "******",
        "hoTen": user_profile.ho_ten,
        "email": user_profile.email,
        "soDT": user_profile.so_dt,
        "maLoaiNguoiDung": user_profile.ma_loai_nguoi_dung,
        "maNhom": user_profile.ma_nhom,
        "trangThai": bool(user_profile.status),
        "chiTietKhoaHocGhiDanh": chi_tiet_khoa_hoc,
    }


def update_user_profile(current_user, body):
    target_account = body.get("taiKhoan") or current_user.tai_khoan
    target_user = User.objects.filter(tai_khoan=target_account).first()
    if not target_user:
        raise NotFoundException("Tài khoản người dùng không tồn tại!")

    ho_ten = body.get("hoTen")
    email = body.get("email")
    so_dt = body.get("soDT") if "soDT" in body else body.get("soDt")
    mat_khau = body.get("matKhau")
    ma_loai = body.get("maLoaiNguoiDung")
    ma_nhom = body.get("maNhom")
    trang_thai = body.get("trangThai")

    if ho_ten:
        target_user.ho_ten = ho_ten
    if email:
        target_user.email = email
    if so_dt is not None:
        target_user.so_dt = so_dt
    if ma_nhom:
        target_user.ma_nhom = ma_nhom
    if ma_loai:
        target_user.ma_loai_nguoi_dung = ma_loai
    if trang_thai is not None:
        target_user.status = bool(trang_thai)
    if "bio" in body:
        target_user.bio = body.get("bio")
    if "avatar" in body:
        target_user.avatar = body.get("avatar")

    if mat_khau and str(mat_khau).strip() != "" and str(mat_khau) != "******":
        target_user.mat_khau = bcrypt.hashpw(
            str(mat_khau).encode("utf-8"), bcrypt.gensalt(10)
        ).decode("utf-8")

    target_user.updated_at = datetime.now()
    target_user.save()

    return {
        "taiKhoan": target_user.tai_khoan,
        "hoTen": target_user.ho_ten,
        "email": target_user.email,
        "soDT": target_user.so_dt,
        "maLoaiNguoiDung": target_user.ma_loai_nguoi_dung,
        "maNhom": target_user.ma_nhom,
        "trangThai": bool(target_user.status),
    }


def get_users_list():
    users = User.objects.all().order_by("-created_at")
    result = []
    for u in users:
        result.append({
            "taiKhoan": u.tai_khoan,
            "hoTen": u.ho_ten,
            "email": u.email,
            "soDt": u.so_dt,
            "maLoaiNguoiDung": u.ma_loai_nguoi_dung,
            "tenLoaiNguoiDung": get_role_display_name(u.ma_loai_nguoi_dung),
            "trangThai": bool(u.status),
        })
    return result


def search_users(tu_khoa):
    users = User.objects.all()
    keyword = str(tu_khoa or "").strip()
    if not keyword:
        matched_users = list(users)
    else:
        norm_kw = normalize_vietnamese_text(keyword)
        raw_kw_lower = keyword.lower()
        matched_users = []
        for u in users:
            acc_norm = normalize_vietnamese_text(u.tai_khoan)
            name_norm = normalize_vietnamese_text(u.ho_ten)
            if (
                raw_kw_lower in u.tai_khoan.lower()
                or raw_kw_lower in u.ho_ten.lower()
                or (norm_kw and (norm_kw in acc_norm or norm_kw in name_norm))
            ):
                matched_users.append(u)

    result = []
    for u in matched_users:
        result.append({
            "taiKhoan": u.tai_khoan,
            "hoTen": u.ho_ten,
            "email": u.email,
            "soDt": u.so_dt,
            "maLoaiNguoiDung": u.ma_loai_nguoi_dung,
            "trangThai": bool(u.status),
        })
    return result


def add_user(body):
    tai_khoan = str(body.get("taiKhoan") or "").strip()
    mat_khau = str(body.get("matKhau") or "")
    ho_ten = str(body.get("hoTen") or "").strip()
    email = str(body.get("email") or "").strip()
    so_dt = str(body.get("soDT") or body.get("soDt") or "").strip()
    ma_nhom = str(body.get("maNhom") or "GP01").strip()
    ma_loai = str(body.get("maLoaiNguoiDung") or "HV").strip()
    trang_thai = body.get("trangThai")

    if not tai_khoan or not mat_khau or not ho_ten or not email:
        raise BadRequestException("Tài khoản, mật khẩu, họ tên và email là bắt buộc!")

    existing = User.objects.filter(Q(tai_khoan=tai_khoan) | Q(email=email)).first()
    if existing:
        raise ConflictException("Tài khoản hoặc Email đã tồn tại trong hệ thống!")

    hashed_pw = bcrypt.hashpw(mat_khau.encode("utf-8"), bcrypt.gensalt(10)).decode("utf-8")
    now = datetime.now()

    user = User.objects.create(
        tai_khoan=tai_khoan,
        mat_khau=hashed_pw,
        ho_ten=ho_ten,
        email=email,
        so_dt=so_dt,
        ma_nhom=ma_nhom,
        ma_loai_nguoi_dung=ma_loai,
        status=bool(trang_thai) if trang_thai is not None else True,
        unlocked_courses="",
        created_at=now,
        updated_at=now,
    )

    return {
        "taiKhoan": user.tai_khoan,
        "hoTen": user.ho_ten,
        "email": user.email,
        "soDT": user.so_dt,
        "maLoaiNguoiDung": user.ma_loai_nguoi_dung,
        "maNhom": user.ma_nhom,
        "trangThai": bool(user.status),
    }


def delete_user(tai_khoan):
    if not tai_khoan:
        raise NotFoundException("Tài khoản người dùng không tồn tại!")

    if str(tai_khoan).strip().lower() in ["admin01", "admin"]:
        raise BadRequestException("Không thể xóa tài khoản Quản trị viên mặc định của hệ thống!")

    user = User.objects.filter(tai_khoan=tai_khoan).first()
    if not user:
        raise NotFoundException("Tài khoản người dùng không tồn tại!")

    user.delete()
    return "Xóa người dùng thành công!"


def get_courses_pending(tai_khoan=None):
    return []


def get_students_in_course(ma_khoa_hoc):
    if not ma_khoa_hoc:
        return []

    enrollments = Enrollment.objects.filter(
        course_id=ma_khoa_hoc, trang_thai=True
    ).select_related("user")

    students = []
    seen = set()
    for enr in enrollments:
        u = enr.user
        if u and u.tai_khoan not in seen:
            seen.add(u.tai_khoan)
            students.append({
                "taiKhoan": u.tai_khoan,
                "hoTen": u.ho_ten,
                "email": u.email,
                "soDt": u.so_dt,
                "maLoaiNguoiDung": u.ma_loai_nguoi_dung,
                "trangThai": bool(u.status),
            })
    return students
