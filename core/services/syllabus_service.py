from datetime import datetime
from django.db.models import Prefetch
from core.models import Course, Section, Lesson, Enrollment, LessonProgress
from core.exceptions import NotFoundException, BadRequestException


def serialize_section(section):
    return {
        "ma_chuong": section.ma_chuong,
        "ma_khoa_hoc": section.course_id,
        "ten_chuong": section.ten_chuong,
        "thu_tu": section.thu_tu,
        "created_at": section.created_at.isoformat() if section.created_at else None,
    }


def serialize_lesson(lesson):
    return {
        "ma_bai_hoc": lesson.ma_bai_hoc,
        "ma_chuong": lesson.section_id,
        "ten_bai_hoc": lesson.ten_bai_hoc,
        "loai_bai_hoc": lesson.loai_bai_hoc,
        "url_video": lesson.url_video,
        "noi_dung_text": lesson.noi_dung_text,
        "thoi_luong_giay": lesson.thoi_luong_giay,
        "thu_tu": lesson.thu_tu,
        "is_preview": bool(lesson.is_preview),
        "created_at": lesson.created_at.isoformat() if lesson.created_at else None,
    }


def get_syllabus(ma_khoa_hoc, current_user=None):
    sections_prefetch = Prefetch(
        "sections",
        queryset=Section.objects.order_by("thu_tu", "ma_chuong").prefetch_related(
            Prefetch("lessons", queryset=Lesson.objects.order_by("thu_tu", "ma_bai_hoc"))
        ),
    )
    course = Course.objects.prefetch_related(sections_prefetch).filter(ma_khoa_hoc=ma_khoa_hoc).first()
    if not course:
        raise NotFoundException("Khóa học không tồn tại!")

    is_enrolled = False
    user_progress_map = {}

    if current_user and getattr(current_user, "is_authenticated", False):
        is_premium = bool(current_user.status) is True
        is_admin_or_teacher = current_user.ma_loai_nguoi_dung in ["GV", "GVU"]

        unlocked_list = [
            x.strip() for x in (current_user.unlocked_courses or "").split(",") if x.strip()
        ]
        in_enrollment_table = Enrollment.objects.filter(
            user_id=current_user.tai_khoan,
            course_id=ma_khoa_hoc,
            trang_thai=True,
        ).exists()

        is_enrolled = is_admin_or_teacher or (
            is_premium and (ma_khoa_hoc in unlocked_list or in_enrollment_table)
        )

        progresses = LessonProgress.objects.filter(user_id=current_user.tai_khoan)
        for p in progresses:
            user_progress_map[p.lesson_id] = p

    total_lessons = 0
    completed_lessons = 0
    sections_output = []

    for sec in course.sections.all():
        lessons_output = []
        for les in sec.lessons.all():
            total_lessons += 1
            user_prog = user_progress_map.get(les.ma_bai_hoc)
            da_hoan_thanh = bool(user_prog.da_hoan_thanh) if user_prog else False
            if da_hoan_thanh:
                completed_lessons += 1

            can_view_content = is_enrolled or bool(les.is_preview)
            lessons_output.append({
                "maBaiHoc": les.ma_bai_hoc,
                "tenBaiHoc": les.ten_bai_hoc,
                "loaiBaiHoc": les.loai_bai_hoc,
                "urlVideo": les.url_video if can_view_content else None,
                "noiDungText": les.noi_dung_text if can_view_content else None,
                "thoiLuongGiay": les.thoi_luong_giay,
                "thuTu": les.thu_tu,
                "isPreview": bool(les.is_preview),
                "daHoanThanh": da_hoan_thanh,
                "thoiGianXem": user_prog.thoi_gian_xem if user_prog else 0,
                "actualWatchedSeconds": user_prog.actual_watched_seconds if user_prog else 0,
                "watchedIntervals": (user_prog.watched_intervals or []) if user_prog else [],
            })

        sections_output.append({
            "maChuong": sec.ma_chuong,
            "tenChuong": sec.ten_chuong,
            "thuTu": sec.thu_tu,
            "lessons": lessons_output,
        })

    if total_lessons > 0:
        progress_percent = round((completed_lessons / total_lessons) * 100.0, 1)
    else:
        progress_percent = 0

    return {
        "maKhoaHoc": course.ma_khoa_hoc,
        "tenKhoaHoc": course.ten_khoa_hoc,
        "isEnrolled": is_enrolled,
        "totalLessons": total_lessons,
        "completedLessons": completed_lessons,
        "progressPercent": progress_percent,
        "sections": sections_output,
    }


