from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from source.club_service import views
from rest_framework.routers import DefaultRouter,SimpleRouter

router = DefaultRouter()
router.register(r'clubs',views.ClubViewSet,basename='clubs')
router.register(r'club-posts', views.ClubPostViewSet, basename='club-post')

urlpatterns = [
    # path('clubs/',views.ClubsListView.as_view(),name = 'clubs-list'),
    # path('clubs/<slug:slug>/',views.ClubDetailsView.as_view(),name='club-details'),
    path('',include(router.urls)),

]
