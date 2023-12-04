from source.announcements_service import views



from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from source.announcements_service import views
from rest_framework.routers import DefaultRouter,SimpleRouter

router = DefaultRouter()
router.register(r'announcements',views.AnnouncementsModelViewSet)

urlpatterns = [
    path('',include(router.urls)),
]