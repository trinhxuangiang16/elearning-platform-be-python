from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.models import Course, Section, Lesson
from core.algorithms.search_engine import search_engine_instance
from core.algorithms.course_recommender import course_recommender_instance


def refresh_algorithms_cache():
    search_engine_instance.rebuild_from_db()
    course_recommender_instance.rebuild_from_db()


@receiver(post_save, sender=Course)
@receiver(post_delete, sender=Course)
@receiver(post_save, sender=Section)
@receiver(post_delete, sender=Section)
@receiver(post_save, sender=Lesson)
@receiver(post_delete, sender=Lesson)
def handle_catalog_change(sender, **kwargs):
    refresh_algorithms_cache()

