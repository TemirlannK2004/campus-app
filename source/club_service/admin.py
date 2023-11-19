from django.contrib import admin
from source.club_service.models import Club,ClubNews,ClubPost,ClubStaff,ClubHead,ClubMembership

admin.site.register(Club)
admin.site.register(ClubNews)
admin.site.register(ClubPost)
admin.site.register(ClubStaff)
admin.site.register(ClubHead)
admin.site.register(ClubMembership)
