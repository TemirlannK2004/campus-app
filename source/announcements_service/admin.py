from django.contrib import admin

from source.announcements_service.models import UniversityAnnouncement, AnnouncementImage

admin.site.register(UniversityAnnouncement)
admin.site.register(AnnouncementImage)