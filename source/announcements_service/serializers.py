from rest_framework import serializers
from source.announcements_service import models

class AnnouncementsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnouncementImage
        fields = '__all__'

class AnnouncementsSerializer(serializers.ModelSerializer):
    announcementimage_set = AnnouncementsImageSerializer(many=True)

    class Meta:
        model = models.UniversityAnnouncement
        fields = '__all__'

