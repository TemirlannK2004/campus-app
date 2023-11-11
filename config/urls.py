from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from source.auth_service import views
from source.club_service import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/auth_service/', include('source.auth_service.urls')),
    path('api/v1/club_service/',include('source.club_service.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
