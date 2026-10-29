import os
import time
import random
from datetime import datetime
from django.conf import settings
from core.models import Course, Category, User, Enrollment
from core.exceptions import NotFoundException, ConflictException, BadRequestException
from core.algorithms.search_engine import search_engine_instance
from core.algorithms.course_recommender import course_recommender_instance


COURSE_LEVEL_PRICES_VND = {
    "CoBan": 499000,
    "TrungCap": 799000,
    "NangCao": 1199000,
}


def format_course_output(course):
    if course.ngay_tao:
        if hasattr(course.ngay_tao, "strftime"):
            ngay_tao_str = course.ngay_tao.strftime("%Y-%m-%d")
        else:
            ngay_tao_str = str(course.ngay_tao)[:10]
    else:
        ngay_tao_str = ""

    creator = getattr(course, "creator", None)
    category = getattr(course, "category", None)

    danh_gia_val = course.danh_gia if course.danh_gia is not None else 5
    if isinstance(danh_gia_val, float) and danh_gia_val.is_integer():
        danh_gia_val = int(danh_gia_val)

    cap_do_val = course.cap_do or "CoBan"
    hoc_phi_vnd = COURSE_LEVEL_PRICES_VND.get(cap_do_val, 499000)

    return {
        "maKhoaHoc": course.ma_khoa_hoc,
        "tenKhoaHoc": course.ten_khoa_hoc,
        "biAnh": course.bi_anh or "",
        "moTa": course.mo_ta or "",
        "luotXem": course.luot_xem or 0,
        "danhGia": danh_gia_val,
        "hinhAnh": course.hinh_anh or "",
        "maNhom": course.ma_nhom or "GP01",
        "ngayTao": ngay_tao_str,
        "soLuongHocVien": course.luot_xem if course.luot_xem else 1248,
        "thoiLuongGio": course.thoi_luong_gio or 0,
        "capDo": cap_do_val,
        "hocPhi": hoc_phi_vnd,
        "donViTienTe": "VND",
        "nguoiTao": {
            "taiKhoan": creator.tai_khoan if creator else "admin01",
            "hoTen": creator.ho_ten if creator else "Quản trị viên",
            "maLoaiNguoiDung": creator.ma_loai_nguoi_dung if creator else "GV",
            "tenLoaiNguoiDung": "Giảng viên",
        },
        "danhMucKhoaHoc": {
            "maDanhMucKhoahoc": category.ma_danh_muc if category else "FRONT_END",
            "tenDanhMucKhoaHoc": category.ten_danh_muc if category else "Lập trình Giao diện Web Front-End",
        },
    }


def get_categories():
    categories = Category.objects.all()
    return [
        {
            "maDanhMuc": c.ma_danh_muc,
            "tenDanhMuc": c.ten_danh_muc,
        }
        for c in categories
    ]


def get_courses_by_category(ma_danh_muc):
    courses = Course.objects.select_related("category", "creator").filter(category_id=ma_danh_muc)
    return [format_course_output(c) for c in courses]


def get_course_list(ten_khoa_hoc=None, ma_nhom=None, current_user=None):
    qs = Course.objects.select_related("category", "creator").all()
    if ma_nhom:
        qs = qs.filter(ma_nhom=ma_nhom)

    keyword = str(ten_khoa_hoc or "").strip()
    if keyword:
        matched_ids = search_engine_instance.search(keyword)
        if not matched_ids:
            return []
        course_map = {c.ma_khoa_hoc: c for c in qs.filter(ma_khoa_hoc__in=matched_ids)}
        ordered = [course_map[cid] for cid in matched_ids if cid in course_map]
        return [format_course_output(c) for c in ordered]

    if current_user and getattr(current_user, "is_authenticated", False):
        ranked_courses = course_recommender_instance.rank_courses_for_user(qs, current_user)
        return [format_course_output(c) for c in ranked_courses]

    ordered_guest = qs.order_by("-ngay_tao")
    return [format_course_output(c) for c in ordered_guest]


