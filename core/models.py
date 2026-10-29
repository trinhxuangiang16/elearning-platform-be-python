from django.db import models


class User(models.Model):
    tai_khoan = models.CharField(max_length=50, primary_key=True, db_column="tai_khoan")
    mat_khau = models.CharField(max_length=255, db_column="mat_khau")
    ho_ten = models.CharField(max_length=100, db_column="ho_ten")
    email = models.CharField(max_length=100, unique=True, db_column="email")
    so_dt = models.CharField(max_length=20, default="", db_column="so_dt")
    ma_loai_nguoi_dung = models.CharField(max_length=10, default="HV", db_column="ma_loai_nguoi_dung")
    ma_nhom = models.CharField(max_length=20, default="GP01", db_column="ma_nhom")
    status = models.BooleanField(default=True, db_column="status")
    avatar = models.CharField(max_length=500, null=True, blank=True, db_column="avatar")
    bio = models.TextField(null=True, blank=True, db_column="bio")
    unlocked_courses = models.CharField(max_length=2000, default="", blank=True, db_column="unlocked_courses")
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")
    updated_at = models.DateTimeField(auto_now=True, db_column="updated_at")

    @property
    def is_authenticated(self):
        return True

    class Meta:
        db_table = "NguoiDung"
        managed = False


class Category(models.Model):
    ma_danh_muc = models.CharField(max_length=50, primary_key=True, db_column="ma_danh_muc")
    ten_danh_muc = models.CharField(max_length=100, db_column="ten_danh_muc")
    icon = models.CharField(max_length=255, null=True, blank=True, db_column="icon")
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")

    class Meta:
        db_table = "DanhMucKhoaHoc"
        managed = False


class Course(models.Model):
    ma_khoa_hoc = models.CharField(max_length=50, primary_key=True, db_column="ma_khoa_hoc")
    ten_khoa_hoc = models.CharField(max_length=255, db_column="ten_khoa_hoc")
    bi_anh = models.CharField(max_length=255, null=True, blank=True, db_column="bi_anh")
    mo_ta = models.TextField(null=True, blank=True, db_column="mo_ta")
    luot_xem = models.IntegerField(default=0, db_column="luot_xem")
    danh_gia = models.FloatField(default=5.0, db_column="danh_gia")
    hinh_anh = models.CharField(max_length=500, null=True, blank=True, db_column="hinh_anh")
    ma_nhom = models.CharField(max_length=20, default="GP01", db_column="ma_nhom")
    ngay_tao = models.DateTimeField(auto_now_add=True, db_column="ngay_tao")
    cap_do = models.CharField(max_length=50, default="CoBan", db_column="cap_do")
    thoi_luong_gio = models.IntegerField(default=0, db_column="thoi_luong_gio")
    trang_thai = models.BooleanField(default=True, db_column="trang_thai")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        db_column="ma_danh_muc",
        related_name="courses",
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="tai_khoan_tao",
        related_name="courses_created",
    )

    class Meta:
        db_table = "KhoaHoc"
        managed = False


class Enrollment(models.Model):
    id = models.AutoField(primary_key=True, db_column="id")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="tai_khoan",
        related_name="enrollments",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        db_column="ma_khoa_hoc",
        related_name="enrollments",
    )
    ngay_ghi_danh = models.DateTimeField(auto_now_add=True, db_column="ngay_ghi_danh")
    trang_thai = models.BooleanField(default=True, db_column="trang_thai")

    class Meta:
        db_table = "GhiDanhKhoaHoc"
        managed = False
        unique_together = (("user", "course"),)


class Section(models.Model):
    ma_chuong = models.AutoField(primary_key=True, db_column="ma_chuong")
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        db_column="ma_khoa_hoc",
        related_name="sections",
    )
    ten_chuong = models.CharField(max_length=255, db_column="ten_chuong")
    thu_tu = models.IntegerField(default=1, db_column="thu_tu")
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")

    class Meta:
        db_table = "ChuongHoc"
        managed = False


