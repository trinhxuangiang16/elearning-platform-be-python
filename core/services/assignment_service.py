from datetime import datetime
from core.models import Lesson, Assignment, AssignmentSubmission
from core.exceptions import NotFoundException, BadRequestException


def parse_optional_datetime(val):
    if not val:
        return None
    if isinstance(val, datetime):
        return val
    val_str = str(val).strip()
    if not val_str:
        return None
    if val_str.endswith("Z"):
        val_str = val_str[:-1]
    try:
        return datetime.fromisoformat(val_str)
    except ValueError:
        return None


def serialize_assignment(assignment):
    return {
        "ma_bai_tap": assignment.ma_bai_tap,
        "ma_bai_hoc": assignment.lesson_id,
        "tieu_de": assignment.tieu_de,
        "de_bai_mo_ta": assignment.de_bai_mo_ta,
        "han_nop": assignment.han_nop.isoformat() if assignment.han_nop else None,
        "created_at": assignment.created_at.isoformat() if assignment.created_at else None,
    }


def serialize_submission(submission):
    return {
        "ma_luot_nop": submission.ma_luot_nop,
        "ma_bai_tap": submission.assignment_id,
        "tai_khoan": submission.user_id,
        "link_nop_bai": submission.link_nop_bai,
        "ghi_chu_student": submission.ghi_chu_student,
        "diem_so": submission.diem_so,
        "nhan_xet_gv": submission.nhan_xet_gv,
        "trang_thai": submission.trang_thai,
        "ngay_nop": submission.ngay_nop.isoformat() if submission.ngay_nop else None,
        "updated_at": submission.updated_at.isoformat() if submission.updated_at else None,
    }


def get_lesson_assignment(ma_bai_hoc, current_user=None):
    assignment = Assignment.objects.filter(lesson_id=int(ma_bai_hoc)).first()
    if not assignment:
        return None

    my_submission = None
    if current_user and getattr(current_user, "is_authenticated", False):
        sub = AssignmentSubmission.objects.filter(
            assignment_id=assignment.ma_bai_tap,
            user_id=current_user.tai_khoan,
        ).first()
        if sub:
            my_submission = {
                "maLuotNop": sub.ma_luot_nop,
                "linkNopBai": sub.link_nop_bai,
                "ghiChuStudent": sub.ghi_chu_student,
                "diemSo": sub.diem_so,
                "nhanXetGv": sub.nhan_xet_gv,
                "trangThai": sub.trang_thai,
                "ngayNop": sub.ngay_nop.isoformat() if sub.ngay_nop else None,
            }

    return {
        "maBaiTap": assignment.ma_bai_tap,
        "tieuDe": assignment.tieu_de,
        "deBaiMoTa": assignment.de_bai_mo_ta,
        "hanNop": assignment.han_nop.isoformat() if assignment.han_nop else None,
        "mySubmission": my_submission,
    }


def submit_assignment(tai_khoan, ma_bai_tap, body):
    link_nop_bai = str(body.get("linkNopBai") or body.get("link_nop_bai") or "").strip()
    ghi_chu_student = body.get("ghiChuStudent") or body.get("ghi_chu_student")

    if not link_nop_bai or not (
        link_nop_bai.startswith("http://") or link_nop_bai.startswith("https://")
    ):
        raise BadRequestException("Vui lòng nhập đường dẫn bài nộp hợp lệ (http:// hoặc https://)")

    assignment = Assignment.objects.filter(ma_bai_tap=int(ma_bai_tap)).first()
    if not assignment:
        raise NotFoundException("Bài tập không tồn tại!")

    now_dt = datetime.now()
    existing = AssignmentSubmission.objects.filter(
        assignment_id=assignment.ma_bai_tap,
        user_id=tai_khoan,
    ).first()

    if existing:
        existing.link_nop_bai = link_nop_bai
        existing.ghi_chu_student = ghi_chu_student or None
        existing.trang_thai = "CHUA_CHAM"
        existing.diem_so = None
        existing.nhan_xet_gv = None
        existing.ngay_nop = now_dt
        existing.updated_at = now_dt
        existing.save()
        record = existing
    else:
        record = AssignmentSubmission.objects.create(
            assignment=assignment,
            user_id=tai_khoan,
            link_nop_bai=link_nop_bai,
            ghi_chu_student=ghi_chu_student or None,
            trang_thai="CHUA_CHAM",
            ngay_nop=now_dt,
            updated_at=now_dt,
        )

    return serialize_submission(record)