def get_course_detail(ma_khoa_hoc):
    if not ma_khoa_hoc:
        raise NotFoundException("Không tìm thấy khóa học yêu cầu!")

    course = Course.objects.select_related("category", "creator").filter(ma_khoa_hoc=ma_khoa_hoc).first()
    if not course:
        raise NotFoundException("Không tìm thấy khóa học yêu cầu!")

    return format_course_output(course)


def add_course(body, creator_user=None):
    ma_khoa_hoc = str(body.get("maKhoaHoc") or "").strip()
    ten_khoa_hoc = str(body.get("tenKhoaHoc") or "").strip()
    if not ma_khoa_hoc or not ten_khoa_hoc:
        raise BadRequestException("Mã khóa học và tên khóa học là bắt buộc!")

    if Course.objects.filter(ma_khoa_hoc=ma_khoa_hoc).exists():
        raise ConflictException("Mã khóa học đã tồn tại!")

    category_id = (
        body.get("maDanhMucKhoahoc")
        or body.get("maDanhMucKhoaHoc")
        or body.get("maDanhMuc")
        or "FRONT_END"
    )
    creator_id = body.get("taiKhoanNguoiTao") or (creator_user.tai_khoan if creator_user else "admin01")

    instructor = User.objects.filter(tai_khoan=creator_id).first()
    if not instructor:
        raise NotFoundException(f"Tài khoản người tạo '{creator_id}' không tồn tại!")

    if instructor.ma_loai_nguoi_dung not in ["GV", "GVU"]:
        raise BadRequestException("Người tạo khóa học phải là Giảng viên (GV) hoặc Giáo vụ (GVU)!")

    category_obj = Category.objects.filter(ma_danh_muc=category_id).first()
    if not category_obj:
        category_obj = Category.objects.first()

    now = datetime.now()
    new_course = Course.objects.create(
        ma_khoa_hoc=ma_khoa_hoc,
        ten_khoa_hoc=ten_khoa_hoc,
        bi_anh=body.get("biAnh") or ma_khoa_hoc,
        mo_ta=body.get("moTa") or "",
        luot_xem=int(body.get("luotXem") or 0),
        danh_gia=float(body.get("danhGia") if body.get("danhGia") is not None else 5.0),
        hinh_anh=body.get("hinhAnh") or "",
        ma_nhom=body.get("maNhom") or "GP01",
        ngay_tao=now,
        cap_do=body.get("capDo") or "CoBan",
        thoi_luong_gio=int(body.get("thoiLuongGio") or 0),
        trang_thai=True,
        category=category_obj,
        creator=instructor,
    )

    return format_course_output(new_course)


def update_course(body):
    ma_khoa_hoc = str(body.get("maKhoaHoc") or "").strip()
    existing = Course.objects.select_related("category", "creator").filter(ma_khoa_hoc=ma_khoa_hoc).first()
    if not existing:
        raise NotFoundException("Khóa học không tồn tại!")

    tai_khoan_tao = body.get("taiKhoanNguoiTao")
    if tai_khoan_tao:
        instructor = User.objects.filter(tai_khoan=tai_khoan_tao).first()
        if not instructor:
            raise NotFoundException(f"Tài khoản giảng viên '{tai_khoan_tao}' không tồn tại!")
        if instructor.ma_loai_nguoi_dung not in ["GV", "GVU"]:
            raise BadRequestException("Người tạo khóa học phải là Giảng viên (GV) hoặc Giáo vụ (GVU)!")
        existing.creator = instructor

    if body.get("tenKhoaHoc"):
        existing.ten_khoa_hoc = body.get("tenKhoaHoc")
    if body.get("biAnh"):
        existing.bi_anh = body.get("biAnh")
    if "moTa" in body and body.get("moTa") is not None:
        existing.mo_ta = body.get("moTa")
    if "luotXem" in body and body.get("luotXem") is not None:
        existing.luot_xem = int(body.get("luotXem"))
    if "danhGia" in body and body.get("danhGia") is not None:
        existing.danh_gia = float(body.get("danhGia"))
    if body.get("hinhAnh"):
        existing.hinh_anh = body.get("hinhAnh")
    if body.get("maNhom"):
        existing.ma_nhom = body.get("maNhom")
    if body.get("capDo"):
        existing.cap_do = body.get("capDo")
    if "thoiLuongGio" in body and body.get("thoiLuongGio") is not None:
        existing.thoi_luong_gio = int(body.get("thoiLuongGio"))

    cat_code = body.get("maDanhMucKhoahoc") or body.get("maDanhMucKhoaHoc") or body.get("maDanhMuc")
    if cat_code:
        cat_obj = Category.objects.filter(ma_danh_muc=cat_code).first()
        if cat_obj:
            existing.category = cat_obj

    existing.save()

    return format_course_output(existing)


