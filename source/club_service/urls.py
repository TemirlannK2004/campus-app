from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from source.club_service import views
from rest_framework.routers import DefaultRouter,SimpleRouter

router = DefaultRouter()
router.register(r'clubs',views.ClubViewSet,basename='clubs')
router.register(r'club-posts', views.ClubPostViewSet, basename='club-post')

urlpatterns = [
    path('clubs/<slug:slug>/news/',views.ClubNewsAPI.as_view(),name='club-news'),
    path('',include(router.urls)),

]
