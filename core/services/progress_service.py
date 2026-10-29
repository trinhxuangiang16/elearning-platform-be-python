from datetime import datetime
from core.models import Course, Lesson, LessonProgress
from core.exceptions import NotFoundException
from core.algorithms.progress_intervals import process_video_progress_ping


def update_lesson_progress(tai_khoan, ma_bai_hoc, body, strict_anticheat=False):
    lesson = Lesson.objects.filter(ma_bai_hoc=int(ma_bai_hoc)).first()
    if not lesson:
        raise NotFoundException("Bài học không tồn tại!")

    now_dt = datetime.now()
    existing = LessonProgress.objects.filter(user_id=tai_khoan, lesson_id=lesson.ma_bai_hoc).first()

    existing_intervals = existing.watched_intervals if existing else []
    previous_position = existing.thoi_gian_xem if existing else 0
    existing_completed = existing.da_hoan_thanh if existing else False
    last_ping_at = existing.last_ping_at if existing else None

    computed = process_video_progress_ping(
        existing_intervals=existing_intervals,
        previous_position=previous_position,
        existing_completed=existing_completed,
        last_ping_at=last_ping_at,
        now_dt=now_dt,
        lesson_duration=lesson.thoi_luong_giay,
        payload=body,
        strict_anticheat=strict_anticheat,
    )

    if existing:
        existing.thoi_gian_xem = computed["thoi_gian_xem"]
        existing.da_hoan_thanh = computed["da_hoan_thanh"]
        existing.watched_intervals = computed["watched_intervals"]
        existing.actual_watched_seconds = computed["actual_watched_seconds"]
        existing.last_ping_at = computed["last_ping_at"]
        existing.updated_at = now_dt
        existing.save()
        record = existing
    else:
        record = LessonProgress.objects.create(
            user_id=tai_khoan,
            lesson=lesson,
            thoi_gian_xem=computed["thoi_gian_xem"],
            da_hoan_thanh=computed["da_hoan_thanh"],
            watched_intervals=computed["watched_intervals"],
            actual_watched_seconds=computed["actual_watched_seconds"],
            last_ping_at=computed["last_ping_at"],
            updated_at=now_dt,
        )

    return {
        "id": record.id,
        "tai_khoan": record.user_id,
        "ma_bai_hoc": record.lesson_id,
        "da_hoan_thanh": bool(record.da_hoan_thanh),
        "thoi_gian_xem": record.thoi_gian_xem,
        "watched_intervals": record.watched_intervals or [],
        "actual_watched_seconds": record.actual_watched_seconds,
        "updated_at": record.updated_at.isoformat() if record.updated_at else None,
    }


def get_course_progress(tai_khoan, ma_khoa_hoc):
    course = Course.objects.filter(ma_khoa_hoc=ma_khoa_hoc).first()
    if not course:
        raise NotFoundException("Khóa học không tồn tại!")

    lesson_ids = list(
        Lesson.objects.filter(section__course_id=ma_khoa_hoc).values_list("ma_bai_hoc", flat=True)
    )
    total_lessons = len(lesson_ids)
    if total_lessons == 0:
        return {
            "maKhoaHoc": ma_khoa_hoc,
            "progressPercent": 0,
            "completedLessons": 0,
            "totalLessons": 0,
        }

    completed_lessons = LessonProgress.objects.filter(
        user_id=tai_khoan,
        lesson_id__in=lesson_ids,
        da_hoan_thanh=True,
    ).count()

    progress_percent = round((completed_lessons / total_lessons) * 100.0, 1)
    return {
        "maKhoaHoc": ma_khoa_hoc,
        "progressPercent": progress_percent,
        "completedLessons": completed_lessons,
        "totalLessons": total_lessons,
    }


def get_resume_learning(tai_khoan):
    last_progress = (
        LessonProgress.objects.filter(user_id=tai_khoan)
        .select_related("lesson__section__course")
        .order_by("-updated_at", "-id")
        .first()
    )

    if not last_progress or not last_progress.lesson or not last_progress.lesson.section:
        return None

    course = getattr(last_progress.lesson.section, "course", None)
    if not course:
        return None
    return {
        "maKhoaHoc": course.ma_khoa_hoc,
        "tenKhoaHoc": course.ten_khoa_hoc,
        "maBaiHoc": last_progress.lesson.ma_bai_hoc,
        "tenBaiHoc": last_progress.lesson.ten_bai_hoc,
        "thoiGianXem": last_progress.thoi_gian_xem,
    }
