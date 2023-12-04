from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from source.announcements_service import models


@shared_task
def delete_old_posts():
    six_months_ago = timezone.now() - timedelta(days=180)
    old_posts = models.UniversityAnnouncement.objects.filter(created_at__lt=six_months_ago)
    old_posts.delete()