class Lesson(models.Model):
    ma_bai_hoc = models.AutoField(primary_key=True, db_column="ma_bai_hoc")
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        db_column="ma_chuong",
        related_name="lessons",
    )
    ten_bai_hoc = models.CharField(max_length=255, db_column="ten_bai_hoc")
    loai_bai_hoc = models.CharField(max_length=20, default="VIDEO", db_column="loai_bai_hoc")
    url_video = models.CharField(max_length=500, null=True, blank=True, db_column="url_video")
    noi_dung_text = models.TextField(null=True, blank=True, db_column="noi_dung_text")
    thoi_luong_giay = models.IntegerField(default=0, db_column="thoi_luong_giay")
    thu_tu = models.IntegerField(default=1, db_column="thu_tu")
    is_preview = models.BooleanField(default=False, db_column="is_preview")
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")

    class Meta:
        db_table = "BaiHoc"
        managed = False


class LessonProgress(models.Model):
    id = models.AutoField(primary_key=True, db_column="id")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="tai_khoan",
        related_name="lesson_progresses",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        db_column="ma_bai_hoc",
        related_name="progresses",
    )
    da_hoan_thanh = models.BooleanField(default=False, db_column="da_hoan_thanh")
    thoi_gian_xem = models.IntegerField(default=0, db_column="thoi_gian_xem")
    watched_intervals = models.JSONField(null=True, blank=True, db_column="watched_intervals")
    actual_watched_seconds = models.IntegerField(default=0, db_column="actual_watched_seconds")
    last_ping_at = models.DateTimeField(null=True, blank=True, db_column="last_ping_at")
    updated_at = models.DateTimeField(auto_now=True, db_column="updated_at")

    class Meta:
        db_table = "TienDoBaiHoc"
        managed = False
        unique_together = (("user", "lesson"),)


class Assignment(models.Model):
    ma_bai_tap = models.AutoField(primary_key=True, db_column="ma_bai_tap")
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        db_column="ma_bai_hoc",
        related_name="assignments",
    )
    tieu_de = models.CharField(max_length=255, db_column="tieu_de")
    de_bai_mo_ta = models.TextField(db_column="de_bai_mo_ta")
    han_nop = models.DateTimeField(null=True, blank=True, db_column="han_nop")
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")

    class Meta:
        db_table = "BaiTap"
        managed = False


class AssignmentSubmission(models.Model):
    ma_luot_nop = models.AutoField(primary_key=True, db_column="ma_luot_nop")
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        db_column="ma_bai_tap",
        related_name="submissions",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="tai_khoan",
        related_name="submissions",
    )
    link_nop_bai = models.CharField(max_length=1000, db_column="link_nop_bai")
    ghi_chu_student = models.TextField(null=True, blank=True, db_column="ghi_chu_student")
    diem_so = models.FloatField(null=True, blank=True, db_column="diem_so")
    nhan_xet_gv = models.TextField(null=True, blank=True, db_column="nhan_xet_gv")
    trang_thai = models.CharField(max_length=20, default="CHUA_CHAM", db_column="trang_thai")
    ngay_nop = models.DateTimeField(auto_now_add=True, db_column="ngay_nop")
    updated_at = models.DateTimeField(auto_now=True, db_column="updated_at")

    class Meta:
        db_table = "NopBaiTap"
        managed = False
        unique_together = (("assignment", "user"),)


class LessonNote(models.Model):
    ma_ghi_chu = models.AutoField(primary_key=True, db_column="ma_ghi_chu")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="tai_khoan",
        related_name="notes",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        db_column="ma_bai_hoc",
        related_name="notes",
    )
    timestamp = models.IntegerField(default=0, db_column="timestamp")
    noi_dung = models.TextField(db_column="noi_dung")
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")

    class Meta:
        db_table = "GhiChuBaiHoc"
        managed = False
