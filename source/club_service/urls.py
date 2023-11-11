from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from source.club_service import views

urlpatterns = [
    path('clubs/',views.AllClubsView.as_view(),name='clubs-list'),

]
