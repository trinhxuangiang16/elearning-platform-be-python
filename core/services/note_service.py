from datetime import datetime
from core.models import Lesson, LessonNote
from core.exceptions import NotFoundException, ForbiddenException, BadRequestException


def serialize_note(note):
    return {
        "ma_ghi_chu": note.ma_ghi_chu,
        "tai_khoan": note.user_id,
        "ma_bai_hoc": note.lesson_id,
        "timestamp": note.timestamp,
        "noi_dung": note.noi_dung,
        "created_at": note.created_at.isoformat() if note.created_at else None,
    }


def get_notes_by_lesson(tai_khoan, ma_bai_hoc):
    notes = LessonNote.objects.filter(
        user_id=tai_khoan,
        lesson_id=int(ma_bai_hoc),
    ).order_by("timestamp", "ma_ghi_chu")
    return [serialize_note(n) for n in notes]


def create_note(tai_khoan, ma_bai_hoc, body):
    lesson = Lesson.objects.filter(ma_bai_hoc=int(ma_bai_hoc)).first()
    if not lesson:
        raise NotFoundException("Bài học không tồn tại!")

    noi_dung = body.get("noiDung")
    if not noi_dung or not str(noi_dung).strip():
        raise BadRequestException("Nội dung ghi chú là bắt buộc!")

    timestamp = int(body.get("timestamp") or 0)
    note = LessonNote.objects.create(
        user_id=tai_khoan,
        lesson=lesson,
        timestamp=timestamp,
        noi_dung=noi_dung,
        created_at=datetime.now(),
    )
    return serialize_note(note)


def delete_note(tai_khoan, ma_ghi_chu):
    note = LessonNote.objects.filter(ma_ghi_chu=int(ma_ghi_chu)).first()
    if not note:
        raise NotFoundException("Ghi chú không tồn tại!")

    if note.user_id != tai_khoan:
        raise ForbiddenException("Bạn không có quyền xóa ghi chú này!")

    note.delete()
    return {"success": True}