def upload_course_image(uploaded_file, ma_khoa_hoc=None):
    if not uploaded_file:
        image_path = "http://localhost:5000/uploads/course-default-thumbnail.png"
        if ma_khoa_hoc:
            Course.objects.filter(ma_khoa_hoc=ma_khoa_hoc).update(hinh_anh=image_path)
        return {
            "hinhAnh": image_path,
            "message": "Sử dụng hình ảnh khóa học mặc định thành công",
        }

    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    _, ext = os.path.splitext(uploaded_file.name)
    if not ext:
        ext = ".png"
    unique_name = f"{int(time.time() * 1000)}-{random.randint(100000000, 999999999)}{ext}"
    file_path = os.path.join(settings.MEDIA_ROOT, unique_name)

    with open(file_path, "wb+") as dest:
        for chunk in uploaded_file.chunks():
            dest.write(chunk)

    image_path = f"http://localhost:5000/uploads/{unique_name}"

    if ma_khoa_hoc:
        Course.objects.filter(ma_khoa_hoc=ma_khoa_hoc).update(hinh_anh=image_path)

    return {
        "hinhAnh": image_path,
        "message": "Tải lên hình ảnh thành công",
    }


def delete_course(ma_khoa_hoc):
    if not ma_khoa_hoc:
        raise NotFoundException("Khóa học không tồn tại!")

    existing = Course.objects.filter(ma_khoa_hoc=ma_khoa_hoc).first()
    if not existing:
        raise NotFoundException("Khóa học không tồn tại!")

    existing.delete()

    return "Xóa khóa học thành công!"


def register_course(ma_khoa_hoc, tai_khoan):
    user = User.objects.filter(tai_khoan=tai_khoan).first()
    if not user:
        raise NotFoundException("Tài khoản người dùng không tồn tại!")

    course = Course.objects.filter(ma_khoa_hoc=ma_khoa_hoc).first()
    if not course:
        raise NotFoundException("Khóa học không tồn tại!")

    Enrollment.objects.update_or_create(
        user=user,
        course=course,
        defaults={
            "trang_thai": True,
            "ngay_ghi_danh": datetime.now(),
        },
    )

    unlocked_list = [x.strip() for x in (user.unlocked_courses or "").split(",") if x.strip()]
    if ma_khoa_hoc not in unlocked_list:
        unlocked_list.append(ma_khoa_hoc)
        user.unlocked_courses = ",".join(unlocked_list)
        user.updated_at = datetime.now()
        user.save()

    return "Đăng ký khóa học thành công!"


def unenroll_course(ma_khoa_hoc, tai_khoan):
    user = User.objects.filter(tai_khoan=tai_khoan).first()
    if not user:
        raise NotFoundException("Tài khoản người dùng không tồn tại!")

    Enrollment.objects.filter(user_id=tai_khoan, course_id=ma_khoa_hoc).delete()

    unlocked_list = [x.strip() for x in (user.unlocked_courses or "").split(",") if x.strip()]
    if ma_khoa_hoc in unlocked_list:
        unlocked_list = [x for x in unlocked_list if x != ma_khoa_hoc]
        user.unlocked_courses = ",".join(unlocked_list)
        user.updated_at = datetime.now()
        user.save()

    return "Hủy ghi danh khóa học thành công!"