def create_section(body):
    ma_khoa_hoc = body.get("maKhoaHoc")
    ten_chuong = body.get("tenChuong")
    thu_tu = int(body.get("thuTu") or 1)

    if not ma_khoa_hoc or not ten_chuong:
        raise BadRequestException("Mã khóa học và tên chương là bắt buộc!")

    course = Course.objects.filter(ma_khoa_hoc=ma_khoa_hoc).first()
    if not course:
        raise NotFoundException("Khóa học không tồn tại!")

    section = Section.objects.create(
        course=course,
        ten_chuong=ten_chuong,
        thu_tu=thu_tu,
        created_at=datetime.now(),
    )
    return serialize_section(section)


def update_section(section_id, body):
    section = Section.objects.filter(ma_chuong=int(section_id)).first()
    if not section:
        raise NotFoundException("Chương học không tồn tại!")

    if body.get("tenChuong") is not None:
        section.ten_chuong = body.get("tenChuong")
    if body.get("thuTu") is not None:
        section.thu_tu = int(body.get("thuTu") or 1)
    section.save()
    return serialize_section(section)


def delete_section(section_id):
    if int(section_id) == 283:
        raise BadRequestException("Không thể xóa chương học mẫu mặc định của khóa học!")

    section = Section.objects.filter(ma_chuong=int(section_id)).first()
    if not section:
        raise NotFoundException("Chương học không tồn tại!")

    data = serialize_section(section)
    section.delete()
    return data


def create_lesson(body):
    ma_chuong = body.get("maChuong")
    ten_bai_hoc = body.get("tenBaiHoc")
    if not ma_chuong or not ten_bai_hoc:
        raise BadRequestException("Mã chương và tên bài học là bắt buộc!")

    section = Section.objects.filter(ma_chuong=int(ma_chuong)).first()
    if not section:
        raise NotFoundException("Chương học không tồn tại!")

    lesson = Lesson.objects.create(
        section=section,
        ten_bai_hoc=ten_bai_hoc,
        loai_bai_hoc=body.get("loaiBaiHoc") or "VIDEO",
        url_video=body.get("urlVideo") or None,
        noi_dung_text=body.get("noiDungText") or None,
        thoi_luong_giay=int(body.get("thoiLuongGiay") or 0),
        thu_tu=int(body.get("thuTu") or 1),
        is_preview=bool(body.get("isPreview", False)),
        created_at=datetime.now(),
    )
    return serialize_lesson(lesson)


def update_lesson(lesson_id, body):
    lesson = Lesson.objects.filter(ma_bai_hoc=int(lesson_id)).first()
    if not lesson:
        raise NotFoundException("Bài học không tồn tại!")

    if body.get("tenBaiHoc") is not None:
        lesson.ten_bai_hoc = body.get("tenBaiHoc")
    if body.get("loaiBaiHoc") is not None:
        lesson.loai_bai_hoc = body.get("loaiBaiHoc") or "VIDEO"
    if "urlVideo" in body:
        lesson.url_video = body.get("urlVideo") or None
    if "noiDungText" in body:
        lesson.noi_dung_text = body.get("noiDungText") or None
    if body.get("thoiLuongGiay") is not None:
        lesson.thoi_luong_giay = int(body.get("thoiLuongGiay") or 0)
    if body.get("thuTu") is not None:
        lesson.thu_tu = int(body.get("thuTu") or 1)
    if "isPreview" in body:
        lesson.is_preview = bool(body.get("isPreview"))

    lesson.save()
    return serialize_lesson(lesson)


def delete_lesson(lesson_id):
    if int(lesson_id) in [846, 847, 848]:
        raise BadRequestException("Không thể xóa bài học mẫu mặc định của khóa học!")

    lesson = Lesson.objects.filter(ma_bai_hoc=int(lesson_id)).first()
    if not lesson:
        raise NotFoundException("Bài học không tồn tại!")

    data = serialize_lesson(lesson)
    lesson.delete()
    return data
