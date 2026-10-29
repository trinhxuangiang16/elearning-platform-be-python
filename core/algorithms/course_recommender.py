from datetime import datetime
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.algorithms.search_engine import normalize_vietnamese_text


LEVEL_ORDER = {
    "CoBan": 1,
    "TrungCap": 2,
    "NangCao": 3,
}


class PersonalizedCourseRecommender:
    def __init__(self):
        self.similarity_cache = {}
        self.course_meta = {}
        self.is_built = False

    def build_cache(self, courses_list):
        self.similarity_cache = {}
        self.course_meta = {}

        if not courses_list:
            self.is_built = True
            return

        course_ids = []
        corpus = []

        for item in courses_list:
            cid = item["ma_khoa_hoc"]
            course_ids.append(cid)
            self.course_meta[cid] = {
                "cap_do": item.get("cap_do", "CoBan"),
                "ma_danh_muc": item.get("ma_danh_muc", ""),
            }

            raw_features = " ".join([
                str(item.get("ten_khoa_hoc", "")) * 3,
                str(item.get("ma_danh_muc", "")) * 3,
                str(item.get("ten_danh_muc", "")) * 2,
                str(item.get("mo_ta", "")),
                str(item.get("sections_text", "")),
                str(item.get("lessons_text", "")),
            ])
            corpus.append(normalize_vietnamese_text(raw_features))

        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(corpus)
        sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

        count = len(course_ids)
        for i in range(count):
            cid_i = course_ids[i]
            self.similarity_cache[cid_i] = {}
            for j in range(count):
                cid_j = course_ids[j]
                if i == j:
                    self.similarity_cache[cid_i][cid_j] = 1.0
                else:
                    self.similarity_cache[cid_i][cid_j] = float(sim_matrix[i, j])

        self.is_built = True

    def rebuild_from_db(self):
        from core.models import Course
        courses = Course.objects.select_related("category").prefetch_related("sections__lessons").all()
        courses_list = []
        for c in courses:
            sec_titles = []
            les_titles = []
            for sec in c.sections.all():
                sec_titles.append(sec.ten_chuong)
                for les in sec.lessons.all():
                    les_titles.append(les.ten_bai_hoc)
            courses_list.append({
                "ma_khoa_hoc": c.ma_khoa_hoc,
                "ten_khoa_hoc": c.ten_khoa_hoc,
                "mo_ta": c.mo_ta or "",
                "cap_do": c.cap_do or "CoBan",
                "ma_danh_muc": c.category_id or "",
                "ten_danh_muc": c.category.ten_danh_muc if c.category else "",
                "sections_text": " ".join(sec_titles),
                "lessons_text": " ".join(les_titles),
            })
        self.build_cache(courses_list)

    def ensure_built(self):
        if not self.is_built:
            self.rebuild_from_db()

    def get_user_learning_profile(self, user):
        from core.models import Enrollment, Lesson, LessonProgress, AssignmentSubmission

        enrolled_ids = set(
            Enrollment.objects.filter(user_id=user.tai_khoan, trang_thai=True).values_list("course_id", flat=True)
        )
        unlocked_str = getattr(user, "unlocked_courses", "") or ""
        for code in unlocked_str.split(","):
            cleaned = code.strip()
            if cleaned:
                enrolled_ids.add(cleaned)

        completed_progresses = LessonProgress.objects.filter(
            user_id=user.tai_khoan, da_hoan_thanh=True
        ).select_related("lesson__section")

        completed_by_course = defaultdict(int)
        for prog in completed_progresses:
            if prog.lesson and prog.lesson.section:
                cid = prog.lesson.section.course_id
                completed_by_course[cid] += 1
                enrolled_ids.add(cid)

        if not enrolled_ids:
            return {}

        all_lessons = Lesson.objects.filter(section__course_id__in=enrolled_ids).select_related("section")
        total_lessons_by_course = defaultdict(int)
        for les in all_lessons:
            total_lessons_by_course[les.section.course_id] += 1

        graded_subs = AssignmentSubmission.objects.filter(
            user_id=user.tai_khoan,
            trang_thai="DA_CHAM",
            diem_so__isnull=False,
        ).select_related("assignment__lesson__section")

        scores_by_course = defaultdict(list)
        for sub in graded_subs:
            if sub.assignment and sub.assignment.lesson and sub.assignment.lesson.section:
                cid = sub.assignment.lesson.section.course_id
                scores_by_course[cid].append(float(sub.diem_so))

        profile = {}
        for cid in enrolled_ids:
            total_les = total_lessons_by_course.get(cid, 0)
            comp_les = completed_by_course.get(cid, 0)
            completion_ratio = (comp_les / total_les) if total_les > 0 else 0.0
            course_scores = scores_by_course.get(cid, [])
            avg_gpa = (sum(course_scores) / len(course_scores)) if course_scores else 80.0
            interest_weight = 1.0 + 0.5 * completion_ratio + 0.5 * (avg_gpa / 100.0)
            profile[cid] = {
                "completion_ratio": completion_ratio,
                "gpa": avg_gpa,
                "interest_weight": interest_weight,
            }

        return profile

    def rank_courses_for_user(self, courses_queryset, user):
        courses_list = list(courses_queryset)
        if not user or not getattr(user, "is_authenticated", False):
            courses_list.sort(key=lambda c: c.ngay_tao or datetime.min, reverse=True)
            return courses_list

        self.ensure_built()
        user_profile = self.get_user_learning_profile(user)
        if not user_profile:
            courses_list.sort(key=lambda c: c.ngay_tao or datetime.min, reverse=True)
            return courses_list

        enrolled_set = set(user_profile.keys())
        recommendation_scores = {}

        for candidate in courses_list:
            cand_id = candidate.ma_khoa_hoc
            cand_meta = self.course_meta.get(cand_id, {
                "cap_do": candidate.cap_do or "CoBan",
                "ma_danh_muc": candidate.category_id or "",
            })
            cand_level = LEVEL_ORDER.get(cand_meta["cap_do"], 1)
            cand_cat = cand_meta["ma_danh_muc"]

            total_score = 0.0
            for base_id, stats in user_profile.items():
                if base_id == cand_id:
                    continue
                sim = self.similarity_cache.get(base_id, {}).get(cand_id, 0.0)
                base_meta = self.course_meta.get(base_id, {"cap_do": "CoBan", "ma_danh_muc": ""})
                base_level = LEVEL_ORDER.get(base_meta["cap_do"], 1)
                base_cat = base_meta["ma_danh_muc"]

                if base_cat and cand_cat and base_cat == cand_cat:
                    sim += 0.25

                comp_ratio = stats["completion_ratio"]
                if comp_ratio >= 0.5:
                    if cand_level == base_level + 1:
                        level_boost = 1.25
                    else:
                        level_boost = 1.0
                else:
                    if cand_level == base_level:
                        level_boost = 1.15
                    else:
                        level_boost = 1.0

                total_score += stats["interest_weight"] * sim * level_boost

            if cand_id in enrolled_set:
                total_score -= 100.0

            recommendation_scores[cand_id] = total_score

        courses_list.sort(
            key=lambda c: (recommendation_scores.get(c.ma_khoa_hoc, 0.0), c.ngay_tao or datetime.min),
            reverse=True,
        )
        return courses_list


course_recommender_instance = PersonalizedCourseRecommender()

