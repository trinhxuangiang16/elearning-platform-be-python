from django.db.models import Count, Q
from core.models import User, Course, Enrollment, Lesson, LessonProgress, AssignmentSubmission


def get_quick_stats():
    user_agg = User.objects.aggregate(
        total_students=Count("tai_khoan", filter=Q(ma_loai_nguoi_dung="HV")),
        total_instructors=Count("tai_khoan", filter=Q(ma_loai_nguoi_dung__in=["GV", "GVU"])),
    )
    total_courses = Course.objects.count()
    total_lessons = Lesson.objects.count()
    total_enrollments = Enrollment.objects.filter(trang_thai=True).count()
    pending_submissions = AssignmentSubmission.objects.filter(trang_thai="CHUA_CHAM").count()

    progress_agg = LessonProgress.objects.aggregate(
        total_progress=Count("id"),
        completed_progress=Count("id", filter=Q(da_hoan_thanh=True)),
    )
    total_prog = progress_agg["total_progress"] or 0
    comp_prog = progress_agg["completed_progress"] or 0

    if total_prog > 0:
        avg_completion_rate = round((comp_prog / total_prog) * 100.0, 1)
    else:
        avg_completion_rate = 0

    return {
        "totalStudents": user_agg["total_students"] or 0,
        "totalInstructors": user_agg["total_instructors"] or 0,
        "totalCourses": total_courses,
        "totalLessons": total_lessons,
        "totalEnrollments": total_enrollments,
        "avgPlatformCompletionRate": avg_completion_rate,
        "pendingSubmissionsCount": pending_submissions,
    }


def get_top_students():
    top_progress = (
        LessonProgress.objects.filter(da_hoan_thanh=True)
        .values("user_id")
        .annotate(completed_count=Count("lesson_id"))
        .order_by("-completed_count")[:10]
    )

    student_ids = [row["user_id"] for row in top_progress]
    users = User.objects.filter(tai_khoan__in=student_ids)
    user_map = {u.tai_khoan: u for u in users}

    result = []
    for row in top_progress:
        uid = row["user_id"]
        u = user_map.get(uid)
        result.append({
            "taiKhoan": uid,
            "hoTen": u.ho_ten if u else uid,
            "email": u.email if u else "",
            "completedLessonsCount": row["completed_count"],
        })
    return result
