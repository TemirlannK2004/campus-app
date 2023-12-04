from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from source.announcements_service import models
from source.announcements_service import serializers
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
# Create your views here.

class AnnouncementsModelViewSet(viewsets.ModelViewSet):
    queryset = models.UniversityAnnouncement.objects.prefetch_related('announcementimage_set').order_by('-created_at')
    serializer_class = serializers.AnnouncementsSerializer