def get_submissions_by_assignment(ma_bai_tap):
    submissions = (
        AssignmentSubmission.objects.filter(assignment_id=int(ma_bai_tap))
        .select_related("user")
        .order_by("-ngay_nop")
    )
    result = []
    for s in submissions:
        result.append({
            "maLuotNop": s.ma_luot_nop,
            "taiKhoan": s.user.tai_khoan if s.user else s.user_id,
            "hoTen": s.user.ho_ten if s.user else s.user_id,
            "email": s.user.email if s.user else "",
            "linkNopBai": s.link_nop_bai,
            "ghiChuStudent": s.ghi_chu_student,
            "diemSo": s.diem_so,
            "nhanXetGv": s.nhan_xet_gv,
            "trangThai": s.trang_thai,
            "ngayNop": s.ngay_nop.isoformat() if s.ngay_nop else None,
        })
    return result


def grade_submission(ma_luot_nop, body):
    raw_score = body.get("diemSo") if body.get("diemSo") is not None else body.get("diem_so")
    nhan_xet_gv = body.get("nhanXetGv") if "nhanXetGv" in body else body.get("nhan_xet_gv")

    if raw_score is None:
        raise BadRequestException("Điểm số phải nằm trong khoảng từ 0 đến 100")

    try:
        score = float(raw_score)
    except (TypeError, ValueError):
        raise BadRequestException("Điểm số phải nằm trong khoảng từ 0 đến 100")

    if score < 0.0 or score > 100.0:
        raise BadRequestException("Điểm số phải nằm trong khoảng từ 0 đến 100")

    existing = AssignmentSubmission.objects.filter(ma_luot_nop=int(ma_luot_nop)).first()
    if not existing:
        raise NotFoundException("Bài nộp không tồn tại!")

    existing.diem_so = score
    existing.nhan_xet_gv = nhan_xet_gv or None
    existing.trang_thai = "DA_CHAM"
    existing.updated_at = datetime.now()
    existing.save()

    return serialize_submission(existing)


def get_my_grades(tai_khoan):
    submissions = (
        AssignmentSubmission.objects.filter(user_id=tai_khoan)
        .select_related("assignment")
        .order_by("-ngay_nop")
    )

    graded_scores = [
        float(s.diem_so)
        for s in submissions
        if s.trang_thai == "DA_CHAM" and s.diem_so is not None
    ]

    if graded_scores:
        gpa = round(sum(graded_scores) / len(graded_scores), 1)
    else:
        gpa = None

    sub_list = []
    for s in submissions:
        sub_list.append({
            "maLuotNop": s.ma_luot_nop,
            "maBaiTap": s.assignment_id,
            "assignmentTitle": s.assignment.tieu_de if s.assignment else "",
            "linkNopBai": s.link_nop_bai,
            "diemSo": s.diem_so,
            "nhanXetGv": s.nhan_xet_gv,
            "trangThai": s.trang_thai,
            "ngayNop": s.ngay_nop.isoformat() if s.ngay_nop else None,
        })

    return {
        "gpa": gpa,
        "submissions": sub_list,
    }


def create_assignment(ma_bai_hoc, body):
    lesson = Lesson.objects.filter(ma_bai_hoc=int(ma_bai_hoc)).first()
    if not lesson:
        raise NotFoundException("Bài học không tồn tại!")

    tieu_de = body.get("tieuDe")
    de_bai_mo_ta = body.get("deBaiMoTa")
    han_nop = parse_optional_datetime(body.get("hanNop"))

    if not tieu_de or not de_bai_mo_ta:
        raise BadRequestException("Tiêu đề và nội dung đề bài là bắt buộc!")

    assignment = Assignment.objects.create(
        lesson=lesson,
        tieu_de=tieu_de,
        de_bai_mo_ta=de_bai_mo_ta,
        han_nop=han_nop,
        created_at=datetime.now(),
    )
    return serialize_assignment(assignment)


def update_assignment(ma_bai_tap, body):
    existing = Assignment.objects.filter(ma_bai_tap=int(ma_bai_tap)).first()
    if not existing:
        raise NotFoundException("Bài tập không tồn tại!")

    if body.get("tieuDe") is not None:
        existing.tieu_de = body.get("tieuDe")
    if body.get("deBaiMoTa") is not None:
        existing.de_bai_mo_ta = body.get("deBaiMoTa")
    if "hanNop" in body:
        existing.han_nop = parse_optional_datetime(body.get("hanNop"))

    existing.save()
    return serialize_assignment(existing)


def delete_assignment(ma_bai_tap):
    if int(ma_bai_tap) == 259:
        raise BadRequestException("Không thể xóa bài tập mẫu mặc định của bài học 846!")

    existing = Assignment.objects.filter(ma_bai_tap=int(ma_bai_tap)).first()
    if not existing:
        raise NotFoundException("Bài tập không tồn tại!")

    existing.delete()
    return {"success": True}
